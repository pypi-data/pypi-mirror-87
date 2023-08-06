import click
import os
import shutil

from . import TEMPLATE_DIR, paud

CWD = os.getcwd()


@click.group()
def main():
    pass


@click.command("template")
@click.argument("nama", default="Simdak-Paud.xlsx")
def template(nama: str):
    click.echo("Membuat template...")
    shutil.copy(
        os.path.join(TEMPLATE_DIR, "Simdak-Paud.xlsx"),
        os.path.join(CWD, nama),
    )


@click.command("export")
@click.option("--email", prompt=True)
@click.password_option()
@click.argument("nama", default="Simdak-Paud.xlsx", required=True)
def exports(email: str, password: str, nama: str):
    filepath = os.path.join(CWD, nama)
    paud.exports(filepath, email, password)


@click.command("import")
@click.option("--email", prompt=True)
@click.password_option()
@click.argument("nama", default="Simdak-Paud.xlsx", required=True)
def imports(email: str, password: str, nama: str):
    filepath = os.path.join(CWD, nama)
    paud.imports(filepath, email, password)


if __name__ == "__main__":
    main()
