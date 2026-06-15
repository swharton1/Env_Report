#!/bin/bash

#Type bash update_data.sh or ./update_data.sh to run this script. 

echo 'Updating Environmental Data...'

#Get current year. 
current_year=$(date +%Y)
echo $current_year 

#Update F10.7 data. 
echo 'Updating F10.7...' 
wget https://spaceweather.gc.ca/solar_flux_data/daily_flux_values/fluxtable.txt

#Move it into the data folder if the file has been downloaded. 
if [ -f fluxtable.txt ] 
then
    echo 'Found '$fluxtable'. Move to data folder.' 
    mv fluxtable.txt data/fluxtable.txt
fi 

#Update the OMNI data. 
echo 'Updating...'
omni_file=omni_5min$current_year.asc
omni_link=https://cdaweb.gsfc.nasa.gov/pub/data/omni/high_res_omni/$omni_file
echo $omni_link 

ip $omni_link show 

wget https://cdaweb.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni_5min$current_year.asc

#Move it into the folder if the file has been downloaded. 
if [ -f $omni_file ];
then 
    echo 'Found '$omni_file'. Move to data folder.' 
    mv omni_5min$current_year.asc data/omni_5min$current_year.asc 
fi 
