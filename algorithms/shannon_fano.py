def shannon_fano_compress(data):
    if not data: return ""
    freqs = {}
    for ch in data: freqs[ch] = freqs.get(ch, 0) + 1
    symbols = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    codes = {s[0]: "" for s in symbols}

    def split(s_list):
        if len(s_list) <= 1: return
        total = sum(wt for _, wt in s_list)
        acc, min_diff, split_idx = 0, float('inf'), 1
        for i in range(1, len(s_list)):
            acc += s_list[i-1][1]
            diff = abs(acc - (total - acc))
            if diff < min_diff:
                min_diff = diff
                split_idx = i
        for ch, _ in s_list[:split_idx]: codes[ch] += "0"
        for ch, _ in s_list[split_idx:]: codes[ch] += "1"
        split(s_list[:split_idx])
        split(s_list[split_idx:])

    split(symbols)
    return ''.join(codes[ch] for ch in data)
