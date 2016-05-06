import data_scraping_utils as Uds
import io
import requests
import ast
import general_utils as Ugen

def build_gf_url(num_records,exchange): #build google finance URL
	if exchange=='TSE':
		curr='CAD'
	else:
		curr='USD'
	gf_mid_url=Ugen.read_file('/Users/whitesi/Documents/Programming/Python/ValueScreener/gf_mid_url.txt')
	url="https://www.google.com/finance?output=json&start=0&num="+str(num_records)+"&noIL=1&q="\
		"[currency%20%3D%3D%20%22"+curr+"%22%20%26%20%28exchange%20%3D%3D%20%22"+exchange\
		+gf_mid_url[0]+"&restype=company&ei=NSYqV7GEI9adjAGw14bIBA"

	return url


def scrape_gf(exchange):
	"""
	Exchanges include: NASDAQ TSE NYSE
	"""
	r_text=Uds.http_get(build_gf_url(20,exchange))
	data=ast.literal_eval(r_text)
	print (data['num_company_results'])
	r_text=Uds.http_get(build_gf_url(data['num_company_results'],exchange))
	data=ast.literal_eval(r_text)
	stock_dict={row['ticker']:{comp['field']:comp['value'] for comp in row['columns']} for row in data['searchresults']}
	return stock_dict

