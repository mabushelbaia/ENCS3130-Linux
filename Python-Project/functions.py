import prettytable

from classes import *


def printEmployee(employeeList):
    """
    print a table containing all data about employees
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
    Returns:

    """

    table = prettytable.PrettyTable()
    table.field_names = ["ID", "NAME", "BIRTHDATE", "MARTIAL STATUS", "CHILDREN", "GENDER", "CONTACT",
                         "EMPLOYEE TYPE", "STATUS", "DEPARTMENT", "START DATE", "BASIC SALARY", "HEALTH INSURANCE",
                         "VACATIONS/EXPERIENCE", "DATA"]
    for item in employeeList.values():  # adding employees
        l1 = [item.ID, item.name, item.birthDate, item.maritalStatus, item.children, item.gender, item.contact,
              item.e_type, item.status, item.department, item.start_date, item.basicSalary, item.Insurance]
        l1 += ["Experience", item.experience] if isinstance(item, Academic) else ["Vacations", item.vacations]
        table.add_row(l1)
    second_table = [table.field_names[0]] + table.field_names[13:]  # cutting tables
    print(table.get_string(fields=table.field_names[0:13]))
    table.align["DATA"] = "l"  # left-alignment
    print(table.get_string(fields=second_table[0:]))


def salaryInformation(employeeList):
    """
    Print salary statistics
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
    Returns:

    """
    while True:
        try:
            salary = int(input("Enter Salary: "))  # Salary
            break
        except ValueError:
            print("ValueError: Enter an integer")

    table = prettytable.PrettyTable()
    table.field_names = ["NAME", "FINAL SALARY"]
    academic_salary = 0
    administrative_salary = 0
    for item in employeeList.values():
        if isinstance(item, Academic):
            academic_salary += item.final_salary()
        else:
            administrative_salary += item.final_salary()
        if item.final_salary() > salary:
            table.add_row([item.name, item.final_salary()])
    print("• Average academic employees’ salary: ", academic_salary / Employee.academicCount)
    print("• Average administrative employees’ salary: ", administrative_salary / Employee.administrativeCount)
    print(f"• Employees with salaries greater than {salary}: ")
    print(table)


def employeeInformation():
    """
    print static employee statistics
    Arguments:

    Returns:

    """
    print(
        "• Number of academic employees: ", Employee.academicCount,
        "\n• Number of administrative employees: ", Employee.administrativeCount,
        "\n• Percent of Full-time employees: ",
        Employee.fullTimeCount / (Employee.academicCount + Employee.administrativeCount),
        "%\n• Number of Male employees: ", Employee.maleCount,
        "\n• Number of Female employees: ", Employee.femaleCount
    )


def administrativeStats(employeeList):
    """
    print a table containing administrative attributes
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
    Returns:

    """
    table = prettytable.PrettyTable()
    table.field_names = ["NAME", "VACATIONS", "Average"]
    for employee in employeeList.values():
        if isinstance(employee, Administrative):
            if len(employee.vacations) == 0:
                table.add_row([employee.name, 0, 0])
            else:
                vacation_sum = sum(employee.vacations.values())
                average = "{:.2f}".format(vacation_sum / len(employee.vacations))
                table.add_row([employee.name, vacation_sum, average])
    print(table)


def academicStats(employeeList):
    """
    print a table containing academic attributes
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
    Returns:

    """
    table = prettytable.PrettyTable()
    table.field_names = ["NAME", "COURSES", "Average"]
    for employee in employeeList.values():
        if isinstance(employee, Academic):
            if len(employee.experience) == 0:
                table.add_row([employee.name, 0, 0])
            else:
                summation = 0
                for x in employee.experience.values():
                    summation += len(x)
                average = "{:.2f}".format(summation / len(employee.experience))
                table.add_row([employee.name, summation, average])
    print(table)


def courseStats(employeeList):
    for employee in employeeList.values():
        if isinstance(employee, Academic):
            for semester in employee.experience.values():
                for course in semester:
                    if course in Academic.courses.keys():
                        if employee.ID in Academic.courses[course].keys():
                            Academic.courses[course][employee.ID] += 1
                        else:
                            Academic.courses[course][employee.ID] = 1
                    else:
                        Academic.courses[course] = dict()
                        Academic.courses[course][employee.ID] = 1
    table = prettytable.PrettyTable()
    table.field_names = ["COURSE", "OFFERED TIMES", "TEACHERS"]
    for course in Academic.courses:
        table.add_row([course, sum(Academic.courses[course].values()), len(Academic.courses[course].values())])
    print(table)


def loadFile(attributes_file, experience_file, vacations_file):
    """
    load the data files into a dictionary of employees
    Arguments:
        attributes_file: file containing basic employee attributes
        experience_file: file containing academic employee attributes
        vacations_file: file containing administrative employee attributes
    Returns:
        employeeList: dictionary; key -> ID, Value -> Object
    """
    employeeList = {}
    lines = attributes_file.readlines()
    for line in lines:
        tokens = [elem.strip() for elem in line.split(';')]
        name = " ".join([elem.strip() for elem in tokens[1].split(',')])  # One line command to join the NAME
        tokens[1] = name  # Reassigning The new name to the EMPLOYEE list
        try:
            if tokens[0] not in employeeList.keys():
                if tokens[7].lower() == "academic":
                    employeeList[tokens[0]] = Academic(tokens, experience_file)
                elif tokens[7].lower() == "administrative":
                    employeeList[tokens[0]] = Administrative(tokens, vacations_file)
            else:
                print("Attribute Error: Employee already exists")
        except AttributeError as e:
            print(f"Attribute Error: {e}")
    return employeeList


def RetirementStats(employeeList):
    """
    print a table containing remaining years for all employees
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
    Returns:

    """
    today = datetime.today()
    table = prettytable.PrettyTable()
    table.field_names = ["NAME", "AGE", "S-YEARS", "Y-REMAINING"]
    for employee in employeeList.values():
        age = today.year - employee.birthDate.year
        serviceYears = today.year - employee.start_date.year
        if employee.status.lower() != "left-university":
            if age < 65 or serviceYears < 35:
                n = min(65 - age, 35 - serviceYears)
                table.add_row([employee.name, age, serviceYears, n])
    print(table)


def addEmployee(employeeList, experience_file, vacations_file):
    """
    add employee to the dictionary and load his data from experience and vacations file
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
        experience_file: file containing academic employee attributes
        vacations_file: file containing administrative employee attributes
    Returns:

    """
    print(
        "Employee ID; Name{First Name, Middle Name,Last Name}; Data of birth; Martial status; Number of children; "
        "Gender; Contact information {email, mobile number, fax}; Type; Status; Department; Starting Time; Basic "
        "Salary; health insurance"
    )
    line = input("Enter data according to the above format: ")
    tokens = [elem.strip() for elem in line.split(';')]
    if len(tokens) < 13:
        print("invalid data {Not all arguments are included}")
        return
    name = " ".join([elem.strip() for elem in tokens[1].split(',')])  # One line command to join the NAME
    if len(name) < 3:
        print("invalid data {full-name is required}")
        return
    tokens[1] = name  # Reassigning The new name to the EMPLOYEE list
    if tokens[0] in employeeList.keys():
        print("Employee exists")
        return
    try:
        if tokens[7].lower() == "academic":
            employeeList[tokens[0]] = Academic(tokens, experience_file)
        elif tokens[7].lower() == "administrative":
            employeeList[tokens[0]] = Administrative(tokens, vacations_file)
    except AttributeError as e:
        print(f"Attribute Error: {e}")


def updateEmployee(employeeList, experience_file, vacations_file):
    """
    update general employee attributes by deleting the employee and creating a new one with the same id
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
        experience_file: file containing academic employee attributes
        vacations_file: file containing administrative employee attributes
    Returns:

    """
    ID = input("Enter ID: ")

    if ID not in employeeList.keys():
        print("Employee doesn't Exist")
        return
    print(
        "Name{First Name, Middle Name,Last Name}; Data of birth; Martial status; Number of children; "
        "Gender; Contact information {email, mobile number, fax}; Type; Status; Department; Starting Time; Basic "
        "Salary; health insurance"
    )
    line = input("Enter data according to the above format: ")
    tokens = [elem.strip() for elem in line.split(';')]
    print(tokens)
    if len(tokens) < 12:
        print("invalid data {Not all arguments are included}")
        return
    tokens = [ID] + tokens
    name = " ".join([elem.strip() for elem in tokens[1].split(',')])  # One line command to join the NAME
    if len(name) < 3:
        print("invalid data {full-name is required}")
        return
    tokens[1] = name  # Reassigning The new name to the EMPLOYEE list
    try:
        temp = employeeList[tokens[0]]

        if tokens[7].lower() == "academic":
            employeeList[tokens[0]] = Academic(tokens, experience_file)
        elif tokens[7].lower() == "administrative":
            employeeList[tokens[0]] = Administrative(tokens, vacations_file)
        if temp.gender.lower() == "male":
            Employee.maleCount -= 1
        else:
            Employee.femaleCount -= 1
        if temp.status.lower() == "full-time":
            Employee.fullTimeCount -= 1
        if temp.e_type.lower() == "academic":
            Employee.academicCount -= 1
        else:
            Employee.administrativeCount -= 1
        del temp

    except AttributeError as e:
        print(f"Attribute Error: {e}")


def updateAcademic(employeeList):
    """
    update academic employee attributes by updating the dictionary containing employee data
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
    Returns:

    """
    option = input("Enter ID: ")
    if option not in employeeList.keys():
        print("Invalid ID")
        return
    if not isinstance(employeeList[option], Academic):
        print("Not Academic employee")
        return
    employee = employeeList[option]
    while True:
        year = input("Enter year or (q to Quit): ")
        if year.lower() == "q":
            break
        if len(year) != 4 or not year.isdigit():  # checks entered year
            print("Invalid Data")
            continue
        semester = input("Enter semester number (1, 2 or 3): ")
        if len(semester) != 1 or not semester.isdigit():  # checks semester
            print("Invalid Data")
            continue
        if int(semester) < 1 or int(semester) > 3:
            print("Invalid Data")
            continue
        if year + "-" + semester in employee.experience.keys():  # check if the data already exists
            print("Old data: ", employee.experience[year + "-" + semester])  # print old data
        courses = input("Enter courses seperated by comma or (q to Quit): ")
        if courses.lower() == "q":
            break
        elif all(course.strip().isalnum() for course in courses.split(",")):
            # check if all courses containing only AlphaNumeric characters
            courses_list = [course.strip() for course in courses.split(",")]
            if not courses_list:  # check if empty
                print("Invalid data")
                break
            employee.experience[year + "-" + semester] = courses_list  # update data
        else:
            print("Invalid Data")
            continue


def updateAdministrative(employeeList):
    """
    update administrative employee attributes by updating the dictionary containing employee data
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
    Returns:

    """
    option = input("Enter ID: ")
    if option not in employeeList.keys():  # check if he exists
        print("Invalid ID")
        return
    if not isinstance(employeeList[option], Administrative):  # check if administrative
        print("Not Administrative employee")
        return
    employee = employeeList[option]
    while True:
        year = input("Enter year or (q to Quit): ")
        if year.lower() == "q":
            break
        if len(year) != 4 or not year.isdigit():  # check year
            print("Invalid Data")
            continue
        if year in employee.vacations.keys():  # update or insert
            print("Old data: ", employee.vacations[year])
        vac = input("Enter number of vacations or (q to Quit): ")
        if vac.lower() == "q":
            break
        elif vac.isdigit():
            try:
                employee.vacations[year] = int(vac)
            except Exception as e:
                print(e)
        else:
            print("Invalid Data")
            continue


def StoreFiles(employeeList, attributes_file, experience_file, vacations_file):
    """
    store the data in the dictionary into the files
    Arguments:
        employeeList: dictionary key -> ID , Value -> Object
        attributes_file: file to save employees into
        experience_file: file to save academic attributes
        vacations_file: file to save administrative attributes
    Returns:

    """
    with open(attributes_file, "w") as f, open(experience_file, "w") as g, open(vacations_file, "w") as y:
        for emp in employeeList.values():
            if isinstance(emp, Administrative):
                for record in emp.vacations:
                    string = "; ".join([str(emp.ID), str(record), str(emp.vacations[record])]) + "\n"
                    y.write(string)
            elif isinstance(emp, Academic):
                for record in emp.experience:
                    string = "; ".join([str(emp.ID), record.split("-")[0], record.split("-")[1],
                                        " ".join([course.strip() for course in emp.experience[record]])]) + "\n"
                    g.write(string)
            emp = str(emp) + "\n"
            f.write(emp)
        f.close()
        g.close()
        y.close()
