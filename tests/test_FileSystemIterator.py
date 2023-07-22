from file_iterator.FileSystemIterator import FileSystemIterator

import unittest
from pathlib import Path
import os
import shutil

class TestFileIterator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.empty = Path('./empty')
        os.makedirs(cls.empty, exist_ok=True)

        cls.root = Path('./root')
        cls.dirs = list(map(Path, [
            './root/subdir1',
            './root/subdir1/subsubdir1',
            './root/subdir1/subsubdir2',
            './root/subdir1/subsubdir2/subsubsubdir1',
            './root/subdir1/subsubdir3',
            './root/subdir2',
            './root/subdir2/subsubtxtdir4',
            './root/subdir2/subsubdir5',
            './root/subtxtdir3',
            './root/subdir4',
            './root/subdir5',
            './root/subdir5/subsubdir6',
        ]))

        cls.files = list(map(Path, [
            './root/file1.txt',
            './root/file2.txt',
            './root/subdir1/file3.jpg',
            './root/subdir1/subsubdir1/file4.txt',
            './root/subdir1/subsubdir1/file5.docx',
            './root/subdir1/subsubdir1/file6',
            './root/subdir1/subsubdir3/file7.txt',
            './root/subdir1/subsubdir3/file8.doc',
            './root/subdir2/subsubtxtdir4/file9.txt',
            './root/subdir2/subsubtxtdir4/file10.py',
            './root/subdir2/subsubdir5/file11.c',
            './root/subtxtdir3/file12.cpp',
            './root/subtxtdir3/file13.txt',
            './root/subtxtdir3/subfile14.txt',
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
        # проверить ещё раз этот тест и идти дальше
        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, False, 'txt')],
            [Path(item).parts for item in self.dirs if 'txt' in str(item)] + \
            [Path(item).parts for item in self.files if '.txt' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, True, False, 'txt')],
            [Path(item).parts for item in self.files if '.txt' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, True, False, 'c')],
            [Path(item).parts for item in self.files if 'c' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, True, 'txt')],
            [Path(item).parts for item in self.dirs if 'txt' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, True, 'sub')],
            [Path(item).parts for item in self.dirs if 'sub' in str(item)]
        )

        self.assertCountEqual(
            [Path(item).parts for item in FileSystemIterator(self.root, False, True, 'subsub')],
            [Path(item).parts for item in self.dirs if 'subsub' in str(item)]
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
            [item for item in FileSystemIterator(self.empty, False, False, None)],
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
        lst = [item for item in self.dirs if 'txt' in item] + \
              [item for item in self.files if '.txt' in item]
        [next(iterator) for _ in range(len(lst))]
        self.assertRaises(StopIteration, next, iterator)

    def test_nextNonexistentRoot(self):
        with self.assertRaises(FileNotFoundError):
            next(FileSystemIterator('None', False, False, None))

    def test_nextEmptyRoot(self):
        self.assertRaises(StopIteration, next, FileSystemIterator(self.empty, False, False, None))

    def test_iterReturnSelf(self):
        self.assertIsInstance(iter(FileSystemIterator(self.empty, False, False, None)), FileSystemIterator)
