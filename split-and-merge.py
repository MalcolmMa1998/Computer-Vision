import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


def set_coordinates(codes):
    print('Code length: ', len(codes))
    x = 0
    y = 0
    coordinate_list = [(x, y)]
    for i in codes:
        # 输出此多边形的坐标
        if i == 0:
            x = x + 1
            coordinate_list.append((x, y))
            # print((x, y))
        if i == 1:
            x = x + 1
            y = y + 1
            coordinate_list.append((x, y))
            # print((x, y))
        if i == 2:
            y = y + 1
            coordinate_list.append((x, y))
            # print((x, y))
        if i == 3:
            x = x - 1
            y = y + 1
            coordinate_list.append((x, y))
            # print((x, y))
        if i == 4:
            x = x - 1
            coordinate_list.append((x, y))
            # print((x, y))
        if i == 5:
            x = x - 1
            y = y - 1
            coordinate_list.append((x, y))
            # print((x, y))
        if i == 6:
            y = y - 1
            coordinate_list.append((x, y))
            # print((x, y))
        if i == 7:
            x = x + 1
            y = y - 1
            coordinate_list.append((x, y))
            # print((x, y))

    print("Coordinate list length: ", len(coordinate_list))
    return coordinate_list


def random_select(codes):
    # 随机选出27个初始点
    point_list = set_coordinates(codes)
    select_point = np.random.randint(0, 1, len(point_list))
    for i in range(0, len(point_list), 3):
        select_point[i] = 1
    print(Counter(select_point))
    for i in range(3, 46, 6):
        select_point[i] = 0
    print(Counter(select_point))
    print(select_point)
    return select_point


def cal_distance(x1, y1, x2, y2, x0, y0):
    # 点到直线距离
    distance = ((y2 - y1) * x0 + (x1 - x2) * y0 + (x2 * y1 - x1 * y2)) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    if distance < 0:
        distance = -distance
    return distance


def show_img(img_list):
    for (x, y) in img_list:
        plt.plot(x, y, '*', color='black')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('./homework_1.png')
    plt.show()


def main():
    code = [0, 0, 0, 0, 7,
            0, 0, 7, 7, 7,
            7, 7, 7, 6, 6,
            7, 6, 6, 6, 6,
            6, 6, 6, 6, 5,
            7, 6, 7, 6, 6,
            5, 6, 4, 5, 4,
            4, 3, 4, 3, 6,
            6, 6, 6, 5, 6,
            5, 5, 4, 5, 4,
            4, 4, 4, 3, 4,
            3, 3, 2, 3, 2,
            2, 2, 2, 5, 4,
            5, 4, 4, 3, 4,
            2, 3, 2, 2, 1,
            2, 1, 3, 2, 2,
            2, 2, 2, 2, 2,
            2, 1, 2, 2, 1,
            1, 1, 1, 1, 1,
            0, 0, 1, 0, 0,
            0, 0]
    point_list = set_coordinates(code)
    is_choose = random_select(code)
    is_choose = is_choose.tolist()
    max_distance = 0
    min_distance = 1000
    max_num = 0
    min_num = 0

    # 第一轮的总误差
    total_error = 35.19067448629661

    # 新的总误差
    new_error = 0

    # split and merge
    while new_error != 35.19067448629661:
        for i in range(0, len(is_choose) - 4):
            if is_choose[i] == 1:
                index = is_choose.index(1, i + 1, len(is_choose))
                (x1, y1) = point_list[i]
                (x2, y2) = point_list[index]
            if is_choose[i] == 0:
                (x0, y0) = point_list[i]
                now_distance = cal_distance(x1, y1, x2, y2, x0, y0)
                # totalError = totalError + nowDistance
                new_error = new_error + now_distance
                if new_error < 35.19067448629661:
                    total_error = new_error
                if now_distance > max_distance:
                    max_distance = now_distance
                    max_num = i
                if now_distance < min_distance:
                    if now_distance != 0:
                        min_distance = now_distance
                        min_num = i
        print('Minimium distance: ', min_distance)
        print('Maximium distance: ', max_distance)
        print('Minimium number: ', min_num)
        print('Maximium number: ', max_num)

        is_choose[min_num] = 0
        is_choose[max_num] = 1

    end_list = []
    print(total_error)
    for i in range(0, len(is_choose) - 1):
        if is_choose[i] == 1:
            (x, y) = point_list[i]
            end_list.append((x, y))
    end_list.append((0, 0))

    show_img(end_list)


if __name__ == '__main__':
    main()
