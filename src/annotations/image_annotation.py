import os
import tkinter as tk
import csv

"""
CLASS: Image Annotator
DESCRIPTION: class that displays a window so user can click in every photo from determined folder in order
to get ulcer coordinates, that will be stored in annotations.csv.
CREATION DATE: 12/04/2024
AUTHOR: Jaume Adrover Fernández
"""
class ImageAnnotator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        self.current_index = 0
        self.annotations = {}

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.load_image()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()

    def load_image(self):
        if self.current_index < len(self.image_files):
            image_path = os.path.join(self.folder_path, self.image_files[self.current_index])
            self.image = tk.PhotoImage(file=image_path)
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

if __name__ == "__main__":
    folder_path = '' # Write color photos path
    annotator = ImageAnnotator(folder_path)
    csv_file = 'annotations.csv'
    annotator.save_annotations_to_csv(csv_file)
