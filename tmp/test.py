def closure():
    i = 0
    def integral(value):
        nonlocal i
        i += int(value)
        return i
    return integral

if __name__ == "__main__":
    A = closure()
    while True:
        value = input("Enter integer: ")
        if value == "exit": break
        print(A(value))
