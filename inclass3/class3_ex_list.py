# Class Exercise 3: List
# Complete the functions below EXACTLY as specified.
# ⚠️ AUTO-GRADER CRITICAL WARNING ⚠️
# - Changing function names/parameters will cause 50% score deduction
# - Incorrect return types/formats will result in 0 marks for that question
# - Comments are ignored by Python and auto-grader (you can add your own)


# 1. create a list with 5 items of the input parameters
def create_list(num1, num2, num3, num4, num5):
    return [num1, num2, num3, num4, num5]

# 2. sort the list in accending order
def sort_list(lst):
    return sorted(lst)

# 3. find the number of items of the list
def find_length(lst):
    return len(lst)

# 4. return sorted union of two list, i.e. a list that contains all elements of both list
#    and sort the result in accending order. keep duplicate values
def union_list(lst1, lst2):
    return sorted(lst1 + lst2)
