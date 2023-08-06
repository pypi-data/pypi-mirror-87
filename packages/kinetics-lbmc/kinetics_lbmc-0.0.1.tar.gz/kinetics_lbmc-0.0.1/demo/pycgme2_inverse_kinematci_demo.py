from .. import Kinetics_LBMC as lbmc
from matplotlib import pyplot as plt

import numpy as np
import os
import ezc3d
from extraction_pycgm2 import extraction_pycgm2 as extraction_pycgm2

import time

list_static = ["03489_05293_20201029-SBNNN-VDEF-01.c3d",
               "03444_05238_20200903-SBNNN-VDEF-02.c3d", "03397_05177_20200701-SBNNN-VDEF-02.c3d"]
list_dynamic = ["03489_05293_20201029-GBNNN-VDEF-07.c3d",
                "03444_05238_20200903-GBNNN-VDEF-03.c3d", "03397_05177_20200701-GBNNN-VDEF-03.c3d"]
list_nb_frame = []
list_time = []

for name_static, name_dynamic in zip(list_static, list_dynamic):
    print(name_static)
    print(name_dynamic)
    # ---Extraction en utilisant EzC3D---
    filename_static = os.path.join(
        '.', 'data_demo_pycgm', name_static)
    filename_dynamic = os.path.join(
        '.', 'data_demo_pycgm', name_dynamic)

    # Extraction du c3d
    acq_static = ezc3d.c3d(filename_static)
    # Point ind name extraction
    points_names_static = acq_static['parameters']['POINT']['LABELS']['value']
    # Extraction du c3d
    acq_dynamic = ezc3d.c3d(filename_dynamic)
    # Point ind name extraction
    points_names_dynamic = acq_dynamic['parameters']['POINT']['LABELS']['value']

    points_static = lbmc.points_treatment(
        acq_static, 10, unit_point='mm')
    points_dynamic = lbmc.points_treatment(
        acq_dynamic, 10, unit_point='mm')

    [Rsegment_foot_static, Rsegment_tibia_static, Rsegment_thigh_static,
     segment_pelvis_static,
     Lsegment_thigh_static, Lsegment_tibia_static, Lsegment_foot_static] = extraction_pycgm2(points_static, points_names_static)

    [Rsegment_foot_dynamic, Rsegment_tibia_dynamic, Rsegment_thigh_dynamic,
     segment_pelvis_dynamic,
     Lsegment_thigh_dynamic, Lsegment_tibia_dynamic, Lsegment_foot_dynamic] = extraction_pycgm2(points_dynamic, points_names_dynamic)

    R_segment_foot_final = lbmc.Segment.fromSegment(
        Rsegment_foot_dynamic, segment_static=Rsegment_foot_static)
    R_segment_tibia_final = lbmc.Segment.fromSegment(
        Rsegment_tibia_dynamic, segment_static=Rsegment_tibia_static)
    R_segment_thigh_final = lbmc.Segment.fromSegment(
        Rsegment_thigh_dynamic, segment_static=Rsegment_thigh_static)
    segment_pelvis_final = lbmc.Segment.fromSegment(
        segment_pelvis_dynamic, segment_static=segment_pelvis_static)
    L_segment_thigh_final = lbmc.Segment.fromSegment(
        Lsegment_thigh_dynamic, segment_static=Lsegment_thigh_static)
    L_segment_tibia_final = lbmc.Segment.fromSegment(
        Lsegment_tibia_dynamic, segment_static=Lsegment_tibia_static)
    L_segment_foot_final = lbmc.Segment.fromSegment(
        Lsegment_foot_dynamic, segment_static=Lsegment_foot_static)

    # Joint definition
    LAnkle_joint = lbmc.spherical_model(Lsegment_tibia_static, Lsegment_foot_static,
                                        Lsegment_tibia_static.rd, Lsegment_foot_static.rp)

    LKnee_joint = lbmc.spherical_model(Lsegment_thigh_static, Lsegment_tibia_static,
                                       Lsegment_thigh_static.rd, Lsegment_tibia_static.rp)

    LHip_joint = lbmc.spherical_model(segment_pelvis_static, Lsegment_thigh_static,
                                      Lsegment_thigh_static.rp, Lsegment_thigh_static.rp)

    RHip_joint = lbmc.spherical_model(Rsegment_thigh_static, segment_pelvis_static,
                                      Rsegment_thigh_static.rp, Rsegment_thigh_static.rp)

    RKnee_joint = lbmc.spherical_model(Rsegment_tibia_static, Rsegment_thigh_static,
                                       Rsegment_tibia_static.rp, Rsegment_thigh_static.rd)

    RAnkle_joint = lbmc.spherical_model(Rsegment_foot_static, Rsegment_tibia_static,
                                        Rsegment_foot_static.rp, Rsegment_tibia_static.rd)

    full_segment = list([R_segment_foot_final, R_segment_tibia_final,
                         R_segment_thigh_final, segment_pelvis_final,
                         L_segment_thigh_final, L_segment_tibia_final,
                         L_segment_foot_final])
    # full_segment = list(
    #     [R_segment_foot_final, Rsegment_tibia_dynamic, Rsegment_thigh_dynamic])
    full_model_test = [RAnkle_joint, RKnee_joint,
                       RHip_joint, LHip_joint,
                       LKnee_joint, LAnkle_joint]
    # full_model_test = [joint_model.no_model(), joint_model.no_model(),
    #                    joint_model.no_model(), joint_model.no_model(),
    #                    joint_model.no_model(), joint_model.no_model()]
    start_time = time.time()
    lbmc.multi_body_optimisation(full_segment, full_model_test)
    final_time = time.time() - start_time

    # copy des infos pour les points
    temp_list = points_names_dynamic.copy()
    list_point = temp_list

    # Creation of the equivalent name value in ezc3d
    points_ind = dict()
    for index_point, name_point in enumerate(list_point):
        points_ind[name_point] = index_point
    new_list = []
    for value in temp_list:

        if 'pyCGM2' not in value:
            new_list.append(value)
    nb_frame = acq_dynamic['data']['points'].shape[2]
    new_array = np.zeros((4, len(new_list), nb_frame))

    # Choice of the list to analyse

    points_temp = acq_dynamic['data']['points'][0:3, :, :]
    for ind_point, name_point in enumerate(new_list):
        new_array[0:3, ind_point, :] = points_temp[:,
                                                   points_ind[name_point], :]
        new_array[3, ind_point, :] = 1

    for segment in full_segment:
        name_segment = segment.segment_name
        for ind_rm in range(len(segment.nm_list)):
            name_marker = name_segment + str(ind_rm)
            # print(name_marker)

            new_list.append(name_marker)
            new_point = np.zeros((4, 1, nb_frame))

            temp = np.dot(
                segment.nm_list[ind_rm].T, segment.Q)*1000
            new_point[0, 0, :] = temp[0, :]
            new_point[1, 0, :] = -temp[2, :]
            new_point[2, 0, :] = temp[1, :]
            new_point[3, 0, :] = 1

            new_array = np.append(new_array, new_point, axis=1)
        list_point_to_add = [segment.rp+0.1*segment.u,
                             segment.rp, segment.rd, segment.rd+0.1*segment.w]
        list_name = ['u', 'rp', 'rd', 'w']

        for ind_point, point in enumerate(list_point_to_add):
            name_point = list_name[ind_point] + '_'+name_segment
            # print(name_point)
            new_list.append(name_point)
            new_point = np.zeros((4, 1, nb_frame))
            temp = point * 1000
            new_point[0, 0, :] = temp[0, :]
            new_point[1, 0, :] = -temp[2, :]
            new_point[2, 0, :] = temp[1, :]
            new_point[3, 0, :] = 1

            new_array = np.append(new_array, new_point, axis=1)

        homo_segment_rel_frame = segment.Tprox*segment.corr_prox

        Or = homo_segment_rel_frame.T_homo[:, 3, :]
        X = Or+0.1*homo_segment_rel_frame.T_homo[:, 0, :]
        Y = Or+0.1*homo_segment_rel_frame.T_homo[:, 1, :]
        Z = Or+0.1*homo_segment_rel_frame.T_homo[:, 2, :]

        # list_point_to_add = [Or, X, Y, Z]
        # list_name = ['Or', 'X', 'Y', 'Z']

        # for ind_point, point in enumerate(list_point_to_add):
        #     name_point = list_name[ind_point] + '_'+name_segment
        #     # print(name_point)
        #     new_list.append(name_point)
        #     new_point = np.zeros((4, 1, nb_frame))
        #     temp = point * 1000
        #     new_point[0, 0, :] = temp[0, :]
        #     new_point[1, 0, :] = -temp[2, :]
        #     new_point[2, 0, :] = temp[1, :]
        #     new_point[3, 0, :] = 1

        #     new_array = np.append(new_array, new_point, axis=1)

    c3d = ezc3d.c3d()

    # Fill it with random data
    c3d['parameters']['POINT']['RATE']['value'] = [nb_frame]
    c3d['parameters']['POINT']['LABELS']['value'] = new_list
    c3d['data']['points'] = new_array
    new_filename = filename_dynamic.replace('.c3d', 'invkin.c3d')
    print(new_filename)
    c3d.write(new_filename)
    print("--- %s frames ---" % (nb_frame))
    print("--- %s seconds ---" % (final_time))
    print("--- %s seconds ---" % (final_time/nb_frame))
    list_nb_frame.append(nb_frame)
    list_time.append(final_time)


for nb_frame, final_time, filename in zip(list_nb_frame, list_time, list_dynamic):
    print(filename)
    print("--- %s frames ---" % (nb_frame))
    print("--- %s seconds ---" % (final_time))
    print("--- %s seconds ---" % (final_time/nb_frame))
