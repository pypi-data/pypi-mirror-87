def get_tree(data, parent):
    result = []
    for item in data:
        if parent == item["parent"]:
            temp = get_tree(data, item["id"])
            if (len(temp) > 0):
                item["children"] = temp
            result.append(item)
    return result


def get_tree_menu(data, parent):
    state = True
    for item in data:
        if parent == item['id']:
            state = False
    return state
