#This contains code to read in and plot the F10.7 and OMNI data. 

import os
import numpy as np 
import matplotlib.pyplot as plt 
import datetime as dt 


from . import read_config 
from . import time_support as ts 

class plot():
    '''This class reads in and plots the F10.7 and OMNI data.''' 
    
    
    def __init__(self, start=None, end=None):
        '''This reads in the data files.
        
        Parameters
        ----------
        start - start time for plotting. (YYYY,mm,dd,HH,MM,SS) Def = None, means one day before end.  
        end - start time for plotting. (YYYY,mm,dd,HH,MM,SS) Def = None, means yesterday. 
        
        '''
        
        #Sort out times. Use the previous 24 hours if needed. 
        
            
        if end is None: 
            self.end = dt.datetime.today() 
        else:
            self.end = dt.datetime(*end) 
        
        if start is None: 
            self.start = self.end - dt.timedelta(days=1) 
        else:
            self.start = dt.datetime(*start)
            
        print ('Get these times:') 
        print (self.start)
        print (self.end) 
        
        #Get the path to the data from the config file. 
        self.data_path = read_config.read_config(path_type='data_path') 
        self.report_path = read_config.read_config(path_type='report_path') 
        print (self.data_path) 
        
        #Read F10.7 data. 
        self.read_f107() 

        #Read the OMNI data. 
        self.read_omni_all() 

        
        
    def read_f107(self, filename='fluxtable.txt'):
        '''This reads in the whole fluxtable.txt file to get the F10.7 data.''' 
        
        #Check for presence of file. 
        abs_name = self.data_path+filename 
        assert os.path.exists(abs_name), f'{abs_name} was not found!' 
        
        print (f'Reading {abs_name}...') 
        #Open file and read contents. 
        with open(abs_name, 'r') as f: 
            lines = f.readlines() 
        
        #Make empty lists to fill. 
        dtime_all = [] 
        f107_all = [] 
        
        for l in lines[2:]:
            #Extract data. 
            date = str(l[0:8])
            time = str(l[12:18])
            f107 = float(l[54:65])
            
            #Produce datetime object. 
            dt_str = date+'-'+time
            dtime = dt.datetime.strptime(dt_str, '%Y%m%d-%H%M%S') 
            
            #Add to lists. 
            dtime_all.append(dtime)
            f107_all.append(f107) 
        
        dtime_all = np.array(dtime_all)
        f107_all = np.array(f107_all) 
        
        #Filter by start and end dates. 
        i = np.where((dtime_all > self.start) & (dtime_all <= self.end)) 
        self.dtime = dtime_all[i]
        self.f107 = f107_all[i] 
    
    
    def read_omni_all(self):
        '''This works out which OMNI files you need to read and concatenates them together.''' 
        
        #Make a list of years. 
        years = np.arange(self.start.year, self.end.year+1) 
        data_yr = [] 
        for y in years:
            filename=f'omni_5min{y}.asc'
            
            #Read in this file. 
            omni_dict = self.read_omni_single(filename=filename)
            data_yr.append(omni_dict) 
        
        #Get keys from first dictionary and print to show what has been extracted. 
        keys = data_yr[0].keys()
        print (keys) 
        
        #Initialise with first dictionary. 
        self.omni_dict = dict.fromkeys(keys, []) 
        
        #Concatenate dictionaries. 
        for key in keys:
            for d in data_yr:
                self.omni_dict[key] = np.concatenate((self.omni_dict[key], d[key])) 
        
        #Now filter by the times exactly. 
        i = np.where((self.omni_dict['dtime'] > self.start) & (self.omni_dict['dtime'] <= self.end))
        for key in keys: 
            self.omni_dict[key] = self.omni_dict[key][i] 
        
        
        
    def read_omni_single(self, filename='omni_5min2026.asc'):  
        '''This reads a single omni file. Code taken from omni2binary.py. ''' 
        
        #Check for presence of file. 
        abs_name = self.data_path+filename 
        assert os.path.exists(abs_name), f'{abs_name} was not found!' 
        
        print (f'Reading {abs_name}...') 
        with open(abs_name, 'r') as f: 
            lines = f.readlines() 
        
        n = len(lines) 
        
        
        #Empty arrays will go here. 
        month = np.ones(n)
        Date = np.ones(n) 
        Dtime = []
        
        Id_imf = np.ones(n)
        Id_plas = np.ones(n)
        No_imf = np.ones(n)
        No_plas = np.ones(n) 
        Per_int = np.ones(n)
        Timeshift = np.ones(n)
        Rms_timeshift = np.ones(n)
        Rms_phase_front = np.ones(n)
        Time_obs = np.ones(n)
        
        B_mag = np.ones(n)
        Bx = np.ones(n)
        By_gse = np.ones(n)
        Bz_gse = np.ones(n)
        By_gsm = np.ones(n)
        Bz_gsm = np.ones(n)
        Rms_B_scalar = np.ones(n)
        Rms_B_vector = np.ones(n)
        
        Flow_speed = np.ones(n)
        Vx = np.ones(n)
        Vy = np.ones(n)
        Vz = np.ones(n)
        Nden = np.ones(n)
        Temp = np.ones(n)
        Pressure = np.ones(n)
        Electric = np.ones(n)
        Beta = np.ones(n)
        Alfven_mach = np.ones(n)
        
        X_sc = np.ones(n)
        Y_sc = np.ones(n)
        Z_sc = np.ones(n)
        Nosex = np.ones(n)
        Nosey = np.ones(n)
        Nosez = np.ones(n)
        
        Ae = np.ones(n)
        Al = np.ones(n)
        Au = np.ones(n)
        Symd = np.ones(n)
        Symh = np.ones(n)
        Asyd = np.ones(n)
        Asyh = np.ones(n)
        Pc = np.ones(n)
        Msonic_mach = np.ones(n) 
        
        #Loop over each line and extract the data. 
        for i, L in enumerate(lines):
            l = L.split() 
            #print (i)
            #Dates (x4)
            yr = l[0]
            dy = l[1]
            hr = l[2]
            mnt = l[3]
            #Convert to a datetime object and then to an appropriate string.  
            dtime = dt.datetime.strptime(yr+' '+dy+' '+hr+' '+mnt, '%Y %j %H %M') 
            Date[i] = dtime.strftime('%Y%m%d%H%M') 
            month[i] = dtime.month
            Dtime.append(dtime)
            
            #Spacecraft stuff (x9)
            Id_imf[i] = np.float64(l[4])
            Id_plas[i] = np.float64(l[5])
            if l[6] == '999': No_imf[i] = np.nan
            else: No_imf[i] = np.float64(l[6])
            if l[7] == '999': No_plas[i] = np.nan
            else: No_plas[i] = np.float64(l[7]) 
            if l[8] == '999': Per_int[i] = np.nan
            else: Per_int[i] = np.float64(l[8])
            if l[9] == '999999': Timeshift[i] = np.nan
            else: Timeshift[i] = np.float64(l[9])
            if l[10] == '999999': Rms_timeshift[i] = np.nan
            else: Rms_timeshift[i] = np.float64(l[10])
            if l[11] == '999999': Rms_phase_front[i] = np.nan
            else: Rms_phase_front[i] = np.float64(l[11])
            if l[12] == '999999': Time_obs[i] = np.nan
            else: Time_obs[i] = np.float64(l[12])
            
            #Magnetic Field (x8) 
            if l[13] == '9999.99': B_mag[i] = np.nan
            else: B_mag[i] = np.float64(l[13])
            if l[14] == '9999.99': Bx[i] = np.nan
            else: Bx[i] = np.float64(l[14])
            if l[15] == '9999.99': By_gse[i] = np.nan
            else: By_gse[i] = np.float64(l[15])
            if l[16] == '9999.99': Bz_gse[i] = np.nan
            else: Bz_gse[i] = np.float64(l[16])
            if l[17] == '9999.99': By_gsm[i] = np.nan
            else: By_gsm[i] = np.float64(l[17])
            if l[18] == '9999.99': Bz_gsm[i] = np.nan
            else: Bz_gsm[i] = np.float64(l[18])
            if l[19] == '9999.99': Rms_B_scalar[i] = np.nan
            else: Rms_B_scalar[i] = np.float64(l[19])
            if l[20] == '9999.99': Rms_B_vector[i] = np.nan
            else: Rms_B_vector[i] = np.float64(l[20])
            
            
            #Solar Wind (x10)
            if l[21] == '99999.9': Flow_speed[i] = np.nan
            else: Flow_speed[i] = np.float64(l[21])
            if l[22] == '99999.9': Vx[i] = np.nan
            else: Vx[i] = np.float64(l[22])
            if l[23] == '99999.9': Vy[i] = np.nan
            else: Vy[i] = np.float64(l[23])
            if l[24] == '99999.9': Vz[i] = np.nan
            else: Vz[i] = np.float64(l[24])
            
            if l[25] == '999.99': Nden[i] = np.nan
            else: Nden[i] = np.float64(l[25])
            if l[26] == '9999999.': Temp[i] = np.nan
            else: Temp[i] = np.float64(l[26])
            if l[27] == '99.99': Pressure[i] = np.nan
            else: Pressure[i] = np.float64(l[27])
            if l[28] == '999.99': Electric[i] = np.nan
            else: Electric[i] = np.float64(l[28])
            if l[29] == '999.99': Beta[i] = np.nan
            else: Beta[i] = np.float64(l[29])
            if l[30] == '999.9': Alfven_mach[i] = np.nan
            else: Alfven_mach[i] = np.float64(l[30])
            
            
            
            
            #Positions of s/c and bowshock nose (x6)
            if l[31] == '9999.99': X_sc[i] = np.nan
            else: X_sc[i] = np.float64(l[31])
            if l[32] == '9999.99': Y_sc[i] = np.nan
            else: Y_sc[i] = np.float64(l[32])
            if l[33] == '9999.99': Z_sc[i] = np.nan
            else: Z_sc[i] = np.float64(l[33])
            if l[34] == '9999.99': Nosex[i] = np.nan
            else: Nosex[i] = np.float64(l[34])
            if l[35] == '9999.99': Nosey[i] = np.nan
            else: Nosey[i] = np.float64(l[35])
            if l[36] == '9999.99': Nosez[i] = np.nan
            else: Nosez[i] = np.float64(l[36])
            
            
            #Ancillary data (x9)
            Ae[i] = np.float64(l[37])
            Al[i] = np.float64(l[38])
            Au[i] = np.float64(l[39])
            Symd[i] = np.float64(l[40])
            Symh[i] = np.float64(l[41])
            Asyd[i] = np.float64(l[42])
            Asyh[i] = np.float64(l[43])
            if l[44] == '99.99': Pc[i] = np.nan
            else: Pc[i] = np.float64(l[44])
            if l[45] == '99.99': Msonic_mach[i] = np.nan
            else: Msonic_mach[i] = np.float64(l[45]) 
        
        #Put all values into one dictionary. 
        #Only pulled out the useful ones so far. 
        omni_dict = {} 
        omni_dict['dtime'] = np.array(Dtime)        
        omni_dict['bx'] = Bx
        omni_dict['by_gse'] = By_gse
        omni_dict['by_gsm'] = By_gsm
        omni_dict['bz_gse'] = Bz_gse
        omni_dict['bz_gsm'] = Bz_gsm
        omni_dict['vx_gse'] = Vx    
        omni_dict['vy_gse'] = Vy    
        omni_dict['vz_gse'] = Vz
        omni_dict['density'] = Nden
        omni_dict['temp'] = Temp
        omni_dict['beta'] = Beta 
        omni_dict['flux'] = 1e5*Vx*Nden
        omni_dict['Al'] = Al
        omni_dict['Au'] = Au
        omni_dict['symh'] = Symh
        
        return omni_dict     
                

    def plot_summary(self, save=False, filetype='pdf'):
        '''This will plot a summary plot. Uses default limits on y axis. ''' 
        
        plt.close("all")
        fig = plt.figure(figsize=(6,8))   
        fig.subplots_adjust(left=0.15, hspace=0.3, bottom=0.05)
        
        n = 7
        ax1 = fig.add_subplot(n,1,1)
        ax2 = fig.add_subplot(n,1,2)
        ax3 = fig.add_subplot(n,1,3)
        ax4 = fig.add_subplot(n,1,4)
        ax5 = fig.add_subplot(n,1,5)
        ax6 = fig.add_subplot(n,1,6)
        ax7 = fig.add_subplot(n,1,7)
        
        #Plot F10.7 
        ax1.plot(self.dtime, self.f107, c='k', lw=0.5)
        #ax2.plot(self.omni_dict['dtime'], self.omni_dict['bx'], c='b', label='bx', lw=0.5)
        #ax2.plot(self.omni_dict['dtime'], self.omni_dict['by_gse'], c='r', label='by', lw=0.5)
        ax2.plot(self.omni_dict['dtime'], self.omni_dict['bz_gse'], c='c', label='bz', lw=0.5)
        ax3.plot(self.omni_dict['dtime'], self.omni_dict['vx_gse'], c='r', label='vx', lw=0.5) 
        ax4.plot(self.omni_dict['dtime'], self.omni_dict['density'], c='g', label='n', lw=0.5)
        ax5.plot(self.omni_dict['dtime'], self.omni_dict['beta'], c='purple', label='beta', lw=0.5) 
        ax6.plot(self.omni_dict['dtime'], self.omni_dict['symh'], c='k', label='symh', lw=0.5) 
        ax7.plot(self.omni_dict['dtime'], self.omni_dict['Au'], c='darkblue', label='Au', lw=0.5) 
        ax7.plot(self.omni_dict['dtime'], self.omni_dict['Al'], c='b', label='Au', lw=0.5) 
        
        ax1.set_ylabel('F10.7 \nsfu]') 
        ax2.set_ylabel('Bz GSE\n[nT]')
        ax3.set_ylabel('Vx\n[km/s]')
        ax4.set_ylabel('Density\n'+r'[cm$^{-3}$]')      
        ax5.set_ylabel('Beta\n')
        ax6.set_ylabel('Sym H\n[nT]') 
        ax7.set_ylabel('Au/Al\n[nT]') 
        
        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()
        ax6.grid()
        ax7.grid()
        
        ts.NewTimeAxis(ax1, self.start, self.end, fontsize=8, UT=False)
        ts.NewTimeAxis(ax2, self.start, self.end, fontsize=8, UT=False)
        ts.NewTimeAxis(ax3, self.start, self.end, fontsize=8, UT=False)
        ts.NewTimeAxis(ax4, self.start, self.end, fontsize=8, UT=False)
        ts.NewTimeAxis(ax5, self.start, self.end, fontsize=8, UT=False)
        ts.NewTimeAxis(ax6, self.start, self.end, fontsize=8, UT=False)
        ts.NewTimeAxis(ax7, self.start, self.end, fontsize=8, UT=False)
        
        #Put standard y limits in place. 
        ax1.set_ylim(0,300)
        ax2.set_ylim(-20,20)
        ax3.set_ylim(-800,0)
        ax4.set_ylim(0,60)
        ax5.set_ylim(0,5)
        ax6.set_ylim(-200,20)
        ax7.set_ylim(-500,500)
        
        #Add title information. 
        now = dt.datetime.now()
        fig.text(0.15, 0.9, f"F10.7/OMNI Report\nCreated: {now.strftime('%Y-%m-%d %H:%M')}", ha='left') 

        fig.text(0.90, 0.9, f"Start date: {self.start.strftime('%Y-%m-%d')}\nEnd date: {self.end.strftime('%Y-%m-%d')}", ha='right') 

        if save: 
        
            assert filetype in ['pdf', 'png'], f'{filetype} not a valid file ending.' 
            
            st = self.start.strftime('%Y%m%d-%H%M%S') 
            en = self.end.strftime('%Y%m%d-%H%M%S') 
            figname = f'Env_report_{st}_{en}.{filetype.lower()}'
        
        
            fig.savefig(self.report_path+figname) 
            
            assert os.path.exists(self.report_path+figname), f'{self.report_path+figname} was not made!'
            print (f'Saved: {self.report_path+figname}') 


if __name__ == "__main__":
    plot() 
