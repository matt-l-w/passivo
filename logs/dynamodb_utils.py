def group_db_response_by_date_project(response):
    items = response['Items'] 

    projects_by_day = dict()
    for item in items:
        minutes = item['minutes']
        project = item['project']
        date = epoch_to_datetime_string(item['createdAt'])

        if date in projects_by_day.keys():
            minutes_by_project = projects_by_day[date]
            if project in minutes_by_project.keys():
                minutes_by_project[project] += int(minutes)
            else:
                minutes_by_project[project] = int(minutes)
        else:
            projects_by_day[date] = { project: int(minutes) }

    return projects_by_day

def epoch_to_datetime_string(epoch):
    from datetime import date

    return date.fromtimestamp(int(epoch/1000)).strftime("%x")