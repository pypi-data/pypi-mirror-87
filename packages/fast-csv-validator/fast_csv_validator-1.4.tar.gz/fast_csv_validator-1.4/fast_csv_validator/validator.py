#!/usr/bin/python
import re
import sys
import xlsxwriter
import os
from six.moves import urllib


def create_file(filename, row_seq):
    #create a file containing the rows
    file = open(filename, "w+")
    file.seek(0, 0)
    file.writelines(row_seq)


def create_summary_file(filename, table, number):
    workbook = xlsxwriter.Workbook(filename + '_summary.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.name = 'summary_with_pie_chart'
    bold = workbook.add_format({'bold': 1})
    # Add the worksheet data that the charts will refer to.
    headings = ['delimiter number', 'row count']
    key_list = list(table.keys())
    value_list = list(table.values())
    value_len = len(value_list)
    data = list()
    data.append(key_list)
    data.append(value_list)
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    # draw a pie chart
    chart1 = workbook.add_chart({'type': 'pie'})
    chart1.add_series({
        'name':       'pie ',
        'categories': [worksheet.name, 1, 0, value_len, 0],
        'values':     [worksheet.name, 1, 1, value_len, 1],
    })
    chart1.set_title({'name': 'delimiters occrrance pie'})
    chart1.set_style(10)
    worksheet.insert_chart('F2', chart1, {'x_offset': 25, 'y_offset': 10})
    workbook.close()


def validate():
    param = len(sys.argv)
    if param != 2:
        print("should accept a file as parameter")
        exit(1)
    else:
        url = sys.argv[1]
        if url.startswith('http'):
            filename = url.split('/')[-1]
            (filenamebase, extension) = os.path.splitext(filename)
            save_path = os.path.join(os.getcwd(), filename)
            urllib.request.urlretrieve(url, save_path)
            url = save_path
        else:
            (path, filename) = os.path.split(url)
            (filenamebase, extension) = os.path.splitext(filename)
    total = 0
    table = {}
    number = 0
    standard_seq = list()
    non_standard_seq = list()

    with open(url, 'r') as reader:
        for line in reader:
            total = total + 1
            occurances = re.findall(r'\,', line)
            count = len(occurances)
            if total == 1:
                number = count
            if count == number:
                standard_seq.append(line)
            else:
                non_standard_seq.append("line("+str(total) + ")\t" + line)
            if count in table:
                table[count] += 1
            else:
                table[count] = 1

    #print("the expected line delimiter number is %d"%number)
    if table[number] == total:
        print("All row is standard format")
    else:
        create_file(filenamebase + "_standard.csv", standard_seq)
        create_file(filenamebase + "_non_standard.csv", non_standard_seq)
        create_summary_file(filenamebase, table, number)
    print("expect delimiter number every row : %d" % number)
    print("total row number : %d" % total)
    print("[ delimiter number: row number ] %s" % table)


if __name__ == "__main__":
    validate()
