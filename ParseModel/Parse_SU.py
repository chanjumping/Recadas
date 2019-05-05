#!/usr/bin/env python
# -*- coding: utf-8 -*

from ParseModel.ParseUpgrade import *
import time
from Util.GlobalVar import *
from Util.Log import logger
from ParseModel.ParseUpgrade import upgrade_su


# 解析工作状态上报
def parse_state_report(data):
    peripheral = data[6:7]
    function_no = data[7:8]
    serial_num = data[2:4]
    state_return_body = '%s%s%s' % (COMPANY_NO, byte2str(peripheral), byte2str(function_no))
    state_return = '%s%s%s%s%s' % (SU_FLAG, calc_check_code(state_return_body), byte2str(serial_num),
                                   state_return_body, SU_FLAG)
    send_queue.put(state_return)
    work_state = data[8:9]
    logger.debug('—————— 当前的工作状态是 {} ——————'.format(work_state_dict.get(big2num(byte2str(work_state)))))

    # if data[8:9] == b'\x04':
    #     start_test_thread = threading.Thread(target=start_test_su)
    #     start_test_thread.setDaemon(True)
    #     start_test_thread.start()


# 解析工作状态上报
def parse_query_state_report(data):
    work_state = data[8:9]
    logger.debug('—————— 当前的工作状态是 {} ——————'.format(work_state_dict.get(big2num(byte2str(work_state)))))


# 解析恢复默认参数应答
def parse_reset(data):
    logger.debug('—————— 恢复默认参数应答 ——————')


# 解析查询外设应答
def parse_query_peripheral(data):
    logger.debug('—————— 查询外设指令应答 ——————')


# 解析设置参数应答
def parse_set_para_reply(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '成功'
    elif state == b'\x01':
        txt = '失败'
    else:
        txt = '状态出错'
    logger.debug('—————— 查询外设指令应答结果 {} ——————'.format(txt))


# 解析读写ID应答
def parse_set_device_id(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '成功'
    elif state == b'\x01':
        txt = '失败'
    else:
        txt = '状态出错'
    logger.debug('—————— 写设备ID结果 {} ——————'.format(txt))


# 解析读写ID应答
def parse_tf_status(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '读写正常'
    elif state == b'\x01':
        txt = '读写异常'
    else:
        txt = '状态出错'
    logger.debug('—————— TF卡读写状态 {} ——————'.format(txt))


# 解析ADAS授权状态应答
def parse_adas_status(data):
    state = data[8:12]
    device_id_len = big2num(byte2str(data[12:13]))
    device_id = data[13:13 + device_id_len].decode('utf-8')
    if state == b'\x00\x00\x00\x01':
        txt = '授权成功'
    else:
        txt = '授权失败 返回码 {}'.format(byte2str(state))
    logger.debug('—————— ADAS授权状态 {} ——————'.format(txt))
    logger.debug('—————— 设备ID {} ——————'.format(device_id))


# 解析读取烟感状态应答
def parse_smoke_sensor_status(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '初始化正常'
    elif state == b'\x01':
        txt = '初始化失败'
    else:
        txt = '状态出错'
    logger.debug('—————— 烟感状态 {} ——————'.format(txt))


# 解析转向灯状态
def parse_turn_signal_status(data):
    status = data[8:9]
    if status == b'\x00':
        txt = '未打转向灯'
    elif status == b'\x01':
        txt = '左转向'
    elif status == b'\x10':
        txt = '右转向'
    logger.debug('—————— 转向灯状态 {} ——————'.format(txt))


# 苏标获取日志功能
def get_log_su(start_date, end_date):
    logger.debug('—————— 获取 {} 到 {} 的日志 ——————'.format(start_date, end_date))
    start_date = num2big(int(start_date), 4)
    end_date = num2big(int(end_date), 4)

    body = '%s%s%s%s%s' % (COMPANY_NO, PERIPHERAL, 'FA', start_date, end_date)
    data = '%s%s%s%s%s' % ('7E', calc_check_code(body), num2big(get_serial_no()), body, '7E')
    send_queue.put(data)


# test_rec_failed = True
# 解析苏标日志传送分片
def parse_get_log_su(data):
    serial_num = data[2:4]
    peripheral = data[6:7]
    pkg_total = data[8:10]
    pkg_num = data[10:12]
    return_state = '00'
    # global test_rec_failed
    # if big2num(byte2str(pkg_num)) == 5 and test_rec_failed is True:
    #     pass
    # else:
    #     log_queue.put(data)
    # if big2num(byte2str(pkg_num)) == 5:
    #     if test_rec_failed:
    #         return_state = '01'
    #         test_rec_failed = False
    #         logger.debug('测试返回状态为1时，终端的返回情况。')
    #         log_event.debug('测试返回状态为1时，终端的返回情况。')
    log_queue.put(data)
    log_return_body = '%s%s%s%s%s%s' % (COMPANY_NO, byte2str(peripheral), 'F9', byte2str(pkg_total),
                                        byte2str(pkg_num), return_state)
    log_return = '%s%s%s%s%s' % ('7E', calc_check_code(log_return_body), byte2str(serial_num),
                                 log_return_body, '7E')
    send_queue.put(log_return)


# 解析获取日志状态
def parse_get_log_result_su(data):
    result = data[8:9]
    if result == b'\x00':
        txt = '成功'
    elif result == b'\x01':
        txt = '未找到文件'
    elif result == b'\x02':
        txt = '超时'
    elif result == b'\x03':
        txt = '失败'
    else:
        txt = '返回状态错误'
    logger.debug('—————— 获取日志状态 {} ——————'.format(txt))


# 存储日志
def save_log_su():
    logger.debug(threading.current_thread().getName())
    t = time.strftime(r'%Y%m%d%H%M%S', time.localtime())
    log_name = 'log_{}.zip'.format(t)
    while True:
        while not log_queue.empty():
            data = log_queue.get(block=False)
            if conf.get_procotol_type_flag() == 1:
                log_data = data[12:-1]
                with open(log_name, 'ab') as f:
                    f.write(log_data)
            time.sleep(0.1)
        time.sleep(0.1)


# 解析苏标外设信息
def parse_get_info(data):
    firm = data[9:41].decode('utf-8')
    product_no = data[42:74].decode('utf-8')
    hardware = data[75:107].decode('utf-8')
    software = data[108:140].decode('utf-8')
    deviceid = data[141:173].decode('utf-8')
    client_code = data[174:206].decode('utf-8')
    logger.debug('———————————————— 读取外设信息响应 ————————————————')
    logger.debug('公司:{}'.format(firm))
    logger.debug('产品编号:{}'.format(product_no))
    logger.debug('硬件版本:{}'.format(hardware))
    logger.debug('软件版本:{}'.format(software))
    logger.debug('设备ID:{}'.format(deviceid))
    logger.debug('客户编码:{}'.format(client_code))
    logger.debug('———————————————— END ————————————————')


# 解析苏标查询疲劳参数情况
def parse_query_dsm_para(data):
    activated_speed = big2num(byte2str(data[8:9]))
    vol = big2num(byte2str(data[9:10]))
    active_photo = big2num(byte2str(data[10:11]))
    active_photo_duration = big2num(byte2str(data[11:13]))
    active_photo_distance = big2num(byte2str(data[13:15]))
    active_photo_count = big2num(byte2str(data[15:16]))
    active_photo_time = big2num(byte2str(data[16:17]))
    photo_resolution = big2num(byte2str(data[17:18]))
    video_resolution = big2num(byte2str(data[18:19]))
    retain1 = byte2str(data[19:29])
    smoke_duration = big2num(byte2str(data[29:31]))
    phone_duration = big2num(byte2str(data[31:33]))
    fatigue_video_duration = big2num(byte2str(data[33:34]))
    fatigue_photo_count = big2num(byte2str(data[34:35]))
    fatigue_photo_time = big2num(byte2str(data[35:36]))
    retain2 = byte2str(data[36:37])
    phone_video_duration = big2num(byte2str(data[37:38]))
    phone_photo_count = big2num(byte2str(data[38:39]))
    phone_photo_time = big2num(byte2str(data[39:40]))
    smoke_video_duration = big2num(byte2str(data[40:41]))
    smoke_photo_count = big2num(byte2str(data[41:42]))
    smoke_photo_time = big2num(byte2str(data[42:43]))
    careful_video_duration = big2num(byte2str(data[43:44]))
    careful_photo_count = big2num(byte2str(data[44:45]))
    careful_photo_time = big2num(byte2str(data[45:46]))
    forward_video_duration = big2num(byte2str(data[46:47]))
    forward_photo_count = big2num(byte2str(data[47:48]))
    forward_photo_time = big2num(byte2str(data[48:49]))
    retain3 = byte2str(data[49:51])
    logger.debug('———————————————— 查询DSM参数应答 ————————————————')
    logger.debug('报警使能速度阈值:{}'.format(activated_speed))
    logger.debug('报警提示音量:{}'.format(vol))
    logger.debug('主动拍照策略:{}'.format(active_photo))
    logger.debug('主动拍照间隔时间:{}'.format(active_photo_duration))
    logger.debug('主动拍照间隔距离:{}'.format(active_photo_distance))
    logger.debug('每次主动拍照张数:{}'.format(active_photo_count))
    logger.debug('每次主动拍照间隔时间:{}'.format(active_photo_time))
    logger.debug('拍照分辨率:{}'.format(photo_resolution))
    logger.debug('视频录制分辨率:{}'.format(video_resolution))
    logger.debug('保留字段1:{}'.format(retain1))
    logger.debug('吸烟报警判断时间间隔:{}'.format(smoke_duration))
    logger.debug('接打电话报警判断时间间隔:{}'.format(phone_duration))
    logger.debug('疲劳驾驶报警前后录制时长:{}'.format(fatigue_video_duration))
    logger.debug('疲劳驾驶报警拍照张数:{}'.format(fatigue_photo_count))
    logger.debug('疲劳驾驶报警拍照间隔时间:{}'.format(fatigue_photo_time))
    logger.debug('保留字段2:{}'.format(retain2))
    logger.debug('打电话报警前后录制时间:{}'.format(phone_video_duration))
    logger.debug('打电话报警拍照张数:{}'.format(phone_photo_count))
    logger.debug('打电话报警时间间隔:{}'.format(phone_photo_time))
    logger.debug('吸烟报警前后录制时间:{}'.format(smoke_video_duration))
    logger.debug('吸烟报警拍照张数:{}'.format(smoke_photo_count))
    logger.debug('吸烟报警时间间隔:{}'.format(smoke_photo_time))
    logger.debug('分神报警前后录制时间:{}'.format(careful_video_duration))
    logger.debug('分神报警拍照张数:{}'.format(careful_photo_count))
    logger.debug('分神报警时间间隔:{}'.format(careful_photo_time))
    logger.debug('驾驶异常报警前后录制时间:{}'.format(forward_video_duration))
    logger.debug('驾驶异常报警拍照张数:{}'.format(forward_photo_count))
    logger.debug('驾驶异常报警时间间隔:{}'.format(forward_photo_time))
    logger.debug('保留字段3:{}'.format(retain3))
    logger.debug('———————————————— END ————————————————')


# 解析苏标查询ADAS参数情况
def parse_query_adas_para(data):
    activated_speed = big2num(byte2str(data[8:9]))
    activated_vol = big2num(byte2str(data[9:10]))
    active_photo_strategy = big2num(byte2str(data[10:11]))
    active_timed_photo_interval = big2num(byte2str(data[11:13]))
    active_fixed_distance_photo_interval = big2num(byte2str(data[13:15]))
    number_of_active_photos_per_time = big2num(byte2str(data[15:16]))
    time_interval_each_photo = big2num(byte2str(data[16:17]))
    photo_resolution = big2num(byte2str(data[17:18]))
    video_recording_resolution = big2num(byte2str(data[18:19]))
    obstacle_alarm_distance_threshold = big2num(byte2str(data[28:29]))
    obstacle_alarm_video_recording_time = big2num(byte2str(data[29:30]))
    number__photos__obstacle_alarm = big2num(byte2str(data[30:31]))
    obstacle_alarm_photo_interval = big2num(byte2str(data[31:32]))
    frequent_lane_change_alarm_timing = big2num(byte2str(data[32:33]))
    frequent_lane_change_alarm_times = big2num(byte2str(data[33:34]))
    frequent_lane_change_video_recordingtime = big2num(byte2str(data[34:35]))
    frequent_lane_change_alarm_photonumber = big2num(byte2str(data[35:36]))
    frequent_lane_change_alarm_photointerval = big2num(byte2str(data[36:37]))
    lane_departure_alarm_video_recordingtime = big2num(byte2str(data[37:38]))
    number_deviation_alarm = big2num(byte2str(data[38:39]))
    lane_alarm_photo_interval = big2num(byte2str(data[39:40]))
    forward_collision_alarm_time_threshold = big2num(byte2str(data[40:41]))
    forward_collision_alarm_video_recordingtime = big2num(byte2str(data[41:42]))
    forward_collision_alarm_photonumber = big2num(byte2str(data[42:43]))
    forward_collision_alarm_photointerval= big2num(byte2str(data[43:44]))
    pedestrian_collision_alarmtime_threshold = big2num(byte2str(data[44:45]))
    pedestrian_collision_alarmvideo_recordingtime = big2num(byte2str(data[45:46]))
    number_photos_pedestrian_collisionalarm = big2num(byte2str(data[46:47]))
    pedestrian_collision_alarm_photointerval = big2num(byte2str(data[47:48]))
    range_distance_monitoring = big2num(byte2str(data[48:49]))
    video_recording_proximity_alarm = big2num(byte2str(data[49:50]))
    number_photos_closealarm = big2num(byte2str(data[50:51]))
    car_interval = big2num(byte2str(data[51:52]))
    number_photos_road_identification = big2num(byte2str(data[52:53]))
    road_photo_intervals = big2num(byte2str(data[53:54]))

    logger.debug('———————————————— 查询ADAS应答 ————————————————')
    logger.debug('报警使能速度阈值：{}'.format(activated_speed))
    logger.debug('报警提示音量：{}'.format(activated_vol))
    logger.debug('主动拍照策略:{}'.format(active_photo_strategy))
    logger.debug('主动定时拍照时间间隔:{}'.format(active_timed_photo_interval))
    logger.debug('主动定距拍照距离间隔:{}'.format(active_fixed_distance_photo_interval))
    logger.debug('每次主动拍照张数:{}'.format(number_of_active_photos_per_time))
    logger.debug('每次主动拍照时间间隔:{}'.format(time_interval_each_photo))
    logger.debug('拍照分辨率:{}'.format(photo_resolution))
    logger.debug('视频录制分辨率:{}'.format(video_recording_resolution))
    logger.debug('障碍物报警距离阈值:{}'.format(obstacle_alarm_distance_threshold))
    logger.debug('障碍物报警前后视频录制时间:{}'.format(obstacle_alarm_video_recording_time))
    logger.debug('障碍物报警拍照张数:{}'.format(number__photos__obstacle_alarm))
    logger.debug('障碍物报警拍照间隔:{}'.format(obstacle_alarm_photo_interval))
    logger.debug('频繁变道报警判断时间段:{}'.format(frequent_lane_change_alarm_timing))
    logger.debug('频繁变道报警判断次数:{}'.format(frequent_lane_change_alarm_times))
    logger.debug('频繁变道报警前后视频录制时间:{}'.format(frequent_lane_change_video_recordingtime))
    logger.debug('频繁变道报警拍照张数:{}'.format(frequent_lane_change_alarm_photonumber))
    logger.debug('频繁变道报警拍照间隔:{}'.format(frequent_lane_change_alarm_photointerval))
    logger.debug('车道偏离报警前后视频录制时间:{}'.format(lane_departure_alarm_video_recordingtime))
    logger.debug('车道偏离报警拍照张数:{}'.format(number_deviation_alarm))
    logger.debug('车道偏离报警拍照间隔:{}'.format(lane_alarm_photo_interval))
    logger.debug('前向碰撞报警时间阈值:{}'.format(forward_collision_alarm_time_threshold))
    logger.debug('前向碰撞报警前后视频录制时间:{}'.format(forward_collision_alarm_video_recordingtime))
    logger.debug('前向碰撞报警拍照张数:{}'.format(forward_collision_alarm_photonumber))
    logger.debug('前向碰撞报警拍照间隔:{}'.format(forward_collision_alarm_photointerval))
    logger.debug('行人碰撞报警时间阈值:{}'.format(pedestrian_collision_alarmtime_threshold))
    logger.debug('行人碰撞报警前后视频录制时间:{}'.format(pedestrian_collision_alarmvideo_recordingtime))
    logger.debug('行人碰撞报警拍照张数:{}'.format(number_photos_pedestrian_collisionalarm))
    logger.debug('行人碰撞报警拍照间隔:{}'.format(pedestrian_collision_alarm_photointerval))
    logger.debug('车距监控报警距离阈值:{}'.format(range_distance_monitoring))
    logger.debug('车距过近报警前后视频录制时间:{}'.format(video_recording_proximity_alarm))
    logger.debug('车距过近报警拍照张数:{}'.format(number_photos_closealarm))
    logger.debug('车距过近报警拍照间隔:{}'.format(car_interval))
    logger.debug('道路标识识别拍照张数:{}'.format(number_photos_road_identification))
    logger.debug('道路标识识别拍照间隔:{}'.format(road_photo_intervals))
    logger.debug('———————————————— END ————————————————')


# 不断进行升级
def start_test_su():
    time.sleep(10)
    upgrade_su('Package.zip', 5120)
