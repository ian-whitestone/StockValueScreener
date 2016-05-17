import data_scraping_utils as Uds
import io
import requests
import ast
import general_utils as Ugen
from bs4 import BeautifulSoup

def build_gf_screener_url(num_records,exchange): #build google finance SCREENR URL
	if exchange=='TSE':
		curr='CAD'
	else:
		curr='USD'
	gf_code="Wbc3V9DWEs-M2AaV1pXoBQ" #update manually if required...may have fixed problem with revised filters in gf_mid_url...
	gf_mid_url=Ugen.read_file('/Users/whitesi/Documents/Programming/Python/ValueScreener/gf_mid_url.txt')
	url="https://www.google.ca/finance?output=json&start=0&num="+str(num_records) \
			+"&noIL=1&q=[currency%20%3D%3D%20%22"+curr+"%22%20%26%20%28exchange%20%3D%3D%20%22" \
			+exchange+gf_mid_url[0]+gf_code
	return url

def build_gf_histprices_url(exchange,ticker):
	gf_code="9Tc7V9mkBsaVjAH2ia3wAg"
	url="https://www.google.ca/finance/historical?q="+exchange+"%3A"+ticker+"&start=0&num=250&ei="+gf_code

	return url

def scrape_gf_histprices(exchange,ticker):
	url=build_gf_histprices_url(exchange,ticker)
	r_text=Uds.http_get(url)
	soup = BeautifulSoup(r_text,"lxml")
	try:
		table=soup.find("table",{"class":"gf-table historical_price"})
		rows=[row for row in table.findAll('tr')]
		rows.pop(0)
		hist_price_dict={row.get_text().split('\n')[1]:row.get_text().split('\n')[5] for row in rows}
	except:
		return None #{}
	return hist_price_dict

def scrape_gf_screen(exchange):
	"""
	Exchanges include: NASDAQ 	TSE 	NYSE
	"""
	r_text=Uds.http_get(build_gf_screener_url(20,exchange))
	data=ast.literal_eval(r_text)
	print (data['num_company_results'])
	r_text=Uds.http_get(build_gf_screener_url(data['num_company_results'],exchange))
	data=ast.literal_eval(r_text)
	
	print (len(data['searchresults']))

	stock_dict={row['ticker']:{comp['field']:comp['value'] for comp in row['columns']} for row in data['searchresults']}
	return stock_dict

def scrape_yf(ticker,exchange):
	if exchange=='TSE':
		ticker=ticker+".TO"
	url="http://finance.yahoo.com/q/ks?s="+ticker
	r_text=Uds.http_get(url)
	soup = BeautifulSoup(r_text,"lxml")
	try:
		table=soup.find("table",{"class":"yfnc_datamodoutline1"})
		row_names=table.findAll("td",{"class":"yfnc_tablehead1"})
		row_values=table.findAll("td",{"class":"yfnc_tabledata1"})
		key_stats_dict={row_name.get_text().split('(')[0][:-1]:row_value.get_text()
							for row_name,row_value in zip(row_names,row_values)}
	except:
		return {}
	return {'EV':key_stats_dict['Enterprise Value']}#temporary, right now i only want EV from yf #key_stats_dict

#python -c "import data_scraping as ds; ds.scrape_yf('AD.TO')"


#{'Enterprise Value/Revenue': '12.92', 'Forward P/E': '13.55', 'Price/Book': '1.55', 'Price/Sales': '12.26', 'PEG Ratio': '3.67', 'Enterprise Value': '1.11B', 'Enterprise Value/EBITDA': '15.68', 'Market Cap': '1.05B', 'Trailing P/E': '17.26'}









