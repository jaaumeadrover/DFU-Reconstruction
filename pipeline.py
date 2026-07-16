import argparse

from src.annotations.image_annotation import annotate
from src.annotations.sam_cleaner import segment
from src.preprocessing.bag_extraction import extract_frames
from src.preprocessing.pcd_creation import create_point_clouds
from src.registration.run_registration import run_registration


def run_pipeline(patient, date, strategy='batch', retry_attempts=3, inner_threshold=0.875,
                  batch_size=5, batch_threshold=0.879):
    print(f'== [1/5] Extracting frames for {patient}/{date} ==')
    extract_frames(patient, date)

    print(f'== [2/5] Annotating wound location for {patient}/{date} ==')
    annotate(patient, date)

    print(f'== [3/5] SAM-segmenting depth frames for {patient}/{date} ==')
    segment(patient, date)

    print(f'== [4/5] Cropping point clouds around the wound for {patient}/{date} ==')
    create_point_clouds(patient, date)

    print(f'== [5/5] Registering point clouds ({strategy}) for {patient}/{date} ==')
    run_registration(patient, date, strategy, retry_attempts, inner_threshold,
                      batch_size, batch_threshold)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Run the full DFU reconstruction pipeline for one patient/date: bag '
                     'extraction, wound annotation, SAM segmentation, point cloud creation '
                     'and registration.')
    parser.add_argument('--patient', required=True, help="Patient folder name, e.g. 'p_0001'")
    parser.add_argument('--date', required=True, help="Recording date, e.g. '2022-05-19'")
    parser.add_argument('--strategy', choices=['sequential', 'batch'], default='batch',
                         help='Registration strategy (default: batch)')
    parser.add_argument('--retry-attempts', type=int, default=3)
    parser.add_argument('--inner-threshold', type=float, default=0.875)
    parser.add_argument('--batch-size', type=int, default=5, help='Only used with --strategy batch')
    parser.add_argument('--batch-threshold', type=float, default=0.879, help='Only used with --strategy batch')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    run_pipeline(args.patient, args.date, args.strategy, args.retry_attempts,
                 args.inner_threshold, args.batch_size, args.batch_threshold)
