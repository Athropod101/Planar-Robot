class Test(Exception):
    pass

class ErrorTest:
    def __init__(self, x):
        self.x = x

    def Run(self):
        if self.x < 6:
            raise Test(
                    f"\nx is less than 6!\n"
                    f"RIP"
                    )
        else:
            print(":)")

T = ErrorTest(5)
T.Run()
