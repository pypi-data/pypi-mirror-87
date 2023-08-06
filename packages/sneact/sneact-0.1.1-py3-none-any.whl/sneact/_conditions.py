from sneact._magic_tags import (
    MagicHTMLTag,
    magic_html_chain_method,
)


class When(MagicHTMLTag):
    def __init__(self, on, template):
        self._condition = True
        self._on = on
        self._then = template.compile()
        super().__init__("")

    def evaluate(self, scope):
        return self._on(scope)

    @property
    def then(self):
        return self._then

    def __matmul__(self, other):
        del other
        raise ValueError("You cant chain 'when' conditions.")


class WhenNot(When):
    def evaluate(self, scope):
        return not self._on(scope)
