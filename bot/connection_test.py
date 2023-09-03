import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from test_util import keyboard_constructor
from callbacks import callback_constructor

url = 'http://195.2.93.26/api/tasks/1/'

# session = requests.Session()
# retry = Retry(connect=3, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# session.mount("http://", adapter)
# session.mount("https://", adapter)

# response = session.get(url).json()
# some = response.get("image")
# answer = response.get("answer")


x = callback_constructor(3)
print(x)
