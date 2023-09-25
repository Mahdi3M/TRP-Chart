import openpyxl


# Custom Files class for import and export files
class Files():
    def __init__(self, file_name):
        self.file_name = file_name


    # For xlsx files....
    def load_data_from_excel(self):
        workbook = openpyxl.load_workbook(self.file_name)
        worksheet = workbook.active
        
        # Create chart_groups according to channels...
        chart_groups = {}
        table_groups = {}
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            if row[0] and row[1] and row[2] and row[3] and row[4]:
                
                # Initialize channel if not exist or Append row is exists...
                if int(row[2]) not in chart_groups:
                    chart_groups[int(row[2])] = []
                    table_groups[int(row[2])] = [0.0, 0, float('inf'), float('-inf'), row[3], row[4]]
                    
                chart_groups[int(row[2])].append((row[0], row[1], row[3], row[4]))
                
                table_groups[int(row[2])][0] = round(table_groups[int(row[2])][0]+float(row[1]), 2)
                table_groups[int(row[2])][1] += 1
                table_groups[int(row[2])][2] = min(round(float(row[1]), 2), table_groups[int(row[2])][2])
                table_groups[int(row[2])][3] = max(float(row[1]), table_groups[int(row[2])][3])
                table_groups[int(row[2])][4] = min(row[3], table_groups[int(row[2])][4])
                table_groups[int(row[2])][5] = max(row[4], table_groups[int(row[2])][5])
                
        return {'chart_data': chart_groups, 'table_data': table_groups}