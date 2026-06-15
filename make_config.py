#This will make a proper python configuration file to store paths in. 

#See: https://configu.com/blog/working-with-python-configuration-files-tutorial-best-practices/#:~:text=Configuration%20files%20in%20Python%20are,can%20be%20read%20and%20modified.

from configparser import ConfigParser

#Make the config object. 
config_object = ConfigParser()

#Add information to the object. 
config_object["PATHINFO"] = {
    "data_path": "/data/smile/Env_Report/data/",
    "report_path": "/data/smile/Env_Report/reports/"
}

#Write the configuration file. 
with open('config.ini', 'w') as conf:
    config_object.write(conf) 
    
