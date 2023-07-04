from typing import List

from bson.objectid import ObjectId
import motor.motor_asyncio
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.tickets

ticket_collection = database.get_collection("tickets_collection")


# helpers


def ticket_helper(ticket) -> dict:
    return {
        "id": str(ticket["id"]),
        "title": ticket["title"],
        "userEmail": ticket["userEmail"],
        "content": ticket["content"],
        "creationTime": ticket["creationTime"],
        "labels": ticket["labels"],
    }

# Retrieve tickets with a matching values

async def retrieve_tickets_by_query(data: dict):
    # Build the query based on the provided search criteria
    if len(data) < 1:
        return []
    tickets = []
    async for ticket in ticket_collection.find(data):
        tickets.append(ticket_helper(ticket))
    # return the matching tickets
    return tickets


# Retrieve all tickets present in the database
async def retrieve_tickets():
    tickets = []
    async for ticket in ticket_collection.find():
        tickets.append(ticket_helper(ticket))
    return tickets


# Add tickets into to the database
async def add_tickets(tickets_data: List[dict]):
    tickets = await ticket_collection.insert_many(tickets_data, ordered=False)
    new_tickets = await ticket_collection.find({"_id": {"$in": tickets.inserted_ids}}).to_list(length=None)
    return [ticket_helper(ticket) for ticket in new_tickets]


# Retrieve a ticket with a matching ID
async def retrieve_ticket(id: str) -> dict:
    ticket = await ticket_collection.find_one({"_id": ObjectId(id)})
    if ticket:
        return ticket_helper(ticket)


# Update a ticket with a matching ID
async def update_ticket(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    ticket = await ticket_collection.find_one({"_id": ObjectId(id)})
    if ticket:
        updated_ticket = await ticket_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_ticket:
            return True
        return False


# Delete a ticket from the database
async def delete_ticket(id: str):
    ticket = await ticket_collection.find_one({"_id": ObjectId(id)})
    if ticket:
        await ticket_collection.delete_one({"_id": ObjectId(id)})
        return True
