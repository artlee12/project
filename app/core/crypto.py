from typing import Tuple, Dict
import struct
from collections import Counter
import heapq

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text: str) -> HuffmanNode:
    frequency = Counter(text)
    heap = [HuffmanNode(char=char, freq=freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    return heap[0]

def build_huffman_codes(node: HuffmanNode, code="", codes=None) -> Dict[str, str]:
    if codes is None:
        codes = {}
    if node.char is not None:
        codes[node.char] = code
    else:
        build_huffman_codes(node.left, code + "0", codes)
        build_huffman_codes(node.right, code + "1", codes)
    return codes

def huffman_encode(text: str) -> Tuple[str, Dict[str, str]]:
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    return encoded_text, codes

def huffman_decode(encoded_text: str, codes: Dict[str, str]) -> str:
    reverse_codes = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_text = ""
    
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""
    
    return decoded_text

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    key_length = len(key)
    return bytes([data[i] ^ key[i % key_length] for i in range(len(data))])

def xor_decrypt(encrypted_data: bytes, key: bytes) -> bytes:
    return xor_encrypt(encrypted_data, key)  # XOR encryption is symmetric 