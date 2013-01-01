# coding:utf-8
''' scholar search character detector
@author yakergong<yakergong at gmail dot com>
'''
import chardet

encoding_alias = { 
    # gb2312 is superseded by gb18030
    'gb2312': 'gb18030',
    'chinese': 'gb18030',
    'csiso58gb231280': 'gb18030',
    'euc- cn': 'gb18030',
    'euccn': 'gb18030',
    'eucgb2312-cn': 'gb18030',
    'gb2312-1980': 'gb18030',
    'gb2312-80': 'gb18030',
    'iso- ir-58': 'gb18030',
    # gbk is superseded by gb18030
    'gbk': 'gb18030',
    '936': 'gb18030',
    'cp936': 'gb18030',
    'ms936': 'gb18030',
    # latin_1 is a subset of cp1252
    'latin_1': 'cp1252',
    'iso-8859-1': 'cp1252',
    'iso8859-1': 'cp1252',
    '8859': 'cp1252',
    'cp819': 'cp1252',
    'latin': 'cp1252',
    'latin1': 'cp1252',
    'l1': 'cp1252',
    # others
    'zh-cn': 'gb18030',
    'win-1251': 'cp1251',
    'macintosh' : 'mac_roman',
    'x-sjis': 'shift_jis',
}


def detect(uBuf, extraEc=''):
    ec_list = ['gb18030','utf-8','cp1252','ascii'];
    if extraEc:
        ec_list.insert(0, extraEc)
    for encoding in ec_list:
        try:
            data_utf8 = uBuf.decode(encoding)
        except Exception, e:
            continue
        return encoding
    result_cd = chardet.detect(uBuf)
    if result_cd['confidence'] > 0.9:
        ret = result_cd['encoding'].lower()
        if ret in encoding_alias:
            ret = encoding_alias[ret]
        return ret
    return encoding
