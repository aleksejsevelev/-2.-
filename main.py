import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(apikey, long_url):
    url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': apikey,
        'url': long_url,
        'v': '5.199'
    }
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(apikey, key):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': apikey,
        'key': key,
        'v': '5.199'
    }
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()['response']['stats'][0]['views']


def is_short_link(parsed_url, apikey):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': apikey,
        'key': parsed_url.path[1:],
        'v': '5.199'
    }
    if parsed_url.netloc == 'vk.cc':
        response = requests.get(url, params)
        response.raise_for_status()
        return 'error' not in response.json()


def main():
    load_dotenv('secret_data.env')
    user_url = input('Введите вашу ссылку: ')
    vk_key = os.environ['VK_KEY']
    parsed_url = urlparse(user_url)
    if is_short_link(parsed_url, vk_key):
        key = parsed_url.path[1:]
        link_stats = count_clicks(vk_key, key)
        print(f'Количество кликов по ссылке: {link_stats}')
    else:
        short_link = shorten_link(vk_key, user_url)
        print(f'Сокращенная ссылка: {short_link}')


if __name__ == '__main__':
    main()
