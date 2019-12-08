from pandas import read_excel

class XlsxReader:

    def read_xlsx(self, file_path):
        """
        Read XLSX (Excel) file and return row data as a dictionary
        """
        data = read_excel(file_path)
        cols = data.columns.to_list()

        data_dict = []

        for row in data.values:
            row_data = {}

            for i in range(0, len(cols) - 1):
                col = cols[i]
                value = row[i]
                row_data[col] = value

            data_dict.append(row_data)

        return data_dict