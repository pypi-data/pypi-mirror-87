#!usr/bin/env python
# encoding: utf-8
# @author: cherry
# @file:demo_01.py
# @time:2020/9/4 11:47 上午

from BasicLibrary.request_utils import *

# res = http_get(url='http://passplus.apps01.ali-bj-sit01.shuheo.net:80/passplus/signPass?pass=135790')
# print(res)


# res = http_get(url='http://directmarketing.apps01.ali-bj-sit01.shuheo.net/directmarketing/hbpay/searchLawToActuation/00b56361-9fcd-44b5-b904-fc2fe069356c')
# print(res)
# get_params_data = {
#     'grant_type':'client_credential',
#     'appid':'wx5189359b0e0ddd89',
#     'secret':'11d4de7719a2276becf27ab573263061'
# }
# res = http_get('https://api.weixin.qq.com/cgi-bin/token', params=get_params_data)
# print(res)

get_param_data = {'access_token':'37_-6YoyQNWu5ZVe2KMdYFKWVJUcW6pNxiF1TeUp4_jEhrU5ZV0h2bkxXfE_xvdzeuJU9qbzknDSAQVTKLH8Li-wfJHXm85I6AcnCF8_RKAal-67mSt_StYbYAA6FwfuQig37xKvGf_eyl0z2NKCVJaAFAQJX'}
access_token='37_-6YoyQNWu5ZVe2KMdYFKWVJUcW6pNxiF1TeUp4_jEhrU5ZV0h2bkxXfE_xvdzeuJU9qbzknDSAQVTKLH8Li-wfJHXm85I6AcnCF8_RKAal-67mSt_StYbYAA6FwfuQig37xKvGf_eyl0z2NKCVJaAFAQJX'
print(type(access_token))
post_param_data = {   "tag" : {     "id" : 100,     "name" : "广东4cherry"   } }
headinfos = {'Content-Type':'application/json'}
res = http_post(url='https://api.weixin.qq.com/cgi-bin/tags/update',
                         params=get_param_data,
                         # data=json.dumps(post_param_data),
                         json=post_param_data,
                         headers=headinfos)
print(res.content.decode('utf-8'))

# save_base_info_header={
#     'content-type':'application/json; charset=utf-8',
#     'x-token':'2gWfGk2cvwqH7OCmOW1P449MCRW4ubxaytP7'}
#
# save_base_info_body = {
#         "lawId": "ZXNB19252012030006",
#         "location": {
#             "latitude": 31.19878,
#             "longitude": 121.603668,
#             "province": "上海市",
#             "city": "上海市",
#             "district": "浦东新区",
#             "address": "上海市浦东新区湖秀路112号靠近上海浦东软件园Y2座"
#         },
#         "cusCar": 0,
#         "cusOnlineLenderFirstlevel": 0,
#         "finished": 'false',
#         "cusMonthlyIncome": "UNWARE",
#         "cusHousingSituation": "PURCHASE",
#         "cusProfessionFirstlevel": "OTHER",
#         "cusProfessionTwolevel": "ZHUANGXIUSHEJI",
#         "registeredShop": 'false',
#         "companyHeader": "jokes",
#         "cusRemark": "n",
#         "cusLawInAddress": {
#             "province": "上海市",
#             "city": "上海市",
#             "address": "浦东新区蔡伦路华陀路Bbox"
#         },
#         "cusHouseAddress": {
#             "province": '',
#             "city": '',
#             "address": ''
#         }
#     }
#
# res = http_post(url='http://b.sit.lattebank.com/directmarketingmgr/directmarketing/hbpay/remark/savebaseinfo',
#                 headers=save_base_info_header,
#                 data=save_base_info_body)
# print(res)