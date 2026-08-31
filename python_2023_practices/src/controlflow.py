###
# ask for user's age
age = int(input('Enter your age: '))

# regular ticket price
ticket_price = 10.00

# check the age and apply discount
if age < 14:
    ticket_price *= 0.5
elif age >= 65:
    ticket_price *= 0.7

print(f"The ticket price is ${ticket_price}")


###
numbers = [7, 8, 0, 4, 3, 0, 5, 6, 0, 1]

for index, number in enumerate(numbers):
    if number == 0:
        print(f"The first zero found at index {index}")
        break


###
# ask for user's wight
weight = int(input('Enter your weight: '))

# regular wight
normal_weight = 75

# check the wight and return the BMI
if weight > 75:
    print('Your BMI is greater than normal')
elif weight < 75:
    print('Your BMI is less than normal')
else:
    print('You are in a normal BMI')