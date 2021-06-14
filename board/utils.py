def validate_data(request=None, data=None):
    try:
        if not data:
            data = request.json
    except Exception as e:
        msg = "payload must be a valid json"
        return {"error": msg}

    err_msg = ''
    name = data.get('name')
    age = data.get('age')
    point = data.get('point')
    address = data.get('address')
    if not (name and age and address):
        err_msg += "Name, age and address are manadatory fields,"
        return {"error": err_msg}
    try:
        age = int(age)
        if age <= 0:
            err_msg += "Age should be a positive number, "
        if age >= 110:
            err_msg += "Quite an age for a human being :'), "
    except Exception as e:
        err_msg += " Age should be a number, "

    name_contains_digit = any(map(str.isdigit, name))
    if name_contains_digit:
        err_msg += " Invalid name "

    addr_contains_digit = all(map(str.isdigit, address))
    if addr_contains_digit:
        err_msg += " Invalid address "

    if err_msg:
        return {"error": err_msg}

    return {"response": 'Data is valid'}