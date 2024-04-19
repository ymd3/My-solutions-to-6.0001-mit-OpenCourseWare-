annual_salary = float(input('enter you annual salary: '))
portion_saved = float(input('Enter the percentage of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))
semi_annual_raise = float(input('Enter the semi-annual raise, as a decimal: '))
portion_down_payment = 0.25*total_cost
current_savings = 0.0
months = 0
while current_savings < portion_down_payment:
    current_savings += current_savings * (0.04 / 12)
    current_savings += (annual_salary*portion_saved)/12
    months += 1
    if months%6 == 0:
        annual_salary = annual_salary*(1+semi_annual_raise)
print('number of months: ', months)
