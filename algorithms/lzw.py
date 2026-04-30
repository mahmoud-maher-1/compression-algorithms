from config.logger import logger

def lzw_compress(text):
    """
    LZW (Lempel-Ziv-Welch): Dictionary-based lossless compression.
    Builds a dictionary of patterns automatically.
    Filters out non-ASCII characters (ord > 255) as requested.
    """
    logger.debug(f"Starting LZW compression (input size: {len(text)} chars)")
    
    # Filter out non-ASCII characters
    clean_text = "".join(c for c in text if ord(c) < 256)
    if len(clean_text) < len(text):
        logger.warning(f"LZW compression: {len(text) - len(clean_text)} non-ASCII characters were ignored.")
        text = clean_text

    if not text:
        logger.debug("LZW compression: empty input, returning empty string.")
        return ""

    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
            
    if w:
        result.append(dictionary[w])
        
    # Returning as string representation to measure "stored" size
    compressed_str = "".join(map(str, result))
    logger.debug(f"LZW compression complete (output string len: {len(compressed_str)})")
    return compressed_str
