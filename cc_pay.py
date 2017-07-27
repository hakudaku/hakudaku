#!/usr/bin/python -tt

from __future__ import division

total_paid = []
int_rate = input('Please enter APR: ')
tot_balance = input('Please enter Total Balance: ')
tot_starting_bal = tot_balance 
# tot_balance = 27819.07 
int_rate_on_tot_bal = 2
monthly_payment = input('Please enter monthly payment amount: ') 
payment_num = 1 

daily_int_rate = int_rate/365/100
minimum_payment = tot_balance*2/100
monthly_int_charge = tot_balance*daily_int_rate*30

print '{} {} {} {} {}'.format('Based on your APR of', int_rate, ', the daily interest rate is', daily_int_rate, '\n')
print '{}: ${}'.format('Initial outstanding balance', tot_balance) + '\n'

while tot_balance > 0:
  if monthly_payment > tot_balance:
    monthly_payment = tot_balance
  print '{}: ${}'.format('Balance carried over from last month', int(tot_balance))
  print '{} {}'.format('Payment #', int(payment_num))
  print '{}: ${}'.format('Amount', int(monthly_payment))
  total_paid.append(monthly_payment)
  tot_balance = tot_balance - monthly_payment
  print '{}: ${}'.format('Remaining balance', int(tot_balance))
  monthly_int_charge = tot_balance * daily_int_rate * 30
  print '{}: ${}'.format('Monthly interest', int(monthly_int_charge))
  tot_balance = tot_balance + monthly_int_charge
  print '{} ${}'.format('Remaining balance + monthly interest:', int(tot_balance))
  minimum_payment = tot_balance*2/100
  print '{}: ${}'.format('Min payment due based on new remaining balance', int(minimum_payment))
  print '\n'
  payment_num = payment_num + 1

tot_int_paid = sum(total_paid) - tot_starting_bal
print '{}: ${}'.format('Total payments made', int(sum(total_paid)))
print '{}: ${}'.format('Total interest paid', int(tot_int_paid)) 
