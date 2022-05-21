from datetime import datetime
import pandas as pd

def market_structure(init, symbol, data, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d, downprice, upprice):
    ms_buy = ms_buy
    ms_sell = ms_sell

    ms_trend = ms_trend
    c_buy = c_buy
    c_sell = c_sell

    wave_count_up = wave_count_up
    wave_count_down = wave_count_down
    wave_count_up_after_d = wave_count_up_after_d
    wave_count_down_after_d = wave_count_down_after_d

    last_a_price_after_d = last_a_price_after_d

    downprice = downprice
    upprice = upprice

    for index, row in data.iterrows():
        if init == True and index == 0:
            upper = row['High']
            lower = row['Low']
            laststate = 1 if row['Close'] > row['Open'] else 0

            a_up = row['Close']
            b_up = row['Close']
            c_up = row['Close']
            d_up = row['Close']

            a_down = row['Close']
            b_down = row['Close']
            c_down = row['Close']
            d_down = row['Close']

            downprice = row['Low']
            upprice = row['High']

        isUptrend = True if (row['High'] > upper and row['Close'] > upper and row['Close'] >= row['Open']) or (row['Close'] > upper and row['Close'] < row['Open']) else False
        isDowntrend = True if (row['Low'] < lower and row['Close'] < lower and row['Close'] <= row['Open']) or (row['Close'] < lower and row['Close'] > row['Open']) else False
        
        if laststate == 0 and isUptrend:
            upper = row['High']
            lower = row['Low']

            if wave_count_up == 0:
                a_up = downprice
                wave_count_up += 1

                if ms_trend == 1:
                    last_a_price_after_d = a_up
                    wave_count_up_after_d += 1

            if wave_count_up == 2 and row['Close'] > a_up:
                if row['Low'] < downprice:
                    c_up = row['Low']
                    a_up = row['Low']
                else:
                    c_up = downprice
                    a_up = downprice
                
                wave_count_up = 1
                ms_buy = True
            
            if wave_count_down == 1:
                b_down = downprice
                wave_count_down += 1

        if laststate == 1 and isDowntrend:
            upper = row['High']
            lower = row['Low']

            if wave_count_down == 0:
                a_down = upprice
                wave_count_down += 1

                if ms_trend == 0:
                    last_a_price_after_d = a_down
                    wave_count_down_after_d += 1

            if wave_count_down == 2 and row['Close'] < a_down:
                if row['High'] > upprice:
                    c_down = row['High']
                    a_down = row['High']
                else:
                    c_down = upprice
                    a_down = upprice
                
                wave_count_down = 1
                ms_sell = True

            if wave_count_up == 1:
                b_up = upprice
                wave_count_up += 1

        if isUptrend:
            upper = row['High']
            lower = row['Low']
            upprice = row['High']
            laststate = 1

        if isDowntrend:
            upper = row['High']
            lower = row['Low']
            downprice = row['Low']
            laststate = 0

        if laststate == 1:
            if row['High'] > upper:
                upprice = row['High']

        if laststate == 0:
            if row['Low'] < lower:
                downprice = row['Low']

        if isUptrend == False and isDowntrend == False:
            upper = row['High'] if row['High'] > upper else upper
            lower = row['Low'] if row['Low'] < lower else lower

        if row['Close'] > b_up and ms_buy == True:
            wave_count_down = 0
            wave_count_down_after_d = 0
            ms_buy = False
            ms_trend = 0
            c_buy = c_up
            temp_candles = []

        if row['Close'] < b_down and ms_sell == True:
            wave_count_up = 0
            wave_count_up_after_d = 0
            ms_sell = False
            ms_trend = 1
            c_sell = c_down
            temp_candles = []

        if row['Close'] < a_up:
            wave_count_up = 0
            b_up = row['High'] + 10000
            ms_buy = False
            if ms_trend == 0:
                ms_trend = 2

        if row['Close'] > a_down:
            wave_count_down = 0
            b_down = row['Low'] - 10000
            ms_sell = False
            if ms_trend == 1:
                ms_trend = 2

    return symbol, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d, downprice, upprice