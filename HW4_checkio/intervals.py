def get_intervals(set_of_ints):
    sorted_set_of_ints = sorted(list(set_of_ints))
    result = []
    for i in range(len(sorted_set_of_ints)):
        if i == 0:
            start_of_interval = sorted_set_of_ints[i]
        elif i == len(sorted_set_of_ints) - 1:
            result.append((start_of_interval, sorted_set_of_ints[i]))
        elif sorted_set_of_ints[i+1] - sorted_set_of_ints[i] > 1:
            result.append((start_of_interval, sorted_set_of_ints[i] ))
            start_of_interval = sorted_set_of_ints[i+1]
    return result


test_result_1 = get_intervals({1, 2, 3, 4, 5, 7, 8, 12})
test_result_2 = get_intervals({1, 2, 3, 6, 7, 8, 4, 5})
print(test_result_1)
print(test_result_2)

