from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import instaloader
from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Button, Controller
import random

#MAKE SURE YOU HAVE THE CORRECT CHROMEDRIVER/webdriver VERSION

class Instabot():
    #create instance of instabot
    def __init__(self, username, password):
        self.username=username
        self.password=password
        #make sure chromedriver is in folder with this file
        self.driver=webdriver.Chrome('./chromedriver')
        self.L=instaloader.Instaloader()
        #logs into instaloader to retrieve follower data
        self.L.login(username, password)
        self.mouse=Controller()

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        username_box=self.driver.find_element_by_name('username')
        password_box=self.driver.find_element_by_name('password')
        username_box.send_keys(self.username)
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.ENTER)
        time.sleep(2)
        #clicks away the notification
        notif=self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        notif.click()
        self.driver.maximize_window()
        
    def close(self):
        time.sleep(3)
        self.driver.close()

    def follow(self, account_name):
        #follows all the FOLLOWEES (people that account follows) of an account
        self.profile=instaloader.Profile.from_username(self.L.context, account_name)
        followees=self.profile.get_followees()
        for followee in followees:
            self.driver.get("https://www.instagram.com/"+followee.username+"/")
            button=self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")
            button[0].click()
            #REST INTERVAL
            time.sleep(60)


    def unfollow(self, account_name):
        #unfollos everyone from your own followers list
        #working
        self.profile=instaloader.Profile.from_username(self.L.context, account_name)
        followees=self.profile.get_followees()
        for followee in followees:
            self.driver.get("https://www.instagram.com/"+followee.username+"/")
            button=self.driver.find_elements_by_tag_name("button")
            button[0].click()
            time.sleep(3)
            #hardcoded coordinates
            self.mouse.position=(636.71875, 509.625)
            self.click()
            self.click()
            time.sleep(15)

    def click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
    

    
    def like_photo(self, hashtag):
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        #increase range if you want more photos
        for i in range(1, 4):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            self.driver.get(pic_href)
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                like_button = lambda: self.driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(1)
            except Exception as e:
                time.sleep(2)
            unique_photos -= 1
                 
        
#SET UP ACCOUNT:
##bot=Instabot('USERNAME', 'PASSWORD')
##bot.login()

#IMPLEMENT FUNCTIONS            
#bot.follow('#accountusername')
#bot.unfollow(#yourusername)
#bot.like_photo('#hashtag')
#bot.close()





    
        
