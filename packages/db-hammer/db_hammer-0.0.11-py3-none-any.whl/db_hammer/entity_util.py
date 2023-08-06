def get_dict(entity):
    dd = dir(entity)
    _dict = {}
    for d in dd:
        if not d.startswith("__"):
            _dict[d] = getattr(entity, d)
    return _dict


def get_insert_sql(entity, fn_db_value):
    dd = get_dict(entity)
    VALUES = []
    for d in dd:
        value = getattr(entity, d)
        if value is None:
            VALUES.append("null")
        elif not hasattr(entity, "__columns") or getattr(entity, "__columns") is None:
            VALUES.append(f"'{value}'")
        else:
            data_type = getattr(entity, "__columns").get(d)
            value = fn_db_value(data_type=data_type, value=value)
            VALUES.append(value)

    return f"""INSERT INTO {getattr(entity, "__table_name")}({",".join(dd)}) VALUES ({",".join(VALUES)})"""


def get_update_sql(entity, fn_db_value):
    keys = getattr(entity, "__primary_key")
    where = "WHERE"
    ps = []
    for k in keys:
        data_type = getattr(entity, "__columns").get(k)
        value = fn_db_value(data_type=data_type, value=getattr(entity, k))
        ps.append(f" {k}={value}")
    where += ' AND '.join(ps)

    dd = get_dict(entity)
    VALUES = []
    for d in dd:
        if d in keys:
            continue
        value = getattr(entity, d)
        if value is None:
            VALUES.append("null")
        elif not hasattr(entity, "__columns") or getattr(entity, "__columns") is None:
            VALUES.append(f"'{value}'")
        else:
            data_type = getattr(entity, "__columns").get(d)
            value = fn_db_value(data_type=data_type, value=value)
            VALUES.append(f"{d}={value}")

    return f"""UPDATE {getattr(entity, "__table_name")} SET {",".join(VALUES)} {where}"""
