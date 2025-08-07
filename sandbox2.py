letters = ["A","B","C","D","E"]
group_letters = []
has_parity = False
for letter in letters:
    if has_parity:
        group_letters[-1] += letter
    else:
        group_letters.append(letter)
    has_parity = not has_parity
print(group_letters)
