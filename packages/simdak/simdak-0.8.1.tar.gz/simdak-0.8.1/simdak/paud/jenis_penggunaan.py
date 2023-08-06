from fuzzywuzzy import fuzz
from logging import getLogger
from typing import Dict, Optional

logger = getLogger(__name__)

JENIS_PENGGUNAAN: Dict[int, Dict[int, str]] = {
    1: {
        21: "bahan pembelajaran peserta didik yang dibutuhkan sesuai dengan kegiatan tematik",
        22: "penyediaan Alat Permainan Edukatif (APE)",
        23: "penyediaan alat mengajar bagi pendidik",
    },
    2: {
        24: "penyediaan makanan tambahan",
        25: "pembelian alat-alat deteksi dini tumbuh kembang, pembelian obat-obatan ringan, dan isi kotak Pertolongan Pertama pada Kecelakaan (P3K)",
        26: "kegiatan pertemuan dengan orang tua/wali murid (kegiatan parenting)",
        27: "memberi transport pendidik",
        28: "penyediaan buku administrasi",
    },
    3: {
        29: "perawatan sarana dan prasarana",
        30: "penyediaan alat- alat publikasi PAUD",
        31: "langganan listrik, telepon/internet, air",
    },
}

PENGGUNAAN = {
    21: "bahan pembelajaran peserta didik yang dibutuhkan sesuai dengan kegiatan tematik",
    22: "penyediaan Alat Permainan Edukatif (APE)",
    23: "penyediaan alat mengajar bagi pendidik",
    24: "penyediaan makanan tambahan",
    25: "pembelian alat-alat deteksi dini tumbuh kembang, pembelian obat-obatan ringan, dan isi kotak Pertolongan Pertama pada Kecelakaan (P3K)",
    26: "kegiatan pertemuan dengan orang tua/wali murid (kegiatan parenting)",
    27: "memberi transport pendidik",
    28: "penyediaan buku administrasi",
    29: "perawatan sarana dan prasarana",
    30: "penyediaan alat- alat publikasi PAUD",
    31: "langganan listrik, telepon/internet, air",
}

JENIS_KOMPONEN = {
    1: "Kegiatan Pembelajaran dan Bermain",
    2: "Kegiatan Pendukung",
    3: "Kegiatan Lainnya",
}


def get_key(nama: str, data: Dict[int, str] = JENIS_KOMPONEN) -> Optional[int]:
    nama = nama.replace("\r\n", " ")
    for k, v in data.items():
        if v == nama:
            return k
    return None


def get_fuzz(f: str, data: Dict[int, str], default: int = 0, ok: int = 80) -> int:
    for k, v in data.items():
        if fuzz.ratio(v, f) > ok:
            logger.debug(f"Key dari {f} ditemukan")
            return k
    logger.debug(f"Key dari {f} tidak ditemukan")
    return default
