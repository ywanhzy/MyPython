# coding=utf-8

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
import pandas as pd
import numpy as np

plt.figure(figsize=(16,8))
#平面地图
m = Basemap(
    llcrnrlon=77,
    llcrnrlat=14,
    urcrnrlon=140,
    urcrnrlat=51,
    projection='lcc',
    lat_1=33,
    lat_2=45,
    lon_0=100
)
#圆形地图
# m = Basemap(projection='ortho',lat_0=35,lon_0=120,resolution='l')

# draw coastlines, country boundaries, fill continents.
m.drawcountries(linewidth=0.25)
m.drawcoastlines(linewidth=0.25)

# # draw the edge of the map projection region (the projection limb)
# m.drawmapboundary(fill_color='#689CD2')
# # draw lat/lon grid lines every 30 degrees.
# m.drawmeridians(np.arange(0,360,30))
# m.drawparallels(np.arange(-90,90,30))
# # Fill continent wit a different color
# m.fillcontinents(color='#BF9E30',lake_color='#689CD2',zorder=0)
# # compute native map projection coordinates of lat/lon grid.


m.readshapefile('CHN_adm_shp/CHN_adm1', 'states', drawbounds=True)

df = pd.read_csv('CHN_adm_shp/rkpc.csv')
# df = pd.read_excel('CHN_adm_shp/rkpc.xlsx')
# chunk = df.get_chunk(2)
# print chunk
# for rk in zip(df['地区']):
#     print rk
# print df[:3]

# first_rows = df.head() #返回前n条数据,默认返回5条
# cols = df.columns #返回全部列名
# print first_rows
# print cols

pop = df['人口数']
# print pop

# df['省名'] = df['地区']
df.set_index('地区', inplace=True)
# pop = df['人口数']['山西']

statenames=[]
colors={}
cmap = plt.cm.YlOrRd
vmax = 100000000
vmin = 3000000
for shapedict in m.states_info:
    statename = shapedict['NL_NAME_1']
    # print statename
    p = statename.split('|')
    if len(p) > 1:
        s = p[1]
    else:
        s = p[0]
    s=s.decode('utf8')[0:2].encode('utf8')
    if s == '黑龍':
        s = '黑龙江'
    elif s=='内蒙':
        s = '内蒙古'

    #pop = df['人口数'][s]
    #print s,pop
    if(statenames.count(s)==0):
        statenames.append(s)
        pop = df['人口数'][s]
        colors[s] = cmap(np.sqrt((pop - vmin) / (vmax - vmin)))[:3]
        # print s,pop

#着色
ax = plt.gca()
for nshape, seg in enumerate(m.states):
    if(nshape<len(statenames)):
        # print nshape
        # print statenames[nshape]
        print (statenames[nshape],df['人口数'][statenames[nshape]],colors[statenames[nshape]])
        color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)

# for nshape, seg in enumerate(m.states):
#     poly = Polygon(seg, facecolor='r')
#     ax.add_patch(poly)

#显示图片
plt.show()

#将图片保存到指定目录
# plt.savefig("D:/python/pj4/img/bug_trend.png")