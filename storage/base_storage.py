import os
import uuid
from abc import ABC, abstractmethod
import json
from fastapi import HTTPException, status

from pymongo import MongoClient

from schemas import NewTour, SavedTour
from settings import settings

class BaseStorage(ABC):
    @abstractmethod
    def create_tour(self, new_tour: NewTour) -> SavedTour:
        pass

    @abstractmethod
    def get_tour(self, tour_id: str) -> SavedTour:
        pass

    @abstractmethod
    def get_tours(
        self, q: str = "", limit: int = 10, skip: int = 0) -> list[SavedTour]:
        pass

    @abstractmethod
    def delete_tour(self, tour_id: str) -> None:
        pass


class MongoStorage(BaseStorage):
    def __init__(self, uri: str):
        client = MongoClient(uri)
        db = client.tour
        collection_tour = db.products
        self.collection_tour = collection_tour

    def create_tour(self, new_tour: NewTour) -> SavedTour:
        payload = {
            "price": new_tour.price,
            "title": new_tour.title,
            "description": new_tour.description,
            "tourist": new_tour.tourist,
            "tate_of_dispatch": new_tour.tate_of_dispatch,
            "tour_duration": new_tour.tour_duration,
            "type_room": new_tour.type_room,
            "services": new_tour.services,
            "cover": new_tour.cover,
            "id": uuid.uuid4().hex,
        }

        self.collection_tour.insert_one(payload)
        saved_product = SavedTour(**payload)
        return saved_product

    def get_tour(self, tour_id: str) -> SavedTour:
        query = {"id": tour_id}
        tour = self.collection_tour.find_one(query)
        if not tour:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return tour

    def get_tours(
        self, q: str = "", limit: int = 10, skip: int = 0
    ) -> list[SavedTour]:
        query = {}
        if q:
            query = {
                "$or": [
                    {
                        "title": {
                            "$regex": q,
                            "$options": "i",
                        }
                    },
                    {
                        "description": {
                            "$regex": q,
                            "$options": "i",
                        }
                    },
                ]
            }
        tours = self.collection_tour.find(query).limit(limit).skip(skip)
        return tours or []

    def delete_tour(self, tour_id: str) -> None:
        query = {"id": tour_id}
        self.collection_tour.delete_many(query)


class FileStorage(BaseStorage):
    def __init__(self, file_name: str):
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(self.file_name, mode="w") as file:
                json.dump([], file, indent=4)

    def create_tour(self, new_tour: NewTour) -> SavedTour:
        with open(self.file_name, mode="r") as file:
            content: list[dict] = json.load(file)
        payload = {
            "price": new_tour.price,
            "title": new_tour.title,
            "description": new_tour.description,
            "tourist": new_tour.tourist,
            "tate_of_dispatch": new_tour.tate_of_dispatch,
            "tour_duration": new_tour.tour_duration,
            "type_room": new_tour.type_room,
            "services": new_tour.services,
            "cover": new_tour.cover,
            "id": uuid.uuid4().hex,

        }
        content.append(payload)
        with open(self.file_name, mode="w") as file:
            json.dump(content, file, indent=4)
        # saved_product = SavedProduct(title=payload['title']...)
        saved_tour = SavedTour(**payload)
        return saved_tour


# storage: BaseStorage = FileStorage("storage.json")
storage: BaseStorage = MongoStorage(settings.MONGO_URI)