import os.path

import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
import xml.etree.ElementTree as ET
import json

from mysqlconnect import *

model=YOLO('model/yolov8s_fold_0.pt')
# model=YOLO('yolov8s.pt')
LABEL_PATH = 'data/labels'
IMAGE_PATH = 'data/images'
result_path = 'data/results'

def predict(image):
    # image = cv2.resize(image, (1920, 1200))


    results = model(image)
    # results[0].show()
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    return px

def save_areas_to_json(filename):
    tree = ET.parse(os.path.join(LABEL_PATH, filename))
    root = tree.getroot()
    parking_data = {}
    for space in root.findall('space'):

        space_id = space.get('id')


        contour = space.find('contour')
        points = []
        for point in contour.findall('point'):
            x = int(point.get('x'))
            y = int(point.get('y'))
            points.append((x, y))
        parking_data[space_id] = {
            "id": space_id,
            "contour": points
        }
    # with open('data/labels/2012-11-09_09_51_41.json', 'w') as json_file:
    #     json.dump(parking_data, json_file, indent=4)
    return parking_data

def get_areas(fila_path):

    with open(fila_path, 'r') as json_file:
        parking_data = json.load(json_file)
    rows = []
    for space_id, space_info in parking_data.items():
        contour_points = space_info['contour']

        row = {
            'space_id': space_id,
            'x1': contour_points[0][0],
            'y1': contour_points[0][1],
            'x2': contour_points[1][0],
            'y2': contour_points[1][1],
            'x3': contour_points[2][0],
            'y3': contour_points[2][1],
            'x4': contour_points[3][0],
            'y4': contour_points[3][1],

        }
        rows.append(row)

    parking_data = pd.DataFrame(rows)
    return parking_data

def check_ocupied(areas,predicts):
    areas["occupy"] = 0
    for x,row in predicts.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])

        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        for i in range(len(areas)):
            area_space = [
                (areas.loc[i]['x1'], areas.loc[i]['y1']),
                (areas.loc[i]['x2'], areas.loc[i]['y2']),
                (areas.loc[i]['x3'], areas.loc[i]['y3']),
                (areas.loc[i]['x4'], areas.loc[i]['y4'])
            ]
            result =cv2.pointPolygonTest(np.array(area_space,np.int32),((cx,cy)),False)
            if result >=0:
                areas.at[i, "occupy"] = 1
    return areas


def save_pred(areas,image,save_name):
    image1 = image.copy()
    # image1 = cv2.resize(image1, (1920, 1200))
    for i in range(len(areas)):
        area_space = [(areas.loc[i]["x1"],areas.loc[i]["y1"]),
                      (areas.loc[i]["x2"],areas.loc[i]["y2"]),
                      (areas.loc[i]["x3"],areas.loc[i]["y3"]),
                      (areas.loc[i]["x4"],areas.loc[i]["y4"])]
        if areas.loc[i]["occupy"]==0:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv2.polylines(image1, [np.array(area_space, np.int32)], True, color, 2)
        cv2.putText(image1, str(areas.loc[i]["space_id"]), (areas.loc[i]["x1"],areas.loc[i]["y1"]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,255),1)
    save_path = os.path.join(result_path, save_name)
    cv2.imwrite(save_path, image1)
    # cv2.imshow('predict', image1)


def updata_parking_info(areas_pd,parking_id):
    if isinstance(parking_id, list):
        parking_id_tuple = tuple(parking_id)
    else:
        parking_id_tuple = (parking_id,)
    delete_query = f"DELETE FROM parkinginfo WHERE plotId IN ({','.join(['%s'] * len(parking_id_tuple))})"
    # excute delete
    res = execute_one_query(delete_query,parking_id_tuple)
    print(f"{res} rows deleted from parkinginfo.")

    parking_pd =areas_pd[["space_id","occupy"]]
    parking_pd.loc[:,'parking_ids'] = parking_id
    insert_data =[tuple(row) for row in parking_pd.itertuples(index=False, name=None)]
    insert_query = """
                    INSERT INTO parkinginfo (parkingId, occupied, plotId)
                    VALUES (%s, %s, %s);
                """
    res = execute_many_query(insert_query, insert_data)
    print(f"{res} rows inserted into parkinginfo.")

    # parking_pd =areas_pd[["space_id","occupy"]]
    # parking_pd.loc[:,'parking_ids'] = parking_id
    # new_parking_pd_oder = ["occupy",'parking_ids','space_id']
    # parking_pd=parking_pd[new_parking_pd_oder]
    # update_query = """
    #     UPDATE parkinginfo
    #     SET  occupied = %s
    #     WHERE parkingId = %s and plotId =%s;
    #     """
    # update_data = [tuple(row) for row in parking_pd.itertuples(index=False, name=None)]
    # res = execute_many_query(update_query, update_data)
    # print(f"{res} rows updated into parkinginfo.")


if __name__ == '__main__':
    img ='2012-11-09_09_51_41.jpg'
    image =os.path.join(IMAGE_PATH, img)
    image = cv2.imread(image)
    start1 = time.time()

    px = predict(image)

    tree = '2012-11-09_09_51_41.json'
    fila_path = os.path.join(LABEL_PATH, tree)
    park_space = get_areas(tree)
    pred_park = check_ocupied(park_space,px)
    save_pred(pred_park,image)
    end1 = time.time()
    print(end1 - start1)
    # print("----------------")
    # tree = '2012-11-09_09_51_41.xml'
    # start2 = time.time()
    # save_areas_to_json(tree)
    # end2 = time.time()
    # print(end2 - start2)
