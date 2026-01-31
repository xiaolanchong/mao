import zlib
import os
from pathlib import Path


def is_zlib(data: bytes) -> (bool, bytes):
    """
    Check if byte array is valid zlib-compressed data.
    Returns True if decompress succeeds, False otherwise.
    """
    if len(data) < 2:
        return False, None
    
    try:
        # Try to decompress - zlib will validate header/checksum automatically
        result = zlib.decompress(data)
        # Optional: check if decompressed data is reasonable size
        if len(result) > 0 and len(result) < len(data) * 10:
            return True, result
        return False, None
    except zlib.error:
        return False, None

def is_zlib_stream(data: bytes) -> (bool, bytes):
    """
    More robust: handles partial streams using decompressobj
    """
    if len(data) < 2:
        return False, None
    
    try:
        decomp = zlib.decompressobj()
        result = decomp.decompress(data)
        # Check if we consumed all input (unused_data empty)
        return len(decomp.unused_data) == 0 and len(result) > 0, result
    except zlib.error:
        return False, None


def scan_custom_archive(exe_path):
    file_num = 1
    with open(exe_path, 'rb') as f:
        data = f.read()
    
    # Find all #1!# entries (file headers)
    pos = 0
    while True:
        pos = data.find(b'#1!#', pos)
        if pos == -1: break
        
        # Extract filename after #1!#
        filename_end = data.find(b'\xb6', pos + 4)
        if filename_end != -1:
            fname = data[pos+4:filename_end].decode('ascii', errors='ignore')
            print(f"Found file: {fname} at 0x{pos:08X}")
            
            # Look for matching #2!#CONTENT block
            content_pos = data.find(b'!2!#' + fname.encode(), pos)
            if content_pos != -1:
                print(f"  Content at 0x{content_pos:08X}, size: {content_pos - filename_end}")
            archive = data[filename_end + 1:content_pos]
            is_z, unzipped = is_zlib_stream(archive)
            if is_z:
                path = Path('book') / Path(fname.lower())
                path.parent.mkdir(parents=True, exist_ok=True)
        
                with open(path, 'wb') as f:
                    f.write(unzipped)
                file_num += 1
                #if file_num > 15:
                #    exit(0)
                #print('Zlib:')
                #if '.HTML' in fname:
                #    print()

        
        pos += 4

scan_custom_archive('mao-book.exe')
