 #!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
Created on 2013-10-30

@author: dell
@summary: 汉字处理的工具:
       判断unicode是否是汉字，数字，英文，或者其他字符。
         全角符号转半角符号。
"""

from string import punctuation 
 
 
def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
                return True
        else:
                return False
 
def is_number(uchar):
        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar <= u'\u0039':
                return True
        else:
                return False

def is_all_number(u_string):
    """
    @summary:  判断一个unicode的字符串是否全为数字
    """
    count = 0
    for uchar in u_string:
        if is_number(uchar):
            count += 1
    if count == len(u_string):
        return True
    else:
        return False
    
def is_num_word(u_string):
    """
    @summary: 判定一个词是数字和字母组合的但是又不是全数字
    """
    
    if is_all_number(u_string):
        return False
    
    for uchar in u_string:
        if is_alphabet(uchar) or is_number(uchar):
            return True
 
def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
                return True
        else:
                return False
 
def is_other(uchar):
        """判断是否非汉字，数字和英文字符"""
        if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
                return True
        else:
                return False
 
def B2Q(uchar):
        """半角转全角"""
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
                return uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code = 0x3000
        else:
                inside_code += 0xfee0
        return unichr(inside_code)
 
def Q2B(uchar):
        """全角转半角"""
        inside_code = ord(uchar)
        if inside_code == 0x3000:
                inside_code = 0x0020
        else:
                inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                return uchar
        return unichr(inside_code)


 
def stringQ2B(ustring):
        """把字符串全角转半角"""
        return "".join([Q2B(uchar) for uchar in ustring])
 
def uniform(ustring):
        """格式化字符串，完成全角转半角，大写转小写的工作"""
        return stringQ2B(ustring).lower()
 
def string2List(ustring):
        """将ustring按照中文，字母，数字分开"""
        retList = []
        utmp = []
        for uchar in ustring:
                if is_other(uchar):
                        if len(utmp) == 0:
                                continue
                        else:
                                retList.append("".join(utmp))
                                utmp = []
                else:
                        utmp.append(uchar)
        if len(utmp) != 0:
                retList.append("".join(utmp))
        return retList
    
def is_punctuation(uchar):
    """
    @summary: 判定是否为标点
    """
    if uchar in punctuation:
        return True
    else:
        return False
    
def replace_punctuation(u_string, r_char=' '):
    
    return ''.join([char if char not in punctuation else r_char  for char in u_string ])


def get_ordered_unique(keywords=[]):
    """
    @summary: 去除list中的重复元素,并保持原有的顺序
    #list(set(lists)) 这样是不能保持顺序的.
    """
    return  sorted(set(keywords), key=keywords.index)

    
 
if __name__ == "__main__":
        # test Q2B and B2Q
        for i in range(0x0020, 0x007F):
                print Q2B(B2Q(unichr(i))), B2Q(unichr(i))
 
        # test uniform
        ustring = u'中国 人名ａ高频Ａ'
        ustring = uniform(ustring)
        ret = string2List(ustring)
        tmp = '3d'
        print is_alphabet(tmp)
        print is_number(tmp)
        print is_number('d3')
        print is_alphabet('uchar')
        
        x = is_all_number(tmp)
        tmp = is_number(tmp)
        
        print tmp
