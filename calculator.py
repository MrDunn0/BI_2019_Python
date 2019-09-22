input_data = []
for i in range(3):
    input_data.append(input())

if input_data[1] == "-":
    print(int(input_data[0]) - int(input_data[2]))

elif input_data[1] == "+":
    print(int(input_data[0]) + int(input_data[2]))

elif input_data[1] == "*":
    print(int(input_data[0]) * int(input_data[2]))

elif input_data[1] == ":" or "/":
    print(int(input_data[0]) / int(input_data[2]))
