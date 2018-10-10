class Employee:

    num_of_emps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = '{}.{}@company.com'.format(first, last)

        Employee.num_of_emps += 1

    def fullname(self):
        return '{}'.format(self.pay)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount )


emp_1 = Employee('Vineet', 'Bhatia', 50000)
emp_2 = Employee('test', 'user', 60000)
emp_3 = Employee('ass', 'punk', 70000)

print Employee.num_of_emps
print emp_1.last
print Employee.fullname(emp_1)
print emp_1.fullname()
