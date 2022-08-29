try:
    x = int(input("Enter length: "))
except ValueError:
    print("invalid input")
else:
    with open("output", "w") as f:
        for i in range(2 ** x):
            y = bin(i)[2:].zfill(x) # Zfill fills zeros at start
            if y.count("1") >= y.count("0"):
                print(y)
                f.write(y+"\n")
    f.close()
