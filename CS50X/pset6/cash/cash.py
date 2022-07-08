from cs50 import get_float

while True:
    cash = get_float("Change: ")
    if cash > 0:
        break
cash = round(cash * 100)

counter = 0

while cash >= 25:
    cash -= 25
    counter += 1
    
while cash >= 10:
    cash -= 10
    counter += 1

while cash >= 5:
    cash -= 5
    counter += 1
    
while cash >= 1:
    cash -= 1
    counter += 1
    
print(counter)