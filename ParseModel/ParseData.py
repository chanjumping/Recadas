#!/usr/bin/env python
# -*- coding: utf-8 -*
from Util.CommonMethod import *
from Util.GlobalVar import *
from Util.ReadConfig import conf
from Util.Log import log_event


def produce(buf, remain):
    if conf.get_protocol_type() == 1:
        data = remain + buf
        st_list = [m.start() for m in re.finditer(b"\x7e", data)]
        current = -1
        for x in range(len(st_list)):
            if st_list[x] <= current:
                continue
            if not st_list[x] == st_list[-1]:
                if st_list[x]+1 == st_list[x+1]:
                    logger.info(data[st_list[x]:st_list[x]+2])
                    continue
            for y in range(x + 1, len(st_list)):
                data_piece = rec_translate(data[st_list[x]:st_list[y] + 1])
                if byte2str(data_piece[1:2]) == calc_check_code(byte2str(data_piece[4:-1])):
                    rec_queue.put(data_piece)
                    current = st_list[y]
                    break
                else:
                    logger.error("未能解析的7E数据" + byte2str(data_piece))
        remain = data[current + 1:]
        return remain
    elif conf.get_protocol_type() == 2:
        data = remain + buf
        # 找出所有FB的位置
        st_list = [m.start() for m in re.finditer(b"\xfb", data)]
        # current 变量用于记录当前截取的有效报文末位的索引
        current = -1
        for x in range(len(st_list)):
            # 若FB位于 current之前，则忽略不处理
            if st_list[x] < current:
                continue
            # 判断剩余的报文是否满足报文的最短要求
            elif len(data[st_list[x]:]) >= 15:
                # 判断保留位是否为0
                if data[st_list[x] + 5:st_list[x] + 9] == b'\x00\x00\x00\x00':
                    len_start = st_list[x] + 1
                    len_end = st_list[x] + 5
                    length_hex = byte2str(data[len_start:len_end])
                    length = small2num(length_hex)
                    # 根据报文长度截出相应的报文
                    data_piece = data[st_list[x]:st_list[x] + length]
                    # 判断报文长度字段与实际报文长度是否一致
                    if len(data_piece) == length:
                        data_piece_hex = byte2str(data_piece)
                        calc_code = calc_check_code(data_piece_hex[:-2])
                        check_code = data_piece_hex[-2:]
                        # 判断校验码与实际校验字段是否一致
                        if calc_code == check_code:
                            rec_queue.put(data_piece)
                            current = st_list[x] + length
                        else:
                            logger.error(byte2str(data_piece))
        if current == -1:
            current = 0
        remain = data[current:]
        return remain
    elif conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        data = remain + buf
        if data[0:1] == b'\x7e':
            st_list = [m.start() for m in re.finditer(b"\x7e", data)]
            if len(st_list) >= 2:
                data_piece = data[:st_list[1] + 1]
                data_piece = rec_translate(data_piece)
                if byte2str(data_piece[-2:-1]) == calc_check_code(byte2str(data_piece[1:-2])):
                    rec_queue.put(data_piece)
                    remain = data[st_list[1]+1:]
                else:
                    logger.error('校验码错误。')
                    logger.error(byte2str(data_piece))
            else:
                remain = data
        elif data[0:4] == b'\x30\x31\x63\x64':
            data_length = data[58:62]
            if data_length:
                if big2num(byte2str(data_length)) + 62 > len(data):
                    remain = data
                else:
                    data_piece = data[:62 + big2num(byte2str(data_length))]
                    media_queue.put(data_piece)
                    text = byte2str(data)[:200]
                    text_hex = ' '.join(text[i:i + 2] for i in range(0, len(text), 2))
                    logger.debug('%s%s%s%s%s' % ("RECV DATA:   ", 'lens: ',
                                                 str(len(data_piece)).ljust(5, ' '), '   data: || ', text_hex))
                    remain = data[62 + big2num(byte2str(data_length)):]
            else:
                remain = data
        else:
            if len(data) >= 4:
                logger.error('收到错误开头的报文。')
                logger.error(byte2str(data))
            else:
                remain = data
        return remain
    elif conf.get_protocol_type() == 4:
        data = remain + buf
        st_list = [m.start() for m in re.finditer(b"\x55", data)]
        current = -1
        for x in range(len(st_list)):
            if st_list[x] <= current:
                continue
            if not st_list[x] == st_list[-1]:
                if st_list[x]+1 == st_list[x+1]:
                    logger.info(data[st_list[x]:st_list[x]+2])
                    continue
            for y in range(x + 1, len(st_list)):
                data_piece = rec_translate(data[st_list[x]:st_list[y] + 1])
                if len(data_piece) > 2:
                    rec_queue.put(data_piece)
                    current = st_list[y]
                    break
                else:
                    logger.error("未能解析的55数据" + byte2str(data_piece))
        remain = data[current + 1:]
        return remain


def send_queue_data():
    try:
        data = send_queue.get_nowait()
    except queue.Empty:
        data = None
    if data:
        if ' ' in data:
            data = ''.join(data.split(' '))
        data_bak = data
        if conf.get_protocol_type() == 1 or conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
            data = send_translate(bytes.fromhex(data))
            send_data = data
        elif conf.get_protocol_type() == 2:
            data = bytes.fromhex(data)
            send_data = data
        elif conf.get_protocol_type() == 4:
            data = send_translate(bytes.fromhex(data))
            send_data = data
        else:
            logger.debug('读取协议类型错误。')

        if conf.get_protocol_type() == 1:
            if bytes.fromhex(data_bak)[7:8] == b'\x50':
                media_id = data[-5:-1]
                log_event.debug('—————— 正在请求多媒体ID为 {} 的数据 ——————'.format(byte2str(media_id)))

        text_hex = ' '.join(data_bak[i:i + 2] for i in range(0, len(data_bak), 2))
        if len(text_hex) > 3000:
            text_hex = text_hex[:3000]
        if conf.get_protocol_type() == 1:
            if not data_bak[14:16] == '31':
                logger.debug('%s%s%s%s%s' % ("SEND DATA:   ", 'lens: ', str(int(len(data_bak)/2)).ljust(5, ' '), '   data: || ', text_hex))
            else:
                serial_no_ = big2num(data_bak[4:8])
                if serial_no_ % 120 == 1:
                    logger.debug('—————— 实时数据同步信息 ——————')
                    logger.debug('%s%s%s%s%s' % (
                    "SEND DATA:   ", 'lens: ', str(int(len(data_bak) / 2)).ljust(5, ' '), '   data: || ', text_hex))

        else:
            logger.debug('%s%s%s%s%s' % ("SEND DATA:   ", 'lens: ', str(int(len(data_bak) / 2)).ljust(5, ' '), '   data: || ', text_hex))
        return send_data

