import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel
import PyQt5.QtWidgets as QtWidgets
from registry_manager import RegistryManager

APP_TITLE = "C&C Online Path Fixer"
WINDOW_SIZE = (500, 200)

class Example(QWidget):

  def __init__(self, window_size):
    super().__init__()
    self.window_width, self.window_height = window_size
    self.registry_manager_instance = RegistryManager()
    try:
      assert self.registry_manager_instance.exists()
    except AssertionError:
      raise Exception("Zero Hour registry key not found.")
    self.initUI()

  def initUI(self):
    self.resize(self.window_width, self.window_height)
    self.setWindowTitle(APP_TITLE)

    vbox = QVBoxLayout()
    
    self.browse_button = QPushButton("Browse")
    self.browse_button.pressed.connect(self.browseButtonClicked)
    self.directory_lineedit = QLineEdit()
    hbox_directory = QHBoxLayout()
    hbox_directory.addWidget(self.directory_lineedit)
    hbox_directory.addWidget(self.browse_button)
    vbox.addLayout(hbox_directory)

    hbox_installpath = QHBoxLayout()
    self.current_install_path = self.registry_manager_instance.getInstallPath()
    self.current_installpath_label = QLabel("Current InstallPath: ")
    self.current_installpath_value_lineedit = QLineEdit()
    #self.current_installpath_value_lineedit.setReadOnly(True)
    self.current_installpath_value_lineedit.setEnabled(False)
    self.__set_installpath_value()
    hbox_installpath.addWidget(self.current_installpath_label)
    hbox_installpath.addWidget(self.current_installpath_value_lineedit)
    self.copy_button = QPushButton("Copy")
    self.copy_button.pressed.connect(self.copyButtonClicked)
    hbox_installpath.addWidget(self.copy_button)
    vbox.addLayout(hbox_installpath)

    hbox_change = QHBoxLayout()
    self.change_button = QPushButton("Change")
    self.change_button.pressed.connect(self.changeButtonClicked)
    hbox_change.addStretch(1)
    hbox_change.addWidget(self.change_button)
    vbox.addLayout(hbox_change)

    self.setLayout(vbox)
    qr = self.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
    self.show()
    
  def __set_installpath_value(self):
    if self.current_install_path is None:
      current_installpath_value = "{not found}"
    else:
      if self.current_install_path == "":
        current_installpath_value = "{empty}"
      else:
        current_installpath_value = self.current_install_path
    self.current_installpath_value_lineedit.setText(current_installpath_value)
  
  def browseButtonClicked(self):
    zero_hour_directory = QFileDialog.getExistingDirectory(self, 'Locate Zero Hour Directory')
    zero_hour_directory_slashes = zero_hour_directory.replace('/', '\\')
    self.directory_lineedit.setText(zero_hour_directory_slashes)

  def copyButtonClicked(self):
    QApplication.clipboard().setText(self.current_install_path)

  def changeButtonClicked(self):
    directory = self.directory_lineedit.text()
    self.registry_manager_instance.setInstallPath(directory)
    try:
      self.current_install_path = self.registry_manager_instance.getInstallPath()
      assert self.current_install_path == directory
      self.__set_installpath_value()
    except AssertionError:
      print("Failure - InstallPath = {}, Directory = {}".format(self.current_install_path, directory))

  #def exitButtonClicked(self):
    #QCoreApplication.quit()
    

# start up application
app = QApplication(sys.argv)
ex = Example(WINDOW_SIZE)
sys.exit(app.exec_())