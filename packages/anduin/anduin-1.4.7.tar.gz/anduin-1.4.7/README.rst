a lite mysql connector...
Name from the Lord of Ring

<=========how to use=========>

from anduin.river import Ring

cond = [
    (col1,'=',val1),
    (col2,'=',val2),
    ....]

fields = [
    col1,
    col2
    ...]

params = {
    key1:val1,
    key2:val2,
    ...}

find one line of data:

    Ring.find(__TableName__,conditions=cond,fields=fields)

    return a python dict like { col1:value1,col2:value2...}

find datas

    Ring.select(__TableName__,conditions=cond,fields=fields)

    return a python list like [{ col1:value1,col2:value2...}]

update data:

    Ring.update(__TableName__,conditions=cond,params=params)

    return None

insert data:

    Ring.insert(__TableName__,params=params)

    return None

delete data:

    Ring.delete(__TableName__,conditions=cond)

    return None

using Ring.query() to execute sql directly like Ring.query('select * from table')

