import numpy as np

from modules.humans_to_array import calc_cog, segment_cog, humans_to_array

"""
Estimation of PROPERTIES of BODY segments
this estimation depends on japanese paper;
Ae et,al. "ESTIMATION OF INERTIA PROPERTIES OF THE BODY SEGMENTS IN JAPANESE ATHLETES"
バイオメカニズム 11(0), 23-33, 1992
"""


class MotionAnalysis():
    # japanese male average length of body segments
    # units are meter-kg

    def __init__(self, height=1.70, weight=60, fps=30, humans_for_gravity=[]):
        self.fps = fps
        self.height = height
        self.weight = weight
    # body_length:
        self.foot_length = 0.26 / 1.70 * self.height
        self.leg_length = 0.43 / 1.70 * self.height  # from ankle to knee
        self.thigh_length = 0.43 / 1.70 * self.height  # from knee to troachanter
        self.torso_length = 0.5 / 1.70 * self.height  # from trochanter to neck
        self.head_length = 0.28 / 1.70 * self.height  # from neck to head-top
        self.arm_length = 0.3 / 1.70 * self.height
        self.forearm_length = 0.25 / 1.70 * self.height
        self.hand_length = 0.19 / 1.70 * self.height
    # body_weight:
        self.foot_weight = -0.26784 + 2.61804 * self.foot_length + 0.00545 * self.weight
        self.leg_weight = -1.71524 + 6.04396 * self.leg_length + 0.03885 * self.weight
        self.thigh_weight = -4.53542 + 14.5253 * self.thigh_length + 0.09324 * self.weight
        self.pelvis_weight = (-10.1647 + 18.7503 * self.torso_length + 0.48275 * self.weight) * (163/592)#座位時の肩峰高/超骨稜高
        self.head_weight = -1.1968 + 25.9526 * self.head_length + 0.02604 * self.weight
        self.arm_weight = -0.36785 + 1.15588 * self.arm_length + 0.02712 * self.weight
        self.forearm_weight = -0.43807 + 2.22923 * self.forearm_length + 0.01397 * self.weight
        self.hand_weight = -0.01474 + 2.09424 * self.hand_length + 0.00414 * self.weight
        self.torso_weight = self.weight \
                            - (self.foot_weight + self.leg_weight + self.thigh_weight
                            + self.arm_weight + self.forearm_weight + self.hand_weight) * 2\
                            - self.pelvis_weight - self.head_weight
        # self.torso_weight = (-10.1647 + 18.7503 * self.torso_length + 0.48275 * self.weight) * 0.43/0.54
        self.weights = np.array([self.head_weight, self.torso_weight,
                            self.thigh_weight, self.thigh_weight, self.leg_weight, self.leg_weight,
                            self.foot_weight, self.foot_weight, self.arm_weight, self.arm_weight,
                            self.forearm_weight, self.forearm_weight, self.hand_weight, self.hand_weight,])
    #     # estimation of inertia of body segments
    #     foot_inertia = np.zeros(3, 3)
    #     foot_inertia[1, 1] = (-38.9258 + 214.578*self.foot_length + 0.01445*self.weight)/10000
    #     foot_inertia[2, 2] = (-6.29702 + 37.6738*self.foot_length + 0.01248*self.weight)/10000
    #     foot_inertia[3, 3] = (-40.9844 + 228.138*self.foot_length + 0.00753*self.weight)/10000
    #     leg_inertia = np.zeros(3, 3)
    #     leg_inertia[1, 1] = (-1190.24 + 3093.33*self.leg_length + 5.27481*self.weight)/10000
    #     leg_inertia[2, 2] = (-1174.66 + 3048.1 *self.leg_length + 5.19169*self.weight)/10000
    #     leg_inertia[3, 3] = (-62.7928 + 104.746*self.leg_length + 1.10838*self.weight)/10000
    #     thigh_inertia = np.zeros(3, 3)
    #     thigh_inertia[2, 2] = (-2043.38 + 5547.75*self.thigh_length + 10.6498*self.weight)/10000
    #     thigh_inertia[3, 3] = (-350.308 + 418.338*self.thigh_length + 6.6271 *self.weight)/10000
    #     torso_inertia = np.zeros(3, 3)
    #     torso_inertia[1, 1] = (-6157.42  + 15247.8*self.torso_length*(1-163/592) + 58.0109*self.weight)/10000
    #     torso_inertia[2, 2] = (-6423.4   + 15063.0*self.torso_length*(1-163/592) + 71.5226*self.weight)/10000
    #     torso_inertia[3, 3] = (-2016.55  - 1516.61*self.torso_length*(1-163/592) + 48.8973*self.weight)/10000
    #     pelvis_inertia = np.zeros(3, 3)
    #     pelvis_inertia[1, 1] = (-1687.06 + 5588.38*self.torso_length*163/592 + 22.6268*self.weight)/10000
    #     pelvis_inertia[2, 2] = (-1982.55 + 6516.01*self.torso_length*163/592 + 27.7046*self.weight)/10000
    #     pelvis_inertia[3, 3] = (-1376.85 - 2246.6 *self.torso_length*163/592 + 29.075 *self.weight)/10000
    #     arm_inertia = np.zeros(3, 3)
    #     arm_inertia[1, 1] = (-317.679 + 1007.85*self.arm_length + 1.85249*self.weight)/10000
    #     arm_inertia[2, 2] = (-312.14 + 999.691*self.arm_length + 1.74277*self.weight)/10000
    #     arm_inertia[3, 3] = (-11.1029 -44.8794*self.arm_length + 0.71203*self.weight)/10000
    #     forearm_inertia = np.zeros(3, 3)
    #     forearm_inertia[1, 1] = (-145.867 + 562.219*self.forearm_length + 0.85722*self.weight)/10000
    #     forearm_inertia[2, 2] = (-146.449 + 576.661*self.forearm_length + 0.79727*self.weight)/10000
    #     forearm_inertia[3, 3] = (-13.4756 + 26.3785*self.forearm_length + 0.24644*self.weight)/10000
    #     hand_inertia = np.zeros(3, 3)
    #     hand_inertia[1, 1] = (-6.36541 + 80.3581*self.hand_length + 0.10995*self.weight)/10000
    #     hand_inertia[2, 2] = (-7.30695 + 82.0684*self.hand_length + 0.14433*self.weight)/10000
    #     hand_inertia[3, 3] = (-1.67255 + 9.0812*self.hand_length + 0.05381*self.weight)/10000
    #     head_inertia = np.zeros(3, 3)
    #     head_inertia[1, 1] = (-367.903 + 2843.24*self.head_length + 2.71413*self.weight)/10000
    #     head_inertia[2, 2] = (-354.077 + 2680.71*self.head_length + 2.4924*self.weight)/10000
    #     head_inertia[3, 3] = (-138.956 + 1307.37*self.head_length + 1.24856*self.weight)/10000
    #     [humans_for_gravity

    def single_body_cog(self, human):
        segments_cog = segment_cog(human)
        cog = calc_cog(segments_cog,
                       [self.head_weight, self.torso_weight,
                        self.thigh_weight, self.thigh_weight, self.leg_weight,
                        self.leg_weight,
                        self.foot_weight, self.foot_weight, self.arm_weight,
                        self.arm_weight,
                        self.forearm_weight, self.forearm_weight, self.hand_weight,
                        self.hand_weight,
                        ])
        return segments_cog.append(cog)

    def multi_bodies_cog(self, humans):
        a_humans = humans_to_array(humans)
        cogs = []
        for a_human in a_humans:
            segments_cog = segment_cog(a_human=a_human)
            cog = calc_cog(segments_cog,
                           [self.head_weight, self.torso_weight,
                            self.thigh_weight, self.thigh_weight,
                            self.leg_weight, self.leg_weight,
                            self.foot_weight, self.foot_weight,
                            self.arm_weight, self.arm_weight,
                            self.forearm_weight, self.forearm_weight, self.hand_weight,
                            self.hand_weight,
                            ])
            segments_cog.append(cog)
            cogs.append(segments_cog)
        return np.array(cogs)

    def motion(self, human, human_motion):
        """
        :param human:  [body_points_current]
        :param human_motion:  [[body_points], [vel_points], [acl_points]]
        :return:  [[body_points], [vel_points], [acl_points]]
        """
        if not human_motion:
            human_motion = [[0] * 3 for i in range(15)]
            human_motion[0] = human
        seg_cog = segment_cog(human)
        cog_body = calc_cog(seg_cog, self.weights)
        seg_cog = np.array(seg_cog.append(cog_body))
        vel_cur = (seg_cog - human_motion[0]) * self.fps
        acc_cur = (vel_cur - human_motion[1]) * self.fps
        return np.concatenate((seg_cog, vel_cur, acc_cur))

    # def rotation(self, human):


# class CocoPart(Enum):
#     Nose = 0
#     Neck = 1
#     RShoulder = 2
#     RElbow = 3
#     RWrist = 4
#     LShoulder = 5
#     LElbow = 6
#     LWrist = 7
#     RHip = 8
#     RKnee = 9
#     RAnkle = 10
#     LHip = 11
#     LKnee = 12
#     LAnkle = 13
#     REye = 14
#     LEye = 15
#     REar = 16
#     LEar = 17
#     Background = 18
