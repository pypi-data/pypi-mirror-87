'''
给stageplan_utils.py模块使用
'''
from decimal import Decimal

def float_deal(args):
    return float('%.2f' %args)


if __name__ == '__main__':
    print(type(float_deal(Decimal('1000.00'))))
    print(float_deal(Decimal('1000.00')))