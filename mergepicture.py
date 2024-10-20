import cv2
import os

# 设置图片所在的路径
image_folder = 'D:\Data\LingLing\workdata\compitition\PKLot\PKLot\PUCPR\Sunny'  # 替换为你的图片路径
video_name = 'output_video.avi'  # 输出视频的名称

# 读取文件夹中的图片文件
images = []
for root, dirs, files in os.walk(image_folder):
    for file in files:
        if file.endswith(".jpg"):
            images.append(os.path.join(root, file))  # 加入图片的完整路径
    print(f'solve file{files}')
images.sort()  # 确保图片按顺序排列

# 获取第一张图片的尺寸作为视频的尺寸
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

# 设置视频的帧速率 (fps)
fps = 30

# 初始化视频写入对象
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))

# 逐帧将图片写入视频
for image in images:
    img_path = os.path.join(image_folder, image)
    video.write(cv2.imread(img_path))

# 释放视频对象
video.release()

print(f"视频已生成并保存为 {video_name}")
