from icepyx import icesat2data as ipd
import os
import shutil

region_a = ipd.Icesat2Data('ATL06',[-55, 68, -48, 71],['2019-02-01','2019-02-28'], \
                            start_time='00:00:00', end_time='23:59:59', version='002')

earthdata_uid = 'icepyx_devteam'
email = 'icepyx.dev@gmail.com'
region_a.earthdata_login(earthdata_uid, email)

region_a.order_granules()