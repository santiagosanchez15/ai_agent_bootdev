from functions import run_python_file as run_python

test_list = [
                ("calculator", "main.py"), 
                ("calculator", "main.py", ["3 + 5"]),
                ("calculator", "tests.py"),
                ("calculator", "../main.py"), 
                ("calculator", "nonexistent.py"),
                ("calculator", "lorem.txt")
            ]

for test in test_list:
    if len(test) == 3: print(run_python.run_python_file(test[0],test[1], test[2]))
    else: print(run_python.run_python_file(test[0], test[1]))