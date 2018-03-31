import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def read_data(fname):
    df = pd.read_csv(fname,header=None)
    #preprocess
    df.columns = ['date','price']
    df.set_index('date',inplace = True)
    df['return'] = (df['price']/df['price'].shift(1)) -1
    #df.index = [datetime.strptime(temp_date, '%Y-%m-%d').tz_localize('UTC').tz_convert('US/Pacific') for temp_date in df.index.values]
    df.index = pd.to_datetime(df.index)
    return df

def determine_positions(price_data):
    '''set postion to either long (1) or flat (0) '''
    positions = pd.DataFrame()
    start = 0
    dates = price_data.index.values
    for i in range(10,len(price_data.index.values)):
        if price_data['price'].iloc[i] > price_data['price'].iloc[i-10]:
            positions.loc[dates[i],'position'] = 1
        else:
            positions.loc[dates[i],'position'] = 0
            
    return positions
    
    
def backtest(positions, price_data):
    #total standard return
    value = 100
    base_Nav = pd.DataFrame()
    first_day = positions.index.values[0]
    last_day = positions.index.values[-1]
    total_return = (price_data.loc[last_day,'price']/price_data.loc[first_day,'price'])-1
    print(total_return)
    print(price_data)
    temp_price_data= price_data.iloc[9::]
    print('here')
    #################iloc causing the problems
    for day in range(0,len(positions.index.values)-1):
        #update value 
        value = value + temp_price_data['return'].iloc[day]*value
        base_Nav.loc[positions.index.values[day+1],'level'] = value
        
    return base_Nav
    
def backtest_positions(positions,price_data):
    value = 100
    Nav = pd.DataFrame()
    temp_price_data = price_data.iloc[9::]
    for day in range(0,len(positions.index.values)-2):
        #update value 
        value = value + positions['position'].iloc[day]*temp_price_data['return'].iloc[day+1]*value
        Nav.loc[positions.index.values[day],'level'] = value
    total_return = value/100-1
    print(total_return)
    return Nav

def compare_results(base_Nav,Nav):
    plt.plot(Nav.index, Nav.level,base_Nav.index, base_Nav.level)
    plt.show()    
    return

if __name__ == '__main__':
    fname = "BitcoinPrice.csv"
    price_data = read_data(fname)
    print('Starting...')
    positions=determine_positions(price_data)
    base_Nav = backtest(positions,price_data)
    #Nav = backtest_positions(positions,price_data)
    #compare_results(base_Nav,Nav)
    