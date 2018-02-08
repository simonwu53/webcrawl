from bs4 import BeautifulSoup
from selenium import webdriver
import pickle
import time
import os

# with open('html/pics2.html') as f:
#     soup = BeautifulSoup(f, 'lxml')
#     pics = soup.find_all('img', class_='spotlight')
#     print(len(pics))
#     url = pics[0]['src']
#
# chrome = webdriver.Chrome()
# page = 'https://www.facebook.com'
# chrome.get(page)  # open url
# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
#     chrome.add_cookie(cookie)
# # refresh
# chrome.refresh()
# time.sleep(1)
# chrome.get(url)
# img = chrome.find_element_by_xpath('/html/body/img')
# location = img.location
# size = img.size
# print(location)
# print(size)
# chrome.save_screenshot('img.png')

# im = Image.open('img.png')
# left = location['x']
# top = location['y']
# right = left + 700
# bottom = top + 700
# im = im.crop((left,top,right,bottom))
# im.save('img.png')

# chrome.quit()

# albums = soup.find_all('span', class_='_2ieo _50f7')
# for album in albums:
#     if album.string == 'Profile Pictures':
#         url = album.parent.parent.parent.parent.parent['href']
#         print(url)

# for i in range(len(url)):
#     print(url[i])
#     input('press enter to continue')

lst = []
if not lst:
    print('111')
