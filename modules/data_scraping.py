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
	# gf_mid_url=Ugen.read_file('/Users/whitesi/Documents/Programming/Python/ValueScreener/gf_mid_url.txt')
	gf_mid_url=Ugen.read_file('/Users/whitesi/Documents/Programming/Python/ValueScreener/gf_mid_url_new.txt')
	# url="https://www.google.com/finance?output=json&start=0&num="+str(num_records)+"&noIL=1&q="\
	# 	"[currency%20%3D%3D%20%22"+curr+"%22%20%26%20%28exchange%20%3D%3D%20%22"+exchange\
	# 	+gf_mid_url[0]+"&restype=company&ei=NSYqV7GEI9adjAGw14bIBA"
	
	url="https://www.google.com/finance?start=0&num="+str(num_records)+"&q=%5Bcurrency%20%3D%3D%20%22"\
		+curr+"%22%20%26%20(exchange%20%3D%3D%20%22"+exchange \
		+gf_mid_url[0]+"%5D&restype=company&output=json&noIL=1&ei=BWsuV4H5K8HfjAGt7amIDA"
	##Track ^ this url, see if it becomes out of date again...

	##NYSE still missing some using url above (see below url to fix...)
	# url="https://www.google.com/finance?output=json&start=0&num=20&noIL=1&q=[currency%20%3D%3D%20%22USD%22%20%26%20%28exchange%20%3D%3D%20%22NYSE%22%29%20%26%20%28market_cap%20%3E%3D%200%29%20%26%20%28market_cap%20%3C%3D%20367360000000%29%20%26%20%28pe_ratio%20%3E%3D%200%29%20%26%20%28pe_ratio%20%3C%3D%206683%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%2070.17%29%20%26%20%28price_to_book%20%3E%3D%200%29%20%26%20%28price_to_book%20%3C%3D%20983%29%20%26%20%28price_to_sales_trailing_12months%20%3E%3D%200%29%20%26%20%28price_to_sales_trailing_12months%20%3C%3D%20603621%29%20%26%20%28last_price%20%3E%3D%200%29%20%26%20%28last_price%20%3C%3D%20217000%29%20%26%20%28average_volume%20%3E%3D%200%29%20%26%20%28average_volume%20%3C%3D%2093080000%29%20%26%20%28ebitd_margin_trailing_12months%20%3E%3D%20-672052%29%20%26%20%28ebitd_margin_trailing_12months%20%3C%3D%20393%29%20%26%20%28beta%20%3E%3D%20-0.97%29%20%26%20%28beta%20%3C%3D%204.73%29]&restype=company&ei=BWsuV4H5K8HfjAGt7amIDA"
	return url





def scrape_gf(exchange):
	"""
	Exchanges include: NASDAQ 	TSE 	NYSE
	"""
	r_text=Uds.http_get(build_gf_url(20,exchange))
	data=ast.literal_eval(r_text)
	print (data['num_company_results'])
	r_text=Uds.http_get(build_gf_url(data['num_company_results'],exchange))
	data=ast.literal_eval(r_text)
	
	##extras
	# for row in data['searchresults']:
	# 	if row['title']=="Apple Inc.":
	# 		print (row)
	
	print (len(data['searchresults']))


	##
	stock_dict={row['ticker']:{comp['field']:comp['value'] for comp in row['columns']} for row in data['searchresults']}
	return stock_dict

