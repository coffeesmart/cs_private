import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, qApp, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import ftn_SIMPLE_stats_analysis
import os

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType('./SIMPLE_stats_analyzer_GUI_v1.ui')[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(800, 180)
        self.setAcceptDrops(True)
        self.statusBar().showMessage('Ready')

        # Icon 설정
        # self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))

        # 단축키 설정
        self.shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.shortcut.activated.connect(qApp.quit)

        # btn 기능 추가
        self.btn_path_finder.clicked.connect(self.btn_path_finder_Function)
        self.btn_stats_analysis.clicked.connect(self.btn_stats_analysis_Function)
        self.btn_savepath_open.clicked.connect(self.btn_savepath_open_Function)

        # Radio btn 초기 상태 설정
        self.radiobtn_justsave.setChecked(True)
        self.figshow_onoff = 'off'
        # Radio btn 기능 추가
        self.radiobtn_both.clicked.connect(self.groupboxRadFunction)
        self.radiobtn_justsave.clicked.connect(self.groupboxRadFunction)

        # file_path 초기상태
        self.file_path = ""
        self.save_path = ""

    # Drag and drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if len(files) == 1:
            self.file_path = files[0]
            self.label_find_path.setText(self.file_path)
            self.statusBar().showMessage('File loaded')
        else :
            self.label_find_path.setText('error - please drop just one file')
            self.statusBar().showMessage('error - too many files are loaded')

    def groupboxRadFunction(self):
        if self.radiobtn_both.isChecked():
            self.statusBar().showMessage('Checked')
            self.figshow_onoff = 'on'
        elif self.radiobtn_justsave.isChecked():
            self.statusBar().showMessage('Checked')
            self.figshow_onoff = 'off'

    # btn_path_finder가 눌리면 작동할 함수
    def btn_path_finder_Function(self):
        self.file_path = QFileDialog.getOpenFileName(self)[0]
        self.label_find_path.setText(self.file_path)
        self.statusBar().showMessage('File loaded')

    # btn_stats_analysis가 눌리면 작동할 함수
    def btn_stats_analysis_Function(self):
        if not self.file_path :
            self.label_save_path.setText('Error occurred, please load the file.')
            self.statusBar().showMessage('error - no file')
        else :
            self.save_path = ftn_SIMPLE_stats_analysis.stats_analysis(self.file_path, self.figshow_onoff)
            self.label_save_path.setText(self.save_path)
            self.statusBar().showMessage('Stats analyzed, save plot and data')

    # btn_savepath_open이 눌리면 작동할 함수
    def btn_savepath_open_Function(self):
        if not self.save_path :
            self.label_save_path.setText('Error occurred, please analyse stats.')
            self.statusBar().showMessage('error - no result')
        else :
            os.startfile(self.save_path)
            self.statusBar().showMessage('Open saved folder')

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()