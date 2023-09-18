from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from lib.MyChart import *
from lib.MyFile import *
import sys



# The Main Frame class...
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("lib\interface.ui", self)
        
        self.chart = CustomChart()
        
        # Define Widgets...
        menu_open_button = self.actionOpen
        
        self.welcome_frame= self.findChild(QFrame, 'welcomeFrame')
        self.chart_frame= self.findChild(QFrame, 'chartFrame')
        
        copyright_label = self.findChild(QLabel, 'copyright')
        
        # Edit widget UI...
        self.chart_frame.hide()
        
        copyright_label.setText(f"© Md. Mahdi Mohtasim  {datetime.now().year}")
        
        # Triggering the buttons...
        menu_open_button.triggered.connect(self.menu_open_button_triggered)

        
    def menu_open_button_triggered(self):
        try:
            # Fetching data from the Excel file...
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)")
            file = Files(file_name[0])
            groups, start, finish = file.load_data_from_excel()
            
            # Drawing the custom chart...
            self.welcome_frame.hide()
            self.chart_frame.show()
            chart_layout = self.findChild(QVBoxLayout, 'verticalLayout_4')
            chart_layout.addWidget(self.chart.canvas)
            self.chart.plot_custom_chart(groups, start, finish)
            
        except Exception:
            print("Error...")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QIcon('Images\logo.jpg'))
    window.show()
    app.exec()
