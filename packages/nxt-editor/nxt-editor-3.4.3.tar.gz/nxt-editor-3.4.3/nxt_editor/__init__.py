# Builtin
import os
import sys
import logging
import sys

# External
from Qt import QtCore, QtWidgets, QtGui

# Internal
import nxt

logger = logging.getLogger('nxt.nxt_editor')

LOGGER_NAME = logger.name


class DIRECTIONS:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class LoggingSignaler(QtCore.QObject):
    """Qt object used to emit logging messages. This object allows us to make
    thread safe visual loggers.
    """
    signal = QtCore.Signal(logging.LogRecord)


class StringSignaler(QtCore.QObject):
    """Qt object used to emit strings. This object allows us to use Qt
    signals in objects that themselves can't be a QObject.
    """
    signal = QtCore.Signal(str)


def make_resources(qrc_path=None, result_path=None):
    import PySide2
    pyside_dir = os.path.dirname(PySide2.__file__)
    full_rcc_path = os.path.join(pyside_dir, 'pyside2-rcc')
    this_dir = os.path.dirname(os.path.realpath(__file__))
    if not qrc_path:
        qrc_path = os.path.join(this_dir, 'resources/resources.qrc')
    if not result_path:
        result_path = os.path.join(this_dir, 'qresources.py')
    msg = 'First launch nxt resource generation from {} to {}'
    logger.info(msg.format(qrc_path, result_path))
    import subprocess
    ver = ['-py2']
    if sys.version_info[0] == 3:
        ver += ['-py3']
    args = [qrc_path] + ver + ['-o', result_path]
    try:
        subprocess.check_call(['pyside2-rcc'] + args)
    except:
        try:
            subprocess.check_call([full_rcc_path] + args)
        except:
            raise Exception("Cannot find pyside2-rcc to generate UI resources."
                            " Reinstalling pyside2 may fix the problem.")


try:
    from nxt_editor import qresources
except ImportError:
    make_resources()


def launch_editor(paths=None, start_rpc=True):
    """Creates a new QApplication with editor main window and shows it.
    """
    # Deferred import since main window relies on us
    from nxt_editor.main_window import MainWindow
    path = None
    if paths is not None:
        path = paths[0]
        paths.pop(0)
    else:
        paths = []
    app = QtWidgets.QApplication(sys.argv)
    app.setEffectEnabled(QtCore.Qt.UI_AnimateCombo, False)
    style_file = QtCore.QFile(':styles/styles/dark/dark.qss')
    style_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(style_file)
    app.setStyleSheet(stream.readAll())
    instance = MainWindow(filepath=path, start_rpc=start_rpc)
    for other_path in paths:
        instance.load_file(other_path)
    pixmap = QtGui.QPixmap(':icons/icons/nxt.svg')
    app.setWindowIcon(QtGui.QIcon(pixmap))
    app.setActiveWindow(instance)
    instance.show()
    return app.exec_()
