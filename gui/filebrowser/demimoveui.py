"""demimove-ui

Usage:
    dmv-ui [-d <path>] [-c <file>] [-v|-vv|-vvv] [-q] [-h]

Options:
    -c, --config=<file>  <NYI> Specify a config file to load.
    -d, --dir=<path>     Specify the working directory. Otherwise CWD is used.
    -v                   Logging verbosity level, up to -vvv.
    -q, --quiet          Do not print logging messages to console.
    -h,  --help          Show this help text and exit.
    --version            Show the current demimove-ui version.
"""
# TODO: ConfigParser
import logging
import sys

from PyQt4 import QtGui, QtCore, uic

from fileops import FileOps


log = logging.getLogger("gui")

try:
    from docopt import docopt
except ImportError:
    print "ImportError: Please install docopt to use the CLI."


class PreviewFileModel(QtGui.QFileSystemModel):

    autopreview = False

    def columnCount(self, parent=QtCore.QModelIndex()):
        return super(PreviewFileModel, self).columnCount() + 1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                return self.get_preview_text()
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignHCenter

        return super(PreviewFileModel, self).data(index, role)

    def get_preview_text(self, *args):
        return self.get_file_list()

    def get_file_list(self):
        return QtCore.QString("Preview here")

    def get_dir_list(self):
        pass


class DemiMoveGUI(QtGui.QMainWindow):

    def __init__(self, fileops, parent=None):

        super(DemiMoveGUI, self).__init__(parent)
        self._autopreview = True
        self.fileops = fileops
        uic.loadUi("demimove.ui", self)

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.mainsplitter.setStretchFactor(0, 2)
        self.mainsplitter.setStretchFactor(1, 3)

        self.create_dirtree()
        self.create_browsertree()
        self.connect_buttons()
        log.info("demimove-ui initialized.")

    @property
    def autopreview(self):
        return self._autopreview

    @autopreview.setter
    def autopreview(self, boolean):
        log.debug("Setting autopreview to {}.".format(boolean))
        self._autopreview = boolean

    def on_previewbutton(self):
        log.debug("{}".format(self.sender()))
#         srcpat, destpat, path = None, None, None
#         self.fileops.stage(srcpat, destpat, path)

    def on_commitbutton(self):
        pass
        # self.fileops.commit()

    def on_undobutton(self):
        pass
        # self.fileops.undo()

    def on_regexcheck(self, checked):
        if checked:
            self.fileops.regex = True
        else:
            self.fileops.regex = False

    def on_autopreviewcheck(self, checked):
        if checked:
            self.autopreview = True
        else:
            self.autopreview = False

    def on_extensioncheck(self, checked):
        if checked:
            self.fileops.keepext = True
        else:
            self.fileops.keepext = False

    def on_hiddencheck(self, checked):
        if checked:
            self.fileops.hidden = True
        else:
            self.fileops.hidden = False

    def on_mirrorcheck(self, checked):
        if checked:
            self.fileops.mirror = True
        else:
            self.fileops.mirror = False

    def on_recursivecheck(self, checked):
        if checked:
            self.fileops.recursive = True
        else:
            self.fileops.recursive = False

    def on_autostopcheck(self, checked):
        if checked:
            self.fileops.autostop = True
        else:
            self.fileops.autostop = False

    def insertpos(self, value):
        pass

    def insertedit(self, text):
        pass

    def on_replacecase(self):
        pass

    def on_replaceglob(self):
        pass

    def on_replaceregex(self):
        pass

    def on_insertpos(self):
        pass

    def on_insertedit(self):
        pass

    def on_countstart(self):
        pass

    def on_countstep(self):
        pass

    def on_countpreedit(self):
        pass

    def on_countsufedit(self):
        pass

    def on_countfillcheck(self, checked):
        if checked:
            self.fileops.countfill = True
        else:
            self.fileops.countfill = False

    def on_removeduplicates(self, checked):
        if checked:
            self.fileops.duplicates = True
        else:
            self.fileops.duplicates = False

    def on_removeextensions(self, checked):
        if checked:
            self.fileops.ext = True
        else:
            self.fileops.ext = False

    def on_removenonwords(self, checked):
        if checked:
            self.fileops.nonwords = True
        else:
            self.fileops.nonwords = False

    def on_varaccents(self, checked):
        if checked:
            self.fileops.accents = True
        else:
            self.fileops.accents = False

    def on_allradio(self, checked):
        if checked:
            self.fileops.filesonly = False
            self.fileops.dirsonly = False

    def on_dirsradio(self, checked):
        if checked:
            self.fileops.dirsonly = True
            self.fileops.filesonly = False
        else:
            self.fileops.dirsonly = False

    def on_filesradio(self, checked):
        if checked:
            self.fileops.filesonly = True
            self.fileops.dirsonly = False
        else:
            self.fileops.filessonly = False

    def connect_buttons(self):
        # Main buttons:
        self.previewbutton.clicked.connect(self.on_previewbutton)
        self.commitbutton.clicked.connect(self.on_commitbutton)
        self.undobutton.clicked.connect(self.on_undobutton)
        # Main check and lineedits:
        self.regexcheck.clicked.connect(self.on_regexcheck)
        self.allradio.clicked.connect(self.on_allradio)
        self.dirsradio.clicked.connect(self.on_dirsradio)
        self.filesradio.clicked.connect(self.on_filesradio)

        # Main options:
        self.autopreviewcheck.clicked.connect(self.on_autopreviewcheck)
        self.autostopcheck.clicked.connect(self.on_autostopcheck)
        self.extensioncheck.clicked.connect(self.on_extensioncheck)
        self.hiddencheck.clicked.connect(self.on_hiddencheck)
        self.mirrorcheck.clicked.connect(self.on_mirrorcheck)
        self.recursivecheck.clicked.connect(self.on_recursivecheck)

        # Replace options:
        self.replacecase.clicked.connect(self.on_replacecase)
        self.replaceglob.clicked.connect(self.on_replaceglob)
        self.replaceregex.clicked.connect(self.on_replaceregex)

        # Insert options:
        self.insertpos.valueChanged.connect(self.on_insertpos)
        self.insertedit.textChanged.connect(self.on_insertedit)

        # Count options:
        self.countstart.valueChanged.connect(self.on_countstart)
        self.countstep.valueChanged.connect(self.on_countstep)
        self.countpreedit.textChanged.connect(self.on_countpreedit)
        self.countsufedit.textChanged.connect(self.on_countsufedit)
        self.countfillcheck.clicked.connect(self.on_countfillcheck)

        # Remove options:
        self.removeduplicatescheck.clicked.connect(self.on_removeduplicates)
        self.removeextensionscheck.clicked.connect(self.on_removeextensions)
        self.removenonwordscheck.clicked.connect(self.on_removenonwords)

        # Various options:
        self.varaccentscheck.clicked.connect(self.on_varaccents)

    def create_dirtree(self):
        # Passing self as arg/parent here to avoid QTimer errors.
        self.dirmodel = QtGui.QFileSystemModel(self)
        self.dirmodel.setRootPath("")
        self.dirmodel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Hidden |
                                QtCore.QDir.NoDotAndDotDot)
        self.dirmodel.fileRenamed.connect(self.on_rootchange)
        self.dirmodel.rootPathChanged.connect(self.on_rootchange)
        self.dirmodel.directoryLoaded.connect(self.on_rootchange)

        self.dirtree.setModel(self.dirmodel)
        self.dirtree.setColumnHidden(1, True)
        self.dirtree.setColumnHidden(2, True)
        self.dirtree.setColumnHidden(3, True)

    def create_browsertree(self):
        self.browsermodel = PreviewFileModel(self)
        self.browsermodel.setRootPath("")
        self.browsermodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                                    QtCore.QDir.NoDotAndDotDot |
                                    QtCore.QDir.Hidden)

        self.browsertree.setModel(self.browsermodel)
        self.browsertree.header().swapSections(4, 1)
        self.browsertree.setColumnHidden(2, True)

    def on_rootchange(self, *args):
#         print self.dirmodel.filePath(self.dirtree.currentIndex())
        path = self.dirmodel.filePath(self.dirtree.currentIndex())
#         print self.browsertree.selectionModel()
#         model = self.browsertree.model()
#         idx = model.index(model.rootPath())
#         for i in range(0, model.rowCount(idx)):
#             child = idx.child(i, idx.column())
#             print model.fileName(child)
#         print self.dirtree.currentIndex()
        print path
#         self.browsermodel.setRootPath(path)
#         self.browsertree.setRootIndex(self.dirtree.currentIndex())
#         self.browsertree.setRootIndex(self.dirmodel.index(path))

def main():
    "Main entry point for demimove."
    try:
        args = docopt(__doc__, version="0.1")
        args["-v"] = 3
        fileops = FileOps(verbosity=args["-v"], quiet=args["--quiet"])
    except NameError:
        fileops = fileops.FileOps()
        log.error("Please install docopt to use the CLI.")
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("demimove")
#     app.setStyle("plastique")
    gui = DemiMoveGUI(fileops)
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
