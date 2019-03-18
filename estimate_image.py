import argparse
import logging
import os
import sys
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

from modules.motion_analysis import MotionAnalysis


def estimate_image(imagefile, model='cmu', path='', resize='432x368', plt_network=False,
              cog="", cog_color='black', debug=False, resize_out_ratio=4.0, orientation='horizontal'):
    logger = logging.getLogger('TfPoseEstimator')
    logger.setLevel(logging.DEBUG) if debug else logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG) if debug else ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    # formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    w, h = model_wh(resize)
    if orientation == 'horizontal':
        if w == 0: w = 432
        if h == 0: h = 368
    else:
        if w == 0: w = 368
        if h == 0: h = 432
    e = TfPoseEstimator(get_graph_path(model), target_size=(w, h))
    logger.info('resize: %d,  %d' % (w, h))
    path_image = os.path.join(path, 'pictures', imagefile)
    path_out = os.path.join(path, 'pictures')

    # estimate human poses from a single image !
    image = common.read_imgfile(path_image, None, None)
    if image is None:
        logger.error('Image can not be read, path=%s' % path_image)
        sys.exit(-1)
    h_pxl, w_pxl = image.shape[0], image.shape[1]

    t = time.time()
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
    elapsed = time.time() - t
    logger.info('inference image: %s in %.4f seconds.' % (path_image, elapsed))
    logger.debug('shape of image: ' + str(image.shape))

    if cog != 'skip':
        ma = MotionAnalysis()

    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    if not plt_network:
        fig = plt.figure(figsize=(int(w_pxl/200), int(h_pxl/200)))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if cog != 'skip':
            # bodies_cog = bodies_cog[~np.isnan(bodies_cog[:, :, 1])]
            bodies_cog = ma.multi_bodies_cog(humans=humans)
            bodies_cog[np.isnan(bodies_cog[:, :, :])] = 0
            plt.scatter(bodies_cog[:, 14, 0] * w_pxl, bodies_cog[:, 14, 1] * h_pxl, color=cog_color, s=150)
            plt.vlines(bodies_cog[:, 6, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')
            plt.vlines(bodies_cog[:, 7, 0] * w_pxl, ymin=0, ymax=h_pxl, linestyles='dashed')
            plt.ylim(h_pxl, 0)
        bgimg = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)
        bgimg = cv2.resize(bgimg, (e.heatMat.shape[1], e.heatMat.shape[0]), interpolation=cv2.INTER_AREA)
        os.makedirs(path_out, exist_ok=True)
        plt.savefig(os.path.join(path_out,
                                 imagefile.split('.')[-2] + "_estimated.png"))
        plt.show()
    else:
        fig = plt.figure()
        a = fig.add_subplot(2, 2, 1)
        a.set_title('Result')
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.plot()
        bgimg = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)
        bgimg = cv2.resize(bgimg, (e.heatMat.shape[1], e.heatMat.shape[0]), interpolation=cv2.INTER_AREA)

        # show network output
        a = fig.add_subplot(2, 2, 2)
        plt.imshow(bgimg, alpha=0.5)
        tmp = np.amax(e.heatMat[:, :, :-1], axis=2)
        plt.imshow(tmp, cmap=plt.cm.gray, alpha=0.5)
        plt.colorbar()

        tmp2 = e.pafMat.transpose((2, 0, 1))
        tmp2_odd = np.amax(np.absolute(tmp2[::2, :, :]), axis=0)
        tmp2_even = np.amax(np.absolute(tmp2[1::2, :, :]), axis=0)

        a = fig.add_subplot(2, 2, 3)
        a.set_title('Vectormap-x')
        # plt.imshow(CocoPose.get_bgimg(inp, target_size=(vectmap.shape[1], vectmap.shape[0])), alpha=0.5)
        plt.imshow(tmp2_odd, cmap=plt.cm.gray, alpha=0.5)
        plt.colorbar()

        a = fig.add_subplot(2, 2, 4)
        a.set_title('Vectormap-y')
        # plt.imshow(CocoPose.get_bgimg(inp, target_size=(vectmap.shape[1], vectmap.shape[0])), alpha=0.5)
        plt.imshow(tmp2_even, cmap=plt.cm.gray, alpha=0.5)
        plt.colorbar()
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--image', type=str, default='./images/p1.jpg')
    parser.add_argument('--model', type=str, default='cmu', help='cmu / mobilenet_thin')

    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. '
                             'default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize_out_ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')
    parser.add_argument('--plt_network', type=bool, default=False)
    parser.add_argument('--path', type=str, default="")
    parser.add_argument('--cog', type=str, default="")
    parser.add_argument('--cog_color', type=str, default='black')
    parser.add_argument('--debug', type=bool, default=False)
    parser.add_argument('--orientation', type=bool, default="horizontal")

    args = parser.parse_args()
    estimate_image(imagefile=args.image, model=args.model, path=args.path, resize=args.resize,
                   resize_out_ratio=args.resize_out_ratio, plt_network=args.plt_network,
                   cog=args.cog, cog_color=args.cog_color, debug=args.debug, orientation=args.orientation)
