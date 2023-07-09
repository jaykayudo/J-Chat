from string import ascii_lowercase
a = list(ascii_lowercase)
example = 'zendaya'
hash_key = 13
def hash_word(word):
    hashedletter = []
    for x in word:
        number1 = a.index(x) + hash_key
        rangedData = (len(a)-1)
        original_number = number1 - (rangedData + 1) if number1 > rangedData else  number1
        hashedletter.append(a[original_number])
    return ''.join(hashedletter)
def unhash_word(word):
    hashedletter = []
    for x in word:
        number1 = a.index(x) - hash_key
        rangedData = (len(a)-1)
        original_number = (rangedData + 1) + number1 if number1 < 0 else number1
        hashedletter.append(a[original_number])
    return ''.join(hashedletter)
print("\033[36m"+hash_word(example))
print("\033[91m"+unhash_word(hash_word(example)))