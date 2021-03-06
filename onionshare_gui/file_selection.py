# -*- coding: utf-8 -*-
"""
OnionShare | https://onionshare.org/

Copyright (C) 2017 Micah Lee <micah@micahflee.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from .alert import Alert

from onionshare import strings, common

class FileList(QtWidgets.QListWidget):
    """
    The list of files and folders in the GUI.
    """
    files_dropped = QtCore.pyqtSignal()
    files_updated = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(FileList, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setSortingEnabled(True)

        class DropHereLabel(QtWidgets.QLabel):
            """
            When there are no files or folders in the FileList yet, display the
            'drop files here' message and graphic.
            """
            def __init__(self, parent, image=False):
                self.parent = parent
                super(DropHereLabel, self).__init__(parent=parent)
                self.setAcceptDrops(True)
                self.setAlignment(QtCore.Qt.AlignCenter)

                if image:
                    self.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(common.get_resource_path('images/drop_files.png'))))
                else:
                    self.setText(strings._('gui_drag_and_drop', True))
                    self.setStyleSheet('color: #999999;')

                self.hide()

            def dragEnterEvent(self, event):
                self.parent.drop_here_image.hide()
                self.parent.drop_here_text.hide()
                event.ignore()

        self.drop_here_image = DropHereLabel(self, True)
        self.drop_here_text = DropHereLabel(self, False)

        self.filenames = []
        self.update()

    def update(self):
        """
        Update the GUI elements based on the current state.
        """
        # file list should have a background image if empty
        if len(self.filenames) == 0:
            self.drop_here_image.show()
            self.drop_here_text.show()
        else:
            self.drop_here_image.hide()
            self.drop_here_text.hide()

    def resizeEvent(self, event):
        """
        When the widget is resized, resize the drop files image and text.
        """
        self.drop_here_image.setGeometry(0, 0, self.width(), self.height())
        self.drop_here_text.setGeometry(0, 0, self.width(), self.height())

    def dragEnterEvent(self, event):
        """
        dragEnterEvent for dragging files and directories into the widget.
        """
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """
        dragLeaveEvent for dragging files and directories into the widget.
        """
        event.accept()
        self.update()

    def dragMoveEvent(self, event):
        """
        dragMoveEvent for dragging files and directories into the widget.
        """
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        dropEvent for dragging files and directories into the widget.
        """
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                filename = str(url.toLocalFile())
                self.add_file(filename)
        else:
            event.ignore()
        self.files_dropped.emit()

    def add_file(self, filename):
        """
        Add a file or directory to this widget.
        """
        if filename not in self.filenames:
            if not os.access(filename, os.R_OK):
                Alert(strings._("not_a_readable_file", True).format(filename))
                return

            self.filenames.append(filename)

            fileinfo = QtCore.QFileInfo(filename)
            basename = os.path.basename(filename.rstrip('/'))
            ip = QtWidgets.QFileIconProvider()
            icon = ip.icon(fileinfo)

            if os.path.isfile(filename):
                size = common.human_readable_filesize(fileinfo.size())
            else:
                size = common.human_readable_filesize(common.dir_size(filename))
            item_name = '{0:s} ({1:s})'.format(basename, size)
            item = QtWidgets.QListWidgetItem(item_name)
            item.setToolTip(size)

            item.setIcon(icon)
            self.addItem(item)

            self.files_updated.emit()


class FileSelection(QtWidgets.QVBoxLayout):
    """
    The list of files and folders in the GUI, as well as buttons to add and
    delete the files and folders.
    """
    def __init__(self):
        super(FileSelection, self).__init__()
        self.server_on = False

        # file list
        self.file_list = FileList()
        self.file_list.currentItemChanged.connect(self.update)
        self.file_list.files_dropped.connect(self.update)

        # buttons
        self.add_files_button = QtWidgets.QPushButton(strings._('gui_add_files', True))
        self.add_files_button.clicked.connect(self.add_files)
        self.add_dir_button = QtWidgets.QPushButton(strings._('gui_add_folder', True))
        self.add_dir_button.clicked.connect(self.add_dir)
        self.delete_button = QtWidgets.QPushButton(strings._('gui_delete', True))
        self.delete_button.clicked.connect(self.delete_file)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_files_button)
        button_layout.addWidget(self.add_dir_button)
        button_layout.addWidget(self.delete_button)

        # add the widgets
        self.addWidget(self.file_list)
        self.addLayout(button_layout)

        self.update()

    def update(self):
        """
        Update the GUI elements based on the current state.
        """
        # all buttons should be disabled if the server is on
        if self.server_on:
            self.add_files_button.setEnabled(False)
            self.add_dir_button.setEnabled(False)
            self.delete_button.setEnabled(False)
        else:
            self.add_files_button.setEnabled(True)
            self.add_dir_button.setEnabled(True)

            # delete button should be disabled if item isn't selected
            current_item = self.file_list.currentItem()
            if not current_item:
                self.delete_button.setEnabled(False)
            else:
                self.delete_button.setEnabled(True)

        # update the file list
        self.file_list.update()

    def add_files(self):
        """
        Add files button clicked.
        """
        file_dialog = QtWidgets.QFileDialog(caption=strings._('gui_choose_files', True))
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        file_dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        file_dialog.setOption(QtWidgets.QFileDialog.ReadOnly, True)
        tree_view = file_dialog.findChild(QtWidgets.QTreeView)
        tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        list_view = file_dialog.findChild(QtWidgets.QListView, "listView")
        list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
          for filename in file_dialog.selectedFiles():
              self.file_list.add_file(filename)

        self.update()

    def add_dir(self):
        """
        Add folder button clicked.
        """
        file_dialog = QtWidgets.QFileDialog(caption=strings._('gui_choose_folder', True))
        file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        file_dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        file_dialog.setOption(QtWidgets.QFileDialog.ReadOnly, True)
        file_dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        tree_view = file_dialog.findChild(QtWidgets.QTreeView)
        tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        list_view = file_dialog.findChild(QtWidgets.QListView, "listView")
        list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
          for filename in file_dialog.selectedFiles():
              self.file_list.add_file(filename)

        self.update()

    def delete_file(self):
        """
        Delete button clicked
        """
        current_row = self.file_list.currentRow()
        self.file_list.filenames.pop(current_row)
        self.file_list.takeItem(current_row)
        self.update()

    def server_started(self):
        """
        Gets called when the server starts.
        """
        self.server_on = True
        self.file_list.setAcceptDrops(False)
        self.update()

    def server_stopped(self):
        """
        Gets called when the server stops.
        """
        self.server_on = False
        self.file_list.setAcceptDrops(True)
        self.update()

    def get_num_files(self):
        """
        Returns the total number of files and folders in the list.
        """
        return len(self.file_list.filenames)

    def setFocus(self):
        """
        Set the Qt app focus on the file selection box.
        """
        self.file_list.setFocus()
