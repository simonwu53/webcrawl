import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from bs4 import BeautifulSoup
import numpy as np
import urllib.request


class Bot:
    def __init__(self):
        print('Application Started.')
        # price list dict -> {bank name: [last 24 hrs currency]}
        self.pricelist = {'工商银行': [], '中国银行': [], '农业银行': [], '交通银行': [], '建设银行': [], '招商银行': [], '光大银行': [],
                          '浦发银行': [], '兴业银行': [], '中兴银行': []}
        # self.phantomjs = webdriver.PhantomJS()
        self.phantomjs = None  # web driver, start later
        self.min = 800  # best deal
        self.bank = 'Null'  # which bank
        self.trend = 'Increase'
        self.se_var = 0
        self.stable = True
        # target price
        self.target = float(770)

    def check_currency(self):
        self.phantomjs.get("http://finance.sina.com.cn/forex/paijia.html#0")
        try:
            print('Starting subscribing CNY/EUR exchange rate...')
            while True:
                # open webpage
                self.phantomjs.refresh()
                print('Web Page Refreshed.')
                time.sleep(5)
                # brew soup
                soup = BeautifulSoup(self.phantomjs.page_source, 'lxml')
                rmb2euro = soup.find_all('table', class_='js-table')[1]
                # extract price list
                try:
                    eurosell = rmb2euro.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.children
                except AttributeError as e:
                    print('Can Not Find Items...Refreshing...')
                    continue
                eurosell_list = [price for price in eurosell]

                # collect data
                for index, item in enumerate(self.pricelist):
                    ratelist = self.pricelist[item]
                    price = float(eurosell_list[index].string)
                    if price < self.min:
                        self.min = price
                        self.bank = item
                    ratelist.append(price)
                print('Price List Updated.')
                # display data
                self.statistics()
                # finishing loop
                time.sleep(900)
        except KeyboardInterrupt as e:
            print('Ctrl + C Issued...')

    def statistics(self):
        print('----------------------------------------------------')
        print(time.asctime(time.localtime(time.time())))
        print('Current best deal is: %s: %f.' % (self.bank, self.min))
        bank_list = self.pricelist[self.bank]
        if len(bank_list) >= 12:
            first = bank_list[-12]
            last = bank_list[-1]
            if first - last < 0:
                self.trend = 'Increase'
            else:
                self.trend = 'Decrease'
            self.se_var = np.var(bank_list)
            if self.se_var <= 0.01:
                self.stable = True
            else:
                self.stable = False
        else:
            print('Not Enough Data for Statistics.')
            print('----------------------------------------------------')
            return
        if self.trend == 'Increase':
            print('Rate Trend: %s.' % self.trend)
            if self.stable:
                print('Now at high point, suggest waiting for more time.')
            else:
                print('Still increasing...')
        else:
            price = min(first, last)
            print('Rate Trend: %s.' % self.trend)
            if self.stable:
                if self.target > price:
                    print('Now at low point, suggest buying!')
                else:
                    print('Now at low point, but still higher than expected.')
            else:
                print('Still decreasing, suggest waiting for more time.')
        print('----------------------------------------------------')
        return

    def get_pricelist(self):
        self.phantomjs.get("http://finance.sina.com.cn/forex/paijia.html#0")
        print('Getting Price List...')
        time.sleep(1)
        # brew soup
        soup = BeautifulSoup(self.phantomjs.page_source, 'lxml')
        try:
            rmb2euro = soup.find_all('table', class_='js-table')[1]
        except IndexError as e:
            self.phantomjs.get('https://www.google.ee')
            print('Getting List Failed...')
            return None
        # extract price list
        try:
            eurosell = rmb2euro.tbody.tr.next_sibling.next_sibling.next_sibling.next_sibling.children
        except AttributeError as e:
            self.phantomjs.get('https://www.google.ee')
            print('Getting List Failed...')
            return None
        print('List Got.')
        eurosell_list = [price for price in eurosell]
        # collect data
        for index, item in enumerate(self.pricelist):
            ratelist = self.pricelist[item]
            price = float(eurosell_list[index].string)
            if price < self.min:
                self.min = price
                self.bank = item
            ratelist.append(price)
        self.phantomjs.get('https://www.google.ee')
        return self.pricelist

    def get_statistics(self):
        bank_list = self.pricelist[self.bank]
        if len(bank_list) >= 12:
            first = bank_list[-12]
            last = bank_list[-1]
            if first - last < 0:
                self.trend = 'Increase'
            else:
                self.trend = 'Decrease'
            self.se_var = np.var(bank_list)
        else:
            self.trend = 'None'
            self.se_var = 'None'
        print('Getting Statistics...')
        return self.bank, str(self.min), self.trend, str(self.se_var)

    @staticmethod
    def save_websource(path, url):
        chrome = webdriver.Chrome()
        chrome.get(url)
        # write down html file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(chrome.page_source)
        print('Web Source saved!')
        time.sleep(1)
        chrome.quit()
        return

    def set_target(self, target):
        self.target = float(target)
        return

    def start(self):
        self.phantomjs = webdriver.PhantomJS()
        print('Browser Opened.')
        return

    def quit(self):
        self.phantomjs.quit()
        print('Browser Closed.')
        return


if __name__ == '__main__':
    t1 = time.time()
    bot = Bot()
    """do something"""
    bot.check_currency()
    # bot.save_websource('html/currency.html', 'http://finance.sina.com.cn/forex/paijia.html#0')

    """ end """
    duration = (time.time() - t1) / 60
    print('Application Stopped. Processing time: %f mins' % duration)
    # waiting for quit
    input('Press enter to terminate...')
    bot.quit()
