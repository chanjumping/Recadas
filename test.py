# import pymongo
# #建立数据库连接，指定ip和端口号
# client = pymongo.MongoClient("47.112.133.250", 27017)
# #指定mydb数据库
# mydb = client.reconova_vehicle
# #指定mydb数据库里user集合
# collection = mydb.t_car_location
# #查询内容
# import re
# pattern = re.compile('2019-07-14')
# result = collection.find({
#     "facilityNo": "00219210070",
#     "createTime": pattern
# })
# for x in result:
#     # if x['isLocate']:
#         print(x)
#         # import time
#         # timeStamp = x['locationTime']/1000
#         # timeArray = time.localtime(timeStamp)
#         # otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
#         # print(x['createTime'], x['bdLatitude'], x['bdLongitude'], x['isLocate'], otherStyleTime, x['speed'])
#         # # with open("7.11.txt", 'a') as f:
#         # #     f.write("{},{}".format(x['bdLatitude'], x['bdLongitude']))
#         # #     f.write('\n')
