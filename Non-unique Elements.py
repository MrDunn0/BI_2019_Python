def get_non_unique_els(initial_list):
    non_unique_list = []
    for element in initial_list:
        if initial_list.count(element) > 1:
            non_unique_list.append(element)
    return non_unique_list
