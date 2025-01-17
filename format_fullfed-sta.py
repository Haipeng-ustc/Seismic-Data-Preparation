""" format station file in Fullfed format, e.g. http://www.fdsn.org/networks/detail/7D_2011/
"""
import numpy as np
from obspy import UTCDateTime

# i/o paths
fsta = 'input/station_eg.fullfed'
fout = open('output/station_eg.csv','w')
chn_codes = ['HH','BH']
lat_min, lat_max = 40., 49.
lon_min, lon_max = -128, -126
t_min, t_max = UTCDateTime('20110101'), UTCDateTime('20170101')

sta_dict = {}
f=open(fsta); lines=f.readlines(); f.close()
for line in lines[3:]:
    codes = line.split('|')
    if len(codes)<11: continue
    net_sta = '.'.join(codes[0:2])
    chn = codes[3]
    net_sta_chn = '%s.%s'%(net_sta, chn[0:2])
    if chn[0:2] not in chn_codes: continue
    lat, lon, ele = [float(code) for code in codes[4:7]]
    if not (lat_min<lat<lat_max and lon_min<lon<lon_max): continue
    gain = float(codes[11])
    t0, t1 = [UTCDateTime(code) for code in codes[-2:]]
    if t1<t_min or t0>t_max: continue
    if net_sta_chn not in sta_dict: sta_dict[net_sta_chn] = [lat, lon, ele, [gain], [t0.date,t1.date]]
    else: sta_dict[net_sta_chn][-2].append(gain)

out_lines = []
net_sta_old = '0.0'
for net_sta_chn, [lat, lon, ele, gains, [t0,t1]] in sta_dict.items():
    net,sta,chn = net_sta_chn.split('.')
    net_sta = '%s.%s'%(net,sta)
    if len(gains)==1: gain_code = '%s,%s,%s'%(gains[0], gains[0], gains[0])
    else: gain_code = '%s,%s,%s'%(gains[0], gains[1], gains[2])
    out_line = '{},{},{},{},{},{},{}\n'.format(net_sta_chn, lat, lon, ele, gain_code, t0, t1)
    if net_sta!=net_sta_old: out_lines.append(out_line)
    else: out_lines[-1] = out_line
    net_sta_old = net_sta
for line in out_lines: fout.write(line)
fout.close()
