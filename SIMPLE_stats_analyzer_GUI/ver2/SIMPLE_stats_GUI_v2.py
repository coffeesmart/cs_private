import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import ftn_SIMPLE_stats_analysis_v2
import os

# #UI파일 연결
# #단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
# form_class = uic.loadUiType('./SIMPLE_stats_analyzer_GUI_v1.ui')[0]

#화면을 띄우는데 사용되는 Class 선언
# class WindowClass(QMainWindow, form_class) :

class MyApp(QMainWindow, QWidget):

    def __init__(self) :
        super().__init__()
        # self.setupUi(self)
        self. initUI()

    def initUI(self):

        self.setWindowTitle('My First Application')
        self.move(500, 300)
        self.resize(810, 470)

        self.setFixedSize(810, 470)
        self.setAcceptDrops(True)
        self.statusBar().showMessage('Ready')

        # Icon 설정
        self.setWindowIcon(QIcon('web.png'))

        # 단축키 설정
        self.shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.shortcut.activated.connect(qApp.quit)

        # QLabel - label_file_path (white box)
        self.label_file_path = QLabel(self)
        self.label_file_path.setFrameShape(QFrame.Panel)
        self.label_file_path.setFrameShadow(QFrame.Sunken)
        self.label_file_path.setStyleSheet("background-color: white")
        self.label_file_path.setLineWidth(1)
        self.label_file_path.setGeometry(30,40,650,250)
        font_helve_plain_small = self.label_file_path.font()
        font_helve_plain_small.setFamily('Helvetica')
        font_helve_plain_small.setPointSize(8)
        self.label_file_path.setFont(font_helve_plain_small)

        # QLabel - Drag & Drop
        self.label_dragdrop = QLabel('Drag & Drop files ↓', self)
        self.label_dragdrop.setFixedSize(200,20)
        self.label_dragdrop.move(30,20)
        font_helve_bold = self.label_dragdrop.font()
        font_helve_bold.setFamily('Helvetica')
        font_helve_bold.setPointSize(10)
        font_helve_bold.setBold(True)
        self.label_dragdrop.setFont(font_helve_bold)

        # QPushButton - Find files
        btn_path_finder = QPushButton('Find files', self)
        btn_path_finder.setGeometry(690,39,100,120)
        btn_path_finder.clicked.connect(self.btn_path_finder_Function)

        # QPushButton - Stats analysis
        btn_stats_analysis = QPushButton('Stats analysis', self)
        btn_stats_analysis.setGeometry(690,170,100,120)
        btn_stats_analysis.clicked.connect(self.btn_stats_analysis_Function)

        # QLabel - label_save_path (white box)
        self.label_save_path = QLabel(self)
        self.label_save_path.setFrameShape(QFrame.Panel)
        self.label_save_path.setFrameShadow(QFrame.Sunken)
        self.label_save_path.setStyleSheet("background-color: white")
        self.label_save_path.setLineWidth(1)
        self.label_save_path.setGeometry(30,400,650,30)
        self.label_save_path.setFont(font_helve_plain_small)

        # QGroupBox - options
        GB = QGroupBox("Options",self)
        GB.setGeometry(50,315,710,50)
        GB.setFont(font_helve_bold)

        # QCheckBox - options
        self.CB_Last_stats_summary = QCheckBox('Last_stats_summary', self)
        self.CB_Last_stats_summary.move(80,336)
        self.CB_Last_stats_summary.setFixedSize(200, 20)
        font_helve_plain = self.CB_Last_stats_summary.font()
        font_helve_plain.setFamily('Helvetica')
        font_helve_plain.setPointSize(9)
        self.CB_Last_stats_summary.setFont(font_helve_plain)
        self.CB_Last_stats_summary.clicked.connect(self.groupboxCheckFunction)

        # QLabel - saved folder
        self.label_saved_folder = QLabel('Saved folder ↓', self)
        self.label_saved_folder.setFixedSize(200,20)
        self.label_saved_folder.move(30,380)
        self.label_saved_folder.setFont(font_helve_bold)

        # QPushButton - Open saved folder
        btn_savepath_open = QPushButton('Open folder', self)
        btn_savepath_open.setGeometry(690,400,100,30)
        btn_savepath_open.clicked.connect(self.btn_savepath_open_Function)

        # 변수들 초기상태
        self.file_path = ""
        self.file_path_text = ""
        self.file_path_list = []
        self.save_path = ""
        self.summary_onoff = 'off'

        self.show()

    # Drag and drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.file_path_text = ""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for u in files :
            self.file_path_list.append(u)
            self.file_path_text += u + '\n'
        self.label_file_path.setText(self.file_path_text)
        self.statusBar().showMessage('Files loaded')

    def groupboxCheckFunction(self):
        if self.CB_Last_stats_summary.isChecked():
            self.statusBar().showMessage('Checked')
            self.summary_onoff = 'on'
        elif self.CB_Last_stats_summary.isChecked() == False :
            self.statusBar().showMessage('Unchecked')
            self.summary_onoff = 'off'

    # btn_path_finder가 눌리면 작동할 함수
    def btn_path_finder_Function(self):
        self.file_path_list = []
        self.file_path = QFileDialog.getOpenFileName(self)[0]
        self.file_path_list.append(self.file_path)
        self.label_file_path.setText(self.file_path_list[0])
        self.statusBar().showMessage('File loaded')

    # btn_stats_analysis가 눌리면 작동할 함수
    def btn_stats_analysis_Function(self):
        if not self.file_path_list :
            self.label_save_path.setText('Error occurred, please load the file.')
            self.statusBar().showMessage('error - no file')
        else :
            self.save_path = ftn_SIMPLE_stats_analysis_v2.stats_analysis(self.file_path_list, self.summary_onoff)
            self.label_save_path.setText(self.save_path)
            self.statusBar().showMessage('Stats analyzed, save plot and data')

    # btn_savepath_open이 눌리면 작동할 함수
    def btn_savepath_open_Function(self):
        if not self.save_path :
            self.label_save_path.setText('Error occurred, please analyze stats.')
            self.statusBar().showMessage('error - no result')
        else :
            os.startfile(self.save_path)
            self.statusBar().showMessage('Open saved folder')

if __name__ == "__main__" :
    # #QApplication : 프로그램을 실행시켜주는 클래스
    # app = QApplication(sys.argv)
    #
    # #WindowClass의 인스턴스 생성
    # myWindow = WindowClass()
    #
    # #프로그램 화면을 보여주는 코드
    # myWindow.show()
    #
    # #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    # app.exec_()

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())