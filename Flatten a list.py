def flat_list(list_with_nested_lists, flat_result=None):
    if flat_result is None:         # It's because not allowed to change default arguments
        flat_result = []            # I tried flat_list(lst, flat_result = [])...
    for i in list_with_nested_lists:
        if type(i) is list:
            flat_list(i, flat_result)
        else:
            flat_result.append(i)
    return flat_result


print(flat_list([1, 2, 3]))
print(flat_list([1, [2, 2, 2], 4]))
print(flat_list([[[2]], [4, [5, 6, [6], 6, 6, 6], 7]]))
print(flat_list([-1, [1, [-2], 1], -1]))
