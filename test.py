import json
import Questions

import submitDataToDB

with open('data.json') as json_file:
    information = json.load(json_file)
content = Questions.reportContent()
content.information = information
pdf = "F://reportQuery//input//access_to_justice_2018_final_report.pdf"

content.information["project_finance"]["PERIOD_START"].append("")
content.information["project_finance"]["PERIOD_START"].append("")
content.information["project_finance"]["PERIOD_END"].append("")
content.information["project_finance"]["PERIOD_END"].append("")

s = submitDataToDB.submitDataToDB()
s.submit(content, pdf)
s.close_connection()
