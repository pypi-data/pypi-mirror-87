"""WFunction class."""
from PyQt5 import QtWidgets, QtCore, QtGui

from cryspy_editor.widgets.w_presentation import pass_func, run_function


class WBaseObj(QtWidgets.QGroupBox):
    """
    WBaseObj class.

    Attributes
    ----------
        - thread
    Mehtods
    -------
        - set_object
    """

    def __init__(self, parent=None):
        super(WBaseObj, self).__init__(parent)
        self.thread = None
        layout_central = QtWidgets.QVBoxLayout(self)
        # self.setWidgetResizable(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding))

        # self.wdoc = QtWidgets.QLabel(self)
        # self.wdoc.setSizePolicy(
        #     QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
        #                           QtWidgets.QSizePolicy.Expanding))

        self.wlabel = QtWidgets.QTextEdit(self)
        self.wlabel.setAcceptRichText(True)
        self.wlabel.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding))
        self.wlabel.setFont(QtGui.QFont("Courier", 8, QtGui.QFont.Normal))
        # self.wlabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.wlabel.setAlignment(QtCore.Qt.AlignTop)
        # self.wlabel.setWordWrap(True)
        self.wlabel.setStyleSheet("background-color:white;")

        # layout_central.addWidget(self.wdoc,3)
        layout_central.addWidget(self.wlabel)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Write to the object")
        pb.clicked.connect(self.write_to_object)
        layout_central.addWidget(pb)

        self.setLayout(layout_central)
        # self.setWidget(self.wlabel)

    def set_thread(self, thread: QtCore.QThread):
        """Set thread."""
        self.thread = thread

    def setText(self, text: str):
        """Set text."""
        self.wlabel.setText(text)

    def write_to_object(self):
        """Write to object."""
        if self.object is None:
            return
        stext = self.wlabel.toPlainText()
        obj2 = self.object.from_cif(stext)
        if obj2 is not None:
            self.object.copy_from(obj2)
        run_function(pass_func, (), self.thread)

    def set_object(self, obj):
        """Set text."""
        if obj is None:
            return
        self.object = obj
        self.wlabel.setText(obj.__repr__())
        self.wlabel.setToolTip(obj.__doc__)
        # self.wlabel.setHtml(obj._repr_html_())
