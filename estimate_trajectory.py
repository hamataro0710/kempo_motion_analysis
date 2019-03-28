import argparse
import gc
import logging
import os
import subprocess
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
# from tf_pose.common import CocoPart
from modules.humans_to_array import humans_to_array
from modules.motion_analysis import MotionAnalysis
# from modules.track_humans import track_humans
from modules.track_humans import TrackHumans
fps_time = 0


# if __name__ == '__main__':
def estimate_trajectory(video, path='', resize='432x368', model='cmu', resize_out_ratio=4.0, orientation='horizontal',
                   cog="skip", cog_color='black', cog_size='M', showBG=True, start_frame=0, debug=False, plot_image=""):
    logger = logging.getLogger('TfPoseEstimator')
    logger.setLevel(logging.DEBUG) if debug else logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG) if debug else ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    # formatter = logging.Formatter('[#(asctime)s] [#(name)s] [#(levelname)s] #(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # data directory
    if path:
        path_movie_src = os.path.join(path, 'movies', video)
    else:
        path_movie_src = video
    path_movie_out = os.path.join(path, 'movies_estimated')
    path_csv_estimated = os.path.join(path, 'data_estimated')
    path_png_estimated = os.path.join(path, 'png_estimated')
    csv_file = os.path.join(path_csv_estimated, video.rsplit('.')[0] + '.csv')
    os.makedirs(path_movie_out, exist_ok=True)
    os.makedirs(path_png_estimated, exist_ok=True)
    os.makedirs(path_csv_estimated, exist_ok=True)

    w, h = model_wh(resize)
    if orientation == 'horizontal':
        if w == 0: w = 432
        if h == 0: h = 368
    else:
        if w == 0: w = 368
        if h == 0: h = 432
    e = TfPoseEstimator(get_graph_path(model), target_size=(w, h))
    logger.info('resize: %d,  %d' % (w, h))

    cap = cv2.VideoCapture(path_movie_src)
    logger.info("OPEN: %s" % path_movie_src)
    if cap.isOpened() is False:
        logger.info("ERROR: opening video stream or file")
    caps_fps = cap.get(cv2.CAP_PROP_FPS)

    logger.info('MODE: Plot Center of Gravity')
    ma = MotionAnalysis()
    # CSV FILE SETTING
    segments = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist",
                "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "human_id",
                "head_cog", "torso_cog", "r_thigh_cog", "l_thigh_cog", "r_leg_cog", "l_leg_cog", "r_foot_cog",
                "l_foot_cog",
                "r_arm_cog", "l_arm_cog", "r_forearm_cog", "l_forearm_cog", "r_hand_cog", "l_hand_cog"]
    seg_columns = ['frame']
    [seg_columns.extend([x + '_x', x + '_y', x + '_score']) for x in segments]
    df_template = pd.DataFrame(columns=seg_columns)
    df_template.to_csv(csv_file, index=False)

    # change marker size of cog
    if (cog_size == "s") or (cog_size == "S"):
        cog_size = 10000
    else:
        cog_size = 20000

    # processing video
    frame_no = 0
    # cmap = plt.get_cmap("tab10")
    track = TrackHumans(start_frame=start_frame)
    while cap.isOpened():
        ret_val, image = cap.read()
        if not ret_val:
            break
        if frame_no == 0:
            h_pxl, w_pxl = image.shape[0], image.shape[1]
        if frame_no < start_frame:
            frame_no += 1
            continue

        # estimate pose
        t = time.time()
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
        time_estimation = time.time() - t
        array_humans = humans_to_array(humans)

        # check the time to estimation
        if (frame_no % int(caps_fps)) == 0:
            logger.info("Now estimating at:" + str(int(frame_no / caps_fps)) + "[sec]")
            logger.info('inference in %.4f seconds.' % time_estimation)
            logger.debug('shape of image: ' + str(image.shape))
            logger.debug(str(array_humans))

        # track human
        # if frame_no == start_frame:
        #     # initialize
        #     humans_id = np.array(range(len(array_humans)))
        #     np_humans_current = np_humans = np.concatenate((np.c_[np.repeat(frame_no, len(array_humans))],
        #                                 array_humans.reshape(array_humans.shape[0], array_humans.shape[1] * array_humans.shape[2]),
        #                                 np.c_[humans_id]), axis=1)
        #     clm_of_id = np_humans.shape[1] - 1
        # else:
        #     humans_id = track_humans(array_humans, post_humans, humans_id)
        #     np_humans_current = np.concatenate((np.c_[np.repeat(frame_no, len(array_humans))],
        #                                      array_humans.reshape(array_humans.shape[0], array_humans.shape[1] * array_humans.shape[2]),
        #                                      np.c_[humans_id]), axis=1)
        #     np_humans = np.concatenate((np_humans[np_humans[:, 0] > (frame_no - 30)], np_humans_current))
        # post_humans = array_humans
        track.track_humans(frame_no, array_humans)

        # calculate center of gravity
        if cog != 'skip':
            t = time.time()
            bodies_cog = ma.multi_bodies_cog(humans=humans)
            bodies_cog[np.isnan(bodies_cog[:, :, :])] = 0
            humans_feature = np.concatenate((track.humans_current,
                                             bodies_cog.reshape(bodies_cog.shape[0],
                                                                bodies_cog.shape[1] * bodies_cog.shape[2])), axis=1)
            df_frame = pd.DataFrame(humans_feature.round(4))
            df_frame.to_csv(csv_file, index=False, header=None, mode='a')
            time_cog = time.time() - t
            if frame_no % int(caps_fps) == 0:
                logger.info('calculation of cog in %.4f seconds.' % time_cog)

        if plot_image != 'skip':
            fig_resize = 100
            plt.figure(figsize=(int(w_pxl / fig_resize), int(h_pxl / fig_resize)))
            if not showBG:
                image = np.zeros(image.shape)
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if cog != 'skip':
                plt.scatter(bodies_cog[:, 14, 0] * w_pxl, bodies_cog[:, 14, 1] * h_pxl, color=cog_color,
                            marker='o', s=cog_size/fig_resize)
                plt.vlines(bodies_cog[:, 6, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')
                plt.vlines(bodies_cog[:, 7, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')

            # plot trajectories r_wrist:4, l_wrist:7
            for i, hum in enumerate(np.sort(track.humans_id)):
                df_human = track.humans_tracklet[track.humans_tracklet[:, track.clm_num] == hum]
                plt.plot(df_human[:, 4 * 3 + 1] * w_pxl, df_human[:, 4 * 3 + 2] * h_pxl, linewidth=400/fig_resize)
                plt.plot(df_human[:, 7 * 3 + 1] * w_pxl, df_human[:, 7 * 3 + 2] * h_pxl, linewidth=400/fig_resize)

            plt.ylim(h_pxl, 0)

            # bgimg = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)
            # bgimg = cv2.resize(bgimg, (e.heatMat.shape[1], e.heatMat.shape[0]), interpolation=cv2.INTER_AREA)
            plt.savefig(os.path.join(path_png_estimated,
                                     video.split('.')[-2] + '{:06d}'.format(frame_no) + ".png"))
            plt.close()
            plt.clf()

        # before increment, renew some args
        frame_no += 1
        gc.collect()
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    logger.info("finish estimation & start encoding")
    cmd = ["ffmpeg", "-r", str(caps_fps), "-start_number", str(start_frame),
           "-i", os.path.join(path_png_estimated, video.split('.')[-2] + "%06d.png"),
           "-vcodec", "libx264", "-pix_fmt", "yuv420p",
           os.path.join(path_movie_out, video.split('.')[-2] + "_track.mp4")]
    subprocess.call(cmd)
    logger.debug('finished+')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('--path', type=str, default="")
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--resize', type=str, default='0x0', help='network input resize. default=432x368')
    parser.add_argument('--model', type=str, default='cmu', help='cmu / mobilenet_thin')
    parser.add_argument('--showBG', type=bool, default=True, help='False to show skeleton only.')
    parser.add_argument('--start_frame', type=int, default=0)
    parser.add_argument('--cog', type=str, default="")
    parser.add_argument('--cog_color', type=str, default='black')
    parser.add_argument('--cog_size', type=str, default='M')
    parser.add_argument('--resize_out_ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')
    parser.add_argument('--debug', type=bool, default=False)
    parser.add_argument('--orientation', type=str, default="horizontal")
    parser.add_argument('--plot_image', type=str, default="")
    args = parser.parse_args()
    print(str(args.cog))
    estimate_trajectory(video=args.video, path=args.path, resize=args.resize, model=args.model, orientation=args.orientation,
                        resize_out_ratio=args.resize_out_ratio, showBG=args.showBG, plot_image=args.plot_image,
                        cog=args.cog, cog_color=args.cog_color, cog_size=args.cog_size, start_frame=args.start_frame, debug=args.debug)

