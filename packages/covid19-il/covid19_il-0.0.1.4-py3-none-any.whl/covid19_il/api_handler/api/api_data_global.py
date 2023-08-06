from covid19_il.api_handler.iapi_handler import IAPIHandler


class ApiDataGlobal(IAPIHandler):
    def __init__(self, logger):
        self._logger = logger

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def _get_request(self) -> Exception:
        pass

    def url_query(self) -> Exception:
        pass

