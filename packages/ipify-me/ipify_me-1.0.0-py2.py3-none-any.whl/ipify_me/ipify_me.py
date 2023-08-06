import requests
import json


def get_ipify_ip():
    """
    Returns your public IP address from ipify.
    """
    response = requests.get('https://api.ipify.org?format=json')
    ip = json.loads(response.content)['ip']
    return ip


def print_ipify_ip():
    """
    Prints your public IP address in friendly format.
    """
    print("Your external IP is " + get_ipify_ip())
