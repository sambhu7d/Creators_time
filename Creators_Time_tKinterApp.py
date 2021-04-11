#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:16:13 2020
@author: sambhu7d
"""
import pip
import time


def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


while True:
    
    try:
        modules=['requests','geocoder','tkinter','datetime']
        for module in modules:
            install(module)   
        break
    except:
        print('Bad Internet Connection')
        time.sleep(5)


import requests as rq
import datetime
import geocoder
import tkinter as tk





class backend(object):
    
    def __int__(self):
        self.sunrise=''
        self.sunset=''
        self.mrg_bg=''
        self.mrg_ed=''
        self.eve_bg=''
        self.eve_ed=''
         
    def check(self,ttt):
        try:
            int(ttt[-1])
            if len(ttt)!=8:
                ttt='0'+ttt
        except:
            if len(ttt)!=11:
                ttt='0'+ttt
            
        finally:
            return ttt
    
    def convert24(self,str1): 
         
        # Checking if last two elements of time 
        # is AM and first two elements are 12 
        if str1[-2:] == "AM" and str1[:2] == "12": 
            return "00" + str1[2:-2] 
            
                 
        # remove the AM     
        elif str1[-2:] == "AM": 
            return str1[:-2] 
          
        # Checking if last two elements of time 
        # is PM and first two elements are 12    
        elif str1[-2:] == "PM" and str1[:2] == "12": 
            return str1[:-2] 
              
        else: 
              
            # add 12 to hours and remove PM 
            return str(int(str1[:2]) + 12) + str1[2:8]    
    
    def sec(self,time):
        hh,mm,ss=time.split(":")   
        return int(ss)+(int(mm)*60)+(int(hh)*3600)
        
    def convert(self,seconds): 
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
          
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def main(self):
        
        g = geocoder.ip('me')
        lat=str(g.lat)
        lng=str(g.lng)
        
        t=str(datetime.date.today() + datetime.timedelta(days=1))
        
        def zone():
            z=time.timezone
            if z>0:
                z=self.convert(z)
                return -self.sec(z)
                
            elif z<0:
                z=abs(z)
                z=self.convert(z)
                return +self.sec(z)
                
        url='https://api.sunrise-sunset.org/json?lat='+lat+'&lng='+lng+'&date='+t
        r=rq.get(url)             #data not readable for python
        j=r.json()                #readable data from r to json
        
        sr=self.check(j['results']['sunrise'])
        ss=self.check(j['results']['sunset'])
        
        self.sunrise=self.check(self.convert(self.sec(self.convert24(sr))+zone()))
        self.sunset=self.check(self.convert(self.sec(self.convert24(ss))+zone()))
        
        # print("sunrise = "+ self.sunrise)
        # print("sunset  = "+ self.sunset)
        
        self.mrg_bg=self.check(self.convert(self.sec(self.sunrise)-self.sec("01:36:00")))
        self.mrg_ed=self.check(self.convert(self.sec(self.mrg_bg)+self.sec("00:48:00")))
        
        self.eve_bg=self.check(self.convert(self.sec(self.sunset)-self.sec("01:36:00")))
        self.eve_ed=self.check(self.convert(self.sec(self.eve_bg)+self.sec("00:48:00")))
        
        # print("\n")
        # print("Brahma Muhrat Morning Time ")
        # print("\t"+self.mrg_bg+"--"+self.mrg_ed)
        
        # print("\n")
        # print("Brahma Muhrat Evening Time ")
        # print("\t"+self.eve_bg+"--"+self.eve_ed)
            
class frontend(backend):
    def __init__(self):
        self.main()
        backend.__init__(self)
        
    def display(self):
        root=tk.Tk() #Frame #tk.Tk()
        root.title("Brahma Muhrat App")  
        root.geometry("400x400+500+0")
        
        srt=tk.Label(root,fg='YELLOW',text='SUNRISE \n'+str(self.sunrise),bg='ORANGE')
        srt.place(x=40,y=0)
        
        sst=tk.Label(root,fg='YELLOW',text='SUNSET \n'+str(self.sunset),bg='ORANGE')
        sst.place(x=270,y=0)
     
        bmm=tk.Label(root,fg='Red',text='Morning Time \n'+str(self.mrg_bg)+'--'+str(self.mrg_ed),bg='white')
        bmm.place(x=120,y=40)
        
        bme=tk.Label(root,fg='Red',text='Evening Time \n'+str(self.eve_bg)+'--'+str(self.eve_ed),bg='white')
        bme.place(x=120,y=80)
        
        
        root.mainloop()
            
obj=frontend()
obj.display()