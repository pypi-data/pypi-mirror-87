"""Tests for CoBib's commands."""
# pylint: disable=unused-argument, redefined-outer-name

import os
import re
import sys
from datetime import datetime
from io import StringIO
from itertools import zip_longest
from pathlib import Path
from shutil import copyfile

import pytest
from cobib import commands
from cobib.config import CONFIG
from cobib.database import read_database


@pytest.fixture
def setup():
    """Setup."""
    root = os.path.abspath(os.path.dirname(__file__))
    CONFIG.set_config(Path(root + '/../cobib/docs/debug.ini'))
    read_database()


def test_set_config(setup):
    """Test config setting.

    Args:
        setup: runs pytest fixture.
    """
    # from setup
    assert CONFIG.config['DATABASE']['file'] == './test/example_literature.yaml'
    # change back to default
    CONFIG.set_config()
    assert CONFIG.config['DATABASE']['file'] == \
        os.path.expanduser('~/.local/share/cobib/literature.yaml')


def test_init():
    """Test init command."""
    # use temporary config
    tmp_config = "[DATABASE]\nfile=/tmp/cobib_test_database.yaml\n"
    with open('/tmp/cobib_test_config.ini', 'w') as file:
        file.write(tmp_config)
    CONFIG.set_config(Path('/tmp/cobib_test_config.ini'))
    # store current time
    now = float(datetime.now().timestamp())
    commands.InitCommand().execute({})
    # check creation time of temporary database file
    ctime = os.stat('/tmp/cobib_test_database.yaml').st_ctime
    # assert these times are close
    assert ctime - now < 0.1 or now - ctime < 0.1
    # clean up file system
    os.remove('/tmp/cobib_test_database.yaml')
    os.remove('/tmp/cobib_test_config.ini')


def test_init_safe():
    """Test init aborts when database file exists."""
    # use temporary config
    tmp_config = "[DATABASE]\nfile=/tmp/cobib_test_database.yaml\n"
    with open('/tmp/cobib_test_config.ini', 'w') as file:
        file.write(tmp_config)
    CONFIG.set_config(Path('/tmp/cobib_test_config.ini'))
    # fill database file
    with open('/tmp/cobib_test_database.yaml', 'w') as file:
        file.write('test')
    # try running init
    commands.InitCommand().execute({})
    # check init aborted and database file still contains 'test'
    with open('/tmp/cobib_test_database.yaml', 'r') as file:
        assert file.read() == 'test'
    # clean up file system
    os.remove('/tmp/cobib_test_database.yaml')
    os.remove('/tmp/cobib_test_config.ini')


# DEPRECATD: to be removed in v2.6
def test_init_force():
    """Test init can be forced when database file exists."""
    # use temporary config
    tmp_config = "[DATABASE]\nfile=/tmp/cobib_test_database.yaml\n"
    with open('/tmp/cobib_test_config.ini', 'w') as file:
        file.write(tmp_config)
    CONFIG.set_config(Path('/tmp/cobib_test_config.ini'))
    # fill database file
    with open('/tmp/cobib_test_database.yaml', 'w') as file:
        file.write('test')
    # try running init
    with pytest.deprecated_call():
        commands.InitCommand().execute(['-f'])
        # check init was forced and database file was overwritten
        assert os.stat('/tmp/cobib_test_database.yaml').st_size == 0
    # clean up file system
    os.remove('/tmp/cobib_test_database.yaml')
    os.remove('/tmp/cobib_test_config.ini')


@pytest.mark.parametrize(['args', 'expected'], [
        [[], ['einstein', 'latexcompanion', 'knuthwebsite']],
        [['-r'], ['knuthwebsite', 'latexcompanion', 'einstein']],
        [['-s', 'year'], ['einstein', 'knuthwebsite', 'latexcompanion']],
        [['-r', '-s', 'year'], ['latexcompanion', 'knuthwebsite', 'einstein']],
    ])
def test_list(setup, args, expected):
    """Test list command.

    Args:
        setup: runs pytest fixture.
        args: arguments for the list command call.
        expected: expected result.
    """
    # redirect output of list to string
    file = StringIO()
    tags = commands.ListCommand().execute(args, out=file)
    assert tags == expected
    for line in file.getvalue().split('\n'):
        if line.startswith('ID') or all([c in '- ' for c in line]):
            # skip table header
            continue
        assert line.split()[0] in expected


def test_list_with_missing_keys(setup):
    """Asserts issue #1 is fixed.

    When a key is queried which is not present in all entries, the list command should return
    normally.

    Args:
        setup: runs pytest fixture.
    """
    # redirect output of list to string
    file = StringIO()
    tags = commands.ListCommand().execute(['++year', '1905'], out=file)
    expected = ['einstein']
    assert tags == expected
    for line in file.getvalue().split('\n'):
        if line.startswith('ID') or all([c in '- ' for c in line]):
            # skip table header
            continue
        assert line.split()[0] in expected


def test_show(setup):
    """Test show command.

    Args:
        setup: runs pytest fixture.
    """
    file = StringIO()
    commands.ShowCommand().execute(['einstein'], out=file)
    with open('./test/example_literature.bib', 'r') as expected:
        for line, truth in zip_longest(file.getvalue().split('\n'), expected):
            if not line:
                continue
            assert line == truth.strip('\n')


@pytest.fixture
def open_setup():
    """Setup for OpenCommand testing."""
    # ensure configuration is empty
    CONFIG.config = {}
    root = os.path.abspath(os.path.dirname(__file__))
    CONFIG.set_config(Path(root + '/../cobib/docs/debug.ini'))
    # NOTE: normally you would never trigger an Add command before reading the database but in this
    # controlled testing scenario we can be certain that this is fine
    commands.AddCommand().execute(['-b', './test/dummy_multi_file_entry.bib'])
    read_database()
    yield setup
    # clean up
    commands.DeleteCommand().execute(['dummy_multi_file_entry'])


def test_open(open_setup):
    """Test open command.

    Args:
        open_setup: runs pytest fixture.
    """
    # pylint: disable=missing-class-docstring
    class DummyStdin:
        # pylint: disable=missing-function-docstring
        def readline(self):
            # pylint: disable=no-self-use
            return '\n'
    # replace sys.stdout and sys.stdin
    original_stdout = sys.stdout
    original_stdin = sys.stdin
    sys.stdout = StringIO()
    sys.stdin = DummyStdin()
    commands.OpenCommand().execute(['dummy_multi_file_entry'])
    expected = [
        "  1: [file] /tmp/a.txt",
        "  2: [file] /tmp/b.txt",
        "  3: [url] https://www.duckduckgo.com",
        "  4: [url] https://www.google.com",
        "Entry to open [Type 'help' for more info]: ",
    ]
    for line, truth in zip_longest(sys.stdout.getvalue().split('\n'), expected):
        assert line == truth
    # clean up
    sys.stdout = original_stdout
    sys.stdin = original_stdin


def test_add():
    """Test add command."""
    # use temporary config
    tmp_config = "[DATABASE]\nfile=/tmp/cobib_test_database.yaml\n"
    with open('/tmp/cobib_test_config.ini', 'w') as file:
        file.write(tmp_config)
    CONFIG.set_config(Path('/tmp/cobib_test_config.ini'))
    # ensure database file exists and is empty
    open('/tmp/cobib_test_database.yaml', 'w').close()
    # freshly read in database to overwrite anything that was read in during setup()
    read_database(fresh=True)
    # add some data
    commands.AddCommand().execute(['-b', './test/example_literature.bib'])
    # compare with reference file
    with open('/tmp/cobib_test_database.yaml', 'r') as file:
        with open('./test/example_literature.yaml', 'r') as expected:
            for line, truth in zip_longest(file, expected):
                assert line == truth
    # clean up file system
    os.remove('/tmp/cobib_test_database.yaml')
    os.remove('/tmp/cobib_test_config.ini')


def test_add_overwrite_label():
    """Test add command while specifying a label manually.

    Regression test against #4.
    """
    # use temporary config
    tmp_config = "[DATABASE]\nfile=/tmp/cobib_test_database.yaml\n"
    with open('/tmp/cobib_test_config.ini', 'w') as file:
        file.write(tmp_config)
    CONFIG.set_config(Path('/tmp/cobib_test_config.ini'))
    # ensure database file exists and is empty
    open('/tmp/cobib_test_database.yaml', 'w').close()
    # freshly read in database to overwrite anything that was read in during setup()
    read_database(fresh=True)
    # add some data
    commands.AddCommand().execute(['-b', './test/example_literature.bib'])
    # add potentially duplicate entry
    commands.AddCommand().execute(['-b', './test/example_duplicate_entry.bib',
                                   '--label', 'duplicate_resolver'])
    # compare with reference file
    with open('./test/example_literature.yaml', 'r') as expected:
        true_lines = expected.readlines()
    with open('./test/example_duplicate_entry.yaml', 'r') as extra:
        true_lines += extra.readlines()
    with open('/tmp/cobib_test_database.yaml', 'r') as file:
        for line, truth in zip_longest(file, true_lines):
            assert line == truth
    # clean up file system
    os.remove('/tmp/cobib_test_database.yaml')
    os.remove('/tmp/cobib_test_config.ini')


@pytest.mark.parametrize(['labels'], [
        ['knuthwebsite'],
        [['knuthwebsite', 'latexcompanion']],
    ])
def test_delete(labels):
    """Test delete command."""
    # use temporary config
    tmp_config = "[DATABASE]\nfile=/tmp/cobib_test_database.yaml\n"
    with open('/tmp/cobib_test_config.ini', 'w') as file:
        file.write(tmp_config)
    CONFIG.set_config(Path('/tmp/cobib_test_config.ini'))
    # copy example database to configured location
    copyfile(Path('./test/example_literature.yaml'), Path('/tmp/cobib_test_database.yaml'))
    # delete some data
    # NOTE: for testing simplicity we delete the last entry
    commands.DeleteCommand().execute(labels)
    with open('/tmp/cobib_test_database.yaml', 'r') as file:
        with open('./test/example_literature.yaml', 'r') as expected:
            # NOTE: do NOT use zip_longest to omit last entry (thus, we deleted the last one)
            for line, truth in zip(file, expected):
                assert line == truth
            with pytest.raises(StopIteration):
                file.__next__()
    # clean up file system
    os.remove('/tmp/cobib_test_database.yaml')
    os.remove('/tmp/cobib_test_config.ini')


def test_edit():
    """Test edit command."""
    pytest.skip("There is currently no meaningful way of testing this.")


def test_export(setup):
    """Test export command.

    Args:
        setup: runs pytest fixture.
    """
    commands.ExportCommand().execute(['-b', '/tmp/cobib_test_export.bib'])
    with open('/tmp/cobib_test_export.bib', 'r') as file:
        with open('./test/example_literature.bib', 'r') as expected:
            for line, truth in zip_longest(file, expected):
                if truth[0] == '%':
                    # ignore comments
                    continue
                assert line == truth
    # clean up file system
    os.remove('/tmp/cobib_test_export.bib')


def test_export_selection(setup):
    """Test the `selection` interface of the export command.

    Args:
        setup: runs pytest fixture.
    """
    commands.ExportCommand().execute(['-b', '/tmp/cobib_test_export_s.bib', '-s', '--', 'einstein'])
    with open('/tmp/cobib_test_export_s.bib', 'r') as file:
        with open('./test/example_literature.bib', 'r') as expected:
            for line, truth in zip_longest(file, expected):
                print(line, truth)
                if truth[0] == '%':
                    # ignore comments
                    continue
                if truth.strip() == '@book{latexcompanion,':
                    # reached next entry
                    break
                assert line == truth
    # clean up file system
    os.remove('/tmp/cobib_test_export_s.bib')


@pytest.mark.parametrize(['args', 'expected', 'config_overwrite'], [
        [['einstein'], ['einstein - 1 match', '@article{einstein,', 'author = {Albert Einstein},'],
         'False'],
        [['einstein', '-i'], [
            'einstein - 2 matches', '@article{einstein,', 'author = {Albert Einstein},',
            'doi = {http://dx.doi.org/10.1002/andp.19053221004},'
        ], 'False'],
        [['einstein', '-i', '-c', '0'], [
            'einstein - 2 matches', '@article{einstein,', 'author = {Albert Einstein},'
        ], 'False'],
        [['einstein', '-i', '-c', '2'], [
            'einstein - 2 matches', '@article{einstein,', 'author = {Albert Einstein},',
            'doi = {http://dx.doi.org/10.1002/andp.19053221004},', 'journal = {Annalen der Physik},'
        ], 'False'],
        [['einstein'], [
            'einstein - 2 matches', '@article{einstein,', 'author = {Albert Einstein},',
            'doi = {http://dx.doi.org/10.1002/andp.19053221004},'
        ], 'True'],
        [['einstein', '-i'], [
            'einstein - 2 matches', '@article{einstein,', 'author = {Albert Einstein},',
            'doi = {http://dx.doi.org/10.1002/andp.19053221004},'
        ], 'True'],
    ])
def test_search(setup, args, expected, config_overwrite):
    """Test search command.

    Args:
        setup: runs pytest fixture.
        args: arguments for the list command call.
        expected: expected result.
        config_overwrite: with what to overwrite the DATABASE/ignore_search_case config option.
    """
    CONFIG.config['DATABASE']['search_ignore_case'] = config_overwrite
    file = StringIO()
    commands.SearchCommand().execute(args, out=file)
    for line, exp in zip_longest(file.getvalue().split('\n'), expected):
        line = line.replace('\x1b', '')
        line = re.sub(r'\[[0-9;]+m', '', line)
        if exp:
            assert exp in line
        if line and not (line.endswith('match') or line.endswith('matches')):
            assert re.match(r'\[[0-9]+\]', line)
