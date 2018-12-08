from flask import Flask, render_template, request
import pprint
import datetime
import time
import jinja2
from people import employees
from schedules import schedules
from useful_functions import schedule_update_day
from useful_functions import generate_days_schedule
from hourly_wages import hourly_wages
import calendar
from calendar import monthrange
app = Flask(__name__)


@app.route('/')
@app.route('/emplist',  methods=["GET","POST"])
def emp_list_get() -> str:
    #ID will be added from sql, once it is connected to the project.

    #check to see whether this is an update or insert request (from empdetails or empadd)


    try:
        if request.method == 'POST':
            emp_id = int(request.form['employee_id'])
            employees['records'][emp_id].update(
                {
                    'name': request.form['first_name'],
                    'last_name': request.form['last_name'],
                    'email': request.form['email'],
                    'phone': request.form['phone'],
                    'role': request.form['role']
                }
            )
            hourly_wages[emp_id] = float(request.form['hourly_wage'])
    except:
        pass

    return render_template(
                            "emplist.html",
                            the_title="Title page here!",
                            the_employees=employees
                            )


#Temporary route without sql?
@app.route('/emplistadd', methods=['GET','POST'])
def emp_list_add() -> str:

    if request.method == 'POST':
        i = 0
        while i in employees['records']:
            i += 1


        employees['records'].update(
                {
                    i: {
                        'id':i,
                        'name': request.form['first_name'],
                        'last_name': request.form['last_name'],
                        'email': request.form['email'],
                        'phone': request.form['phone'],
                        'role': request.form['role']
                    }
                }
            )
        hourly_wages[i] = float(request.form['hourly_wage'])

    return render_template("emplist.html", the_employees=employees)

@app.route('/empadd')
def emp_add() ->str:

    return render_template("empadd.html", the_title="Create an Employee")

@app.route('/empdetails/<id>')
def emp_details(id) -> str:

    #assign id parameter to emp_id variable
    emp_id =  int(id)
    #from employees records table get object with id that equals emp_id variable
    sel_employee = employees['records'][emp_id]

    hourly_wage = hourly_wages[emp_id]


    return render_template("empdetails.html", emp = sel_employee, hourly_wage=hourly_wage)
    #"This is the employee details page, accessible when clicking the
    #details button on the emp entry. It may also list employee's working hours."


@app.route('/scheduleinfo/<id>', methods=["GET", "POST"])
def schedule_info(id) -> str:
    #consider using object.setdefault("key", "value")

    #GET EMPLOYEE BY ID
    emp_id = int(id)
    now = datetime.datetime.today()
    #SET DEFAULTS
    current_month = now.month
    current_year = now.year
    sel_year = current_year
    sel_month = current_month
    month_len = monthrange(2018, sel_month)[1] + 1
    sel_schedule = {}
    sel_employee = employees['records'][emp_id]
    #INIT VARIABLES
    updated_sched_data = {}
    logger = []

    #PROCESS POST REQUEST
    if request.method == "POST":

        #CHECK FOR 'date' VALUE IN REQUEST FORM
        try:

            if "date" in request.form:

                #PROCESS 'date' VALUE THROUGH datetime
                full_date_converted = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d")

                #ASSIGN datetime VALUES TO VARIABLES
                sel_year = full_date_converted.year
                sel_month = full_date_converted.month
                sel_day = full_date_converted.day

                #PREPARE REQUEST DATA FOR SELECTED DAY
                updated_sched_data = schedule_update_day(sel_day, request)

            #IF NO DATE IN REQUEST FORM
            if "day" in request.form and request.form['day']  and int(request.form['day']) <= month_len and int(request.form['day']) >=1:

                #GET 'month' & 'day' FROM REQUEST FORM
                sel_month = int(request.form['selmonth'])
                sel_day = int(request.form['day'])
                updated_sched_data = schedule_update_day(sel_day, request)
                #logger.append("day's value is {}".format(type(request.form['day'])))

                if 'bulk_days' is not None and 'bulk_days' in request.form:

                    bulk_days = int(request.form['bulk_days'])
                else:

                    bulk_days = sel_day

                #COMPARE if selected day is larger than "apply to" bulk days
                if bulk_days < sel_day:

                    begin = bulk_days
                    end = sel_day
                #SET selected day to be end range if "apply to" bulk days is smaller
                else:
                    begin = sel_day
                    end = bulk_days

                for i in range(begin, (end + 1)):

                    if sel_month in schedules['employees'][emp_id][sel_year]:
                        #CHECK if selected day in month
                        if i in schedules['employees'][emp_id][sel_year][sel_month]:
                            #UPDATE selected day with prepared request data
                            schedules['employees'][emp_id][sel_year][sel_month][i].update(schedule_update_day(i, request))
                            #IF selected day not in month and truthy
                        elif i not in schedules['employees'][emp_id][sel_year][sel_month] and i:
                            #UPDATE month with selected day containing prepared request data
                            schedules['employees'][emp_id][sel_year][sel_month].update({i:schedule_update_day(i, request)})
                            #IF selected month not in schedule and truthy
                    elif sel_month not in schedules['employees'][emp_id][sel_year] and sel_month:
                            #UPDATE year with selected month containing selected day with prepared request data
                        schedules['employees'][emp_id][sel_year].update({sel_month: { i: schedule_update_day(i, request) }})

            #Display current month
            else:
                pass

            #GENERATE schedule and SET month length if no value in quick schedule add.

            sel_month = int(request.form['selmonth'])
            month_len = monthrange(2018, sel_month)[1] + 1

            #Obtain hours worked value from fields that have those

            for i in range(1, month_len):
                hrs_worked_instance = "hours_worked_" + str(i)
                if (hrs_worked_instance) in request.form and (request.form[hrs_worked_instance]):
                    #logger.append("hours worked in day {}: {} . Type of value is {}".format(i, request.form[hrs_worked_instance], type(request.form[hrs_worked_instance]) ) )
                    #Schedule should already be present in this case, no need to confirm
                    sel_day = int(i)
                    schedules['employees'][emp_id][2018][sel_month][sel_day].update({
                        "hours_worked": int(request.form[hrs_worked_instance])
                    })


            if sel_month in schedules['employees'][emp_id][2018]: #IF sel_month is in schedules
                sel_schedule = schedules['employees'][emp_id][2018][sel_month]
            else:
                sel_schedule = {}



            return render_template(
                "scheduleinfo.html",
                the_title="Schedule Info page",
                emp = sel_employee,
                sched = sel_schedule,
                sel_month=sel_month,
                month_len = month_len,
                logger=logger
            )

        except:
            return render_template(
                "scheduleinfo.html",
                the_title="Schedule Info page",
                emp = sel_employee,
                sched = sel_schedule,
                sel_month = current_month,
                month_len = month_len + 1
            )
    if request.method == "GET":
        #DEFAULTS
        month_len = monthrange(2018, current_month)[1]


        if emp_id not in schedules['employees']: #IF employee does not have schedules

            schedules['employees'].update({ emp_id: { 2018:{ current_month:{} }  } }) #CREATE blank schedule for current month

        sel_schedule = schedules['employees'][emp_id][2018][current_month]

        if request.args.get("months"):

            sel_month = int(request.args.get('months')) #Assign req month to sel_month and count how many days are available in selected month
            month_len = monthrange(2018, sel_month)[1] + 1

            if sel_month in schedules['employees'][emp_id][2018]: #IF sel_month is in schedules

                sel_schedule = schedules['employees'][emp_id][2018][sel_month]

                return render_template(
                    "scheduleinfo.html",
                    the_title="Schedule Info page",
                    emp = sel_employee,
                    sched = sel_schedule,
                    sel_month = sel_month,
                    month_len = month_len,
                )
            else:
                #GET schedule from current month

                sel_schedule = {}

                return render_template(
                    "scheduleinfo.html",
                    the_title="Schedule Info page",
                    emp = sel_employee,
                    sched = sel_schedule,
                    sel_month = sel_month,
                    month_len = month_len,
                )

    return render_template(
        "scheduleinfo.html",
        the_title="Schedule Info page",
        emp = sel_employee,
        sched = sel_schedule,
        sel_month = current_month,
        month_len = month_len + 1
    )



@app.route('/schedulenew/<id>')
def schedule_new(id) -> str:

    emp_id = int(id)
    sel_employee = employees['records'][emp_id]

    return render_template(
        "schedulenew.html",
        the_title="schedule creation page",
        emp = sel_employee
    )

#add import csv functionality for mass schedule import?

@app.route('/schedulesall', methods=["GET", "POST"])
def show_time_worked_all() -> str:
    now = datetime.datetime.today() #SET sel variables if date exists in request form (wherever it came from)
    sel_year = now.year
    sel_month = now.month
    sel_day = now.day


    schedules_all = {     #SET time worked dict
    }

    #IF request method is "GET"
    #GET Schedules FROM all employees where date equals request (COMPREHENSION?)
    if request.method == "POST":
        if "date" in request.form:

            now = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d") #PROCESS 'date' VALUE THROUGH datetime

            #ASSIGN datetime VALUES TO VARIABLES
            sel_year = now.year
            sel_month = now.month
            sel_day = now.day

    for employee, years in schedules['employees'].items():
        #replace employee value with name & last_name from employee records' id
        employee = employees['records'][employee]['name'] + " " + employees['records'][employee]['last_name']
        for year, months in years.items():
            if year == sel_year:
                for month, days in months.items():
                    if month == sel_month:
                        for day, schedule in days.items():
                            if day == sel_day:
                                if schedules_all == {}: #if list empty upon day iteration create new list with employee schedule
                                    schedules_all.update(
                                        {
                                            year:{
                                                month:{
                                                    day:{
                                                        employee: schedule,
                                                    }
                                                }
                                            }
                                        }
                                    )
                                #for all other iterations, update the list
                                else:
                                    schedules_all[year][month][day].update({employee: schedule })


    return render_template(
    'schedulesall.html',
    the_title="Schedules For All Emplpyees",
    schedules_all = schedules_all,
    datenow = now
    )


@app.route('/timeworked', methods=["GET", "POST"])
def schedule_time_worked() -> str:

    time_worked_all = {
        'employees':{}
    }


    current_date = datetime.datetime.today().strftime("%m/%d/%Y")


    old_month_start_day = 0
    old_month_end_day = 0
    new_month_start_day = 0
    new_month_end_day = 0

    if request.method == "GET":

        now = datetime.datetime.today()

        prior = datetime.datetime.today() - datetime.timedelta(days= 6)
        prior_date = prior.strftime("%m/%d/%Y")


        if prior.year < now.year:
            start_year = prior.year
        else:
            start_year = now.year

        if prior.month != now.month:
            start_month = prior.month
        else:
            start_month = now.month

        start_day = prior.day
        start_month_abbr = calendar.month_abbr[start_month]

        end_year = now.year
        end_month = now.month
        end_month_abbr = calendar.month_abbr[end_month]
        end_day = now.day

        start_month_range = monthrange(start_year, start_month)


    if request.method == "POST":

        if 'daterange' in request.form:#checks for daterange in request
            date_start = datetime.datetime.strptime(request.form['daterange'][0:10], "%m/%d/%Y")
            date_end = datetime.datetime.strptime(request.form['daterange'][13:23], "%m/%d/%Y")

            start_year = date_start.year
            end_year = date_end.year

            start_month = date_start.month
            start_month_abbr = calendar.month_abbr[start_month]
            start_month_range = monthrange(start_year, start_month)

            start_day = date_start.day
            end_day = date_end.day

            end_month = date_end.month
            end_month_abbr = calendar.month_abbr[end_month]


            current_date = date_end.strftime("%m/%d/%Y")
            prior_date = date_start.strftime("%m/%d/%Y")


    for records, employee_ids in employees.items():

        for employee, data in employee_ids.items():

            full_name = data['name'] + " " + data['last_name']
            employee_id = data['id']
            role = data['role']

            for id in hourly_wages:
                if employee_id == id:
                    hourly_wage = hourly_wages[employee_id]


            if employee_id in schedules['employees']:

                time_worked_all['employees'].update(
                    {
                        employee_id:{
                            'full_name': full_name,
                            'role': role,
                            'hourly_wage': hourly_wage,
                            'time_worked':{},
                            'total_hours_worked': 0,
                            'total_payroll': 0
                        }
                    }
                )
                #Generate time_worked_all based on data provided

                time_worked_all['employees'][employee_id]['time_worked'].update({start_year:{}, end_year:{}} or {start_year:{}, end_year:{}})
                time_worked_all['employees'][employee_id]['time_worked'][start_year].update({start_month:{}} or {start_month:{}})
                time_worked_all['employees'][employee_id]['time_worked'][end_year].update({end_month:{}} or {end_month:{}})

                if start_year < end_year:

                    old_year = start_year

                    old_month_start = start_month
                    old_month_range = start_month_range
                    old_month_start_day = start_day
                    old_month_end_day = old_month_start_day + (start_month_range[1] - old_month_start_day)

                    new_month_start_day = 1

                    new_year = end_year
                    new_month_start = 1
                    new_month_end_day = end_day


                    #generate schedule for old year month
                    generate_days_schedule(
                        old_month_start_day,
                        old_month_end_day,
                        schedules,
                        time_worked_all,hourly_wage,
                        employee_id,
                        old_year,
                        old_month_start)

                    #generate schedule for new year month
                    generate_days_schedule(
                        new_month_start_day,
                        new_month_end_day,
                        schedules,
                        time_worked_all,hourly_wage,
                        employee_id,
                        new_year,
                        new_month_start)

                if start_year == end_year:

                    if start_month == end_month:
                        generate_days_schedule(
                            start_day,
                            end_day,
                            schedules,
                            time_worked_all,
                            hourly_wage,
                            employee_id,
                            start_year,
                            start_month)

                    elif start_month < end_month:

                        old_month_start_day = start_day
                        old_month_end_day = old_month_start_day + (start_month_range[1] - old_month_start_day)
                        new_month_start_day = 1
                        new_month_end_day = end_day




                        generate_days_schedule(
                            old_month_start_day,
                            old_month_end_day,
                            schedules,
                            time_worked_all,
                            hourly_wage,
                            employee_id,
                            start_year,
                            start_month)

                        generate_days_schedule(
                            new_month_start_day,
                            new_month_end_day,
                            schedules,
                            time_worked_all,
                            hourly_wage,
                            employee_id,
                            start_year,
                            end_month)
                else:
                    pass

            else:
                pass




    return render_template('timeworked.html',
                           start_month_range=start_month_range,
                           old_month_start_day = old_month_start_day,
                           old_month_end_day = old_month_end_day,
                           new_month_start_day = new_month_start_day,
                           new_month_end_day = new_month_end_day,
                           time_worked_all = time_worked_all,
                           the_title="Time Worked Page",
                           current_date = current_date,
                           prior_date = prior_date,
                           start_month= start_month,
                           end_month=end_month,
                           start_day= start_day,
                           start_year=start_year,
                           end_year=end_year,
                           end_day = end_day,
                           start_month_abbr = start_month_abbr,
                           end_month_abbr = end_month_abbr
                           )






app.run(debug="True")
