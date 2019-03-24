import numpy as np
from scipy.spatial import distance
from collections import Counter
from modules.humans_to_array import segments_degree


def track_humans(humans, prev_humans, prev_id):
    """
    features... body size, cog_whole,
    :param :
    :return:
    """
    # heights = [max(h[~np.isnan(h[:, 1])]) - min(h[~np.isnan(h[:, 1])]) for h in humans]
    # stances = np.array([human[10, 0] - human[13, 0] for human in humans])
    # torsos = np.array([segments_degree(human)[0] for human in humans])
    # features = np.concatenate((heights, stances, torsos))

    # calculate humans points distances
    # 1.distance of body parts
    distances = np.array([distance.cdist(humans[:, i, :2], prev_humans[:, i, :2]) for i in range(18)])
    # 2. search nearest body
    nearest_body_dist = np.nanmean(distances, axis=0)
    # nearest_body_num means previous frame's body's index from current ones
    nearest_body_num = np.argmin(np.nanmean(distances, axis=0), axis=1)
    # print(nearest_body_num)
    # print(prev_id)
    new_body_num = prev_id[nearest_body_num]

    duplicate_num = [item for item, count in Counter(nearest_body_num).items() if count > 1]
    # diff in 1 frame should be less than 5% of the pixels
    new_body_idx = np.where(nearest_body_dist[0, nearest_body_num] > 0.0025)[0]
    if len(duplicate_num):
        for idx in duplicate_num:
            target_num =np.where(nearest_body_num==idx)
            correct_idx = np.argmin(nearest_body_dist[target_num, idx])
            new_body_idx = np.concatenate((new_body_idx, np.delete(target_num, correct_idx))).astype('int')
        new_body_num[new_body_idx] = range(max(new_body_num) + 1, max(new_body_num) + 1 + len(new_body_idx))
    return new_body_num
