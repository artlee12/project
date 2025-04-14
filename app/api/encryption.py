from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.encode import EncodeRequest, EncodeResponse, DecodeRequest, DecodeResponse
from app.core.encryption import encode_text, decode_text
from app.api import deps
from app.crud import crud_operation
from app.schemas.operation import OperationCreate, Operation
from app.models.operation import Operation as OperationModel

router = APIRouter()

@router.post("/encode", response_model=EncodeResponse)
async def encode_endpoint(
    request: EncodeRequest,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Encode text using Huffman compression and XOR encryption
    """
    try:
        encoded_data, key, huffman_codes, padding = encode_text(request.text)
        
        operation = OperationCreate(
            operation_type="encode",
            input_text=request.text,
            output_text=encoded_data
        )
        crud_operation.create_operation(db, operation, current_user.id)
        
        return EncodeResponse(
            encoded_data=encoded_data,
            key=key,
            huffman_codes=huffman_codes,
            padding=padding
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/decode", response_model=DecodeResponse)
async def decode_endpoint(
    request: DecodeRequest,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Decode text using XOR decryption and Huffman decompression
    """
    try:
        decoded_text = decode_text(
            request.encoded_data,
            request.key,
            request.huffman_codes,
            request.padding
        )
        
        # Log operation
        operation = OperationCreate(
            operation_type="decode",
            input_text=request.encoded_data,
            output_text=decoded_text
        )
        crud_operation.create_operation(db, operation, current_user.id)
        
        return DecodeResponse(decoded_text=decoded_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=list[Operation])
async def get_operation_history(
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get user's operation history
    """
    return crud_operation.get_user_operations(db, current_user.id, skip, limit) 