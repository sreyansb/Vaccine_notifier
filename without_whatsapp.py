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
        try:
            response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params2,timeout=10)
        except Exception as E:
            engine.say(str(E))
            engine.runAndWait()
            sleep(10)
            break
        print(response)
        final=response.json()
        try:
            if final["sessions"]:
                for i in final["sessions"]:
                        if i['available_capacity_dose1'] and i["vaccine"]=="COVAXIN" and i['min_age_limit']==18 :
                            print(i["name"],i["pincode"],i['available_capacity_dose1'])
                            engine.say((i["name"],i['available_capacity_dose1']))
                            engine.runAndWait()
                            winsound.Beep(750,800)    
                            di.append(({"D":f,"N":i['name'],"Cap":str(i['available_capacity_dose1']),"Add":i['address'],"F":i['fee'],"V":str(i["vaccine"]),"S":i["session_id"],"sl":i["slots"]}))
                            print(di[-1])
                    #print(di)
        except:
            engine.say("ERROR")
            engine.runAndWait()
            winsound.Beep(600,800)
        t=t+timedelta(days=1)
        flag-=1
    if di:
        fi=open("alreadysent.csv","a")
        for i in di:
            fi.write(f+","+i["N"]+","+i["Cap"]+","+i["V"]+"\n")
        fi.close()
        winsound.Beep(600,800)
    sleep(12)
engine.say("LOOP OVER")
engine.runAndWait()
winsound.Beep(600,800)
