#!/usr/bin/env python
# -*- coding: utf-8 -*

from ParseModel.Parse_JT808 import *
from ParseModel.Parse_SU import *
from ParseModel.Parse_SU_TER import *
from ParseModel.Parse_SF import *


class Consumer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        # self.rec_obj = rec_obj
        self.setName(self.name)

    def run(self):
        logger.debug(threading.current_thread().getName())
        while True:
            while not rec_queue.empty():
                try:
                    data = rec_queue.get_nowait()
                except queue.Empty:
                    data = None
                if data:
                    data_rec = data
                    text = byte2str(data)
                    text_hex = ' '.join(text[i:i + 2] for i in range(0, len(text), 2))
                    logger.debug(
                        '%s%s%s%s%s' % ("RECV DATA:   ", 'lens: ', str(len(data_rec)).ljust(5, ' '), '   data: || ', text_hex))

                    # 进入解析过程
                    if conf.get_protocol_type() == 1:
                        command = data[6:8]
                    elif conf.get_protocol_type() == 2:
                        command = data[9:12]
                    elif conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
                        command = data[1:3]
                    elif conf.get_protocol_type() == 4:
                        n = 0
                        if big2num(byte2str(data[2:3])) & 0x80 == 0:
                            pass
                        elif big2num(byte2str(data[3:4])) & 0x80 == 0:
                            n += 1
                        elif big2num(byte2str(data[4:5])) & 0x80 == 0:
                            n += 1
                        else:
                            n += 1
                        command = big2num(byte2str(data[33 + n:35 + n])) >> 6
                    if get_media_command_dict.get(command):
                        rec_alarm_queue.put((data, command))
                    else:
                        # parse(data, command)
                        common_queue.put((data, command))
                time.sleep(0.001)
            time.sleep(0.001)


parse_type_su = {
    UPGRADE_SU: lambda x: parse_upgrade_su(x),
    GET_LOG: lambda x: parse_get_log_su(x),
    STATE_REPORT_DSM: lambda x: parse_state_report(x),
    STATE_REPORT_ADAS: lambda x: parse_state_report(x),
    b'\x65\x37': lambda x: parse_query_state_report(x),
    b'\x64\x37': lambda x: parse_query_state_report(x),
    b'\x65\x30': lambda x: parse_reset(x),
    b'\x64\x30': lambda x: parse_reset(x),
    b'\x65\x2f': lambda x: parse_query_peripheral(x),
    b'\x64\x2f': lambda x: parse_query_peripheral(x),
    b'\x65\x35': lambda x: parse_set_para_reply(x),
    b'\x64\x35': lambda x: parse_set_para_reply(x),
    b'\x65\xff': lambda x: parse_set_device_id(x),
    b'\x64\xff': lambda x: parse_set_device_id(x),
    b'\x65\xfd': lambda x: parse_tf_status(x),
    b'\x64\xfd': lambda x: parse_tf_status(x),
    b'\x65\xfc': lambda x: parse_adas_status(x),
    b'\x64\xfc': lambda x: parse_adas_status(x),
    b'\x65\xfb': lambda x: parse_smoke_sensor_status(x),
    b'\x64\xfb': lambda x: parse_smoke_sensor_status(x),
    GET_DSM_INFO: lambda x: parse_get_info(x),
    GET_ADAS_INFO: lambda x: parse_get_info(x),
    QUERY_DSM_PARA: lambda x: parse_query_dsm_para(x),
    QUERY_ADAS_PARA: lambda x: parse_query_adas_para(x),
    b'\x65\xfa': lambda x: parse_get_log_result_su(x),
    b'\x64\xfa': lambda x: parse_get_log_result_su(x),
    b'\x65\xfe': lambda x: parse_turn_signal_status(x),
    b'\x64\xfe': lambda x: parse_turn_signal_status(x),
          }


parse_type_jt808 = {
    LOCATION_UPLOAD: lambda x: parse_location_upload_jt808(x),
    HEART_BEAT: lambda x: parse_heart_jt808(x),
    AUTHENTICATION: lambda x: parse_authentication_jt808(x),
    REGISTER: lambda x: parse_register_jt808(x),

    b'\x01\x07': lambda x: parse_query_pro_jt808(x),
    b'\x01\x04': lambda x: parse_query_para_jt808(x),
    b'\x01\x08': lambda x: parse_upgrade_result_jt808(x),
    b'\x00\x01': lambda x: parse_device_comm_reply_jt808(x),
    b'\x8f\x03': lambda x: parse_route_id_jt808(x),
    b'\x0f\xa1': lambda x: parse_upgrade_request_jt808(x),
    b'\x8B\x01': lambda x: parse_driver_manage_jt808(x),
    b'\x08\x05': lambda x: parse_take_picture_jt808(x),
}
parse_type_su_ter = {
    LOCATION_UPLOAD: lambda x: parse_location_upload_su_ter(x),
    HEART_BEAT: lambda x: parse_heart_su_ter(x),
    AUTHENTICATION: lambda x: parse_authentication_su_ter(x),
    REGISTER: lambda x: parse_register_su_ter(x),

    b'\x01\x07': lambda x: parse_query_pro_su_ter(x),
    b'\x09\x00': lambda x: parse_upload_msg_su_ter(x),
    b'\x01\x04': lambda x: parse_query_para_su_ter(x),
    b'\x01\x08': lambda x: parse_upgrade_result_su_ter(x),
    b'\x08\x05': lambda x: parse_take_picture_su_ter(x),
    b'\x00\x01': lambda x: parse_device_comm_reply_su_ter(x),

}

parse_type_su_ter_for_file = {
    b'\x12\x10': lambda x, y: parse_alarm_attachment_msg_su_ter(x, y),
    b'\x12\x11': lambda x, y: parse_media_msg_upload_su_ter(x, y),
    b'\x12\x12': lambda x, y: parse_media_upload_finish_su_ter(x, y)
}

parse_type_sf = {
    2: lambda x: parse_login_sf(x),
    3: lambda x: parse_register_sf(x),
    6: lambda x: send_upgrade_pkg_sf(x),
    8: lambda x: parse_upgrade_result_sf(x),
    100: lambda x: parse_device_msg_sf(x),
    101: lambda x: parse_device_pro_sf(x),
    102: lambda x: parse_location_upload_sf(x),
    103: lambda x: parse_alarm_upload_sf(x),
    104: lambda x: parse_media_upload_sf(x),
    105: lambda x: parse_device_para_sf(x),
}


class ParseComm(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        # self.rec_obj = rec_obj
        self.setName(self.name)

    def run(self):
        logger.debug(threading.current_thread().getName())
        while True:
            try:
                data, command = common_queue.get_nowait()
            except queue.Empty:
                data = None
            if data:
                if conf.get_protocol_type() == 1:
                    func = parse_type_su.get(command)
                    if func:
                        func(data)
                elif conf.get_protocol_type() == 2:
                    func = parse_type.get(command)
                    if func:
                        func(data)
                elif conf.get_protocol_type() == 3:
                    func = parse_type_jt808.get(command)
                    if func:
                        func(data)
                elif conf.get_protocol_type() == 4:
                    func = parse_type_sf.get(command)
                    if func:
                        func(data)
                elif conf.get_protocol_type() == 5:
                    func = parse_type_su_ter.get(command)
                    if func:
                        func(data)
            time.sleep(0.001)
