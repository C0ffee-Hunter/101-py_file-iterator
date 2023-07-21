from file_iterator import FileSystemIterator as FSI

# __iter__ method is called once

for item in FSI.FileSystemIterator('..', only_files=False, only_dirs=False, pattern='resolve'):
    print(item)

#
print("################################")
# __next__ method is called every time
try:
    iterator = FSI.FileSystemIterator("..", False, True, pattern="ref")
    for i in range(100):
        print(next(iterator))

except StopIteration:
    print('Tree is over')

