# coding=UTF-8
from Mortgage import *
from MonthlyROI import MonthlyROI


class ROI(object):
    """ ATTRIBUTES

    mortgage  (private)
    target_sell_price  (private)
    appreciation  (private)
    baseline_return  (private)
    investments  (private)
    property_tax  (private)
    property_insurance  (private)
    sale expences in % - realtor cut, house reconditioning etc.

    sale_expences  (private)

    end_date  (private)
        end date of investment. Could be mortgage early termination
    """

    def __init__(self,
                 mortgage,
                 target_sell_price,
                 appreciation,
                 baseline_return,
                 investments,
                 property_tax_rate,
                 property_insurance,
                 tax_rate,
                 sale_expences,
                 end_date=None):
        self._mortgage = mortgage
        self._target_sell_price = target_sell_price
        self._appreciation = appreciation
        self._baseline_return = baseline_return
        self._investments = investments
        self._property_tax = property_tax_rate
        self._property_insurance = property_insurance
        self._sale_expences = sale_expences
        self._end_date = end_date
        self._tax_rate=tax_rate

    @property
    def mortgage(self):
        return self._mortgage

    @property
    def target_sell_price(self):
        return self._target_sell_price

    @property
    def appreciation(self):
        return self._appreciation

    @property
    def baseline_return(self):
        return self._baseline_return

    @property
    def investments(self):
        return self._investments

    @property
    def sale_expenses(self):
        return self._sale_expences

    @property
    def property_tax(self):
        return self._property_tax

    @property
    def property_insurance(self):
        return self._property_insurance

    @property
    def tax_rate(self):
        return self._tax_rate

    def __call__(self, start_month=0, already_paid=0):
        house_tax_monthly = float(self.mortgage.house_price) * self.property_tax / 12
        insurance_monthly = self.property_insurance / 12
        write_off_gain = 0
        principal_remaining = float(self.mortgage.principal)

        principal_paid = float(0)
        interest_paid = float(0)
        insurance_paid = float(0)
        mortgage_paid = float(0)
        # house_tax_paid=float(0)
        target_net_worth = self.baseline_return + self.investments

        year = 0
        month = 0

        total_paid = already_paid

        for index, payment in enumerate(self.mortgage.payments()):
            principal, interest = payment.principal, payment.interest
            mortgage_month = payment.period
            month = (mortgage_month % 12) + 1
            year = (mortgage_month / 12)
            mortgage_paid += float(principal) + float(interest)
            principal_remaining -= float(principal)
            principal_paid += float(principal)
            interest_paid += float(interest)

            month_appreciation_delta = month * \
                float(self.mortgage.house_price) * (self.appreciation **
                                                    (year - 1)) * (self.appreciation - 1) / 12
            appreciated_price = float(self.mortgage.house_price) * \
                (self.appreciation**(year)) + month_appreciation_delta
            house_tax_monthly = float(appreciated_price) * self.property_tax / 12

            monthly_writeoff_gain = (float(interest) + float(house_tax_monthly)) * self.tax_rate

            # house_tax_paid+=house_tax_monthly
            insurance_paid += insurance_monthly
            write_off_gain += monthly_writeoff_gain

            # net_worth_gain=self.target_sell_price*0.93-principal_remaining-target_net_worth-house_tax_paid-insurance_paid+write_off_gain
            net_worth_gain = self.target_sell_price * \
                (1 - self.sale_expenses) - principal_remaining - target_net_worth + write_off_gain

            # appreciated_net_worth_gain=appreciated_price*0.93-principal_remaining-target_net_worth-house_tax_paid-insurance_paid+write_off_gain
            appreciated_net_worth_gain = appreciated_price * \
                (1 - self.sale_expenses) - principal_remaining - target_net_worth + write_off_gain

            total_paid += float(house_tax_monthly) +\
                float(principal) +\
                float(interest) +\
                float(insurance_monthly) -\
                float(monthly_writeoff_gain)
            monthly_cost = (total_paid + self._investments - net_worth_gain) / (mortgage_month + 1)
            monthly_cost_appreciated = (total_paid + self._investments -
                                        appreciated_net_worth_gain) / (mortgage_month + 1)
            # all_paid_monthly (mortgage+tax+insurance)
            # principal_remaining
            # sale_gain (surplus_money-insurance_paid-house_tax_paid)
            # net_worth_gain (surplus_money)
            # appreciated_net_worth_gain (surplus_money+potential_price_gain)
            mroi=MonthlyROI(
                year=year, month=month,
                mortgage_payment=principal+interest,
                principal_paid=principal_paid,
                interest_paid=interest_paid,
                appreciated_price=appreciated_price,
                tax=house_tax_monthly,
                insurance=insurance_monthly,
                writeoff=monthly_writeoff_gain,
                net_worth_gain=net_worth_gain,
                appreciated_net_worth_gain=appreciated_net_worth_gain,
                rent_equivalent=monthly_cost,
                appreciated_rent_equivalent=monthly_cost_appreciated,
                mortgage=self.mortgage
            )

            yield mroi
