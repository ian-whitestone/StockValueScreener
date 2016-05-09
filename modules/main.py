import finsymbols as ss
import yahoo_finance as yf
import general_utils as Ugen
import data_scraping as ds
import pandas as pd
import numpy as np
import StockScreen
# cd ~/Documents/Programming/Python/ValueScreener/modules


def get_stock_symbols():
	nyse=[company['symbol'] for company in ss.get_nyse_symbols() if '$' not in company['symbol']]
	amex=[company['symbol'] for company in ss.get_amex_symbols() if '$' not in company['symbol']]
	ndaq=[company['symbol'] for company in ss.get_nasdaq_symbols() if '$' not in company['symbol']]
	sp500=[company['symbol'] for company in ss.get_sp500_symbols() if '$' not in company['symbol']]
	tsx=get_tsx_companies
	return sp_500,amex,nyse,ndaq,tsx

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
	print ('%s has %f percent coverage for %s' 
				%(name,round(sum(x is not None for x in featured_stocks_list)/len(featured_stocks_list),2),cov_type))
	return

def run_program():
	screen=StockScreen.StockScreen('NASDAQ')
	filtered_df=screen.filter_universe()
	ranked_df=screen.assign_ranks(filtered_df)
	print(ranked_df)
	print ("program executed")
	return


run_program()

##add function to print interesting stats/info about the top ranked companys...include spaces in between prints i,e /n

##May 7, 2016 
##TSE - 2680,2680
##NASDAQ - 3722, 3722
##NYSE - 3975, 3974


##Enterpise value data...
# https://finance.yahoo.com/q/ks?s=F+Key+Statistics


####YAHOO FINANCE COVERAGE TESTING

# determine_yf_coverage('NDAQ',ndaq,'P')
# determine_yf_coverage('SP500',sp500,'P')
# determine_yf_coverage('NYSE',nyse,'P')
# determine_yf_coverage('TSX',tsx,'P')

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
#1) Figure out which companies are missign data - account for this in ranking??
#2) Figure out which companies are no longer listed/public
#3) 