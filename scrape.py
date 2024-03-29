#!/usr/bin/env python

"""This script allows the user to scarpe all video links and save it to a file"""

import argparse
import json
import os
import re
import sys
import time
from signal import SIGINT, signal

import requests
import pyshorteners
import urllib3
from alive_progress import alive_bar
from bs4 import BeautifulSoup as bs
from PyInquirer import prompt
from requests_ntlm import HttpNtlmAuth
from rich import print
from rich.console import Console
from rich.panel import Panel
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

__author__ = "Ibrahim Abou Elenein"
__copyright__ = "Copyright (C) 2021 Ibrahim Abou Elenein"
__license__ = "MIT"
__version__ = "2021.1.0"


def authenticate_user(username, password):
    """validate user credentials"""
    session = requests.Session()
    r = session.get(
        "https://cms.guc.edu.eg/", verify=False, auth=HttpNtlmAuth(username, password)
    )
    if r.status_code == 200:
        console.log()
        console.rule("[+] You are authorized", style="bold green")
    else:
        console.log()
        console.rule(
            "[!] You are not authorized. review your login credentials",
            style="bold red",
        )
        if os.path.isfile(".env"):
            os.remove(".env")
        sys.exit(1)


def get_cardinalities():
    """login to cms website"""
    if not os.path.isfile(".env"):
        console.rule("[**] Credentials")
        cred = prompt(questions)
        user_name = list(cred.values())[0]
        pass_word = list(cred.values())[1]
        authenticate_user(user_name, pass_word)
        file_env = open(".env", "w")
        file_env.write(user_name + "\n" + str(pass_word))
    else:
        file_env = open(".env", "r")
        lines = file_env.readlines()
        user_name = lines[0].strip()
        pass_word = lines[1].strip()
        authenticate_user(user_name, pass_word)
    file_env.close()
    return user_name, pass_word


def welcome():
    """Welcome the user"""
    first_name = username.split(".")[0]
    last_name = username.split(".")[1].split("@")[0]
    console.log()
    console.print(
        Panel.fit(
            f"""        [bold cyan] Welcome [/bold cyan] [bold yellow] {first_name.upper()} {last_name.upper()} [/bold yellow]       

         [bold magenta]Run $ python scrape.py -h for help[/bold magenta]           
        """,
            title="Welcome!",
        ),
        justify="center",
    )


def get_avaliable_courses():
    """fetch courses links"""
    course_links = []
    link_tags = homePage_soup("a")
    console.rule("[::] Fetching courses")
    console.log()
    with console.status("[bold green] Fetching courses"):
        for link_tag in link_tags:
            ans = link_tag.get("href", None)
            if ans is None:
                continue
            match = re.match(r"\/apps\/student\/CourseViewStn\?id(.*)", ans)
            if match:
                course_links.append(ans)
                if args.verbose > 0:
                    console.log(f"course_link : {course_links[-1]}")
            time.sleep(0.05)
    return course_links


def get_course_names():
    """get courses names"""
    courses_table = list(
        homePage_soup.find(
            "table",
            {"id": "ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses"},
        )
    )
    courses_name = []
    with console.status("[bold green] getting courses names"):
        for i in range(2, len(courses_table) - 1):
            courses_name.append(
                re.sub(
                    r"\n*[\(][\|]([^\|]*)[\|][\)]([^\(]*)[\(].*\n*",
                    "[\\1]\\2",
                    courses_table[i].text,
                )
            )
            if args.verbose > 0:
                console.log(courses_name[-1])
    return courses_name


def choose_course():
    """prompt the user to choose the string"""
    if not os.path.isfile(".courses.json"):
        courses_links = get_avaliable_courses()
        courses_names = get_course_names()
        courses = dict(zip(courses_names, courses_links))
        with open(".courses.json", "w") as outfile:
            json.dump(courses, outfile)
    with open(".courses.json") as json_file:
        links = json.load(json_file)
    courses = [i for i in links]
    questions = [
        {
            "type": "list",
            "name": "size",
            "message": "What Course do you want?",
            "choices": courses,
        }
    ]
    console.rule("[..] Choosing Course")
    console.log()
    course = prompt(questions)
    course = list(course.values())[0]
    return links.get(course)


def process_browser_log_entry(entry):
    """gets log of process"""
    response = json.loads(entry["message"])["message"]
    if args.verbose > 7:
        print(response)
    return response


def get_link_master(driver):
    """scape m3u8 link for one video"""
    while True:
        browser_log = driver.get_log("performance")
        events = [process_browser_log_entry(entry) for entry in browser_log]
        events = [event for event in events if "Network.response" in event["method"]]
        for event in events:
            if args.verbose > 3 and args.verbose < 7:
                console.log(event)
            if (
                "params" in event.keys()
                and "response" in event["params"].keys()
                and "url" in event["params"]["response"].keys()
                and re.search("master", event["params"]["response"]["url"])
            ):
                links.append(s.tinyurl.short(event["params"]["response"]["url"]))
                if args.verbose > 0:
                    console.log(f" {event['params']['response']['url']} ")
                return


def get_video_ids(driver):
    """get id for videos and pass it to get the link master"""
    with console.status("[bold green] Getting videos names and ids"):
        for _ in range(30):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ids = []
        course_soup = bs(driver.page_source.encode("utf-8"), "html.parser")
        inputs = course_soup("input")

        for ink in inputs:
            if ink.get("value") == "Watch Video" and ink["id"] != "":
                ids.append(ink["id"])
                if args.verbose > 1:
                    time.sleep(0.05)
                    console.log(ids[-1])
                name = (
                    ink.find_parent("div")
                    .find_parent("div")
                    .find_parent("div")("strong")
                )
                name_new = re.sub(r"[0-9]* - (.*)", "\\1", str(name))
                names.append(
                    name_new.replace("[<strong>", "")
                    .replace("</strong>]", "")
                    .replace("&amp;", "")
                    .strip()
                )
                if args.verbose > 1:
                    time.sleep(0.05)
                    console.log(names[-1])

    console.rule("Scraping")
    with alive_bar(
        len(ids), title="Scraping Links", bar="blocks", spinner="dots"
    ) as bar:
        for item in ids:
            driver.quit()
            driver = webdriver.Chrome(desired_capabilities=caps, options=options)
            driver.get(f"https://{username}:{password}@cms.guc.edu.eg{course_link}")
            button = driver.find_element_by_id(item)
            driver.execute_script("arguments[0].click();", button)
            try:
                get_link_master(driver)
            except:
                print("")
            bar()


def bye():
    console.print(
        Panel.fit(
            """    [bold red]Thank YOU [/bold red][bold]for using  cms scraper 

    If you enjoy it, feel free to leave a [/bold][bold red]Star[/bold red]

    [italic bold yellow]https://github.com/aboueleyes/cms-scrapper[/italic bold yellow]

    [italic cyan]Feedback and contribution is welcome as well :smiley:![/italic cyan]
        """,
            title="Bye!",
        ),
        justify="center",
    )


def handler(signal_received, frame):
    # Handle any cleanup here
    print("\n[bold]SIGINT or CTRL-C detected. [red]Exiting gracefully[/red][/bold]")
    bye()
    sys.exit(0)


if __name__ == "__main__":
    signal(SIGINT, handler)

    s = pyshorteners.Shortener()
    # args options
    parser = argparse.ArgumentParser(
        prog="cms-scrapper",
        description="""
                    scrape m3u8 for cms website
                """,
    )
    parser.add_argument("-o", "--output", help="name of output file", required=True)

    parser.add_argument(
        "--verbose", "-v", help="be more talkative", action="count", default=0
    )
    parser.add_argument(
        "-r",
        "--replace",
        help="replace existing file",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    if os.path.isfile(args.output):
        if args.replace:
            os.remove(args.output)
        else:
            print(
                "[bold][red]file exists if you want to overwrite it please use -r :smiley:![/bold][/red]"
            )
            sys.exit(0)

    # ssl Warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    console = Console()

    # selenium options
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--window-size=1920,1080")

    questions = [
        {
            "type": "input",
            "name": "username",
            "message": "Enter your GUC username:",
        },
        {"type": "password", "message": "Enter your GUC password:", "name": "password"},
    ]

    username, password = get_cardinalities()

    welcome()

    session = requests.Session()
    homePage = session.get(
        "https://cms.guc.edu.eg/", verify=False, auth=HttpNtlmAuth(username, password)
    )
    homePage_soup = bs(homePage.text, "html.parser")

    course_link = choose_course()

    driver = webdriver.Chrome(desired_capabilities=caps, options=options)

    if args.verbose > 0:
        console = Console()
        console.log("[-] Initializing The Browser", style="bold yellow")

    driver.get(f"https://{username}:{password}@cms.guc.edu.eg{course_link}")

    names, links = [], []

    get_video_ids(driver)

    driver.quit()

    my_dict = dict(zip(links, names))

    with open(args.output, "w") as fp:
        json.dump(my_dict, fp)

    bye()
