class Answer:
    """
    机器人回答
    """
    def __init__(self, text: str,related:list=[],score: float=0.0):
        self.text = text
        self.related = related
        self.score = score

    def __str__(self):
        if self.related:
            return 'text: {},related: {}, score: {}'.format(self.text,self.related, self.score if self.score else 0.0)
        return 'text: {}, score: {}'.format(self.text,self.score if self.score else 0.0)
    def __repr__(self):
        return self.__str__()

    def keys(self):
        return ('text', 'related', 'score')
    def __getitem__(self, item):
        return getattr(self, item)
