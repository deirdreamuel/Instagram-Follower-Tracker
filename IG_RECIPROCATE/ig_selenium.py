import time
import random
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class reciprocate:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        chrome_options = Options()  #run browser in the background
        chrome_options.add_argument("--headless")  
        self.browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)

    def endReciprocate(self):
        self.browser.close()

    def login(self):
        # go to instagram login page
        browser = self.browser
        browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(2)
        # --------------------------

        # fill username & password => log in!
        userINPUT = browser.find_element_by_xpath("//input[@name='username']")
        userINPUT.clear()
        userINPUT.send_keys(self.username)
        #---------------------------------
        passINPUT = browser.find_element_by_xpath("//input[@name='password']")
        passINPUT.clear()
        passINPUT.send_keys(self.password)
        passINPUT.send_keys(Keys.RETURN)

        time.sleep(3)

    def getFollowers(self, count):
        followerCount = count

        #open up followers window
        browser = self.browser
        followersList = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
        followersList.click()   
        time.sleep(2)

        #scroll through followers window to load all followers
        fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
        while followerCount > 0:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(.5)
            followerCount -= 5

        #get all the data in pop-up window
        followersDATA = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div")
        followersDATA = followersDATA.text

        #extract followers and return as array
        followersList = self.extractProfiles(followersDATA, count)
        browser.get("https://www.instagram.com/" + self.username + '/')
        time.sleep(2)
        return followersList


    def getFollowing(self, count):
        followCount = count

        #open up following pop-window
        browser = self.browser
        followingList = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a")
        followingList.click()
        time.sleep(2)

        #scroll through following pop-window to load all followers
        fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
        while followCount > 0:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(.5)
            followCount -= 5

        #get data in pop-up window as text
        followingDATA = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div")
        followingDATA = followingDATA.text

        #extract following and return as array
        followingList = self.extractProfiles(followingDATA, count)
        browser.get("https://www.instagram.com/" + self.username + '/')
        time.sleep(2)
        return followingList

    def extractProfiles(self, s, limit):
        usernames = []
        arr = s.split('\n')

        for i, name in enumerate(arr):
            if (arr[i-1] == 'Following' or arr[i-1] == 'Follow' or arr[i-1] == 'Requested'):
                usernames.append(name)

        return sorted(usernames)

    def getProfileStats(self):
        browser = self.browser
        browser.get("https://www.instagram.com/" + self.username + '/')
        time.sleep(3)

        #extract profile stats
        profile_elem = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div")
        profile = profile_elem.text
        profile_arr = profile.split('\n')
        return profile_arr[:7]
# ---------------------------