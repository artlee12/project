import heapq
from collections import defaultdict
import random
import string
from typing import Dict, Tuple

class HuffmanNode:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def generate_key(length: int = 16) -> str:
    """Generate random key for XOR encryption"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def xor_encrypt(text: str, key: str) -> str:
    """XOR encryption of text with key"""
    key_length = len(key)
    text_length = len(text)
    result = []
    
    for i in range(text_length):
        result.append(chr(ord(text[i]) ^ ord(key[i % key_length])))
    
    return ''.join(result)

def xor_decrypt(encrypted_text: str, key: str) -> str:
    """XOR decryption of text with key"""
    return xor_encrypt(encrypted_text, key)  # XOR is symmetric

def build_frequency_dict(text: str) -> Dict[str, int]:
    """Build frequency dictionary for characters in text"""
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return dict(frequency)

def build_huffman_tree(frequency: Dict[str, int]) -> HuffmanNode:
    """Build Huffman tree from frequency dictionary"""
    heap = []
    for char, freq in frequency.items():
        heapq.heappush(heap, HuffmanNode(char, freq))
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        internal = HuffmanNode(None, left.freq + right.freq)
        internal.left = left
        internal.right = right
        
        heapq.heappush(heap, internal)
    
    return heap[0] if heap else None

def build_huffman_codes(root: HuffmanNode, current_code: str = "", codes: Dict[str, str] = None) -> Dict[str, str]:
    """Build Huffman codes dictionary"""
    if codes is None:
        codes = {}
    
    if root is None:
        return codes
    
    if root.char is not None:
        codes[root.char] = current_code
        return codes
    
    build_huffman_codes(root.left, current_code + "0", codes)
    build_huffman_codes(root.right, current_code + "1", codes)
    return codes

def huffman_encode(text: str, codes: Dict[str, str]) -> Tuple[str, int]:
    """Encode text using Huffman codes"""
    encoded = ''.join(codes[char] for char in text)
    padding = 8 - (len(encoded) % 8)
    if padding < 8:
        encoded += '0' * padding
    return encoded, padding

def huffman_decode(encoded: str, codes: Dict[str, str], padding: int) -> str:
    """Decode text using Huffman codes"""
    if padding < 8:
        encoded = encoded[:-padding]
    
    reverse_codes = {code: char for char, code in codes.items()}
    current_code = ""
    decoded = []
    
    for bit in encoded:
        current_code += bit
        if current_code in reverse_codes:
            decoded.append(reverse_codes[current_code])
            current_code = ""
    
    return ''.join(decoded)

def encode_text(text: str) -> Tuple[str, str, Dict[str, str], int]:
    """Encode text using Huffman compression and XOR encryption"""
    # Generate random key
    key = generate_key()
    
    # Build Huffman tree and codes
    frequency = build_frequency_dict(text)
    root = build_huffman_tree(frequency)
    codes = build_huffman_codes(root)
    
    # Huffman encoding
    encoded, padding = huffman_encode(text, codes)
    
    # XOR encryption
    encrypted = xor_encrypt(encoded, key)
    
    return encrypted, key, codes, padding

def decode_text(encrypted: str, key: str, codes: Dict[str, str], padding: int) -> str:
    """Decode text using XOR decryption and Huffman decompression"""
    # XOR decryption
    encoded = xor_decrypt(encrypted, key)
    
    # Huffman decoding
    return huffman_decode(encoded, codes, padding) 