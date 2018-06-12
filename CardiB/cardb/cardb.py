from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import collate
from datetime import datetime
import os
from cardb import types
import json


class CarDB(object):

    def __init__(self):
        engine = create_engine(os.environ['DATABASE_URL'])
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_brand(self, name):
        brands = self.session.query(types.Brand).all()
        ex = self.session.query(
            types.Brand).filter(
            types.Brand.name == name).one_or_none()
        if ex is None:
            brand = types.Brand(name=name)
            self.session.add(brand)
            self.session.commit()
            return brand

    def delete_brand(self, id):
        brand = self.session.query(
            types.Brand).filter(
            types.Brand.id == id).one_or_none()
        if brand is not None:
            cars = self.session.query(
                types.Car).filter(
                types.Car.brand == brand.name).all()
            if len(cars) == 0:
                self.session.delete(brand)
                self.session.commit()
                return "Brand deleted"
            else:
                return "Cannot be removed"
        else:
            return "No such brand"

    def query_brands(self, filters):
        if filters == ():
            brands = self.session.query(
                types.Brand).order_by(
                types.Brand.id).all()
            return brands
        else:
            key = filters[0]
            value = filters[1]
            if key == "id":
                brand = self.session.query(
                    types.Brand).filter(
                    types.Brand.id == value).one_or_none()
                return [brand]
            elif key == "name":
                brand = self.session.query(
                    types.Brand).filter(
                    types.Brand.name == value).one_or_none()
                if brand is not None:
                    return [brand]
                else:
                    return "No such brand"

    def create_car(self, brand, model, **info):
        if isinstance(brand, types.Brand):
            car = types.Car(brand=brand.name, model=model, info=info)
            self.session.add(car)
            self.session.commit()
            return car
        elif isinstance(brand, int):
            br = self.session.query(
                types.Brand).filter(
                types.Brand.id == brand).one_or_none().name
            car = types.Car(brand=br, model=model, info=info)
            self.session.add(car)
            self.session.commit()
            return car
        else:
            brands = self.session.query(types.Brand).all()
            b = [b.name for b in brands]
            if brand in b:
                car = types.Car(brand=brand, model=model, info=info)
                self.session.add(car)
                self.session.commit()
                return car
            else:
                return "Integrity error"

    def delete_car(self, id):
        car = self.session.query(
            types.Car).filter(
            types.Car.id == id).one_or_none()
        if car is not None:
            self.session.delete(car)
            self.session.commit()
            return "Car deleted"

        else:
            return "No such car"

    def update_car(self, id, data):
        car = self.session.query(
            types.Car).filter(
            types.Car.id == id).one_or_none()
        brands = self.session.query(types.Brand).all()
        brands = [b.name for b in brands]
        if car is not None:
            keys = sorted(list(data.keys()))
            if "brand" in keys:
                if data["brand"] in brands:
                    car.brand = data["brand"]
                else:
                    return "Invalid brand"
            if "model" in keys:
                car.model = data["model"]
            if "info" in keys:
                car.info = data["info"]
            self.session.flush()
            self.session.commit()
            return "Update succesfull"
        else:
            return "No car to update"

    def query_cars(self, filters):
        if isinstance(filters, dict):
            filtered_cars = self.session.query(
                types.Car).filter(
                types.Car.info.contains(filters)).all()
            return filtered_cars
        else:
            if filters == []:
                all_cars = self.session.query(
                    types.Car).order_by(
                    types.Car.id).all()
                return all_cars
            else:
                if ":" not in filters and isinstance(filters, dict) == False:
                    filters = filters[0]
                    key = filters[0]
                    value = filters[1][0]
                    if key == "id":
                        filtered_car = self.session.query(types.Car).filter(
                            types.Car.id == value).one_or_none()
                        return [filtered_car]
                    elif key == "brand":
                        filtered_cars = self.session.query(
                            types.Car).filter(
                            types.Car.brand == value).all()
                        return filtered_cars
                    elif key == "model":
                        filtered_cars = self.session.query(
                            types.Car).filter(
                            types.Car.model == value).all()
                        return filtered_cars
                elif ":" in filters or isinstance(filters, dict):
                    filtered_cars = self.session.query(types.Car).filter(
                        types.Car.info.contains(filters)).all()
                    return filtered_cars
