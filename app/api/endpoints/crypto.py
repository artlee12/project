from fastapi import APIRouter, HTTPException
from app.schemas.crypto import EncodeRequest, EncodeResponse, DecodeRequest, DecodeResponse
from app.utils.crypto import xor_encrypt, xor_decrypt, huffman_encode, huffman_decode

router = APIRouter()

@router.post("/encode", response_model=EncodeResponse)
async def encode_text(request: EncodeRequest):
    try:
        # Шифруем текст с помощью XOR
        encrypted_data, key = xor_encrypt(request.text)
        
        # Сжимаем зашифрованные данные с помощью Хаффмана
        encoded_data, huffman_codes, padding_info = huffman_encode(encrypted_data)
        
        return EncodeResponse(
            encrypted_data=encoded_data,
            key=key,
            huffman_codes=huffman_codes,
            padding_info=padding_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decode", response_model=DecodeResponse)
async def decode_text(request: DecodeRequest):
    try:
        # Распаковываем данные Хаффмана
        decoded_data = huffman_decode(
            request.encrypted_data,
            request.huffman_codes,
            request.padding_info
        )
        
        # Расшифровываем данные с помощью XOR
        decrypted_text = xor_decrypt(decoded_data, request.key)
        
        return DecodeResponse(decoded_text=decrypted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 