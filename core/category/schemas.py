from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    description:str
    color:str
    icon:str
    is_default:bool