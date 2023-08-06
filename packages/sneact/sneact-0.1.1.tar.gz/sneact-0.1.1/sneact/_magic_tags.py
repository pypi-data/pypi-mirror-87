import warnings


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
        warnings.warn(
            "The as_html method is too slow. We recomend to use 'compile().as_html()'.",
            UserWarning,
        )
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

    def compile(self):
        return Template(self)

    __lshift__ = magic_html_chain_method("<")
    __rshift__ = magic_html_chain_method(">")
    __truediv__ = magic_html_chain_method("/")
    __pow__ = magic_html_chain_method("")
    __matmul__ = magic_html_chain_method("")
    __pos__ = magic_html_mod_method("")
    __neg__ = magic_html_mod_method("/")


class Template:
    def __init__(self, compileable):
        self.segments = []
        last_segment = ""
        for segment in compileable.segments:
            if hasattr(segment, "_sneact"):
                self.sneact = segment
            elif (
                hasattr(segment, "_condition")
                or hasattr(segment, "_loop")
                or hasattr(segment, "value_placeholder")
            ):
                self.segments.append(last_segment)
                self.segments.append(segment)
                last_segment = ""
            elif isinstance(segment, MagicHTMLTag):
                last_segment = last_segment + segment.token
            else:
                last_segment = last_segment + segment
        self.segments.append(last_segment)

    def compile(self):
        return self

    def as_html(self, data=None):
        if data is None:
            sneact = self.sneact
        else:
            try:
                sneact = data
            except TypeError:
                sneact = data._scope
            try:
                sneact.update(data)
            except TypeError:
                sneact.update(data._scope)
        html_code = ""
        for segment in self.segments:
            if hasattr(segment, "_condition"):
                if segment.evaluate(sneact):
                    then = segment.then.as_html(sneact)
                    html_code = html_code + then
            elif hasattr(segment, "_loop"):
                html_code = html_code + segment.do(sneact)
            elif hasattr(segment, "value_placeholder"):
                nested = segment(sneact)
                if isinstance(nested, MagicHTMLTag):
                    warnings.warn(
                        f"Nested template {repr(nested)} are not compiled with 'compile()'.",
                        UserWarning,
                    )
                    nested = nested.compile().as_html(sneact)
                elif isinstance(nested, Template):
                    nested = nested.as_html(sneact)
                if callable(nested):
                    nested = nested()
                html_code = html_code + str(nested)
            else:
                html_code = html_code + segment
        return html_code

    def show_for(self, user):
        return self.as_html(user.as_sneact())
