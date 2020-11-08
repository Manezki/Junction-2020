from os import path as op
import json
from utils import humanFormat, groupBy, categorySummary

HEADER = """
    <html lang="en"><head>
    <meta charset="utf-8">
    <link href="styles/index.css" rel="stylesheet">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#000000">
    <meta name="description" content="OPH Avustusraportti visualisointi">
    <title>OPH Avustusraportti visualisointi</title>
  </head>
  <body>"""
PAGE_TITLE = """
  <div id="page-title">
    <h1>OPH Educational grants Dashboard</h1>
    <h2>Data aggregation demonstration for Junction 2020 - Janne Holopainen</h2>
    <p>OPH awards millions of euros in grants to different educational projects each year. Currently, it is difficult to keep an overview on how this money is spent and what its impact is. This simple dashboard is a step towards such an overview. It can be expanded to include more information about the projects, such as automated summaries and a rough indication of their success.</p>
  </div>
  <div id="main-container">"""
FOOTER = """
</div>
</body>
</html>"""


def generateCategoryArticle(category_summary) -> str:
    return f"""<article id="category" onClick="location.href='{category_summary["onClick_destination"]}'">
    <h3 id="title">{category_summary["category_name"]}</h3>
    <p id="num-reports">{category_summary["num_reports"]} reports</p>
    <p id="total-expenses">{humanFormat(category_summary["category_expenses"])} spent</p>
    </article>"""


if __name__ == "__main__":
    with open(op.join(op.dirname(__file__), "data", "reports.json"), "r") as reports_fp:
        reports = json.load(reports_fp)

    with open(op.join(op.dirname(__file__), "data", "applications.json",), "r") as file_fp:
        applications = json.load(file_fp)

    for report in reports:
        key = report["haku_id"]
        for application in applications:
            if application["id"] == key:
                name = application["content"]["name"]["fi"]
                break
        else:
            raise KeyError()

        report["haku_name"] = name

    with open(op.join(op.dirname(__file__), "index.html"), "w+") as index:
        index.write(HEADER)
        index.write(PAGE_TITLE)

        group_by_haku = groupBy(reports, "haku_name")

        category_summaries = [categorySummary(grouped_reports) for _, grouped_reports in group_by_haku.items()]
        category_summaries = sorted(category_summaries, key = lambda x: x["category_expenses"], reverse = True)

        for category_summary in category_summaries:
            index.write(generateCategoryArticle(category_summary))

        index.write(FOOTER)
