import numpy as np
from ..Kinetics_LBMC.utils.norm_vector import norm_vector as norm_vector
from ..Kinetics_LBMC.Segment import Segment as Segment


def extraction_pycgm2(points, points_name):
    points_ind = dict()
    for index_point, name_point in enumerate(points_name):
        points_ind[name_point] = index_point
    # Pelvis
    RASI = points[:, points_ind['RASI'], :]
    LASI = points[:, points_ind['LASI'], :]
    RPSI = points[:, points_ind['RPSI'], :]
    LPSI = points[:, points_ind['LPSI'], :]

    midASIS = points[:, points_ind['midASIS'], :]
    PELVIS_X = points[:, points_ind['PELVIS_X'], :]
    PELVIS_Y = points[:, points_ind['PELVIS_Y'], :]
    PELVIS_Z = points[:, points_ind['PELVIS_Z'], :]

    # Right Leg
    RTHAP = points[:, points_ind['RTHAP'], :]
    RTAD = points[:, points_ind['RTAD'], :]
    RTHI = points[:, points_ind['RTHI'], :]
    RKNE = points[:, points_ind['RKNE'], :]

    RHJC = points[:, points_ind['RHJC'], :]
    RFEMUR_X = points[:, points_ind['RFEMUR_X'], :]
    RFEMUR_Y = points[:, points_ind['RFEMUR_Y'], :]
    RFEMUR_Z = points[:, points_ind['RFEMUR_Z'], :]

    # Left Leg
    LTHAP = points[:, points_ind['LTHAP'], :]
    LTAD = points[:, points_ind['LTAD'], :]
    LTHI = points[:, points_ind['LTHI'], :]
    LKNE = points[:, points_ind['LKNE'], :]

    LHJC = points[:, points_ind['LHJC'], :]
    LFEMUR_X = points[:, points_ind['LFEMUR_X'], :]
    LFEMUR_Y = points[:, points_ind['LFEMUR_Y'], :]
    LFEMUR_Z = points[:, points_ind['LFEMUR_Z'], :]

    # Right Tibia
    RTTU = points[:, points_ind['RTTU'], :]
    RTIAD = points[:, points_ind['RTIAD'], :]
    RTIB = points[:, points_ind['RTIB'], :]
    RANK = points[:, points_ind['RANK'], :]

    RKJC = points[:, points_ind['RKJC'], :]
    RTIBIA_X = points[:, points_ind['RTIBIAPROX_X'], :]
    RTIBIA_Y = points[:, points_ind['RTIBIAPROX_Y'], :]
    RTIBIA_Z = points[:, points_ind['RTIBIAPROX_Z'], :]

    # Left Tibia
    LTTU = points[:, points_ind['LTTU'], :]
    LTIAD = points[:, points_ind['LTIAD'], :]
    LTIB = points[:, points_ind['LTIB'], :]
    LANK = points[:, points_ind['LANK'], :]

    LKJC = points[:, points_ind['LKJC'], :]
    LTIBIA_X = points[:, points_ind['LTIBIAPROX_X'], :]
    LTIBIA_Y = points[:, points_ind['LTIBIAPROX_Y'], :]
    LTIBIA_Z = points[:, points_ind['LTIBIAPROX_Z'], :]

    # Right fOOT
    RHEE = points[:, points_ind['RHEE'], :]
    RMIF = points[:, points_ind['RMIF'], :]
    RTOE = points[:, points_ind['RTOE'], :]
    RMET = points[:, points_ind['RMET'], :]
    RFMH = points[:, points_ind['RFMH'], :]

    RAJC = points[:, points_ind['RAJC'], :]
    RFOOT_X = points[:, points_ind['RFOOT_X'], :]
    RFOOT_Y = points[:, points_ind['RFOOT_Y'], :]
    RFOOT_Z = points[:, points_ind['RFOOT_Z'], :]

    # Left fOOT
    LHEE = points[:, points_ind['LHEE'], :]
    LMIF = points[:, points_ind['LMIF'], :]
    LTOE = points[:, points_ind['LTOE'], :]
    LMET = points[:, points_ind['LMET'], :]
    LFMH = points[:, points_ind['LFMH'], :]

    LAJC = points[:, points_ind['LAJC'], :]
    LFOOT_X = points[:, points_ind['LFOOT_X'], :]
    LFOOT_Y = points[:, points_ind['LFOOT_Y'], :]
    LFOOT_Z = points[:, points_ind['LFOOT_Z'], :]

    # Definition
    u_pelvis = norm_vector(PELVIS_X-midASIS)
    w_pelvis = -norm_vector(PELVIS_Y-midASIS)
    rp_pelvis = midASIS
    rd_pelvis = midASIS-(PELVIS_Z-midASIS)
    rm_pelvis = [RASI, LASI, RPSI, LPSI]

    # Thigh definition
    Ru_thigh = norm_vector(RFEMUR_X-RHJC)
    Rrp_thigh = RHJC
    Rrd_thigh = RKJC
    Rw_thigh = -norm_vector(RFEMUR_Y-RHJC)
    Rrm_thigh = [RTHAP, RTAD, RTHI, RKNE]

    Lu_thigh = norm_vector(LFEMUR_X-LHJC)
    Lrp_thigh = LHJC
    Lrd_thigh = LKJC
    Lw_thigh = -norm_vector(LFEMUR_Y-LHJC)
    Lrm_thigh = [LTHAP, LTAD, LTHI, LKNE]

    # Tibia
    Ru_tibia = norm_vector(RTIBIA_X-RKJC)
    Rrp_tibia = RKJC
    Rrd_tibia = RAJC
    Rw_tibia = -norm_vector(RTIBIA_Y-RKJC)
    Rrm_tibia = [RTTU, RTIAD, RTIB, RANK]

    Lu_tibia = norm_vector(LTIBIA_X-LKJC)
    Lrp_tibia = LKJC
    Lrd_tibia = LAJC
    Lw_tibia = -norm_vector(LTIBIA_Y-LKJC)
    Lrm_tibia = [LTTU, LTIAD, LTIB, LANK]

    # Foot
    Ru_foot = -norm_vector(RFOOT_Z-RAJC)
    Rrp_foot = RAJC
    Rrd_foot = RTOE
    Rw_foot = -norm_vector(RFOOT_Y-RAJC)
    Rrm_foot = [RHEE, RMIF, RTOE, RMET, RFMH]

    Lu_foot = -norm_vector(LFOOT_Z-LAJC)
    Lrp_foot = LAJC
    Lrd_foot = LTOE
    Lw_foot = -norm_vector(LFOOT_Y-LAJC)
    Lrm_foot = [LHEE, LMIF, LTOE, LMET, LFMH]

    segment_pelvis = Segment(u_pelvis, rp_pelvis, rd_pelvis, w_pelvis, rm_pelvis,
                             'Buv', 'Bwu',
                             'Pelvis', rigid_parameter=True)
    Rsegment_thigh = Segment(Ru_thigh, Rrp_thigh, Rrd_thigh, Rw_thigh, Rrm_thigh,
                             'Buv', 'Buw',
                             'RThigh', rigid_parameter=True)
    Rsegment_tibia = Segment(Ru_tibia, Rrp_tibia, Rrd_tibia, Rw_tibia, Rrm_tibia,
                             'Buv', 'Buw',
                             'RTibia', rigid_parameter=True)
    Rsegment_foot = Segment(Ru_foot, Rrp_foot, Rrd_foot, Rw_foot, Rrm_foot,
                            'Buw', 'Bwu',
                            'RFoot', rigid_parameter=True)
    # on inverse rp et rd ici pour pouvoir faire une chaine cinématique
    Lsegment_thigh = Segment(Lu_thigh, Lrp_thigh, Lrd_thigh, Lw_thigh, Lrm_thigh,
                             'Buv', 'Buw',
                             'LThigh', rigid_parameter=True)
    Lsegment_tibia = Segment(Lu_tibia, Lrp_tibia, Lrd_tibia, Lw_tibia, Lrm_tibia,
                             'Buv', 'Buw',
                             'LTibia', rigid_parameter=True)
    Lsegment_foot = Segment(Lu_foot, Lrp_foot, Lrd_foot, Lw_foot, Lrm_foot,
                            'Buw', 'Bwu',
                            'LFoot', rigid_parameter=True)

    return[Rsegment_foot, Rsegment_tibia, Rsegment_thigh, segment_pelvis,
           Lsegment_thigh, Lsegment_tibia, Lsegment_foot]
