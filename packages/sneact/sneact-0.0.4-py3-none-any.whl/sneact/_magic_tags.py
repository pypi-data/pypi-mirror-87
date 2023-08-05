def magic_html_chain_method(op):
    def method(self, other):
        self_copy = MagicHTMLTag(self.token)
        try:
            self_copy.segments = (
                *(s for s in self.segments),
                op,
                *(s for s in other.segments),
            )
        except AttributeError:
            self_copy.segments = (*(s for s in self.segments), op, other)
        return self_copy

    return method


def magic_html_mod_method(op):
    def method(self):
        self_copy = MagicHTMLTag(self.token)
        self_copy.segments = (
            op,
            *(s for s in self.segments),
        )
        return self_copy

    return method


class MagicHTMLTag:
    def __init__(self, token_name):
        self.token = token_name
        self.segments = (self,)

    def __call__(self, **kwargs):
        attributes_segments = []
        for k, v in kwargs.items():
            attributes_segments.extend((" ", k, "=", v))
        self_with_attributes = MagicHTMLTag(self.token)
        self_with_attributes.segments += tuple(attributes_segments)
        self_with_attributes.segments += self.segments[1:]
        return self_with_attributes

    def as_html(self):
        html_code = ""
        sneact = None
        for segment in self.segments:
            if hasattr(segment, "_sneact"):
                sneact = segment
            if isinstance(segment, MagicHTMLTag):
                html_code = html_code + segment.token
            elif hasattr(segment, "value_placeholder"):
                nested = segment(sneact)
                if isinstance(nested, MagicHTMLTag):
                    nested = nested.as_html()
                html_code = html_code + str(nested)
            else:
                html_code = html_code + segment
        return html_code

    __lshift__ = magic_html_chain_method("<")
    __rshift__ = magic_html_chain_method(">")
    __truediv__ = magic_html_chain_method("/")
    __pow__ = magic_html_chain_method("")
    __neg__ = magic_html_mod_method("/")
