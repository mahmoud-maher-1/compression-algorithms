import itertools
import heapq
from config.logger import logger

def huffman_compress(text):
    """
    Huffman Coding: Lossless entropy encoding using a frequency-based tree.
    Assigns shorter codes to frequent characters.
    """
    logger.debug(f"Starting Huffman compression (input size: {len(text)} chars)")
    
    if not text:
        logger.debug("Huffman compression: empty input, returning empty string.")
        return ""

    # Calculate frequencies
    freqs = {}
    for char in text:
        freqs[char] = freqs.get(char, 0) + 1

    # Tie-breaker counter to fix the TypeError [str vs NoneType comparison]
    tie_breaker = itertools.count()

    # Build priority queue (Min-Heap)
    # Format: [frequency, unique_count, char, left_child, right_child]
    heap = [[f, next(tie_breaker), char, None, None] for char, f in freqs.items()]
    heapq.heapify(heap)
    
    # Handle edge case where input has only 1 unique character
    if len(heap) == 1:
        logger.debug("Huffman compression: only 1 unique character found.")
        char = heap[0][2]
        h_codes = {char: "0"}
    else:
        # Build Huffman Tree
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            merged = [lo[0] + hi[0], next(tie_breaker), None, lo, hi]
            heapq.heappush(heap, merged)

        # Generate prefix codes by traversing the tree
        def build_codes(node, prefix=""):
            if node[2] is not None:
                return {node[2]: prefix}
            codes = {}
            codes.update(build_codes(node[3], prefix + "0"))
            codes.update(build_codes(node[4], prefix + "1"))
            return codes

        h_codes = build_codes(heap[0])

    compressed_str = "".join([h_codes[c] for c in text])
    logger.debug(f"Huffman compression complete (output bits: {len(compressed_str)})")
    return compressed_str
