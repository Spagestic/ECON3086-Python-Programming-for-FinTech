# Class Exercise 3: Conditional Statements
# Complete the functions below EXACTLY as specified.
# ⚠️ AUTO-GRADER CRITICAL WARNING ⚠️
# - Changing function names/parameters will cause 50% score deduction
# - Incorrect return types/formats will result in 0 marks for that question
# - Comments are ignored by Python and auto-grader (you can add your own)


# Q1 - create a function to return True if a number is odd, False if it's even
#
#      It's ok that you Google if you don't know how to determine whether a
#      number is odd or even
#
def is_odd(x):
    # do something here
    if x % 2 != 0:
        return True
    else:
        return False # replace this line with the correct logic


# Q2 - create a function to compare two integer. output the bigger number
#      Don't use the max() function for exercise purpose
def compare(x, y):
    # do something here
    if x > y:
        return x
    else:
        return y  # replace this line with the correct logic


# Q3 - create a function to compare three integer. output the bigger number
#      Don't use the max() function for exercise purpose
def compare_3(x, y, z):
    # do something here
    if x >= y and x >= z:
        return x
    elif y >= x and y >= z:
        return y
    else: 
        return z  # replace this line with the correct logic


# Q4 - create a function to compare 4 integer. output the bigger number
#      Don't use the max() function for exercise purpose
def compare_4(a, b, c, d):
    # do something here
    if a >= b and a >= c and a >= d:
        return a
    elif b >= a and b >= c and b >= d:
        return b
    elif c >= a and c >= b and c >= d:
        return c
    else:
        return d  # replace this line with the correct logic


# Q5 - write a function to check whether a year is a leap year. return True or False
def leap_year(year):
    # do something here
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False  # replace this line with the correct logic


# Q6 - write a function to input 3 anglers of a triangle and check whether that is a
#      valid triangle. return True or False.
def is_triangle(a, b, c):
    # do something here
    if (a + b + c == 180) and a > 0 and b > 0 and c > 0:
        return True
    else:
        return False  # replace this line with the correct logic