import argparse
import logging
import time
import os
import cv2
import numpy as np
import subprocess

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import matplotlib.pyplot as plt
from motion_analysis import MotionAnalysis

logger = logging.getLogger('TfPoseEstimator-Video')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[#(asctime)s] [#(name)s] [#(levelname)s] #(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('--path', type=str, default="")
    parser.add_argument('--write', type=str, default=None)
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')
    parser.add_argument('--model', type=str, default='cmu', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('--showBG', type=bool, default=True, help='False to show skeleton only.')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')
    parser.add_argument('--start_frame', type=int, default=0)
    parser.add_argument('--cog', type=bool, default=False)
    parser.add_argument('--cog_color', type=str, default='black')
    args = parser.parse_args()

    logger.debug('initialization #s : #s')  # (args.model, get_graph_path(args.model)))

    # data directory
    if args.path:
        path_movie_src = os.path.join(args.path, 'movie', args.video)
    else:
        path_movie_src = args.video
    path_movie_out = os.path.join(args.path, 'movie_estimated')
    path_csv_estimated = os.path.join(args.path, 'data_estimated')
    path_png_estimated = os.path.join(args.path, 'png_estimated')
    os.makedirs(path_movie_out, exist_ok=True)
    os.makedirs(path_png_estimated, exist_ok=True)
    os.makedirs(path_csv_estimated, exist_ok=True)

    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    cap = cv2.VideoCapture(path_movie_src)
    if args.cog:
        ma = MotionAnalysis()

    if cap.isOpened() is False:
        print("Error opening video stream or file")
    frame_no = 0
    # f = open(os.path.join(path_csv_estimated,"test.txt"), 'w')
    while cap.isOpened():
        ret_val, image = cap.read()
        if not ret_val:
            break
        if frame_no == 0:
            h_pxl, w_pxl = image.shape[0], image.shape[1]
        plt.figure(figsize=(int(w_pxl/20), int(h_pxl/20)))

        if frame_no > args.start_frame:
            # humans = e.inference(image)
            humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
            print(humans)
            print(frame_no)
            # f.writelines(humans)
            if not args.showBG:
                image = np.zeros(image.shape)
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if args.cog:
                bodies_cog = ma.multi_bodies_cog(humans=humans)
                bodies_cog[np.isnan(bodies_cog[:, :, :])] = 0
                logger.debug(str(bodies_cog))
                plt.scatter(bodies_cog[:, 14, 0] * w_pxl, bodies_cog[:, 14, 1] * h_pxl, color=args.cog_color,
                            marker='o', s=150)
                plt.vlines(bodies_cog[:, 6, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')
                plt.vlines(bodies_cog[:, 7, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')
            bgimg = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)
            bgimg = cv2.resize(bgimg, (e.heatMat.shape[1], e.heatMat.shape[0]), interpolation=cv2.INTER_AREA)
            plt.savefig(os.path.join(path_png_estimated,
                                     args.video.split('.')[-2] + '{:06d}'.format(frame_no) + ".png"))
            # plt.savefig("../short/"+args.video.split('.')[-2] + '{%06d}'.format(frame_no) + ".png")
        frame_no += 1
        # cv2.putText(image, "FPS: #f" # (1.0 / (time.time() - fps_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # cv2.imshow('tf-pose-estimation result', image)
        # fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
    # f.close()
    cv2.destroyAllWindows()
    logger.info("finish estimation & start encoding")
    cmd = ["ffmpeg", "-r", "30",
           "-i", os.path.join(path_png_estimated,args.video.split('.')[-2] + "%06d.png"),
           "-vcodec", "libx264", "-pix_fmt", "yuv420p",
           os.path.join(path_movie_out, args.video.split('.')[-2] + "out.mp4")]
    subprocess.call(cmd)
logger.debug('finished+')
