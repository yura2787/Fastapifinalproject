from pydantic import BaseModel, Field


class NewTour(BaseModel):
    price: float = Field(ge=500, lt=1500, examples=[500, 1500])
    title: str = Field(
        min_length=3, examples=["Єгипет.Хургада"]
    )
    description: str = Field(
        min_length=50,
        max_length=1024,
        examples=[
            "Готель розташований в місті Хургада. Відвідвачі готелю можуть насолоджуватися туром по визначним місцям міста:"
            " Океанаріум «Гранд-Акваріум» в Хургаді та District Court of Hurghada. Підходить для молодіжного відпочинку."
        ],
    )
    tourist: float = Field(ge=1, lt=5, examples=[2])
    tate_of_dispatch: str = Field(min_length=3, max_length=500, examples=['12 березня'])
    tour_duration: float = Field(ge=1, lt=30, examples=[7])
    type_room: str = Field(min_length=5, max_length=200, examples=['STANDARD DOPPEL ZIMMER'])
    services: str = Field(min_length=5, max_length=200, examples=['+Трансфер -Страховка -Вiза'])

    cover: str = Field(
        examples=[
            "https://cdn.coraltravel.ua/content/egypt/img-2_1.jpg"
        ]
    )

class TourId(BaseModel):
    id: str

class SavedTour(TourId, NewTour):
    pass
