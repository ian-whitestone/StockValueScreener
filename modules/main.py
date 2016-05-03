import finsymbols as stock_symb


# cd ~/Documents/Programming/Python/ValueScreener/modules


sp_500=stock_symb.get_sp500_symbols()
amex=stock_symb.get_amex_symbols()
nyse=stock_symb.get_nyse_symbols()
ndaq=stock_symb.get_nasdaq_symbols()

sp_500_list=[company['symbol'] for company in sp_500]
print(sp_500_list)
print (len(sp_500_list))