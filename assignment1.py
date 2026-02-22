# Assignment 1
#
# Create the functions below EXACTLY as specified.
# ⚠️ AUTO-GRADER CRITICAL WARNING ⚠️
# - Changing function names/parameters will cause 50% score deduction
# - Incorrect return types/formats will result in 0 marks for that question
# - Comments are ignored by Python and auto-grader (you can add your own)
# - Make sure you define the function once and only once

# Question 1 (15 points)
# Function Name: days_in_month
#
# Input Parameters:
#   - year (integer)
#   - month (integer, 1-12)
#
# Expected Return Value:
#   - Number of days in the given month (integer), accounting for leap years if the month is February.
#
# Hint: A year is a leap year if it is divisible by 4,
#       EXCEPT years divisible by 100 are NOT leap years,
#       UNLESS also divisible by 400 (which ARE leap years).
#
# DO NOT USE ANY LIBRARY IN THIS QUESTION
#
# Examples:
#   days_in_month(2020, 2) → 29
#   days_in_month(2021, 2) → 28
#   days_in_month(2023, 4) → 30
#   days_in_month(2023, 1) → 31
#   days_in_month(1900, 2) → 28
#   days_in_month(2000, 2) → 29

def days_in_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 29
        else:
            return 28
    return 0


# Question 2 (15 points)
# Function Name: categorize_expenses
#
# Input Parameters:
#   - transactions (list of dictionaries, each with keys "amount" and "category". The type of amount is float, the type of category is string)
#
#
# Expected Return Value:
#   - A dictionary where keys are categories and values are the total amount spent in each category (float)
#
# Examples:
#   categorize_expenses([{"amount":50.0,"category":"Food"},{"amount":20.0,"category":"Transport"},{"amount":30.0,"category":"Food"}]) → {"Food":80.0,"Transport":20.0}
#   categorize_expenses([]) → {}

def categorize_expenses(transactions):
    category_totals = {}
    for transaction in transactions:
        category = transaction["category"]
        amount = transaction["amount"]
        category_totals[category] = category_totals.get(category, 0.0) + amount
    return category_totals

# Question 3 (20 points)
# Function Name: is_strong_password
#
# Input Parameters:
#   - password (string)
#
# Expected Return Value:
#   - True if the password meets all criteria; False otherwise.
#
# Criteria:
#   - At least 8 characters long
#   - Contains at least one uppercase letter
#   - Contains at least one digit
#   - Contains at least one of these 6 special characters: !, @, #, $, %, &
#   - Must only contain lowercase letters (a-z), uppercase letters (A-Z),
#     digits (0-9), and the 6 special characters listed above.
#     Any other character (e.g. space, underscore, ^) makes it invalid.
#
# Examples:
#   is_strong_password("Secure123!") → True
#   is_strong_password("weak") → False             (too short, missing uppercase/digit/special)
#   is_strong_password("NoSpecial1") → False        (missing special character)
#   is_strong_password("Secure 1!") → False         (contains a space)
#   is_strong_password("Secure_1!") → False         (contains underscore)

def is_strong_password(password):
    if len(password) < 8:
        return False
        
    has_upper = False
    has_digit = False
    has_special = False
    allowed_specials = "!@#$%&"
    
    for char in password:
        if 'A' <= char <= 'Z':
            has_upper = True
        elif 'a' <= char <= 'z':
            pass
        elif '0' <= char <= '9':
            has_digit = True
        elif char in allowed_specials:
            has_special = True
        else:
            return False  # Invalid character found
            
    return has_upper and has_digit and has_special



# Question 4 (15 points)
# Function Name: identify_low_performers
#
# Input Parameters:
#   - students (dictionary where keys are student names, values are lists of grades)
#   - threshold (integer, minimum average grade)
#
# Expected Return Value:
#   - A list of student names whose average grade is strictly below the threshold,
#     sorted in alphabetical (ascending) order
#
# Examples:
#   identify_low_performers({"Alice":[80,75],"Bob":[50,60],"Charlie":[90,85]}, 70) → ["Bob"]
#   identify_low_performers({"Alice":[50,60],"Bob":[50,60],"Charlie":[90,85]}, 70) → ["Alice","Bob"]

def identify_low_performers(students, threshold):
    low_performers = []
    for name, grades in students.items():
        if len(grades) > 0:
            avg = sum(grades) / len(grades)
        else:
            avg = 0
            
        if avg < threshold:
            low_performers.append(name)
            
    return sorted(low_performers)


# Question 5 (15 points)
# Function Name: validate_transactions
#
# Input Parameters:
#   - transactions (list of dictionaries with "year", "month", "day", "amount" keys)
#
# Expected Return Value:
#   - A dictionary with "valid" and "invalid" keys, each containing a list of transaction dictionaries
#   - A transaction is considered valid if:
#       1. The amount is strictly greater than 0 (amount == 0 is invalid)
#       2. The date exists (month is between 1 and 12, and day is between 1 and the number of days in that month)
#
# Notes:
#   - You could use days_in_month from Question 1 to validate dates
#   - DO NOT USE ANY LIBRARY IN THIS QUESTION
#
# Examples:
#   validate_transactions([{"year":2023,"month":2,"day":29,"amount":100.0},{"year":2024,"month":2,"day":29,"amount":-50.0}]) → {"valid":[],"invalid":[{"year":2023,"month":2,"day":29,"amount":100.0},{"year":2024,"month":2,"day":29,"amount":-50.0}]}
#   validate_transactions([{"year":2025,"month":3,"day":29,"amount":100.0},{"year":2025,"month":9,"day":29,"amount":-50.0}]) → {"valid":[{"year":2025,"month":3,"day":29,"amount":100.0}],"invalid":[{"year":2025,"month":9,"day":29,"amount":-50.0}]}
def validate_transactions(transactions):
    valid = []
    invalid = []
    
    for t in transactions:
        year = t["year"]
        month = t["month"]
        day = t["day"]
        amount = t["amount"]
        
        is_valid = True
        
        # Check amount validation
        if amount <= 0:
            is_valid = False
        # Check month validation
        elif month < 1 or month > 12:
            is_valid = False
        else:
            # Check day validation based on the month and leap year rules
            max_days = days_in_month(year, month)
            if day < 1 or day > max_days:
                is_valid = False
                
        if is_valid:
            valid.append(t)
        else:
            invalid.append(t)
            
    return {"valid": valid, "invalid": invalid}


# Question 6 (20 points)
# Function Name: restock_inventory
#
# Input Parameters:
#   - inventory (dictionary of item:current stock)
#   - min_stock (dictionary of item:minimum required stock)
#
# Expected Return Value:
#   - A dictionary showing additional units needed for each item in min_stock.
#     Include all items from min_stock in the result, even if no restocking is required (show 0).
#     Items that appear only in inventory (not in min_stock) should NOT appear in the result.
#     If current stock exceeds min_stock, show 0 (not a negative number).
#
# Example 1:
#   restock_inventory({"Apples":50,"Bananas":20},{"Apples":100,"Bananas":30})
# 
# Results:
#   {"Apples":50,"Bananas":10}
#
#
# Example 2:
#   restock_inventory({"Bananas":20},{"Apples":100,"Bananas":30})
# 
# Results:
#   {"Apples":100,"Bananas":10}
#
#
# Example 3:
#   restock_inventory({"Bananas":20},{"Apples":100})
# 
# Results:
#   {"Apples":100}
#
#
# Example 4:
#   restock_inventory({"Apples":100},{"Apples":100})
# 
# Results:
#   {"Apples":0}
#
#
# Example 5:
#   restock_inventory({"Apples":150},{"Apples":100})
# 
# Results:
#   {"Apples":0}
#
def restock_inventory(inventory, min_stock):
    restock = {}
    for item, req_stock in min_stock.items():
        curr_stock = inventory.get(item, 0)
        needed = req_stock - curr_stock
        
        if needed > 0:
            restock[item] = needed
        else:
            restock[item] = 0
            
    return restock