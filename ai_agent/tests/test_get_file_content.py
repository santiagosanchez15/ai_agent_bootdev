
from functions import get_file_content as content
file = content.get_file_content("calculator", "lorem.txt")
print(len(file), file[-51:] )

list_test = [('calculator', 'main.py'), ("calculator", "pkg/calculator.py")]
list_error_test = [('calculator', "/bin/cat"), ("calculator", "pkg/does_not_exist.py")]

for test in list_test: print(content.get_file_content(test[0], test[1]))

for error in list_error_test:
    print(content.get_file_content(error[0], error[1]))
