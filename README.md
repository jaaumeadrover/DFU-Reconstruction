# 3D Reconstruction Pipeline for Diabetic Foot Ulcers

Jaume Adrover, Gabriel Moyá Alcover, José Maria Buades Rubio <br>
| [Docs](https://drive.google.com/file/d/1XTKcYXGFRgXhViSaoBWs7K-M7ZZwXTqp) | [Slides](https://docs.google.com/presentation/d/1_hLQ0bMLR88pabbE2PtKA5lz87QHIZISnBW6guoPzoc) |

An end-to-end 3D reconstruction pipeline for diabetic foot ulcers (DFU), built from Intel
RealSense recordings. It turns a raw `.bag` recording of a patient's foot into a cropped,
registered point cloud centered on the wound, ready for surface reconstruction.

## Pipeline overview

The pipeline runs as a sequence of standalone stages, each a script under `src/`:

1. **Preprocessing** (`src/preprocessing/bag_extraction.py`) — extracts aligned color and
   depth frames from each patient's `.bag` recordings.
2. **Annotation** (`src/annotations/image_annotation.py`) — a small Tkinter tool for manually
   clicking the ulcer location on each color frame, saved to `annotations.csv`.
3. **Segmentation** (`src/annotations/sam_cleaner.py`) — runs Meta's Segment Anything (SAM) at
   the annotated point to get a full-leg mask per frame, and uses it to zero out irrelevant
   depth pixels.
4. **Point cloud creation** (`src/preprocessing/pcd_creation.py`) — back-projects each
   color/depth pair into a point cloud and crops a 45x45x45 cm bounding box centered on the
   wound.
5. **Registration** (`src/registration/batch_integrator.py`, `src/registration/seq_fgr.py`) —
   merges consecutive per-frame point clouds into a unified point cloud using Fast Global
   Registration (FGR) and ICP refinement.
6. **Visualization** (`src/visualization/viewer.py`) — steps through the reconstructed point
   clouds of a patient in an Open3D viewer.

Surface-meshing experiments (Poisson, alpha shapes, ball pivoting) live separately in
`experiments/` — see [Repo structure](#repo-structure).

## Setup

Requires Python 3.9+ (developed against 3.9.12).

```bash
pip install -r requirements.txt
```

The pipeline also expects, outside of version control:

- `data/` at the repo root — one folder per patient (`p_XXXX/YYYY-MM-DD/...`) containing the
  `.bag` recordings and derived color/depth/point-cloud data. Not shipped with the repo
  (see `.gitignore`).
- `data/intrinsic.json` — the RealSense camera intrinsics, read by `definitions.py` at import
  time.
- `models/checkpoints/sam_vit_b_01ec64.pth` — the SAM ViT-B checkpoint, used by
  `src/utils/image.py`'s `initSam()`. Download from the
  [Segment Anything repo](https://github.com/facebookresearch/segment-anything#model-checkpoints).

## Usage

Each stage is a plain script with a `patient`/`date` (and, for registration, a config dict) set
at the top of its `if __name__ == "__main__":` block — there's no CLI, so edit those values
before running a stage for a given patient. Run stages in order, from the repo root:

```bash
python src/preprocessing/bag_extraction.py     # extract frames for all patients
python src/annotations/image_annotation.py     # click the wound location for one patient/date
python src/annotations/sam_cleaner.py          # SAM-segment depth frames for one patient/date
python src/preprocessing/pcd_creation.py       # crop point clouds around the wound
python src/registration/batch_integrator.py    # batch-merge point clouds into one
python src/visualization/viewer.py             # step through the result
```

`src/registration/seq_fgr.py` is an alternative, sequential (non-batched) registration path.

## Repo structure

```
DFU-Reconstruction/
├── definitions.py        # project-wide constants (paths, camera intrinsics)
├── requirements.txt
├── src/
│   ├── utils/             # shared library: path helpers, image/SAM helpers, FGR/ICP
│   │                       # registration, metrics, .bag frame extraction
│   ├── preprocessing/      # bag extraction, point cloud creation/cropping
│   ├── annotations/        # wound annotation tool, SAM-based leg segmentation
│   ├── registration/       # batch and sequential point cloud registration
│   └── visualization/      # point cloud viewer
└── experiments/            # standalone surface-reconstruction experiments
                             # (Poisson/alpha shapes, ball pivoting) - not wired into
                             # the main pipeline, operate on a single local .pcd file
```
