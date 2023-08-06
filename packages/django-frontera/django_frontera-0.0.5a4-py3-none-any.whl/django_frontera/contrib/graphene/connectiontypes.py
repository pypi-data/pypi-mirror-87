class PageInfo(object):

    def __init__(self, start_cursor="", end_cursor="",
                 has_previous_page=False, has_next_page=False, total_count=0):
        self.startCursor = start_cursor
        self.endCursor = end_cursor
        self.hasPreviousPage = has_previous_page
        self.hasNextPage = has_next_page
        self.totalCount = total_count

    def to_dict(self):
        return {
            'startCursor': self.startCursor,
            'endCursor': self.endCursor,
            'hasPreviousPage': self.hasPreviousPage,
            'hasNextPage': self.hasNextPage,
            'totalCount': self.totalCount,
        }