import click
import os
import shutil

from . import paud as simdak_paud
from .template import TEMPLATE_FILE

CWD = os.getcwd()

EMAIL_HELP = "Alamat email"
PASSWORD_HELP = "Kata sandi / email"
SHEET_HELP = "Nama Sheet excel yang digunakan dokumen"


@click.group("paud")
def paud():
    pass


@paud.command("template")  # type: ignore
@click.argument("nama", default="Simdak-Paud.xlsx", required=True)
def template(nama: str):
    nama = nama if nama.endswith(".xlsx") else nama + ".xlsx"
    click.echo(f"Membuat template dengan nama {nama}")
    dst = os.path.abspath(os.path.join(CWD, nama))
    shutil.copy(TEMPLATE_FILE, dst)


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
@click.argument("file", default="Simdak-Paud.xlsx", required=True)
def exports(email: str, password: str, sheet: str, file: str):
    click.echo(f"Mengeksport data {email} ke {file}")
    simdak_paud.exports(email, password, file)


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
@click.argument("file", default="Simdak-Paud.xlsx", required=True)
def imports(email: str, password: str, sheet: str, file: str):
    click.echo(f"Mengimport data {email} dari {file}")
    simdak_paud.exports(email, password, file)


main = click.CommandCollection("simdak", sources=[paud])

if __name__ == "__main__":
    main()
