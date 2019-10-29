# Первая попытка - какая-то шиза (но она работает)


def group_equal(list_to_group, prefix=[]):  # Pycharm ноет, но Артем так учил...
    if len(list_to_group) == 0:
        return prefix
    equal_consecutive = []
    for i in range(len(list_to_group)):
        if i == len(list_to_group) - 1:
            equal_consecutive.append(list_to_group[i])
            return group_equal(list_to_group[i + 1:], prefix + [equal_consecutive])
        elif list_to_group[i] == list_to_group[i + 1]:
            equal_consecutive.append(list_to_group[i])
        else:
            equal_consecutive.append(list_to_group[i])
            return group_equal(list_to_group[i + 1:], prefix + [equal_consecutive])


print(group_equal([1, 1, 4, 4, 4, "hello", "hello", 4]))
print(group_equal([1, 2, 3, 4]))
print(group_equal([1]))
print(group_equal([]))


# Вторая попытка задумывалась адекватной, но все равно получилось чутка по-уродски


def group_equal_2(list_to_group):
    result = []
    equal_consecutive = []
    for i in range(len(list_to_group)):
        equal_consecutive.append(list_to_group[i])
        if i == len(list_to_group) - 1:
            result.append([equal for equal in equal_consecutive])
            break
        elif list_to_group[i] != list_to_group[i + 1]:
            result.append([equal for equal in equal_consecutive])
            equal_consecutive.clear()
    return result


print(group_equal_2([1, 1, 4, 4, 4, "hello", "hello", 4]))
print(group_equal_2([1, 2, 3, 4]))
print(group_equal_2([1]))
print(group_equal_2([]))
