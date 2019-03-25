import numpy as np
from scipy.spatial import distance
from collections import Counter


def track_humans(humans, prev_humans, prev_id):
    """
    features... body size, cog_whole,
    :param :
    :return:
    """
    # calculate humans points distances
    # 1.distance of body parts
    distances = np.array([distance.cdist(humans[:, i, :2], prev_humans[:, i, :2]) for i in range(humans.shape[1])])

    # 2. search nearest body
    nearest_body_dist = np.nanmean(distances, axis=0)
    # nearest_body_num means previous frame's body's index from current ones
    nearest_body_num = np.argmin(np.nanmean(distances, axis=0), axis=1)
    # sort previous ids
    current_id = prev_id[nearest_body_num]

    # diff in 1 frame should be less than 15% of the pixels
    new_appearance = np.where(nearest_body_dist[0, nearest_body_num] > 0.0225)[0]
    # check the duplication of nearest body num
    duplicate_num = [item for item, count in Counter(nearest_body_num).items() if count > 1]
    if len(duplicate_num):
        for idx in duplicate_num:
            target_num = np.where(nearest_body_num == idx)
            correct_idx = np.argmin(nearest_body_dist[target_num, idx])
            new_appearance = np.concatenate((new_appearance, np.delete(target_num, correct_idx))).astype('int')
        current_id[new_appearance] = range(max(prev_id) + 1, max(prev_id) + 1 + len(new_appearance))
    return current_id
