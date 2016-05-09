from __future__ import division
import math
from datetime import datetime,date,timedelta
import time
import configparser 
import getpass
import sys
import csv
import unicodedata
import os
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import seaborn as sns
import matplotlib as mpl
from scipy import stats


def explore_list(list_name,num_iter): #Change so it selects random X entries then prints those, rather than first X
	for entry,i in zip(list_name,range(num_iter)):
		print (entry)
	return

def explore_dict(dict_name,num_iter):
	i=1
	for entry,value in dict_name.items():
		if i<=num_iter:
			print (value)
		else:
			break
		i+=1
	return


def seaborn_plot(df,plot_type='pairplot',columns=False):
	sns.set()
	mpl.rc("figure", figsize=(16, 8.65))
	plotting_df=(df[columns] if columns else df)
	if plot_type=='pairplot':
		sns.pairplot(plotting_df)
	elif plot_type=='corr_plot':
		sns.corrplot(plotting_df)
	sns.plt.show()
	return

def split_datetime_range(start, end, split):
    """Splits a range of dates into a list of equal ranges
    with remaining time allocated to the last of the series.
    This function doesn't overlap dates, so seconds are lost
    inbetween each range

    Parameters:
      start - The start of the range
      end - The end of the range
      split - How many ranges to produce

    Returns:
      List of individual ranges, where each range is also a list containing two dates
    """

    start = datetime.strptime(start,"%Y-%m-%d")
    end = datetime.strptime(end,"%Y-%m-%d")
    total_seconds = int((end - start).total_seconds())
    delta = total_seconds / split
    starts = [start + timedelta(seconds=delta * i) for i in range(split)]
    ends = [s + timedelta(seconds=delta - 1) for s in starts]
    ends[len(ends) - 1] = end
    date_tuples=zip(starts, ends)
    return[list(date_tuple) for date_tuple in date_tuples]


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
def getSec(s):
    try:
        if len(s) == 2:
            s = s + ':00'
        l = s.split(':')
        return int(l[0]) * 60 + int(l[1])
    except ValueError:
        return 0

def bin_mapping(x,bin_size):
	return math.trunc(x) - math.trunc(x)%bin_size

def output_dict(data_dict):
	new_sheet()
	rw = 0
	for key, items in data_dict.items():
		rw = rw + 1
		col = 1
		for data_item in items:
			Cell(rw,col).value = data_item
			col = col + 1
	return data_dict

def excel_mapping(map_sheet,key_col,map_col):#Cole: built general mapping utility to use excel as mapping matrix. Data must start at row 2
	excel_map = {}						
	print ('in mapping function')
	rw = 2
	while Cell(map_sheet,rw,key_col).value != None or Cell(map_sheet,rw,map_col).value != None: 
		if Cell(map_sheet,rw,key_col).value != None and Cell(map_sheet,rw,map_col).value != None:
			excel_map[Cell(map_sheet,rw,key_col).value] = Cell(map_sheet,rw,map_col).value
			rw += 1
		else:
			rw += 1
	return excel_map

def ConfigSectionMap(section):
	Config = configparser.ConfigParser()
	config_path = '/Users/whitesi/Documents/Programming/Python/db.ini'
		# config_path = 'C:/Users/Ian Whitestone/Documents/Python Projects/fanduel-master/db.ini'
	Config.read(config_path)
	dict1 = {}
	options = Config.options(section)
	for option in options:
	    try:
	        dict1[option] = Config.get(section, option)
	        if dict1[option] == -1:
	            DebugPrint("skip: %s" % option)
	    except:
	        print("exception on %s!" % option)
	        dict1[option] = None
	return dict1

def previous_day(todays_date): #YYYY-MM-DD
	t=time.strptime(todays_date.replace("-",''),'%Y%m%d')
	previous_day=date(t.tm_year,t.tm_mon,t.tm_mday)-timedelta(1)
	return str(previous_day)

def read_file(filepath):
	f = open(filepath, 'r')
	lines = f.readlines()
	f.close()
	return lines
