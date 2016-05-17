import finsymbols as ss
import yahoo_finance as yf
import general_utils as Ugen
import data_scraping as ds
import pandas as pd
import numpy as np
import StockScreen
import datetime


def get_stock_symbols():
	nyse=[company['symbol'] for company in ss.get_nyse_symbols() if '$' not in company['symbol']]
	amex=[company['symbol'] for company in ss.get_amex_symbols() if '$' not in company['symbol']]
	ndaq=[company['symbol'] for company in ss.get_nasdaq_symbols() if '$' not in company['symbol']]
	sp500=[company['symbol'] for company in ss.get_sp500_symbols() if '$' not in company['symbol']]
	tsx=get_tsx_companies()
	return sp500,amex,nyse,ndaq,tsx

def get_tsx_companies():
	lines=Ugen.read_file('/Users/whitesi/Documents/Programming/Python/ValueScreener/TSX.txt')
	parsed_list=[company.split('\n')[0] for company in lines]
	tsx_dict={company.split('\t')[0]+'.TO':company.split('\t')[1] for company in parsed_list}
	tsx_symbol_list=list(tsx_dict.keys())
	return tsx_symbol_list #,tsx_dict

def determine_yf_coverage(name,stock_list,cov_type): #Determine what % of stocks are covered by yahoo finance
	featured_stocks_list=[]
	featured_stocks_dict={}
	for symbol in stock_list: 
		company=yf.Share(symbol)
		if cov_type=='PE':
			featured_stocks_list.append(company.get_price_earnings_ratio())
		elif cov_type=='P':
			featured_stocks_list.append(company.get_price())
		elif cov_type=='MCAP':
			featured_stocks_list.append(company.get_market_cap())
		elif cov_type=='EBIDTA':
			featured_stocks_list.append(company.get_ebitda())
		elif cov_type=='yf_hist_price':
			hist_date_3=(datetime.date.today() - datetime.timedelta(3*365/12))
			try:
				hist_price=float(company.get_historical(hist_date_3.isoformat(),(hist_date_3+datetime.timedelta(1)).isoformat())[0]['Close'])
			except:
				hist_price=None
			featured_stocks_list.append(hist_price)
		elif cov_type=='gf_hist_price':
			hist_price=ds.scrape_gf_histprices('TSE',symbol.split(".TO")[0])
			featured_stocks_list.append(hist_price)
	print ('%s has %f percent coverage for %s' 
				%(name,round(sum(x is not None for x in featured_stocks_list)/len(featured_stocks_list),2),cov_type))
	return

def run_program(exchange):
	screen=StockScreen.StockScreen(exchange)
	screen.filter_universe()
	ranked_df=screen.assign_ranks()
	top_50=list(ranked_df.head(n=50).index)
	# print (ranked_df)
	print (top_50)				##
	print (ranked_df.ix['AD']) #print key stats for these companies (and latest 5 google news article titles??)
	print ("program executed")
	return

# hist_date_3=(datetime.date.today() - datetime.timedelta(3*365/12))
# hist_date_6=(datetime.date.today() - datetime.timedelta(6*365/12))
# ticker='AD.TO'
# # print (hist_date_3)
# # print (type(hist_date_3))
# stock=yf.Share(ticker)
# hist_price_3=float(stock.get_historical(hist_date_3.isoformat(),(hist_date_3+datetime.timedelta(1)).isoformat())[0]['Close'])
# # hist_price_6=float(stock.get_historical(hist_date_6,hist_date_6)[0]['Close'])

# print (hist_price_3)

###TO RUN FROM COMMAND LINE
# cd ~/Documents/Programming/Python/ValueScreener/modules
#python -c "import main; main.run_program('TSE')" #TSE, NASDAQ or NYSE



##add function to print interesting stats/info about the top ranked companys...include spaces in between prints i,e /n


####YAHOO FINANCE COVERAGE TESTING

# tsx=get_tsx_companies()

# determine_yf_coverage('NDAQ',ndaq,'P')
# determine_yf_coverage('SP500',sp500,'P')
# determine_yf_coverage('NYSE',nyse,'P')
# determine_yf_coverage('TSX',tsx,'gf_hist_price')

#TSX has 0.740000 percent coverage for gf_hist_price
#TSX has 0.62 percent coverage for yf_hist_price


# NDAQ has 0.850000 percent coverage for MCAP
# SP500 has 0.870000 percent coverage for MCAP
# NYSE has 0.770000 percent coverage for MCAP
# TSX has 0.660000 percent coverage for MCAP

# NDAQ has 0.920000 percent coverage for EBIDTA
# SP500 has 0.930000 percent coverage for EBIDTA
# NYSE has 0.890000 percent coverage for EBIDTA
# TSX has 0.760000 percent coverage for EBIDTA


# NDAQ has 0.990000 percent coverage for P
# SP500 has 0.990000 percent coverage for P
# NYSE has 0.920000 percent coverage for P
# TSX has 0.830000 percent coverage for P


###TO DO 
#1) Enterprise value data (DONE)
#2) Shareholder yield data
#3) Figure out which companies are no longer listed/public (NOT NECESSARY?)
#4) Changing google finance urls..... (DONE)
#5) Ranks by sector!!!!
#6) Price to cash flow (DONE)
#7) 3 & 6 month price momentum (use YF) --> implmement google finance...
#8) Trending value strategy
#9) strategies that perform well in bear markets?

#Long term - when is it a good idea to buy a stock? i.e. stock chart methods etc


#can still integrate 10K API??

