# Assignment 2
#
# Create the functions below EXACTLY as specified.
# ⚠️ AUTO-GRADER CRITICAL WARNING ⚠️
# - Changing function names/parameters will cause 50% score deduction
# - Incorrect return types/formats will result in 0 marks for that question
# - Comments are ignored by Python and auto-grader (you can add your own)
# - Assume all inputs are valid unless otherwise stated



# Question 1 (25 points)
# Function Name: aggregate_quarterly_sales
# Input Parameters:
#   - transactions (list of dictionaries, each with "year" (integer), "month" (integer), and "amount" (float))
#
# Expected Return Value:
#   - A dictionary where keys are strings in "YYYY-QN" format (N is the quarter number 1-4),
#     and values are the total amount for that quarter (float).
#   - Only include quarters that have at least one transaction.
#   - If multiple transactions fall in the same quarter, sum their amounts.
#
# Quarter Mapping:
#   - Q1: months 1, 2, 3
#   - Q2: months 4, 5, 6
#   - Q3: months 7, 8, 9
#   - Q4: months 10, 11, 12
#
# Example 1:
#   aggregate_quarterly_sales([
#     {"year": 2023, "month": 1, "amount": 100.0},
#     {"year": 2023, "month": 2, "amount": 50.0},
#     {"year": 2023, "month": 4, "amount": 200.0}
#   ])
# Result:
#   {"2023-Q1": 150.0, "2023-Q2": 200.0}
#
# Example 2:
#   aggregate_quarterly_sales([
#     {"year": 2024, "month": 10, "amount": 300.0},
#     {"year": 2024, "month": 12, "amount": 150.0},
#     {"year": 2024, "month": 10, "amount": 100.0}
#   ])
# Result:
#   {"2024-Q4": 550.0}
#
# Example 3:
#   aggregate_quarterly_sales([
#     {"year": 2023, "month": 7, "amount": 80.0},
#     {"year": 2024, "month": 7, "amount": 120.0},
#     {"year": 2023, "month": 9, "amount": 40.0}
#   ])
# Result:
#   {"2023-Q3": 120.0, "2024-Q3": 120.0}
#
# Example 4:
#   aggregate_quarterly_sales([
#     {"year": 2025, "month": 6, "amount": 500.0}
#   ])
# Result:
#   {"2025-Q2": 500.0}
#
# Remarks:
#   "2023-q1" or "2023-1" are WRONG answers. The format must be "YYYY-QN".
#
def aggregate_quarterly_sales(transactions):
    result = {}
    for t in transactions:
        year = t["year"]
        month = t["month"]
        amount = t["amount"]
        quarter = (month - 1) // 3 + 1
        key = f"{year}-Q{quarter}"
        result[key] = result.get(key, 0.0) + amount
    return result



# Question 2 (25 points)
# Function Name: find_overbudget_categories
# Input Parameters:
#   - transactions (list of dictionaries, each with "category" (string) and "amount" (float))
#   - budgets (dictionary where keys are category names (string) and values are budget limits (float))
#
# Expected Return Value:
#   - A sorted list (alphabetically ascending) of category names (strings) where the total spending
#     is strictly greater than the budget limit.
#   - Only consider categories that appear in the budgets dictionary.
#     Ignore transaction categories not found in budgets.
#   - Categories in budgets that have no transactions should NOT be considered overbudget.
#
# Example 1:
#   find_overbudget_categories([
#     {"category": "Food", "amount": 150.0},
#     {"category": "Food", "amount": 100.0},
#     {"category": "Transport", "amount": 50.0},
#     {"category": "Entertainment", "amount": 80.0}
#   ], {"Food": 200.0, "Transport": 100.0, "Entertainment": 50.0})
# Result:
#   ["Entertainment", "Food"]
#
# Example 2:
#   find_overbudget_categories([
#     {"category": "Food", "amount": 50.0},
#     {"category": "Transport", "amount": 30.0}
#   ], {"Food": 100.0, "Transport": 100.0, "Utilities": 50.0})
# Result:
#   []
#
# Example 3:
#   find_overbudget_categories([
#     {"category": "Food", "amount": 300.0},
#     {"category": "Rent", "amount": 2000.0},
#     {"category": "Transport", "amount": 60.0}
#   ], {"Food": 250.0, "Transport": 100.0})
# Result:
#   ["Food"]
# Note: "Rent" is not in budgets, so it is ignored.
#
# Example 4:
#   find_overbudget_categories([
#     {"category": "Food", "amount": 100.0},
#     {"category": "Food", "amount": 100.0},
#     {"category": "Transport", "amount": 50.0}
#   ], {"Food": 200.0, "Transport": 30.0})
# Result:
#   ["Transport"]
# Note: Food total (200.0) equals the budget (200.0), which is NOT overbudget (must be strictly greater).

def find_overbudget_categories(transactions, budgets):
    spending = {}
    for t in transactions:
        cat = t["category"]
        if cat in budgets:
            spending[cat] = spending.get(cat, 0.0) + t["amount"]
            
    overbudget = []
    for cat, limit in budgets.items():
        if spending.get(cat, 0.0) > limit:
            overbudget.append(cat)
            
    return sorted(overbudget)


# Question 3 (30 points)
# Function Name: allocate_investment
# Input Parameters:
#   - total_amount (float, total amount to allocate)
#   - percentages (list of floats, each representing a percentage, always sum to 100)
#
# Expected Return Value:
#   - A list of floats representing the allocated amount for each percentage.
#   - The order of the output list must match the order of the input percentages list.
#
# Procedure:
#   1. Compute each allocation as total_amount * percentage / 100.
#   2. Round each allocation to 2 decimal places using round half up.
#   3. If the sum of all rounded allocations does not equal total_amount,
#      adjust only the first allocation so that the total is exact.
#   4. The final returned allocations must all be represented to 2 decimal places.
#
# Important:
#   - Do not use Python's default round() for this question.
#   - To avoid floating-point precision issues, you may use Decimal internally.
#   - The function must still return a list of floats.
#
# Example 1:
#   allocate_investment(1000.0, [50.0, 30.0, 20.0])
# Result:
#   [500.0, 300.0, 200.0]
#
# Example 2:
#   allocate_investment(10.00, [33.33, 33.33, 33.34])
# Result:
#   [3.34, 3.33, 3.33]
# Explanation:
#   Raw allocations are 3.333, 3.333, and 3.334.
#   Rounded values are 3.33, 3.33, and 3.33.
#   Since 3.33 + 3.33 + 3.33 = 9.99, adjust the first allocation:
#   first = 10.00 - (3.33 + 3.33) = 3.34
#
# Example 3:
#   allocate_investment(50.0, [40.0, 35.0, 25.0])
# Result:
#   [20.0, 17.5, 12.5]
#
# Example 4:
#   allocate_investment(33.33, [50.0, 50.0])
# Result:
#   [16.66, 16.67]
# Explanation:
#   Raw allocations are 16.665 and 16.665.
#   Rounded values are 16.67 and 16.67.
#   Since 16.67 + 16.67 = 33.34, adjust the first allocation:
#   first = 33.33 - 16.67 = 16.66
#
# Example 5:
#   allocate_investment(99.99, [40.0, 35.0, 25.0])
# Result:
#   [39.99, 35.0, 25.0]
#
# Example 6:
#   allocate_investment(75.50, [60.0, 25.0, 15.0])
# Result:
#   [45.29, 18.88, 11.33]
#
def allocate_investment(total_amount, percentages):
    from decimal import Decimal, ROUND_HALF_UP
    total_dec = Decimal(str(total_amount))
    allocations = []
    
    for p in percentages:
        p_dec = Decimal(str(p))
        val = (total_dec * p_dec / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        allocations.append(val)
        
    diff = total_dec - sum(allocations)
    if diff != Decimal("0.00"):
        allocations[0] += diff
        
    return [float(a) for a in allocations]


# Question 4 (20 points)
#
# Function Name: calculate_progressive_tax
# Input Parameters:
#   - income (float, total taxable income)
#   - brackets (list of tuples, each containing (upper_limit (float), rate (float)))
#     Brackets are non-empty and sorted by upper_limit in ascending order.
#
# Expected Return Value:
#   - Total tax amount (float), rounded to 2 decimal places.
#
# Rules:
#   - Each bracket's rate applies only to the income portion inside that bracket, not the entire income.
#   - The first bracket covers income from 0 up to its upper_limit (inclusive).
#   - Each subsequent bracket covers income from the previous bracket's upper_limit up to its own upper_limit.
#   - If income exceeds the last bracket's upper_limit, the excess is taxed at the last bracket's rate.
#
# Example 1:
#   calculate_progressive_tax(80000, [(20000, 0.0), (50000, 0.10), (100000, 0.20)])
# Result:
#   9000.0
# Explanation:
#   0 - 20000 (20000) at 0%  = 0
#   20000 - 50000 (30000) at 10% = 3000
#   50000 - 80000 (30000) at 20% = 6000
#   Total = 9000.0
#
# Example 2:
#   calculate_progressive_tax(50000, [(10000, 0.05), (40000, 0.10), (80000, 0.15)])
# Result:
#   5000.0
# Explanation:
#   0 - 10000 (10000) at 5%  = 500
#   10000 - 40000 (30000) at 10% = 3000
#   40000 - 50000 (10000) at 15% = 1500
#   Total = 5000.0
#
# Example 3:
#   calculate_progressive_tax(150000, [(30000, 0.0), (60000, 0.10), (120000, 0.20)])
# Result:
#   21000.0
# Explanation:
#   0 - 30000 (30000) at 0%  = 0
#   30000 - 60000 (30000) at 10% = 3000
#   60000 - 120000 (60000) at 20% = 12000
#   120000 - 150000 (30000) at 20% = 6000  (exceeds last bracket, uses last rate)
#   Total = 21000.0
#
# Example 4:
#   calculate_progressive_tax(15000, [(10000, 0.10), (30000, 0.20), (60000, 0.30)])
# Result:
#   2000.0
# Explanation:
#   0 - 10000 (10000) at 10% = 1000
#   10000 - 15000 (5000) at 20% = 1000
#   Total = 2000.0
#
# Example 5:
#   calculate_progressive_tax(0, [(20000, 0.05), (50000, 0.10)])
# Result:
#   0.0
# Explanation:
#   Income is 0, so no tax is owed.
#

def calculate_progressive_tax(income, brackets):
    total_tax = 0.0
    previous_limit = 0.0
    for limit, rate in brackets:
        if income > previous_limit:
            taxable = min(income, limit) - previous_limit
            total_tax += taxable * rate
        previous_limit = limit
        
    if income > previous_limit:
        last_rate = brackets[-1][1]
        total_tax += (income - previous_limit) * last_rate
        
    return round(total_tax, 2)
