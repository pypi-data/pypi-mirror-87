import subprocess

import pytest


@pytest.fixture
def when_no_deps():
    try:
        from bs4 import BeautifulSoup  # noqa F401: imported not used
        # no raise - it's installed
        pytest.skip("This test requires bs4 to be not installed.")
    except ImportError:
        "raised - so perform the test (do not skip)"


def test_dependencies_message(when_no_deps, local_file):
    hello_html_path = local_file('documents', 'hello_world.html')
    p = subprocess.Popen(["airium", str(hello_html_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    assert out == b''
    assert b"Please install `requests` package in order to fetch html files from web." in err


def test_cannot_import_translator(when_no_deps, capsys):
    from airium import from_html_to_airium as tr

    tr()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == 'In order to parse HTML, please install beautifulsoup4 package.'


def test_no_deps_but_airium_base_works():
    from airium import Airium
    a = Airium()
    with a.div(klass="one"):
        a("that")
        a.br()
        a.span(_t="works")

    assert str(a) == """\
<div class="one">
  that
  <br />
  <span>works</span>
</div>"""
