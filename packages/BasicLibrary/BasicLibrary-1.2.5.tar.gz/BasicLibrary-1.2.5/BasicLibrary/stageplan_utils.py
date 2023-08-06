'''
Documentation: 生成等额本息,按月付息还款计划
引用包名是：BasicLibrary   引用本python文件，请使用 from BasicLibrary.stageplan_utils import StagePlanUtils
使用方法：StagePlanUtils('1000','0.16').get_MCEI(6)  # 等额本息,按月付息  传入参数为：金额、利率、期数
返回为：每一期的还款详情展示，返回数据格式为：[{1:(x,x,x)},{2:(x,x,x)},...]
'''

from decimal import Decimal
from prettytable import PrettyTable
import copy
from BasicLibrary.deal_float import float_deal  # Decimal格式

class StagePlanUtils:
    def __init__(self,principal,annual_rate):
        self.principal = Decimal(principal)  # 本金
        self.annual_rate = Decimal(annual_rate)  # 年化利率
        self.term_rate =  self.annual_rate / Decimal('12') # 月利率
        self.day_rate = self.annual_rate / Decimal('12') / Decimal('30')  # 日利率
        self.line = PrettyTable(["期数", "还款本息", "当期本金", "当期利息", "剩余本金", "还款方式"])

    repayPattern = {
        "MCAT": "随借随还,按日计息",
        "BFTO": "利随本清,按日计息",
        "MIRD": "按月付息到期还本",
        "EPEI": "等本等息,按月付息",  # 对借款人最不利
        "MCEP": "等额本金,按月付息",  # 借款总利息最低
        "MCEI": "等额等息,按月付息"
    }


    # line.align["期数"] = "1"  # 以期数字段左对齐
    # line.padding_width = 2    # 填充宽度(字段间隔)


    # "EPEI": "等本等息,按月付息"               每期利息和本金一样,最后一期本金为上一期的剩余本金，最后一期利息为总利息-已还利息
    # def get_EPEI(num):
    #     show = copy.deepcopy(line)
    #     term_int = float_deal(principal * term_rate)  # 每期还利息（2位小数）
    #     total_int = float_deal(principal * term_rate * num)  # 总利息（2位小数）
    #     term_prin = float_deal(principal / num)  # 每期还本金（2位小数）
    #     prin = float_deal(principal)  # 初始化剩余本金为借款本金
    #     for i in range(1, num + 1):
    #         # 如果是最后一期，还款本金为上一期的剩余本金; 利息为总利息-已还利息
    #         if i == num:
    #             term_prin = prin
    #             term_int = total_int - (term_int * (num - 1))
    #         term_amt = term_prin + term_int
    #         prin = prin - term_prin  # 剩余本金=上期剩余本金-当期还本金
    #         show.add_row([i, term_amt, term_prin, term_int, prin, 'EPEI'])
    #     print('等本等息总利息为：', total_int)
    #     print(show)


    # "MIRD": "按月付息到期还本"      最后一期还本金，每期利息固定
    # def get_MIRD(num):
    #     show = copy.deepcopy(line)
    #     term_int = float_deal(principal * term_rate)
    #     term_prin = float_deal(0.0)
    #     total_int = float_deal(principal * term_rate * num)  # 总利息（2位小数）
    #     prin = float_deal(principal)
    #     for i in range(1, num + 1):
    #         # 如果是最后一期，还款本金为上一期的剩余本金; 利息为总利息-已还利息
    #         if i == num:
    #             term_prin = prin
    #             term_int = total_int - (term_int * (num - 1))
    #         term_amt = term_prin + term_int
    #         prin = prin - term_prin  # 剩余本金=上期剩余本金-当期还本金
    #         show.add_row([i, term_amt, term_prin, term_int, prin, 'MIRD'])
    #     print('按月付息到期还本总利息为：', total_int)
    #     print(show)


    # "等额本金,按月付息"
    # def get_MCEP(num):
    #     ## 每月本金相同，利息递减，相当于剩余本金的利息,每期利息固定：上一期本金*利率
    #     show = copy.deepcopy(line)
    #     term_prin = float_deal(principal / num)  # 每期还本金（2位小数）
    #     prin = float_deal(principal)
    #     total_int = float_deal(0.0)
    #     for i in range(1, num + 1):
    #         term_int = float_deal(prin * float_deal(term_rate))  # 每期利息固定：上一期本金*利率
    #         # 如果是最后一期，还款本金为上一期的剩余本金;
    #         if i == num:
    #             term_prin = prin
    #         term_amt = term_prin + term_int
    #         prin = prin - term_prin  # 剩余本金=上期剩余本金-当期还本金
    #         show.add_row([i, term_amt, term_prin, term_int, prin, 'MCEP'])
    #         total_int = float_deal(total_int + term_int)
    #     print('等额本金总利息为：', total_int)
    #     print(show)

    # "MCEI": "等额本息,按月付息"
    def get_MCEI(self,num):
        # 本金+利息保持相同，本金逐月递增，利息逐月递减，月还款数不变。
        plan_list = []
        show = copy.deepcopy(self.line)
        term_amt = float_deal((self.principal*self.term_rate*(1+self.term_rate)**num)/((1+self.term_rate)**num-1))      # 每期还款总额       **是幂运算
        prin = float_deal(self.principal)
        total_int = float_deal(0.0)
        for i in range(1, num + 1):
            plan_by_list = {}
            term_int = float_deal(prin * float_deal(self.term_rate))        # 每期利息计算固定：上一期本金*利率
            term_prin = (term_amt - term_int)   # 如果是最后一期，还款本金为上一期的剩余本金;
            if i == num:
                term_prin = prin
            term_amt = term_prin + term_int
            prin = float_deal(prin - term_prin)      # 剩余本金=上期剩余本金-当期还本金
            show.add_row([i, term_amt, term_prin, term_int,prin,'MCEI'])
            plan_by_list[i] = term_amt*100, term_prin*100, term_int*100
            plan_list.append(plan_by_list)
            total_int = total_int +  term_int
        # print('等额本息总利息为：', total_int)
        print(show)
        print(plan_list)
        print(plan_list[1][2][2])
        return plan_list


    # # "MCAT": "随借随还,按日计息"
    # def get_MCAT(num, pay):
    #     show = copy.deepcopy(line)
    #     day_int = float_deal(pay * day_rate * num)
    #     repay_amt = day_int + pay
    #     re_prin = principal - pay
    #     if pay > principal:
    #         print("还款金额:", pay, "不能大于本金:", principal)
    #     else:
    #         show.add_row([1, repay_amt, pay, day_int, re_prin, 'MCAT'])
    #         print('随借随还总利息为：', day_int)
    #         print(show)
    #
    #
    # # "BFTO": "利随本清,按日计息"
    # def get_BFTO(num):
    #     show = copy.deepcopy(line)
    #     day_int = float_deal(principal * day_rate * num)
    #     repay_amt = day_int + principal
    #     show.add_row([1, repay_amt, principal, day_int, 0.0, 'BFTO'])
    #     print('利随本清总利息为：', day_int)
    #     print(show)



if __name__ == '__main__':
    # get_EPEI(3)  # 等本等息,按月付息
    # get_MIRD(3)  # 到期还本,按月付息
    # get_MCEP(3)  # 等额本金,按月付息
    StagePlanUtils('1000','0.16').get_MCEI(6)  # 等额本息,按月付息
    # get_MCAT(720, 195)  # 随借随还,按日计息
