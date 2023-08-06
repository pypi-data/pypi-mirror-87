from sneact._magic_tags import (
    MagicHTMLTag,
    magic_html_chain_method,
    magic_html_mod_method,
)


class Sneact(MagicHTMLTag):
    def __init__(self, scope=None):
        self._sneact = True
        if scope is None:
            scope = dict()
        self._scope = scope
        super().__init__("")

    def update(self, scope):
        self._scope.update(scope)
