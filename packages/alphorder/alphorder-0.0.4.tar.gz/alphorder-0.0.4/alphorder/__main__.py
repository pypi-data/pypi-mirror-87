import os
import sys

from alphorder.sorter import sort


def main():
    if (len(sys.argv) > 1):
        path = sys.argv[1]
        # print(path)
        if (os.path.isdir(path)):
            sort(sys.argv[1])
        else:
            print('You have no specified a valid route')
    else:
        print('Path has not been specified: ',
              'python locator.py path/to/folder')


if (__name__ == '__main__'):
    main()
