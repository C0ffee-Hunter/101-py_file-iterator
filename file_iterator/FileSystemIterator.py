import os


class FileSystemIterator:
    def __init__(self, root, only_files=False, only_dirs=False, pattern=None):
        """
        [#LEARNING_CENTER-101] Разработка класса-итератора по файловой системе на Python http://jira.nicetu.spb.ru/jira/si/jira.issueviews:issue-html/LEARNING_CENTER-101/LEAR...
        Стр. 1 из 4 13.02.2023, 11:00
         Инициализация объекта
         :param root: корневой каталог
         :param only_files: итерироваться только по файлам
         :param only_dirs: итерироваться только по директориям
         :param pattern: итерироваться только по объектам файловой системы, содержащим в имени строку pattern
         """
        if only_files and only_dirs:
            raise ValueError('Must be either only_files, or only_directories, or both must be False')

        if not os.path.isdir(root):
            raise FileNotFoundError('The directory doesn\'t exist')
        self.root = root
        self.only_files = only_files
        self.only_dirs = only_dirs
        self.pattern = pattern
        self.generator = self.get_generator()

    def __iter__(self):
        return self

    def match(self, root, dirs, files):
        for item in dirs + files:
            if (self.only_files and item in dirs) or (self.only_dirs and item in files):
                continue

            if self.pattern is not None:
                # without register
                if item.lower().find(self.pattern.lower()) != -1:
                    yield os.path.join(root, item).replace('\\', '/')
            else:
                yield os.path.join(root, item).replace('\\', '/')

    def get_generator(self):
        for root, dirs, files in os.walk(self.root):
            yield from self.match(root, dirs, files)

    def __next__(self):
        return next(self.generator)
