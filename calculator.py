print("Привет! Я очень простой, но трудолюбивый калькулятор для 2-х целых чисел. Доступные операции: + - / *")

operators_list = ["+", "-", "/", "*"]
while True:
    first_num = input("Введите первое число: ")
    operator = input("Введите оператор из предложенного списка: ")
    second_num = input("Введите второе число: ")
    if not (first_num.isdigit() and second_num.isdigit()):
        print("Вместо чисел вы ввели что-то другое.\nПожалуйста, вводите только то, что указано, иначе я не пойму.")
        continue
    if (first_num == "0" or second_num == "0") and operator == "/":
        print("Извините, Python не любит делить на ноль.")
        continue
    elif operator not in operators_list:
        print("Вы ввели оператор, которого нет в списке.\nПожалуйста, вводите только то, что указано, иначе я не пойму.")
        continue
    break

first_num, second_num = int(first_num), int(second_num)
result = 0

if operator == "+":
    result = first_num + second_num

elif operator == "-":
    result = first_num - second_num

elif operator == "/":
    result = first_num / second_num

elif operator == "*":
    result = first_num * second_num

print("Ответ: {} {} {} = {} \nCпасибо за обращение! Хорошего настроения!".format(first_num, operator, second_num, result))
