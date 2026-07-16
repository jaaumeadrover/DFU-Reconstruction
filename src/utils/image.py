import os
import tkinter as tk
import csv
import matplotlib.pyplot as plt
import numpy as np

from segment_anything import sam_model_registry, SamPredictor
from definitions import ROOT_DIR
class ImageAnnotator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_files = [f for f in self.get_ordered_file_list(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        self.current_index = 0
        self.annotations = {}

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.load_image()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()

    def get_ordered_file_list(self, folder_path):
        file_list = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        return sorted(file_list, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    def load_image(self):
        if self.current_index < len(self.image_files):
            image_path = os.path.join(self.folder_path, self.image_files[self.current_index])
            self.image = tk.PhotoImage(file=image_path)

            # Get image dimensions
            image_width = self.image.width()
            image_height = self.image.height()

            # Resize canvas to match image dimensions
            self.canvas.config(width=image_width, height=image_height)

            # Display image on canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def on_click(self, event):
        filename = self.image_files[self.current_index]
        self.annotations[filename] = (event.x, event.y)
        print(f"Clicked at ({event.x}, {event.y}) on {filename}")

        self.current_index += 1
        self.canvas.delete("all")
        self.load_image()

    def save_annotations_to_csv(self, csv_file):
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Filename', 'X', 'Y'])
            for filename, (x, y) in self.annotations.items():
                writer.writerow([filename, x, y])




def getLegMask(masks,scores,input_point,input_label, image):
    old_score = 9999
    foot_mask = None
    for i, (mask, score) in enumerate(zip(masks, scores)):
        if old_score > score:
            foot_mask = mask
            old_score = score
        plt.imshow(image)
        show_mask(mask, plt.gca())
        show_points(input_point, input_label, plt.gca())
        plt.title(f"Mask {i + 1}, Score: {score:.3f}", fontsize=18)
        plt.axis('off')
        plt.show()
    return foot_mask


def searchImgCoords(filename,df):
    row = df.loc[df['Filename'] == filename]
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


def initSam():
    # Initialize SAM model
    model_type = "vit_b"
    checkp_path = os.path.join(ROOT_DIR, "models/checkpoints/sam_vit_b_01ec64.pth")
    sam = sam_model_registry[model_type](checkpoint=checkp_path)
    return SamPredictor(sam)
