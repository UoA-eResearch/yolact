#!/usr/bin/env python3.7

import solaris as sol

train_test = {
    "train": "input/BA32_3703.tif",
    "valid": "input/BA32_3603.tif"
}

for k, v in train_test.items():
    raster_tiler = sol.tile.raster_tile.RasterTiler(
        dest_dir=k,  # the directory to save images to
        src_tile_size=(700, 700),  # the size of the output chips
        verbose=True,
    )
    raster_bounds_crs = raster_tiler.tile(v)
    print(raster_bounds_crs)

    vector_tiler = sol.tile.vector_tile.VectorTiler(dest_dir=f"{k}_labels", verbose=True)
    vector_tiler.tile(
        "input/AKL_sidewalks.gpkg",
        tile_bounds=raster_tiler.tile_bounds,
        tile_bounds_crs=raster_bounds_crs,
    )

    coco_dict = sol.data.coco.geojson2coco(
        k,
        f"{k}_labels",
        output_path=f"{k}_coco.json",
        matching_re=r"(\d{7}_\d{7})",
        verbose=True,
        explode_all_multipolygons=True,
    )
