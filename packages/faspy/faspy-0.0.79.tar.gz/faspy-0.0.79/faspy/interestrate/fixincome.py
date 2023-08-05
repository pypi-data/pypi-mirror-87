#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 09:57:01 2020

@author: RMS671214
"""

from numpy import datetime64 as dt64
import numpy as np
from .rmp_dates import generate_dates as gen_dates, \
    frequencies as fre,  day_count_factor as day_cf
from .conventions import start_basis
from .rmp_curves import interpolation, calc_shortrate_from_df, \
calc_df_from_shortrate, calc_fwd_df
from collections import deque


def fixbond_structures(bonds):
    """
    Generate bonds coupon structures.

            Parameters:
                bonds: a dictionary with the following keys - value_date,
                business_day, issue_date, value_date, maturity,
                frequency, day_count, date_generation, face_value, coupon,
                ytm and type.

            Returns:
                a dictionary with the following keys - date, dcf, time,
                days, df, rate
    """
    if isinstance(bonds, dict):
        results = list(_fixbond_gen_structure(bonds))

    elif isinstance(bonds, list):
        results = []
        for bond in bonds:
            if isinstance(bond, dict):
                results.append(list(_fixbond_gen_structure(bond)))

    return results


def _fixbond_gen_structure(bond):
    dates = _dates_gen_structure(bond)
    dates = deque(dates)

    noofcpns = len(dates)
    for no in range(noofcpns):
        structure = {}
        structure["cpn_dcf"] = day_cf(bond["day_count"],
                                      dates[no]["start_date"],
                                      dates[no]["end_date"],
                                      bondmat_date=bond["maturity"],
                                      next_coupon_date=dates[no]["end_date"],
                                      business_day=bond["business_day"],
                                      Frequency=bond["frequency"])
        structure["coupon"] = bond["coupon"]
        structure["face_value"] = bond["face_value"]
        structure["coupon_interest"] = (structure["cpn_dcf"] *
                                        structure["coupon"] *
                                        structure["face_value"] / 100)
        if no != noofcpns - 1:
            structure["fv_flow"] = 0
        else:
            structure["fv_flow"] = structure["face_value"]
        structure["cash_flow"] = (structure["coupon_interest"] +
                                  structure["fv_flow"])

        dates[no].update(structure) # merging the dictionary

    if (bond.get("ytm") and bond["value_date"]):
        fixbond_value(bond["value_date"], dates, bond["ytm"], bond["day_count"],
                      bond["frequency"])

    return dates


def fixbond_value(value_date, structures, yld, day_count, frequency):
    """
    Revalue the bond.

            Parameters:
                value_date: numpy.datetime64.
                structures: a list of dictionaries with the following keys: value_date, start_date, end_date, face_value, coupon, coupon_interest and cpn_dcf. The list must be sorted in ascending order by either start_date or end_date. In the absence of coupon_interest and cpn_dcf, they will be calculated
                day_count: str
                frequeny: str
            Returns:
                a dictionary with the following keys - value_date, start_date, end_date, face_value, coupon, coupon_interest and cpn_dcf, ytm_df, period_df, accrued, df, and pv
    """
    try:
        ytm = float(yld)
    except Exception:
        return
    newstructures = [ dict(x) for x in structures]

    maturity = newstructures[-1]["end_date"]
    # Calculate the periodic discount factor, accrued interest
    for structure in newstructures:
        if structure["start_date"] >= value_date:
            structure["ytm_dcf"] = day_cf(day_count,
                                          structure["start_date"],
                                          structure["end_date"],
                                          bondmat_date=maturity,
                                          next_coupon_date=structure["end_date"],
                                          Frequency=frequency)
            structure["period_df"] = 1 / (1 + structure["ytm_dcf"] * ytm / 100)
            structure["accrued"] = 0.00

        elif structure["end_date"] <= value_date:
            structure["ytm_dcf"] = 0.00
            structure["period_df"] = 0.00
            structure["accrued"] = 0.00
        else:
            structure["ytm_dcf"] = day_cf(day_count,
                                          value_date,
                                          structure["end_date"],
                                          bondmat_date=maturity,
                                          next_coupon_date=structure["end_date"],
                                          Frequency=frequency)
            structure["period_df"] = 1 / (1 + structure["ytm_dcf"] * ytm / 100)
            structure["accrued"] = (structure["ytm_dcf"] *
                                    structure["coupon_interest"] /
                                    structure["cpn_dcf"])
    # Calculate the discount factor, present value
    df = 1
    for structure in newstructures:
        if structure["period_df"] == 0.00:
            structure["pv"] = 0.00
            structure["df"] = 0.00
        else:
            df = structure["df"] = df * structure["period_df"]
            structure["pv"] = structure["cash_flow"] * df
    return newstructures


def date_structures(bonds):
    """
    Generate coupon structures.

            Parameters:
                bonds: a dictionary with the following keys - value_date,
                business_day, issue_date, value_date, maturity,
                frequency, day_count, date_generation, face_value, coupon,
                ytm and type.

            Returns:
                a dictionary with the following keys - date, dcf, time,
                days, df, rate
    """
    if isinstance(bonds, dict):
        results = _dates_gen_structure(bonds)

    elif isinstance(bonds, list):
        results = []
        for bond in bonds:
            if isinstance(bond, dict):
                results.append(_dates_gen_structure(bond))

    return results


def _dates_gen_structure(bond):
    """
    Generate date structures. Function can be used for all coupon bearing products with bullet principal repayment

            Parameters:
                bonds: a dictionary with the following keys - value_date,
                business_day, issue_date, value_date, maturity,
                frequency, day_count, date_generation.

            Returns:
                a dictionary or an array of dictionaries with the following keys - "start_date" and "end_date"
    """
    bus_day = None
    if bond['business_day'] == 'NULL':
        bus_day = 'No Adjustment'
    else:
        bus_day = bond['business_day']


    start_date = bond.get('issue_date')
    if start_date is not None:
        start_date = dt64(start_date, 'D')
    value_date = bond.get('value_date')

    if value_date is not None:
        value_date = dt64(value_date, 'D')
    if start_date is not None and value_date is not None:
        use_date = start_date
    elif start_date is not None:
        use_date = start_date
    elif value_date is not None:
        use_date = value_date
    else:
        raise Exception('Both value_date and issue_date do not have any value')
    # dates is a deque
    dates = gen_dates(use_date, bond['maturity'], issueDate=start_date,
                      frequency=fre[bond['frequency']],
                      business_day=bus_day, method=bond['date_generation'])

    start_dates = deque(dates)
    end_dates = deque(dates)
    start_dates.pop()
    end_dates.popleft()
    noofcpns = len(start_dates)
    structures = deque()
    for no in range(noofcpns):
        structure = {"start_date": start_dates[no], "end_date": end_dates[no]}
        structures.append(structure)

    newstructure = list(map(lambda sdate, edate: {"start_date": sdate, "end_date": edate}, start_dates, end_dates))

    return newstructure


def floatbond_structures(bonds, holidays=[]):
    """
    Generate bonds coupon structures.

            Parameters:
                bonds: a dictionary with the following keys - value_date,
                business_day, issue_date, value_date, maturity,
                frequency, day_count, date_generation, face_value,
                current_coupon, margin, fixing_basis, market_spread.

            Returns:
                a dictionary with the following keys - date, dcf, time,
                days, df, rate
    """
    if isinstance(bonds, dict):
        results = _floatbond_gen_structures(bonds, holidays=holidays,)

    elif isinstance(bonds, list):
        results = []
        for bond in bonds:
            if isinstance(bond, dict):
                results.append(_floatbond_gen_structures(bond,
                                                         holidays=holidays))
    return results


def _floatbond_gen_structures(bond, holidays=[]):
    bdc = np.busdaycalendar(weekmask='1111100', holidays=holidays)
    # generate the face value and coupons
    dates = _coupon_gen_structure(bond)
    dates = [{"start_date": date["start_date"], "end_date": date["end_date"]}
             for date in dates if date["end_date"] > bond["value_date"]]

    for date in dates:
        offset = -start_basis[bond["fixing_basis"]]
        date["fixing_date"] = np.busday_offset(date["start_date"], offset,
                                               roll='backward', busdaycal=bdc)
        date["face_value"] = bond["face_value"]
        date["margin"] = bond["margin"]
        date["cpn_dcf"] = day_cf(bond["day_count"],
                                 date["start_date"],
                                 date["end_date"],
                                 bondmat_date=bond["maturity"],
                                 next_coupon_date=date["end_date"],
                                 business_day=bond["business_day"],
                                 Frequency=bond["frequency"])
        # fixing date is a forward date
        if date["fixing_date"] > bond["value_date"]:
            date["is_fixed"] = False

        # fixing date is for the current coupon period
        elif (date["fixing_date"] <= bond["value_date"] and
              date["end_date"] > bond["value_date"]):
            date["is_fixed"] = True
            date["coupon"] = bond["current_coupon"]
            date["coupon_interest"] = (date["cpn_dcf"] *
                                       date["coupon"] *
                                       date["face_value"] / 100)
        date["fv_flow"] = 0
    dates[-1]["fv_flow"] = bond["face_value"]

    return dates


def floatbond_value(value_date, structures, spread, day_count, df_func=None,
                    dfs=None):
    if df_func is not None:
        ifunc = df_func
    elif dfs is not None:
        x_axis = [x["times"] for x in dfs]
        y_axis = [x["df"] for x in dfs]
        ifunc = interpolation(x_axis, y_axis, 1.00, is_function=True)
    else:
        return None

    datum = structures[0]
    df = 1
    if datum["is_fixed"] is True:
        time = day_cf("Actual/365", value_date, datum["end_date"])
        calc_df = ifunc(time)
        rate = calc_shortrate_from_df(value_date, datum["end_date"],
                                             calc_df, day_count)
        adj_rate = rate + spread
        adj_df = calc_df_from_shortrate(value_date, datum["end_date"],
                                               adj_rate, day_count)
        datum["fwd_df"] = adj_df
        df = df * adj_df
        datum["df"] = df
        datum["pv"] = datum["df"] * (datum["coupon_interest"] +
                                     datum["fv_flow"])
        acc_time = day_cf(day_count, value_date, datum["start_date"])
        datum["accrued"] = datum["coupon_interest"] * acc_time / datum["cpn_dcf"]

    for datum in structures:
        if datum["is_fixed"] is False:
            stime = day_cf("Actual/365", value_date, datum["start_date"])
            etime = day_cf("Actual/365", value_date, datum["end_date"])
            fwd_df = calc_fwd_df(stime, etime, ifunc=ifunc)
            ref_rate = calc_shortrate_from_df(datum["start_date"],
                                                     datum["end_date"],
                                                     fwd_df, day_count)
            datum["coupon"] = ref_rate + datum["margin"]
            datum["coupon_interest"] = (datum["cpn_dcf"] *
                                        datum["coupon"] *
                                        datum["face_value"] / 100)
            adj_refrate = ref_rate + spread
            adj_df = calc_df_from_shortrate(datum["start_date"],
                                                   datum["end_date"], adj_refrate,
                                                   day_count)
            datum["fwd_df"] = adj_df
            df = df * adj_df
            datum["df"] = df
            datum["pv"] = datum["df"] * (datum["coupon_interest"] + datum["fv_flow"])
            datum["accrued"] = 0

    return structures


def floatbond_value2(value_date, structures, day_count, ref_df, market_df):

    ref_x_axis = [x["times"] for x in ref_df]
    ref_y_axis = [x["df"] for x in ref_df]
    ref_func = interpolation(ref_x_axis, ref_y_axis, 1.00, is_function=True)

    m_x_axis = [x["times"] for x in market_df]
    m_y_axis = [x["df"] for x in market_df]
    m_func = interpolation(m_x_axis, m_y_axis, 1.00, is_function=True)

    datum = structures[0]

    if datum["is_fixed"] is True:
        time = day_cf("Actual/365", value_date, datum["end_date"])
        m_df = m_func(time)

        datum["df"] = m_df
        datum["pv"] = datum["df"] * (datum["coupon_interest"] +
                                     datum["fv_flow"])
        acc_time = day_cf(day_count, value_date, datum["start_date"])
        datum["accrued"] = datum["coupon_interest"] * acc_time / datum["cpn_dcf"]

    for datum in structures:
        if datum["is_fixed"] is False:
            stime = day_cf("Actual/365", value_date, datum["start_date"])
            etime = day_cf("Actual/365", value_date, datum["end_date"])
            fwd_df = calc_fwd_df(stime, etime, ifunc=ref_func)
            ref_rate = calc_shortrate_from_df(datum["start_date"],
                                                     datum["end_date"],
                                                     fwd_df, day_count)
            datum["coupon"] = ref_rate + datum["margin"]
            datum["coupon_interest"] = (datum["cpn_dcf"] *
                                        datum["coupon"] *
                                        datum["face_value"] / 100)
            m_df = m_func(etime)
            datum["df"] = m_df
            datum["pv"] = datum["df"] * (datum["coupon_interest"] + datum["fv_flow"])
            datum["accrued"] = 0

    return structures


def loans_structures(loans):
    """
    Generate loan schedule.

            Parameters:
                loans: a dictionary with the following keys - value_date,
                business_day, start_date, value_date, maturity,
                frequency, day_count, date_generation, face_value, rate,
                rate_type and rate_compounding.

            Returns:
                a dictionary with the following keys - date, dcf, time,
                days, df, rate
    """

    if isinstance(loans, dict):
        results = _loan_gen_structure(loans)

    elif isinstance(loans, list):
        results = []
        for loan in loans:
            if isinstance(loan, dict):
                results.append(_fixbond_gen_structure(loan))

    return results


def fixleg_dates(fixedleg):
    """
    Generate date structures. Function can be used for all coupon bearing products with bullet principal repayment

            Parameters:
                bonds: a dictionary with the following keys - value_date,
                business_day, issue_date, value_date, maturity,
                frequency, day_count, date_generation, face_value, coupon,
                ytm and type.

            Returns:
                a dictionary with the following keys - date, dcf, time,
                days, df, rate
    """
    if isinstance(bonds, dict):
        results = _coupon_gen_structure(bonds)

    elif isinstance(bonds, list):
        results = []
        for bond in bonds:
            if isinstance(bond, dict):
                results.append(_coupon_gen_structure(bond))

    return results


def _loan_gen_structure(loan):
    value_date = loan.get("value_date")
    structures = _coupon_gen_structure(loan)
    if loan["rate_type"] == "fixed":
        for structure in structures:
            pass
    elif loan["rate_type"] == float:
        pass

    return structures


def calc_customfix_structures(structures, day_count, frequency, business_day):
    """
    Calculate all the values of the custome structure.

            Parameters:
                value_date: numpy.datetime64.
                structures: a list of dictionaries with the following keys: start_date, end_date, face_value, coupon, fv_flow.
                day_count: str
                frequeny: str
            Returns:
                a dictionary with the following keys - value_date, start_date, end_date, face_value, coupon, coupon_interest, cash_flow and cpn_dcf.
    """

    for structure in structures:
        structure["cpn_dcf"] = day_cf(day_count,
                                      structure["start_date"],
                                      structure["end_date"],
                                      bondmat_date=structure["end_date"],
                                      next_coupon_date=structure["end_date"],
                                      business_day=business_day,
                                      Frequency=frequency)

        structure["coupon_interest"] = (structure["cpn_dcf"] *
                                        structure["coupon"] *
                                        structure["face_value"] / 100)
        if structure.get("fv_flow"):
            structure["cash_flow"] = (structure["coupon_interest"] +
                                            structure["fv_flow"])
        else:
            structure["fv_flow"] = 0.00
            structure["cash_flow"] = (structure["coupon_interest"])

    return structures


def value_customfix_structures(value_date, structures, day_count, frequency, dis_curve):
    """
    Calculate all the values of the custome structure.

            Parameters:
                value_date: numpy.datetime64.
                structures: a list of dictionaries with the following keys: start_date, end_date, face_value, coupon and fv_flow.
                day_count: str
                frequeny: str
                dis_curve: list of ditionaries with the following keys: time and df
            Returns:
                a dictionary with the following keys - value_date, start_date, end_date, face_value, coupon, coupon_interest, cash_flow and cpn_dcf.
    """
    newstructures = [dict(x) for x in structures]

    if isinstance(dis_curve, list):
        xaxis = [x["times"] for x in dis_curve]
        yaxis = [x["df"] for x in dis_curve]
        ifunc = interpolation(xaxis, yaxis, 1, model='chip', is_function=True)

    for structure in newstructures:
        temp_structure = {}
        temp_structure["cpn_dcf"] = day_cf(day_count,
                                      structure["start_date"],
                                      structure["end_date"],
                                      bondmat_date=structure["end_date"],
                                      next_coupon_date=structure["end_date"],
                                      Frequency=frequency)

        temp_structure["coupon_interest"] = (temp_structure["cpn_dcf"] *
                                        structure["coupon"] *
                                        structure["face_value"] / 100)
        if structure.get("fv_flow"):
            temp_structure["cash_flow"] = (temp_structure["coupon_interest"] +
                                            structure["fv_flow"])
        else:
            structure["fv_flow"] = 0.00
            temp_structure["cash_flow"] = (temp_structure["coupon_interest"])
        temp_structure["time"] = float(day_cf(day_count,
                                      value_date,
                                      structure["end_date"]))
        structure.update(temp_structure) # merging the dictionary

    # Discount curve was provided
    if isinstance(dis_curve, list):
        for structure in newstructures:
            if structure["time"] > 0:
                structure["df"] = float(ifunc(structure["time"]))
                structure["pv"] = structure["df"] * structure["cash_flow"]
            else:
                structure["df"] = 0
                structure["pv"] = 0
        #if (structure["start_date"] < value_date and structure["end_date"] > value_date):
        #    accrued_dcf = day_cf(day_count, structure["start_date"],
        #                value_date, bondmat_date=newstructures[-1]["end_date"], next_coupon_date=structure["end_date"] )
        #    cpn_dcf = day_cf(day_count, structure["start_date"],
        #                structure["end_date"] , bondmat_date=newstructures[-1]["end_date"], next_coupon_date=structure["end_date"] )
        #    accrued = accrued_dcf/cpn_dcf * structure[]
    # yield to maturity was provided instead
    elif isinstance(dis_curve, float):
        newstructures = fixbond_value(value_date, newstructures, dis_curve, day_count, frequency)

    return newstructures


def create_structures_from_dates(dates, coupons, face_values, fv_flows):
    """
    Create structures from date.

            Parameters:
                dates: list of dict with the following keys - start_date and
                end_date
                coupons: list of float.
                face_values: list of float
                fv_flows: list of float.

            Returns:
                list of dictionaries with the following keys - start_date, end_date, coupon, face_value, fv_flow
    """

    structures = list(map( lambda date, coupon, face_value, fv_flow: {"start_date": date["start_date"], "end_date": date["end_date"], "coupon": coupon, "face_value": face_value, "fv_flow": fv_flow}, dates, coupons, face_values, fv_flows))

    return structures
