
def get_stock_info():
    pass

def first_condition(bear_ask, bull_ask, usd_ask, retc_bid):
    return True if (retc_bid < (bear_ask + bull_ask) * usd_ask) else False


def second_condition(bear_bid,bull_bid,usd_bid,retc_ask):
    return True if (retc_ask > (bear_bid + bull_bid) * usd_bid) else False



#main function for arbitrage handling
def do_arbitrage(session):
    #accept the data
    bear_ask, bear_bid, bull_ask, bull_bid, usd_ask, usd_bid,retc_ask, retc_bid = get_stock_info()
    
    #verify the conditions and execute trades
    if first_condition() is False:
        #open positions because of the atbitrage
        response_open_short_retc = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'RETC', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        response_open_long_bull = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BULL', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        response_open_long_bear = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BEAR', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        response_open_long_usd = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'USD', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        #close positions because of the arbitrage
        response_close_short_retc = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'RETC', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        response_close_long_bull = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BULL', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        response_close_long_bear = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BEAR', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        response_close_long_usd = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'USD', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        print('Arbitraje on the first rule!')
        
    elif second_condition() is False:
        #open positions because of the atbitrage
        response_open_short_retc = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'RETC', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        response_open_long_bull = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BULL', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        response_open_long_bear = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BEAR', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        response_open_long_usd = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'USD', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        #close positions because of the arbitrage
        response_close_short_retc = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'RETC', 'type':'MARKET', 'quantity':9999, 'action':'SELL'})
        response_close_long_bull = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BULL', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        response_close_long_bear = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'BEAR', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        response_close_long_usd = session.post('http://localhost:9999/v1/orders',
                            params={'ticker':'USD', 'type':'MARKET', 'quantity':9999, 'action':'BUY'})
        print('Arbitrage on the second rule!')
    else:
        print("No arbitrage, yet!")



