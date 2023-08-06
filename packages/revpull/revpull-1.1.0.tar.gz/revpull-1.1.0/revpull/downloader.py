import multiprocessing
import logging as log
import urllib.parse
import threading
import requests
import datetime
import urllib3
import socket
import json
import time
import sys
import os
import re

LOGIN_URL = "http://newdagwood.pok.ibm.com:8080/eReview_WebClient/Login.action"
SESSION_ID = None

DOWNLOADS_TARGET = 0
DOWNLOADS_CURRENT = multiprocessing.Value('i', 0)

DOWNLOAD_THREADS = []
MAX_DOWNLOAD_THREADS = 8

COUNTER = 1
COUNT = 0
INDENT = 0

log.basicConfig(
    stream=sys.stdout,
    level=log.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)


def check_if_url_accessible(url):
    try:
        response = requests.get(url)
        return True
    except requests.ConnectionError as exception:
        return False


def get_session_id(url, w3_auth):
    w3_login, w3_pass = w3_auth
    response = requests.post(url,
        params = {
            "username": w3_login,
            "password": w3_pass,
            "submit": "Log+on+to+eReview"
        }
    )
    if "Login failed" in response.content.decode():
        log.warning("Login failed")
        return None
    else:
        for c in response.cookies:
            if c.name == "JSESSIONID":
                return c.value


def create_review_list(session_id, url, **kwargs):
    global LOGIN_URL
    global COUNT

    query = ""
    if "query" in kwargs:
        query = kwargs["query"]

    try:
        response = requests.post("{0}?query={1}".format(url, query),
            cookies = {
                "JSESSIONID": session_id
            }
        )
    except (
        socket.gaierror,
        urllib3.exceptions.NewConnectionError,
        urllib3.exceptions.MaxRetryError,
        requests.exceptions.ConnectionError
    ) as e:
        time.sleep(3)
        create_review_list(session_id, url, query=query, auth=kwargs["auth"])

    review_list = []
    json_content = {}
    try:
        json_content = json.loads(response.content)
    except json.decoder.JSONDecodeError:
        get_session_id(LOGIN_URL, kwargs["auth"])

    if query == "":
        COUNT = len(json_content)
        log.info("Reviews count: {}".format(COUNT))

    def proccess_item(item):
        global COUNTER
        global COUNT
        global INDENT

        if item["type"] == "reviews":
            log.info("{0}/{1} - {2}".format(COUNTER, COUNT, item["name"]))
            INDENT = len("{0}/{1} - ".format(COUNTER, COUNT))
            COUNTER += 1
        elif item["type"] == "drafts":
            log.info("{0}--- {1}".format(" " * INDENT, item["name"]))
        else:
            log.info("{0}--- {1}".format(" " * (INDENT + 4), item["name"]))

        review_json = {}
        review_json["name"] = item["name"]

        if item["type"] == "files":
            review_json["href"] = item["href"]
        else:
            if ("children" in item and len(item["children"]) > 0):
                review_json["children"] = []
                for child in item["children"]:
                    review_json["children"].append(create_review_list(session_id, url, query=child["$ref"], auth=kwargs["auth"]))

        return review_json

    if isinstance(json_content, list):
        for review in json_content:
            review_list.append(proccess_item(review))
    elif (isinstance(json_content, dict) and len(json_content) > 0):
        review_list.append(proccess_item(json_content))

    if (isinstance(review_list, list) and
        len(review_list) == 1 and
        isinstance(review_list[0], dict)
    ):
        review_list = review_list[0]

    return review_list


def create_download_thread(download_map):
    global SESSION_ID

    url = download_map["href"]
    path = download_map["path"]

    try:
        r = requests.get(url,
            cookies = {
                "JSESSIONID": SESSION_ID
            },
            stream=True,
            allow_redirects=True
        )
    except (
        socket.gaierror,
        urllib3.exceptions.NewConnectionError,
        urllib3.exceptions.MaxRetryError,
        requests.exceptions.ConnectionError
    ) as e:
        create_download_thread(download_map)

    with open(
        os.path.join(
            path, urllib.parse.unquote(url.rsplit("/", 1)[1].rsplit("?", 1)[0])
        ), 'wb') as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)
    update_counter()


def update_counter():
    global DOWNLOADS_CURRENT
    global DOWNLOADS_TARGET

    with DOWNLOADS_CURRENT.get_lock():
        DOWNLOADS_CURRENT.value += 1
    log.info("{0}/{1} downloaded".format(DOWNLOADS_CURRENT.value, DOWNLOADS_TARGET))


def download_file(session_id, url, path):
    global DOWNLOAD_THREADS

    download_thread = threading.Thread(target=create_download_thread, args=(session_id, url, path))
    DOWNLOAD_THREADS.append(download_thread)
    download_thread.start()


def create_fs_tree(session_id, root_path, review_list):
    global SESSION_ID
    global DOWNLOAD_THREADS
    global MAX_DOWNLOAD_THREADS
    global TARGET_COUNT
    global DOWNLOADS_TARGET


    try:
        full_path = os.path.join(root_path, "reviews")
        os.mkdir(full_path)
        root_path = full_path
    except FileNotFoundError:
        os.mkdir(root_path)
    except FileExistsError:
        root_path = os.path.join(root_path, "{0}_{1}".format("review", datetime.datetime.now(datetime.timezone.utc)
            .replace(microsecond=0)
            .astimezone()
            .strftime("%d-%m-%yT%H_%M_%S")
        ))
        os.mkdir(root_path)

    download_map = []
    download_counter = 0
    def deep_dive(root_path, review_list):
        global CURRENT_NUMBER
        global TARGET_COUNT

        for review in review_list:
            if ("children" in review and len(review["children"]) > 0):
                if "/" in review["name"]:
                    review["name"] = review["name"].replace("/", "-")
                review["path"] = os.path.join(root_path, review["name"])
                try:
                    os.mkdir(review["path"])
                except FileExistsError:
                    while True:
                        try:
                            if re.search("^.*_[0-9]+$", review["path"]) == None:
                                review["path"] = "{}_1".format(review["path"])
                            else:
                                review["path"] = "{0}_{1}".format(review["path"].rsplit("_", 1)[0], str(int(review["path"].rsplit("_", 1)[1]) + 1))
                            os.mkdir(review["path"])
                            break
                        except FileExistsError:
                            continue

                deep_dive(review["path"], review["children"])
            elif ("href" in review and not review["href"] == ""):
                download_map.append({
                    "href": review["href"],
                    "path": root_path
                })

    deep_dive(root_path, review_list)

    SESSION_ID = session_id
    DOWNLOADS_TARGET = len(download_map)
    NUM_WORKERS = multiprocessing.cpu_count()*2
    with multiprocessing.Pool(processes=NUM_WORKERS) as pool:
        results = pool.map(create_download_thread, download_map)

    return root_path
