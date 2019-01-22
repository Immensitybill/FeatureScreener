from jira import JIRA
import re
import jira
import openpyxl

jiraDC = JIRA("https://jiradc.int.net.nokia.com", basic_auth=("bichen  ", "cbCB3921107"))

def get_all_records(JQL,fields,maxResults=5000):
    startAt = 0
    total = -1
    resultList = []
    while(startAt < total or total < 0):
        searchResult = jiraDC.search_issues(JQL, fields=fields,startAt=startAt,maxResults=maxResults)
        if(maxResults > searchResult.total):
            total = searchResult.total
        else:
            total = maxResults
        resultList.extend(searchResult)
        startAt = startAt + len(searchResult)
    return resultList

def get_FPB_records():
    fp_title="customfield_38703,"
    functional_discription="customfield_38704,"
    item_id="customfield_38702,"
    summary="summary,"
    JQL = "project = FPB AND issuetype = \"System Item\" AND status in (New, \"Approved for Dev\", \"Pre Analysis Ready\", \"Pre Analysis\") AND \"Planned System Release\" in (5G19, 5G19A, \"AirScale Cloud BTS 19\", \"AirScale Cloud SingleRAN 19\", \"AirScale RNC 19\",  \"Cloud BTS 19A\", \"FDD-LTE 19\", \"FDD-LTE 19A\", SBTS19, SBTS19A, \"SRAN 19\", SRAN19A, \"TD-LTE 19\", \"TD-LTE 19A\", \"TD-LTE 19ASP\", \"WCDMA 19\", \"FDD-LTE 19LF\")"
    system_item_fields = fp_title + functional_discription + item_id+summary
    system_items = get_all_records(JQL, system_item_fields)
    return system_items

def get_MEE_records(maxresults):
    JQL1 = "KEY=MEE-10024"
    JQL = "project = MEE AND issuetype = Sub-task"
    timeestimate = "timeestimate,"
    component = "components,"
    summary = "summary,"
    parent = "parent,"
    status = "status"
    fields = timeestimate + component + summary + parent + status
    mee_items = get_all_records(JQL, fields, maxResults=maxresults)
    return mee_items


def get_fields(items):
    result = {}
    for item in items:
        fields = dir(item.fields)
        for field in fields:
            if (re.match("__", field) == None):
                if field in result.keys():
                    result[field].append(getattr(item.fields, field))
                else:
                    result[field] = [getattr(item.fields, field)]
    return result

def write_to_excel(fields,head,filename):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(head)
    for row in fields:
        sheet.append(row)
    workbook.save(filename)

def get_fields_new(items):
    result = []
    for item in items:
        item_fields = []
        item_fields.append(item.key)
        fields = dir(item.fields)
        for field in fields:
            if (re.match("__", field) == None):
                item_fields.append( getattr(item.fields, field))
        result.append(item_fields)
    return result

def refine_mee_rows(fields):
    rows=[]
    for item_field_list in fields:
        print(item_field_list[0])
        if(len(item_field_list) < 6):
            continue
        refinedFields = []
        i = 0
        for field in item_field_list:
            if i == 1:
                components = ""
                for component in field:
                    components = components + component.name + " "
                refinedFields.append(components)
                i+=1
                continue
            if i == 2:
                refinedFields.append(field.key)
                i+=1
                continue
            if i == 3:
                refinedFields.append(field.name)
                i+=1
                continue
            refinedFields.append(field)
            i+=1
        rows.append(refinedFields)
    return rows

def main():
    # system_items = get_FPB_records()
    # fields = get_fields_new(system_items)
    # write_to_excel(fields,head=["keys", "item_id", "fp_title", "function_description", "sumary"],filename="FPB.xlsx")


    mee_items = get_MEE_records(maxresults=50000)
    fields = get_fields_new(mee_items)
    rows = refine_mee_rows(fields)
    write_to_excel(rows,head=["keys","component","parent","status","summary","timeestimate"],filename="mee.xlsx")


main()