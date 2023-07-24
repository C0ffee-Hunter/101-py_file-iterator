from file_iterator.FileSystemIterator import FileSystemIterator

import unittest
from pathlib import Path
import os
import shutil


class TestFileIterator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.empty = Path('./tests/empty')
        os.makedirs(cls.empty, exist_ok=True)

        cls.root = Path('./tests/root')
        cls.dirs = list(map(Path, [
            './tests/root/subdir1',
            './tests/root/subdir1/subsubdir1',
            './tests/root/subdir1/subsubdir2',
            './tests/root/subdir1/subsubdir2/subsubsubdir1',
            './tests/root/subdir1/subsubdir3',
            './tests/root/subdir2',
            './tests/root/subdir2/subsubtxtdir4',
            './tests/root/subdir2/subsubdir5',
            './tests/root/subtxtdir3',
            './tests/root/subdir4',
            './tests/root/subdir5',
            './tests/root/subdir5/subsubdir6',
        ]))

        cls.files = list(map(Path, [
            './tests/root/file1.txt',
            './tests/root/file2.txt',
            './tests/root/subdir1/file3.jpg',
            './tests/root/subdir1/subsubdir1/file4.txt',
            './tests/root/subdir1/subsubdir1/file5.docx',
            './tests/root/subdir1/subsubdir1/file6',
            './tests/root/subdir1/subsubdir3/file7.txt',
            './tests/root/subdir1/subsubdir3/file8.doc',
            './tests/root/subdir2/subsubtxtdir4/file9.txt',
            './tests/root/subdir2/subsubtxtdir4/file10.py',
            './tests/root/subdir2/subsubdir5/file11.c',
            './tests/root/subtxtdir3/file12.cpp',
            './tests/root/subtxtdir3/file13.txt',
            './tests/root/subtxtdir3/subfile14.txt',
        ]))

        for dir in cls.dirs:
            os.makedirs(dir, exist_ok=True)

        for file in cls.files:
            open(file, 'w').close()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.empty)
        shutil.rmtree(cls.root)

    def test_default(self):
        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, False, None)],
            [item.parts for item in self.dirs + self.files]
        )

    def test_enableOnlyFiles(self):
        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, True, False, None)],
            [item.parts for item in self.files]
        )

    def test_enableOnlyDirs(self):
        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, True, None)],
            [item.parts for item in self.dirs]
        )

    def test_enableOnlyFilesAndOnlyDirs(self):
        with self.assertRaises(ValueError):
            for _ in FileSystemIterator(self.root, True, True, None):
                pass

    def test_pattern(self):
        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, False, 'txt')],
            [item.parts for item in self.dirs if 'txt' in str(item)] + \
            [item.parts for item in self.files if '.txt' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, True, False, 'txt')],
            [item.parts for item in self.files if '.txt' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, True, False, 'c')],
            [item.parts for item in self.files if 'c' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, True, 'txt')],
            [item.parts for item in self.dirs if 'txt' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, True, 'sub')],
            [item.parts for item in self.dirs if 'sub' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, True, 'subsub')],
            [item.parts for item in self.dirs if 'subsub' in str(item)]
        )

    def test_emptyFields(self):
        with self.assertRaises(TypeError):
            for _ in FileSystemIterator(None, None, None, None):
                pass

    def test_nonexistentRoot(self):
        with self.assertRaises(FileNotFoundError):
            FileSystemIterator('None', False, False, None)

    def test_emptyRoot(self):
        self.assertEqual(
            [Path(item).parts for item in FileSystemIterator(self.empty, False, False, None)],
            []
        )

    def test_nextOnlyFiles(self):
        iterator = FileSystemIterator(self.root, True, False, None)
        [next(iterator) for _ in range(len(self.files))]

        # Checking for a new circle
        self.assertRaises(StopIteration, next, iterator)  # New circle initialization needed, e.g. iter.refresh()

    def test_nextOnlyDirs(self):
        iterator = FileSystemIterator(self.root, False, True, None)
        [next(iterator) for _ in range(len(self.dirs))]
        self.assertRaises(StopIteration, next, iterator)

    def test_nextPattern(self):
        iterator = FileSystemIterator(self.root, False, False, 'txt')
        lst = [item.parts for item in self.dirs if 'txt' in str(item)] + \
              [item.parts for item in self.files if '.txt' in str(item)]
        [next(iterator) for _ in range(len(lst))]
        self.assertRaises(StopIteration, next, iterator)

    def test_nextNonexistentRoot(self):
        with self.assertRaises(FileNotFoundError):
            next(FileSystemIterator('None', False, False, None))

    def test_nextEmptyRoot(self):
        self.assertRaises(StopIteration, next, FileSystemIterator(self.empty, False, False, None))

    def test_iterReturnSelf(self):
        self.assertIsInstance(iter(FileSystemIterator(self.empty, False, False, None)), FileSystemIterator)
