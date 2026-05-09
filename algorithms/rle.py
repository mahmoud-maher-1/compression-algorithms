def rle_compress(data):
    if not data: return ""
    res = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            res.append(f"{data[i - 1]}{count}")
            count = 1
    res.append(f"{data[-1]}{count}")
    return "".join(res)
