from typing import Dict, Optional
from pydantic import BaseModel

class EncodeRequest(BaseModel):
    text: str

class EncodeResponse(BaseModel):
    encrypted_data: str
    key: str
    huffman_codes: Dict[str, str]
    padding_info: Optional[int] = None

class DecodeRequest(BaseModel):
    encrypted_data: str
    key: str
    huffman_codes: Dict[str, str]
    padding_info: Optional[int] = None

class DecodeResponse(BaseModel):
    decoded_text: str 