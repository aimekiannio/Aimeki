history = []


def display_all(decimal):
    print("\n==============================")
    print("      CONVERSION RESULT")
    print("==============================")
    print("BIN :", bin(decimal)[2:])
    print("OCT :", oct(decimal)[2:])
    print("DEC :", decimal)
    print("HEX :", hex(decimal)[2:].upper())
    print("==============================")

    history.append(
        f"BIN:{bin(decimal)[2:]} | "
        f"OCT:{oct(decimal)[2:]} | "
        f"DEC:{decimal} | "
        f"HEX:{hex(decimal)[2:].upper()}"
    )


def binary_input():
    binary = input("Enter Binary Number: ")

    try:
        decimal = int(binary, 2)
        display_all(decimal)

    except ValueError:
        print("Invalid Binary Number")


def octal_input():
    octal = input("Enter Octal Number: ")

    try:
        decimal = int(octal, 8)
        display_all(decimal)

    except ValueError:
        print("Invalid Octal Number")


def decimal_input():
    decimal = input("Enter Decimal Number: ")

    try:
        decimal = int(decimal)
        display_all(decimal)

    except ValueError:
        print("Invalid Decimal Number")


def hexadecimal_input():
    hexadecimal = input("Enter Hexadecimal Number: ")

    try:
        decimal = int(hexadecimal, 16)
        display_all(decimal)

    except ValueError:
        print("Invalid Hexadecimal Number")


def show_history():

    print("\n==============================")
    print("           HISTORY")
    print("==============================")

    if len(history) == 0:
        print("No history available.")

    else:
        for item in history:
            print(item)

    print("==============================")


while True:

    print("\n===================================")
    print("     PROGRAMMER CALCULATOR")
    print("===================================")
    print("1. Input Binary (BIN)")
    print("2. Input Octal (OCT)")
    print("3. Input Decimal (DEC)")
    print("4. Input Hexadecimal (HEX)")
    print("5. View History")
    print("6. Exit")

    choice = input("\nSelect Option: ")

    if choice == "1":
        binary_input()

    elif choice == "2":
        octal_input()

    elif choice == "3":
        decimal_input()

    elif choice == "4":
        hexadecimal_input()

    elif choice == "5":
        show_history()

    elif choice == "6":
        print("Calculator Closed.")
        break

    else:
        print("Invalid Option.")