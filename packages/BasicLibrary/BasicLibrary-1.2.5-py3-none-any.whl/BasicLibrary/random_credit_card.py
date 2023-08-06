"""
gencc: A simple program to generate credit card numbers that pass the
MOD 10 check (Luhn formula).
Usefull for testing e-commerce sites during development.
Copyright 2003-2012 Graham King
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

目前该文件只是随机生成信用卡，引用方法：from BasicLibrary.random_credit_card import random_credit_no

返回格式为字符串
"""
# Different naming convention, because translated from PHP
# pylint: disable=C0103
from random import Random
import copy

visaPrefixList = [
    ['4', '5', '3', '9'],
    ['4', '5', '5', '6'],
    ['4', '9', '1', '6'],
    ['4', '5', '3', '2'],
    ['4', '9', '2', '9'],
    ['4', '0', '2', '4', '0', '0', '7', '1'],
    ['4', '4', '8', '6'],
    ['4', '7', '1', '6'],
    ['4']]
mastercardPrefixList = [
    ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]
amexPrefixList = [['3', '4'], ['3', '7']]
discoverPrefixList = [['6', '0', '1', '1']]
dinersPrefixList = [
    ['3', '0', '0'],
    ['3', '0', '1'],
    ['3', '0', '2'],
    ['3', '0', '3'],
    ['3', '6'],
    ['3', '8']]
enRoutePrefixList = [['2', '0', '1', '4'], ['2', '1', '4', '9']]
jcbPrefixList = [['3', '5']]
voyagerPrefixList = [['8', '6', '9', '9']]


def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """
    ccnumber = prefix
    # generate digits
    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)
    # Calculate sum
    sum = 0
    pos = 0
    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()
    while pos < length - 1:
        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9
        sum += odd
        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])
        pos += 2
    # Calculate check digit
    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append(str(checkdigit))
    return ''.join(ccnumber)


def credit_card_number(rnd, prefixList, length, howMany):
    result = []
    while len(result) < howMany:
        ccnumber = copy.copy(rnd.choice(prefixList))
        result.append(completed_number(ccnumber, length))
    return result


# def output(title, numbers):
#     result = []
#     result.append(title)
#     result.append('-' * len(title))
#     result.append('\n'.join(numbers))
#     result.append('')
#     return '\n'.join(result)

generator = Random()
generator.seed()  # Seed from current time
# print("darkcoding credit card generator\n")
mastercard = credit_card_number(generator, mastercardPrefixList, 16, 1)
# print(output("Mastercard", (mastercard)))

# 随机生成信用卡
random_credit_no = mastercard[0][0:16]