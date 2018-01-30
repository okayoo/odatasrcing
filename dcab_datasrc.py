#!/usr/bin/python

from yahoo_finance import Share
import pandas as pd
import numpy as np
#from pprint import pprint

#
# get data from yahoo finance and store in excel file
# so we can get data from the excel file through fget
#
class stockdata:
    def __init__(self, symb, online=1):
        self._symb = symb
        # <class 'yahoo_finance.Share'>
        if (online):
            try:
                self.body = Share(symb)
            except:
                self.body = np.nan
                print("Share error:", self._symb)

    def get_price(self):
        '''
        get today's price
        if market closed, the price is the close price
        Returns
        -------
        price : str
        '''
        price = self.body.get_price()
        return price

    def get_days_high(self):
        '''
        get today's high price
        Returns
        -------
        dayhigh : str
        '''
        dayhigh = self.body.get_days_high()
        return dayhigh

    def get_days_low(self):
        '''
        get today's low price
        Returns
        -------
        daylow : str
        '''
        daylow = self.body.get_days_low()
        return daylow

    def get_historical(self, start_date, end_date):
        '''
        Parameters
        ----------
        start_date : str
            'year-month-day', for example '2015-10-01'
        end_date : str

        Returns
        -------
        historical : dlist, dict list
            historical          : <class 'list'>
            historical[0]       : <class 'dict'>
            historical[0][High] : <class 'str'>
            for example:
            [{'Adj_Close': '75.620003',
              'Close': '75.620003',
              'Date': '2015-10-23',
              'High': '75.760002',
              'Low': '72.839996',
              'Open': '73.980003',
              'Symbol': 'BABA',
              'Volume': '22342100'},
             {}, ... {}]
        '''
        historical = self.body.get_historical(start_date, end_date)
        return historical

    def save_historical_file(self, start_date, end_date):
        '''
        save historical data to excel file in form of DataFrame
        the file name is 'get_historical_SYMB_ENDATE.xlsx', for example, 'get_historical_YHOO_2015-10-24.xlsx'
        Parameters
        ----------
        start_date : str
            'year-month-day', for example '2015-10-01'
        end_date : str

        Returns
        -------
        len : int
            length of historical
        '''
        try:
            historical = self.body.get_historical(start_date, end_date)
        except:
            print("get_historical error:", self._symb, start_date, end_date)
            return 0

        length = len(historical)
        if (length == 0):
            #print("len is 0:", self._symb)
            return 0

        # check data
        try:
            high = float(historical[0]['High'])
        except:
            print("get_high error:", self._symb)
            return 0

        df = pd.DataFrame(historical)
        file_name = './data/' + self._symb + '_historical_' + end_date + '.xlsx'
        df.to_excel(file_name)
        return length

    def read_historical_file(self, end_date):
        '''
        read historical data from file
        the file name is 'get_historical_SYMB_ENDATE.xlsx', for example, 'get_historical_YHOO_2015-10-24.xlsx'
        Parameters
        ----------
        end_date : str
            'year-month-day', for example '2015-10-01'

        Returns
        -------
        df : DataFrame of Pandas
            df                  : <class 'pandas.core.frame.DataFrame'>
            df[:1]              : <class 'pandas.core.frame.DataFrame'>
            df.High(df['High']) : <class 'pandas.core.series.Series'>
            df.loc[0]           : <class 'pandas.core.indexing._LocIndexer'>
            df.iloc[0]          : <class 'pandas.core.indexing._iLocIndexer'>
            for example:
                Adj_Close      Close        Date       High        Low       Open Symbol    Volume
            0   75.620003  75.620003  2015-10-23  75.760002  72.839996  73.980003   BABA  22342100
            1   70.989998  70.989998  2015-10-22  71.629997  70.070000  70.160004   BABA  10691400
            2   69.480003  69.480003  2015-10-21  71.790001  68.889999  71.790001   BABA  16800200
        '''
        file_name = './data/' + self._symb + '_historical_' + end_date + '.xlsx'
#        file_name = './data/get_historical_' + self._symb + '_' + end_date + '.xlsx'
        try:
            df = pd.read_excel(file_name)
        except FileNotFoundError as e:
            df = pd.DataFrame({[]})
            print(e, self._symb)
        self._df = df
        return df

    # get date through row
    def fget_date(self, row):
        val = self._df.Date[row]
        return val

    def fget_close(self, row):
        val = self._df.Close[row]
        return val

    def fget_high(self, row):
        val = self._df.High[row]
        return val

    def fget_low(self, row):
        val = self._df.Low[row]
        return val

    # get date through row && col
    def fget_data(self, col, row):
#        val = self._df[col][row]
#        return val
        return 0

if __name__=="__main__":
    rd = stockdata('BABA')
    price = rd.get_price()
    print("price got:", price)
    sdate = '2015-10-01'
    edate = '2015-10-24'
#    rd.save_historical_file(sdate, edate)
    df = rd.read_historical_file(edate)
    print(df)
#    print('high=', rd.fget_high(1))
#    print('val=', rd.fget_data(1, 1))
'''
    print(type(historical))
    print(type(historical[0]))
    print(historical[0]['High'])
    print(type(historical[0]['High']))
'''

