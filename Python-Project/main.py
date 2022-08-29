from time import sleep

from functions import *

while True:  # checking the files
    attributes = input("Enter Attributes file: ")
    try:
        attributes_file = open(attributes, "r")
    except IOError:
        print("Couldn't access attributes file, try again.")
    else:
        break
while True:
    experience = input("Enter Experience file: ")
    try:
        experience_file = open(experience, "r")
    except IOError:
        print("Couldn't access experience file, try again.")
    else:
        break
while True:
    vacations = input("Enter Vacations file: ")
    try:
        vacations_file = open(vacations, "r")
    except IOError:
        print("Couldn't access vacations file, try again.")
    else:
        break
employeeList = loadFile(attributes_file, experience_file, vacations_file)  # loading the files

menu = "1. Add a new employee record\n" \
       "2. Update general attributes\n" \
       "3. Add/update administrative employee attribute\n" \
       "4. Add/update academic employee attribute\n" \
       "5. Employee’s statistics\n" \
       "6. Salary statistics\n" \
       "7. Retirement information\n" \
       "8. Courses statistics\n" \
       "9. Administrative employees’ statistics\n" \
       "10. Academic employees’ statistics\n" \
       "11. Employee List\n" \
       "12. Save data back to files\n" \
       "0. Exit \n"
print("\n" + menu)
option = input("Enter an option: ")
try:
    option = int(option)
except Exception as e:
    print(e)
# menu
while option != 0:
    if option == 1:
        addEmployee(employeeList, experience_file, vacations_file)
    elif option == 2:
        updateEmployee(employeeList, experience_file, vacations_file)
    elif option == 3:
        updateAdministrative(employeeList)
    elif option == 4:
        updateAcademic(employeeList)
    elif option == 5:
        employeeInformation()
    elif option == 6:
        salaryInformation(employeeList)
    elif option == 7:
        RetirementStats(employeeList)
    elif option == 8:
        courseStats(employeeList)
    elif option == 9:
        administrativeStats(employeeList)
    elif option == 10:
        academicStats(employeeList)
    elif option == 11:
        printEmployee(employeeList)
    elif option == 12:
        StoreFiles(employeeList, attributes, experience, vacations)
    else:
        print("INVALID OPTION")
    # sleep(1)  # to give the reader sometime to thinK :3
    print("\n" + menu)
    option = input("Enter an option: ")
    try:  # Exception to check if its an int
        option = int(option)
    except ValueError as e:
        print(e)
