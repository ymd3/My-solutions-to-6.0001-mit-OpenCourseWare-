annual_salary = float(input('enter you annual salary: '))
current_savings = 0.0

def savings(annual_salary,current_savings,portion_saved):
    for a in range(1,37):
        current_savings += current_savings*(.04/12)
        current_savings += (portion_saved*annual_salary)/12
        if a%6 == 0:
            annual_salary = annual_salary*(1.07)
    return current_savings

upper = 1.0
lower = 0.0
guess = (upper + lower)/2
a = savings(annual_salary,current_savings, guess)
steps = 0

if savings(annual_salary, current_savings, 1)<250000:
    print('It is not possible to pay the down payment in three years')
    exit()
while abs(250000 - a)>=100:
    if a < 250000:
        lower = guess
    if a > 250000:
        upper = guess
    guess = (upper + lower)/2
    a = savings(annual_salary, current_savings, guess)
    steps += 1

print("Best savings rate: ", guess)
print("Steps in bisection search: ", steps)




