#!/usr/bin/env python2.7

from selenium import webdriver
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('http://www.milb.com/milb/stats/stats.jsp?gid=2017_08_01_jaxaax_blxaax_1&t=g_box&sid=milb')
html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
soup = BeautifulSoup(html, 'lxml')
innings = soup.find_all("td", class_="inning inning-2")
print(html)
