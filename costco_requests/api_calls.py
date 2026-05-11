import os
import re
import sys
import json
import tls_client
import requests
import logging as logger
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import save_snapshot

# Variables 
logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logger.getLogger(__name__)


class api_calls:

    SEARCH_API_URL = "https://search.costco.ca/api/apps/www_costco_ca/query/www_costco_ca_search"
    SEARCH_API_KEY = "134a4023-68d5-4138-8e03-8353667d5fb3"

    _KEY_PATTERNS = (
        r'x-api-key["\']?\s*[:=]\s*["\']([0-9a-fA-F-]{36})["\']',
        r'apiKey["\']?\s*[:=]\s*["\']([0-9a-fA-F-]{36})["\']',
        r'searchApiKey["\']?\s*[:=]\s*["\']([0-9a-fA-F-]{36})["\']',
    )

    @classmethod
    def _refresh_api_key(cls):
        try:
            resp = requests.get(
                "https://www.costco.ca/",
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml',
                    'Accept-Language': 'en-US,en;q=0.9',
                },
                timeout=15,
            )
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch costco.ca for key refresh: {e}")
            return False
        for pat in cls._KEY_PATTERNS:
            m = re.search(pat, resp.text)
            if m and m.group(1) != cls.SEARCH_API_KEY:
                logger.info(f"Refreshed SEARCH_API_KEY (pattern: {pat[:20]}...)")
                cls.SEARCH_API_KEY = m.group(1)
                return True
        logger.error("Could not locate search API key in costco.ca HTML")
        return False

    @classmethod
    def _search_request(cls, query):
        return requests.get(
            cls.SEARCH_API_URL,
            params={
                'expoption': 'def',
                'q': query,
                'locale': 'en-CA',
                'start': '0',
                'expand': 'false',
                'loc': '*',
                'rows': '5',
            },
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'x-api-key': cls.SEARCH_API_KEY,
            },
            timeout=15,
        )

    @classmethod
    def _search_price(cls, productId: str, itemID: str):
        for query in (productId, itemID):
            try:
                response = cls._search_request(query)
                if response.status_code in (401, 403) and cls._refresh_api_key():
                    response = cls._search_request(query)
                response.raise_for_status()
                docs = response.json().get('response', {}).get('docs', [])
            except Exception as err:
                logger.error(f"Search API fallback failed for query {query}: {err}")
                continue

            for doc in docs:
                if str(doc.get('group_id')) != str(productId) and str(doc.get('item_number')) != str(itemID):
                    continue
                price = doc.get('item_location_pricing_salePrice')
                if price is None:
                    continue
                result = {
                    'finalOnlinePrice': price,
                    'productId': [str(doc.get('group_id') or productId)],
                    'itemId': str(doc.get('item_number') or itemID),
                    'discount': doc.get('item_location_pricing_discountAmount_f', 0) or 0,
                    'productName': doc.get('item_product_name', ''),
                    'source': 'search.costco.ca',
                }
                text = json.dumps(result, indent=2)
                logger.info(f"Search API fallback price for product ID: {productId} is {text}")
                print(text)
                save_snapshot(
                    item_id=result['itemId'],
                    product_id=result['productId'],
                    name=result['productName'],
                    price=result['finalOnlinePrice'],
                    discount=result['discount'],
                    source='search.costco.ca/fallback',
                )
                return text
        return None

    @staticmethod
    def _save_price_text(productId: str, itemID: str, text: str, source: str) -> None:
        try:
            data = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return
        if not isinstance(data, dict):
            return
        price = (
            data.get('finalOnlinePrice')
            or data.get('price')
            or data.get('salePrice')
        )
        discount = data.get('discount') or data.get('discountAmount') or 0
        save_snapshot(
            item_id=itemID,
            product_id=productId,
            price=price,
            discount=discount,
            source=source,
        )

    def get_price(productId: str, itemID: str):
        proxy = os.getenv("COSTCO_PROXY")
        proxies = {"http": proxy, "https": proxy} if proxy else None
        price_api = f"https://www.costco.ca/AjaxGetContractPrice?itemId={itemID}&productId={productId}"
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.costco.ca/',
            'Connection': 'keep-alive'
        }
        cookies = {
            'invCheckPostalCode': 'M1T%203C4',
            'invCheckCity': 'Scarborough'
        }
        try:
            fallback = requests.get(price_api, cookies=cookies, headers=headers, proxies=proxies, timeout=15)
            fallback.raise_for_status()
            logger.info(f"Price for product ID: {productId} is {fallback.text}")
            print(fallback.text)
            api_calls._save_price_text(productId, itemID, fallback.text, 'AjaxGetContractPrice/requests')
            return fallback.text
        except Exception as e:
            logger.error(f"Requests price endpoint failed: {e}")

        try:
            session = tls_client.Session(
                client_identifier="chrome_112",
                random_tls_extension_order=True,
                force_http1=True,
            )
            response = session.get(
                price_api,
                cookies=cookies,
                headers=headers,
                proxy=proxy if proxy else None,
                timeout_seconds=15,
            )
            if response.status_code != 200:
                raise RuntimeError(f"Costco returned HTTP {response.status_code}: {response.text[:200]}")
            print(response.text)
            logger.info(f"Price for product ID: {productId} is {response.text}")
            print(price_api)
            api_calls._save_price_text(productId, itemID, response.text, 'AjaxGetContractPrice/tls_client')
            time.sleep(random.randint(1, 5))
            return response.text
        except Exception as e:
            logger.error(f"TLS client price endpoint failed: {e}")

        return api_calls._search_price(productId, itemID)
            
            
