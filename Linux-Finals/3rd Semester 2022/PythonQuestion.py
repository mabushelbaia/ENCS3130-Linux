try:
    filename = input("Enter filename: ")
    file = open(filename, "r")
except IOError:
    print("Couldn't access file")
else:
    n = int(input("Enter n: "))
    for line in file.readlines():
        my_dict = {}
        words = [word.strip(",;?!:;()[]\n\t").lower() for word in line.split(" ")] # split the line into words removing punctuation
        for word in words:
            if word == "a" or word == "an" or word == "the":
                continue
            else:
                my_dict[word] = my_dict.get(word, 0) + 1 # my_dict.get(word, 0) returns the value of the key word if it exists, otherwise it returns 0
        for word in my_dict:
            if my_dict[word] >= n:
                print(f"{word}: {my_dict[word]}")
            