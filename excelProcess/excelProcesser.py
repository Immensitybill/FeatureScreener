import openpyxl as excel

# 对于相同feature号的记录去重，同一个feature的多个记录，如果有某一条impact为1,则认为该feature对O&M UI有impact.
# 注意，5G feature用的是sub-feature, Others feature用的是feature
def main():
    wb = excel.load_workbook('others_other_tribe.xlsx')
    sheet = wb.active
    rows = list(sheet.rows)
    row_added = {}
    sub_featureIdx = 7
    featureIdex = 6
    impact_idx = 16
    new_rows = []
    for row in rows:
        subFeature = row[featureIdex].value
        impact = row[featureIdex].value
        if subFeature not in row_added.keys():
            row_added[subFeature] = row
            new_rows.append(row)
            continue
        else:
            if row_added[subFeature][impact_idx].value == impact:
                continue
            else:
                if impact == 1:
                    new_rows.remove(row_added[subFeature])
                    row_added[subFeature] = row
                    new_rows.append(row)
                    continue
                else:
                    continue

    all_row_content = []
    for row in new_rows:
        all_row_content.append(get_row_content(row))
    write_to_excel(all_row_content,[""],"others_other_tribe_result.xlsx")



def get_row_content(row):
    content=[]
    for cell in row:
        content.append(cell.value)
    return content



def write_to_excel(fields,head,filename):
    workbook = excel.Workbook()
    sheet = workbook.active
    sheet.append(head)
    for row in fields:
        sheet.append(row)
    workbook.save(filename)

main()


