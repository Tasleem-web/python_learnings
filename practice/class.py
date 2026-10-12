# class Person:
#     counter = 1
    

# p1 = Person()
# print(p1.counter)

# p1.counter = 20 #change only p1 because counter is an instance variable now

# p2 = Person()
# print(p2.counter)

# Person.counter = 10 #change everything because counter is a class variable
# print(Person.counter)
# print(p1.counter)
# print(p2.counter)



class Person:
    def __init__(self):
        return 'App'
    
p = Person()
print(p)

