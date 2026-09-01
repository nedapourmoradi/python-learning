"""This is a calculatin program"""

first_num = input("Enter your first number: ")

op = input("Enter your operation ['+', '-', '*', '/','//']: ")
valid_op = ['+', '-', '*', '/','//']

second_num = input("Enter your second number: ")


if op in valid_op: #To examinate the entered operation's validation

    #To examinate the validation of entered numbers
    if first_num.replace(".", "", 1).lstrip("-").isdigit() and second_num.replace(".", "", 1).lstrip("-").isdigit() and op:
        f_num = float(first_num)
        s_num = float(second_num)
        number = f_num, s_num
    
        if op == '+':
            result = f_num + s_num
            print(int(result) if result.is_integer() else result)

        elif op == '-':
            result = f_num - s_num
            print(int(result) if result.is_integer() else result)

        elif op == '*':
            result = f_num * s_num
            print(int(result) if result.is_integer() else result)

        elif op == '/':
            result = f_num / s_num
            print(int(result) if result.is_integer() else result)
            
        elif op == '//':
            result = f_num // s_num
            print(int(result) if result.is_integer() else result)
        
else:
    print("Please enter a given valid operation!")
