# Most stupid way


def get_non_unique_els(initial_list):
    non_unique_list = []
    for i in initial_list:
        if i in non_unique_list:      # I think it will speed up function, although only the second condition is enough
            non_unique_list.append(i)
        elif initial_list.count(i) > 1:
            non_unique_list.append(i)
    return non_unique_list


test_list_1 = [1, 2, 3, 1, 3]
test_list_2 = [1, 2, 3, 4, 5]
test_list_3 = [5, 5, 5, 5, 5]
test_list_4 = [10, 9, 10, 10, 9]
print(get_non_unique_els(test_list_1))
print(get_non_unique_els(test_list_2))
print(get_non_unique_els(test_list_3))
print(get_non_unique_els(test_list_4))
