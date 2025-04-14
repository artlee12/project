import random
import string
from typing import Tuple, Dict, List

def xor_encrypt(text: str) -> Tuple[bytes, str]:
    """
    Шифрует текст с помощью XOR с случайным ключом.
    Возвращает зашифрованные данные и ключ.
    """
    # Генерируем случайный ключ той же длины, что и текст
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=len(text)))
    
    # Преобразуем текст и ключ в байты
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    
    # Применяем XOR к каждому байту
    encrypted_bytes = bytes(a ^ b for a, b in zip(text_bytes, key_bytes))
    
    return encrypted_bytes, key

def xor_decrypt(encrypted_data: bytes, key: str) -> str:
    """
    Расшифровывает данные с помощью XOR и ключа.
    Возвращает расшифрованный текст.
    """
    # Преобразуем ключ в байты
    key_bytes = key.encode('utf-8')
    
    # Применяем XOR к каждому байту
    decrypted_bytes = bytes(a ^ b for a, b in zip(encrypted_data, key_bytes))
    
    # Преобразуем байты обратно в строку
    return decrypted_bytes.decode('utf-8')

def huffman_encode(data: bytes) -> Tuple[bytes, Dict[int, str], Dict[str, int]]:
    """
    Сжимает данные с помощью алгоритма Хаффмана.
    Возвращает сжатые данные, коды Хаффмана и информацию о дополнении.
    """
    # Создаем частотный словарь
    freq = {}
    for byte in data:
        freq[byte] = freq.get(byte, 0) + 1
    
    # Создаем узлы для дерева Хаффмана
    nodes = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    
    # Строим дерево Хаффмана
    while len(nodes) > 1:
        nodes.sort()
        left = nodes.pop(0)
        right = nodes.pop(0)
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        for pair in right[1:]:
            pair[1] = '1' + pair[1]
        nodes.append([left[0] + right[0]] + left[1:] + right[1:])
    
    # Создаем словарь кодов
    huffman_codes = {symbol: code for symbol, code in nodes[0][1:]}
    
    # Кодируем данные
    encoded_bits = ''.join(huffman_codes[byte] for byte in data)
    
    # Добавляем дополнение, чтобы длина была кратна 8
    padding = 8 - (len(encoded_bits) % 8)
    if padding != 8:
        encoded_bits += '0' * padding
    
    # Преобразуем биты в байты
    encoded_bytes = bytes(int(encoded_bits[i:i+8], 2) for i in range(0, len(encoded_bits), 8))
    
    # Создаем информацию о дополнении
    padding_info = {
        'padding': padding,
        'original_length': len(data)
    }
    
    return encoded_bytes, huffman_codes, padding_info

def huffman_decode(encoded_data: bytes, huffman_codes: Dict[int, str], padding_info: Dict[str, int]) -> bytes:
    """
    Распаковывает данные, сжатые с помощью алгоритма Хаффмана.
    Возвращает исходные данные.
    """
    # Создаем обратный словарь кодов
    reverse_codes = {code: symbol for symbol, code in huffman_codes.items()}
    
    # Преобразуем байты в биты
    bits = ''.join(format(byte, '08b') for byte in encoded_data)
    
    # Удаляем дополнение
    if padding_info['padding'] != 8:
        bits = bits[:-padding_info['padding']]
    
    # Декодируем данные
    current_code = ''
    decoded_data = bytearray()
    
    for bit in bits:
        current_code += bit
        if current_code in reverse_codes:
            decoded_data.append(reverse_codes[current_code])
            current_code = ''
    
    return bytes(decoded_data) 