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
        
        # Define Widgets...
        menu_open_button = self.actionOpen
        menu_chart_button = self.actionChart_View
        menu_analysis_button = self.actionAnalysis_View
        
        self.pages = self.findChild(QStackedWidget, 'stackedWidget')
        self.welcome_page= self.findChild(QWidget, 'welcomePage')
        self.chart_page= self.findChild(QWidget, 'chartPage')
        self.analysis_page= self.findChild(QWidget, 'analysisPage')
        
        copyright_label = self.findChild(QLabel, 'copyright')
        
        # Edit widget UI...
        self.pages.setCurrentWidget(self.welcome_page)
            # self.chart_frame.setStyleSheet("border: 2px solid black;")
        
        copyright_label.setText(f"© Md. Mahdi Mohtasim  {datetime.now().year}")
        
        # Triggering the buttons...
        menu_open_button.triggered.connect(self.getDataFromFile)
        menu_chart_button.triggered.connect(self.drawCustomChart)
        menu_analysis_button.triggered.connect(self.showAnalysisPage)
        
        
    def resizeEvent(self, event):
        # This function will be called whenever the window is resized
        new_size = event.size()
        print(f"Window size changed to: {new_size.width()} x {new_size.height()}")

        
    def getDataFromFile(self):
        try:
            # Fetching data from the Excel file...
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)")
            file = Files(file_name[0])
            self.data= file.load_data_from_excel()
            print("Data Fetched")
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
            self.chart.plot_custom_chart(self.data)
        except Exception:
            print("Error Drawing The File...")
            return
            
            
    def showAnalysisPage(self):
        self.pages.setCurrentWidget(self.analysis_page)
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.setWindowIcon(QIcon('Images\logo.jpg'))
    window.show()
    app.exec()
