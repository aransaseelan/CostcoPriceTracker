from seleniumbase import SB
from dotenv import load_dotenv

with SB(uc=True) as sb:

    url = "https://basketball.fantasysports.yahoo.com/nba/28160/10"
    sb.uc_open_with_reconnect(url, 4)
    sb.uc_gui_click_captcha()

    # Login to StockX
