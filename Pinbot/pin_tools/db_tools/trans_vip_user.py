# coding: utf-8
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from app.vip.models import (
    UserVip,
    VipRoleSetting,
)
from app.pinbot_point.point_utils import (
    point_utils,
)

users = [
    ('zhaopin@ibookstar.com', 4800, '2015/5/27', '2015/8/27'),
    ('clark@zenzet.com', 4800, '2015/5/28', '2015/8/28'),
    ('guliju@youfumama.com', 4800, '2015/6/2', '2015/9/2'),
    ('juancao@deepglint.com', 4800, '2015/6/5', '2015/9/5'),
    ('daniel.ma@10buck.com', 1900, '2015/6/3', '2015/9/3'),
    ('hr@bp1010.com', 4800, '2015/6/4', '2015/9/4'),
    ('xh.qin@91kge.com', 1900, '2015/6/5', '2015/9/5'),
    ('job@xuelab.com', 4800, '2015/6/5', '2015/9/5'),
    ('yudan@tigerbrokers.com', 4800, '2015/6/6', '2015/9/6'),
    ('yuchen@mikecrm.com', 4800, '2015/6/8', '2015/9/8'),
    ('wanxing@dino-info.com', 4800, '2015/6/8', '2015/9/8'),
    ('623220723@qq.com', 4800, '2015/6/9', '2015/9/9'),
    ('shallow919@126.com', 4800, '2015/6/9', '2015/9/9'),
    ('xulei@uubee.com', 1900, '2015/6/9', '2015/9/9'),
    ('happyjob@mfashion.com.cn', 4800, '2015/6/11', '2015/9/11'),
    ('jhj@dianmi365.com', 4800, '2015/6/12', '2015/9/12'),
    ('hr@cnpayany.com', 4800, '2015/6/12', '2015/9/12'),
    ('jeannie@spiiker.com', 3200, '2015/6/12', '2015/9/12'),
    ('dongjie@ikcare.com', 4800, '2015/6/15', '2015/9/15'),
    ('hr@2345.com', 9600, '2015/6/16', '2015/9/16'),
    ('hr@moyi365.com', 4800, '2015/6/17', '2015/9/17'),
    ('23570824@qq.com', 4800, '2015/6/18', '2015/9/18'),
    ('hr@misihui.com', 4800, '2015/6/18', '2015/9/18'),
    ('hr@carisok.com', 9600, '2015/6/19', '2015/9/19'),
    ('zhanghuili@appvv.com', 1900, '2015/6/19', '2015/9/19'),
    ('jix@fxdata.cn', 4800, '2015/6/19', '2015/9/19'),
    ('linxiejing@huaxunchina.cn', 4800, '2015/6/23', '2015/9/23'),
    ('hr@wojuzuke.com', 4800, '2015/6/24', '2015/9/24'),
    ('huwen@dyyycapital.com', 4800, '2015/6/24', '2015/9/24'),
    ('fangyj@ync365.com', 4800, '2015/6/24', '2015/9/24'),
    ('xulei@uubee.com', 4800, '2015/6/25', '2015/9/25'),
    ('shijianjing@knet.cn', 9600, '2015/6/26', '2015/9/26'),
    ('abing_hu@163.com', 4800, '2015/6/29', '2015/9/29'),
    ('jm_wen@droidhang.com', 4800, '2015/6/29', '2015/9/29'),
    ('hr@yintong.com.cn', 4800, '2015/6/29', '2015/9/29'),
    ('hr@ixiaokan.cn', 4800, '2015/6/30', '2015/9/30'),
    ('zhaojingfang@beequick.cn', 4800, '2015/6/30', '2015/9/30'),
    ('yifeng.lu@2339.com', 1600, '2015/7/1', '2015/10/1'),
    ('yifeng.lu@2339.com', 3500, '2015/7/1', '2015/10/1'),
    ('shiyn@jjmmw.com', 4800, '2015/7/1', '2015/10/1'),
    ('xyy@kingtion.com', 4800, '2015/7/2', '2015/10/1'),
    ('45299740@qq.com', 7500, '2015/7/2', '2015/9/2'),
    ('jiangma@ungtse.com', 2400, '2015/7/2', '2015/10/1'),
    ('xiycheng@thoughtworks.com', 4800, '2015/7/3', '2015/10/3'),
    ('364359107@qq.com', 4800, '2015/7/3', '2015/10/3'),
    ('hr@diandianzu.com', 4800, '2015/7/3', '2015/10/3'),
    ('hr@laibatour.com', 6600, '2015/7/6', '2015/10/6'),
    ('hr@yimihaodi.com', 1900, '2015/7/7', '2015/10/7'),
    ('shuang.zhang@qingteng.me', 7600, '2015/7/9', '2015/10/9'),
    ('qiatuhangzhou@gmail.com', 6600, '2015/7/10', '2015/10/10'),
    ('marlon@baicizhan.com', 10000, '2015/7/16', '2015/10/16'),
    ('sophia.zhang@tcl.com', 4800, '2015/7/16', '2015/10/16'),
    ('koumin@wiseway3.com', 6600, '2015/7/17', '2015/10/17'),
    ('hr@yundongpai.net', 4800, '2015/7/20', '2015/10/20'),
    ('hr@csqing.com', 6600, '2015/7/20', '2015/10/20'),
    ('916024474@qq.com', 6600, '2015/7/21', '2015/10/21'),
    ('hr@dosomi.com', 5000, '2015/7/23', '2015/10/23'),
    ('hr.wego@dfs168.com', 5940, '2015/7/29', '2015/10/29'),
    ('scott@novolio.com', 5940, '2015/7/23', '2015/10/23'),
    ('hr@9niu.com', 6600, '2015/7/28', '2015/9/28'),
    ('zhaopin@hr.jj.cn', 8700, '2015/7/30', '2015/10/30'),
    ('2543478925@qq.com', 5800, '2015/7/31', '2015/10/31'),
    ('zhaoliuliu@jiadao.cn', 6600, '2015/7/31', '2015/10/31'),
    ('fengxin@lionbridgecapital.cn', 6600, '2015/8/4', '2015/11/4'),
    ('hr01@tingyun.com', 5940, '2015/8/5', '2015/11/5'),
    ('hr@tomtop.com', 10000, '2015/8/12', '2015/11/12'),
    ('hr@sczhtech.com', 5800, '2015/8/17', '2015/11/17'),
    ('xianhaihr@521g.com', 6600, '2015/8/17', '2015/11/17'),
    ('hr@icongtai.com', 5100, '2015/8/17', '2015/11/17'),
    ('zny@h3d.com.cn', 6600, '2015/8/19', '2015/11/19'),
    ('zongweiwei@patsnap.com', 2700, '2015/8/20', '2015/9/20'),
    ('1320101207@qq.com', 6600, '2015/8/24', '2015/11/24'),
    ('totwoohr@totwoo.com', 5800, '2015/8/24', '2015/11/24'),
    ('1464487@qq.com', 6600, '2015/8/24', '2015/11/24'),
    ('12758794@qq.com', 6600, '2015/8/24', '2015/11/24'),
    ('275322122@qq.com', 6600, '2015/8/24', '2015/11/24'),
    ('wangxin@ilikelabs.com', 6600, '2015/8/24', '2015/11/24'),
    ('8343080@qq.com', 13200, '2015/8/25', '2015/11/25'),
    ('275194385@qq.com', 6600, '2015/8/25', '2015/11/25'),
    ('hr@dbi.net.cn', 6600, '2015/8/25', '2015/11/25'),
    ('21089870@qq.com', 6600, '2015/8/25', '2015/11/25'),
    ('qinan@bolmedia.cn', 6600, '2015/8/26', '2015/11/26'),
    ('hr@idealhere.com', 5940, '2015/8/27', '2015/11/27'),
    ('dukedu@vip.qq.com', 6600, '2015/8/27', '2015/11/27'),
    ('firstlinkapp@gmail.com', 6600, '2015/8/28', '2015/11/28'),
    ('tangruiling257@pingan.com.cn', 6600, '2015/8/31', '2015/11/31'),
    ('zhangmeng@noyan.com.cn', 6600, '2015/8/31', '2015/11/31'),
    ('hr@acewill.cn', 5940, '2015/9/2', '2015/12/2'),
    ('jowett.zhang@julewu.com', 6600, '2015/9/6', '2015/12/6'),
    ('hr@ikaowo.com', 6000, '2015/9/9', '2015/12/9'),
    ('hr@max-v.com', 5800, '2015/9/8', '2015/12/8'),
    ('hr@detu.com', 6600, '2015/9/11', '2015/12/11'),
    ('keqiang@foryou56.com', 6600, '2015/9/11', '2015/12/11'),
    ('michelle.qin@ismond.com', 6600, '2015/9/11', '2015/12/11'),
    ('187201434@qq.com', 7100, '2015/9/11', '2015/11/11'),
    ('2824734279@qq.com', 6600, '2015/9/14', '2015/12/14'),
    ('247024919@qq.com', 2900, '2015/9/14', '2015/12/14'),
    ('hr@weplanter.com', 9405, '2015/9/15', '2015/12/15'),
    ('zhouyujie@tianailu.com', 6600, '2015/9/15', '2015/12/15'),
]

username_list = [i[0] for i in users]


def trans_normal():
    vip_a = VipRoleSetting.objects.get(code_name='self_a')
    UserVip.objects.filter(
        vip_role__code_name='trial_vip',
        is_active=True,
    ).exclude(
        user__username__in=username_list,
    ).update(
        vip_role=vip_a
    )
    print '转化普通会员成功'


def trans_vip():
    vip_b = VipRoleSetting.objects.get(code_name='self_b')
    all_vip = UserVip.objects.select_related('user').filter(
        vip_role__code_name='normal_vip',
        is_active=True,
    ).exclude(
        user__username__in=username_list,
    )

    user_list = [i.user for i in all_vip]

    all_vip.update(
        vip_role=vip_b
    )
    for user in user_list:
        point_utils.trans_point(user)

    print '转化vip会员成功'


if __name__ == '__main__':
    trans_normal()
    trans_vip()
