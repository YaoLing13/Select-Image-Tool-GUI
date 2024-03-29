import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import glob
import cv2
import shutil

def get_imags(dir):
    images_1 = os.listdir(dir)
    images_1.sort()
    images = []
    for image in images_1:
        images.extend([dir + '/' + image])
    return images


class SelectImage(QMainWindow):

    def __init__(self, size_w, size_h, pos_w, pos_h, Title):
        super().__init__()
        self.line=QLineEdit()
        self.src_dir = ''
        self.save1_dir = ''
        self.del_dir = './del'
        self.initUI(size_w, size_h, pos_w, pos_h, Title)
        # btn_open_dir(self, sb_w, sb_h, pb_w, pb_h, sl_w, sl_h, pl_w, pl_h, bt_name="", holdtext="", bt_tip="")
        self.btn_open_dir(150,30, 30, 70,200,30,200,70, "Source dir", "Source dir", "Source dir", -1)
        self.btn_open_dir(150,30, 30, 120,200,30,200,120, "Save dir 1", "Save dir 1", "Save dir", 1)
        self.btn_open_dir(150,30, 30, 170,200,30,200,170, "Save dir 2", "Save dir 2", "Save dir", 2)
        self.btn_open_dir(150,30, 30, 220,200,30,200,220, "Save dir 3", "Save dir 3", "Save dir", 3)
        self.btn_open_dir(150, 30, 30, 270, 200, 30, 200, 270, "Delete dir", "Delete dir", "Delete dir", 0)
        self.btn_start()
        self.show()

    def initUI(self, size_w, size_h, pos_w, pos_h, Title):
        # self.setGeometry(pos_w,pos_h, size_w,size_h)
        # exitAction = QAction(QIcon('exit.jpeg'), '&Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(qApp.quit)

        self.resize(size_w, size_h)
        self.center()
        self.setWindowTitle(Title)
        self.setWindowIcon(QIcon('./icon/image.png'))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_push(self, name, s_w, s_h, p_w, p_h, tip=''):
        QToolTip.setFont(QFont('SansSerif', 10))
        button = QPushButton(name, self)
        button.setToolTip(tip)
        button.resize(s_w, s_h) # button size
        button.move(p_w, p_h,) # button position: W,H
        return button

    def set_text(self, s_w, s_h, p_w, p_h, holdtext=''):
        lineEdit = QLineEdit(self)
        lineEdit.resize(s_w, s_h)
        lineEdit.move(p_w, p_h)
        lineEdit.setPlaceholderText(holdtext)
        lineEdit.setEchoMode(QLineEdit.Normal)
        return lineEdit

    # def set_key_text(self, s_w, s_h, p_w, p_h, holdtext=''):




    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
    #          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

## delete file
    def open_dir(self, lineEdit, flag):
        directory = QFileDialog.getExistingDirectory(self, "select file", self.src_dir)  # start file
        lineEdit.setText(directory)
        if flag == 0:
            self.del_dir = directory
            return
        elif flag == 1:
            self.save1_dir = directory
            return
        elif flag == 2:
            self.save2_dir = directory
            return
        elif flag == 3:
            self.save3_dir = directory
            return
        else:
            self.src_dir = directory
            return

    def line_edit_text(self, s_w, s_h, p_w, p_h, holdtext=""):
        lineEdit = self.set_text(s_w, s_h, p_w, p_h, holdtext)
        lineEdit.setReadOnly(True)
        return lineEdit


    def btn_open_dir(self, sb_w, sb_h, pb_w, pb_h, sl_w, sl_h, pl_w, pl_h,bt_name="", holdtext="", bt_tip="", flag=1):
        btn = self.button_push(bt_name, sb_w, sb_h, pb_w, pb_h, bt_tip)
        line = self.line_edit_text(sl_w, sl_h, pl_w, pl_h, holdtext)
        btn.clicked.connect(lambda:self.open_dir(line, flag))

    def btn_start(self):
        name = "Begin"
        s_w, s_h = 100, 50
        p_w, p_h = 180, 320
        tip = 'Begin select'
        btn = self.button_push(name, s_w, s_h, p_w, p_h, tip)
        btn.clicked.connect(self.show_images)

    def show_images(self, event):
        reply = -1
        if (self.src_dir == ''):
            QMessageBox.warning(self, 'Message', "Please choose source directoty of images !")
        elif (self.save1_dir == ''):
            QMessageBox.warning(self, 'Message', "Please choose source directoty of images !")
        elif (self.del_dir == './del'):
            reply = QMessageBox.information(self, 'Message', "del file is default: ./del")
        else:
            reply = QMessageBox.Ok
        if reply == QMessageBox.Ok:
            images = get_imags(self.src_dir)
            print("src_dir: %s " % self.src_dir)
            print("save1_dir: %s " % self.save1_dir)
            if not os.path.exists(self.del_dir):
                os.mkdir(self.del_dir)
            print("del_dir: %s " % self.del_dir)
            save1_num = 0
            save2_num = 0
            save3_num = 0
            index = 0
            cv2.namedWindow("src", cv2.WINDOW_NORMAL)
            while True:
                print(images[index])
                img = cv2.imread(images[index])
                cv2.imshow("src", img)
                # c = cv2.waitKeyEx(0)
                c = cv2.waitKey(0)
                if c == 97 or c == 81 or c == 82:  ## last image - 'a'
                    index -= 1
                    if index < 0:
                        index = len(images)-1
                    else:
                        pass
                    continue
                if c == 32 or c == 115: # save image - 's' or 'Spave'
                    if not os.path.exists(self.save1_dir+images[index][images[index].rfind('/'):]):
                        shutil.copy(images[index], self.save1_dir)
                        save1_num += 1
                    print("**** %d - save dir 1: %s" % (save1_num,images[index]))
                    continue
                if c == 100: # save image - 'd'
                    if not os.path.exists(self.save2_dir+images[index][images[index].rfind('/'):]):
                        shutil.copy(images[index], self.save2_dir)
                        save2_num += 1
                    print("**** %d - save dir 2: %s" % (save2_num,images[index]))
                    continue
                if c == 102: # save image - 'f'
                    if not os.path.exists(self.save3_dir+images[index][images[index].rfind('/'):]):
                        shutil.copy(images[index], self.save3_dir)
                        save3_num += 1
                    print("**** %d - save dir 3: %s" % (save3_num,images[index]))
                    continue
                if c == 13 or c == 83 or c == 84 : # next image- 'Enter'
                    index += 1
                    if index > (len(images)-1):
                        index = 0
                    else:
                        pass
                    continue
                if c == 255: # delete image - 'Del'
                    print("*********delete: %s" % images[index])
                    # os.remove(images[index])
                    shutil.move(images[index], self.del_dir)
                    index += 1
                    if index > (len(images)-1):
                        index = 0
                    else:
                        pass
                if c == 27: # Quit - 'ESC'
                    print("*********End: %s" % images[index])
                    print("Quit!")
                    cv2.destroyAllWindows()
                    break
            print("Save dir 1 image: %d" % save1_num)
            print("Save dir 2 image: %d" % save2_num)
            print("Save dir 3 image: %d" % save3_num)
        return



if __name__ == '__main__':
    app = QApplication(sys.argv) # app instance
    # w = QWidget() # window instance
    # w.resize(960,640) ## windoe size: (W, H)
    # w.move(600, 300) ## (W, H): show window position (left top), if not parent win, desktop will be parent
    # w.setWindowTitle("Select images to save")  ## Window title
    # w.show() # show win
    se = SelectImage(450, 500, 600, 300, "Select images to save") # size_w, size_h, pos_w, pos_h
    sys.exit(app.exec_())
