import openpyxl



class Files():
    def __init__(self, file_name):
        self.file_name = file_name


    # For xlsx files....
    def load_data_from_excel(self):
        workbook = openpyxl.load_workbook(self.file_name)
        worksheet = workbook.active
        data = []
        for row in worksheet.iter_rows(values_only=True):
            if row[0] and row[1] and row[2] and row[3] and row[4]:
                data.append(row)
        return data[1:]