import openpyxl


# Custom Files class for import and export files
class Files():
    def __init__(self, file_name):
        self.file_name = file_name


    # For xlsx files....
    def load_data_from_excel(self):
        workbook = openpyxl.load_workbook(self.file_name)
        worksheet = workbook.active
        
        # Create groups according to channels...
        groups = {}
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            if row[0] and row[1] and row[2] and row[3] and row[4]:
                
                # Initialize channel if not exist or Append row is exists...
                if int(row[2]) not in groups:
                    groups[int(row[2])] = []
                    
                groups[int(row[2])].append((row[0], row[1], row[3], row[4]))
                
        return groups