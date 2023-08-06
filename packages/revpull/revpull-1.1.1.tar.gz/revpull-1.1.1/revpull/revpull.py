'''
revpull

Usage:
    revpull --dir=TARGET_DIR_PATH --auth=W3ID_AUTH
    revpull -h | --help
    revpull -v | --version

Options:
    --dir=TARGET_DIR_PATH           Set the path to the directory where the content will be saved
    --auth=W3ID_AUTH                Set the uername:password value for authentication
    -h, --help                      Show this help message.
    -v, --version                   Show the version.
'''

from schema import Schema, And, Or, Use, Optional, Regex, SchemaError
from revpull import downloader as down
from docopt import docopt
import logging as log
import datetime
import time
import json
import sys
import os

LOGIN_URL = "http://newdagwood.pok.ibm.com:8080/eReview_WebClient/Login.action"
NAV_URL = "http://newdagwood.pok.ibm.com:8080/eReview_WebClient/com/ibm/eReview/actions/Navigation.action"

COMPLETED_STATUS = None

log.basicConfig(
    stream=sys.stdout,
    level=log.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

def validate_args(args):
    global LOGIN_URL

    schema = Schema({
        '--dir': Or(None,
            Use(lambda d: (os.path.exists(d) and os.listdir(d)) or (os.path.exists(os.path.expanduser(d)) and os.listdir(os.path.expanduser(d)))),
            error = 'The target path does not exist or cannot be accessed'),
        '--auth': Or(None,
            Regex(r'^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}\:.+$'),
            error = 'The credentials for W3ID are in the wrong format'),
        '--help': Or(True, False),
        '--version': Or(True, False)
    })

    try:
        schema.validate(args)
        if not down.check_if_url_accessible(LOGIN_URL):
            log.error('The eReview system is unavailable')
            return False
    except SchemaError as e:
        log.error(e)
        return False

    return True

def download(dir, w3id_auth):
    global COMPLETED_STATUS
    global LOGIN_URL
    global NAV_URL

    COMPLETED_STATUS = False

    w3id_login = None
    w3id_password = None

    if not w3id_auth == None:
        try:
            w3id_login, w3id_password = w3id_auth.split(':', 1)
            w3id_login = w3id_login.lower()

            log.info("Authentication...")
            session_id = down.get_session_id(LOGIN_URL, (w3id_login, w3id_password))
            if not session_id == None:
                log.info("Scanning and building a content tree...")
                review_list = down.create_review_list(session_id, NAV_URL, auth=(w3id_login, w3id_password))

                log.info("Downloading...")
                dir = (os.path.abspath(dir) if not dir[0] == '~' else os.path.expanduser(dir))
                correct_path = down.create_fs_tree(session_id, dir, review_list)

                log.info("The downloaded content is now in the {}".format(correct_path))

                COMPLETED_STATUS = True
        except KeyboardInterrupt:
            log.info("Execution was interrupted by the user.")
        finally:
            return COMPLETED_STATUS


def main():
    args = docopt(__doc__, version='1.1.1')

    if validate_args(args):
        start_time = time.time()
        COMPLETED_STATUS = download(
            args['--dir'],
            args['--auth']
        )
        finish_time = time.time()

        log.info("EXECUTION TIME: {0}, COMPLETED SUCCESSFULLY: {1}".format(str(datetime.timedelta(seconds=finish_time-start_time)), COMPLETED_STATUS))
        if not COMPLETED_STATUS:
            log.info('''
                TIP: Analyze the logs, try to find and fix the problem, and then perform the action again.
                If you can\'t find or fix the problem, please contact support.
                Sometimes it\'s enough to wait to solve a problem.
            ''')
