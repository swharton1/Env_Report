#This will plot the data for given dates. 

import omnipy 

#Default values of start and end time. (YYYY,mm,dd,HH,MM,SS)
#Set the None to plot the last 24 hours. 
start = (2026, 4, 1, 0, 0, 0)
end = (2026, 4, 2, 0, 0, 0)

#Create the plot object. 
#By default, if the start and end are set to None, end will be set to now and start to 24 hours before that. 
plot = omnipy.plot_omni_f107.plot(start=start, end=end) 

#Now make the summary plot. It will save as a pdf to the reports/ directory. You save as 'pdf' or 'png'. 
plot.plot_summary(save=True, filetype='pdf')
