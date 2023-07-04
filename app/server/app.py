from fastapi import FastAPI

from app.server.routes.ticket import router as TicketRouter

app = FastAPI()

app.include_router(TicketRouter, tags=["Ticket"], prefix="/tickets")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hi Wix! Welcome to my ticket app!"}
