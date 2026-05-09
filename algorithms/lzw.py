def lzw_compress(data):
    dict_size, dictionary, w, res = 256, {chr(i): i for i in range(256)}, "", []
    for c in data:
        wc = w + c
        if wc in dictionary: w = wc
        else:
            res.append(str(dictionary[w]))
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w: res.append(str(dictionary[w]))
    return "".join(res)
