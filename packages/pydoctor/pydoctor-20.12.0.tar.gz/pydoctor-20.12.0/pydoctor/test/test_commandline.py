from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import os
import sys

from pydoctor import driver

from . import CapSys


def geterrtext(*options: str) -> str:
    """
    Run CLI with options and return the output triggered by system exit.
    """
    se = sys.stderr
    f = StringIO()
    print(options)
    sys.stderr = f
    try:
        try:
            driver.main(list(options))
        except SystemExit:
            pass
        else:
            assert False, "did not fail"
    finally:
        sys.stderr = se
    return f.getvalue()

def test_invalid_option() -> None:
    err = geterrtext('--no-such-option')
    assert 'no such option' in err

def test_cannot_advance_blank_system() -> None:
    err = geterrtext('--make-html')
    assert 'No source paths given' in err

def test_no_systemclasses_py3() -> None:
    err = geterrtext('--system-class')
    assert 'requires 1 argument' in err

def test_invalid_systemclasses() -> None:
    err = geterrtext('--system-class=notdotted')
    assert 'dotted name' in err
    err = geterrtext('--system-class=no-such-module.System')
    assert 'could not import module' in err
    err = geterrtext('--system-class=pydoctor.model.Class')
    assert 'is not a subclass' in err


def test_projectbasedir_absolute() -> None:
    """
    The --project-base-dir option, when given an absolute path, should set that
    path as the projectbasedirectory attribute on the options object.
    """
    if os.name == 'nt':
        absolute = r"C:\Users\name\src\project"
    else:
        absolute = "/home/name/src/project"
    options, args = driver.parse_args(["--project-base-dir", absolute])
    assert str(options.projectbasedirectory) == absolute


def test_projectbasedir_relative() -> None:
    """
    The --project-base-dir option, when given a relative path, should convert
    that path to absolute and set it as the projectbasedirectory attribute on
    the options object.
    """
    relative = "projbasedirvalue"
    options, args = driver.parse_args(["--project-base-dir", relative])
    assert options.projectbasedirectory.is_absolute()
    assert options.projectbasedirectory.name == relative
    assert options.projectbasedirectory.parent == Path.cwd()


def test_cache_enabled_by_default() -> None:
    """
    Intersphinx object caching is enabled by default.
    """
    parser = driver.getparser()
    (options, _) = parser.parse_args([])
    assert options.enable_intersphinx_cache


def test_cli_warnings_on_error() -> None:
    """
    The --warnings-as-errors option is disabled by default.
    This is the test for the long form of the CLI option.
    """
    options, args = driver.parse_args([])
    assert options.warnings_as_errors == False

    options, args = driver.parse_args(['--warnings-as-errors'])
    assert options.warnings_as_errors == True


def test_main_project_name_guess(capsys: CapSys) -> None:
    """
    When no project name is provided in the CLI arguments, a default name
    is used and logged.
    """
    exit_code = driver.main(args=[
        '-v', '--testing',
        'pydoctor/test/testpackages/basic/'
        ])

    assert exit_code == 0
    assert "Guessing 'basic' for project name." in capsys.readouterr().out


def test_main_project_name_option(capsys: CapSys) -> None:
    """
    When a project name is provided in the CLI arguments nothing is logged.
    """
    exit_code = driver.main(args=[
        '-v', '--testing',
        '--project-name=some-name',
        'pydoctor/test/testpackages/basic/'
        ])

    assert exit_code == 0
    assert 'Guessing ' not in capsys.readouterr().out


def test_main_return_zero_on_warnings() -> None:
    """
    By default it will return 0 as exit code even when there are warnings.
    """
    stream = StringIO()
    with redirect_stdout(stream):
        exit_code = driver.main(args=[
            '--html-writer=pydoctor.test.InMemoryWriter',
            'pydoctor/test/testpackages/report_trigger/'
            ])

    assert exit_code == 0
    assert "__init__.py:8: Unknown field 'bad_field'" in stream.getvalue()
    assert 'report_module.py:9: Cannot find link target for "BadLink"' in stream.getvalue()


def test_main_return_non_zero_on_warnings() -> None:
    """
    When `-W` is used it returns 3 as exit code when there are warnings.
    """
    stream = StringIO()
    with redirect_stdout(stream):
        exit_code = driver.main(args=[
            '-W',
            '--html-writer=pydoctor.test.InMemoryWriter',
            'pydoctor/test/testpackages/report_trigger/'
            ])

    assert exit_code == 3
    assert "__init__.py:8: Unknown field 'bad_field'" in stream.getvalue()
    assert 'report_module.py:9: Cannot find link target for "BadLink"' in stream.getvalue()
