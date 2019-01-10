from jira import JIRA
import jira
import openpyxl

jiraDC = JIRA("https://jiradc.int.net.nokia.com", basic_auth=("bichen", "cbCB3921106"))


def GetLinkedChildIssues(issue, fields=None):
    Children = []
    for issueLink in issue.fields.issuelinks:
        if hasattr(issueLink, "outwardIssue") and issueLink.type.outward == "is parent of":
            Children.append(jiraDC.issue(issueLink.outwardIssue.key, fields))
    return Children

def IsPlannedEntityReleaseIn(issue, release):
    if issue.fields.customfield_38725 is None:
        return False

    for pRelease in issue.fields.customfield_38725:
        if release == pRelease.value:
            return True
    return False


def IsPlannedSystemReleaseIn(issue, release):
    if issue.fields.customfield_38724 is None:
        return False

    for pRelease in issue.fields.customfield_38724:
        if release == pRelease.value:
            return True
    return False

def fillARow(entity, WebEM_CA, dependency=None):
    row = []
    row.append(entity.key)
    if entity.fields.customfield_38725 is not None and len(entity.fields.customfield_38725) > 0:
        row.append(entity.fields.customfield_38725[0].value)  # planned entity release
    else:
        row.append("")

    if entity.fields.customfield_38724 is not None and len(entity.fields.customfield_38724) > 0:
        row.append(entity.fields.customfield_38724[0].value)  # planned system release
    else:
        row.append("")
    row.append(entity.fields.customfield_38702)  # Item ID

    row.append(WebEM_CA.key)
    row.append(WebEM_CA.fields.status.name)
    row.append(WebEM_CA.fields.customfield_38694)  # start fb
    row.append(WebEM_CA.fields.customfield_38693)  # end fb
    if dependency is not None:
        row.append(dependency.key)
        if dependency.fields.customfield_38690 is not None:
            row.append(dependency.fields.customfield_38690.value)  # competence area
        else:
            row.append("")
        row.append(dependency.fields.status.name)
        row.append(dependency.fields.customfield_38694)  # start fb
        row.append(dependency.fields.customfield_38693)  # end fb
    return row

def main():
    JQL = "project = WEBEM AND assignee in (liangjew, zuhe, the)"
    Epic_Fields = "labels, components, customfield_31094, customfield_29791"
    CA_Fields = "status,issuelinks,customfield_29791,customfield_38690,customfield_38693,customfield_38694,customfield_38725,customfield_38724,customfield_38702"
    Entity_Fields = "customfield_38725,customfield_38724,customfield_38702,customfield_29791,issuelinks"
    WebEM_Epics = jiraDC.search_issues(JQL, startAt=0, maxResults=50, fields=Epic_Fields)

    Entities = []

    for epic in WebEM_Epics:
        WebEM_CA = jiraDC.issue(epic.fields.customfield_29791, fields=CA_Fields)
        Other_CAs = []
        Entity = jiraDC.issue(WebEM_CA.fields.customfield_29791, fields=Entity_Fields)

        for CA in GetLinkedChildIssues(Entity, CA_Fields):
            if CA.fields.customfield_38690 is not None:
                if CA.fields.customfield_38690.value != "MANO WEBEM":
                    Other_CAs.append(CA)
        Entities.append([Entity, WebEM_CA, Other_CAs])
    workbook = openpyxl.Workbook()
    sheet = workbook.create_sheet("WEBEM")
    sheet.append(["Entity","Entity Release","System Release","Entity Item ID",
                  "WEBEM CA", "WEBEM CA Status","WEBEM CA Start FB", "WEBEM CA End FB",
                  "Dependency", "Dependency CA","Dependency Status", "Dependency Start FB", "Dependency End FB"])
    for e in Entities:
        entity = e[0]
        WebEM_CA = e[1]
        if len(e[2]) == 0:
            row = fillARow(entity, WebEM_CA)
            sheet.append(row)
            print(row)
        else:
            for d in e[2]:
                row = fillARow(entity, WebEM_CA, d)
                sheet.append(row)
                print(row)
    workbook.save("D:\\work\\Projects\\Change Lead\\RetroAP\\WebEM Dependenceis.xlsx")


main()