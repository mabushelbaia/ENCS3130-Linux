try:
    filename = input("Enter filename: ")
    file = open(filename, "r")
except IOError:
    print("Couldn't access file")
else:
    lines = file.readlines()
    summation = 0
    index = 1
    for line in lines:
        tokens = [word.strip(",;?!:;()[]\n\t").lower() for word in line.split(" ") if
                  word.strip(",;?!:;()[]\n\t").lower() == word.strip(",;?!:;()[]\n\t")[::-1].lower()]
        print(f"Line {index}:", end=" ")
        for word in tokens: 		# followed the given print format.
            if word == tokens[-1]: 
                print(f"{word}")
            else:
                print(f"{word}", end=", ")
        summation += len(tokens)
        index += 1
    print(f"Total palindromic words: {summation}")
