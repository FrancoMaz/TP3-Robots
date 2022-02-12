class Result:
    def __init__(self, thumbnail, permalink, query):
        self.thumbnail = thumbnail
        self.permalink = permalink
        self.query = query

    def __str__(self):
        return "Result for query % s: thumbnail is % s and permalink is % s " % (
            self.query, self.thumbnail, self.permalink)
