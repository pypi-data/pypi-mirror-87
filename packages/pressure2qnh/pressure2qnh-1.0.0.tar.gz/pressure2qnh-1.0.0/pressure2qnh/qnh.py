import numpy as np

class CorrectPressure:
    
    def __init__(self, Temperature_sensor, Pressure_sensor, Latitude, station_height):
        self.Temp = Temperature_sensor #Degree celsius
        self.P0 = Pressure_sensor #hPa from sensor
        self.Lat = Latitude# Decimal
        self.H = station_height #Meter
        
    def cal_qnh(self):
        lat_zeta = self.Lat*(np.pi/180) #Change Decimal to Radient
        a = 0.002637*np.cos(2*lat_zeta)
        b1 = ((np.cos(2*lat_zeta))+1)/2
        b = 0.0000059*(b1)
        ab = (9.80616/9.80665)*(1 - a + b)
        
        Cg = (ab-1)*self.P0 #Optimize gravity effect value
        
        Cgh = ((-3.147)*(np.power(0.1,7))*self.H)*self.P0 #Optimize station height value

        Pgh = self.P0 + (Cg + Cgh) #Corrected station pressure
        
        Tmsl = self.Temp/100 
        #Lapse rate 1 degree celsiue per 100 meters
        #Tmsl is temperature at mean sea level pressure
        
        Tm = (self.Temp+Tmsl)/2 #Tm is average temperature
        s1 = 1 + (0.00367*Tm)
        s = self.H/(7991.15*s1)
        Pdelta = (np.exp(s)-1)*Pgh
        
        Pmsl = Pgh + Pdelta
        
        print(Pmsl)
        
        return Pmsl