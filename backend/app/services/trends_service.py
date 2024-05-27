from pytrends.request import TrendReq
import time

class TrendsService:
    @staticmethod
    def get_trends_interest(sector):
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [sector]
        pytrends.build_payload(kw_list, cat=0, timeframe='now 1-H', geo='', gprop='')
        trends_data = pytrends.interest_over_time()
        
        if trends_data.empty:
            return 0
        
        interest = trends_data[sector].iloc[-1]
        return interest
