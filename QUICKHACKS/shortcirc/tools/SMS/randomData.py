import json
import random
import string
import os

mails = (
    "mail.ru",
    "inbox.ru",
    "list.ru",
    "bk.ru",
    "ya.ru",
    "yandex.com",
    "yandex.ua",
    "yandex.ru",
    "gmail.com",
)

SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Get random service
def random_service(service_list):
    return random.choice(service_list)


# Create random name
def random_name():
    names_path = os.path.join(SCRIPT_ROOT, 'names.json')
    with open(names_path, "r") as names:
        names = json.load(names)
    return random.choice(names)


# Create random suffix for email
# %random_name%SUFFIX@%random_email%
def random_suffix(int_range=4):
    numbers = []
    for _ in range(int_range):
        numbers.append(str(random.randint(1, 9)))
    return "".join(numbers)


# Create random email by name, suffix, mail
# Example: Jefferson3715@gmail.com
def random_email():
    return random_name() + random_suffix() + "@" + random.choice(mails)


# Create random password
# %random_name%%random_suffix%
def random_password():
    return random_name() + random_suffix(int_range=10)


# Create random token
# %token%
def random_token():
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(random.randint(20, 50)))


# Get random user agent
def random_useragent():
    agents_path = os.path.join(SCRIPT_ROOT, 'user_agents.json')
    with open(agents_path, "r") as agents:
        user_agents = json.load(agents)["agents"]
    return random.choice(user_agents)
