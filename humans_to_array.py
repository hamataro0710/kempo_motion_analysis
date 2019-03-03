import pandas as pd
import numpy as np

from tf_pose import common
# from tf-pose-estimation.tf_pose.common import CocoPart


def humans_to_array(humans):
    array_humans = []
    for human in humans:
        # draw point
        array_human = []
        for i in range(common.CocoPart.Background.value):
            if i not in human.body_parts.keys():
                array_human.append([np.nan, np.nan, 0])
            else:
                array_human.append([human.body_parts[i].x, human.body_parts[i].y, human.body_parts[i].score])

            # body_part = human.body_parts[i]
            # center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
            # centers[i] = center
            # cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)
        array_humans.append(array_human)
    print(array_humans)
    return array_humans


def calc_segment_cog(segments, rates=[]):
    """
    :param segments:
    :param rates:
    :return: center of gravity; this reflects segments' score because there can be occlusion
    """
    seg_cog = (np.dot(np.multiply(rates, segments[:, 2]), segments[:, :2])) / np.dot(segments[:, 2], np.array(rates))
    seg_cog.append(np.mean(segments[:, 2]))
    return seg_cog


def segment_cog(a_human, props_body):
    head_cog = calc_segment_cog(a_human[14:18], [1, 1, 1, 1])
    if a_human[1,2] == 0:
        neck_cog = a_human[1]
    else:
        neck_cog = calc_segment_cog(np.vstack((a_human[2],a_human[5])))
    hip_cog = calc_segment_cog(np.vstack((a_human[8], a_human[11])))
    torso_cog = calc_segment_cog(np.vstack((neck_cog, hip_cog)), [1, 1])
    r_thigh_cog = calc_segment_cog(np.vstack(a_human[8], a_human[9]), [52.5, 47.5])
    l_thigh_cog = calc_segment_cog(np.vstack(a_human[11], a_human[12]), [52.5, 47.5])
    r_leg_cog = calc_segment_cog(np.vstack(a_human[9], a_human[10]), [59.4, 40.6])
    l_leg_cog = calc_segment_cog(np.vstack(a_human[12], a_human[13]), [59.4, 40.6])
    r_arm_cog = calc_segment_cog(np.vstack(a_human[2], a_human[3]), [1, 1])
    l_arm_cog = calc_segment_cog(np.vstack(a_human[5], a_human[6]), [1, 1])
    r_forearm_cog = calc_segment_cog(np.vstack(a_human[3], a_human[4]), [1, 1])
    l_forearm_cog = calc_segment_cog(np.vstack(a_human[6], a_human[7]), [1, 1])

# Neck = 1
# RShoulder = 2
# LShoulder = 5
# RHip = 8
# LHip = 11

# Center of Gravity of each body segments
# head_cog      = (17.9*cervical_JC + 82.1*headT)/100
head_cog      = (17.9*cervical_JC + 82.1*headT)/100
torso_cog     = (50*C_ill + 50*cervical_JC)/100
pelvis_cog    = (50*C_ill + 50*(R_hip_JC + L_hip_JC)/2)/100
R_thigh_cog   = (52.5*R_hip_JC + 47.5*R_knee_JC)/100
L_thigh_cog   = (52.5*L_hip_JC + 47.5*L_knee_JC)/100
R_leg_cog     = (59.4*R_knee_JC + 40.6*R_ankle_JC)/100
L_leg_cog     = (59.4*L_knee_JC + 40.6*L_ankle_JC)/100
R_foot_cog    = R_heel + R_foot_y_axis * foot_length * 40.5/100
L_foot_cog    = L_heel + L_foot_y_axis * foot_length * 40.5/100


# Nose = 0
# Neck = 1
# RShoulder = 2
# RElbow = 3
# RWrist = 4
# LShoulder = 5
# LElbow = 6
# LWrist = 7
# RHip = 8
# RKnee = 9
# RAnkle = 10
# LHip = 11
# LKnee = 12
# LAnkle = 13
# REye = 14
# LEye = 15
# REar = 16
# LEar = 17
# Background = 18
