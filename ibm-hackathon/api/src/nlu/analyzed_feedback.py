"""
REVIEW_TEXT: Original review text
KEYWORDS: Array of keywords objects for the text
"""
class analyzed_feedback:
    def __init__(self, review_text, keywords, rating=None):
        self.review_text = review_text
        self.keywords = keywords
        self.rating = rating

    def __repr__(self):
        return str(self.keywords) + self.review_text

    def get_keyword_with_text(self, text):
        for keyword in self.keywords:
            if keyword.text == text:
                return keyword
