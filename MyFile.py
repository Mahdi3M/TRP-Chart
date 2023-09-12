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
        channel_data = {}
        times = set()
        first_row = True
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            if row[0] and row[1] and row[2] and row[3] and row[4]:
                
                # Initialize channel if not exist or Append row is exists...
                if int(row[2]) not in channel_data:
                    channel_data[int(row[2])] = []
                    
                channel_data[int(row[2])].append((row[0], row[1], row[3], row[4]))
                
                # Find out Starting point and Finishing point of chart...    
                # if first_row:
                #     earliest_start_time = row[3]
                #     latest_finish_time = row[4]
                #     first_row = False
                # else:
                #     if row[3] < earliest_start_time:
                #         earliest_start_time = row[3]
                #     if row[4] > latest_finish_time:
                #         latest_finish_time = row[4]
                        
                # Find the unique start times and endtimes
                times.add(row[3])
                times.add(row[4])
        
        times = sorted(times)
        return channel_data, list(times)