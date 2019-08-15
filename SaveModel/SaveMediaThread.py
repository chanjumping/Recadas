#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.CommonMethod import *
from Util.GlobalVar import *
from Util.ReadConfig import conf


class SaveMediaThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.setName(self.name)
        self.media_name = None
        self.buf = b''

    def run(self):
        logger.debug(threading.current_thread().getName())
        if not os.path.exists('Result'):
            os.mkdir('Result')
        while True:
            if conf.get_protocol_type() == 1:
                while not media_queue.empty():
                    data = media_queue.get(block=False)
                    media_data = data[17:-1]
                    self.buf += media_data
                    total = int(byte2str(data[13:15]), 16)
                    rec = int(byte2str(data[15:17]), 16)
                    if rec == total - 1:
                        media_id = byte2str(data[9:13])
                        if data[6:7] == b'\x65':
                            event_type = alarm_type_code_su_dsm.get(media_alarm_code.get(media_id))
                            dir_name = os.path.join('Result', 'DSM_media')
                        else:
                            event_type = alarm_type_code_su_adas.get(media_alarm_code.get(media_id))
                            dir_name = os.path.join('Result', 'ADAS_media')
                        if not os.path.exists(dir_name):
                            os.makedirs(dir_name)
                        media_type = byte2str(data[8:9])
                        if media_type == '00':
                            self.media_name = r'告警ID{}_{}.jpg'.format(int(media_id, 16), event_type)
                        elif media_type == '02':
                            self.media_name = r'告警ID{}_{}.mp4'.format(int(media_id, 16), event_type)
                        elif media_type == '01':
                            self.media_name = r'告警ID{}_{}.mp3'.format(int(media_id, 16), event_type)
                        else:
                            logger.error('未知的多媒体类型。')
                        file_name = os.path.join(dir_name, self.media_name)
                        if os.path.exists(file_name):
                            file_name_list = file_name.split('.')
                            file_name_list[0] += '_bak'
                            file_name = '.'.join(file_name_list)
                        with open(file_name, 'ab') as f:
                            f.write(self.buf)
                            self.buf = b''
                        try:
                            if media_alarm_code:
                                media_alarm_code.pop(media_id)
                        except KeyError:
                            logger.error('media_id{}不存在。'.format(media_id))
            elif conf.get_protocol_type() == 3:
                while not media_queue.empty():
                    data = media_queue.get(block=False)
                    total_pkg = big2num(byte2str(data[13:15]))
                    pkg_no = big2num(byte2str(data[15:17]))
                    path_dir = os.path.join('Result', 'Alarm_Media')
                    if not os.path.exists(path_dir):
                        os.mkdir(path_dir)
                    if pkg_no == 1:
                        img_data = data[53:-2]
                        self.buf += img_data
                        media_id_byte = data[17:21]
                        media_id = big2num(byte2str(media_id_byte))
                        media_type = big2num(byte2str(data[21:22]))
                        event_type = big2num(byte2str(data[23:24]))
                        channel = byte2str(data[24:25])
                        speed = big2num(byte2str(data[43:45]))
                        alarm_time = byte2str(data[47:53])

                        if media_type == 0:
                            self.media_name = r"告警ID{}_{}_通道{}_速度{}_{}.{}".format(media_id, alarm_type_code_jt808.get(event_type),
                                                                          channel, str(speed), alarm_time, 'jpg')
                        elif media_type == 2:
                            self.media_name = r"告警ID{}_{}_通道{}_速度{}_{}.{}".format(media_id, alarm_type_code_jt808.get(event_type),
                                                                          channel, str(speed), alarm_time, 'mp4')
                        if os.path.exists(os.path.join(path_dir, self.media_name)):
                            file_name_list = self.media_name.split('.')
                            file_name_list[0] += '_bak'
                            self.media_name = '.'.join(file_name_list)
                    else:
                        img_data = data[17:-2]
                        self.buf += img_data
                        if total_pkg == pkg_no:
                            try:
                                with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                    f.write(self.buf)
                            except PermissionError:
                                logger.error(PermissionError)
                                with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                    f.write(self.buf)
                            except FileNotFoundError:
                                logger.error(FileNotFoundError)
                            self.buf = b''
                            self.media_name = ''
            elif conf.get_protocol_type() == 5:
                while not media_queue.empty():
                    data = media_queue.get(block=False)
                    if data[0:4] == b'\x30\x31\x63\x64':
                        media_name = data[4:54].split(b'\x00')[0].decode('utf-8')
                        media_name_bak = media_name
                        media_size = name_size.get(media_name)
                        media_type = media_name.split('_')[2]
                        if media_type[:2] == '65':
                            media_type = alarm_type_code_su_ter_dsm.get(bytes.fromhex(media_type[2:]))
                        elif media_type[:2] == '64':
                            media_type = alarm_type_code_su_ter_adas.get(bytes.fromhex(media_type[2:]))
                        else:
                            media_type = 'error'
                        media_name = media_name.replace('.', '_{}.'.format(media_type))
                        media_name_list = media_name.split('_')
                        media_name = media_name_list[4][:16] + '_' + '_'.join(media_name_list)
                        # media_name = media_type + "_" + media_name
                        offset = big2num(byte2str(data[54:58]))
                        data_length = big2num(byte2str(data[58:62]))
                        data_content = data[62: 62 + data_length]
                        self.buf += data_content
                        if offset + data_length == media_size:
                            path_dir = os.path.join('Result', 'Alarm_Media')
                            if not os.path.exists(path_dir):
                                os.mkdir(path_dir)
                            with open(os.path.join(path_dir, media_name), 'ab') as f:
                                f.write(self.buf)
                                name_size.pop(media_name_bak)
                            self.buf = b''
                            self.media_name = ''
                    else:
                        total_pkg = big2num(byte2str(data[13:15]))
                        pkg_no = big2num(byte2str(data[15:17]))
                        path_dir = os.path.join('Result', 'Alarm_Media')
                        if not os.path.exists(path_dir):
                            os.mkdir(path_dir)
                        if pkg_no == 1:
                            img_data = data[53:-2]
                            self.buf += img_data
                            media_id_byte = data[17:21]
                            media_id = big2num(byte2str(media_id_byte))
                            media_type = big2num(byte2str(data[21:22]))
                            event_type = data[23:24]
                            channel = byte2str(data[24:25])
                            speed = int(big2num(byte2str(data[43:45])))/10
                            alarm_time = byte2str(data[47:53])

                            if media_type == 0:
                                self.media_name = r"告警ID{}_{}_通道{}_速度{}_{}.{}".format(media_id,
                                                event_type_su_ter.get(event_type), channel, speed, alarm_time, 'jpg')
                            elif media_type == 2:
                                self.media_name = r"告警ID{}_{}_通道{}_速度{}_{}.{}".format(media_id,
                                                event_type_su_ter.get(event_type), channel, speed, alarm_time, 'mp4')
                            if os.path.exists(os.path.join(path_dir, self.media_name)):
                                file_name_list = self.media_name.split('.')
                                file_name_list[0] += '_bak'
                                self.media_name = '.'.join(file_name_list)
                        else:
                            img_data = data[17:-2]
                            self.buf += img_data
                            if total_pkg == pkg_no:
                                try:
                                    with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                        f.write(self.buf)
                                except PermissionError:
                                    logger.error(PermissionError)
                                    with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                        f.write(self.buf)
                                except FileNotFoundError:
                                    logger.error(FileNotFoundError)
                                self.buf = b''
                                self.media_name = ''
                time.sleep(0.001)
            time.sleep(0.5)
