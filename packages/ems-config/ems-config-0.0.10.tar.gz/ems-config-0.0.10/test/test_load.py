import unittest
import tempfile
import os
from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
from shutil import copyfile
from unittest import mock

from ems_config import parse_config

res_path = Path(os.path.dirname(os.path.realpath(__file__))) / "res"


@contextmanager
def working_dir(w_dir=None):
    _original_dir = os.getcwd()
    temp_dir = None
    if w_dir is None:
        temp_dir = tempfile.TemporaryDirectory()
        w_dir = temp_dir.name

    os.chdir(w_dir)
    yield Path(w_dir)
    os.chdir(_original_dir)

    if temp_dir:
        temp_dir.cleanup()


class TestLoading(unittest.TestCase):

    def test_sanity(self):
        self.assertTrue(True)

    def test_load_ini(self):
        filename = "config.ini"
        with working_dir() as path:
            copyfile(res_path / filename, path / filename)

            c = parse_config()
            self.assertTrue(isinstance(c, ConfigParser))

            self.assertEqual(c["DEFAULT"]["field"], "value")

    def test_load_json(self):
        filename = "config.yml"
        with working_dir() as path:
            copyfile(res_path / filename, path / filename)

            c = parse_config(filename)
            self.assertTrue(isinstance(c, dict))

            self.assertEqual(c["field"], "value")

    def test_load_yaml(self):
        filename = "config.yml"
        with working_dir() as path:
            copyfile(res_path / filename, path / filename)

            c = parse_config(filename)
            self.assertTrue(isinstance(c, dict))

            self.assertEqual(c["field"], "value")

    @mock.patch.dict(os.environ, {"CONFIG_PATH": "config.ini"})
    def test_copy_if_not_exists(self):
        filename = "config.ini"
        with working_dir():
            self.assertEqual(len(os.listdir()), 0)
            parse_config(str(res_path / filename))
            self.assertTrue(filename in os.listdir())

    def test_raise_if_unknown_ext(self):
        filename = "config.unknown"
        with working_dir():
            self.assertRaises(ValueError, lambda: parse_config(res_path / filename))
