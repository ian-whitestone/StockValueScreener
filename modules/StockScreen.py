import general_utils as Ugen
import pandas as pd
import numpy as np
import data_scraping as ds

class StockScreen(): #Ian: tentative setup for class, may have to move functions out/in accordingly
	def __init__(self,exchange):
		self.exchange=exchange
		self.filters={'MarketCap':1*10**9,'PE':0,'PriceSales':0} #greater than 1 billion
		self.PE_filter=0 #must have earnings
		self.ascending_rank= ['PE','PriceSales','PriceToBook']#value factors to be sorted and ranked
		self.stock_df=self.build_stock_universe()

	def clean_df(self,x):
		if isinstance(x,str):
			x=x.replace(',','')
			if 'M' in x:
				x=x.replace('M','')
				x=round(float(x)*10**6,2)
			elif 'B' in x:
				x=x.replace('B','')
				x=round(float(x)*10**9,2)
			elif 'T' in x:
				x=x.replace('T','')
				x=round(float(x)*10**12,2)
			else:
				x=round(float(x),2)
		return x

	def build_stock_universe(self): #Eventually turn this into a class/part of a class?
		""" 
		# print (df.head(n=5))
		# print (df.tail(5))
		COLUMN NAMES:
		# print (df.columns.values)
		['Beta' 'DividendYield' 'EBITDMargin' 'ForwardPE1Year' 'MarketCap' 'PE'
	 		'PriceSales' 'PriceToBook' 'Volume']
		"""
		stock_dict=ds.scrape_gf(self.exchange)
		df=pd.DataFrame(stock_dict)
		df=df.transpose()
		df=df.replace('-', np.nan)
		df=df.applymap(self.clean_df)
		return df.apply(self.calc_EBITDA_ratio,axis=1)

	def calc_EBITDA_ratio(self,df): #eventually change to Enterprise value from YF
		# print (type(df['EBITDMargin']),df['EBITDMargin'])
		# print (type(df['PriceSales']),df['PriceSales'])
		# print (type(df['MarketCap']),df['MarketCap'])
		# print (type(df['QuoteLast']),df['QuoteLast'])
		# df['EBITDA']=df['EBITDMargin']/df['PriceSales']*df['MarketCap']
		df['EBITDAtoMcap']=df['EBITDMargin']/df['PriceSales']
		return df

	def filter_universe(self):
		for factor,min_value in self.filters.items():
			df=self.stock_df[self.stock_df[factor]>min_value
		return df

	def assign_ranks(self,df):
		#add loop, initialize sorted variables in __init__
		
		for factor in self.ascending_rank:
			df=df.sort_values(factor, ascending=True)
			df[factor+'_rank'] = 100-pd.qcut(df[factor], 100, labels=False)
		
		factor='EBITDAtoMcap'
		df=df.sort_values(factor, ascending=False)
		df[factor+'_rank'] = 1+pd.qcut(df[factor], 100, labels=False)

		return df




