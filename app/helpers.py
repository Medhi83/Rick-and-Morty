from flask_smorest import Page


class SQLCursorPage(Page):
    """SQL cursor pager"""

    # https://flask-smorest.readthedocs.io/en/latest/pagination.html
    @property
    def item_count(self):
        return self.collection.count()
