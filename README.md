# ONLINE JOB APPLICATIONS TRACKER
#### **Video Demo:**
https://youtu.be/jtNmx3cwz8c
#### **Description:**
#### **What will my software do?**
My web application acts as an online record of job applications that users have applied for.
#### **What features will it have?**
- Each user will log in to the web application using his/her own created username and password
- The web application will display a table of job applications that the user has applied for
- Each job application has the following information: Company, job title, job iD, URL, application date, status
- The job application table allows users to directly update all the information which will then be updated in the database
- To record a job application, the user needs to click a button called "Entry" on the navigation bar which will redirect them to another HTML page that contains required field to fill in. The newly added entry will be shown in the job application table
### **How will it be executed?**
It will be executed by typing "Flask run" in the terminal
#### **What new skills will I need to acquire?**
- I will need to learn how to use JSON to send data from the webpage to the Python app and update the SQLITE3 data accordingly
#### **What topics will I need to research?**
- How to create an interactive table on a web application
- How to send information entered by users to update the SQLITE3 database
#### **What might I consider to be a good outcome for my project?**
- New users are able to register their usernames and passwords
- Registered users are able to log in using their registered details
- After successfully logging in, users are able to view their previous job application correctly
- Registered users are able to add in a new job application
- Registered users are able to edit the content on the job application table
#### **What will I continue doing for my project?**
I am planning to add more features in the JobApps Tracker' Home and About buttons in the navigation bar, as well as to host it live on Heroku App
For the "Home" button in the navigation bar, I am going to include a pie chart and a bar chart to show how many percentage of job applications were sent to which employers, and how many job applications have been made in the past weeks respectively.
For the About button, I am planning to include a short description of why I came up with the JobApps Tracker as my final project.
#### **What files are there in my project?**
The JobApps Tracker's style is informal. Its background color is in blue color. The majority of texts in the application are made of dark blue color as well. My purpose of choosing the blue color is to make the users feel relax as the job search is itself stressful.
My project file has a typical structure of a Flask-based web application which includes a flask_session folder, static folder, templates folders, and some other files like app.py, applications.db, helpers.py, README.md, and requirements.txt
One of the most important files is app.py. It is where the backend was written in the Python language of the web application. app.py provides routes to all HTML pages that are saved in the templates folder based on the users' actions like clicking a button or submitting a form.
applications.db is an SQLITE3 database file that contains 2 tables, one of which is to keep a record of users' login information. The other table is to keep track of all job applications that have been entered or modified by the users. These entries are differentiated from one another by not only user_id but also row_id and data_id
The templates folder contains all HTML pages that are available on the web application. It starts from the layout.html page that lists out the basic components of the application, for example, the background, the navigation bar, etc. However, it also allows room for content modification using "{% block main %}{% endblock %}" and "{% block scripts %}{% endblock %}". The other web pages' content and logic are built upon these blocks.