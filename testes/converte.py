import xlrd
import unicodecsv as csv

def csv_from_excel():
    wb = xlrd.open_workbook('Taco.xlsx')
    sh = wb.sheet_by_name('Plan1')
    your_csv_file = open('Taco.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL,  encoding='utf-8')

    for rownum in range(sh.nrows):
        colunas = sh.row_values(rownum)
        colunas2 =[int(colunas[0])] + colunas[1:] 
        wr.writerow(colunas2)

    your_csv_file.close()

# runs the csv_from_excel function:
csv_from_excel()