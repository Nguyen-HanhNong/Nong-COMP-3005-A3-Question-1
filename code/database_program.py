# Student Number: 101220611
# Name: Nguyen-Hanh Nong
# COMP 3005 - Assignment 1 - Question 1
# Purporse: Contains the application implementation to connect to the database.

# Importing necesssary libraries
import psycopg2
import dotenv
import os
import datetime

# Load the environment variables in the .env and then store them in Python variables
dotenv.load_dotenv()

database_name = os.getenv('DATABASE')
host = os.getenv('HOST')
user = os.getenv('USER')
postgres_password = os.getenv('PASSWORD')
postgres_port = os.getenv('PORT')

# Connect to the database using the .env environment variables
conn = psycopg2.connect(database=database_name, host=host, user=user, password=postgres_password, port=postgres_port)

cursor = conn.cursor()

# Function that gets all the students stored in the database and then prints a formatted output   of those students to the console/database
def getAllStudents():
  # Made sure the select statement for the students is sorted by the primary key
  sql_statement = '''SELECT * FROM students ORDER BY students.student_id;'''
  sql_columns_names_statement = '''SELECT column_name FROM information_schema.columns WHERE table_name = 'students' '''

  cursor.execute(sql_statement) 
  students = cursor.fetchall()
  conn.commit()
  
  # Getting the column names from the student table in the DBMS
  cursor.execute(sql_columns_names_statement)
  columns_name = cursor.fetchall()
  conn.commit()

  # Formatting the column names at the top of the output to look nice
  print("\n")
  for column in columns_name:
    print(f"{column[0]} ", end='')
  print("")
  print(f"_____________________________________________________________________________")

  # Extracting all the data from the tuples and formatting it to look nice in output
  for student in students:
    for property in student:
      # Handles formatting of DATE objects from PostgreSQL
      if type(property) is datetime.date:
        property = property.strftime("%Y-%m-%d")
      # Handles null date values in the database
      if property is None:
        property = "NULL"
      print(f"{property} ", end='')
    print(f"\n")
  print(f"\n \n")

# Function that adds a new student to the database using the first_name, last_name, email and enrollment_date properties.
def addStudent(first_name, last_name, email, enrollment_date):
  # Use insert statement to add a new row to the students table
  sql_statement = '''INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);'''
  cursor.execute(sql_statement, (first_name, last_name, email, enrollment_date))
  conn.commit()
  print("The addStudent function has executed successfully.") 

# Function that updates a specific student's email with a new email
def updateStudentEmail(student_id, new_email):
  # Use the UPDATE statement to update a value already inserted in the table using the student_id passed into the function
  sql_statement = f'''UPDATE students SET email = '{new_email}' WHERE student_id = {student_id}'''
  cursor.execute(sql_statement)
  conn.commit()
  print("The updateStudentEmail function has executed successfully.") 

# Function to delete a student using a specific student id
def deleteStudent(student_id):
  # Use the DELETE statement to delete a row in the students table
  sql_statement = f'''DELETE FROM students WHERE student_id = {student_id};'''
  cursor.execute(sql_statement)
  conn.commit()
  print("The deleteStudent function has executed successfully.") 

# Create a loop until the user wants to exit the program
while True:
  # Display a list of options the user can take in the console/terminal
  user_input = input("""
        Here are the following options, type 1, 2, 3, 4 or 5 for the following options:

        1) getAllStudents(): Retrieves and displays all records from the students table.
        2) addStudent(first_name, last_name, email, enrollment_date): Inserts a new student record into the students table.
        3) updateStudentEmail(student_id, new_email): Updates the email address for a student with the specified student_id.
        4) deleteStudent(student_id): Deletes the record of the student with the specified student_id.
        5) Exit the loop and end the program \n
        """)
  
  # Calling the getAllStudents function to print out all the students in the database to the terminal/console
  if user_input == "1":
    getAllStudents()
    continue
  
  # Getting user input for the first_name, last_name, email, and enrollment_date properties and then calling the addStudent function to add the student to the database.
  if user_input == "2":
    first_name = input("What is the new student's first name? ")
    last_name = input("What is the new student's last name? ")
    email = input("What is the new student's email? ")
    enrollment_date = input("What is the new student's enrollment_date (YYYY-MM-DD)? ")

    # Check if the fields are non-empty and the date is in the right format, if it isn't, then the addStudent function will not execute.
    if not first_name or not last_name or not email:
      print("ERROR: One of your fields is empty, so the query will not go through.")
    else:
      # If the enrollment_date was empty the user, we want to insert NULL into the database
      if not enrollment_date:
        addStudent(first_name, last_name, email, None)
        continue
      else:
        # Check if the enrollment_date was formatted correctly, if it's not, then print an error message and do not insert a new user
        try: 
          proper_format = datetime.datetime.strptime(enrollment_date, "%Y-%m-%d")
        except ValueError:
          print("ERROR: The date field is not in the right format. It needs to be in YYYY-MM-DD. The query will not go through.")
        else:
          addStudent(first_name, last_name, email, enrollment_date)
          continue
    
  # Getting the user input for the student_id and the new_email and then calling the updateStudentEmail function to update the specific student's email.
  if user_input == "3":
    student_id = input("What is the student_id of the student you want to update the email of? ")
    new_email = input("What is the new email? ")

    # Check if the fields are non-empty and the student_id is a valid number, if it isn't, then the updateStudentEmail function is not called. 
    if not student_id or not new_email:
      print("ERROR: One of your fields is empty, so the query will not go through.")
    elif student_id.isnumeric() is False:
      print("ERROR: The student_id you inputted is not a number, so the query will not go through.")
    else:
      updateStudentEmail(int(student_id), new_email)
      continue

  # Getting the user input for the student_id and then calling the deleteStudent function to delete the specific student from the database
  if user_input == "4":
    student_id = input("What is the student_id of the student you want to delete? ")

    # Check if the student_id is nonempty and the student_id is a valid number, if it isn't, then the deleteStudent function is not called. 
    if not student_id:
      print("ERROR: The student_id input is empty, so the query will not go through.")
    elif student_id.isnumeric() is False:
      print("ERROR: The student_id you inputted is not a number, so the query will not go through.")
    else:
      deleteStudent(int(student_id))
      continue

  # Closing the connection to the database and then exiting the while loop, thus exiting the program.
  if user_input == "5":
    conn.close()
    break