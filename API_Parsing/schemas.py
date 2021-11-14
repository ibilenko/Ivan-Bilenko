from typing import List, Optional

from pydantic import BaseModel, Field

class SendPackage(BaseModel):
    acc_name: str = Field(alias='acc_name')
    message: str = Field(alias='message')
    client_name: str = Field(alias='client_name')
