from huggingface_hub import hf_hub_download
from segment_anything import sam_model_registry, SamPredictor
import cv2
import matplotlib.pyplot as plt
import numpy as np
from definitions import ROOT_DIR
import os
import pandas as pd

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

""""
CLASS: Sam Cleaner.
DESCRIPTION: script that given a .csv with ulcer correspondences in (x,y), executes
SAM model in order to get full leg mask. Then, each mask is multiplied to depth image
so undesired pixels will have values <=0. This is, in summary, a way to filter depth image by
segmentating foot. 
CREATION DATE: 14/04/2024
AUTHOR: Jaume Adrover Fernández
"""
def getLegMask(masks,scores):
    old_score = 9999
    foot_mask = None
    for i, (mask, score) in enumerate(zip(masks, scores)):
        if old_score > score:
            foot_mask = mask
            old_score = score
        plt.imshow(image)
        show_mask(mask, plt.gca())
        show_points(input_point, input_label, plt.gca())
        print(input_point)
        plt.title(f"Mask {i + 1}, Score: {score:.3f}", fontsize=18)
        plt.axis('off')
        plt.show()
    return foot_mask


def searchImgCoords(filename,df):
    # substitute c for d
    d_file = filename.replace('c', 'd')
    print()
    row = df.loc[df['Filename'] == filename]
    print(row)
    cx, cy = row.iloc()[0]['X'], row.iloc()[0]['Y']
    return cx, cy



def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))

# Initialize SAM model
model_type = "vit_b"
checkp_path = os.path.join(ROOT_DIR, "models/checkpoints/sam_vit_b_01ec64.pth")

sam = sam_model_registry[model_type](checkpoint=checkp_path)
predictor = SamPredictor(sam)


csv_path = 'D:\\FootWoundsSegmentation\\data\\annotations.csv'
df = pd.read_csv(csv_path)
folder_path = 'D:\\FootWoundsSegmentation\\data\\p_0001\\2022-05-19\\color'
depth_images_path = 'D:\\FootWoundsSegmentation\\data\\p_0001\\2022-05-19\\depth'

# Main Loop
for f in os.listdir(folder_path):
    filename = f                        # get filename
    depth_filename = f.replace('c','d') # get depth filename
    depth_filename = depth_filename.replace('.jpg','.png')
    # get frame number
    frame =  int(filename.split('_')[4].split('.')[0])
    print('Frame:'+str(frame))
    if (100 <= frame <= 289) or (10 <= frame <= 29):
        continue
    cx, cy = searchImgCoords(filename,df )  # get coords from filename
    image = cv2.imread(os.path.join(folder_path, filename))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictor.set_image(image)
    input_point = np.array([[cx, cy]])
    input_label = np.array([1])
    masks, scores, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    # get SAM predictions
    foot_mask = getLegMask(masks,scores)    # get worst SAM mask (full leg)
    depth_image = cv2.imread(os.path.join(depth_images_path, depth_filename), cv2.IMREAD_UNCHANGED)  # read depth image
    new_depth_image = depth_image * foot_mask
    print(new_depth_image)
    cv2.imwrite('depth/'+depth_filename, new_depth_image)




