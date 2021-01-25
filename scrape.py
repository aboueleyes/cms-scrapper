#!/usr/bin/env python

"""scrape
This script allows the user to scarpe all video links and save it to a file
"""

import argparse
import getpass
import json
import os
import re
import time
import urllib.request

import requests
import urllib3
from alive_progress import alive_bar
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


def get_credinalities():
    ''' login to cms website'''
    if not os.path.isfile(".env"):
        user_name = input("Enter your username : ")
        pass_word = getpass.getpass(prompt="Enter Your Password : ")
        file_env = open(".env", "w")
        file_env.write(user_name+"\n"+pass_word)
        file_env.close()
    else:
        file_env = open(".env", "r")
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
    print("[-] Fetching Courses[-]")
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


def choose_course():
    ''' promt the user to choose the string '''
    if not os.path.isfile(".courses.json"):
        courses_links = get_avaliable_courses()
        courses_names = get_course_names()
        courses = dict(zip(courses_names, courses_links))
        with open(".courses.json", "w") as outfile:
            json.dump(courses, outfile)
    with open('.courses.json') as json_file:
        links = json.load(json_file)
    courses = []
    for i in links:
        courses.append(i)
    course = iterfzf(courses)
    course_url = links.get(course)
    return course_url


course_link = choose_course()

driver = webdriver.Chrome(desired_capabilities=caps, options=options)
driver.get(
    f'https://{username}:{password}@cms.guc.edu.eg{course_link}')


def process_browser_log_entry(entry):
    ''' gets log of process'''
    response = json.loads(entry['message'])['message']
    return response


names, links = [], []


def get_link_master():
    ''' scape m3u8 link for one video '''
    while True:
        browser_log = driver.get_log('performance')
        events = [process_browser_log_entry(entry) for entry in browser_log]
        events = [
            event for event in events if 'Network.response' in event['method']]

        for event in events:
            if 'params' in event.keys():
                if 'response' in event['params'].keys():
                    if 'url' in event['params']['response'].keys():
                        if re.search("master", event['params']['response']['url']):
                            links.append(event['params']['response']['url'])
                            return


def get_video_ids():
    ''' get id for videos and pass it to get the link master '''
    for _ in range(1000):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
    ids = []
    # print all of the page source that was loaded
    course_soup = bs(driver.page_source.encode("utf-8"), 'html.parser')
    inputs = course_soup('input')
    for ink in inputs:
        if ink.get('value') == 'Watch Video':
            if ink['id'] != "":
                ids.append(ink['id'])
                name = ink.find_parent('div').find_parent(
                    'div').find_parent('div')('strong')
                name_new = re.sub(r'[0-9]* - (.*)', "\\1", str(name))
                names.append(name_new.replace(
                    "[<strong>", "").replace("</strong>]", "").replace("&amp;", "").strip())
    with alive_bar(len(ids), title='scrapping links', bar='filling') as bar:
        for item in ids:
            driver.get(
                f'https://{username}:{password}@cms.guc.edu.eg{course_link}')
            time.sleep(0.6)
            button = driver.find_element_by_id(item)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(0.3)
            try:
                get_link_master()
            except:
                print("")
            bar()
            time.sleep(0.3)


if __name__ == "__main__":
    get_video_ids()
    driver.quit()
    my_dict = dict(zip(links, names))
    with open(args.o, 'w') as fp:
        json.dump(my_dict, fp)
