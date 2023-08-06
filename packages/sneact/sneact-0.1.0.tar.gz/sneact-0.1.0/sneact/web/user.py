from sneact import Sneact


class User:
    def __init__(self, intial_props=None, default_state=None):
        if intial_props is None:
            intial_props = dict()
        if default_state is None:
            default_state = dict()
        self.props = intial_props
        self.state = default_state

    def as_sneact(self):
        return Sneact({**self.props, **self.state})
