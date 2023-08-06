from bs4 import BeautifulSoup
from dataclasses import dataclass
from requests import Session
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .paud import SimdakPaud

from . import BaseSimdakPaud, JENIS_KOMPONEN, JENIS_PENGGUNAAN, PENGGUNAAN


class RkasData(BaseSimdakPaud):
    simdak: SimdakPaud

    def __init__(
        self,
        jenis_komponen_id: int,
        jenis_penggunaan_id: int,
        jenisbelanja: str,
        qty: int,
        satuan: str,
        hargasatuan: int,
    ):
        self.jenis_komponen_id = jenis_komponen_id
        self.jenis_penggunaan_id = jenis_penggunaan_id
        self.jenisbelanja = jenisbelanja
        self.qty = qty
        self.satuan = satuan
        self.hargasatuan = hargasatuan

    def as_data(self, **kwargs) -> dict:
        jenis_komponen_id = str(self.jenis_komponen_id)
        if jenis_komponen_id not in JENIS_PENGGUNAAN:
            raise ValueError(f"jenis komponen {self.jenis_komponen_id} tidak valid!")
        jenis_penggunaan_id = str(self.jenis_penggunaan_id)
        if jenis_penggunaan_id not in JENIS_PENGGUNAAN[jenis_komponen_id]:
            raise ValueError(
                f"jenis penggunaan {self.jenis_penggunaan_id} tidak valid!"
            )
        data = {
            "Boppaudrkas[jenis_komponen_id]": self.jenis_komponen_id,
            "Boppaudrkas[jenis_penggunaan_id]": self.jenis_penggunaan_id,
            "Boppaudrkas[jenisbelanja]": self.jenisbelanja.replace(" ", "+"),
            "Boppaudrkas[qty]": self.qty,
            "Boppaudrkas[satuan]": self.satuan.replace(" ", "+"),
            "Boppaudrkas[hargasatuan]": self.hargasatuan,
        }
        data.update(kwargs)
        return data


class Rkas(BaseSimdakPaud):
    simdak: SimdakPaud

    def __init__(
        self,
        no: str,
        npsn: str,
        satuan_pendidikan: str,
        alamat: str,
        alokasi: str,
        kegiatan_pembelajaran_dan_bermain: str,
        kegiatan_pendukung: str,
        kegiatan_lainnya: str,
        jumlah: str,
        url: str,
    ):
        self.no = no
        self.npsn = npsn
        self.satuan_pendidikan = satuan_pendidikan
        self.alamat = alamat
        self.alokasi = alokasi
        self.kegiatan_pembelajaran_dan_bermain = kegiatan_pembelajaran_dan_bermain
        self.kegiatan_pendukung = kegiatan_pendukung
        self.kegiatan_lainnya = kegiatan_lainnya
        self.jumlah = jumlah
        self.url = url
        self.id = self.url.split("&")[1].split("=")[-1]

    def __call__(self, semester_id: int = 20201) -> List[RkasData]:
        return self.get(semester_id)

    def get(self, semester_id: int = 20201) -> List[RkasData]:
        results: List[RkasData] = []
        params = {"r": "boppaudrkas/create", "id": self.id, "semester_id": semester_id}
        res = self.simdak._session.get(self._base_url, params=params)
        if not res.ok:
            return results
        soup = BeautifulSoup(res.text, "lxml")
        return results

    def create(self, rkas_data: RkasData, semester_id: int = 20201):
        data = rkas_data.as_data()
        data.update({"yt0": "Simpan"})
        params = {"r": "boppaudrkas/creat", "id": self.id, "semester_id": semester_id}


class RkasPaud(BaseSimdakPaud):
    simdak: SimdakPaud

    def __init__(self, paud: SimdakPaud):
        self.simdak = paud

    def __call__(self, semester_id: int = 20201) -> List[Rkas]:
        assert self.simdak._login and self.simdak._modul
        results: List[Rkas] = []
        params = {
            "r": "boppaudrkas/index",
            "Boppaudrkas[semester_id]": semester_id,
            "yt0": "Cari",
        }
        res = self.simdak._session.get(self.simdak._base_url, params=params)
        if not res.status_code == 200:
            return results
        soup = BeautifulSoup(res.text, "lxml")
        for tr in soup.findAll("tr", {"class": "view"}):
            tds = tr.findAll("td")
            result = Rkas(
                no=tds[0].get_text(),
                npsn=tds[1].get_text(),
                satuan_pendidikan=tds[2].get_text(),
                alamat=tds[3].get_text(),
                alokasi=tds[4].get_text(),
                kegiatan_pembelajaran_dan_bermain=tds[5].get_text(),
                kegiatan_pendukung=tds[6].get_text(),
                kegiatan_lainnya=tds[7].get_text(),
                jumlah=tds[8].get_text(),
                url=self.simdak._domain + tds[9].find("a")["href"] or "",
            )
            result.simdak = self.simdak
            results.append(result)
        return results
