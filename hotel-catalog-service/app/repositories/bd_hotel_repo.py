import traceback
import uuid
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.hotel import Hotel 
from app.schemas.hotel import Hotel as DHotel

class HotelRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, hotel: DHotel) -> Hotel:
        result = Hotel.from_orm(hotel)
        # if task.assignee is not 0:
        #     result.assignee = self.assignee_repo.get_assignee_by_id(
        #         task.assignee)

        return result

    def _map_to_schema(self, hotel: Hotel) -> DHotel:
        data = dict(hotel)
        del data['id']
        data['id'] = hotel.id if hotel.id is not 0 else 0
        result = DHotel(**data)
        return result

    def get_hotels(self) -> list[Hotel]:
        hotels = []
      
        for b in self.db.query(DHotel).all():
            hotels.append(self._map_to_model(b))
        return hotels

    def get_hotel_by_id(self, id: UUID) -> Hotel:
        hotel = self.db \
            .query(DHotel) \
            .filter(DHotel.id == id) \
            .first()

        if hotel is None:
            raise KeyError

        return Hotel.from_orm(hotel)

    def add_hotel(self, hotel: Hotel) -> Hotel:
        try:
            db_hotel = self._map_to_schema(hotel)
            self.db.add(db_hotel)
            self.db.commit()
            return self._map_to_model(db_hotel)
        except:
            traceback.print_exc()
            raise KeyError
