history = []


def show_number_systems(num):
    print("\n==============================")
    print("NUMBER REPRESENTATIONS")
    print("==============================")
    print("BIN :", bin(num)[2:])
    print("OCT :", oct(num)[2:])
    print("DEC :", num)
    print("HEX :", hex(num)[2:].upper())
    print("==============================")


def convert_number():
    try:
        num = int(input("Enter Decimal Number: "))
        show_number_systems(num)

        history.append(
            f"CONVERT -> DEC:{num} BIN:{bin(num)[2:]} HEX:{hex(num)[2:].upper()}"
        )

    except ValueError:
        print("Invalid Number")


def arithmetic():
    try:
        a = int(input("First Number: "))
        b = int(input("Second Number: "))

        print("\n1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")

        op = input("Choose: ")

        if op == "1":
            result = a + b
            symbol = "+"

        elif op == "2":
            result = a - b
            symbol = "-"

        elif op == "3":
            result = a * b
            symbol = "*"

        elif op == "4":
            if b == 0:
                print("Cannot divide by zero")
                return

            result = a // b
            symbol = "/"

        else:
            print("Invalid Option")
            return

        print("\nResult:", result)
        show_number_systems(result)

        history.append(f"{a} {symbol} {b} = {result}")

    except ValueError:
        print("Invalid Input")


def bitwise_operations():
    try:
        a = int(input("First Number: "))
        b = int(input("Second Number: "))

        print("\n1. AND")
        print("2. OR")
        print("3. XOR")

        choice = input("Choose: ")

        if choice == "1":
            result = a & b
            operation = "AND"

        elif choice == "2":
            result = a | b
            operation = "OR"

        elif choice == "3":
            result = a ^ b
            operation = "XOR"

        else:
            print("Invalid Option")
            return

        print("\nResult:", result)
        show_number_systems(result)

        history.append(f"{a} {operation} {b} = {result}")

    except ValueError:
        print("Invalid Input")


def shift_operations():
    try:
        num = int(input("Number: "))
        shift = int(input("Shift Amount: "))

        print("\n1. Left Shift")
        print("2. Right Shift")

        choice = input("Choose: ")

        if choice == "1":
            result = num << shift
            operation = "<<"

        elif choice == "2":
            result = num >> shift
            operation = ">>"

        else:
            print("Invalid Option")
            return

        print("\nResult:", result)
        show_number_systems(result)

        history.append(f"{num} {operation} {shift} = {result}")

    except ValueError:
        print("Invalid Input")


def show_history():
    print("\n=========== HISTORY ===========")

    if len(history) == 0:
        print("No History")

    else:
        for item in history:
            print(item)

    print("===============================")


while True:

    print("\n====================================")
    print("      PROGRAMMER CALCULATOR")
    print("====================================")
    print("1. Number Conversion")
    print("2. Arithmetic")
    print("3. Bitwise Operations")
    print("4. Shift Operations")
    print("5. History")
    print("6. Exit")

    choice = input("Select Option: ")

    if choice == "1":
        convert_number()

    elif choice == "2":
        arithmetic()

    elif choice == "3":
        bitwise_operations()

    elif choice == "4":
        shift_operations()

    elif choice == "5":
        show_history()

    elif choice == "6":
        print("Calculator Closed")
        break

    else:
        print("Invalid Option")