"""
from aggregation_api2 import aggregation_api2
from raw_feedback import raw_feedback as rf
import json
from analyzed_feedback import analyzed_feedback as af
from raw_feedback import raw_feedback as rf
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SentimentOptions, SyntaxOptions, SyntaxOptionsTokens
from nltk.corpus import wordnet as wn
from keywordx import keywordx
import copy

def watson_raw():
    with open('sample_feedback.txt', 'r') as file:
        data = file.read().replace('\n', '')
    nlu = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey='5kLneMxCf9SLzD3grPVYfgiYx9Xtx3Arm52SMnrTASQB',
        url='https://gateway.watsonplatform.net/natural-language-understanding/api'
    )
    response = nlu.analyze(
        return_analyzed_text=True,
        text=data,
        features=Features(keywords=KeywordsOptions(sentiment=True, limit=5))).get_result()
    print(response)

with open('sample_feedback.txt', 'r') as file:
    data = file.read().replace('\n', '')
yelp = rf(data)
random = rf("I really hated the ribeye steak. The steak fucking sucked. Never eat the steak.")
raw_feedback_array = [yelp, random]
test = aggregation_api2()

analyzed_feedback_array = []
for raw_feedback in raw_feedback_array:
    analyzed_feedback_array.append(test.get_keywords(raw_feedback))

keyword_array = test.get_keyword_array(analyzed_feedback_array)
print(keyword_array)
print(test.sort_scores(test.score(keyword_array)))"""

import json
from aggregation_api3 import watson_helper

with open('../data.json', 'r') as mock:
    data = {review['review_id']: review['text']
            for review in json.load(mock)[0]['reviews'][:5]}


watson = watson_helper(data)
for id in watson.input_dict:
    watson.analyze_review_text(id)

print(watson.raw_watson_dict)
print(watson.keyword_dict)

watson.all_keywords()
watson.meta_score()
watson.keyword_relevance()
print(watson.final_rv)
