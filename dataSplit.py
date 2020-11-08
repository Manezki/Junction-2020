import json
from os import path as op

with open(op.join(op.dirname(__file__), "data", "applications_and_reports.json"), "r") as full_data:
    applications_and_reports = json.load(full_data, encoding="utf-8")

applications = applications_and_reports["haku"]
reports = applications_and_reports["loppuselvitys"]

del(applications_and_reports)

with open(op.join(op.dirname(__file__), "data", "applications.json"), "w", encoding="utf-8") as applications_fp:
    json.dump(applications, applications_fp, indent=4)

with open(op.join(op.dirname(__file__), "data", "reports.json"), "w", encoding="utf-8") as reports_fp:
    json.dump(reports, reports_fp, indent=4)
