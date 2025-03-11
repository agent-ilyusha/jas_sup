# -- coding: utf-8
import os
from os import path


def __recursion_file(folder, text):
    try:
        for el in os.walk(folder):
            for file in el:
                if file == list():
                    pass
                elif path.isdir(folder+file[0]):
                    __recursion_file(folder, text)
                elif text+'.lnk' in file or el == text+'.lnk':
                    os.startfile(path.join(folder+'\\'+text+'.lnk'))
                    return 1
                elif el == text+'.exe' or text+'.exe' in file:
                    os.startfile(path.join(folder + '\\' + text + '.exe'))
                    return 1
                elif el == text+'.url' or text+'.url' in file:
                    os.startfile(path.join(folder + '\\' + text + '.url'))
                    return 1
    except PermissionError:
        __recursion_file(folder, text)



def func_cycle(txt):
    path_files = path.join('C:\\Users\\1\\Desktop\\')
    list_path = (os.listdir(path_files))
    for el in list_path:
        varib = path.join(path.join('C:\\Users\\1\\Desktop\\'+el))
        if path.isdir(varib):
            file_my = __recursion_file(varib, txt)
            if file_my == 1:
                break
        elif txt + '.lnk' == el:
            os.startfile(path.join(path_files + '\\' + el))
            break
        elif txt + '.url' == el:
            os.startfile(path.join(path_files + '\\' + el))
            break
        elif txt + '.exe' == el:
            os.startfile(path.join(path_files + '\\' + el))
            break
    else:
        return 'Не смогла найти файл'
    return 'Запустила файл'
