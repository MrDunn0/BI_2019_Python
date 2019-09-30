def flat_list(list_with_nested_lists):
    flat_result = []
    for element in list_with_nested_lists:
        if type(element) is list:
            flat_result.extend(flat_list(element))
        else:
            flat_result.append(element)
    return flat_result
