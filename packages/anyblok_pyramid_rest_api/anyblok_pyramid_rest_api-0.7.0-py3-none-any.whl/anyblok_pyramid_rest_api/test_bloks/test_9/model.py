# This file is a part of the AnyBlok / Pyramid / REST api project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import Integer, String
from anyblok.relationship import Many2One, Many2Many


Model = Declarations.Model


@Declarations.register(Declarations.Model)
class City:

    id = Integer(primary_key=True)
    name = String(nullable=False)
    zipcode = String(nullable=False)

    def __repr__(self):
        return '<City(name={self.name!r})>'.format(self=self)


@Declarations.register(Declarations.Model)
class Tag:

    id = Integer(primary_key=True)
    name = String(nullable=False)

    def __repr__(self):
        return '<Tag(name={self.name!r})>'.format(self=self)


@Declarations.register(Declarations.Model)
class Customer:
    id = Integer(primary_key=True)
    name = String(nullable=False)
    tags = Many2Many(model=Declarations.Model.Tag)

    def __repr__(self):
        return '<Customer(name={self.name!r}, tags={self.tags!r})>'.format(
            self=self)


@Declarations.register(Declarations.Model)
class Address:

    id = Integer(primary_key=True)
    street = String(nullable=False)
    city = Many2One(model=Declarations.Model.City, nullable=False)
    customer = Many2One(
        model=Declarations.Model.Customer, nullable=False,
        foreign_key_options={'ondelete': 'cascade'}, one2many="addresses")
