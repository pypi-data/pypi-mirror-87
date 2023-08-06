from unittest import TestCase
from k9.storage import *
from k9.core import abs_path
import subprocess

class TestStorage(TestCase):
    def test_create_storage_class(self):
        name = 'unit-storage-class'

        print("")
        print(create_storage_class(abs_path('../test/storage.yml')))

        self.assertTrue(storage_class_exists(name))

        delete_storage_class(name)

        self.assertFalse(storage_class_exists(name))

    def test_create_storage_class_fail(self):
        with self.assertRaisesRegex(subprocess.CalledProcessError, 'returned non-zero exit status 1.'):
            create_storage_class('bogus')

    def test_delete_storage_class_fail(self):
        with self.assertRaisesRegex(subprocess.CalledProcessError, 'returned non-zero exit status 1.'):
            delete_storage_class('bogus')
