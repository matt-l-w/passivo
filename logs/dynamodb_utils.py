def group_db_response_by_date_project(response):
    items = response['Items'] 

    days = dict()
    for item in items:
        minutes = item['minutes']
        project = item['project']
        work_order = item['work_order']
        date = epoch_to_datetime_string(item['createdAt'])

        new_item = lambda minutes, wo: {'minutes': int(minutes), 'work_order': wo }

        if date in days.keys():
            projects = days[date]
            if project in projects.keys():
                projects[project]['minutes'] += int(minutes)
            else:
                projects[project] = new_item(minutes, work_order)
        else:
            days[date] = { project: new_item(minutes, work_order) }

    return days

def epoch_to_datetime_string(epoch):
    from datetime import date

    return date.fromtimestamp(int(epoch/1000)).strftime("%d/%m/%Y")
