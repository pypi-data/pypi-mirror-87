#!/bin/env python

from decimal import Decimal

class MonthlyROI(object):

    _year = None
    _month = None
    _mortgage_payment = None
    _principal_paid = None
    _interest_paid = None
    _appreciated_price = None
    _tax = None
    _insurance = None
    _writeoff = None
    _net_worth_gain = None
    _appreciated_net_worth_gain = None
    _rent_equivalent = None
    _apppreciated_rent_equivalent = None
    _mortgage = None

    def __init__(self, year, month,
                 mortgage_payment, principal_paid,
                 interest_paid, appreciated_price,
                 tax, insurance, writeoff, net_worth_gain,
                 appreciated_net_worth_gain, rent_equivalent,
                 appreciated_rent_equivalent, mortgage):
        self._year = year
        self._month = month
        self._mortgage_payment = mortgage_payment
        self._principal_paid = principal_paid
        self._interest_paid = interest_paid
        self._appreciated_price = appreciated_price
        self._tax = tax
        self._insurance = insurance
        self._writeoff = writeoff
        self._net_worth_gain = net_worth_gain
        self._appreciated_net_worth_gain = appreciated_net_worth_gain
        self._rent_equivalent = rent_equivalent
        self._apppreciated_rent_equivalent = appreciated_rent_equivalent
        self._mortgage = mortgage

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def mortgage_payment(self):
        return self._mortgage_payment

    @property
    def principal_paid(self):
        return self._principal_paid

    @property
    def interest_paid(self):
        return self._interest_paid

    @property
    def appreciated_price(self):
        return self._appreciated_price

    @property
    def tax(self):
        return self._tax

    @property
    def insurance(self):
        return self._insurance

    @property
    def writeoff(self):
        return self._writeoff 

    @property
    def net_worth_gain(self):
        return self._net_worth_gain

    @property
    def appreciated_net_worth_gain(self):
        return self._appreciated_net_worth_gain

    @property
    def rent_equivalent(self):
        return self._rent_equivalent

    @property
    def appreciated_rent_equivalent(self):
        return self._apppreciated_rent_equivalent

    @property
    def mortgage(self):
        return self._mortgage

    def _str_(self):
        """
        @return string :
        @author
        """
        pass

    def header(self):
        """
        @return string :
        @author
        """
        pass
    def serialize_json(self):
        res = {
            'year': self.year,
            'month': self.month,
            'mortgage_payment': self.mortgage_payment,
            'principal_paid': self.principal_paid,
            'interest_paid': self.interest_paid,
            'appreciated_price': self.appreciated_price,
            'tax': self.tax,
            'insurance': self.insurance,
            'writeoff': self.writeoff,
            'net_worth_gain': self.net_worth_gain,
            'appreciated_net_worth_gain': self.appreciated_net_worth_gain,
            'rent_equivalent': self.rent_equivalent,
            'apppreciated_rent_equivalent': self.appreciated_rent_equivalent
        }
        for k in res:
            if type(res[k]) is Decimal:
                res[k]=float(res[k])
        return res

    def deserialize_json(self,data):
        pass