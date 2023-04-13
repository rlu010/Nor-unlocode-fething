import pandas as pd
import csv
import re

def fetchCodes():
    url = 'https://service.unece.org/trade/locode/no.htm' # replace with the actual URL of the website
    table = pd.read_html(url)[2] # assumes that the table is the first one on the page
    #table.to_csv('unlocodesnor.csv', index=False)

    table.to_csv('unlocodesnor.csv', index=False, columns=[1,2,5,9], header=False)


def convert_coordinates_to_decimal_degrees(coordinates):
    # Split the coordinates into degrees and minutes
    lat_degrees = float(coordinates[:2])
    lat_minutes = float(coordinates[2:4]) / 60

    lon_degrees = float(coordinates[6:9])
    lon_minutes = float(coordinates[9:11]) / 60

    # Convert the coordinate direction to a sign
    lat_sign = 1 if coordinates[4] == 'N' else -1
    lon_sign = 1 if coordinates[11] == 'E' else -1

    # Calculate the decimal degrees coordinates
    lat_decimal_degrees = lat_sign * (lat_degrees + lat_minutes)
    lon_decimal_degrees = lon_sign * (lon_degrees + lon_minutes)

    return lat_decimal_degrees, lon_decimal_degrees

def convert_coordinates(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        header_row = next(csv_reader)

        # Find the index of the 6th column
        function_col_index = 3

        # Replace the last column header with LAT and LON
        header_row[-1] = 'LAT'
        header_row.append('LON')

        # Open a new CSV file for writing
        with open('filtered_fileee.csv', 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(header_row)

            # Iterate over each row in the original CSV file
            for row in csv_reader:
                # Check if the function column contains a 1
                if (row[function_col_index] != ""):
                    new = convert_coordinates_to_decimal_degrees(row[function_col_index])
                    #latlon = re.sub(r'\(|\)', '', new.__str__())
                    row[function_col_index] = new[0]
                    row.append(new[1])
                    # If so, write the row to the new CSV file
                    csv_writer.writerow(row)


def main():
    fetchCodes()
    convert_coordinates('unlocodesnor.csv')


if __name__ == "__main__":
    main()