from typing import List, Optional

from fastapi import APIRouter, Body, Query
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from app.server.database import (
    add_tickets,
    delete_ticket,
    retrieve_ticket,
    retrieve_tickets,
    retrieve_tickets_by_query,
    update_ticket,
)
from app.server.models.ticket import (
    ErrorResponseModel,
    ResponseModel,
    TicketSchema,
    UpdateTicketModel,
    SearchTicketModel,
)

router = APIRouter()


@router.post("/", response_description="Tickets data added into the database")
async def add_tickets_data(tickets: List[TicketSchema] = Body(...)):
    tickets = jsonable_encoder(tickets)
    new_tickets = await add_tickets(tickets)
    return ResponseModel(new_tickets, "Tickets added successfully.")


@router.get("/", response_description="Tickets retrieved")
async def get_tickets():
    tickets = await retrieve_tickets()
    if tickets:
        return ResponseModel(tickets, "Tickets data retrieved successfully")
    return ResponseModel(tickets, "Empty list returned")


@router.put("/{id}")
async def update_ticket_data(id: str, req: UpdateTicketModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_ticket = await update_ticket(id, req)
    if updated_ticket:
        return ResponseModel(
            "Ticket with ID: {} name update is successful".format(id),
            "Ticket name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the ticket data.",
    )


@router.delete("/{id}", response_description="Ticket data deleted from the database")
async def delete_ticket_data(id: str):
    deleted_ticket = await delete_ticket(id)
    if deleted_ticket:
        return ResponseModel(
            "Ticket with ID: {} removed".format(id), "Ticket deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Ticket with id {0} doesn't exist".format(id)
    )


@router.get("/search", response_description="Tickets retrieved by query")
async def search_tickets(title: Optional[str] = None,
                         content: Optional[str] = None,
                         userEmail: Optional[EmailStr] = None,
                         creationTime: Optional[int] = None,
                         creationFrom: Optional[int] = None,
                         creationTo: Optional[int] = None,
                         ):
    query = {}
    # Build the query based on the provided search values
    if title:
        query["title"] = title
    if content:
        query["content"] = content
    if userEmail:
        query["userEmail"] = userEmail
    if creationTime:
        query["creationTime"] = creationTime
    if creationFrom and creationTo:
        query["creationTime"] = {"$gte": creationFrom, "$lte": creationTo}
    # Search for tickets in the collection based on the query
    tickets = await retrieve_tickets_by_query(query)
    if tickets:
        return ResponseModel(tickets, "Tickets data retrieved successfully")
    return ResponseModel(tickets, "Empty list returned")

@router.get("/{id}", response_description="Ticket data retrieved")
async def get_ticket_data(id):
    ticket = await retrieve_ticket(id)
    if ticket:
        return ResponseModel(ticket, "Ticket data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Ticket doesn't exist.")
