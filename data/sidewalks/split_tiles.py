#!/usr/bin/env python3.7

import solaris as sol
from glob import glob
from tqdm.auto import tqdm
import random

files = glob("input/*.tif")
print(f"Found {len(files)} files")

# Randomly choose 20% of tiles for validation
random.seed(1)
valid = random.sample(files, int(len(files) * 0.2))
print(f"validation ({len(valid)}/{len(files)}): {valid}")

for f in tqdm(files):
    if f in valid:
        name = "valid"
    else:
        name = "train"
    try:
        raster_tiler = sol.tile.raster_tile.RasterTiler(
            dest_dir=name,  # the directory to save images to
            src_tile_size=(700, 700),  # the size of the output chips
            verbose=False,
        )
        raster_bounds_crs = raster_tiler.tile(f)
        vector_tiler = sol.tile.vector_tile.VectorTiler(
            dest_dir=f"{name}_labels", verbose=True
        )
        vector_tiler.tile(
            "input/AKL_sidewalks.gpkg",
            tile_bounds=raster_tiler.tile_bounds,
            tile_bounds_crs=raster_bounds_crs,
        )

    except Exception as e:
        print(f"{e} for {f}, skipping")

for name in ["train", "valid"]:
    coco_dict = sol.data.coco.geojson2coco(
        name,
        f"{name}_labels",
        output_path=f"{name}_coco.json",
        matching_re=r"(\d{7}_\d{7})",
        explode_all_multipolygons=True,
        verbose=False,
    )
