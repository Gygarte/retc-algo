
def get_position_info_on_stock(session, stocks):
    #gets stock info fron the API
    info_response = session.get('http://localhost:9999/v1/securities', params={'ticker':stocks})
    if info_response.status_code == 200:
        #parse the HTML response
        info_parse = info_response.json()[0]
        return info_parse['position']


def send_orders(session, action, ticker, units):
    if units == 0:
        return 'No order placed on {}, beacause quantity is {}'.format(ticker, units)
    #place an order for said ticker and said action
    response = session.post('http://localhost:9999/v1/orders',
                            params= {'ticker':ticker, 'type':'MARKET', 'quantity':units, 'action':action})
    #check the response
    if response.status_code == 200:
        response_info = response.json()
        #return ticker and sell price
        return tuple((ticker, response_info['vwap']))

def check_if_any_open_position(positions):
    memo = 0
    for index in positions:
        if index == 0:
            memo += 1
    return True if memo != len(positions) else False

def close_log(log):
    try:
        with open('./close_log.txt', 'w') as clog:
            clog.write(log)
        return True
    except:
        return False


def close_all(session):
    stock_list = ['BEAR', 'BULL', 'RETC',]
    log = []
    UNITS = 5000
    #takes a stock
    for stock in stock_list:
        #find the current position we have
        positions = get_position_info_on_stock(session, stock) 
        #print('Stock: {} at: {}'.format(stock, positions))
        if positions > 0:
            #place orders while the positions are greatear than order volume
            while abs(positions) >= UNITS:
                send_orders(session, 'SELL', stock, UNITS)
                print("For {}, pos {}".format(stock, positions))
                positions -= UNITS
            #liquidate the remained position
            send_orders(session, 'SELL', stock, abs(positions))
            print("For {}, pos {}".format(stock, positions))
        elif positions < 0:
            #place orders while the positions are greatear than order volume
            while abs(positions) >= UNITS:
                send_orders(session, 'BUY', stock, UNITS)
                print("For {}, pos {}".format(stock, positions))
                positions += UNITS
            #liquidate the remained position
            send_orders(session, 'BUY', stock, abs(positions))
            print("For {}, pos {}".format(stock, positions))
        else:
            return 0

#cantitati diferite pentru valute