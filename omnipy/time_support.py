#Samuel Wharton 

#This will contain various functions to support the management of times. 

import datetime as dt
import matplotlib as mpl 
import numpy as np

def NewTimeAxis(ax, stime, etime, fontsize=10, UT=True):
	'''Attempt to make a more sophisticated version of time_axis.
	This is mainly for recording ways of doing it and not necessarily the best approach
	'''
	
	#Check stime/etime. 
	assert(isinstance(stime, dt.datetime)), "stime must be a dt.datetime object"
	assert(isinstance(etime, dt.datetime)), "etime must be a dt.datetime object"
	assert(stime < etime), "stime must be before etime" 
	
	if ((etime-stime).days) > 90:
		t_locate = mpl.dates.MonthLocator(bymonthday=1)
		t_form = mpl.dates.DateFormatter('%b\n%y')
	elif ((etime-stime).days) > 30:
		t_locate = mpl.dates.DayLocator(interval = 2)
		t_form = mpl.dates.DateFormatter('%b-%d\n%y')
	elif ((etime-stime).days) > 4:
		t_locate = mpl.dates.HourLocator(interval = 4)
		t_form = mpl.dates.DateFormatter('%b-%d')
	elif ((etime-stime).days) > 1:
		t_locate = mpl.dates.HourLocator(interval = 1)
		t_form = mpl.dates.DateFormatter('%H:%M\n%b-%d') 
	else:
		t_locate = mpl.dates.MinuteLocator(interval = tick_sep(stime,etime))
		t_form = mpl.dates.DateFormatter('%H:%M')
	
	#Now format the ticks 
	ax.xaxis.set_major_formatter(t_form)
	ax.xaxis.set_major_locator(t_locate)
	
	#Set the limits and label the axis. 
	ax.set_xlim(stime, etime)
	if UT: ax.set_xlabel('UT', fontsize=fontsize) 
	ax.tick_params(labelsize=fontsize)
	
	return ax 
	
	
def time_axis(ax, stime, etime, fontsize=10, UT=True, shift_times=False): 
	''' This will format the time axis of any graph. 
	It is perfectly suitable for quick sorts of plots but for final plots,
	you may wish to do it on a case-by-case basis.  
	
	Parameters
	----------
	ax - the axis on which this will take place. 
	stime - start time as a datetime object. 
	etime - end time as a datetime object. 
	
	Returns
	-------
	ax - with the formatting completed. 
	
	'''
	
	#Check stime/etime. 
	assert(isinstance(stime, dt.datetime)), "stime must be a dt.datetime object"
	assert(isinstance(etime, dt.datetime)), "etime must be a dt.datetime object"
	assert(stime < etime), "stime must be before etime" 
	
	
	#Decide whether to use dates or just times. 
	
	if((etime-stime).total_seconds() > 90*86400): t_form = mpl.dates.DateFormatter('%b\n%y')
	elif((etime-stime).total_seconds() > 30*86400): t_form = mpl.dates.DateFormatter('%b-%d\n%y')
	elif((etime-stime).total_seconds() > 4*86400): t_form = mpl.dates.DateFormatter('%b-%d')
	elif((etime-stime).total_seconds() > 1*86400): t_form = mpl.dates.DateFormatter('%H:%M\n%b-%d')
	else: t_form = mpl.dates.DateFormatter('%H$^{%M}$')
		
	#Set ticks using the tick_sep function. 
	t_locate = mpl.dates.MinuteLocator(interval = tick_sep(stime,etime))
	
	#Now format the ticks 
	ax.xaxis.set_major_formatter(t_form)
	ax.xaxis.set_major_locator(t_locate)
	
	#Set the limits and label the axis. 
	ax.set_xlim(stime, etime)
	if UT: ax.set_xlabel('UT', fontsize=fontsize) 
	ax.tick_params(labelsize=fontsize)
	
	#Shift the times onto sensible hours. 
	#Choose some nicer labels. 
	if shift_times:
		tlabels = [] 
		start = np.ceil(ax.get_xlim()[0])
		while start <= ax.get_xlim()[1]:
			tlabels.append(start)
			start += (tick_sep(stime,etime)/(60*24))
		#print (tlabels)
		ax.set_xticks(tlabels) 

	return ax 
	
	
def tick_sep(stime, etime):
	''' Set the tick separation on the x axis  
	
	Parameters
	----------
	stime - start time in datetime format
	etime - end time "
	
	Returns
	-------------------
	interval - in minutes between tick marks. 
	
	'''
	
	#Find the full time width of the interval. 
	t_diff = etime - stime
	t = t_diff.total_seconds()
	interval = None 
	n = 0
	unit = 10800 #8th of a day or 3 hours
	d = 0
	day = 86400
	#print (t, unit)
	if (t >= unit/18) and (t <= unit/6):
		#From 10 minutes to 30 minutes.
		interval = 2 
	elif (t >= unit/6) and (t <= unit/3):
		#From 30 minutes to 1 hour.
		interval = 5
	elif (t >= unit/3) and (t <= unit):
		#From 1 hour to 3 hours. 
		interval = 15 
	elif (t <= day) and (t > unit):
		while interval is None:
			if (t >= unit*(2**n)) and (t <= unit*(2**(n+1))):
				interval = 15*(2**(n+1))
			else: n += 1 
	else:
		while interval is None:
			if (t >= day*(2**d)) and (t <= day*(2**(d+1))):
				interval = 180*(2**(d+1))
			else: d += 1
	#print (interval)	
	return(interval) 	

def CreateDatetimeList(stime, etime, inc, inclusive=False): 
	'''Will create a list of datetimes
	
	Parameters
	----------
	stime - start time as a datetime object
	etime - end time as a datetime object
	inc - time increment between values, eg. dt.timedelta(hours=1) 
	inclusive - whether to add the end time to the list (def = False) 
		
	Returns
	-------
	times - list of datetimes from stime including etime  
	
	'''
	
	stime0 = stime	
	times = list() 
	
	while(stime0 < etime):
		times.append(stime0)
		stime0 += inc 	
	
	if inclusive: times.append(etime)
	
	return times

def CreateMonthList(stime, etime):
	'''Makes a list of times incrementing on the same day each month. 
	
	Parameters
	----------
	stime 
	etime 
	
	Returns
	-------
	times - list, including stime and etime. 
	
	'''
	
	stime0 = stime 
	month = stime.month
	year = stime.year 
	times = list() 
	while(stime0 < etime):
		if month > 12:
			#Increment the year and reset to Jan if month = 13. 
			year += 1
			month = 1
		stime0 = dt.datetime(year, month, stime0.day)
		#Increase the month normally and keep the year the same. 
		month += 1
		times.append(stime0)
		 
	return times 	
		
		
def ConvertDatetimeToDay(dtimes):
	'''This will convert a list of datetime objects to days. '''

	from matplotlib.dates import date2num
	dtimes = np.array(dtimes) 
	days = date2num(dtimes)
	return days

def ConvertDayToDatetime(days):
	'''This will convert a list of days to datetime objects that are timezone naive '''
	
	from matplotlib.dates import num2date
	days = np.array(days) 
	dtimes = [] 
	for d in days:
		dtime = num2date(d)
		dtimes.append(dt.datetime(dtime.year, dtime.month, dtime.day, dtime.hour, dtime.minute, dtime.second, dtime.microsecond))
	dtimes = np.array(dtimes)
	return dtimes 	
		
def ConvertDatetimeToSecond(dtimes):
	'''This will convert a list of datetime objects to seconds. '''
	
	from matplotlib.dates import date2num
	dtimes = np.array(dtimes) 
	days = date2num(dtimes)
	seconds = days*86400.
	return seconds	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
