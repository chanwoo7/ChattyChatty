import sys
from PyQt5.QtWidgets import QApplication, QDialog
import ui_server


class ServerDialog(QDialog, ui_server.Ui_server_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = ServerDialog()
    myWindow.show()
    app.exec_()