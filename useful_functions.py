def schedule_update_day(sel_day, request):
    return {
            "day": sel_day,
            "start_hours": int(request.form["start_hours"] or 0),
            'start_minutes': int(request.form["start_minutes"] or 0),
            '1break_start_hours': int(request.form['1break_start_hours']or 0),
            '1break_start_minutes':int(request.form['1break_start_minutes'] or 0),
            '1break_end_hours':int(request.form['1break_end_hours'] or 0),
            '1break_end_minutes': int(request.form['1break_end_minutes'] or 0),
            'lunch_start_hours': int(request.form['lunch_start_hours'] or 0),
            'lunch_start_minutes': int(request.form['lunch_start_minutes'] or 0),
            'lunch_end_hours': int(request.form['lunch_end_hours'] or 0),
            'lunch_end_minutes': int(request.form['lunch_end_minutes'] or 0),
            '2break_start_hours': int(request.form['2break_start_hours'] or 0),
            '2break_start_minutes': int(request.form['2break_start_minutes'] or 0),
            '2break_end_hours': int(request.form['2break_end_hours'] or 0),
            '2break_end_minutes': int(request.form['2break_end_minutes'] or 0),
            'finish_hours': int(request.form["finish_hours"] or 0),
            'finish_minutes': int(request.form["finish_minutes"] or 0)
            }


def generate_days_schedule(start,end, schedules,time_worked_all,hourly_wage,employee_id,y,m):
    for d in range(start, end+1):
        if d in schedules['employees'][employee_id][y][m]:
            #create the day iteration in time_worked_all and populate with data from before.
            time_worked_all['employees'][employee_id]['time_worked'][y][m].update(
                {
                    d:{
                        'hours_worked':schedules['employees'][employee_id][y][m][d].get('hours_worked', 0),
                        'payroll': schedules['employees'][employee_id][y][m][d].get('hours_worked', 0) * hourly_wage
                    }

                }
            )
            time_worked_all['employees'][employee_id]['total_hours_worked'] += time_worked_all['employees'][employee_id]['time_worked'][y][m][d]['hours_worked']
            time_worked_all['employees'][employee_id]['total_payroll'] += time_worked_all['employees'][employee_id]['time_worked'][y][m][d]['payroll']
        else:
            pass
