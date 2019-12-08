import csv
import os

class CsvReader:

    def read_csv(self, file_path):
        '''
        Read CSV file and return data as a dictionary
        '''
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, file_path)
        return_data = []

        with open(abs_file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            cols = []
            for row in csv_reader:
                if not cols:
                    cols = row
                else:
                    row_data = {}
                    for i in range(0, len(cols) - 1):
                        col = cols[i]
                        row_data[col] = row[i]
                    return_data.append(row_data)
        return return_data