from flask import Flask, render_template, request
import pprint
import datetime
import time
import jinja2
from people import employees
from schedules import schedules
from useful_functions import schedule_update_day
from hourly_wages import hourly_wages
import calendar
from calendar import monthrange
app = Flask(__name__)


@app.route('/')
@app.route('/emplist',  methods=["GET","POST"])
def emp_list_get() -> str:
    #ID will be added from sql, once it is connected to the project.

    #check to see whether this is an update or insert request (from empdetails or empadd)

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
        hourly_wages[emp_id] = int(request.form['hourly_wage'])

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
        hourly_wages[i] = int(request.form['hourly_wage'])

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
    sel_schedule = {}
    sel_employee = employees['records'][emp_id]
    #INIT VARIABLES
    updated_sched_data = {}
    logger = []

    #PROCESS POST REQUEST
    if request.method == "POST":

        #CHECK FOR 'date' VALUE IN REQUEST FORM

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
        if "day" in request.form and request.form['day']:

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

                    if i in schedules['employees'][emp_id][sel_year][sel_month]: #CHECK if selecte day in month

                        schedules['employees'][emp_id][sel_year][sel_month][i].update(schedule_update_day(i, request)) #UPDATE selected day with prepared request data

                    elif i not in schedules['employees'][emp_id][sel_year][sel_month] and i: #IF selected day not in month and truthy

                        schedules['employees'][emp_id][sel_year][sel_month].update({i:schedule_update_day(i, request)}) #UPDATE month with selected day containing prepared request data

                elif sel_month not in schedules['employees'][emp_id][sel_year] and sel_month: #IF selected month not in schedule and truthy

                    schedules['employees'][emp_id][sel_year].update({sel_month: { i: schedule_update_day(i, request) }}) #UPDATE year with selected month containing selected day with prepared request data

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


    time_worked_all = { #time_worked_all created as empty dictionary with 'employees' key
        'employees':{}
    }
    err = ""
    now = datetime.datetime.today()
    current_date = datetime.datetime.today().strftime("%m/%d/%Y")
    prior = datetime.datetime.today() - datetime.timedelta(days= 7)
    prior_date = prior.strftime("%m/%d/%Y")
    start_year = now.year
    start_month = now.month
    start_month_abbr = calendar.month_abbr[start_month]
    start_day = now.day - 7

    end_year = now.year
    end_month = now.month
    end_month_abbr = calendar.month_abbr[end_month]
    end_day = now.day



    if request.method == "POST":

        if 'daterange' in request.form:#checks for daterange in request
            date_start = datetime.datetime.strptime(request.form['daterange'][0:10], "%m/%d/%Y")
            date_end = datetime.datetime.strptime(request.form['daterange'][13:23], "%m/%d/%Y")



            start_year = date_start.year
            start_month = date_start.month
            start_month_abbr = calendar.month_abbr[start_month]
            start_day = date_start.day




            end_year = date_end.year
            end_month == date_end.month
            end_month_abbr = calendar.month_abbr[end_month]
            end_day = date_end.day
    #PREPARE time_worked_all variables for each entry in employees['records']:


    for records, employee_ids in employees.items(): #From the employees['records'] dict...

        for employee, data in employee_ids.items():  #For each employee id from employee records...
            #extract data and add to time_worked_all as a separate entry...
            full_name = data['name'] + " " + data['last_name'] #combine the first and last name from the record
            employee_id = data['id'] #retrieve employee id
            role = data['role'] #retrieve his role

            for id in hourly_wages: #Go through id's in hourly_wages
                if employee_id == id: #check if any equals the employee's id
                    hourly_wage = hourly_wages[employee_id] #assign as his hourly_wages in the time_worked_all entry

            #check if employee has a schedule entry in schedules
            #confirm fully that employee exists, and that the day for payroll exists
            if employee_id in schedules['employees']:

                 #set total hours worked(for later?)
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
                #STOPS WORKING HERE
                for y in range(start_year, (end_year+1)):
                    if y in schedules['employees'][employee_id]:
                        time_worked_all['employees'][employee_id]['time_worked'].update({y:{}})
                        for m in range(start_month, (end_month + 1) ):
                            if m in schedules['employees'][employee_id][y]:
                                time_worked_all['employees'][employee_id]['time_worked'][y].update({m:{}})
                                for d in range(start_day, (end_day + 1)):
                                    if d in schedules['employees'][employee_id][y][m]:
                                        time_worked_all['employees'][employee_id]['time_worked'][y][m].update(
                                            {
                                                d:{
                                                    'hours_worked':schedules['employees'][employee_id][y][m][d]['hours_worked'],
                                                    'payroll': schedules['employees'][employee_id][y][m][d]['hours_worked'] * hourly_wage
                                                }

                                            }
                                        )
                                        time_worked_all['employees'][employee_id]['total_hours_worked'] += time_worked_all['employees'][employee_id]['time_worked'][y][m][d]['hours_worked']
                                        time_worked_all['employees'][employee_id]['total_payroll'] += time_worked_all['employees'][employee_id]['time_worked'][y][m][d]['payroll']
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass




    return render_template('timeworked.html', time_worked_all = time_worked_all, the_title="Time Worked Page", current_date = current_date, prior_date = prior_date, err= err, start_month= start_month, end_month=end_month, start_day=start_day, end_day = end_day, start_month_abbr = start_month_abbr, end_month_abbr = end_month_abbr)






app.run(debug="True")
