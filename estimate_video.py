import argparse
import gc
import logging
import os
import subprocess

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
# from tf_pose.common import CocoPart

from modules.humans_to_array import humans_to_array
from modules.motion_analysis import MotionAnalysis

fps_time = 0


# if __name__ == '__main__':
def estimate_video(video, path='', resize='432x368', model='cmu',resize_out_ratio=4.0,
                   cog=True, cog_color='black', showBG=True, start_frame=0, debug=False, plot_image=True):
    logger = logging.getLogger('TfPoseEstimator-Video')
    logger.setLevel(logging.DEBUG) if debug else logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG) if debug else ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[#(asctime)s] [#(name)s] [#(levelname)s] #(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # data directory
    if path:
        path_movie_src = os.path.join(path, 'movie', video)
    else:
        path_movie_src = video
    path_movie_out = os.path.join(path, 'movie_estimated')
    path_csv_estimated = os.path.join(path, 'data_estimated')
    path_png_estimated = os.path.join(path, 'png_estimated')
    csv_file = os.path.join(path_csv_estimated, video.rsplit('.')[0] + '.csv')
    os.makedirs(path_movie_out, exist_ok=True)
    os.makedirs(path_png_estimated, exist_ok=True)
    os.makedirs(path_csv_estimated, exist_ok=True)

    w, h = model_wh(resize)
    e = TfPoseEstimator(get_graph_path(model), target_size=(w, h))
    cap = cv2.VideoCapture(path_movie_src)
    if cog:
        ma = MotionAnalysis()

    # CSV FILE SETTING
    segments = ["Nose","Neck","RShoulder","RElbow","RWrist","LShoulder","LElbow","LWrist",
                "RHip","RKnee","RAnkle","LHip","LKnee","LAnkle","REye","LEye","REar","LEar",
                "head_cog", "torso_cog","r_thigh_cog", "l_thigh_cog","r_leg_cog", "l_leg_cog","r_foot_cog", "l_foot_cog",
                "r_arm_cog", "l_arm_cog","r_forearm_cog", "l_forearm_cog", "r_hand_cog", "l_hand_cog"]
    seg_columns = ['frame']
    [seg_columns.extend([x + '_x', x + '_y', x + '_score']) for x in segments]
    df_template = pd.DataFrame(columns=seg_columns)
    df_template.to_csv(csv_file, index=False)

    if cap.isOpened() is False:
        logger.info("ERROR: opening video stream or file")
    frame_no = 0
    # f = open(os.path.join(path_csv_estimated,"test.txt"), 'w')
    while cap.isOpened():
        ret_val, image = cap.read()
        if not ret_val:
            break
        if frame_no == 0:
            h_pxl, w_pxl = image.shape[0], image.shape[1]
        if frame_no < start_frame:
            frame_no += 1
            continue
            # humans = e.inference(image)
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
        logger.debug(str(frame_no))
        a_humans = humans_to_array(humans)
        logger.debug(str(a_humans))

        if cog:
            bodies_cog = ma.multi_bodies_cog(humans=humans)
            bodies_cog[np.isnan(bodies_cog[:, :, :])] = 0
            humans_feature = np.concatenate((np.c_[np.repeat(frame_no, len(a_humans))],
                                             a_humans.reshape(a_humans.shape[0], a_humans.shape[1] * a_humans.shape[2]),
                                             bodies_cog.reshape(bodies_cog.shape[0], bodies_cog.shape[1] * bodies_cog.shape[2])),axis=1)
            df_frame = pd.DataFrame(humans_feature.round(4))
            df_frame.to_csv(csv_file, index=False, header=None, mode='a')

        if plot_image:
            plt.figure(figsize=(int(w_pxl / 200), int(h_pxl / 200)))
            if not showBG:
                image = np.zeros(image.shape)
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            # logger.debug(str(bodies_cog))
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.scatter(bodies_cog[:, 14, 0] * w_pxl, bodies_cog[:, 14, 1] * h_pxl, color=cog_color,
                        marker='o', s=150)
            plt.vlines(bodies_cog[:, 6, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')
            plt.vlines(bodies_cog[:, 7, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')
            # print(humans_feature)

            bgimg = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)
            bgimg = cv2.resize(bgimg, (e.heatMat.shape[1], e.heatMat.shape[0]), interpolation=cv2.INTER_AREA)
            plt.savefig(os.path.join(path_png_estimated,
                                     video.split('.')[-2] + '{:06d}'.format(frame_no) + ".png"))
            plt.clf()
        frame_no += 1
        gc.collect()
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    logger.info("finish estimation & start encoding")
    cmd = ["ffmpeg", "-r", "30",
           "-i", os.path.join(path_png_estimated,video.split('.')[-2] + "%06d.png"),
           "-vcodec", "libx264", "-pix_fmt", "yuv420p",
           os.path.join(path_movie_out, video.split('.')[-2] + ".mp4")]
    subprocess.call(cmd)
    logger.debug('finished+')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('--path', type=str, default="")
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--resize', type=str, default='432x368', help='network input resize. default=432x368')
    parser.add_argument('--model', type=str, default='cmu', help='cmu / mobilenet_thin')
    parser.add_argument('--showBG', type=bool, default=True, help='False to show skeleton only.')
    parser.add_argument('--start_frame', type=int, default=0)
    parser.add_argument('--cog', type=bool, default=True)
    parser.add_argument('--cog_color', type=str, default='black')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')
    parser.add_argument('--debug', type=bool, default=False)
    parser.add_argument('--plot_image', type=bool, default=True)
    args = parser.parse_args()
    estimate_video(video=args.video, path=args.path, resize=args.resize, model=args.model,
                   resize_out_ratio=args.resize_out_ratio, showBG=args.showBG, plot_image=args.plot_image,
                   cog=args.cog, cog_color=args.cog_color, start_frame=args.start_frame, debug=args.debug)

