from file_iterator.FileSystemIterator import FileSystemIterator

import unittest

import os
import shutil

class TestFileIterator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty = './tests/empty'
        os.makedirs(cls.empty, exist_ok=True)

        cls.root = './tests/root'

        cls.dirs = [
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
        ]

        cls.files = [
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
        ]

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
            [item for item in FileSystemIterator(self.root, False, False, None)],
            self.dirs + self.files
        )
    
    def test_enableOnlyFiles(self):
        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, True, False, None)],
            self.files
        )
    
    def test_enableOnlyDirs(self):
        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, False, True, None)],
            self.dirs
        )
    
    def test_enableOnlyFilesAndOnlyDirs(self):
        try:
            self.assertEqual(
                [item for item in FileSystemIterator(self.root, True, True, None)],
                []
            )
        except Exception as e:
            self.assertIsInstance(e, StopIteration)

    def test_pattern(self):
        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, False, False, 'txt')],
            [item for item in self.dirs if 'txt' in item] + \
                [item for item in self.files if '.txt' in item]
        )

        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, True, False, 'txt')],
            [item for item in self.files if '.txt' in item]
        )

        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, True, False, 'c')],
            [item for item in self.files if 'c' in item]
        )

        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, False, True, 'txt')],
            [item for item in self.dirs if 'txt' in item]
        )

        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, False, True, 'sub')],
            [item for item in self.dirs if 'sub' in item]
        )

        self.assertCountEqual(
            [item for item in FileSystemIterator(self.root, False, True, 'subsub')],
            [item for item in self.dirs if 'subsub' in item]
        )

    def test_emptyFields(self):
        with self.assertRaises(TypeError):
            for item in FileSystemIterator(None, None, None, None):
                pass
    
    def test_nonexistentRoot(self):
        # Expect empty list or raise error
        try:
            self.assertEqual(
                [item for item in FileSystemIterator('None', False, False, None)],
                []
            )
        except Exception as e:
            self.assertIsInstance(e, FileNotFoundError)

    def test_emptyRoot(self):
        self.assertEqual(
            [item for item in FileSystemIterator(self.empty, False, False, None)],
            []
        )
    
    def test_nextOnlyFiles(self):
        iterator = FileSystemIterator(self.root, True, False, None)
        self.assertCountEqual(
            [next(iterator) for _ in range(len(self.files))],
            self.files
        )

        # Checking for a new circle
        self.assertRaises(StopIteration, next, iterator) # New circle initialization needed, e.g. iter.refresh()
    
    def test_nextOnlyDirs(self):
        iterator = FileSystemIterator(self.root, False, True, None)
        self.assertCountEqual(
            [next(iterator) for _ in range(len(self.dirs))],
            self.dirs
        )
        self.assertRaises(StopIteration, next, iterator)
    
    def test_nextPattern(self):
        iterator = FileSystemIterator(self.root, False, False, 'txt')
        lst = [item for item in self.dirs if 'txt' in item] + \
            [item for item in self.files if '.txt' in item]
        self.assertCountEqual(
            [next(iterator) for _ in range(len(lst))],
            lst
        )
        self.assertRaises(StopIteration, next, iterator)

    def test_nextNonexistentRoot(self):
        self.assertRaises(StopIteration, next, FileSystemIterator('None', False, False, None))
    
    def test_nextEmptyRoot(self):
        self.assertRaises(StopIteration, next, FileSystemIterator(self.empty, False, False, None))
