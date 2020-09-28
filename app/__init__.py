import csv
import os
import sys
import json
import random
import string

def fixed_width_to_csv(csv_cols, csv_col_widths, fixed_width_file, fixed_width_encoding, csv_encoding):
    
    output_csv_file = os.path.join(sys.path[0], "output.csv")
    '''
    Every row item of the fixed width file is stored as a list and hence the name "output_list_of_lists"
    with a list for header items followed by fixed with data lists
    '''
    output_list_of_lists = []
    '''
    list for headers items fetched from "spec.json"
    '''
    headers = []
    '''
    list for body of fixed width file
    '''
    fixed_width_rows_list = []

    with open(fixed_width_file, 'r', encoding=fixed_width_encoding) as fixed_width_file_obj:
        for line in fixed_width_file_obj:
            line = [line.strip()]
            fixed_width_rows_list.append(line)

    for columnName in csv_cols:
        headers.append(columnName)
    '''
    Append the headers first
    '''
    output_list_of_lists.append(headers)

    '''
    Split the single string list items into multiple strings
    '''
    for row in fixed_width_rows_list:
        csv_row = [cols for singlestringlist in row for cols in singlestringlist.split()]
        output_list_of_lists.append(csv_row)

    with open(output_csv_file, 'w', newline='', encoding=csv_encoding) as out_csv_file:
        writer = csv.writer(out_csv_file)
        writer.writerows(output_list_of_lists)

def gen_fixed_width_file(fNames, fWidths, fWidthEncoding):

    metadata_dict = dict(zip(fNames, fWidths))
    rows = []
    '''
    generate randomized data of 100 rows with offsets as inherited from spec.json
    '''
    for _ in range(100):
        listItems = []
        for colWidth in metadata_dict.values():
            listItem = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(int(colWidth))])
            listItems.append(listItem)
        rows.append(listItems)

    fixed_width_file_path = os.path.join(sys.path[0], "fixed_width_file")
    fixed_width_file_obj = open(fixed_width_file_path, "w", encoding=fWidthEncoding)
    for row in rows:
        ''' A padding of "two" spaces to the right every list item '''
        fixed_width_row_item = "  ".join(map(str,row))
        fixed_width_file_obj.write(fixed_width_row_item + '\n')

    return(fixed_width_file_path)

if __name__ == '__main__':

    '''
    Read spec.json file and create a JSON object
    '''
    with open(os.path.join(sys.path[0], "spec.json"), "r") as spec_file_obj:
        jsonObj = json.load(spec_file_obj)

    '''
    Generate a fixed-width file with randomized data using "FixedWidthEncoding" 
    provided in spec.json file. The function returns the path where the fixed 
    width file is written
    '''
    fixed_width_file_at_path = gen_fixed_width_file(jsonObj['ColumnNames'], jsonObj['Offsets'], jsonObj['FixedWidthEncoding'])
    
    '''
    Create a csv from the fixed-width file in the same path
    with "DelimitedEncoding" provided in spec.json file
    '''
    fixed_width_to_csv(jsonObj['ColumnNames'], jsonObj['Offsets'], fixed_width_file_at_path, jsonObj['FixedWidthEncoding'], jsonObj['DelimitedEncoding'] )
    
