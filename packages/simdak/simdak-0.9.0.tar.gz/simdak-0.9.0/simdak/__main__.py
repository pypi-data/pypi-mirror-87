#!/usr/bin/env python
import click
import os
import shutil
import logging


from . import paud as simdak_paud
from .template import TEMPLATE_FILE

CWD = os.getcwd()

EMAIL_HELP = "Alamat email"
PASSWORD_HELP = "Kata sandi / email"
SHEET_HELP = "Nama Sheet excel yang digunakan dokumen"


def log_level(level: int):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    if level == logging.DEBUG:
        click.echo("Debug diaktifkan!")


class CommandContext:
    def __init__(self, debug: bool):
        self.debug = debug


@click.group("paud")
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def paud(ctx: click.Context, debug: bool):
    context = CommandContext(debug)
    ctx.obj = context
    log_level(logging.DEBUG if debug else logging.INFO)


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
@click.option("--debug/--no-debug", required=False, default=False)
@click.argument("file", default="", required=False)
def exports(email: str, password: str, sheet: str, debug: bool, file: str):
    log_level(logging.DEBUG if debug else logging.INFO)
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
@click.option("--dari", default=1, required=False, help="Dari nomor")
@click.option("--ke", default=0, required=False, help="Ke nomor")
@click.option(
    "--simpan/--no-simpan", default=True, is_flag=True, required=False, help="Simpan id"
)
@click.option("--sheet", default="Sheet1", required=False, help=SHEET_HELP)
@click.option("--debug/--no-debug", required=False, default=False)
@click.argument("file", default="", required=False)
def imports(
    email: str,
    password: str,
    dari: int,
    ke: int,
    simpan: bool,
    sheet: str,
    debug: bool,
    file: str,
):
    log_level(logging.DEBUG if debug else logging.INFO)
    click.echo(f"Mengimport data {email} dari {file}")
    try:
        simdak_paud.imports(
            email,
            password,
            file,
            start=int(dari),
            ke=int(ke),
            sheet=str(sheet),
            save=simpan,
        )
        click.echo(f"Import data berhasil!")
    except Exception as e:
        click.echo(f"Export data gagal! Karena {e}")


@paud.command("reset")  # type: ignore
@click.option("--email", required=True, prompt=True, help=EMAIL_HELP)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help=PASSWORD_HELP,
)
@click.option("--semester", default=20201)
@click.option("--debug/--no-debug", required=False, default=False)
def reset(email: str, password: str, semester: int, debug: bool):
    log_level(logging.DEBUG if debug else logging.INFO)
    sp = simdak_paud.SimdakPaud(email, password)
    rkas = sp.rkas.get(semester)[0]
    rabs = rkas.get()
    for rab in rabs:
        if rab.delete():
            click.echo(f"RAB [{rab.data_id}] berhasil dihapus")
        else:
            click.echo(f"RAB [{rab.data_id}] gagal dihapus")
    sp.logout()


main = click.CommandCollection("simdak", sources=[paud])


if __name__ == "__main__":
    main()
