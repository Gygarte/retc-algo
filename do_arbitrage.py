
def get_stock_info(session, stocks):
    info = []
    add_info = {}
    for stock in stocks:
        spam = []
        info_response = session.get('http://localhost:9999/v1/securities', params={'ticker':stock})
        if info_response.status_code == 200:
            info_parse = info_response.json()[0]
            for index in ['ask', 'bid']:
                spam.append(info_parse[index])
                info.append(info_parse[index])
            add_info.update({stock : spam})
    return tuple(info)

def parse_stock_info(stocks):
    bear_ask = stocks[0]
    bear_bid = stocks[1]
    bull_ask = stocks[2]
    bull_bid = stocks[3]
    retc_ask = stocks[4]
    retc_bid = stocks[5]
    usd_ask = stocks[6]
    usd_bid = stocks[7]
    return bear_ask, bear_bid, bull_ask, bull_bid, retc_ask, retc_bid, usd_ask, usd_bid

def first_condition(bear_ask, bull_ask, usd_bid, retc_bid):
    return True if ((retc_bid - 0.12) * usd_bid > bear_ask + bull_ask) else False

def second_condition(bear_bid,bull_bid,usd_ask,retc_ask):
    return True if ((retc_ask + 0.12) < (bear_bid + bull_bid) * usd_ask)  else False

def first_close_condition(bear_ask, bull_ask, usd_bid, retc_bid):
    return True if ((retc_bid - 0.06) * usd_bid == bear_ask + bull_ask) else False

def second_close_condition(bear_bid,bull_bid,usd_ask,retc_ask):
    return True if ((retc_ask + 0.06) == (bear_bid + bull_bid) * usd_ask)  else False


def cash_flow(quant, prices, operation):
    total = 0
    if operation == 'BUY':
        for quantity, price in zip(quant, prices):
            total = quantity * price
        return -1 * total
    else:
        for quantity, price in zip(quant, prices):
            total = quantity * price
        return total
    
def order_info(order_response):
    quantity = []
    prices = []
    order_info = order_response.json()
    quantity.append(order_info['quantity'])
    prices.append(order_info['vwap'])
    return quantity, prices
    
    
#main function for arbitrage handling
def do_arbitrage(session):
    #stock list to work with
    stock_list = ['BEAR', 'BULL', 'RETC', 'USD']
    #accept the data
    bear_ask, bear_bid, bull_ask, bull_bid, retc_ask, retc_bid, usd_ask, usd_bid  = parse_stock_info(get_stock_info(session, stock_list))
    
    #verify the conditions and execute trades
    if first_condition(bear_ask,bull_ask, usd_bid, retc_bid):
        #open positions
        response_open_short_retc = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'RETC', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
        quantity, price = order_info(response_open_short_retc)
        print(cash_flow(quantity, price, 'SELL'))
        response_open_long_bull = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BULL', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
        response_open_long_bear = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BEAR', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
        response_open_long_usd = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'USD', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
        if first_close_condition(bear_ask, bull_ask, usd_bid, retc_bid):
            #close positions
            response_close_short_retc = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'RETC', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
            response_close_long_bull = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'BULL', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
            response_close_long_bear = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'BEAR', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
            response_close_long_usd = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'USD', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
        
        print('Arbitraje on the first rule!')
        
    elif second_condition(bear_bid,bull_bid,usd_ask,retc_ask):
        #open positions because of the atbitrage
        response_open_short_retc = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'RETC', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
        response_open_long_bull = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BULL', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
        response_open_long_bear = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BEAR', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
        response_open_long_usd = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'USD', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
        if second_close_condition(bear_bid,bull_bid,usd_ask,retc_ask):
            #close positions because of the arbitrage
            response_close_short_retc = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'RETC', 'type':'MARKET', 'quantity':1000, 'action':'SELL'})
            response_close_long_bull = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'BULL', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
            response_close_long_bear = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'BEAR', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
            response_close_long_usd = session.post('http://localhost:9999/v1/orders',
                                params={'ticker':'USD', 'type':'MARKET', 'quantity':1000, 'action':'BUY'})
        
        print('Arbitrage on the second rule!')
    else:
        print("No arbitrage, yet!")