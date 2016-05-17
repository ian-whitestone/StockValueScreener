import general_utils as Ugen
import pandas as pd
import numpy as np
import yahoo_finance as yf
import data_scraping as ds
import math
import datetime

class StockScreen(): #Ian: tentative setup for class, may have to move functions out/in accordingly
	def __init__(self,exchange):
		self.exchange=exchange
		self.value_factors=['PE','PriceSales','PriceToBook','EBITDAtoEV',
								'PriceToCashFlow','DividendYield','6monthmom','3monthmom']
		self.filters={'MarketCap':1*10**9,'PE':0,'PriceSales':0} #greater than 1 billion
		self.ascending_rank= ['PE','PriceSales','PriceToBook','PriceToCashFlow']#value factors to be sorted and ranked
		self.descending_rank=['EBITDAtoEV','DividendYield','6monthmom','3monthmom']
		self.stock_df=self.build_stock_universe()

	def clean_df(self,x): #Ian: probably a cleaner way of doing this?
		if isinstance(x,str):
			x=x.replace(',','')
			if 'M' in x:
				x=x.replace('M','')
				x=round(float(x)*10**6,2)
			elif 'K' in x:
				x=x.replace('K','')
				x=round(float(x)*10**3,2)
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
		gf_dict=ds.scrape_gf_screen(self.exchange)
		# yf_dict={ticker:ds.scrape_yf(ticker,self.exchange) for ticker in gf_dict.keys()}
		# merged_dict={k: dict(gf_dict.get(k, {}).items()|yf_dict.get(k, {}).items()) for k in gf_dict.keys()}
		merged_dict=gf_dict		
		df=pd.DataFrame(merged_dict)
		df=df.transpose()
		df=df.replace(to_replace=['-','N/A'],value= np.nan)
		df=df.applymap(self.clean_df)
		return df.apply(self.calc_addl_ratio,axis=1)

	def calc_addl_ratio(self,df):
		df['EBITDAtoEV']=df['EBITDMargin']/100/df['PriceSales']*df['MarketCap']/10000#df['EV'] 
		df['PriceToCashFlow']=df['PriceSales']/(df['OperatingMargin']/100)
		hist_price_3,hist_price_6=self.calc_price_momemtum(df.name)
		if hist_price_3 and hist_price_6:
			df['6monthmom']=(df['QuoteLast']-hist_price_6)/hist_price_6
			df['3monthmom']=(df['QuoteLast']-hist_price_3)/hist_price_3
		else:
			df['6monthmom']=np.nan
			df['3monthmom']=np.nan
		return df

	def calc_price_momemtum(self,ticker):
		hist_date_3=datetime.date.today() - datetime.timedelta(3*365/12)
		hist_date_6=datetime.date.today() - datetime.timedelta(6*365/12)
		if self.exchange=='TSE':
			ticker=ticker+'.TO'
		try:
			stock=yf.Share(ticker)
			hist_price_3=float(stock.get_historical(hist_date_3.isoformat(),(hist_date_3+datetime.timedelta(1)).isoformat())[0]['Close'])
			hist_price_6=float(stock.get_historical(hist_date_6.isoformat(),(hist_date_6+datetime.timedelta(1)).isoformat())[0]['Close'])
		except:
			return None,None
		return hist_price_3,hist_price_6

	def filter_universe(self):
		# df=self.stock_df[self.stock_df['PE']>0]
		for factor,min_value in self.filters.items():
			self.stock_df=self.stock_df[self.stock_df[factor]>min_value]
		return

	def assign_ranks(self):
		df=self.stock_df
		for factor in self.ascending_rank:
			df=df.sort_values(factor, ascending=True)
			try:
				df[factor+'_rank'] = 100-pd.qcut(df[factor], 100, labels=False)
			except:
				df[factor+'_rank'] = 100-pd.qcut(df[factor], 50, labels=False)*2
		for factor in self.descending_rank:
			df=df.sort_values(factor, ascending=False)
			try:
				df[factor+'_rank'] = 1+pd.qcut(df[factor], 100, labels=False)
			except:
				df[factor+'_rank'] = 1+pd.qcut(df[factor], 50, labels=False)*2
		
		df=df.apply(self.sum_ranks,axis=1)
		return df.sort_values('norm_rank',ascending=False)

	def sum_ranks(self,df): #eventually account for missing data (i.e. missing/NA ranks)
	#If nan give a medium ranking (i.e. 50???) - that is the O'Shaugnessy method
		df['num_ranks']=sum([1 for factor in self.value_factors if not math.isnan(df[factor+'_rank'])]) #count how many ranks it had non nan values for
		df['total_rank']=sum([df[factor+'_rank'] for factor in self.value_factors])
		df['norm_rank']=df['total_rank']/df['num_ranks']
		return df




