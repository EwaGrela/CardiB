from cardb import types

def test_query_cars5(cardb):
    brand = cardb.create_brand("Brand")
    info = {
        "production_year": 2013,
        "number_of_engines": 2
    }
    car = cardb.create_car(brand, "Model", **info)
    res = cardb.query_cars(filters=info)
    assert res is not None
    assert res[0] == car
    assert res[0].brand == "Brand"


def test_query_cars6(cardb):
    info = {"production_year": 2013}
    car = cardb.create_car("Audi", "ModelSamochodu", **info)
    res = cardb.query_cars(filters=[("id", [str(car.id)])])
    assert res is not None
    assert res[0].id == car.id


def test_query_brands1(cardb):
    brand = cardb.create_brand("NewBrand")
    res = cardb.query_brands(filters=("id", brand.id))
    info = {
        "engines_type": 1
    }
    car = cardb.create_car(brand, "Model123", **info)
    assert res is not None
    assert res[0] == brand
    assert res[0].id == brand.id
    assert car.brand == brand.name


def test_query_brands2(cardb):
    brand = cardb.create_brand("NewBrand2")
    res = cardb.query_brands(filters=("name", brand.name))
    info = {
        "engines_type": 32,
        "production_year": 1998
    }
    car = cardb.create_car(brand, "Model321", **info)
    assert res is not None
    assert car.brand == brand.name
    assert res[0].name == "NewBrand2"


def test_delete_car1(cardb):
    new_brand = cardb.create_brand("Brand1")
    new_car_info = {
        "production_year": 2015
    }
    new_car = cardb.create_car(new_brand, "NewModel", **new_car_info)
    cardb.delete_car(new_car.id)
    res = cardb.query_cars(filters=("id", new_car.id))
    assert res is None


def test_delete_car2(cardb):
    new_info = {
        "production_year": 2005,
        "hatchback": True
    }
    new_brand2 = cardb.create_brand("Brand2")
    new_car2 = cardb.create_car(new_brand2, "SpecialAudi", **new_info)
    cardb.delete_car(new_car2.id)
    res = cardb.query_cars(filters=("brand", new_brand2))
    assert res is None


def test_delete_brand1(cardb):
    new_brand = cardb.create_brand("Brand3")
    cardb.delete_brand(new_brand.id)
    res = cardb.query_brands(filters=("id", new_brand.id))
    assert res[0] is None


def test_update_car(cardb):
    info = {
        "production_year": 2000
    }
    car = cardb.create_car("Audi", "AudiSuper", **info)
    data = {"brand": "Volkswagen", "model": "EvenMoreSuper"}
    res = cardb.update_car(car.id, data)
    assert car is not None
    assert car.model == "EvenMoreSuper"
    assert car.brand == "Volkswagen"


def test_update_car2(cardb):
    info = {"first_production_year": 2018}
    car = cardb.create_car("Audi", "A666", **info)
    data = {"brand": "DifferentBrand", "model": "A667"}
    res = cardb.update_car(car.id, data)
    assert car.brand == "Audi"
    assert car.model == "A666"
