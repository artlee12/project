from typing import List
from sqlalchemy.orm import Session
from app.models.operation import Operation
from app.schemas.operation import OperationCreate

def create_operation(db: Session, operation: OperationCreate, user_id: int) -> Operation:
    db_operation = Operation(
        user_id=user_id,
        operation_type=operation.operation_type,
        input_text=operation.input_text,
        output_text=operation.output_text
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation

def get_user_operations(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Operation]:
    return db.query(Operation).filter(Operation.user_id == user_id).offset(skip).limit(limit).all() 