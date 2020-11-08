def humanFormat(num):
    # From https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def __groupByList(input_list, key) -> dict:

    group_by = {}

    for item in input_list:
        
        entity = item[key]

        if entity not in group_by:
            group_by[entity] = []
        
        group_by[entity].append(item)
    
    return group_by


def groupBy(collection, key) -> dict:
    if isinstance(collection, list):
        return __groupByList(collection, key)
    else:
        raise NotImplementedError


def categorySummary(reports) -> dict:

    category = reports[0]["haku_name"]
    num_reports = len(reports)

    expenses = []
    
    category_expenses = 0.0
    highest_expense = 0.0

    for report in reports:

        summary = reportSummary(report)
        report_expenses = summary["expenses"]

        if report_expenses > highest_expense:
            highest_expense = report_expenses

        category_expenses += report_expenses
        expenses.append(report_expenses)

    category_html = f"categories/{reports[0]['haku_id']}/index.html"

    return {
        "category_name": category,
        "num_reports": num_reports,
        "expenses": expenses,
        "category_expenses": category_expenses,
        "average_expense": category_expenses/len(reports),
        "highest_expense": highest_expense,
        "onClick_destination": category_html
    }


def reportSummary(report) -> dict:

    name = report["project_name"]
    organizer = report["organization_name"]

    report_expenses = 0.0

    for item in report["loppuselvitys_answers"]["value"]:
        key = item["key"]
        value = item["value"]

        if "costs" in key and ".amount" in key:

            if value == "" or value == " ":
                value = 0.

            report_expenses += float(value)

    return {
        "name": name,
        "organizer": organizer,
        "expenses": report_expenses
    }
