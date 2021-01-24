#!/usr/bin/env python

"""scrape
This script allows the user to scarpe all video links and save it to a file
"""

import argparse
import getpass
import os
import re
import time
import urllib.request
import requests
import urllib3

from bs4 import BeautifulSoup as bs
from iterfzf import iterfzf
from requests_ntlm import HttpNtlmAuth
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

__author__ = 'Ibrahim Abou Elenein'
__copyright__ = 'Copyright (C) 2021 Ibrahim Abou Elenein'
__license__ = 'MIT'
__version__ = '2021.1.0'

# args options
praser = argparse.ArgumentParser()
praser.add_argument('-o')
args = praser.parse_args()

# ssl Warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# selenium options
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(desired_capabilities=caps, options=options)


def get_credinalities():
    ''' login to cms website'''
    if not os.path.isfile(".env"):
        user_name = input("Enter your username : ")
        pass_word = getpass.getpass(prompt="Enter Your Password : ")
        file_env = open(".credenalites", "w")
        file_env.write(username+"\n"+password)
        file_env.close()
    else:
        file_env = open("env", "r")
        lines = file_env.readlines()
        user_name = lines[0].strip()
        pass_word = lines[1].strip()
        file_env.close()
    return user_name, pass_word

username, password = get_credinalities()

session = requests.Session()
homePage = session.get("https://cms.guc.edu.eg/",
                       verify=False, auth=HttpNtlmAuth(username, password))
homePage_soup = bs(homePage.text, 'html.parser')

def get_avaliable_courses():
    ''' fetch courses links'''
    print("[-] Fetching Courses(-)")
    course_links = []
    link_tags = homePage_soup('a')
    for link_tag in link_tags:
        ans = link_tag.get('href', None)
        if ans is None:
            continue
        match = re.match(r'\/apps\/student\/CourseViewStn\?id(.*)', ans)
        if match:
            course_links.append(ans)
    return course_links

def get_course_names():
    ''' get courses names'''
    courses_table = list(homePage_soup.find('table', {
        'id': 'ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses'}))
    courses_name = []
    for i in range(2, len(courses_table) - 1):
        courses_name.append(re.sub(
            r'\n*[\(][\|]([^\|]*)[\|][\)]([^\(]*)[\(].*\n*', '[\\1]\\2', courses_table[i].text))
    return courses_name

