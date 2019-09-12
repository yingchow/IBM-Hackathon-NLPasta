import json
from analyzed_feedback import analyzed_feedback as af
from raw_feedback import raw_feedback as rf
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SentimentOptions, SyntaxOptions, SyntaxOptionsTokens
from nltk.corpus import wordnet as wn
from keywordx import keywordx
import copy



class aggregation_api2:
    """
    Initializes an aggregation object with watson api keys
    NLU: Natural Language Understanding keys
    """
    def __init__(self):
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2018-11-16',
            iam_apikey='5kLneMxCf9SLzD3grPVYfgiYx9Xtx3Arm52SMnrTASQB',
            url='https://gateway.watsonplatform.net/natural-language-understanding/api'
        )

    """
    Uses watson API to analyze the review text of a single raw_feedback object.
    Returns an analyzed_feedback object
    """
    def get_keywords(self, raw_feedback):
        response = self.nlu.analyze(
            return_analyzed_text=True,
            text=raw_feedback.review_text,
            features=Features(keywords=KeywordsOptions(sentiment=True, limit=5))).get_result()
        keywords_array = []
        for keyword in response['keywords']:
            keywords_array.append(keywordx(keyword['text'], keyword['sentiment']['score'], keyword['relevance']))
        return af(raw_feedback.review_text, keywords_array)

    """
    NOT USED!!!!!!
    Given an analyzed_feedback object, returns an updated anaylzed_feedback object such that keywords
    are given pos and lemma values based on first encounter in text 
    """
    def get_syntax(self, analyzed_feedback):
        response = self.nlu.analyze(
            return_analyzed_text=True,
            text=analyzed_feedback.review_text,
            part_of_speech=True,
            features=Features(
                syntax=SyntaxOptions(tokens=SyntaxOptionsTokens(lemma=True, part_of_speech=True, )))).get_result()

        keywords_to_find = set()
        for keyword in analyzed_feedback.keywords:
            keywords_to_find.add(keyword.text)
        for word in response['syntax']['tokens']:
            if word['text'] in keywords_to_find:
                keywords_to_find.remove(word['text'])
                keyword = analyzed_feedback.get_keyword_with_text(word['text'])
                keyword.pos = word['part_of_speech']
                keyword.lemma = word['lemma']

    """
    Returns an array of all keywords from an analyzed_feedback array
    """
    def get_keyword_array(self, feedback_array):
        big_keyword_array = []
        for feedback in feedback_array:
            for keyword in feedback.keywords:
                big_keyword_array.append(keyword)
        return big_keyword_array

    """
    Returns a dictionary of scored keywords. For a given keyword, sums all 
    relevance*sentiment scores
    """
    def score(self, keyword_array):
        scores = {}
        for keyword in keyword_array:
            if keyword not in scores:
                scores[keyword] = 0
            scores[keyword] = scores[keyword] + keyword.sentiment * keyword.relevance
        return scores

    """
    Sorts the dictionary of scores. Returns an array of tuples where index 0 is keyword,
    index 1 is score. Ascending order based on score. 
    """
    def sort_scores(self, score_dict):
        rv = []
        for keyword in score_dict.keys():
            rv.append((keyword, score_dict[keyword]))
        rv.sort(key=lambda tup: tup[1])
        return rv

    def
