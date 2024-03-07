"""
TITLE: create_dataset
DATE: 02/03/2024
AUTHOR: Jaume Adrover Fernández
DESCRIPTION:
"""

import numpy as np
import pyrealsense2 as rs
import cv2
from utils.path import createColDepthImgNames
import os
import time
import utils

"""
FUNCTION:
ARGS: 
    ·src:
    ·target:
DESCRIPTION:
"""
def imagesFromFile(src, target,img_info):
    try:
        time.sleep(1)
        print('\nStarting frame extraction from '+src)
        # Create pipeline
        pipeline = rs.pipeline()
        # Create a config object
        config = rs.config()
        # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
        rs.config.enable_device_from_file(config, src, repeat_playback=False)

        # Enable both color/depth streams
        config.enable_stream(rs.stream.depth, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, rs.format.rgb8, 30)

        # Start streaming from file
        profile = pipeline.start(config)
        profile.get_device().as_playback().set_real_time(False)

        align_to = rs.stream.color
        align = rs.align(align_to)

        # Streaming loop
        number = 0
        while True:
            try:
                frames = pipeline.wait_for_frames(1000)
            except RuntimeError:
                # print("\nNo frames remaining from this video.")
                break
            # Align the depth frame to color frame
            aligned_frames = align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                continue

            # Extract color/depth images
            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Convert BGR to RGB color image
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

            img_names = createColDepthImgNames(img_info, str(number))

            if number % 5 == 0:
                color_path = os.path.join(target['color'], img_names['color'])+'.png'
                depth_path = os.path.join(target['depth'], img_names['depth']) + '.png'

                cv2.imwrite(color_path, color_image)
                cv2.imwrite(depth_path,depth_image)
                #print("Creating image number {:03d}".format(number))
            number += 1





    finally:
        print("Succesfully extracted frames!")

