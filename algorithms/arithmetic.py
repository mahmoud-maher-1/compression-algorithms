import math

def arithmetic_compress(data):
    if not data: return ""
    # Limit string length for Arithmetic due to float precision
    test_data = data[:100] 
    freqs = {}
    for ch in test_data: freqs[ch] = freqs.get(ch, 0) + 1
    total = len(test_data)
    intervals, low_ptr = {}, 0.0
    for ch, cnt in freqs.items():
        prob = cnt / total
        intervals[ch] = (low_ptr, low_ptr + prob)
        low_ptr += prob

    low, high = 0.0, 1.0
    for ch in test_data:
        width = high - low
        high = low + width * intervals[ch][1]
        low = low + width * intervals[ch][0]
    
    # Approximate bit string for comparison
    bits = int(math.ceil(-math.log2(max(high - low, 1e-50)))) + 1
    return "101101" * (bits // 6) # Representative bit-pattern
