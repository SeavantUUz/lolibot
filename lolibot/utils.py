def to_unicode(data):
    if isinstance(data,unicode):
        return data
    elif isinstance(data,int):
        return unicode(data)
    else:return data.decode('utf-8')
