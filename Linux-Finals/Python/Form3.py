while True:
    n = input("Enter first string: ").lower()
    m = input("Enter second string: ").lower()
    if len(n) != len(m):
        print("NO")
    else:
        n = n * 2
        if n.count(m) > 0:
            print("Yes")
        else:
            print("No")
    x = input("Do you want to continue (c, q): ").lower()
    if x == "q":
        break
