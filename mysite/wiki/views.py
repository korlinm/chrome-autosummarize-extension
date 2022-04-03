from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

import wikipedia

import bs4 as bs
import urllib.request
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import nltk
nltk.download(['wordnet', 'stopwords', 'punkt'])

model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
tokenizer = AutoTokenizer.from_pretrained("t5-base")


def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")


# https://pypi.org/project/wikipedia/#description
def get_wiki_summary(request):
    topic = request.GET.get('topic', None)
    try:
        result = wikipedia.summary(topic, sentences=2)
    except:
        result = "Error: Need more concise wiki search term"

    data = {
        'summary': result,
        'raw': 'Successful',
    }

    return JsonResponse(data)


def get_page_summary(request):
    topic = request.GET.get('topic', None)

    scraped_data = urllib.request.urlopen(topic)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text

    topics = get_topics(article_text)

    inputs = tokenizer("summarize: " + article_text,
                       return_tensors="pt", max_length=512, truncation=True)

    outputs = model.generate(
        inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True
    )
    # decode the result from transformer and remove remaining html tags that are generated?
    result = tokenizer.decode(outputs[0])
    result = re.sub(r"<[^>]*>", "", result)

    data = {
        'summary': result,
        "topics": topics,
        'raw': 'Successful',
    }

    return JsonResponse(data)


def get_topics(article_text):
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    en_stopwords = stopwords.words('english')

    custom_stopwords = ['class', 'adam', 'mcquistan', 'adammcquistan']
    article_stopwords = set(en_stopwords + custom_stopwords)

    lmr = WordNetLemmatizer()

    article_doc = []
    for t in word_tokenize(article_text):
        if t.isalpha():
            t = lmr.lemmatize(t.lower())
            if t not in article_stopwords:
                article_doc.append(t)

    from gensim.corpora.dictionary import Dictionary
    doc_dict = Dictionary([article_doc])
    article_bow = doc_dict.doc2bow(article_doc)

    most_frequent = sorted(article_bow, key=lambda x: x[1], reverse=True)

    term_ids, counts = zip(*most_frequent)

    top_terms = [doc_dict[id] for id in term_ids[:5]]
    return ", ".join(top_terms)
