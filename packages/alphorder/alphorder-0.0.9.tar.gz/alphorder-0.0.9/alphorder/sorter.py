import shutil
from os.path import isdir, isfile, join
import os


def compare(object1, object2):
    return object1 == object2


class Alphorder:

    @staticmethod
    def sort(path):
        for node in os.listdir(path):
            newPath = join(path, node)
            first_char = '#' if node[0].isnumeric() else node[0].upper()
            posible_parent = join(path, first_char)
            posible_future = join(posible_parent, node)
            if(isdir(newPath) and not compare(node, 'Recovery') and not compare(node, 'System Volume Information') and not compare(node, '$RECYCLE.BIN')):

                if(len(node) > 1):

                    if (not os.path.exists(posible_parent)):
                        os.mkdir(posible_parent)

                    shutil.move(newPath, posible_future)

            elif(isfile(newPath)):
                posible_parent = join(path, first_char)
                if (not os.path.exists(posible_parent)):
                    os.mkdir(posible_parent)

                shutil.move(newPath, posible_future)

    @staticmethod
    def moveToFolder(path, foldername):
        folderToMove = foldername if isdir(
            foldername) else join(path, foldername)

        if (not os.path.exists(folderToMove)):
            os.mkdir(folderToMove)

        for node in os.listdir(path):
            currentPath = join(path, node)
            if(isdir(currentPath) and not compare(node, 'Recovery') and not compare(node, 'System Volume Information') and not compare(node, '$RECYCLE.BIN')):
                if not currentPath == folderToMove:
                    shutil.move(currentPath, folderToMove)

            elif(isfile(currentPath)):
                shutil.move(currentPath, folderToMove)

    @staticmethod
    def moveToFolderByKeywords(path, foldername, keywords):
        folderToMove = foldername if isdir(
            foldername) else join(path, foldername)

        if (not os.path.exists(folderToMove)):
            os.mkdir(folderToMove)

        for node in os.listdir(path):
            currentPath = join(path, node)
            if(isdir(currentPath) and not compare(node, 'Recovery') and not compare(node, 'System Volume Information') and not compare(node, '$RECYCLE.BIN')):
                for word in keywords:
                    if word.lower() in node.lower():
                        if not currentPath == folderToMove:
                            shutil.move(currentPath, folderToMove)
                            break

            elif(isfile(currentPath)):
                for word in keywords:
                    if word in node:
                        shutil.move(currentPath, join(folderToMove, node))
