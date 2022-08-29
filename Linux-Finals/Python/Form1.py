# Question 1
string = "AAaAaASSSsSSQQQQ XXxcB"
string = string.lower().strip()
temp = ""
i = 0
while i < len(string):
    j = i + 1
    counter = 1
    while j < len(string) and string[j] == string[i]:
        counter += 1
        j += 1
    if string[i] != " ":
        temp += str(counter) + string[i].upper()
    else:
        temp += string[i]
    i = j
print(temp)
