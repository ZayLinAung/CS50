from cs50 import get_string
import sys

def main():

    credit = get_string("Credit Card Number: ")
    add = calculate (credit)
    if not add % 10 == 0:
        sys.exit("INVALID")
    
    digit = counter(credit)
    if digit == 15 and credit[0] == str(3) and (credit[1] == str(4) or credit[1] == str(7)):
        print("AMEX")
    elif digit == 16 and credit[0] == str(5) and (credit[1] == str(1) or credit[1] == str(2) or credit[1] == str(3) or credit[1] == str(4) or credit[1] == str(5)):
        print("MASTERCARD")
    elif (digit == 13 or digit == 16) and credit[0] == str(4):
        print("VISA")

def calculate (credit):

    add = 0

    credit = int(credit)
    while credit > 0:
        digit1 = credit % 10
        credit = int(credit / 10)


        digit2 = (credit % 10) * 2
        if digit2 > 9:
            x = int(digit2 / 10)
            y = digit2 % 10
            digit2 = x + y
        credit = int(credit / 10)
        add = add + digit1 + digit2

    return add

def counter(credit):
    counter = 0
    credit = int(credit)
    while credit > 0:
        credit = int(credit / 10)
        counter += 1
    return (counter)

main()