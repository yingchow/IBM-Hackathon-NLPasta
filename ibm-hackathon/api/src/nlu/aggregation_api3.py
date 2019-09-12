import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SentimentOptions, SyntaxOptions, SyntaxOptionsTokens
from .keywordx import keywordx as kw

class watson_helper:
    def __init__(self, input_dict):
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2018-11-16',
            iam_apikey='5kLneMxCf9SLzD3grPVYfgiYx9Xtx3Arm52SMnrTASQB',
            url='https://gateway.watsonplatform.net/natural-language-understanding/api'
        )
        self.input_dict = input_dict
        self.raw_watson_dict = {} #<id, raw watson data>
        self.keyword_dict = {} #<id, keyword_object[]>
        self.all_keywords_arr = [] #keyword_object[]
        self.meta_score_dict = {} #<keyword text (not metadata), score>
        self.final_rv = []

    """
    Takes in single review, analyzes the text. Puts the keywords in raw_watson_dict
    """
    def analyze_review_text(self, id):
        response = self.nlu.analyze(
            text=self.input_dict[id],
            features=Features(keywords=KeywordsOptions(sentiment=True, limit=5, emotion=True))).get_result()
        self.raw_watson_dict[id] = response

        keyword_array = []
        for keyword in response['keywords']:
            obj = kw(keyword['text'], keyword['sentiment']['score'], keyword['relevance'])
            keyword_array.append(obj)
        self.keyword_dict[id] = keyword_array

    """
    Takes all the keywords from keyword_dict and returns one array of all the keywords
    """
    def all_keywords(self):
        for keyword_arr in self.keyword_dict.values():
            for keyword in keyword_arr:
                self.all_keywords_arr.append(keyword)


    """
    Takes rv from all_keywords and aggregates the score. Returns dict of <keyword text(not object), meta_score>
    """
    def meta_score(self):
        for keyword in self.all_keywords_arr:
            if keyword.text not in self.meta_score_dict:
                self.meta_score_dict[keyword.text] = 0
            self.meta_score_dict[keyword.text] += keyword.relevance * keyword.sentiment

    """
    Returns the relevance for a keyword in a specific piece of feedback
    """

    def keyword_relevance_in_feedback(self, target_keyword, id):
        for keyword in self.keyword_dict[id]:
            if keyword == target_keyword:
                return keyword.relevance
        return 0

    """
    Takes in a keyword, iterates through ALL the feedback and returns an array of ids in ascending order
    of keyword relevance in feedback
    """
    def most_relevant_feedback_for_keyword(self, keyword):
        rv = []
        for id in self.input_dict.keys():
            relevance = self.keyword_relevance_in_feedback(keyword, id)
            rv.append((id, relevance))
        rv.sort(key=lambda tup: tup[1])
        final_rv = []
        for tup in rv:
            if tup[1] != 0:
                final_rv.append((tup[0], tup[1]))
        return final_rv

    """
    2d arrays of keywords and relevance
    """
    def keyword_relevance(self):
        for keyword in self.meta_score_dict.keys():
            rel = self.most_relevant_feedback_for_keyword(keyword)
            self.final_rv.append({'keyword': keyword, 'relevance': rel, 'meta_score': self.meta_score_dict[keyword]})
