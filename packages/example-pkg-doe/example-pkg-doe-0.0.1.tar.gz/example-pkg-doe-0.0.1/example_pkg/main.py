class MyClass:
    def __init__(self, name):
        self.name = name
        self.called = 0

    def call(self):
        self.called += 1

    def printy(self):
        print("Hello " + self.name + " for the " + self.called + " time.")