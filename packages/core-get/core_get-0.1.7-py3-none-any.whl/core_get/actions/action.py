from core_get.options.options import Options


class Action:
    def exec(self, options: Options):
        raise NotImplementedError
