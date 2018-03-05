# coding:utf8

from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}


def get_html_zhidao(url):
    # Get HTML from baidu zhidao
    soup_zhidao = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    return html_filter(soup_zhidao)


def get_html_baike(url):
    # Get HTML from baidu baike
    soup_baike = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    return html_filter(soup_baike)


def get_html_bingkg(url):
    # Get HTML from bing knowledge graph
    soup_bingwd = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    return html_filter(soup_bingwd)


def get_html_baidu(url):
    # Get HTML from baidu search
    soup_baidu = BeautifulSoup(requests.get(url=url, headers=headers).content.decode('utf-8'), "lxml")
    return html_filter(soup_baidu)


def get_html_bing(url):
    # Get HTML from bing search
    soup_bing = BeautifulSoup(requests.get(url=url, headers=headers).content.decode('utf-8'), "lxml")
    return html_filter(soup_bing)


def html_filter(soup):
    # Remove irrelevant tags to increase speed
    [s.extract() for s in soup(['script', 'style', 'img', 'sup', 'b'])]
    return soup

