from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from lib.MyChart import *
from lib.MyFile import *
from datetime import datetime
import sys



# The Main Frame class...
class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("lib\interface.ui", self)
        
        self.chart = None
        self.data = None
        self.resolution = None
        self.movie = QMovie('images\\loading.gif')
        print(self.movie)
        
        # Define Widgets...
        menu_open_button = self.actionOpen
        menu_chart_button = self.actionChart_View
        menu_analysis_button = self.actionAnalysis_View
        
        self.pages = self.findChild(QStackedWidget, 'stackedWidget')
        self.welcome_page= self.findChild(QWidget, 'welcomePage')
        self.chart_page= self.findChild(QWidget, 'chartPage')
        self.analysis_page= self.findChild(QWidget, 'analysisPage')
        self.qa_page= self.findChild(QWidget, 'qaPage')
        self.result_page= self.findChild(QWidget, 'resultPage')
        self.loading_page= self.findChild(QWidget, 'loadingPage')
        
        self.analysis_table= self.findChild(QTableWidget, 'analysisTable')
        self.next_button= self.findChild(QPushButton, 'nextButton')
        self.submit_button= self.findChild(QPushButton, 'submitButton')
                
        self.loading_gif= self.findChild(QLabel, 'animationLabel')
        self.result_label= self.findChild(QLabel, 'resultLabel')
        
        copyright_label = self.findChild(QLabel, 'copyright')
        
        # Edit widget UI...
        self.pages.setCurrentWidget(self.welcome_page)
        
        self.analysis_table.setColumnCount(7)
        self.analysis_table.setShowGrid(True)
        
        copyright_label.setText(f"© Md. Mahdi Mohtasim  {datetime.now().year}")
        
        # Triggering the buttons...
        menu_open_button.triggered.connect(self.getDataFromFile)
        menu_chart_button.triggered.connect(self.drawCustomChart)
        menu_analysis_button.triggered.connect(self.showAnalysisPage)
        
        self.next_button.clicked.connect(self.showQAPage)
        self.submit_button.clicked.connect(self.showResultPage)
        
        
    def resizeEvent(self, event):
        # This function will be called whenever the window is resized
        self.resolution = event.size()
        # print(f"Window size changed to: {new_size.width()} x {new_size.height()}")        
        if self.pages.currentIndex() in [1]:
            self.drawCustomChart()
        elif self.pages.currentIndex() in [2, 3]:
            self.showAnalysisPage()

        
    def getDataFromFile(self):
        try:
            # Fetching data from the Excel file...
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)")
            file = Files(file_name[0])
            self.data = file.load_data_from_excel()
        except Exception:
            print("Error Fetching The File...")
            return
        
        if self.pages.currentIndex() in [1]:
            self.drawCustomChart()
        elif self.pages.currentIndex() in [2]:
            self.showAnalysisPage()
        else:
            self.drawCustomChart()
            
            
    def drawCustomChart(self):
        self.pages.setCurrentWidget(self.chart_page)
        if not self.data:
            self.getDataFromFile()
            return
        try:
            # Drawing the custom chart...
            if self.chart:
                self.chart.canvas.setParent(None)   # Remove the canvas widget
                self.chart.canvas.deleteLater()     # Destroy the canvas
                del self.chart
                
            self.chart = CustomChart()
            chart_layout = self.findChild(QVBoxLayout, 'verticalLayout')
            chart_layout.addWidget(self.chart.canvas)
            self.chart.plot_custom_chart(self.data['chart_data'])
        except Exception:
            print("Error Drawing The File...")
            return
            
            
    def showAnalysisPage(self):
        self.pages.setCurrentWidget(self.analysis_page)
        if not self.data:
            self.getDataFromFile()
            return
        
        for col in range(7):
            if col in [3, 4]:
                self.analysis_table.setColumnWidth(col, max(self.resolution.width()//7, 160))
            elif col in [5, 6]:
                self.analysis_table.setColumnWidth(col, max(self.resolution.width()//7, 120))
            else:
                self.analysis_table.setColumnWidth(col, max((self.resolution.width()-175)//7, 100))
        
        # print(self.resolution.width())
        row_count = len(self.data['table_data'])
        self.analysis_table.setRowCount(row_count)

        header = self.analysis_table.horizontalHeader()
        for col in range(7):
            header.setStyleSheet(
                "QHeaderView::section {"
                f"background-color: #d4d4d4;"
                "}"
            )
            
        for row, (key, values) in enumerate(self.data['table_data'].items()):
            item = QTableWidgetItem("Channel " + str(key))
            item.setTextAlignment(Qt.AlignCenter)
            self.analysis_table.setItem(row, 0, item)
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.analysis_table.setItem(row, col+1, item)
                
                
    def showQAPage(self):
        self.pages.setCurrentWidget(self.qa_page)
                
                
    def showResultPage(self):
        self.pages.setCurrentWidget(self.loading_page)
        self.loading_gif.setMovie(self.movie)
        
        timer = QTimer(self.loading_gif)
        self.start_loading()
        timer.singleShot(3000, self.stop_loading)
        
        
    def start_loading(self):
        self.movie.start()
        print("Loading Start")
        
        
    def stop_loading(self):
        self.movie.stop()
        print("Loading End")
        
        self.pages.setCurrentWidget(self.result_page)
        channel = "Channel 1"
        result = "Actual Watched Channel: " + channel
        
        self.result_label.setText(result)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.setWindowIcon(QIcon('Images\logo.jpg'))
    window.show()
    app.exec()
