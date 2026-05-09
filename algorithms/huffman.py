import heapq
import itertools

def huffman_compress(data):
    if not data: return ""
    freqs = {}
    for ch in data: freqs[ch] = freqs.get(ch, 0) + 1
    tie_breaker = itertools.count()
    heap = [[f, next(tie_breaker), ch, None, None] for ch, f in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo, hi = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, [lo[0] + hi[0], next(tie_breaker), None, lo, hi])

    def build_codes(node, prefix=""):
        if node[2] is not None: return {node[2]: prefix}
        c = {}
        c.update(build_codes(node[3], prefix + "0"))
        c.update(build_codes(node[4], prefix + "1"))
        return c
    h_codes = build_codes(heap[0])
    return "".join(h_codes[ch] for ch in data)
