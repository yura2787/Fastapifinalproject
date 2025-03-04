from fastapi import FastAPI
from fastapi import FastAPI, status, Request, Form
from fastapi.templating import Jinja2Templates
from schemas import NewTour, SavedTour, PatchTour
from storage.base_storage import storage


app = FastAPI()

templates = Jinja2Templates(directory="templates")



@app.get("/")
@app.post("/")
def index(request: Request, q: str = Form(default=""),limit: int = 10, skip: int = 0):
    tours = storage.get_tours(q=q, limit=limit, skip=skip)
    context = {"request": request, "tours": tours}
    return templates.TemplateResponse(
        "index.html",
        context=context,
    )

@app.get("/map_route")
def map_route(request: Request):

    context = {"request": request}
    return templates.TemplateResponse(
        "map.html",
        context=context,
    )


@app.get("/video")
def video(request: Request):

    context = {"request": request}
    return templates.TemplateResponse(
        "video.html",
        context=context,
    )

@app.get("/{tour_id}")
def get_tour_info(request: Request, tour_id: str):
    tour = storage.get_tour(tour_id=tour_id, with_raise=False)
    if not tour:
        return templates.TemplateResponse(
            "404.html",
            context={"request": request},
        )

    context = {"request": request, "tour": tour}
    return templates.TemplateResponse(
        "details.html",
        context=context,
    )


@app.post("/tours/", tags=["Тур"], status_code=status.HTTP_201_CREATED)
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
def edit_tour(tour_id: str, data: PatchTour) -> SavedTour:
    tour = storage.patch_tour(tour_id, data)
    return tour



@app.delete("/tours/{tour_id}")
def delete_tour(tour_id: str) -> dict:
    storage.delete_tour(tour_id)
    return {}

