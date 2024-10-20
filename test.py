import os

import sched
import time

from sipbuild.generator.outputs import output_api

from parkingDetect import *
from pathlib import Path

LABEL_PATH = 'data/labels'
IMAGE_PATH = 'data/images'


def read_image(image_path):
    image_path = Path(image_path)
    images = []
    for file_path in image_path.glob('*.jpg'):
        file_name = file_path.name
        images.append(file_name)
    return images


def parking_detect(image_path, label_path):
    image = os.path.join(IMAGE_PATH, image_path)
    image = cv2.imread(image)
    px = predict(image)

    tree = os.path.join(LABEL_PATH, label_path)
    park_space = get_areas(tree)
    pred_park = check_ocupied(park_space, px)
    save_pred(pred_park, image, image_path)
    updata_parking_info(pred_park, 1)


def parking_detect_multi(image_paths, label_path):
    image_path = read_image(image_paths)
    for path in image_path:
        parking_detect(path, label_path)


def get_parking_detail(plotId=1):
    if isinstance(plotId, list):
        plot_id_tuple = tuple(plotId)
    else:
        plot_id_tuple = (plotId,)
    plot_name_querry = f"SELECT name FROM parkinglot WHERE id= %s;"
    select_all_querry = f"SELECT * FROM parkinginfo WHERE plotId = %s;"
    plot_name = execute_search_query(plot_name_querry, plot_id_tuple)[0][0]
    print(plot_name)
    all_info = execute_search_query(select_all_querry, plot_id_tuple)
    parking_details = []
    occupy_count = 0
    total = len(all_info)
    for info in all_info:
        parking_details.append({"parkingId": info[1], "plotId": info[2], "occupy": info[3]})
        occupy_count += info[3]
    result = {
        "plotid": plotId,
        "plotname": plot_name,
        "totalplot": total,
        "occupiedplot": occupy_count,
        "emptyplot": total - occupy_count,
        "parkingdetails": parking_details,
        "updatatime": str(info[4]),
    }

    return result


def parking_detect_video(video_path, label_path):
    cap = cv2.VideoCapture(video_path)
    tree = os.path.join(LABEL_PATH, label_path)
    park_space = get_areas(tree)

    if not cap.isOpened():
        print(f"can not open video: {video_path}")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue


        if frame_count % 2 == 0:
            px = predict(frame)
            pred_park = check_ocupied(park_space, px)
            updata_parking_info(pred_park, 1)
            show_pred(pred_park, frame, px)

        frame_count += 1

        if cv2.waitKey(2) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def show_pred(areas, image, save_name):
    save_path = "static/image/output.jpg"
    image1 = image.copy()
    # image1 = cv2.resize(image1, (1920, 1200))
    for i in range(len(areas)):
        area_space = [(areas.loc[i]["x1"], areas.loc[i]["y1"]),
                      (areas.loc[i]["x2"], areas.loc[i]["y2"]),
                      (areas.loc[i]["x3"], areas.loc[i]["y3"]),
                      (areas.loc[i]["x4"], areas.loc[i]["y4"])]
        if areas.loc[i]["occupy"] == 0:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv2.polylines(image1, [np.array(area_space, np.int32)], True, color, 2)
        cv2.putText(image1, str(areas.loc[i]["space_id"]), (areas.loc[i]["x1"], areas.loc[i]["y1"]),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
    # save_path = os.path.join(result_path, save_name)

    cv2.imwrite(save_path, image1)
    # cv2.imshow('predict', image1)

def get_parking_count_history(plotId=1):
    if isinstance(plotId, list):
        plot_id_tuple = tuple(plotId)
    else:
        plot_id_tuple = (plotId,)
    select_all_querry = f"SELECT * FROM parking_occupancy WHERE plotId = %s;"
    all_info = execute_search_query(select_all_querry, plot_id_tuple)
    total = len(all_info)
    count_history = []
    for info in all_info:
        count_history.append({'id':info[0],'availablenum':info[2],"createtime":info[3]})
    result = {
        "plotid": plotId,
        "total": total,
        "data": count_history
    }
    return result


if __name__ == '__main__':
    tree_path = '2012-11-09_09_51_41.json'
    parking_detect_video("data/video/output_video.mp4",tree_path)