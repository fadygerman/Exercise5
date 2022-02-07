from pytest import raises
from chocolate_discount import calculate_price
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

"""
vBVA1 stands for valid BVA of totals
iBVA1 stands for invalid BVA of totals
vBVA2 stands for valid BVA of dates
iBVA2 stands for invalid BVA of dates

Total:
1.    vBVA1_1: [0] -> 0                         
2.    vBVA1_2: [0.01] -> 0.01
3.    vBVA1_3: [0.02 - 49.98] -> 100/3 (33.33)
4.    vBVA1_4: [49.99] -> 49.99
5.    vBVA1_5: [50.00] -> 50
6.    vBVA1_6: [50.01] -> 50.01
7.    vBVA1_7: [50.02 - 99.98] -> 200/3 (66.67)
8.    vBVA1_8: [99.99] -> 99.99
9.    vBVA1_9: [100.00] -> 100
10.   vBVA1_10: [100.01] -> 100.01
11.   vBVA1_11: [100.02 - MAX] -> 300000.9999 (300001.00)
12.   iBVA1_1: [MIN - (-0.02)] -> (-3.34878)
13.   iBVA1_2: [-0.01] -> (-0.01)
14.   iBVA1_3: not of type Decimal -> String
Date:
15.   vBVA2_1: [(date(2022, 4, 9))] 
16.   vBVA2_2: [(date(2022, 4, 10))] 
17.   vBVA2_3: [(date(2022, 4, 11)) - (date(2022, 4, 16))] -> date(2022, 4, 13)
18.   vBVA2_4: [(date(2022, 4, 17))] 
19.   vBVA2_5: [(date(2022, 4, 18))] 
20.   iBVA2_1: [(date(2022, 4, 19))] 
21.   iBVA2_2: [(date(2022, 4, 8))] 
22.   iBVA2_3: [MIN_DATE - (date(2022, 4, 7))[ -> date(2022, 4, 5)
23.   iBVA2_4: [(date(2022, 4, 20)) - MAX_DATE] -> date(2022, 4, 25)
24.   iBVA2_5: not of type date -> String
"""

# VALID VALUES

list_total_valid = [0, 0.01, (100 / 3), 49.99, 50, 50.01, (200 / 3), 99.99, 100, 100.01, 300000.9999]

ltv_decimal = [Decimal(s).quantize(Decimal('0.01'), ROUND_HALF_UP) for s in list_total_valid]
# ltv stands for list total valid

ldv = [date(2022, 4, 9), date(2022, 4, 10), date(2022, 4, 13), date(2022, 4, 17), date(2022, 4, 18)]
# ldv stands for list date valid


# INVALID VALUES

list_total_invalid = [-3.34878, -0.01]

lti_decimal = [Decimal(s).quantize(Decimal('0.01'), ROUND_HALF_UP) for s in list_total_invalid]
# lti stands for list total invalid

ldi = [date(2022, 4, 19), date(2022, 4, 8), date(2022, 4, 5), date(2022, 4, 25)]
# ldi stands for list date invalid


# expected results
expected = [0, 0.0095, 31.6635, 47.4905, 47.5, 45.009, 60.003, 89.991, 90, 85.0085, 255000.85]
expected_decimal = [Decimal(s).quantize(Decimal('0.01'), ROUND_HALF_UP) for s in expected]


# test valid total values
def test_discount_vbva_1_1():
    """
    print("\n", pairs_valid_total_date)
    print(pairs_valid_total_date[3])
    print(pairs_valid_total_date[5][0])
    print(pairs_valid_total_date[30][1])
    print(pairs_valid_date_total)
    print(pairs_valid_date_total[3])
    print()
    print(pairs_valid_date_total[5][1])
    print(pairs_valid_date_total[30][0])
    print()
    print(expected_decimal)
    # """
    assert calculate_price(ltv_decimal[0], ldv[2]) == expected_decimal[0]


def test_discount_vbva_1_2():
    assert calculate_price(ltv_decimal[1], ldv[2]) == expected_decimal[1]


def test_discount_vbva_1_3():
    assert calculate_price(ltv_decimal[2], ldv[2]) == expected_decimal[2]


def test_discount_vbva_1_4():
    assert calculate_price(ltv_decimal[3], ldv[2]) == expected_decimal[3]


def test_discount_vbva_1_5():
    assert calculate_price(ltv_decimal[4], ldv[2]) == expected_decimal[4]


def test_discount_vbva_1_6():
    assert calculate_price(ltv_decimal[5], ldv[2]) == expected_decimal[5]


def test_discount_vbva_1_7():
    assert calculate_price(ltv_decimal[6], ldv[2]) == expected_decimal[6]


def test_discount_vbva_1_8():
    assert calculate_price(ltv_decimal[7], ldv[2]) == expected_decimal[7]


def test_discount_vbva_1_9():
    assert calculate_price(ltv_decimal[8], ldv[2]) == expected_decimal[8]


def test_discount_vbva_1_10():
    assert calculate_price(ltv_decimal[9], ldv[2]) == expected_decimal[9]


def test_discount_vbva_1_11():
    assert calculate_price(ltv_decimal[10], ldv[2]) == expected_decimal[10]


# test valid date values
def test_discount_vbva_2_1():
    assert calculate_price(ltv_decimal[6], ldv[0]) == expected_decimal[6]


def test_discount_vbva_2_2():
    assert calculate_price(ltv_decimal[6], ldv[1]) == expected_decimal[6]


def test_discount_vbva_2_3():
    assert calculate_price(ltv_decimal[6], ldv[2]) == expected_decimal[6]


def test_discount_vbva_2_4():
    assert calculate_price(ltv_decimal[6], ldv[3]) == expected_decimal[6]


def test_discount_vbva_2_5():
    assert calculate_price(ltv_decimal[6], ldv[4]) == expected_decimal[6]


# test invalid total values
def test_discount_ibva_1_1():
    with raises(Exception):
        calculate_price(lti_decimal[0], ldv[2])


def test_discount_ibva_1_2():
    with raises(Exception):
        calculate_price(lti_decimal[1], ldv[2])


def test_discount_ibva_1_3():
    with raises(Exception):
        calculate_price("lti_decimal[0]", ldv[2])


# test invalid date values
def test_discount_ibva_2_1():
    assert calculate_price(ltv_decimal[6], ldi[0]) == ltv_decimal[6]


def test_discount_ibva_2_2():
    assert calculate_price(ltv_decimal[6], ldi[1]) == ltv_decimal[6]


def test_discount_ibva_2_3():
    assert calculate_price(ltv_decimal[6], ldi[2]) == ltv_decimal[6]


def test_discount_ibva_2_4():
    assert calculate_price(ltv_decimal[6], ldi[3]) == ltv_decimal[6]


def test_discount_ibva_2_5():
    with raises(Exception):
        calculate_price(ltv_decimal[6], "ldi[0]")


# test mixed invalid total and date values

def test_discount_ibva_1():
    with raises(Exception):
        calculate_price("lti_decimal[1]", "ldi[0]")


def test_discount_ibva_2():
    with raises(Exception):
        calculate_price(lti_decimal[0], ldi[0])


def test_discount_ibva_3():
    with raises(Exception):
        calculate_price(lti_decimal[1], ldi[1])
