from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


class TicketSchema(BaseModel):
    id: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    userEmail: EmailStr = Field(...)
    creationTime: int = Field(...)
    labels: Optional[List[str]]


    class Config:
        schema_extra = {
            "example":    {
                "id": "21179ee2-cb21-560c-85ed-14f4909e1d01",
                "title": "Progressive Web Apps",
                "content": "Hey everyone, this is my example ticket...",
                "userEmail": "im2@ihi.vi",
                "creationTime": 1518867438530
            },
        }


class UpdateTicketModel(BaseModel):
    id: Optional[str]
    title: Optional[str]
    content: Optional[str]
    userEmail: Optional[EmailStr]
    creationTime: Optional[int]
    labels: Optional[List[str]]

    class Config:
        schema_extra = {
            "example":    {
                "id": "21179ee2-cb21-560c-85ed-14f4909e1d01",
                "title": "Progressive Web Apps",
                "content": "Hey everyone, this is my example ticket...",
                "userEmail": "im2@ihi.vi",
                "creationTime": 1518867438530
            },
        }


class SearchTicketModel(BaseModel):
    id: Optional[str]
    title: Optional[str]
    content: Optional[str]
    userEmail: Optional[EmailStr]
    creationTime: Optional[int]
    labels: Optional[List[str]]

    class Config:
        schema_extra = {
            "example":    {
                "id": "21179ee2-cb21-560c-85ed-14f4909e1d01",
                "title": "Progressive Web Apps",
                "content": "Hey everyone, this is my example ticket...",
                "userEmail": "im2@ihi.vi",
                "creationTime": 1518867438530,
                "creationFrom": 1518867438525,
                "creationTo": 1518867438535,
            },
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}