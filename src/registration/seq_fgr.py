import os
import time

import open3d as o3d
import pandas as pd

from utils.fgr import run
from utils.path import getPatientPath, writeCsv, getOrderedFileList


def run_seq():
    patient = 'p_0001'
    date = '2022-05-19'

    path = getPatientPath(patient, date) + '/pcd/single/'

    conf = {'files_path': path,
            'retry_attempts': 3,
            'inner_threshold': 0.875, #0.875
            'patient': patient,
            'date': date
            }

    ordered_file_list = getOrderedFileList(path)

    fitness = [None] * 2 * len(ordered_file_list)
    rmse = [None] * 2 * len(ordered_file_list)
    corrsp_set = [None] * 2 * len(ordered_file_list)

    i = 0
    comb = 0
    start = time.time()
    while i < len(ordered_file_list)-1:#100:
        attempts = 0
        current_file = ordered_file_list[i]
        next_file = ordered_file_list[i + 1]

        if comb == 0:
            pcd, score = run(current_file, next_file)
        else:
            current_file = getPatientPath(patient, date) + f'/pcd/unified/pcd_{comb - 1}.pcd'
            pcd, score = run(current_file, next_file)

        while score.fitness < conf['inner_threshold'] and attempts < conf['retry_attempts']:
            pcd, score = run(current_file, next_file)
            attempts += 1

        fitness[i] = score.fitness
        rmse[i] = score.inlier_rmse
        corrsp_set[i] = len(score.correspondence_set)

        print("FITNESS:  ->" +str(score.fitness))
        if score.fitness < conf['inner_threshold']:
            i = i+1
            continue
        print(f'Two point clouds merged successfully! Iteration number: {i}')



        output_combined_path = getPatientPath(patient, date) + f'/pcd/unified/pcd_{comb}.pcd'
        #o3d.io.write_point_cloud(output_combined_path, pcd)
        o3d.visualization.draw_geometries([pcd])
        print(f'Saved combined point cloud: {output_combined_path}')

        i += 1
        comb += 1

    print("Fast global registration took %.3f sec.\n" % (time.time() - start))

    df = pd.DataFrame({"Fitness": fitness, "RMSE": rmse,
                        "Corrsp_set":corrsp_set})
    #writeCsv(getPatientPath(patient, date)+'/validation/metrics3_3.csv', df)


run_seq()
