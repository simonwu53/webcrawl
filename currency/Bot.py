import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from bs4 import BeautifulSoup
import numpy as np


class Bot:
    def __init__(self):
        print('Application Started.')
        # price list dict -> {bank name: [last 24 hrs currency]}
        self.pricelist = {'工商银行': [], '中国银行': [], '农业银行': [], '交通银行': [], '建设银行': [], '招商银行': [], '光大银行': [],
                          '浦发银行': [], '兴业银行': [], '中兴银行': []}
        self.phantomjs = webdriver.PhantomJS()
        self.min = 800  # best deal
        self.bank = 'Null'  # which bank
        self.trend = 'Increase'
        self.stable = True
        # input target price
        self.target = float(input('Your expected price is: \n'))
        print('PhantomJS Started.')

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
                time.sleep(120)
        except KeyboardInterrupt as e:
            print('Ctrl + C Issued...')

    def statistics(self):
        print('Current best deal is: %s: %f.' % (self.bank, self.min))
        icbc_list = self.pricelist['工商银行']
        if len(icbc_list) >= 12:
            first = icbc_list[-12]
            last = icbc_list[-1]
            if first - last < 0:
                self.trend = 'Increase'
            else:
                self.trend = 'Decrease'
            var = np.var(icbc_list)
            if var <= 0.01:
                self.stable = True
            else:
                self.stable = False
        else:
            print('Not Enough Data for Statistics.')
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
        return

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

    def quit(self):
        self.phantomjs.quit()
        print('Bye:)')
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
