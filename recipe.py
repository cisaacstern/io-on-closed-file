from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.recipes import XarrayZarrRecipe

base = "https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access"

date = "1981-09-01".replace("-", "")

urls = [base + f"/avhrr/{date[:6]}/oisst-avhrr-v02r01.{date}.nc" for i in range(2)]

pattern = pattern_from_file_sequence(urls, "time", nitems_per_file=1)

recipe = XarrayZarrRecipe(pattern, target_chunks={"time": 2})
