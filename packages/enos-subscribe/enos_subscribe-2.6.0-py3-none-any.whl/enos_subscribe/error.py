from __future__ import absolute_import


class EnosClientError(RuntimeError):
    def __str__(self):
        if not self.args:
            return self.__class__.__name__
        return '{0}: {1}'.format(self.__class__.__name__,
                                 super(EnosClientError, self).__str__())


class EnosClientConfigurationError(EnosClientError):
    pass


class EnosClientSubIdNotExist(EnosClientError):
    pass


class EnosClientInnerParamsError(EnosClientError):
    pass
