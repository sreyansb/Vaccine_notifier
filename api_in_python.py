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


def check_in_file(di):#to check that I haven't sent the same place for the same date before
    f=open("alreadysent.csv","a+")
    f.seek(0)
    l=set(f.readlines())
    print(l)
    fin=[]
    for i in di:
        if i["date"]+","+i["Name"]+"\n" not in l:
            fin.append(i)
    for i in range(len(fin)):
        f.write(fin[i]["date"]+","+fin[i]["Name"]+"\n")
        fin[i]=str(fin[i])
    f.close()
    #print(fin)
    return fin

def send_whatsapp_message(event):
    x=["me"]
    PATH="C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/sreya/yo/User_Data')

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
            sleep(0.5)
            for string in event:
                input_box.send_keys(string)
                sleep(0.5)
                input_box.send_keys(Keys.SHIFT+Keys.ENTER)
            time.sleep(0.5)
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
            print("Successfully Send Message to : "+ target + '\n')
            print("DONE")
    except Exception as E:
        print(E)
    finally:
        print("DONE all")
        #whenever qr code dena padega, usko driver.quit() nahi karke
        #khud hi quit karna hoga->manually
        driver.quit()

t=date.today()#+timedelta(days=1)
k=time.localtime()
if k.tm_hour>=17:
    t=t+timedelta(days=1)
t=t.strftime("%d-%m-%Y")
print(t)

params1={"district_id":294,"date":t}#for BBMP
params2={"district_id":265,"date":t}#for Bangalore Urban
keyval=0
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"}
flag=2
di=[]
while(flag):
    if keyval:
        response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params2)
    else:
        response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params1)
    print(response)
    final=response.json()
    #print(final)
    
    if final["sessions"]:
        vals=0
        for i in final["sessions"]:
            if i['available_capacity'] and i['min_age_limit']==18:
                if vals:
                    di.append(({"date":t,"Name":i['name'],"1st dose capacity":i['available_capacity_dose1'],"2nd dose capacity":i['available_capacity_dose2'],"Address":i['address'],"Fees":i['fee'],"Vaccine":i["vaccine"]}))
                else:
                    di.append(({"date":t,"Name":i['name'],"1st dose capacity":i['available_capacity_dose1'],"2nd dose capacity":i['available_capacity_dose2'],"Address":i['address'],"Fees":i['fee'],"Vaccine":i["vaccine"]}))
                vals^=1
        #print(di)
    flag-=1
    sleep(1)
    keyval^=1
if di:
        di=check_in_file(di)
        if di:
            send_whatsapp_message(di)
