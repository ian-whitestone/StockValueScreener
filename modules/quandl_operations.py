import quandl
import general_utils as Ugen

quandl.ApiConfig.api_key = Ugen.ConfigSectionMap('quandl')['key']



