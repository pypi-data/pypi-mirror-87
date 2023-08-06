import sys
import os
import inspect


def addTihsDir(depth=1):
    aframe = sys._getframe(depth)
    af_code = aframe.f_code
    pyFilePath = af_code.co_filename
    adir = os.path.dirname(pyFilePath)
    if adir not in sys.path:
        sys.path.append(adir)


def doNothing():
    return


def addTihsDirEx(modDepth=1):
    count = 0
    stacks = inspect.stack()
    find = False
    for bframe in stacks:
        if bframe.function == '<module>':
            count += 1
            if count == modDepth:
                find = True
                break
    if find is False:
        print('sysPathThisDir addTihsDirEx fail')
        return
    # af_code = bframe.f_code
    pyFilePath = bframe.filename
    adir = os.path.dirname(pyFilePath)
    if adir not in sys.path:
        sys.path.append(adir)
