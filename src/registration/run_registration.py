import argparse
import time

import open3d as o3d
import pandas as pd

from src.registration.fgr import run_until_threshold
from src.utils.path import getPatientPath, getOrderedFileList, createSomeFolders
from src.utils.tools_3d import BatchIntegrator


def run_sequential(conf):
    patient = conf['patient']
    date = conf['date']
    visualize = conf.get('visualize', False)
    ordered_file_list = getOrderedFileList(conf['files_path'])

    fitness = [None] * 2 * len(ordered_file_list)
    rmse = [None] * 2 * len(ordered_file_list)
    corrsp_set = [None] * 2 * len(ordered_file_list)

    i = 0
    comb = 0
    start = time.time()
    while i < len(ordered_file_list) - 1:
        current_file = ordered_file_list[i]
        next_file = ordered_file_list[i + 1]

        if comb != 0:
            current_file = getPatientPath(patient, date) + f'/pcd/unified/pcd_{comb - 1}.pcd'

        pcd, score = run_until_threshold(current_file, next_file,
                                          conf['inner_threshold'], conf['retry_attempts'])

        fitness[i] = score.fitness
        rmse[i] = score.inlier_rmse
        corrsp_set[i] = len(score.correspondence_set)

        print("FITNESS:  ->" + str(score.fitness))
        if score.fitness < conf['inner_threshold']:
            i = i + 1
            continue
        print(f'Two point clouds merged successfully! Iteration number: {i}')

        output_combined_path = getPatientPath(patient, date) + f'/pcd/unified/pcd_{comb}.pcd'
        #o3d.io.write_point_cloud(output_combined_path, pcd)
        if visualize:
            o3d.visualization.draw_geometries([pcd])
        print(f'Saved combined point cloud: {output_combined_path}')

        i += 1
        comb += 1

    print("Fast global registration took %.3f sec.\n" % (time.time() - start))

    df = pd.DataFrame({"Fitness": fitness, "RMSE": rmse,
                        "Corrsp_set": corrsp_set})
    #writeCsv(getPatientPath(patient, date)+'/validation/metrics3_3.csv', df)


def run_batch(conf):
    val_path = getPatientPath(conf['patient'], conf['date']) + '/validation/' + \
               str(conf['batch_size']) + '-batch/'
    createSomeFolders([val_path])

    print('Starting frame integration process with parameters: ')
    print(conf)

    agent = BatchIntegrator(conf)
    start = time.time()
    agent.run()
    print('Batch Integration took:' + str((time.time() - start)))


def run_registration(patient, date, strategy='batch', retry_attempts=3, inner_threshold=0.875,
                      batch_size=5, batch_threshold=0.879, visualize=False):
    conf = {
        'files_path': getPatientPath(patient, date) + '/pcd/single/',
        'retry_attempts': retry_attempts,
        'inner_threshold': inner_threshold,
        'batch_size': batch_size,
        'batch_threshold': batch_threshold,
        'patient': patient,
        'date': date,
        'visualize': visualize,
    }

    if strategy == 'sequential':
        run_sequential(conf)
    else:
        run_batch(conf)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Merge per-frame point clouds of a patient/date into one registered point cloud.')
    parser.add_argument('--patient', required=True, help="Patient folder name, e.g. 'p_0001'")
    parser.add_argument('--date', required=True, help="Recording date, e.g. '2022-05-19'")
    parser.add_argument('--strategy', choices=['sequential', 'batch'], default='batch',
                         help='sequential: chain-merge one pair at a time. '
                              'batch: merge in batches, then fragment-merge batches (default).')
    parser.add_argument('--retry-attempts', type=int, default=3)
    parser.add_argument('--inner-threshold', type=float, default=0.875)
    parser.add_argument('--batch-size', type=int, default=5, help='Only used with --strategy batch')
    parser.add_argument('--batch-threshold', type=float, default=0.879, help='Only used with --strategy batch')
    parser.add_argument('--visualize', action='store_true',
                         help='Show each merged point cloud (sequential strategy only)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    run_registration(args.patient, args.date, args.strategy, args.retry_attempts,
                      args.inner_threshold, args.batch_size, args.batch_threshold, args.visualize)
