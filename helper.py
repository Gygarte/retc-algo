import pandas as pd

model = {'BEAR':{'ASK':[],"BID":[]},
         'BULL':{'ASK':[],'BID':[]},
         'RETC':{'ASK':[],'BID':[]},
         'USD':{'ASK':[], 'BID':[]}}

def price_view_helper():
    df = pd.DataFrame