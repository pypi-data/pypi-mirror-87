# coding: utf-8

"""Peform an HTTP GET on a URL and print the status code."""

import sys

import requests


def get_url_and_print_status_code():
    response = requests.get(sys.argv[1])
    print(response.status_code)


if __name__ == "__main__":
    get_url_and_print_status_code()
