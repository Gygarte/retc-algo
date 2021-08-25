import requests
import signal
from do_arbitrage import do_arbitrage
from do_arbitrage import parse_stock_info, cash_flow, get_stock_info, order_info
#main class for exceptions
class APIException(Exception):
    pass

# set your API key to authenticate to the RIT client
API_KEY = {'X-API-Key': '8KTHEJQ9'}
shutdown = False

# this signal handler allows for a graceful shutdown when CTRL+C is pressed
def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

# this function gets the tick
def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.status_code == 401:
        raise APIException('The API key provided in this Python code must match that in the RIT client (please refer to the API hyperlink in the client toolbar and/or the RIT – User Guide – REST API Documentation.pdf)')
    case = resp.json()
    return case['tick']

#this is the main function
def main():
    with requests.Session() as session:
        session.headers.update(API_KEY)
        tick = get_tick(session)
        while tick >= 1 and tick <= 299 and not shutdown:
            
        
            #do_arbitrage(session)
            #get_stock_info(session, ['BEAR', 'BULL', 'RETC', 'USD'])
            #update the tick
            stock_list = ['BEAR', 'BULL', 'RETC', 'USD']
            bear_ask, bear_bid, bull_ask, bull_bid, retc_ask, retc_bid, usd_ask, usd_bid  = parse_stock_info(get_stock_info(session, stock_list))
            response_open_short_retc = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'RETC', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
            quantity, price = order_info(response_open_short_retc)
            print(cash_flow(quantity, price, 'SELL'))
            
            
            
            
            
            
            
            
            tick = get_tick(session)


#executor of the main function and signal handler
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
    