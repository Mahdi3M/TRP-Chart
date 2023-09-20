from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from lib.MyChart import *
from lib.MyFile import *
import sys



# The Main Frame class...
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("lib\interface.ui", self)
        
        self.chart = None
        self.data = None
        
        # Define Widgets...
        menu_open_button = self.actionOpen
        
        self.pages = self.findChild(QStackedWidget, 'stackedWidget')
        self.welcome_page= self.findChild(QWidget, 'welcomePage')
        self.chart_page= self.findChild(QWidget, 'chartPage')
        
        copyright_label = self.findChild(QLabel, 'copyright')
        
        # Edit widget UI...
        self.pages.setCurrentWidget(self.welcome_page)
            # self.chart_frame.setStyleSheet("border: 2px solid black;")
        
        copyright_label.setText(f"© Md. Mahdi Mohtasim  {datetime.now().year}")
        
        # Triggering the buttons...
        menu_open_button.triggered.connect(self.getDataFromFile)
        
        
    def resizeEvent(self, event):
        # This function will be called whenever the window is resized
        new_size = event.size()
        print(f"Window size changed to: {new_size.width()} x {new_size.height()}")
        print(self.pages.currentIndex())

        
    def getDataFromFile(self):
        try:
            # Fetching data from the Excel file...
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)")
            file = Files(file_name[0])
            self.data= file.load_data_from_excel()
        except Exception:
            print("Error Fetching The File...")            
        
        self.drawCustomChart()
            
    def drawCustomChart(self):
        try:
            # Drawing the custom chart...
            if self.chart:
                self.chart.canvas.setParent(None)   # Remove the canvas widget
                self.chart.canvas.deleteLater()     # Destroy the canvas
                del self.chart
                
            self.chart = CustomChart()
            self.pages.setCurrentWidget(self.chart_page)
            chart_layout = self.findChild(QVBoxLayout, 'verticalLayout')
            chart_layout.addWidget(self.chart.canvas)
            self.chart.plot_custom_chart(self.data)
        except Exception:
            print("Error Drawing The File...")   
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QIcon('Images\logo.jpg'))
    window.show()
    app.exec()
