from bs4 import BeautifulSoup, Comment
import requests
from tqdm import tqdm_notebook as tqdm
from difflib import SequenceMatcher
from pymorphy2 import MorphAnalyzer


morf = MorphAnalyzer()

spec_words = []
with open('./specalnosty.txt', 'r') as f:
    spec_words = f.read().split('\n')


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    list_l = filter(None, [t.strip().split(' ') for t in visible_texts])
    res = []
    for i in list_l:
        res += i
    return list(filter(None, res))


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def difsc(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()


def format_padej(text):
    res = []
    for i in text:
        res.append(morf.parse(i.lower())[0].normal_form)
    return res


def sovpad(target_words, text):
    result = {}
    for i in target_words:
        result[i] = 0

    for word in text:
        for target in target_words:
            result[target] += difsc(target, word)
    return result


def get_html(url):
    return requests.get(url).text


def parce(url):
    html = get_html(url)
    text = text_from_html(html)
    text = format_padej(text)
    values = sovpad(spec_words, text)
    sort_orders = sorted(values.items(), key=lambda x: x[1], reverse=True)
    return str(sort_orders[:3])

