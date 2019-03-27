import numpy as np
from scipy.spatial import distance
from collections import Counter


class TrackHumans:
    def __init__(self, start_frame=0,):
        self.start = start_frame
        self.humans_id = None
        # self.humans_current = None
        # self.humans_tracklet = None
        self.clm_num = None
        self.humans_post = None

    def track_humans(self, frame, humans):
        """
        features... body size, cog_whole,
        :param :
        :return:
        """
        # initialize
        humans_current = np.concatenate((np.c_[np.repeat(frame, len(humans))],
                                         humans.reshape(humans.shape[0], humans.shape[1] * humans.shape[2])), axis=1)
        if frame == self.start:
            self.humans_id = np.array(range(len(humans)))
            self.humans_current = np.concatenate((humans_current, np.c_[self.humans_id]), axis=1)
            self.humans_tracklet = self.humans_current
            self.clm_num = self.humans_current.shape[1] - 1

        else:
            self.humans_id = self.search_nearest(humans, self.humans_post, self.humans_id)
            self.humans_current = np.concatenate((humans_current, np.c_[self.humans_id]), axis=1)
            self.humans_tracklet = np.concatenate((self.humans_tracklet[self.humans_tracklet[:, 0] > (frame - 30)],
                                                   self.humans_current))
        self.humans_post = humans

    @staticmethod
    def search_nearest(humans, prev_humans, prev_id):
        # calculate humans points distances
        # 1.distance of body parts
        distances = np.array([distance.cdist(humans[:, i, :2], prev_humans[:, i, :2]) for i in range(humans.shape[1])])

        # 2. search nearest body
        nearest_body_dist = np.nanmean(distances, axis=0)
        nearest_body_dist[np.isnan(nearest_body_dist)] = 1  # set 1(over threshold)
        # nearest_body_num means previous frame's body's index from current ones
        nearest_body_num = np.nanargmin(nearest_body_dist, axis=1)
        # sort previous ids
        current_id = prev_id[nearest_body_num]

        # diff in 1 frame should be less than 15% of the pixels
        new_appearance = np.where(nearest_body_dist[0, nearest_body_num] > 0.50)[0]
        # check the duplication of nearest body num
        duplicate_num = [item for item, count in Counter(nearest_body_num).items() if count > 1]
        if len(duplicate_num):
            for idx in duplicate_num:
                target_num = np.where(nearest_body_num == idx)
                correct_idx = np.argmin(nearest_body_dist[target_num, idx])
                new_appearance = np.concatenate((new_appearance, np.delete(target_num, correct_idx))).astype('int')
            current_id[new_appearance] = range(max(prev_id) + 1, max(prev_id) + 1 + len(new_appearance))
        return current_id
