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

praser = argparse.ArgumentParser()
praser.add_argument('-o')
args = praser.parse_args()
