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
