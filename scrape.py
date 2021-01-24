import argparse
import getpass
import json
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

