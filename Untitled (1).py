#!/usr/bin/env python
# coding: utf-8

# In[85]:


from bs4 import BeautifulSoup, Comment
import requests
from tqdm import tqdm_notebook as tqdm
from difflib import SequenceMatcher
from pymorphy2 import MorphAnalyzer


# In[88]:


morf = MorphAnalyzer()


# In[109]:


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

def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0

    for sym in s1:
        if sym in s2:
            c += 1

    return c / (a + b - c)

def difsc(s1,s2):
    return SequenceMatcher(None, s1, s2).ratio()

def to_imen(text):
    res = []
    for i in text:
        res.append(morf.parse(i.lower())[0].normal_form)
    return res
    


def sovpad(target_words, text):
    result = {}
    for i in target_words:
        result[i] = 0
    
    for word in tqdm(text):
        for target in target_words:
            result[target] += difsc(target ,word)
    return result
        


# In[110]:


spec_words = []
with open('../specalnosty.txt', 'r') as f:
    spec_words = f.read().split('\n')


# In[111]:



html = requests.get('https://moeobrazovanie.ru/reiting_professii_top_300').text
text = text_from_html(html)
text = to_imen(text)
values = sovpad(spec_words,text)


# In[ ]:





# In[112]:


sort_orders = sorted(values.items(), key=lambda x: x[1], reverse=True)

for i in sort_orders:
    print(i[0], i[1])




# In[ ]:




