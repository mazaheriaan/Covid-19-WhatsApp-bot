from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import Message
import pyperclip
import os
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))
driver=webdriver.Firefox(executable_path=dir_path+'/geckodriver')
driver.get("https://web.whatsapp.com")
input("prees any key to continue...")
greenCircleClass='OUeyt'
newMessageClass='_1wjpf'
wait = WebDriverWait(driver,3600)
        
def ConvertPersinanToEnglish(n):
    n=n.replace('۰','0').replace('۱','1').replace('۲','2').replace('۳','3').replace('۴','4').replace('۵','5').replace('۶','6').replace('۷','7').replace('۸','8').replace('۹','9')
    return n

def Send(msg):
    wait.until(ec.element_to_be_clickable((By.XPATH,'//div[@spellcheck="true"]')))
    txtBox=driver.find_element_by_xpath('//div[@spellcheck="true"]')
    txtBox.click()
    if (msg.endswith('.png') or msg.endswith('.jpg'))==False:
        pyperclip.copy(msg)
        txtBox.send_keys(Keys.CONTROL+'V')
        txtBox.send_keys(Keys.ENTER)
    else:
        subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', dir_path+'/'+msg])
        txtBox.send_keys(Keys.CONTROL+'V')
        wait.until(ec.element_to_be_clickable((By.CLASS_NAME,'_2gZno')))
        driver.find_element_by_class_name('_3hV1n').click()

    
def Response(q):
    if q.startswith('بیمارستان') and 'کرونا'  not in q:
        q=q.split( )
        if len(q)>1:
            return Message.Hospital(' '.join(q[1:]))
    elif  q.startswith('شیوع'):
        q=q.split( )
        if len(q)>1:
            return Message._WorldCloud(' '.join(q[1:]))
    try:
        return Message.response[q]
    except:
        return ''
read=True

while read:
    #isNewMessage=False
    try:
        wait.until(ec.presence_of_element_located((By.CLASS_NAME,greenCircleClass)))
        newMessages=driver.find_elements_by_class_name(greenCircleClass)

        for newMessage in newMessages:
            parent=newMessage.find_element_by_xpath("../../../..")
            parent.click()
            #keyboard.press_and_release('ctrl+k')
            messageText=parent.find_element_by_class_name(newMessageClass).text

            messageText=messageText.replace('آ','ا')

            if Response(ConvertPersinanToEnglish(messageText))!='':
                parent.click()
                Send(Response(ConvertPersinanToEnglish(messageText)))

    except Exception as e:
        print(str(e))
                

driver.close()
driver.quit()
