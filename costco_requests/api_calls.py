import requests
import json 
import logging as logger
from  get_cookie import get_new_cookie

# Variables 
logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logger.getLogger(__name__)
headers = {
  'Cookie': 'BCO=pm3; _abck=FDECCB8F880EFC1D71BD74BD14116315~-1~YAAQBpYqF+zhcw6TAQAAqinzEQzfMQ2M4qxRynfac/jkSwoqqZg9BvZ1hp998BKqRzKVkEKs7Jtj7OcmpBlHiJPnek+L4bTvKWQipL2RmkcTEYHWF7JLxaNtOU9Ql0vZ/NF5go18ASHFYdly/B4xu/qA8MiXnP/hwqQ/4fd6GRiV0FfP9LNLm3XflZFhgRwGby7MuCKO4Cx8SWoTSBbsucRqWaqWO0cTeAtll62rPXioYEiqnUJtVFeE5kjsQrvgVt0e0G8SW7UShTY9DD2QCNbYYBU7SDXtvA1/18fxEX+/2n9S1dhfRATIRYZZiy0girUCXWoTH2OkA9HJMnhqVorNKoLpy3iJoTB2aJRoGs/wxe5xSY2PKNL8JVL3UIy+usV4fImdr/TdCEoOBvNcs4MR6gd1TVtMqti+OHsyY3gvS20/DeU7~-1~-1~-1; ak_bmsc=792D30DCC8E0C1C791AB7529ADA2AC68~000000000000000000000000000000~YAAQBpYqF+3hcw6TAQAAqinzERmG8exutWP+Q71kuEPs8vAgwbkKDB9pkQrDPFLQHva/w04ZAb5tPtDg5xNd7QRun422Q9jI6jn24Xx++w2PyCz64lGa8K4FQ/2WZgVvDQd+D3vBHGEGPq1OCyrZleHvvCwTyjm3KCcbuXZbdEytQyRaJpvHvuMaEaQ0b4fsZP6UXyRoeZCeKESqvik2rU8clYO1jDztAaJIV75YObDLWsCllYD5imp48zPwBtcQsFfPVxdGx5vCSULE0FsVj1eRAdOR0dFO1pnIGbAw7Z60fWUp8pVHXGSzWh1XzZNhVRnIw6+cBm/qYVZrA6/Mh85/TghO0ElLRg==; bm_sz=68EA53DB5CFDF8C5DCE0F1131D29EA37~YAAQBpYqF+/hcw6TAQAAqinzERneYfIkoVeCfGNufpg5PKKf4Xz9UFg/3Aj7kKrWxuXX4Zi5wr4Rsndp+8Klx0oQClb70fv1FtO+0Kl4a8ebhC0BLDL5nJCGYyt8XsJDuaAAdxsmdhWZP4y45igJq8ZJYTWyeq8KKGJ0LHiUclgh2sKpN33KSY/WmhP2M0VHzLFtFtd56JVwmF+PnYmZUTrhU7kIgAiS+0DPjH5M/VtDLvcRrxwYcVcPJW6Tntx+MhPkz57rsN1SZEpbwvM52p77fZSN71R0b3V05NhjpXqLpTYulVscqb4JddItSxQtQF2ryxOE+m8GTA29a0YCJYL11sBN38f8NnXA~4600627~3556934; JSESSIONID=0000SvPcHjmokQkzw9tXgv5W8kF:1g20uqe83; WAREHOUSEDELIVERY_WHS=%7B%22distributionCenters%22%3A%5B%22559-dz%22%2C%22559-wm%22%2C%22792-wm%22%2C%22894_0-cwt%22%2C%22894_0-edi%22%2C%22894_0-membership%22%2C%22894_0-mpt%22%2C%22894_0-otw%22%2C%22894_0-spc%22%2C%22894_1-edi%22%2C%22894_1-mpt%22%2C%22946-dz%22%2C%22946-wm%22%2C%229894-wcs%22%2C%22993-wm%22%5D%2C%22groceryCenters%22%3A%5B%221436-bd%22%5D%7D; WC_ACTIVEPOINTER=-24%2C10302; WC_AUTHENTICATION_-1002=-1002%2CtMlGzWl0cXkJgxNmSw2bN88J4PwPTaLQto2HrkgAI8Q%3D; WC_GENERIC_ACTIVITYDATA=[41325974330%3Atrue%3Afalse%3A0%3A4KEsU0i6muSwydHoxywaKC4BzT4I3r80m5Ruu3NFiSM%3D][com.ibm.commerce.context.entitlement.EntitlementContext|120950%253B120551%253B120552%253B120769%253B120771%253B120768%253B120773%253B120772%253B120770%253B120774%253B120953%253B120554%253B4000000000000101007%253B120553%253B81323%253B4000000000000001004%26null%26null%26-2000%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|1730991594628-1043936][com.ibm.commerce.context.globalization.GlobalizationContext|-24%26CAD%26-24%26CAD][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.ExternalCartContext|null][com.costco.commerce.member.context.ProfileApiTokenCustomContext|null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null][com.costco.pharmacy.commerce.common.context.PharmacyCustomContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|11201%26null%26false%26false%26false][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10302%26-1002%26-1002%26-1]; WC_PERSISTENT=RFOHvSDwnOHrPQf5AxZ3VwrtIodrO7QQE0upK3FmzqM%3D%3B2024-11-09+09%3A22%3A48.631_1730991594628-1043936_10302_-1002%2C-24%2CCAD%2C4fokp2r6FxJlg9mPxND9hIThu0CRRX4dicXjrY9biL%2BVJF%2Brit2B%2BQPvY8BDXPSJY82D3NpTjs1LNR%2FI4JBzMQ%3D%3D_10302; WC_SESSION_ESTABLISHED=true; WC_USERACTIVITY_-1002=-1002%2C10302%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1149577842%2CLzuvZyPIr3CP%2FxG37UhebejDXa1gmyqeIdTyH%2F69URK3BDCdSybhw8tTehTbvkPgtX6Lq32AnYpYlvNr4aHNl47BvX1mnxk0D8iMgPOV5yz%2BlSILuFrB7bbidqmcD9CDaTMWEaqyH7MbQKI9a00p956IgN9YAI%2BDc4aRl9gk%2Ban50kwyMyd8iY8WYTUx2SZNZphZZvc0kyUaswiBjJyxccD7EhoVunLePijE5yocNBkJbPWYtRAC8gokQ%2BXt88aQ; akaas_AS_CA=2147483647~rv=58~id=21872f23468a502597fa9e57cebfbb39; akavpau_zezxapz5yfca=1731173268~id=55d1ba9d69610e2a4dd338511e7ff0b9; client-zip-short=M3H; invCheckPostalCode=M3H'
}

class api_calls:

    def get_price(itemId: str, productId: str, catalogId: str):
        try: 
            session = requests.Session()
            response = session.get("https://www.costco.ca/")
            price_api = f"https://www.costco.com/AjaxGetInventoryDetail?itemId={itemId}&catalogId={catalogId}&productId={productId}&WH=any"
            response = session.get(price_api)
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.info(f"{e}")
            new_cookie = get_new_cookie().get_cookie()
            headers["Cookie"] = new_cookie

