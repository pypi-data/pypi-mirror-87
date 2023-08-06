from sneact import Sneact
from sneact._magic_tags import MagicHTMLTag


class ForEach(MagicHTMLTag):
    def __init__(self, each, template):
        self._loop = True
        self._each = each
        self._do = template.compile()
        super().__init__("")

    def do(self, scope):
        html_code = ""
        for item in self._each(scope):
            html_code += self._do.as_html(Sneact({"item": item}))
        return html_code


class Item(MagicHTMLTag):
    def __init__(self):
        super().__init__("")