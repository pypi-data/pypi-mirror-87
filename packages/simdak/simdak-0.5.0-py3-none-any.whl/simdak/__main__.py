import click
import os
import shutil
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from . import paud as simdak_paud
from .template import TEMPLATE_FILE

CWD = os.getcwd()

EMAIL_HELP = "Alamat email"
PASSWORD_HELP = "Kata sandi / email"
SHEET_HELP = "Nama Sheet excel yang digunakan dokumen"


@click.group("paud")
def paud():
    pass


@paud.command("bantuan")  # type: ignore
def bantuan():
    help_msg = (
        "Untuk mengambil data gunakan export, untuk mengirim data gunakan import. "
        "export nama-file\n"
        "import nama-file\n"
        "Tips : Export dahulu, tambahkan RPD lalu import\n"
        "!Jangan rubah cell yang berwarna kuning!\n"
        "!Pastikan setiap RPD bernomor yang urut!\n"
    )
    click.echo(help_msg)


@paud.command("template")  # type: ignore
@click.argument("nama", default="Simdak-Paud.xlsx", required=True)
def template(nama: str):
    nama = nama if nama.endswith(".xlsx") else nama + ".xlsx"
    click.echo(f"Membuat template dengan nama {nama}")
    dst = os.path.abspath(os.path.join(CWD, nama))
    shutil.copy(TEMPLATE_FILE, dst)
    click.echo(f"Berhasil membuat template {nama}")


@paud.command("export")  # type: ignore
@click.option("--email", required=True, prompt=True, help=EMAIL_HELP)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help=PASSWORD_HELP,
)
@click.option("--sheet", default="Sheet1", required=False, help=SHEET_HELP)
@click.argument("file", default="", required=False)
def exports(email: str, password: str, sheet: str, file: str):
    click.echo(f"Mengeksport data {email} ke {file}")
    try:
        simdak_paud.exports(email, password, file)
        click.echo(f"Export data {email} berhasil!")
    except Exception as e:
        click.echo(f"Export data gagal! Karena {e}")


@paud.command("import")  # type: ignore
@click.option("--email", required=True, prompt=True, help=EMAIL_HELP)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help=PASSWORD_HELP,
)
@click.option("--sheet", default="Sheet1", required=False, help=SHEET_HELP)
@click.argument("file", default="", required=False)
def imports(email: str, password: str, sheet: str, file: str):
    click.echo(f"Mengimport data {email} dari {file}")
    try:
        simdak_paud.imports(email, password, file)
        click.echo(f"Import data berhasil!")
    except Exception as e:
        click.echo(f"Export data gagal! Karena {e}")


main = click.CommandCollection("simdak", sources=[paud])

if __name__ == "__main__":
    main()
