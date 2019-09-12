import json
from analyzed_feedback import analyzed_feedback
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SentimentOptions, SyntaxOptions, SyntaxOptionsTokens
from nltk.corpus import wordnet as wn

class aggregation_api:
    key = '5kLneMxCf9SLzD3grPVYfgiYx9Xtx3Arm52SMnrTASQB'
    url = 'https://gateway.watsonplatform.net/natural-language-understanding/api'

    """
    KEYWORDS: Array of keywords to by evaluated for sentiment
    TEXT: .txt or .json file.  TO DO: Convert it into a usable string 
    """
    def senti(self, keywords, text):
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2018-11-16',
            iam_apikey=aggregation_api.key,
            url=aggregation_api.url
        )

        response = natural_language_understanding.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions(targets=keywords))).get_result()

        print(json.dumps(response, indent=2))


    """
    Returns json of sentiment, keywords, and relevance
    TEXT: text file
    """
    def keywords(self, text="somewhere over the rainbow"):
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2018-11-16',
            iam_apikey=aggregation_api.key,
            url=aggregation_api.url
        )

        #with open('sample_feedback.txt', 'r') as file:
        #    data = file.read().replace('\n', '')

        response = natural_language_understanding.analyze(
            return_analyzed_text=True,
            text=text,
            part_of_speech=True,
            features=Features(keywords=KeywordsOptions(sentiment=True, limit=10))).get_result()
        print(response)
        return response

    """
    Given an analyzed_feedback object, will get the syntax of the keywords and store that information. Syntax is for the
    first instance of each word. 
    """
    def get_syntax(self, analyzed):
        keyword_set = set()
        for keyword in analyzed.keywords:
            keyword_set.add(keyword['text'])

        response = natural_language_understanding.analyze(
            return_analyzed_text=True,
            text=analyzed.feedback,
            part_of_speech=True,
            features=Features(syntax=SyntaxOptions(tokens=SyntaxOptionsTokens(lemma=True, part_of_speech=True, )))).get_result()

        print(response)

    """
    Takes in an array of raw feedback data. Returns an array with the feedback, keywords, and sentiment
     
    """
    def analyze(self, feedback_array):
        rv = []
        for feedback in feedback_array:
            temp = self.keywords(feedback)
            rv.append(analyzed_feedback(temp))
        return rv




with open('sample_feedback.txt', 'r') as file:
    data = file.read().replace('\n', '')
feedback_array = [data, "I really hated the ribeye steak. The steak fucking sucked. Never eat the steak."]
test = aggregation_api()
print(test.get_syntax(test.analyze(feedback_array)[0]))
