import os
from dataclasses import dataclass, field
from typing import Text

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from mortar import persist, metadata


@persist
@dataclass
class Driver(object):
    driver_id: int = field(metadata=Column(Integer, primary_key=True), default=None)
    Name: Text = field(default=None)
    age: int = field(default=None)


@persist
@dataclass
class Car(object):
    Id: int = field(metadata=Column(Integer, primary_key=True))
    Name: Text
    Price: int
    driver: Driver = field(default=None)


if __name__ == "__main__":
    try:
        os.remove('cars.sqlite')
    except:  ...
    metadata.engine('sqlite:///cars.sqlite')

    Car.truncate()
    Driver.truncate()
    dave = Driver(1, 'Dave', 34)
    lnone_car = Car(Id=1, Name='Audi', Price=52642)
    lnone_car.driver = dave
    print(lnone_car)
    metadata.add_all(
        [lnone_car,
            Car(Id=2, Name='Mercedes', Price=57127),
            Car(Id=3, Name='Skoda', Price=9000, driver=dave),
            Car(Id=4, Name='Volvo', Price=29000, driver=dave),
            Car(Id=5, Name='Bentley', Price=350000, driver=dave),
            Car(Id=6, Name='Citroen', Price=21000),
            Car(Id=7, Name='Hummer', Price=41400),
            Car(Id=8, Name='Volkswagen', Price=21600, driver=dave)])

    rs = metadata.query(Car).all()

    for car in rs:
        print(car.driver)

    metadata(Car).delete()
