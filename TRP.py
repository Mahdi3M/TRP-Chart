from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from MyFile import *
from MyChart import *
import sys



# The Main Frame class...
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self)
        
        self.chart = CustomChart()
        
        # Define Widgets...
        menu_open_button = self.actionOpen
        
        central_widget = self.centralwidget
        chart_layout = self.verticalLayout
        
        # Edit widget UI...
        central_widget.setLayout(chart_layout)
        chart_layout.addWidget(self.chart.canvas)
        
        # Triggering the buttons...
        menu_open_button.triggered.connect(self.menu_open_button_triggered)

        
    def menu_open_button_triggered(self):
        try:
            # Fetching data from the Excel file...
            file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)")
            file = Files(file_name[0])
            data = file.load_data_from_excel()
            
            # Drawing the custom chart...
            self.chart.plot_custom_chart(data)
        except Exception:
            print("Error...")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QIcon('logo.jpg'))
    window.show()
    app.exec()
