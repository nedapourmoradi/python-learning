import random


def validate_inpute(user_guess):
    if not user_guess.isdigit():
        print("Invalid input. Please try again.")
        return False
    
    user_guess = int(user_guess)
    if user_guess > 100 or user_guess < 1: 
        print("Your guess should be between 1 and 100! Please try again.") 
        return False
    return True


def main():
    rand_num = random.randint(1, 100)
    score = 100

    while True:
        user_guess = input("Guess a number between 1 and 100:")
        if user_guess == 'q':
            print("Thank you for playing. Goodbye!")
            break
        if not validate_inpute(user_guess):
            continue
        user_guess = int(user_guess)
        if rand_num > user_guess:
            print(f"Your guess is:{user_guess} and it is too low! Please guess another number.") 
        elif rand_num < user_guess: 
            print(f"Your guess is:{user_guess} and it is too high! Please guess another number.") 
        else:
            print(f"The number is: {user_guess}")
            print("Congradulations! Your guess is correct.")
            print(f"Your score is: {score}")
            break
        score -= 10
        score = max(score, 0)

if __name__ == '__main__':
    main()