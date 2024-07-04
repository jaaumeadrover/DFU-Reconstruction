import time

from utils.path import getPatientPath, createSomeFolders
from utils.tools_3d import BatchIntegrator

if __name__ == '__main__':
    patient = 'p_0001'
    date = '2022-05-19'

    # PointCloud path
    path = getPatientPath(patient, date) + '/pcd/single/'

    # Initial config
    conf = {'files_path': path,
            'retry_attempts': 3,
            'batch_size': 5,
            'batch_threshold': 0.879,
            'inner_threshold': 0.875,
            'patient': patient,
            'date': date
            }

    # Validation Path
    val_path = getPatientPath(patient, date) + '/validation/' + \
               str(conf['batch_size']) + '-batch/'
    createSomeFolders([val_path])

    print('Starting frame integration process with parameters: ')
    print(conf)

    agent = BatchIntegrator(conf)
    start=time.time()
    agent.run()

    print('Batch Integration took:'+str((time.time()-start)))
