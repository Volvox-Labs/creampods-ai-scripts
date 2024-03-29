import os
import cv2

BASE_DIR = os. getcwd() 

def images_to_video(image_folder, output_video, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    video.release()

# save_video(file_prefix, BASE_DIR + "\\all_frames")
images_to_video(BASE_DIR + "\\all_frames", "000", 8)
