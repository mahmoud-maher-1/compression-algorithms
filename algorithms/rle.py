from config.logger import logger

def rle_compress(data):
    """
    Run-Length Encoding (RLE): Replaces repeated data with value + count.
    Best for data with long consecutive repeats.
    """
    logger.debug(f"Starting RLE compression (input size: {len(data)} chars)")
    
    if not data:
        logger.debug("RLE compression: empty input, returning empty string.")
        return ""
        
    res = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            res.append(f"{data[i - 1]}{count}")
            count = 1
    res.append(f"{data[-1]}{count}")
    
    compressed_str = "".join(res)
    logger.debug(f"RLE compression complete (output size: {len(compressed_str)} chars)")
    return compressed_str
