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
        self.browser = webdriver.Chrome()

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
        #------------------------------------

        # !!!! try with pressing tab instead of find password path
        passINPUT = browser.find_element_by_xpath("//input[@name='password']")
        passINPUT.clear()
        passINPUT.send_keys(self.password)
        passINPUT.send_keys(Keys.RETURN)

        time.sleep(3)

    def getFollowers(self, count):
        followerCount = count
        browser = self.browser
        followersList = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
        followersList.click()
        time.sleep(2)

        fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
        while count > 0:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(.5)
            count -= 6

        #prints out all the followers in pop-up window
        followersDATA = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]")
        followersDATA = followersDATA.text

        followersList = extractProfiles(followersDATA, followerCount)
        browser.get("https://www.instagram.com/" + self.username + '/')
        time.sleep(2)
        return followersList


    def getFollowing(self, count):
        followCount = count
        browser = self.browser
        followingList = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a")
        followingList.click()
        time.sleep(2)

        fBody = browser.find_element_by_xpath("//div[@class='isgrP']")
        while count > 0:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(.5)
            count -= 5

        # prints out all the followers in pop-up window
        followingDATA = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]")
        followingDATA = followingDATA.text

        followingList = extractProfiles(followingDATA, followCount)
        browser.get("https://www.instagram.com/" + self.username + '/')
        time.sleep(2)
        return followingList


    def getProfileStats(self):
        browser = self.browser
        browser.get("https://www.instagram.com/" + self.username + '/')
        time.sleep(3)

        profile_elem = browser.find_element_by_xpath("//span[@id = 'react-root']")
        profile = profile_elem.text
        profile_arr = profile.split('\n')
        return profile_arr[:7]

    def unfollowUsers(self, unfollowArr):
        browser = self.browser
        for user in unfollowArr:
            browser.get("https://www.instagram.com/" + user + '/')
            time.sleep(3)
            unfollowUser = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/ header / section / div[1] / button")
            unfollowUser.click()

            time.sleep(5)



# ---------------------------
def unfollowing(followers, following):
    unfollowArr = []
    index = 0
    for user in following:
        followingBack = False
        while True:
            if followers[index] == user:
                followingBack = True
                break
            elif followers[index] > user:
                break
            index += 1
        if not followingBack:
            unfollowArr.append(user)

    return unfollowArr

def extractProfiles(s, limit):
    usernames = []
    arr = s.split('\n')

    index = 0
    while limit > 0:
        usernames.append(arr[index])
        if index + 1 > len(arr):
            break
        elif arr[index + 1] == 'Verified':
            index += 1

        if isProfileName(arr[index + 1]):
            index += 2
        else:
            index += 3
        limit -= 1
    return sorted(usernames)

def isProfileName(s):
    if (s == 'Following') or (s == 'Follow') or (s == 'Requested'):
        return True
    else:
        return False

def extractCount(s):
    arr = s.split()
    return arr[0]

if __name__ == "__main__":

    username = input("USERNAME: ")
    password = input("PASSWORD: ")

    ig = reciprocate(username, password)
    ig.login()

    profile = ig.getProfileStats()
    profileName = profile[5]
    profileBio = profile[6]
    followersCount = extractCount(profile[3])
    followingCount = extractCount(profile[4])
    postsCount = extractCount(profile[2])

    print("Profile Name: " + profileName)
    print("Profile Bio: " + profileBio)
    print("Followers: " + followersCount)
    print("Following: " + followingCount)

    followers = ig.getFollowers(int(followersCount))

    print("----------------------------------------------------------")

    following = ig.getFollowing(int(followingCount))

    print(followers,'\n',following)

    unfollow = unfollowing(followers, following)

    for i in unfollow:
        print (i)

    print("unreciprocated count: ", len(unfollow))


    closeAuthorization = input("press q to close: ")
    if closeAuthorization == 'q':
        ig.endReciprocate()



