import os


class FileSystemIterator:
    def __init__(self, root_path, only_files=False, only_dirts=False, pattern=None):
        self.root_path = root_path
        self.only_files = only_files
        self.only_dirts = only_dirts
        self.pattern = pattern
        self._iterator = self._create_iterator()

    def _create_iterator(self):
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            if not self.only_dirts:
                for filename in filenames:
                    if not self.pattern or self.pattern in filename:
                        yield os.path.join(dirpath, filename)
            if not self.only_files:
                for dirname in dirnames:
                    if not self.pattern or self.pattern in dirname:
                        yield os.path.join(dirpath, dirname)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterator)


for item in FileSystemIterator('/', False, False, None):
    print(item)

print('#########################################')

print(next(FileSystemIterator('/', False, False, None)))
