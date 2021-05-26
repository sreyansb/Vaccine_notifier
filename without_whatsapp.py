import json
import requests
from datetime import datetime,date,timedelta
import time
from time import sleep
import winsound

import pyttsx3
engine=pyttsx3.init()
engine.setProperty('rate',225)
engine.setProperty('volume',1.0)

while(True):
    t=date.today()#+timedelta(days=1)
    k=time.localtime()
    if k.tm_hour>=17:
        t=t+timedelta(days=1)
    #print(t)
    #winsound.Beep(750,800)
    #params1={"district_id":294,"date":t}
    #params2={"district_id":265,"date":t}
    keyval=0
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"}
    flag=2
    di=[]
    while(flag):
        f=t.strftime("%d-%m-%Y")
        print(f)
        params2={"district_id":294,"date":f}
        response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params2)
        print(response)
        final=response.json()
        #print(final)
        try:
            if final["sessions"]:
                for i in final["sessions"]:
                        if  i["vaccine"]=="COVAXIN" and i['available_capacity_dose1'] and i['min_age_limit']==18 :
                            print(i["name"],i["pincode"])
                            engine.say((i["name"],i['available_capacity_dose1']))
                            engine.runAndWait()
                            di.append(({"P":i["pincode"],"D":f,"N":i['name'],"Cap":i['available_capacity_dose1'],"Add":i['address'],"F":i['fee'],"V":i["vaccine"],"S":i["session_id"],"sl":i["slots"]}))
                    #print(di)
        except:
            winsound.Beep(600,800)
        t=t+timedelta(days=1)
        flag-=1
    if di:
            di=check_in_file(di)
            if di:
                winsound.Beep(600,800)
    sleep(15)
winsound.Beep(600,800)
