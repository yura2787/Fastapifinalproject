from fastapi import FastAPI

from schemas import NewTour, SavedTour
from storage.base_storage import storage

app = FastAPI()


@app.get("/")
def index():
    return {"status": "OK lll"}


@app.post("/tours/", tags=["Тур"])
def create_book(new_tour: NewTour) -> SavedTour:
    tour = storage.create_tour(new_tour)
    return tour


@app.get("/tour/{tour_id}")
def get_tour(tour_id: str) -> SavedTour:
    tour = storage.get_tour(tour_id)
    return tour

@app.get("/tours/")
def get_tours(query: str = "", limit: int = 10, skip: int = 0) -> list[SavedTour]:
    tours = storage.get_tours(q=query, limit=limit, skip=skip)
    return tours

@app.patch("/tours/{tour_id}")
def edit_tour(tour_id: str, data: dict):
    pass


@app.delete("/tours/{tour_id}")
def delete_tour(tour_id: str) -> dict:
    storage.delete_tour(tour_id)
    return {}

