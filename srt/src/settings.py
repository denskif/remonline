# ~*~ coding: utf-8 ~*~

import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
SCREEN_PATH = os.path.join(ROOT_PATH, 'screen')

LOCAL_HOST = "http://example.com:8000"
DEV_HOST = "https://dev.remonline.ru"
STABLE_HOST = "https://stable.remonline.ru"

HOST = DEV_HOST

TIME = 10 # Seconds.

LOGIN = "remtest"
PASSWORD = "test"
