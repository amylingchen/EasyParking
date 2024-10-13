import os

import sched
import time
from parkingDetect import *
from pathlib import Path

LABEL_PATH = 'data/labels'
IMAGE_PATH = 'data/images'


def read_image(image_path):
    image_path = Path(image_path)
    images=[]
    for file_path in image_path.glob('*.jpg'):
        file_name = file_path.name
        images.append(file_name)
    return images


def parking_detect(image_path,label_path):
    image = os.path.join(IMAGE_PATH, image_path)
    image = cv2.imread(image)
    px = predict(image)

    tree = os.path.join(LABEL_PATH, label_path)
    park_space = get_areas(tree)
    pred_park = check_ocupied(park_space, px)
    save_pred(pred_park, image,image_path)
    updata_parking_info(pred_park, 1)

def parking_detect_multi(image_paths,label_path):
    image_path = read_image(image_paths)
    for path in image_path:
        parking_detect(path,label_path)


def get_parking_detail(plotId=1):
    if isinstance(plotId, list):
        plot_id_tuple = tuple(plotId)
    else:
        plot_id_tuple = (plotId,)
    plot_name_querry =f"SELECT name FROM parkinglot WHERE id= %s;"
    select_all_querry = f"SELECT * FROM parkinginfo WHERE plotId = %s;"
    plot_name = execute_search_query(plot_name_querry,plot_id_tuple)[0][0]
    print(plot_name)
    all_info = execute_search_query(select_all_querry,plot_id_tuple)
    parking_details =[]
    occupy_count =0
    total =len(all_info)
    for info in all_info:
        parking_details.append({"parkingId":info[1],"plotId":info[2],"occupy":info[3]})
        occupy_count += info[3]
    result={
        "plotid":plotId,
        "plotname":plot_name,
        "totalplot":total,
        "occupiedplot":occupy_count,
        "emptyplot":total-occupy_count,
        "parkingdetails":parking_details,
        "updatatime":str(info[4]),
    }
    print(result)
    return result


if __name__ == '__main__':
    tree_path = '2012-11-09_09_51_41.json'
    while True:

        parking_detect_multi(IMAGE_PATH, tree_path)
        time.sleep(60)
    # get_parking_detail()

