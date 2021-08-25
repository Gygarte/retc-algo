
def get_position_info_on_stock(session, stocks):
    position_info = []
    add_info = {}
    #gets each stock from the list
    for stock in stocks:
        spam = []
        #gets stock info fron the API
        info_response = session.get('http://localhost:9999/v1/securities', params={'ticker':stock})
        if info_response.status_code == 200:
            #parse the HTML response
            info_parse = info_response.json()[0]
            #adds the position to a list and dictionary for logs
            position_info.append(info_parse['position'])
            add_info.update({stock : info_parse['position']})
    return position_info

def send_orders(session, action, ticker):
    #place an order for said ticker and said action
    response = session.post('http://localhost:9999/v1/orders',
                            params= {'ticker':ticker, 'type':'MARKET', 'quantity':1000, 'action':action})
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

def close_all(session):
    stock_list = ['BEAR', 'BULL', 'RETC', 'USD']
    #takes the current positions
    positions = get_position_info_on_stock(session, stock_list)
    if check_if_any_open_position(positions) is not True:
        return "All positions closed!"
    log = []
    #takes a stock
    for stock in stock_list:
        #find the current position we have
        if positions[stock_list.index(stock)] > 0:
            #how many time to send the order
            turns = int(positions[stock_list.index(stock)] / 5000)
            for times in range(turns):
                #append the log list
                log.append(send_orders(session,'SELL', stock))
        else:
            #how many time to send the order
            turns = int(positions[stock_list.index(stock)] / 5000)
            for times in range(turns):
                #append the log list
                log.append(send_orders(session,'BUY', stock))
    return log

#cantitati diferite pentru valute