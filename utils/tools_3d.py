"""


"""

import open3d as o3d
import numpy as np
import pandas as pd

from definitions import INTRINSICS
from utils.path import getOrderedFileList, writeCsv, getPatientPath
from utils.metrics import Metrics3D
from utils.fgr import run
"""
Function:
Description:

"""
def buildPcd(color_path,depth_path):
    color_raw = o3d.io.read_image(color_path)
    depth_raw = o3d.io.read_image(depth_path)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw, convert_rgb_to_intensity=False)

    return o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, INTRINSICS)


def getBestPcdIndex(pcd, score):
    index = score.index(max(score))
    return pcd[index], index

class BatchIntegrator:
    def __init__(self, conf):
        self.list = getOrderedFileList(conf['files_path'])
        self.batch_size = conf['batch_size']
        self.retry_attempts = conf['retry_attempts']
        self.batch_threshold = conf['batch_threshold']
        self.inner_threshold = conf['inner_threshold']
        self.patient = conf['patient']
        self.date = conf['date']
        self.patient_path = getPatientPath(self.patient, self.date)

        self.inner_metrics = Metrics3D(len(self.list))
        self.outer_metrics = Metrics3D(int(len(self.list)/self.batch_size) + 1)

    def batchProcess(self, path, index):
        for indx in range(index, index+(self.batch_size-1)):
            pcd, score = run(path, self.list[indx + 1])
            attempts = 0
            while score.fitness < self.inner_threshold:
                pcd, score = run(path, self.list[indx + 1])
                attempts = attempts + 1
                if attempts == self.retry_attempts:
                    break
            self.inner_metrics.setScore(score, indx)
            path = self.patient_path+'/pcd/unified/single/pcd_' + \
            str(indx)+'.pcd'
            o3d.io.write_point_cloud(path, pcd)
        avg_fitness = sum(self.inner_metrics.fitness[index:index+(self.batch_size-1)])/(self.batch_size-1)
        return pcd, avg_fitness

    def saveBatchResult(self, index, pcd):
        header = str(index) + '_' + str(index+(self.batch_size-1))
        path = self.patient_path + '/pcd/unified/batch/pcd_'+header+'.pcd'
        o3d.io.write_point_cloud(path, pcd)

        return header, path


    def mergeBatches(self, checkpoint, actual):
        pcd = [None] * self.retry_attempts
        score = [None] * self.retry_attempts
        score_fitness = [None] * self.retry_attempts

        for ix in range(0, self.retry_attempts):
            pcd[ix], score[ix] = run(checkpoint, actual)
            score_fitness[ix] = score[ix].fitness

        return pcd, score, score_fitness

    def processFragment(self, pcd, score,fitness):
        og_pcd, best_index = getBestPcdIndex(pcd,fitness)
        og_pcd, _ = og_pcd.remove_radius_outlier(nb_points=30, radius=0.05)

        return og_pcd, score[best_index]



    def run(self):
        i = 0
        integr = 0
        integr_Score = 0
        batches_len = int(2 * (len(self.list)/self.batch_size))


        #while i < (len(self.list)-self.batch_size):
        while i < (100):
            print('Iteration number: ' + str(i))
            path = self.list[i]

            # Batch processing
            pcd, avg_fitness = self.batchProcess(path, i)
            print(self.inner_metrics.fitness[i:i+self.batch_size])
            print(avg_fitness)
            # Save batch result
            header, path = self.saveBatchResult(i, pcd)
            actual = path

            # Merge batch Point Clouds
            if integr > 0:
                pcd, score, fitness = self.mergeBatches(checkpoint, actual)
                pcd, score = self.processFragment(pcd, score, fitness)

                self.outer_metrics.setScore(score, integr_Score)
                # Show result
                #o3d.visualization.draw_geometries([pcd])


                print((score.fitness > self.batch_threshold and avg_fitness > self.inner_threshold))
                if score.fitness > self.batch_threshold and avg_fitness > self.inner_threshold:
                    checkpoint = self.patient_path + '/pcd/unified/combined/pcd_'+str(integr)+'.pcd'
                    o3d.io.write_point_cloud(checkpoint,pcd)
                    integr = integr + 1
                integr_Score+=1

            else:
                checkpoint = self.patient_path + '/pcd/unified/batch/pcd_'+header+'.pcd'
                integr = integr + 1
                integr_Score += 1

            i = i + self.batch_size

        self.inner_metrics.write_to_csv(self.patient_path+'/validation/inner_metrics7.csv')
        self.outer_metrics.write_to_csv(self.patient_path+'/validation/outer_metrics7.csv')
        # Write down .csv metrics result
        # path = get
        # df = pd.DataFrame({"inner_fitness": inner_fitness, "inner_rmse": inner_rmse,
        #                    "inner_corrsp_set": inner_correspondence_set, "fragm_fitness": fragm_fitness,
        #                    "fragm_rmse": fragm_rmse, "batch_corrsp_set": fragm_corr_set})
        # writeCsv(path, df)
