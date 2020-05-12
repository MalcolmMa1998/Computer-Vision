import cv2 as cv
import os


def load_data(path):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    os.chdir(os.path.join("CIFAR-10  subset", path))


def load_hsv(data):
    load_data(data)
    hsv_list = []
    pic_num = []
    for image_name in os.listdir(os.getcwd()):
        picNum = image_name.split('(')[1]
        picNum = picNum.split(')')[0]
        img = cv.imread(image_name)
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    return hsv_list


def main():
    database_deatures = [[0] * 72 for _ in range(180)]
    feature = [0] * 72
    feature_query = [0] * 72
    h1 = 0
    s1 = 0
    v1 = 0
    pic_num = 0
    load_data('database')
    for image_name in os.listdir(os.getcwd()):
        pic_num = image_name.split('(')[1]
        pic_num = pic_num.split(')')[0]
        img = cv.imread(image_name)
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        height_database = img_hsv.shape[0]
        weight_database = img_hsv.shape[1]
        channels = img_hsv.shape[2]
        for row in range(height_database):
            for col in range(weight_database):
                h = img_hsv[row, col][0]
                s = img_hsv[row, col][1]
                v = img_hsv[row, col][2]
                if 316 <= h <= 360 or 0 <= h <= 20:
                    h1 = 0
                if 21 <= h <= 40:
                    h1 = 1
                if 41 <= h <= 75:
                    h1 = 2
                if 76 <= h <= 155:
                    h1 = 3
                if 156 <= h <= 190:
                    h1 = 4
                if 191 <= h <= 270:
                    h1 = 5
                if 271 <= h <= 295:
                    h1 = 6
                if 296 <= h <= 315:
                    h1 = 7
                if 0 <= s < 0.2:
                    s1 = 0
                if 0.2 <= s < 0.7:
                    s1 = 1
                if 0.7 <= s <= 1:
                    s1 = 2
                if 0 <= v < 0.2:
                    v1 = 0
                if 0.2 <= v < 0.7:
                    v1 = 1
                if 0.7 <= v <= 1:
                    v1 = 2
                hist = h1 * 9 + s1 * 3 + v1
                feature[hist] = feature[hist] + 1

        database_deatures[int(pic_num) - 1] = feature
        feature = [0] * 72

    # 初始化query操作变量
    d = 0
    right_num1 = 0
    right_num2 = 0
    AP1 = 0
    AP2 = 0
    distance = []

    # 读取每一张待对比图片，计算出其颜色直方图特征并与database_deatures中的每一张图片的特征进行对比
    load_data('query')
    for queryImage_name in os.listdir(os.getcwd()):
        print('Query图片名称：' + queryImage_name + '\nTop 20相似图片索引：')
        m = 0
        n = 0
        pic_num = queryImage_name.split('(')[1]
        pic_num = pic_num.split(')')[0]
        if 11 <= int(pic_num) <= 20:
            label_q = 1
        else:
            label_q = 0

        img = cv.imread(queryImage_name)
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        height_query = img_hsv.shape[0]
        weight_query = img_hsv.shape[1]
        channels_query = img_hsv.shape[2]
        for row in range(height_query):
            for col in range(weight_query):
                h = img_hsv[row, col][0]
                s = img_hsv[row, col][1]
                v = img_hsv[row, col][2]
                if 316 <= h <= 360 or 0 <= h <= 20:
                    h1 = 0
                if 21 <= h <= 40:
                    h1 = 1
                if 41 <= h <= 75:
                    h1 = 2
                if 76 <= h <= 155:
                    h1 = 3
                if 156 <= h <= 190:
                    h1 = 4
                if 191 <= h <= 270:
                    h1 = 5
                if 271 <= h <= 295:
                    h1 = 6
                if 296 <= h <= 315:
                    h1 = 7
                if 0 <= s < 0.2:
                    s1 = 0
                if 0.2 <= s < 0.7:
                    s1 = 1
                if 0.7 <= s <= 1:
                    s1 = 2
                if 0 <= v < 0.2:
                    v1 = 0
                if 0.2 <= v < 0.7:
                    v1 = 1
                if 0.7 <= v <= 1:
                    v1 = 2
                hist = h1 * 9 + s1 * 3 + v1
                feature_query[hist] = feature_query[hist] + 1

        # 计算相似度，使用chi-square distance
        for m in range(180):
            for n in range(72):
                if (feature_query[n] + database_deatures[m][n]) != 0:
                    d = ((feature_query[n] - database_deatures[m][n]) ** 2 / (
                                feature_query[n] + database_deatures[m][n])) + d
            distance.append(d)
            d = 0
        new_distance = [None] * len(distance)

        # 对相似度高低进行排列并输入最相似前二十张图片的索引
        for i in range(len(distance)):
            new_distance[i] = distance[i]
        distance.sort()
        for i in range(20):
            print('database(' + str(new_distance.index(distance[i]) + 1) + ').png')
            if 1 <= (new_distance.index(distance[i]) + 1) <= 90:
                label_d = 0
            else:
                label_d = 1
            if label_d == label_q and label_q == 0:
                # 计算准确率mAP
                right_num1 = right_num1 + 1
                AP1 = AP1 + (1 * (right_num1 / (i + 1))) / 20
            if label_d == label_q and label_q == 1:
                right_num2 = right_num2 + 1
                AP2 = AP2 + (1 * (right_num2 / (i + 1))) / 20
        feature_query = [0] * 72
        distance = []
        print('-----------------------------------\n')
    mAP = AP1 + AP2
    mAP = mAP / 2
    print('mAP: ' + str(mAP))


if __name__ == '__main__':
    main()
