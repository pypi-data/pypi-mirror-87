from cmdliner import cli
from unittest.mock import patch


@cli("1.0")
def main():
    print("hello")


def test_version(capsys):
    with patch("sys.argv", ["program_name", "--version"]):
        main()
    assert capsys.readouterr().out == "__main__.py 1.0\n"
