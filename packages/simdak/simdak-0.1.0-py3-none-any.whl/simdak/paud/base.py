from requests import Session
from logging import getLogger


class BaseSimdakPaud(object):
    _domain = "https://app.paud-dikmas.kemdikbud.go.id"
    _base_url = "https://app.paud-dikmas.kemdikbud.go.id/simdak/index.php"

    def __init__(self):
        self._logger = getLogger(self.__class__.__name__)
        self._session = Session()
        self._login = False
        self._modul = False
