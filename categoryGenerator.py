from os import path as op
import json
from utils import humanFormat, groupBy, categorySummary, reportSummary
from indexGenerator import FOOTER
import os
import seaborn
from matplotlib import pyplot as plt

seaborn.set()

FORCE_REPLOT = True

# TODO Change title to match haku_name
CATEGORY_HEADER = """
    <html lang="en"><head>
    <meta charset="utf-8">
    <link href="../../styles/index.css" rel="stylesheet">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#000000">
    <meta name="description" content="OPH Avustusraportti visualisointi">
    <title>OPH Avustusraportti visualisointi</title>
  </head>
  <body>
"""

def titleGenerator(reports):
    return f"""
        <div id="page-title">
            <h1>{reports[0]["haku_name"]}</h1>
        </div>
        """


def summaryGenerator(reports):
    
    summary = categorySummary(reports)

    return f"""
    <div id="category-summary">
        <h2 id="title">Category summary</h2>
        <p id="average"><b>{humanFormat(summary["average_expense"])}</b> spent on average</p>
        <p id="max-spending"><b>{humanFormat(summary["highest_expense"])}</b> highest spending</p>
    </div>
    """


def generateExpensePlot(reports) -> None:

    summary = categorySummary(reports)

    expenses = summary["expenses"]
    expenses = sorted(expenses, reverse=True)

    fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8))

    ax.bar(range(0, len(expenses)), expenses)
    
    ax.set_title("Project spending in the category")
    ax.set_ylabel("Expenses (€)")
    ax.set_xlabel("Projects")
    
    ax.set_xticks([])

    fig.tight_layout()

    fig.savefig(op.join(op.dirname(__file__), "categories", f"{haku_id}", "images", "expenses.jpg"))
    plt.close(fig)


def projectGenerator(report_summary) -> str:

    if report_summary["name"] == "":
        project_name = " - "
    else:
        project_name = report_summary["name"]


    return f"""
    <article id="project-summary">
        <h3 id="organizer">{report_summary["organizer"]}</h3>
        <h4 id="project-name">Project name: {project_name}</h4>
        <p id="expenses">{humanFormat(report_summary["expenses"])} spent</p>
    </article>
    """


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


    grouped_reports = groupBy(reports, "haku_id")

    for haku_id, reports in grouped_reports.items():

        category_folder = op.join(op.dirname(__file__), "categories", "%s" % haku_id)

        if not op.exists(category_folder):
            os.mkdir(category_folder)
            os.mkdir(op.join(category_folder, "images"))


        with open(op.join(category_folder, "index.html"), "w+") as index:
            index.write(CATEGORY_HEADER)

            index.write(titleGenerator(reports))
            index.write(summaryGenerator(reports))

            if FORCE_REPLOT:
                generateExpensePlot(reports)

            index.write("""<div id="category-plot-container"><img src="images/expenses.jpg"
     alt="Uh oh, a plot is missing"
     width="750"
     height="500"></div>""")

            # TODO Plot

            index.write("""
            <div id="projects-container">
            <h2 id="title">Reports in the category</h2>
            """)

            summaries = [reportSummary(report) for report in reports]
            summaries = sorted(summaries, key = lambda x: x["expenses"], reverse = True)

            for summary in summaries:
                index.write(projectGenerator(summary))

            index.write("""</div>""")

            index.write(FOOTER)

