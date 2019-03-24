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
    # try:
    # print(humans.shape, prev_humans.shape)
    distances = np.array([distance.cdist(humans[:, i, :2], prev_humans[:, i, :2]) for i in range(18)])
    # except:
    #     print(humans.shape, prev_humans.shape)
    # 2. search nearest body
    nearest_body_dist = np.nanmean(distances, axis=0)
    # nearest_body_num means previous frame's body's index from current ones
    nearest_body_num = np.argmin(np.nanmean(distances, axis=0), axis=1)
    # print(nearest_body_num)
    # print(prev_id)
    new_body_num = prev_id[nearest_body_num]

    duplicate_num = [item for item, count in Counter(nearest_body_num).items() if count > 1]
    # diff in 1 frame should be less than 3% of the pixels
    new_body_idx = np.where(nearest_body_dist[0, nearest_body_num] > 0.0009)[0]
    if len(duplicate_num):
        for idx in duplicate_num:
            target_num =np.where(nearest_body_num==idx)
            correct_idx = np.argmin(nearest_body_dist[target_num, idx])
            new_body_idx = np.concatenate((new_body_idx, np.delete(target_num, correct_idx))).astype('int')
        new_body_num[new_body_idx] = range(max(new_body_num) + 1, max(new_body_num) + 1 + len(new_body_idx))
    return new_body_num
