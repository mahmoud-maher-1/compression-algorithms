from .rle import rle_compress
from .shannon_fano import shannon_fano_compress
from .arithmetic import arithmetic_compress
from .huffman import huffman_compress
from .lzw import lzw_compress

class CompressionAlgorithms:
    rle_compress = staticmethod(rle_compress)
    shannon_fano_compress = staticmethod(shannon_fano_compress)
    arithmetic_compress = staticmethod(arithmetic_compress)
    huffman_compress = staticmethod(huffman_compress)
    lzw_compress = staticmethod(lzw_compress)
