from functions import write_file as write

test_list = [
             ('lorem.txt', "wait, this isn't lorem ipsum"), 
             ("pkg/morelorem.txt","lorem ipsum dolor sit amet"), 
             ("/tmp/temp.txt", "this should not be allowed")
            ]

for test in test_list:
    print(write.write_file('calculator', test[0], test[1]))