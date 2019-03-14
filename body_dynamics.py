def velocity_single_body(human_track):
    return human_track[1] - human_track[0]


def acceleration_single_body(human_velocity):
    return human_velocity[1] - human_velocity[0]


def velocity_multi_bodies(self, humans_track):
    """
    :param humans_track:
    :return:
    """

