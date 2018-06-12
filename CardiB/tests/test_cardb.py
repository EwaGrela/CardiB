from cardb import types


def test_create_brand(cardb):
    mercedes = cardb.create_brand('Mercedes')
    assert isinstance(mercedes, types.Brand)
    assert isinstance(mercedes.id, int)
    assert mercedes.name == 'Mercedes'


def test_create_car(cardb):
    audi = cardb.create_brand('Audi')

    a5_info = {
        'first_production_year': 2007,
        'engines': [
            '1.8 TFSI',
            '2.0 TDI',
        ],
        'cabrio_avail': True,
    }
    audi_a5 = cardb.create_car(
        audi,
        'A5',
        **a5_info,
    )
    assert isinstance(audi_a5, types.Car)
    assert audi_a5.model == 'A5'
    assert audi_a5.brand == 'Audi'
    assert audi_a5.info == a5_info

    a3_info = {
        'first_production_year': 1996,
        'body_types': [
            '3-door hatchback',
            '5-door hatchback',
        ],
        'wheelbase': [
            'FWD',
            '4WD',
        ]
    }
    audi_a3 = cardb.create_car(
        audi.id,
        'A3',
        **a3_info,
    )
    assert audi_a3.id != audi_a5.id
    assert isinstance(audi_a3, types.Car)
    assert audi_a3.model == 'A3'
    assert audi_a3.brand == 'Audi'
    assert audi_a3.info == a3_info


def _create_vw(cardb):
    vw = cardb.create_brand('Volkswagen')
    golf_info = {
        'first_production_year': 1974,
        'wheelbase': [
            'FWD',
            '4WD',
        ]
    }
    golf = cardb.create_car(vw, 'Golf', **golf_info)

    passat_info = {
        'first_production_year': 1973,
        'wheelbase': [
            'FWD',
        ]
    }
    passat = cardb.create_car(vw, 'Passat', **passat_info)

    beetle_info = {
        'first_production_year': 1938,
    }
    cardb.create_car(vw, 'Beetle', **beetle_info)

    return golf, passat


# production year equal to 1973
def test_query_cars_1(cardb):
    golf, passat = _create_vw(cardb)
    res = cardb.query_cars({
        'first_production_year': 1973,
    })
    assert res[0].id == passat.id


# production year greater than 1980
def test_query_cars_2(cardb):
    golf, passat = _create_vw(cardb)
    res = cardb.query_cars({
        'first_production_year': {'gt': 1980}
    })
    assert len(res) == 0


# production year greater or equal to 1974
def test_query_cars_3(cardb):
    golf, passat = _create_vw(cardb)
    res = cardb.query_cars({
        'first_production_year': {'gte': 1974}
    })
    assert res[0].id == golf.id


# has 4WD or production year greater than or equal 1973
def test_query_cars_4(cardb):
    golf, passat = _create_vw(cardb)
    res = cardb.query_cars(
        {
            'or': [
                {'wheelbase': {'contains': '4WD'}},
                {'first_production_year': 1973}
            ]
        }
    )
    assert len(res) == 2
    ids = [c.id for c in res]
    assert golf.id in ids
    assert passat.id in ids
