from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
from datetime import datetime,date,timedelta
import time
from time import sleep
import winsound
import pyttsx3
engine=pyttsx3.init()
engine.setProperty('rate',250)
engine.setProperty('volume',1.0)

def check_in_file(di):
    return di

def send_whatsapp_message(event):
    x=["me"]
    PATH="C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/sreyans/yo/User_Data')
    print(event)
    driver = webdriver.Chrome(executable_path=PATH,options=options)
    driver.get('https://web.whatsapp.com/')
    try:
        #wait for max 200s
        #whatsapp loads but the search button does not appear and hence WebDriverWait to wait until search loads
        initi = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]")))
        #initi = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CLASS_NAME, "C28xL")))
        
        for target in x:
            #print("Wishing",target,"on their",event)
            input_box_search=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')
            input_box_search.click()
            input_box_search.send_keys(target,Keys.ENTER)
            print("Target Successfully Selected")
            sleep(1)

            inp_xpath = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
            input_box = WebDriverWait(driver,20).until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            sleep(0.1)
            for string in event:
                input_box.send_keys(str(string))
                sleep(0.01)
                input_box.send_keys(Keys.SHIFT+Keys.ENTER)
            input_box.send_keys("https://selfregistration.cowin.gov.in")
            input_box.send_keys(Keys.ENTER)
            sleep(1)
            print("Successfully Send Message to : "+ target + '\n')
            print("DONE")
    except Exception as E:
        print(E)
    finally:
        print("DONE all")
        f=open("alreadysent.csv","a")
        fin=[]
        for i in event:
            f.write(i["D"]+","+i["N"]+","+str(i["Cap"])+","+i["V"]+"\n")
        f.close()
        #whenever qr code dena padega, usko driver.quit() nahi karke
        #khud hi quit karna hoga->manually
        driver.quit()
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
                        if  i["vaccine"]=="COVAXIN" and i['min_age_limit']==18 and i['available_capacity_dose1'] :
                            print(i["name"],i["pincode"])
                            engine.say((i["name"],i["pincode"][-3],i["pincode"][-2],i["pincode"][-1],i['available_capacity_dose1']))
                            engine.runAndWait()
                            di.append(({"P":i["pincode"],"D":f,"N":i['name'],"Cap":i['available_capacity_dose1'],"Add":i['address'],"F":i['fee'],"V":i["vaccine"],"S":i["session_id"],"sl":i["slots"]}))
                    #print(di)
        except:
            winsound.Beep(600,800)
        t=t+timedelta(days=1)
        flag-=1
    if di:
            send_whatsapp_message(di)
    sleep(15)
winsound.Beep(600,800)
