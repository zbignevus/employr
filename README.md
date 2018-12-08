<h1>Employr (working title)</h1>

This is a prototype of a project I am working on, which is an employee payroll application written in Python 3. Please be aware that it is still lacking authentication, many forms are missing type validations and the database is still not pushed to SQL, so at least make sure to provide strictly integers in the schedules hours/minutes.

<b>Usage instructions:</b>

1. Download and run the app.py with Python 3.
2. Open the Title page - this page contains the employee list, each entry containing name, last name, email and role and links to additional details and their schedule information.
3. Press the pencil icon under the actions column to access the employee details page, which also allows to modify the current employee information, including the role they have and their current hourly wage.
4. Press the calendar icon under the actions column to access the employee schedule information.
a) The quick schedule tool on the top of the page allows to quickly add new schedules for an employee. Input the day in the selected month and specify the times (start - end) as per each column description. Finally, you can bulk copy the schedule by selecting which days to apply this to from the specified day under "Apply until day" dropdown (bulk copy overrides existing schedule if it existed in the specified range).
5. You may view and edit the hours worked at a specified day under the "hours worked" column.
6. To view schedules assigned for a specified day for all employees, Press the "person with clock" icon on the top of the page.

7. To calculate the payroll for employees based on hours worked in a given range, press the "calendar with a checkmark" icon on the top of the page.


If you have any further usage questions regarding the current prototype, please contact me at zbignevus@gmail.com


<b>Recent changes:</b>

2018.10.13
  <i>
  *Added Try/Exception to validate quick schedule values for day field.

2018.10.10

Time Worked:
  <i>
  *Fixed key error when trying to view time worked for days that exist but have no hours specified yet.
  </i>

2018.10.09

Schedule Info:

  <i>
  *Fixed error when clicking "Add Schedule" in the quick schedule tool.
  *Added Time Worked Window - this is where you can view and specify the hours an employee has worked.
  *Improved logic to allow both time worked and quick schedule variables to operate on same POST method.
 </i>

2018.10.05

Employee Details:

  <i>*Hourly wages can now be dynamically assigned to each employee
  </i>
