from bs4 import BeautifulSoup
import requests


def get_data(url):
    data = {}
    page = requests.get('https://www.google.com/')
    soup = BeautifulSoup(page.content, features='html.parser')
    title = soup.find('title')
    text = title.text.replace('&nbsp;', '')
    data['title'] = text
    print(data)
    return data


get_data('hello')
