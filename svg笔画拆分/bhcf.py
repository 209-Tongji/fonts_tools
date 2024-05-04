import re
import math
import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import heapq

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def kruskal(points):
    n = len(points)
    parent = list(range(n))
    mst_edges = []

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(v1, v2):
        root1, root2 = find(v1), find(v2)
        parent[root1] = root2

    edges = [(distance(points[u], points[v]), u, v) for u in range(n) for v in range(u + 1, n)]
    edges.sort()

    for edge_weight, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v))

    return mst_edges

def points_to_svg_path(points):
    if len(points) < 2:
        raise ValueError("需要至少两个点来生成路径")

    path_data = f"M {points[0][0]} {points[0][1]} "  # 移动到第一个点的坐标

    for point in points[1:]:
        path_data += f"L {point[0]} {point[1]} "  # 用直线连接到下一个点的坐标

    return path_data

# 生成长椭圆上的随机点
def generate_ellipse_points(center, a, b, num_points):
    theta = np.linspace(0, 2*np.pi, num_points)
    x = center[0] + a * np.cos(theta)
    y = center[1] + b * np.sin(theta)
    points = np.column_stack((x, y))
    return points

def order_clockwise(a, b, c, d):
    # 计算每个点相对于一个中心点的极角
    def angle_from_center(p, center):
        return math.atan2(p[1] - center[1], p[0] - center[0])

    # 计算中心点，可以是四个点的平均值
    center = (
        (a[0] + b[0] + c[0] + d[0]) / 4,
        (a[1] + b[1] + c[1] + d[1]) / 4
    )

    # 计算每个点相对于中心点的极角
    angles = [
        (a, angle_from_center(a, center)),
        (b, angle_from_center(b, center)),
        (c, angle_from_center(c, center)),
        (d, angle_from_center(d, center))
    ]

    # 按照极角从小到大排序
    angles.sort(key=lambda x: x[1])

    # 返回排序后的顶点
    return [angle[0] for angle in angles]



def is_convex(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    cross_product = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)

    return cross_product > 0
def angle_between_vectors(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    cosine_theta = dot_product / (norm_a * norm_b)

    # 通过反余弦函数计算夹角（弧度）
    theta_rad = np.arccos(np.clip(cosine_theta, -1.0, 1.0))

    # 将弧度转换为角度
    theta_deg = np.degrees(theta_rad)

    return theta_deg
def convert_to_absolute_MLQ(svg_path_data):
    # 解析SVG路径数据
    path_commands = re.findall(r'([A-Za-z])([^A-Za-z]*)', svg_path_data)

    new_path_data = ""

    # 用于存储当前点的坐标
    current_point = (0, 0)

    for command, params in path_commands:
        params_list = [float(param) for param in re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', params)]
        if command.lower() == 'm':
            # 转换成绝对坐标的移动命令
            x, y = params_list[0], params_list[1]
            new_path_data += f"M {x} {y} "
            current_point = (x, y)
        elif command.lower() == 'l':
            # 转换成绝对坐标的直线命令
            x, y = params_list[0]+x, params_list[1]+y
            new_path_data += f"L {x} {y} "
            current_point = (x, y)
        elif command.lower() == 'q':
            # 转换成绝对坐标的二次贝塞尔曲线命令
            x1, y1 = x+params_list[0], y+params_list[1]
            x, y = x+params_list[2], y+params_list[3]
            new_path_data += f"Q {x1} {y1} {x} {y} "
            current_point = (x, y)
            pre_point=(x1,y1)
        elif command.lower() == 'h':
            # 转换成绝对坐标的水平线命令
            x = params_list[0]+x
            new_path_data += f"L {x} {current_point[1]} "
            current_point = (x, current_point[1])
        elif command.lower() == 'v':
            # 转换成绝对坐标的垂直线命令
            y = params_list[0]+y
            new_path_data += f"L {current_point[0]} {y} "
            current_point = (current_point[0], y)
        elif command.lower() == 't':
            # 转换成绝对坐标的二次贝塞尔曲线命令，t命令使用前一个控制点的镜像点作为新的控制点
            x1, y1 = 2 * current_point[0] - pre_point[0], 2 * current_point[1] - pre_point[1]
            x, y = params_list[0]+x, params_list[1]+y
            new_path_data += f"Q {x1} {y1} {x} {y} "
            current_point = (x, y)
            pre_point = (x1, y1)
        elif command.lower() == 'z':
            new_path_data += f"z"
    return new_path_data.strip()






# 示例路径数据
path_with_relative = "M 231.0 363.0 L 223.0 369.0 L 224.0 381.0 L 244.0 386.0 L 317.0 437.0 L 398.0 483.0 L 456.0 513.0 L 472.0 537.0 L 473.0 566.0 L 473.0 573.0 L 471.0 582.0 L 467.0 613.0 L 467.0 640.0 L 465.0 665.0 L 508.0 683.0 L 551.0 669.0 L 568.0 574.0 L 631.0 550.0 L 635.0 545.0 L 636.0 538.0 L 628.0 508.0 L 611.0 482.0 L 597.0 467.0 L 584.0 460.0 L 568.0 442.0 L 538.0 268.0 L 523.0 225.0 L 781.0 119.0 L 845.0 108.0 L 906.0 90.0 L 891.0 69.0 L 828.0 55.0 L 786.0 43.0 L 743.0 20.0 L 699.0 32.0 L 589.0 74.0 L 571.0 84.0 L 543.0 97.0 L 485.0 145.0 L 357.0 60.0 L 312.0 48.0 L 289.0 44.0 L 265.0 55.0 L 279.0 63.0 L 411.0 203.0 L 277.0 259.0 L 324.0 280.0 L 398.0 271.0 L 401.0 271.0 L 422.0 265.0 L 441.0 259.0 L 457.0 305.0 L 466.0 375.0 L 463.0 379.0 L 454.0 376.0 L 423.0 355.0 L 389.0 337.0 L 353.0 332.0 L 291.0 343.0 L 231.0 363.0z"
path_absolute_MLQ = convert_to_absolute_MLQ(path_with_relative)
print(path_absolute_MLQ)
path_absolute_MLQ=path_with_relative
path_commands = re.findall(r'([A-Za-z])([^A-Za-z]*)', path_absolute_MLQ)
paths=[]
p=[]
for i in path_commands:
    point=i[1].split()
    if i[0]=="Q":
        p.append([float(point[2]),float(point[3])])
    elif i[0]=="z"or i[0]=="Z":
        paths.append(p)
        p=[]
        continue
    else:
        p.append([float(point[0]),float(point[1])])
corners=[]

#确定凹点
for path in paths:
    corner=[]
    for i in range(len(path)-1):

        p1=path[i]
        p2=path[(i+1)%(len(path)-1)]
        p3=path[(i+2)%(len(path)-1)]
        p4=path[(i+3)%(len(path)-1)]
        if p1==[597.0,467.0 ]:
            aa=1
        v1=((p2[0]-p1[0]),(p2[1]-p1[1]))
        v2=((p3[0]-p2[0]),(p3[1]-p2[1]))
        v3=((p4[0]-p3[0]),(p4[1]-p3[1]))
        theta_deg = angle_between_vectors(v1, v2)
        beta_deg=angle_between_vectors(v1, v3)
        dis=(p3[0]-p2[0])**2+(p3[1]-p2[1])**2
        if is_convex(p1, p2, p3) and theta_deg>50:

            corner.append(p2)
        elif is_convex(p1, p2, p3) and is_convex(p2, p3, p4) and beta_deg>30 and dis<600:
            corner.append(p2)
    corners.append(corner)

edges=[]





#确定桥
for corner in corners:
    edge=[]
    if corner:
        corner_cop=corner[:]
        corner = np.array(corner)
        distances = np.linalg.norm(corner[:, np.newaxis, :] - corner, axis=-1)
        ssum=0
        for i in distances:
            # print(ssum)
            # print("_____________")
            ssum=ssum+1
            min_values = sorted(enumerate(i), key=lambda x: x[1])[:4]
            ss=0
            ee=[]
            res=[]
            for index, value in min_values:
                if value==0:
                    continue
                if value<250and value:
                    if ss==3:
                        break
                    ee.append(index)
                    res.append(index)
                    ss=ss+1
            if ss>=3:
                ordered_vertices = order_clockwise([corner[ee[0]][0],corner[ee[0]][1]],[corner[ee[1]][0],corner[ee[1]][1]], [corner[ee[2]][0],corner[ee[2]][1]], [corner[ssum-1][0],corner[ssum-1][1]])
                res=[]
                ind0= ordered_vertices.index([corner[ssum-1][0],corner[ssum-1][1]])
                ind1 =corner_cop.index(ordered_vertices[(ind0-1)%4])
                ind2 =corner_cop.index(ordered_vertices[(ind0+1)%4])
                res.append(ind1)
                res.append(ind2)
            edge.append(res)
    edges.append(edge)

#分割笔画
strokes=[]
for i,path in enumerate(paths):
    corner=corners[i]
    edge=edges[i]
    flag=path[:]
    for i in range(len(flag)):
        flag[i]=0
    while sum(flag)!=(len(flag)):
        for j in range(len(path)):
            if flag[j]==0 and path[j] not in corner:
                stroke = []
                break
        start=path[j]
        j_for=[]
        p=0
        while True:#每一笔画的筛选
            if path[j]==start and p!=0:
                stroke.append(path[j])
                flag[j] = 1
                strokes.append(stroke)
                break
            p=p+1
            stroke.append(path[j])
            if path[j]==[249.0,115.0]:
                aaa=1
            flag[j] = 1
            if path[j] in corner:
                judge={}
                jj = (j + 1) % (len(path)-1)
                judge[999]=angle_between_vectors((path[jj][0]-path[j][0],path[jj][1]-path[j][1]),(path[j][0]-j_for[0],path[j][1]-j_for[1]))
                if flag[jj]==1 and judge[999]>10:
                    judge[999]=179
                for kk in edge[corner.index(path[j])]:
                    judge[kk]=angle_between_vectors((corner[kk][0]-path[j][0],corner[kk][1]-path[j][1]),(path[j][0]-j_for[0],path[j][1]-j_for[1]))
                sorted_dict = dict(sorted(judge.items(), key=lambda item: item[1]))
                # 获取排序后字典的第一个值
                kk= next(iter(sorted_dict.keys()))
                j_for = path[j]
                if kk==999:
                    j=jj
                else:
                    nextt=corner[kk]
                    j=path.index(nextt)

            else:
                j_for = path[j]
                j=(j+1) %len(path)

voronois=[]
for num,i in enumerate(strokes):
    voronoi = []
    vor = Voronoi(i)
    stroke=strokes[num]
    voronoi_points = vor.vertices
    curve_points = stroke
    # 离散点集，这里使用一些离散点作为示例
    points_to_check =voronoi_points.tolist()
    # 创建闭合曲线的多边形
    curve_polygon = Polygon(curve_points)

    # 绘制闭合曲线
    x_curve, y_curve = zip(*curve_points + [curve_points[0]])  # 添加闭合点

    # 检查离散点是否在闭合曲线内部
    for point in points_to_check:
        point_geometry = Point(point)
        if point_geometry.within(curve_polygon):
            voronoi.append(point)
    voronois.append(voronoi)



#最小生成树
structs=[]
for i in voronois:
    struct=[]
    mst_kruskal = kruskal(i)
    flag = [0 for _ in i]
    for j in mst_kruskal:
        flag[j[0]]=flag[j[0]]+1
        flag[j[1]] = flag[j[1]] + 1
    for j in flag:
        if j==1:
            break


# 转换点集为 SVG 格式的路径
for i in strokes:
    svg_path = points_to_svg_path(i)

    # 生成完整的 SVG 文档
    svg_document = f'<path d="{svg_path}" stroke="black" fill="transparent"/>'

    # 打印 SVG 文档
    print(svg_document)




