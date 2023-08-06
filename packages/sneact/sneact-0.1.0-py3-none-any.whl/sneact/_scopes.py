class _SneactScope:
    def __getattr__(self, item):
        return self.get(item)

    @staticmethod
    def get(item, default=None):
        def get_from_scope(self):
            return self._scope.get(item, default)

        get_from_scope.value_placeholder = default
        return get_from_scope
