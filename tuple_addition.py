def tuple_add(t1, t2):
    n = len(t1)
    if n != len(t2):
        raise TypeError()
    ret = []
    for i in range(n):
        ret.append(t1[i] + t2[i])
    return tuple(ret)