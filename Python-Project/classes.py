from datetime import datetime


class Employee:
    """
        A class used to represent Employee

    ...
        Attributes
        ----------
        ID : int
        name : str
        birthDate : str
        maritalStatus : str
        children : int
        gender : str
        contact : str
        e_type : str
            academic or administrative
        department : str
        start_date : str
        basicSalary : int
        Insurance : bool
        Methods
        -------
        final_salary(self)
            returns the final salary according to the provided equation
        """
    fullTimeCount: int = 0
    maleCount: int = 0
    femaleCount: int = 0
    academicCount: int = 0
    administrativeCount: int = 0

    def __str__(self):
        self.tokens[1] = ", ".join([elem.strip(",") for elem in self.tokens[1].split(" ")])
        return "; ".join(self.tokens)

    def __init__(self, tokens):
        """
        Parameters
        ----------
        tokens : list containing all attributes
        """
        self.tokens = tokens
        if len(tokens[0]) != 5 or not tokens[0].isdigit():
            raise AttributeError("Invalid ID")
        else:
            self.ID = int(tokens[0])
        if tokens[1] != '' and all(ch.isalpha() or ch.isspace() for ch in tokens[1]):
            self.name = tokens[1]
        else:
            raise AttributeError("Invalid Name")

        if tokens[3].lower() in {"single", "married"}:
            self.maritalStatus = tokens[3]
        else:
            raise AttributeError("Invalid Martial Status")
        if tokens[5].lower() in {"male", "female"}:
            self.gender = tokens[5]
        else:
            raise AttributeError("Invalid Gender")
        if tokens[7].lower() in {"academic", "administrative"}:
            self.e_type = tokens[7]
        else:
            raise AttributeError("Invalid Employee type")
        if tokens[8].lower() in {"full-time", "part-time", "left-university"}:
            self.status = tokens[8]
        else:
            raise AttributeError("Invalid Status")

        self.Insurance = True if tokens[12].lower() == "true" else False
        self.birthDate = datetime.strptime(tokens[2], "%d/%m/%Y")
        if self.birthDate > datetime.today():
            raise AttributeError("Birthdate is in the future")

        if tokens[4].isdigit():
            self.children = int(tokens[4])
        else:
            raise AttributeError("Invalid Children")
        self.contact = tokens[6]
        self.department = tokens[9]
        self.start_date = datetime.strptime(tokens[10], "%m/%Y")
        if self.start_date > datetime.today():
            raise AttributeError("Start-date is in the future")
        if tokens[11].isdigit():
            self.basicSalary = int(tokens[11])
        else:
            raise AttributeError("Invalid Salary")

        if self.status.lower() == "full-time":
            Employee.fullTimeCount += 1
        if self.gender.lower() == "male":
            Employee.maleCount += 1
        else:
            Employee.femaleCount += 1
        if self.e_type.lower() == "academic":
            Employee.academicCount += 1
        else:
            Employee.administrativeCount += 1

    def final_salary(self):
        """ Print the final salary of employee according to an equation
        Equation -> Final salary = basic salary + 20 if the marital status is married + 15*number of children – 12 *
         (1 + (1 + number of children) if marital status is married and joint the health insurance)

        :return: Final Salary
        """
        salary = self.basicSalary + 15 * self.children - 12
        if self.maritalStatus.lower() == "married":
            salary += 20
            if self.Insurance:
                salary -= 12 * (1 + self.children)
        return salary


class Academic(Employee):
    """
        A class used to represent academic employee

    ...
        Attributes
        ----------
        file_name : str
            the name of the file containing the academic attributes
        experience : dict
            dictionary containing employee given courses in given semesters
        Methods
        -------
        __loadFile(file_name)
            loads employee academic attributes from file
        """

    courses = dict()


    def __init__(self, tokens, file_name):
        super().__init__(tokens)
        self.experience = dict()
        self.__loadFile(file_name)

    def __loadFile(self, file_name):
        file_name.seek(0)
        lines = file_name.readlines()
        for line in lines:
            tokens = [elem.strip() for elem in line.split("; ")]
            try:
                if int(tokens[0]) == self.ID:
                    self.experience[tokens[2] + "-" + tokens[1]] = [elem.strip() for elem in tokens[3].split(" ")]
            except Exception as e:
                print(e)


class Administrative(Employee):
    """
        A class used to represent administrative employee

    ...
        Attributes
        ----------
        file_name : str
            the name of the file containing the administrative attributes
        vacations : dict
            dictionary containing employee vacations in given year
        Methods
        -------
        __loadFile(file_name)
            loads employee administrative attributes from file
        """

    def __init__(self, tokens, file_name):
        super().__init__(tokens)
        self.vacations = dict()
        self.__loadFile(file_name)

    def __loadFile(self, file_name):
        file_name.seek(0)  # Resets the pointer to the start of the file
        lines = file_name.readlines()
        for line in lines:
            tokens = [elem.strip() for elem in line.split("; ")]
            try:
                if int(tokens[0]) == self.ID:
                    self.vacations[tokens[1]] = int(tokens[2])
            except Exception as e:
                print(e)
