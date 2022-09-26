from asyncore import write
import csv
from getpass import getpass
from lib2to3.pgen2 import driver
from optparse import Option
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions
#from twitter_scraper_things import getTweetData

#function to extract all infos
def getTweetData(card):                                                                         

    username = card.find_element_by_xpath('.//span').text                                           
    atUsername = card.find_element_by_xpath('.//span[contains(text(), "@")]').text 
    try:
        timeStamp = card.find_element_by_xpath('.//time').get_attribute('datetime') 
    except NoSuchElementException:                                                              
        return
    tweetText = card.find_element_by_xpath('.//div[@data-testid="tweetText"]').text
    replyCnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text                  
    reTweetCnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text              
    likesCnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text                  

    return (username, atUsername, timeStamp, tweetText, replyCnt, reTweetCnt, likesCnt)

#Create instance of web driver
options = EdgeOptions()
options.use_chromium = True
driver = Edge(options=options)

#Navigate to login screen
driver.get('https://twitter.com/login')
driver.maximize_window()
sleep(5)

#Enter the username/email
username = driver.find_element_by_xpath('//input[@name="text"]')                                
username.send_keys('TwittyScrapy')                                                              
username.send_keys(Keys.RETURN)                                                                 
sleep(3)   

#Enter the password
my_password = getpass()
password = driver.find_element_by_xpath('//input[@name="password"]')                            
password.send_keys(my_password)                                                              
password.send_keys(Keys.RETURN)                                                                 
sleep(3)  

#Search term
search_input = driver.find_element_by_xpath('//input[@aria-label="Consulta de busca"]')         
search_input.send_keys('futebol')                                                              
search_input.send_keys(Keys.RETURN)                                                            
sleep(3)                                                                             

#Navigate to historical 'Principais' tab
driver.find_element_by_link_text('Principais').click()                                       
sleep(3)

#Get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True
while scrolling:
    page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
    for card in page_cards[-15:]:                                                               #Look ate the last 15 tweet because the continuous growing of the page
        tweet = getTweetData(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
    scroll_attempt = 0  
    while True:                                                                                 #Preventing the slow speed of internet
        #Check the scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            #End of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2)                                                                        #Attempt to scroll again
        else:
            last_position = curr_position
            break

print(len(data))

#Saving the tweet data
with open('futebol_tweets.csv', 'w', newline='', encoding='utf-8') as f:
    header = {'Username', 'Handle', 'Timestamp', 'Comments', 'Likes', 'Retweets', 'Text'}
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)