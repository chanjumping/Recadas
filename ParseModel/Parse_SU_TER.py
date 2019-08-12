#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.GlobalVar import *
from Util import GlobalVar
from Util.Log import log_event
from Util.CommonMethod import *

comm_type = {
    b'\x81\x03': '设置终端参数',
    b'\x81\x00': '下发TTS语音',
    b'\x92\x08': '下发服务器地址',
    b'\x92\x11': '新增0x9211',
    b'\x81\x06': '查询参数',
    b'\x8F\x01': '重启设备',
    b'\x8F\xA0': '平台主动升级'
}


# 通用应答
def comm_reply_su_ter(data, reply_result):
    msg_id = data[1:3]
    serial_num = data[11:13]
    result = reply_result
    body = '8001' + '0005' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + byte2str(serial_num) + byte2str(msg_id) + result
    data = '7E' + body + calc_check_code(body) + '7E'
    return data


# 解析苏标终端通用应答
def parse_device_comm_reply_su_ter(data):
    comm = data[15:17]
    serial_no = byte2str(data[13:15])
    result = byte2str(data[17:18])
    type_name = comm_type.get(comm)
    logger.debug('—————— 收到 {} 的通用应答 流水号 {} 应答结果 {} ——————'.format(type_name, serial_no, result))
    if comm == b'\x92\x08':
        if GlobalVar.send_address_dict.get(serial_no):
            GlobalVar.send_address_dict.pop(serial_no)


# 解析位置上报
def parse_location_upload_su_ter(data):
    state = byte2str(data[17:21])
    if 0x00000002 & big2num(state) == 0:
        gps_state = '定位失败'
    else:
        gps_state = '定位成功'
    latitude = big2num(byte2str(data[21:25]))
    longitude = big2num(byte2str(data[25:29]))
    speed = big2num(byte2str(data[31:33]))
    alarm_time = byte2str(data[35:41])
    logger.debug('—————— 状态 {} 速度 {} km/h {} 纬度 {} 经度 {} 时间 {} ——————'.format(state, speed/10, gps_state, latitude, longitude, alarm_time))
    if len(data) > 53:
        peripheral = data[41:42]
        logger.debug('')
        if peripheral == b'\x64':
            logger.debug('========== 收到ADAS告警信息 ==========')
        elif peripheral == b'\x65':
            logger.debug('========== 收到DSM告警信息 ==========')
        elif peripheral == b'\x67':
            logger.debug('========== 收到BSD告警信息 ==========')
        length = data[42:43]
        if not big2num(byte2str(length)) == len(data[43:-2]):
            logger.debug('告警事件中附加项长度与实际长度不一致 {}'.format(byte2str(data)))
        else:
            alarm_id = big2num(byte2str(data[43:47]))
            state_flag = byte2str(data[47:48])
            event_type = data[48:49]
            if peripheral == b'\x64':
                alarm_type = alarm_type_code_su_ter_adas.get(event_type)
                alarm_level = byte2str(data[49:50])
                front_car_speed = byte2str(data[50:51])
                front_distance = byte2str(data[51:52])
                departure_type = byte2str(data[52:53])
                road_identify_type = byte2str(data[53:54])
                road_identify_data = byte2str(data[54:55])
                speed = big2num(byte2str(data[55:56]))
                height = byte2str(data[55:59])
                latitude = big2num(byte2str(data[59:63]))
                longitude = big2num(byte2str(data[63:67]))
                alarm_time = byte2str(data[66:72])
                car_state = byte2str(data[72:74])
                alarm_flag = byte2str(data[74:90])
                logger.debug('告警ID {} 标识状态 {} 报警级别 {} 前车速度 {} 前车/行人距离 {} 偏离类型 {} 道路识别类型 {} 道路识别数据 {} '
                                '告警类型 - - - - - - - - - - - - - - - - - - - - - - - - 【 {} 】'.format(alarm_id, state_flag, alarm_level,
                                front_car_speed, front_distance, departure_type, road_identify_type, road_identify_data, alarm_type))

                logger.debug('车速 {} 高程 {} 纬度 {} 经度 {} 日期 {} 车辆状态 {} 报警标识号 {}'.format(speed, height, latitude, longitude,
                                                                                     alarm_time, car_state, alarm_flag))
            elif peripheral == b'\x65':
                alarm_type = alarm_type_code_su_ter_dsm.get(event_type)
                alarm_level = byte2str(data[49:50])
                fatigue_level = byte2str(data[50:51])
                retain = byte2str(data[51:55])
                speed = big2num(byte2str(data[55:56]))
                height = byte2str(data[56:58])
                latitude = big2num(byte2str(data[58:62]))
                longitude = big2num(byte2str(data[62:66]))
                alarm_time = byte2str(data[66:72])
                car_state = byte2str(data[72:74])
                alarm_flag = byte2str(data[74:90])
                logger.debug('告警ID {} 标识状态 {} 报警级别 {} 疲劳级别 {} 预留 {} 告警类型 - - - - - - - - - - - - - - - - - - - - '
                                '【 {} 】'.format(alarm_id, state_flag, alarm_level, fatigue_level, retain, alarm_type))

                logger.debug('车速 {} 高程 {} 纬度 {} 经度 {} 日期 {} 车辆状态 {} 报警标识号 {}'.format(speed, height, latitude, longitude,
                                                                                     alarm_time, car_state, alarm_flag))

            elif peripheral == b'\x67':
                alarm_type = alarm_type_code_su_ter_bsd.get(event_type)
                speed = big2num(byte2str(data[49:50]))
                height = byte2str(data[50:52])
                latitude = big2num(byte2str(data[52:56]))
                longitude = big2num(byte2str(data[56:60]))
                alarm_time = byte2str(data[60:66])
                car_state = byte2str(data[66:70])
                alarm_flag = byte2str(data[70:86])
                logger.debug('告警ID {} 标识状态 {} 告警类型 - - - - - - - - - - - - - - - - - - - - 【 {} 】'.
                                format(alarm_id, state_flag, alarm_type))
                logger.debug('车速 {} 高程 {} 纬度 {} 经度 {} 日期 {} 车辆状态 {} 报警标识号 {}'.
                                format(speed, height, latitude, longitude, alarm_time, car_state, alarm_flag))

            logger.debug('')
            send_server_command_su_ter(alarm_flag)

    reply_data = comm_reply_su_ter(data, '00')
    send_queue.put(reply_data)


# 解析心跳
def parse_heart_su_ter(data):
    logger.debug('—————— Heart Beat ——————')
    data = comm_reply_su_ter(data, '00')
    send_queue.put(data)


# 鉴权
def parse_authentication_su_ter(data):
    authentication_code = data[13:-2]
    logger.debug('—————— 收到鉴权请求 ——————')
    logger.debug('鉴权码 {}'.format(authentication_code.decode('utf-8')))
    reply_data = comm_reply_su_ter(data, '00')
    send_queue.put(reply_data)


# 注册
def parse_register_su_ter(data):
    logger.debug('—————— 收到注册请求 ——————')
    serial_num = data[11:13]
    state = '00'
    auth_code = 'test'
    msg_body = '%s%s%s' % (byte2str(serial_num), state, str2hex(auth_code, 4))
    # msg_body = '%s%s' % (byte2str(serial_num), state)
    body = '%s%s%s%s%s' % ('8100', num2big(int(len(msg_body) / 2)), GlobalVar.DEVICEID, num2big(
        GlobalVar.get_serial_no()), msg_body)
    data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
    send_queue.put(data)


# 苏标终端下发服务器命令
def send_server_command_su_ter(alarm_flag):
    logger.debug('—————— 下发服务器地址 ——————')
    server = conf.get_file_address()
    port = conf.get_file_port()
    control = '00'
    if control == 'AA':
        upload = '05'
    else:
        upload = '00'
    alarm_num = str(int(time.time()*1000000))
    logger.debug('下发报警编号为 {}'.format(alarm_num*2))
    msg_body = num2big(len(server), 1) + str2hex(server, len(server)).upper() + num2big(port, 2) + '0000' + alarm_flag + \
               str2hex(alarm_num, 16)*2 + control + upload + '00' * 14
    serial_num = num2big(GlobalVar.get_serial_no())
    body = '%s%s%s%s%s' % ('9208', num2big(int(len(msg_body) / 2)), GlobalVar.DEVICEID, serial_num, msg_body)
    data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
    GlobalVar.send_address_dict[serial_num] = data
    send_queue.put(data)
    GlobalVar.send_address_time_out = 10


# 苏标终端告警附件信息
def parse_alarm_attachment_msg_su_ter(data, rec_obj):
    terminal_id = byte2str(data[13:20])
    alarm_flag = byte2str(data[20:36])
    alarm_num = byte2str(data[36:68])
    msg_type = byte2str(data[68:69])
    attachment_num = big2num(byte2str(data[69:70]))
    log_event.debug('{} —————— 报警附件信息 ——————'.format(rec_obj.client_address))
    log_event.debug('{} 终端ID {}'.format(rec_obj.client_address, terminal_id))
    log_event.debug('{} 报警标识号 {}'.format(rec_obj.client_address, alarm_flag))
    log_event.debug('{} 报警编号 {}'.format(rec_obj.client_address, alarm_num))
    log_event.debug('{} 信息类型 {}'.format(rec_obj.client_address, msg_type))
    log_event.debug('{} 附件数量 {}'.format(rec_obj.client_address, attachment_num))
    attachment_data = data[70:-2]
    while len(attachment_data):
        name_len = big2num(byte2str(attachment_data[0:1]))
        log_event.debug('{} 文件名称长度 {}'.format(rec_obj.client_address, name_len))
        name = attachment_data[1:1+name_len].decode('utf-8')
        log_event.debug('{} 文件名称 {}'.format(rec_obj.client_address, name))
        file_size = big2num(byte2str(attachment_data[1+name_len:1+name_len+4]))
        log_event.debug('{} 文件大小 {}'.format(rec_obj.client_address, file_size))
        attachment_data = attachment_data[1+name_len+4:]

    log_event.debug('{} —————— END ——————'.format(rec_obj.client_address))
    reply_data = comm_reply_su_ter(data, '00')
    return reply_data


# 苏标终端文件信息上传
def parse_media_msg_upload_su_ter(data, rec_obj):
    name_len = data[13:14]
    media_name = data[14:14 + big2num(byte2str(name_len))].split(b'\x00')[0].decode('utf-8')
    media_type = byte2str(data[-7:-6])
    media_size = big2num(byte2str(data[-6:-2]))
    name_size[media_name] = media_size
    quotient = media_size//65536
    name_offset_data[media_name] = dict(zip([x * 65536 for x in range(quotient + 1)], [None] * quotient))
    log_event.debug('{} —————— 文件信息上传 ——————'.format(rec_obj.client_address))
    log_event.debug('{} 文件名 {}'.format(rec_obj.client_address, media_name))
    log_event.debug('{} 文件类型 {}'.format(rec_obj.client_address, media_type))
    log_event.debug('{} 文件大小 {}'.format(rec_obj.client_address, media_size))
    log_event.debug('{} —————— END ——————'.format(rec_obj.client_address))

    reply_data = comm_reply_su_ter(data, '00')
    return reply_data


# 苏标终端告警上传结束标识
def parse_media_upload_finish_su_ter(data, rec_obj):
    loss_pkg_list = []
    name_len = data[13:14]
    media_name = data[14:14 + big2num(byte2str(name_len))].split(b'\x00')[0].decode('utf-8')
    media_type = byte2str(data[-7:-6])
    media_size = big2num(byte2str(data[-6:-2]))
    quotient = media_size//65536
    remainder = media_size % 65536
    log_event.debug('{} —————— 告警结束 ——————'.format(rec_obj.client_address))
    log_event.debug('{} 文件名 {}'.format(rec_obj.client_address, media_name))
    log_event.debug('{} 文件类型 {} '.format(rec_obj.client_address, media_type))
    log_event.debug('{} 文件大小 {}'.format(rec_obj.client_address, media_size))
    log_event.debug('{} —————— END ——————'.format(rec_obj.client_address))

    filename_length = data[13:14]
    file_name = data[14:14 + big2num(byte2str(filename_length))]
    file_type = data[-7:-6]
    offset_data = name_offset_data.get(media_name)

    if offset_data:
        # if len(offset_data) > 1:
        #     offset_data[0] = None
        #     offset_data[65536] = None
        for x in offset_data.keys():
            if not offset_data.get(x):
                    loss_pkg_list.append(x)
        if not loss_pkg_list:
            msg_body = byte2str(filename_length) + byte2str(file_name) + byte2str(file_type) + '00' + '00'
            for x in sorted(offset_data.keys()):
                media_queue.put(offset_data.get(x))
            name_offset_data.pop(media_name)
        else:
            loss_pkg = ''
            loss_len = len(loss_pkg_list)
            log_event.info("{} {} 多媒体数据丢包，丢包偏移量为 {}".format(rec_obj.client_address, media_name, loss_pkg_list))
            if quotient in loss_pkg_list:
                loss_pkg_list.pop(quotient)
                for x in loss_pkg_list:
                    loss_pkg += num2big(x, 4) + num2big(65536, 4)
                loss_pkg += num2big(quotient, 4) + num2big(remainder, 4)
            else:
                for x in loss_pkg_list:
                    loss_pkg += num2big(x, 4) + num2big(65536, 4)
            msg_body = byte2str(filename_length) + byte2str(file_name) + byte2str(file_type) + '01' + num2big(loss_len, 1) + loss_pkg
    else:
        msg_body = byte2str(filename_length) + byte2str(file_name) + byte2str(file_type) + '00' + '00'
    body = '%s%s%s%s%s' % ('9212', num2big(int(len(msg_body) / 2)), GlobalVar.DEVICEID, num2big(
        GlobalVar.get_serial_no()), msg_body)
    data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
    return data


# 解析请求终端属性
def parse_query_pro_su_ter(data):
    terminal_type = byte2str(data[13:15])
    manufacture_id = byte2str(data[15:20])
    terminal_model = byte2str(data[20:40])
    terminal_id = byte2str(data[40:47])
    terminal_SIM = byte2str(data[47:57])
    hardware_len = big2num(byte2str(data[57:58]))
    hardware = data[58:58 + hardware_len].decode('utf-8')
    firmware_len = big2num(byte2str(data[58 + hardware_len:59 + hardware_len]))
    firmware = data[59 + hardware_len:59 + hardware_len + firmware_len].decode('utf-8')
    gnss_model = byte2str(data[59 + hardware_len + firmware_len:60 + hardware_len + firmware_len])
    communication_model = byte2str(data[60 + hardware_len + firmware_len:61 + hardware_len + firmware_len])
    # software_len = big2num(byte2str(data[61 + hardware_len + firmware_len:62 + hardware_len + firmware_len]))
    # software = data[62 + hardware_len + firmware_len:62 + hardware_len + firmware_len + software_len].decode('utf-8')
    logger.debug('———————————————— 查询终端属性应答 ————————————————')
    logger.debug('终端类型 {}'.format(terminal_type))
    logger.debug('制造商ID {}'.format(manufacture_id))
    logger.debug('终端型号 {}'.format(terminal_model))
    logger.debug('终端ID {}'.format(terminal_id))
    logger.debug('终端SIM卡 {}'.format(terminal_SIM))
    logger.debug('硬件版本 {}'.format(hardware))
    logger.debug('固件版本 {}'.format(firmware))
    # logger.debug('软件版本 {}'.format(software))
    logger.debug('GNSS模块属性 {}'.format(gnss_model))
    logger.debug('通信模块属性 {}'.format(communication_model))
    logger.debug('———————————————— END ————————————————')


# 苏标终端下发升级请求
def send_upgrade_command(filename, flag, upgrade_type, hw, fw, sw, url):
    with open(filename, 'rb') as f:
        package_len = len(f.read())
    msg_body = num2big(flag, 1) + num2big(upgrade_type, 1) + num2big(package_len, 4) + get_md5(filename) + \
               num2big(32, 1) + str2hex(hw, 32) + num2big(32, 1) + str2hex(fw, 32) + num2big(32, 1) + str2hex(sw, 32) \
               + num2big(len(url), 1) + str2hex(url, len(url))
    body = '8FA1' + num2big(int(len(msg_body)/2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
    data = '7E' + body + calc_check_code(body) + '7E'
    send_queue.put(data)


# 解析上传基本信息
def parse_upload_msg_su_ter(data):
    logger.debug('———————————————— START ————————————————')
    msg_type = data[13:14]
    if msg_type == b'\xf7':
        logger.debug('上传状态查询报文')
    elif msg_type == b'\xf8':
        logger.debug('上传信息查询报文')
    else:
        logger.debug('透传消息类型错误！！！')

    list_num = data[14:15]
    logger.debug('消息列表总数 {}'.format(big2num(byte2str(list_num))))

    peripheral = data[15:16]
    if peripheral == b'\x64':
        logger.debug('====== ADAS系统 ======')
    elif peripheral == b'\x65':
        logger.debug('====== DSM系统 ======')
    elif peripheral == b'\x67':
        logger.debug('====== BSD系统 ======')
    msg_len = big2num(byte2str(data[16:17]))
    logger.debug('消息长度 {}'.format(msg_len))
    if not msg_len == len(data[17:-2]):
        logger.error('实际长度为 {}，消息长度错误！！！'.format(len(data[17:-2])))
    if msg_type == b'\xf7':
        work_state = byte2str(data[17:18])
        logger.debug('工作状态 {}'.format(work_state))
        alarm_state = byte2str(data[18:22])
        logger.debug('报警状态 {}'.format(alarm_state))
        logger.debug('———————————————— END ————————————————')
    elif msg_type == b'\xf8':
        company_name_len = big2num(byte2str(data[17:18]))
        company_name = data[18:18 + company_name_len]
        logger.debug('公司名称 {}'.format(company_name.decode('utf-8')))
        product_len = big2num(byte2str(data[18 + company_name_len:19 + company_name_len]))
        product = data[19 + company_name_len: 19 + company_name_len + product_len]
        logger.debug('产品型号 {}'.format(product.decode('utf-8')))
        firmware_len = big2num(byte2str(data[19 + company_name_len + product_len:20 + company_name_len + product_len]))
        firmware = data[20 + company_name_len + product_len:20 + company_name_len + product_len + firmware_len]
        logger.debug('硬件版本 {}'.format(firmware.decode('utf-8')))
        software_len = big2num(byte2str(data[20 + company_name_len + product_len + firmware_len:21 + company_name_len + product_len + firmware_len]))
        software = data[21 + company_name_len + product_len + firmware_len:21 + company_name_len + product_len + firmware_len + software_len]
        logger.debug('软件版本 {}'.format(software.decode('utf-8')))
        device_id_len = big2num(byte2str(data[21 + company_name_len + product_len + firmware_len + software_len:22 + company_name_len + product_len + firmware_len + software_len]))
        device_id = data[22 + company_name_len + product_len + firmware_len + software_len:22 + company_name_len + product_len + firmware_len + software_len + device_id_len]
        logger.debug('设备ID {}'.format(device_id.decode('utf-8')))
        customer_code_len = big2num(byte2str(data[22 + company_name_len + product_len + firmware_len + software_len + device_id_len:23 + company_name_len + product_len + firmware_len + software_len + device_id_len]))
        customer_code = data[23 + company_name_len + product_len + firmware_len + software_len + device_id_len:23 + company_name_len + product_len + firmware_len + software_len + device_id_len+customer_code_len]
        logger.debug('客户代码 {}'.format(customer_code.decode('utf-8')))
        logger.debug('———————————————— END ————————————————')


# 解析查询参数指令
def parse_query_para_su_ter(data):
    logger.debug('———————————————— START ————————————————')
    reply_serial_no = byte2str(data[13:15])
    logger.debug('应答流水号 {}'.format(reply_serial_no))
    msg_num = byte2str(data[15:16])
    logger.debug('消息个数 {}'.format(msg_num))
    para_num = byte2str(data[16:17])
    logger.debug('参数个数 {}'.format(para_num))
    peripheral = data[17:21]
    if peripheral == b'\x00\x00\xF3\x64':
        logger.debug('====== 查询ADAS信息 ======')
        activated_speed = big2num(byte2str(data[22:23]))
        vol = big2num(byte2str(data[23:24]))
        active_photo = big2num(byte2str(data[24:25]))
        active_photo_duration = big2num(byte2str(data[25:27]))
        active_photo_distance = big2num(byte2str(data[27:29]))
        active_photo_count = big2num(byte2str(data[29:30]))
        active_photo_time = big2num(byte2str(data[30:31]))
        photo_resolution = big2num(byte2str(data[31:32]))
        video_resolution = big2num(byte2str(data[32:33]))
        alarm_enable = byte2str(data[33:37])
        event_enable = byte2str(data[37:41])
        logger.debug('报警使能速度阈值:{}'.format(activated_speed))
        logger.debug('报警提示音量:{}'.format(vol))
        logger.debug('主动拍照策略:{}'.format(active_photo))
        logger.debug('主动拍照间隔时间:{}'.format(active_photo_duration))
        logger.debug('主动拍照间隔距离:{}'.format(active_photo_distance))
        logger.debug('每次主动拍照张数:{}'.format(active_photo_count))
        logger.debug('每次主动拍照间隔时间:{}'.format(active_photo_time))
        logger.debug('拍照分辨率:{}'.format(photo_resolution))
        logger.debug('视频录制分辨率:{}'.format(video_resolution))
        logger.debug('报警使能:{}'.format(alarm_enable))
        logger.debug('事件使能:{}'.format(event_enable))
        retain1 = byte2str(data[41:42])
        obstacle_distance_threshold = big2num(byte2str(data[42:43]))
        obstacle_level_speed = big2num(byte2str(data[43:44]))
        obstacle_video_duration = big2num(byte2str(data[44:45]))
        obstacle_photo_count = big2num(byte2str(data[45:46]))
        obstacle_photo_time = big2num(byte2str(data[46:47]))
        frequent_lane_change_judge_duration = big2num(byte2str(data[47:48]))
        frequent_lane_change_judge_times = big2num(byte2str(data[48:49]))
        frequent_lane_change_level_speed = big2num(byte2str(data[49:50]))
        frequent_lane_change_video_duration = big2num(byte2str(data[50:51]))
        frequent_lane_change_count = big2num(byte2str(data[51:52]))
        frequent_lane_change_time = big2num(byte2str(data[52:53]))
        lane_departure_level_speed = big2num(byte2str(data[53:54]))
        lane_departure_video_duration = big2num(byte2str(data[54:55]))
        lane_departure_video_count = big2num(byte2str(data[55:56]))
        lane_departure_video_time = big2num(byte2str(data[56:57]))
        forward_collision_threshold = big2num(byte2str(data[57:58]))
        forward_collision_level_speed = big2num(byte2str(data[58:59]))
        forward_collision_video_duration = big2num(byte2str(data[59:60]))
        forward_collision_count = big2num(byte2str(data[60:61]))
        forward_collision_time = big2num(byte2str(data[61:62]))
        pedestrian_collision_threshold = big2num(byte2str(data[62:63]))
        pedestrian_collision_level_speed = big2num(byte2str(data[63:64]))
        pedestrian_collision_duration = big2num(byte2str(data[64:65]))
        pedestrian_collision_count = big2num(byte2str(data[65:66]))
        pedestrian_collision_time = big2num(byte2str(data[66:67]))
        too_close_threshold = big2num(byte2str(data[67:68]))
        too_close_level_speed = big2num(byte2str(data[68:69]))
        too_close_duration = big2num(byte2str(data[69:70]))
        too_close_count = big2num(byte2str(data[70:71]))
        too_close_time = big2num(byte2str(data[71:72]))
        road_identify_count = big2num(byte2str(data[72:73]))
        road_identify_time = big2num(byte2str(data[73:74]))
        retain2 = byte2str(data[74:75])
        logger.debug('保留字段:{}'.format(retain1))
        logger.debug('障碍物报警距离阈值:{}'.format(obstacle_distance_threshold))
        logger.debug('障碍物报警分级速度阈值:{}'.format(obstacle_level_speed))
        logger.debug('障碍物报警前后视频录制时间:{}'.format(obstacle_video_duration))
        logger.debug('障碍物报警拍照张数:{}'.format(obstacle_photo_count))
        logger.debug('障碍物报警拍照间隔:{}'.format(obstacle_photo_time))
        logger.debug('频繁变道报警判断时间段:{}'.format(frequent_lane_change_judge_duration))
        logger.debug('频繁变道报警判断次数:{}'.format(frequent_lane_change_judge_times))
        logger.debug('频繁变道报警分级速度阈值:{}'.format(frequent_lane_change_level_speed))
        logger.debug('频繁变道报警前后视频录制时间:{}'.format(frequent_lane_change_video_duration))
        logger.debug('频繁变道报警拍照张数:{}'.format(frequent_lane_change_count))
        logger.debug('频繁变道报警拍照间隔:{}'.format(frequent_lane_change_time))
        logger.debug('车道偏离报警分级速度阈值:{}'.format(lane_departure_level_speed))
        logger.debug('车道偏离报警前后视频录制时间:{}'.format(lane_departure_video_duration))
        logger.debug('车道偏离报警拍照张数:{}'.format(lane_departure_video_count))
        logger.debug('车道偏离报警拍照间隔:{}'.format(lane_departure_video_time))
        logger.debug('前向碰撞报警时间阈值:{}'.format(forward_collision_threshold))
        logger.debug('前向碰撞报警分级速度阈值:{}'.format(forward_collision_level_speed))
        logger.debug('前向碰撞报警前后视频录制时间:{}'.format(forward_collision_video_duration))
        logger.debug('前向碰撞报警拍照张数:{}'.format(forward_collision_count))
        logger.debug('前向碰撞报警拍照间隔:{}'.format(forward_collision_time))
        logger.debug('行人碰撞报警时间阈值:{}'.format(pedestrian_collision_threshold))
        logger.debug('行人碰撞报警使能速度阈值:{}'.format(pedestrian_collision_level_speed))
        logger.debug('行人碰撞报警前后视频录制时间:{}'.format(pedestrian_collision_duration))
        logger.debug('行人碰撞报警拍照张数:{}'.format(pedestrian_collision_count))
        logger.debug('行人碰撞报警拍照间隔:{}'.format(pedestrian_collision_time))
        logger.debug('车距监控报警距离阈值:{}'.format(too_close_threshold))
        logger.debug('车距监控报警分级速度阈值:{}'.format(too_close_level_speed))
        logger.debug('车距过近报警前后视频录制时间:{}'.format(too_close_duration))
        logger.debug('车距过近报警拍照张数:{}'.format(too_close_count))
        logger.debug('车距过近报警拍照间隔:{}'.format(too_close_time))
        logger.debug('道路标识识别拍照张数:{}'.format(road_identify_count))
        logger.debug('道路标识识别拍照间隔:{}'.format(road_identify_time))
        logger.debug('保留字段:{}'.format(retain2))
        logger.debug('———————————————— END ————————————————')

    elif peripheral == b'\x00\x00\xF3\x65':
        logger.debug('====== 查询DSM信息 ======')
        activated_speed = big2num(byte2str(data[22:23]))
        vol = big2num(byte2str(data[23:24]))
        active_photo = big2num(byte2str(data[24:25]))
        active_photo_duration = big2num(byte2str(data[25:27]))
        active_photo_distance = big2num(byte2str(data[27:29]))
        active_photo_count = big2num(byte2str(data[29:30]))
        active_photo_time = big2num(byte2str(data[30:31]))
        photo_resolution = big2num(byte2str(data[31:32]))
        video_resolution = big2num(byte2str(data[32:33]))
        alarm_enable = byte2str(data[33:37])
        event_enable = byte2str(data[37:41])
        smoke_duration = big2num(byte2str(data[41:43]))
        phone_duration = big2num(byte2str(data[43:45]))
        retain1 = byte2str(data[45:48])
        fatigue_level_speed = byte2str(data[48:49])
        fatigue_video_duration = big2num(byte2str(data[49:50]))
        fatigue_photo_count = big2num(byte2str(data[50:51]))
        fatigue_photo_time = big2num(byte2str(data[51:52]))
        photo_level_speed = big2num(byte2str(data[52:53]))
        phone_video_duration = big2num(byte2str(data[53:54]))
        phone_photo_count = big2num(byte2str(data[54:55]))
        phone_photo_time = big2num(byte2str(data[55:56]))
        smoke_level_speed = big2num(byte2str(data[56:57]))
        smoke_video_duration = big2num(byte2str(data[57:58]))
        smoke_photo_count = big2num(byte2str(data[58:59]))
        smoke_photo_time = big2num(byte2str(data[59:60]))
        distracted_level_speed = big2num(byte2str(data[60:61]))
        distracted_video_duration = big2num(byte2str(data[61:62]))
        distracted_photo_count = big2num(byte2str(data[62:63]))
        distracted_photo_time = big2num(byte2str(data[63:64]))
        abnormal_level_speed = big2num(byte2str(data[64:65]))
        abnormal_video_duration = big2num(byte2str(data[65:66]))
        abnormal_photo_count = big2num(byte2str(data[66:67]))
        abnormal_photo_time = big2num(byte2str(data[67:68]))
        driver_identify = byte2str(data[68:69])
        retain2 = byte2str(data[69:71])
        logger.debug('报警使能速度阈值:{}'.format(activated_speed))
        logger.debug('报警提示音量:{}'.format(vol))
        logger.debug('主动拍照策略:{}'.format(active_photo))
        logger.debug('主动拍照间隔时间:{}'.format(active_photo_duration))
        logger.debug('主动拍照间隔距离:{}'.format(active_photo_distance))
        logger.debug('每次主动拍照张数:{}'.format(active_photo_count))
        logger.debug('每次主动拍照间隔时间:{}'.format(active_photo_time))
        logger.debug('拍照分辨率:{}'.format(photo_resolution))
        logger.debug('视频录制分辨率:{}'.format(video_resolution))
        logger.debug('报警使能:{}'.format(alarm_enable))
        logger.debug('事件使能:{}'.format(event_enable))
        logger.debug('吸烟报警判断时间间隔:{}'.format(smoke_duration))
        logger.debug('接打电话报警判断时间间隔:{}'.format(phone_duration))
        logger.debug('保留字段1:{}'.format(retain1))
        logger.debug('疲劳驾驶报警分级速度阈值:{}'.format(fatigue_level_speed))
        logger.debug('疲劳驾驶报警前后录制时长:{}'.format(fatigue_video_duration))
        logger.debug('疲劳驾驶报警拍照张数:{}'.format(fatigue_photo_count))
        logger.debug('疲劳驾驶报警拍照间隔时间:{}'.format(fatigue_photo_time))
        logger.debug('打电话报警分级速度阈值:{}'.format(photo_level_speed))
        logger.debug('打电话报警前后录制时间:{}'.format(phone_video_duration))
        logger.debug('打电话报警拍照张数:{}'.format(phone_photo_count))
        logger.debug('打电话报警时间间隔:{}'.format(phone_photo_time))
        logger.debug('抽烟报警分级速度阈值:{}'.format(smoke_level_speed))
        logger.debug('吸烟报警前后录制时间:{}'.format(smoke_video_duration))
        logger.debug('吸烟报警拍照张数:{}'.format(smoke_photo_count))
        logger.debug('吸烟报警时间间隔:{}'.format(smoke_photo_time))
        logger.debug('分神报警分级速度阈值:{}'.format(distracted_level_speed))
        logger.debug('分神报警前后录制时间:{}'.format(distracted_video_duration))
        logger.debug('分神报警拍照张数:{}'.format(distracted_photo_count))
        logger.debug('分神报警时间间隔:{}'.format(distracted_photo_time))
        logger.debug('驾驶员异常报警分级速度阈值:{}'.format(abnormal_level_speed))
        logger.debug('驾驶异常报警前后录制时间:{}'.format(abnormal_video_duration))
        logger.debug('驾驶异常报警拍照张数:{}'.format(abnormal_photo_count))
        logger.debug('驾驶异常报警时间间隔:{}'.format(abnormal_photo_time))
        logger.debug('驾驶员身份识别触发:{}'.format(driver_identify))
        logger.debug('保留字段3:{}'.format(retain2))
        logger.debug('———————————————— END ————————————————')

    elif peripheral == b'\x00\x00\xF3\x67':
        logger.debug('====== 查询BSD信息 ======')
        behind_threshold = big2num(byte2str(data[22:23]))
        beside_threshold = big2num(byte2str(data[23:24]))
        logger.debug('后方接近报警时间阈值:{}'.format(behind_threshold))
        logger.debug('侧后方接近报警时间阈值:{}'.format(beside_threshold))
        logger.debug('———————————————— END ————————————————')


def parse_upgrade_result_su_ter(data):
    upgrade_type = byte2str(data[13:14])
    upgrade_result = byte2str(data[14:15])
    logger.debug('—————— 终端升级结果: 升级类型 {} 升级结果 ——————'.format(upgrade_type, upgrade_result))


def parse_take_picture_su_ter(data):
    reply_serial_no = byte2str(data[13:15])
    result = byte2str(data[15:16])
    media_num = byte2str(data[16:18])
    media_no = byte2str(data[18:-2])
    logger.debug('———————————————— 立即拍照应答 ————————————————')
    logger.debug('应答流水号 {}'.format(reply_serial_no))
    logger.debug('应答结果 {}'.format(result))
    logger.debug('多媒体数量 {}'.format(media_num))
    logger.debug('多媒体ID {}'.format(media_no))
    logger.debug('———————————————— END ————————————————')