from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

for i in range(height):
    for space in range(height - i - 1):
        print(" ", end = "")
    row = (2*i) + 3
    for block in range(row):
        if block == (row - 1) / 2:
            print("  ", end = "")
        else:
            print("#", end = "")
    print()
        