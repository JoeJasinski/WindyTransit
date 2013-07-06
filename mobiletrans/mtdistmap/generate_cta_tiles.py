from mobiletrans.mtdistmap.utils import generate_tiles_multiprocess, generate_tiles
from mobiletrans.mtdistmap.cta_heatmap import CTAHeatmap
import mapnik

m = mapnik.Map(256,256)
cta_map = CTAHeatmap(m)


bbox = (-87.749176, 42.019203, -87.528419, 41.723412,)
generate_tiles.render_tiles(bbox, cta_map.map, 'out/', 11,13, 'CTA_HEAT')