from __future__ import annotations
from bs4 import BeautifulSoup, Tag
from typing import List, Optional, Type
from . import BaseSimdakPaud, Rab


class Rkas(BaseSimdakPaud):
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
        self._logger.info(f"RKAS ({self.id}) berhasil dibuka")

    def __call__(self, semester_id: int = 20201, save_as: Type[Rab] = Rab) -> List[Rab]:
        return self.get(semester_id, save_as)

    def get(self, semester_id: int = 20201, save_as: Type[Rab] = Rab) -> List[Rab]:
        results: List[Rab] = []
        params = {"r": "boppaudrkas/create", "id": self.id, "semester_id": semester_id}
        res = self._session.get(self._base_url, params=params)
        if not res.ok:
            return results
        soup = BeautifulSoup(res.text, "html.parser")
        table: Tag = soup.findAll("table")[1]
        for tr in table.findAll("tr"):
            try:
                result = save_as.from_tr(tr)
                results.append(result)
            except ValueError as e:
                self._logger.exception(e)
                continue
        self._logger.info(f"Berhasil mendapatkan {len(results)} rpd")
        return results

    def create(self, rkas_data: Rab, semester_id: int = 20201) -> Optional[Rab]:
        data = rkas_data.as_data()
        data.update({"yt0": "Simpan"})
        params = {"r": "boppaudrkas/create", "id": self.id, "semester_id": semester_id}
        res = self._session.post(self._base_url, data=data, params=params)
        if not res.ok:
            return None
        soup = BeautifulSoup(res.text, "html.parser")
        table: List[Tag] = soup.findAll("table")
        tr: Tag = table[-1].findAll("tr")[-1]
        return Rab.from_tr(tr)
