#!/usr/bin/env python

# Python OOB
# Creating and instantiating classes 
# Allows us to logically group data and functions
# In the world of classes, data = attributes and functions = methods

# Class (blueprint for creating instances)
# Instance of a class (each employee will be instance of the class)

# Each employee will have it's own attribues and methods

# Instance variables: contain data unique to each instance

class Employee: # class is a blueprint
    def __init__(self, first, last, pay): # An example of a method within a class. Init is a special method as it initializes a class. A method automatically gets the instance (e.g. emp_1 or emp_2) as the first argument. This is referenced to as 'self'. Then you can specify the attribues of the instance that you want for the method. For example: first, last, email, pay. 
        self.first = first # These are instance variables that we are setting. Same as saying <instance>.<variable> = <value> (e.g. emp_1.first = 'Vineet')
        self.last = last # These are instance variables that we are setting. When emp_1 is passed to Employee class, the variables first, last, pay will be assigned the proper values.
        self.pay = pay # These are instance variables that we are setting
        self.email = first + '.' + last + '@yahoo.com' # we can construct email by using first and last variables

    def fullname(self): # Creating another method with class to perform some action. In this case, printing full name of employee.
        return '{} {}'.format(self.first, self.last)

emp_1 = Employee('Vineet', 'Bhatia', 50000) # emp_1 is instance of class Employee. We are passing this to the Employee class. The instance (emp_1) will be passed automatically to "self" above so it does not need to be specified.
emp_2 = Employee('Kiran', 'Kajal', 60000) # emp_2 is another instance of class Employee

print emp_1.fullname() # Need () after fullname since fullname is a method
print Employee.fullname(emp_1) # will do same as above. Above is a shorhand as you don't have to specify emp_1 as an argument, it is automatically passed to fullname method as self


