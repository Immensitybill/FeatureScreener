import openpyxl

import dictionary_creater as dc



def write_to_excel(fields,head,filename):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(head)
    col = sheet.column_dimensions['A']
    col.number_format="General"
    for row in fields:
        sheet.append(row)
    workbook.save(filename)

str, df =dc.read_csv("fun_desc.csv")
data, count, dictionary, reversed_dictionary = dc.build_dataset(str,10000)
words = []
for k in reversed_dictionary.keys():
    words.append([reversed_dictionary[k]])
write_to_excel(words,[""],"dictory.xlsx")
re = dc.convertData2Index(df,dictionary)



print();