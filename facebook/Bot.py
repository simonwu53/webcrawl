from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from bs4 import BeautifulSoup
import pickle
import time
import os
from glob import glob
from PIL import Image


class Bot:
    def __init__(self, admin=False, usecookie=False):
        print('Application Started...')
        print('Initializing...')
        self.ADMIN = admin
        self.usecookie = usecookie
        self.chrome = webdriver.Chrome()
        self.friendlist = []
        self.friendlink = []
        self.usrname = ''
        self.password = ''
        # auto login
        if self.usecookie:
            self.auto_login_by_cookie()
        else:
            self.auto_login()
            self.save_cookies()  # save cookies for future use

    def auto_run(self):
        # run whole process
        self.get_friendlist()
        self.download_bot(mode=True)
        return

    def auto_login(self):
        print('Automation Bot Started...')

        # get username & pw
        if not self.ADMIN:
            self.usrname = str(input('Please input your email account: \n'))
            self.password = str(input('Please input your password: \n'))
        else:
            self.usrname = 'your account'
            self.password = 'your password'

        url = 'https://www.facebook.com'
        self.chrome.get(url)  # open url
        time.sleep(2)  # waiting for loading

        # login by username & pw
        email = self.chrome.find_element_by_name('email')
        email.send_keys(self.usrname)
        pw = self.chrome.find_element_by_name('pass')
        pw.send_keys(self.password)
        pw.send_keys(Keys.ENTER)

        # 2-step Authenticator
        try:
            code = self.chrome.find_element_by_name('approvals_code')
            print('Two Factor Authentication Required: ')
            tempcode = input('Please input your two factor authencation code: \n')
            while True:
                if tempcode.isdigit():
                    code.send_keys(str(tempcode))
                    break
                else:
                    print('Wrong input! Please input digital numbers!')
                    tempcode = input('Please input your two factor authencation code: \n')
            code.send_keys(Keys.ENTER)
            time.sleep(2)  # waiting for loading next page
            dontsave = self.chrome.find_element_by_id('u_0_3')  # don't save browser
            dontsave.click()
            submitbutton = self.chrome.find_element_by_id('checkpointSubmitButton')  # submit
            submitbutton.click()
            print('Login Success!')
        except NoSuchElementException as e:
            pass  # no 2-step authentication
        time.sleep(2)
        return

    def auto_login_by_cookie(self):
        print('Automation Bot Started...')
        # open url
        url = 'https://www.facebook.com'
        self.chrome.get(url)  # open url
        # add cookies
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.chrome.add_cookie(cookie)
        # refresh
        self.chrome.refresh()
        print('Login Success!')
        time.sleep(2)  # waiting for loading
        return

    def save_cookies(self):
        if os.path.isfile('cookies.pkl'):
            os.remove('cookies.pkl')
        cookies = self.chrome.get_cookies()
        pickle.dump(cookies, open('cookies.pkl', 'wb'))
        print('Cookies saved!')
        return

    def get_friendlist(self):
        # get friends list
        print('Getting Friends List...')
        # goto profile
        soup = BeautifulSoup(self.chrome.page_source, 'lxml')
        url = soup.find('a', class_='_2s25 _606w')['href']
        self.chrome.get(url)
        time.sleep(2)
        # goto friends
        soup = BeautifulSoup(self.chrome.page_source, 'lxml')
        url = soup.find_all('a', class_='_6-6')[2]['href']
        self.chrome.get(url)
        time.sleep(2)
        # scroll to bottom to load all friends
        self.scroll_down()
        # get friend list
        soup = BeautifulSoup(self.chrome.page_source, 'lxml')
        friends = soup.find_all('div', class_='fsl fwb fcb')
        for friend in friends:
            self.friendlist.append(friend.a.string)
            self.friendlink.append(friend.a['href'])
        print('Friend list load complete!')
        print('Total Friends: %d' % len(self.friendlist))
        self.save_friendlist()  # save friendlist for future use
        time.sleep(2)  # waiting for next
        return

    def save_friendlist(self):
        dumpfiles = glob('friend*.txt')
        for file in dumpfiles:
            os.remove(file)

        with open('friendlist.txt', 'w') as f:
            for i in range(len(self.friendlist)):
                if self.friendlink[i] == '#':
                    pass
                else:
                    f.write(self.friendlist[i] + '\t' + self.friendlink[i] + '\n')
        # with open('friendlist.txt', 'w') as f:
        #     for name in self.friendlist:
        #         f.write(name + '\n')
        # with open('friendlink.txt', 'w') as f:
        #     for link in self.friendlink:
        #         if link == '#':
        #             pass
        #         else:
        #             f.write(link + '\n')
        print('Friendlist saved!')
        return

    def download_bot(self, mode=False):  # False->run separately, True->run by auto_bot
        print('Start downloading pics...')
        # check directory for pics
        if not os.path.exists('./pics/'):
            os.makedirs('./pics/')
        # check mode
        if mode:
            links = self.friendlink
            names = self.friendlist
        else:
            with open('friendlist.txt', 'r') as f:
                names = []
                links = []
                for person in f:
                    info = person.split('\t')
                    names.append(info[0])
                    links.append(info[1][:-1])  # delete '\n' while appending
        count = 0  # name list index
        for link in links:
            j = 0  # pic counter
            # set friend directory
            name = names[count]
            path = './pics/' + name
            if not os.path.exists(path):
                os.makedirs(path)
            print('Process: %d. Name: %s' % (count+1, name))
            # open friend's profile
            self.chrome.get(link)
            # get photos' page
            soup = BeautifulSoup(self.chrome.page_source, 'lxml')
            url = soup.find_all('a', class_='_6-6')[3]['href']
            self.chrome.get(url)
            time.sleep(1)
            # get albums' page
            soup = BeautifulSoup(self.chrome.page_source, 'lxml')
            url = soup.find_all('a', class_='_3c_')
            try:
                if url[1].span.string == 'Albums':
                    url = url[1]['href']
                else:
                    url = url[2]['href']
            except IndexError as e:
                count += 1
                continue
            self.chrome.get(url)
            time.sleep(1)
            # open profile picture album
            soup = BeautifulSoup(self.chrome.page_source, 'lxml')
            albums = soup.find_all('div', class_='_2gxd _2pis')
            for album in albums:
                if not album.span:
                    continue
                if album.span.string == 'Profile Pictures':
                    url = album.parent.parent.parent.parent['href']
            self.chrome.get(url)
            time.sleep(1)
            # go to specific pics
            soup = BeautifulSoup(self.chrome.page_source, 'lxml')
            pics = soup.find_all('img', class_='_pq3 img')

            num = 0  # number of pics you want to download for each person
            for pic in pics:
                url = pic.parent['href']
                self.chrome.get(url)
                time.sleep(1)
                # download pic
                soup = BeautifulSoup(self.chrome.page_source, 'lxml')
                if num == 10:
                    break
                try:
                    pic_url = soup.find_all('img', class_='spotlight')[0]['src']
                    self.chrome.get(pic_url)
                    # time.sleep(1)
                    filename = path + '/' + str(j) + '.png'
                    self.chrome.save_screenshot(filename)
                    img = Image.open(filename)
                    img.thumbnail((480, 348))
                    img.save(filename)
                    j += 1
                    num += 1
                except IndexError as e:
                    pass
            count += 1
        print('All pics downloaded!')
        return

    def save_websource(self, path, url=None):
        if not url:
            pass
        else:
            self.chrome.get(url)
        # write down html file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.chrome.page_source)
        print('Web Source saved!')
        return

    def scroll_down(self, times=10):
        print('Scrolling down...')
        for i in range(times + 1):
            self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        print('Scrolled to Bottom!')
        return

    def quit(self):
        self.chrome.quit()
        print('Bye:)')
        return


if __name__ == '__main__':
    t1 = time.time()
    bot = Bot(admin=True, usecookie=True)
    """do something"""
    bot.save_websource('currency.html', url='http://www.icbc.com.cn/icbc/%E9%87%91%E8%9E%8D%E4%BF%A1%E6%81%AF/%E5%A4%96%E6%B1%87%E7%89%8C%E4%BB%B7/%E4%BA%BA%E6%B0%91%E5%B8%81%E5%A4%96%E6%B1%87%E7%89%8C%E4%BB%B7/default.htm')

    """ end """
    duration = (time.time() - t1) / 60
    print('Application Stopped. Processing time: %f mins' % duration)
    # waiting for quit
    input('Press enter to terminate...')
    bot.quit()
