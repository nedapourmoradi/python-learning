###
temperatures = [19, 21, 22, 24, 23, 19, 20]

total_temp = 0

for temp in temperatures:
    total_temp += temp

average_temp = total_temp / len(temperatures)

print(f"Average temperature: {average_temp:.2f}°C")


###
max_temp = temperatures[0]
min_temp = temperatures[0]

for temp in temperatures:
    if temp > max_temp:
        max_temp = temp
    elif temp < min_temp:
        min_temp = temp

print(f"Maximum temperature: {max_temp:.2f}°C")
print(f"Minimum temperature: {min_temp:.2f}°C")


###
warm_day_count = 0

for temp in temperatures:
    if temp >= 22:
        warm_day_count += 1

print(f"Number of warm days: {warm_day_count}")


###
fluctuations = []

for i in range(len(temperatures) - 1):
    fluctuation = abs(
        temperatures[i + 1] - temperatures[i]
    )
    fluctuations.append(fluctuation)

print(f"Temperature fluctuations: {fluctuations}")


###
largest_fluctuation = 0
day_of_largest_fluctuation = 0

for i in range(len(fluctuations)):
    if fluctuations[i] > largest_fluctuation:
        largest_fluctuation = fluctuations[i]
        day_of_largest_fluctuation = i + 1

print(
    f"Largest fluctuation: {largest_fluctuation}°C "
    f"from day {day_of_largest_fluctuation} "
    f"to day {day_of_largest_fluctuation + 1}"
)

###
initial_balance = 1000  # The starting balance in the account.
monthly_deposit = 200   # The fixed amount deposited into the account each month.
annual_interest_rate = 0.05  # The annual interest rate as a decimal (5% here).
savings_goal = 4000     # The target balance you want to reach.

balance = initial_balance
months = 0

while balance < savings_goal:
    balance += monthly_deposit

    if months % 12 == 0 and months > 0:
        balance += balance * annual_interest_rate

    months += 1

print(
    f"It will take {months} months "
    f"to reach the savings goal."
)


###
balance = initial_balance
months = 0

while balance < savings_goal:
    # Add monthly deposit to balance
    balance += monthly_deposit
    # Check if a year has passed and apply interest
    if months % 12 == 0 and months > 0:
        balance += balance * annual_interest_rate
    # Increment the month count
    months += 1

print(f"It will take {months} months to reach the savings goal.")


# Task 2: Print the Account Balance at the End of Each Year
balance = initial_balance
months = 0

while balance < savings_goal:
    # Add monthly deposit to balance
    balance += monthly_deposit
    # Increment the month count
    months += 1
    # Check if a year has passed and apply interest
    if months % 12 == 0:
        balance += balance * annual_interest_rate
        print(f"Account balance at the end of year {months // 12}: ${balance:.2f}")


# logocal extension for the problem
balance = initial_balance
months = 0
interest_frequency = 12

while balance < savings_goal:
    balance += monthly_deposit
    if months % interest_frequency == 0 and months > 0:
        balance += balance * (annual_interest_rate / (12 / interest_frequency))
    months += 1
print(f"Interest applied every {interest_frequency} months: It will take {months} months to reach the savings goal.")