from cs50 import get_string

text = get_string("TEXT: ")


def main():
    L = letters(text)
    W = words(text)
    S = sentences(text)
    print(L)
    print(W)
    print(S)
    L = (100/W)*L
    S = (100/W)*S
    
    print(L)
    print(S)
    
    index = round(0.0588 * L - 0.296 * S - 15.8)
    
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


def letters(text):
    counter = 0
    text = text.lower()
    for i in range(len(text)):
        if ord(text[i]) >= 97 and ord(text[i]) <= 122:
            counter += 1
            
    return counter
    
    
def words(text):
    counter = 1
    for i in range(len(text)):
        if ord(text[i]) == 32:
            counter += 1
    return counter
    
    
def sentences(text):
    counter = 0
    for i in range(len(text)):
        if ord(text[i]) == 33 or ord(text[i]) == 46 or ord(text[i]) == 63:
            counter += 1
    return counter
    
    
main()