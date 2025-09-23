TEST_PING = "pingping!"


from pydantic import BaseModel, Field
from typing import Dict

class UserAddResultType(BaseModel):
    status_code: int = Field(..., description="HTTP status code for the result")
    message: str = Field(..., description="Description message for the result")

USER_ADD_RESULT: Dict[str, UserAddResultType] = {
    "success": UserAddResultType(status_code=200, message="User added successfully"),
    "duplicate": UserAddResultType(status_code=401, message="User already exsited"),
    "error": UserAddResultType(status_code=501, message="Database error"),
}