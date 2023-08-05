import shutil
from os.path import isdir, isfile, join
import os


def compare(object1, object2):
    return object1 == object2


def sort(path):
    for node in os.listdir(path):
        newPath = join(path, node)
        first_char = '#' if node[0].isnumeric() else node[0].upper()
        posible_parent = join(path, first_char)
        posible_future = join(posible_parent, node)
        if(isdir(newPath) and not compare(node, 'Recovery') and not compare(node, 'System Volume Information') and not compare(node, '$RECYCLE.BIN')):
            # print(node,)

            if(len(node) > 1):

                if (not os.path.exists(posible_parent)):
                    os.mkdir(posible_parent)

                shutil.move(newPath, posible_future)

        elif(isfile(newPath)):
            posible_parent = join(path, first_char)
            if (not os.path.exists(posible_parent)):
                os.mkdir(posible_parent)

            shutil.move(newPath, posible_future)
