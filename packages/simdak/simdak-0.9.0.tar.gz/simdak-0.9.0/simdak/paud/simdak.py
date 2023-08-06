from __future__ import annotations
from bs4 import BeautifulSoup
from typing import List
from . import BaseSimdakPaud, Rkas

class SimdakRkasPaud(BaseSimdakPaud):
    # TODO : Refactor!
    def __call__(self, semester_id: int = 20201) -> List[Rkas]:
        return self.get(semester_id)

    def get(self, semester_id: int = 20201) -> List[Rkas]:
        results: List[Rkas] = []
        params = {
            "r": "boppaudrkas/index",
            "Boppaudrkas[semester_id]": semester_id,
            "yt0": "Cari",
        }
        res = self._session.get(self._base_url, params=params)
        if not res.status_code == 200:
            return results
        soup = BeautifulSoup(res.text, "html.parser")
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
                url=self._domain + tds[9].find("a")["href"] or "",
            )
            self._logger.debug(f"Berhasil mendapat RKAS [{result.id}]")
            results.append(result)
        return results
