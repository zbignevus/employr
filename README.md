<h1>Employr (working title)</h1>

This is a prototype of a project I am working on, which is an employee payroll application written in Python 3. Please be aware that it is still lacking authentication, many forms are missing type validations and the database is still not pushed to SQL, so at least make sure to provide strictly integers in the schedules hours/minutes.

Usage instructions:

1. Download and run the app.py with Python 3.
2. Open the Title page - this page contains the employee list, each entry containing name, last name, email and role and links to additional details and their schedule information.
3. Press the pencil icon under the actions column to access the employee details page, which also allows to modify the current employee information, including the role.
4. Press the calendar icon under the actions column to access the employee schedule information.
a) The quick schedule tool on the top of the page allows to quickly add new schedules for an employee. Input the day in the selected month and specify the times (start - end) as per the column description. Finally, you can bulk copy the schedule by selecting which days to apply this to from the specified day under "Apply until day" dropdown (bulk copy overrides existing schedule if it existed in specified range).
5. To view schedules assigned for a specified day for all employees, Press the "person with clock" icon on the top of the page.

6. To calculate the payroll for employees based on hours worked in a given range, press the "calendar with a checkmark" icon on the top of the page. Please keep in mind that the current prototype has the hours worked hardcoded in the schedules.py file under each employee's day schedules. 


If you have any further usage questions regarding the current prototype, please contact me at zbignevus@gmail.com
