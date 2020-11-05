import os
import yaml
import requests
from locust.exception import StopUser


def get_config_file_path():
    current_path = os.path.dirname(__file__)
    return current_path + '/../' + 'global_config.yml'


def get_parameters_file_path(file_name):
    current_path = os.path.dirname(__file__)
    return current_path + '/../input/' + file_name


def dso_login(env='dev'):
    with open(get_config_file_path(), 'r') as f:
        properties = yaml.load(f.read(), yaml.SafeLoader)
    env_property = properties[env]
    url = env_property['login_url']
    header = {
        "Authorization": env_property['login_authorization'],
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "grant_type": env_property['login_grant_type'],
        "scope": env_property['login_scope']
    }
    response = requests.post(url, data=body, headers=header)
    if response.status_code == 200:
        return response
    else:
        print(response.status_code.__str__() + " : " + response.text)
        raise StopUser()


def dso_authorization_header(env='dev'):
    access_token = dso_login(env).json().get("access_token")
    return {
        "Authorization": "Bearer" + " " + access_token
    }
