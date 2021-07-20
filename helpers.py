import gcsfs
from fsspec.implementations.local import LocalFileSystem
from pangeo_forge_recipes.storage import MetadataTarget, CacheFSSpecTarget


def setup_logging():
    import logging
    import sys
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("pangeo_forge_recipes")
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)


def setup_targets(recipe, cache):
    """
    Parameters
    ----------
    recipe: dict
        A single-entry dictionary mapping a string key to an
        instance of pangeo_forge_recipes.recipes.XarrayZarrRecipe
    cache: str
        Cache filesystem; one of "local" or "cloud"

    Returns
    -------
    XarrayZarrRecipe
    """
    fs_local = LocalFileSystem()
    cache_fs = fs_local if cache == "local" else gcsfs.GCSFileSystem(anon=True,)
    cache_base = (
        "input_cache" if cache == "local" else "gs://pangeo-forge-us-central1/pangeo-forge-cache"
    )

    key = [k for k in recipe.keys()][0]
    rec = recipe[key]

    rec.input_cache = CacheFSSpecTarget(cache_fs, f"{cache_base}/{key}")
    rec.target = MetadataTarget(fs_local, f"zarr_build/{key}.zarr")

    print(f"""Targets for recipe "{key}" set to:
    input_cache: {rec.input_cache.root_path}
    target: {rec.target.root_path}
    """)

    return rec
