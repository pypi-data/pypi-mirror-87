from requests import Session
from logging import getLogger
from . import BaseSimdakPaud, SimdakRkasPaud


class SimdakPaud(BaseSimdakPaud):
    def __init__(self, email: str, password: str):
        self._logger = getLogger(self.__class__.__name__)
        self._email = email
        self._password = password
        self._login = self.login()
        self._modul = self.modul()
        self.rkas = SimdakRkasPaud()

    def login(self) -> bool:
        if self._login:
            raise PermissionError("Anda sudah login.")
        params = {"r": "site/login"}
        res = self._session.get(self._base_url, params=params)
        if not res.status_code == 200:
            raise Exception("Error! tidak dapat menghubungi website simdak")
        data = {
            "LoginForm[username]": self._email,
            "LoginForm[password]": self._password,
            "LoginForm[rememberMe]": ["0", "1"],
            "yt0": "Masuk",
        }
        res = self._session.post(self._base_url, data, params=params)
        if res.ok and "DAK NON FISIK" in res.text:
            self._logger.debug(f"Berhasil login dengan {self._email}.")
            return True
        self._logger.error(f"Gagal login dengan {self._email}.")
        return False

    def logout(self) -> bool:
        params = {"r": "site/logout"}
        res = self._session.get(self._base_url, params=params)
        self._logger.debug(f"Berhasil keluar dari akun {self._email}")
        return res.ok

    def modul(self, jenisdak: str = "daknfpaud") -> bool:
        params = {"r": "site/modul", "jenisdak": jenisdak}
        res = self._session.get(self._base_url, params=params)
        if (
            res.ok
            and "RKAS" in res.text
            and "Laporan Penggunaan  Dana (SP)" in res.text
        ):
            self._logger.debug("Berhasil mendapatkan halaman DAK")
            return True
        self._logger.error("Gagal mendapatkan halaman DAK")
        return False

    def __del__(self):
        self.logout()
