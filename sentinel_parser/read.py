from datetime import timedelta
from random import shuffle

import shapefile
from matplotlib.path import Path
from pyproj import Transformer
from sentinelhub import CRS, BBox, bbox_to_dimensions, SentinelHubRequest, DataSource, MimeType, SHConfig, WmsRequest
import numpy as np
import datetime as dt
from PIL import Image, ImageDraw
from tqdm import tqdm
import matplotlib.pyplot as plt

transformer = Transformer.from_proj('epsg:32640', 'epsg:4326')

config = SHConfig()
config.instance_id = "fd2116de-b567-4cdc-902f-e77d22f06a5e"

resolution = 10


def plot_image(image, factor=1):
    """
    Utility function for plotting RGB images.
    """
    fig = plt.subplots(nrows=1, ncols=1)

    if np.issubdtype(image.dtype, np.floating):
        plt.imshow(np.minimum(image * factor, 1))
    else:
        plt.imshow(image)
    plt.show()


def get_image(coords_wgs84, size, history_search, date):
    date_string = date.strftime("%d-%m-%Y")
    bbox = BBox(bbox=coords_wgs84, crs=CRS.WGS84)
    wms_request = WmsRequest(
        layer='HVOSTCH',
        bbox=bbox,
        time=date_string,
        width=size[0],
        height=size[1],
        config=config
    )
    wms_img = wms_request.get_data()
    if len(wms_img) == 0 and history_search > 0:
        return get_image(coords_wgs84, size, history_search - 1, date - timedelta(days=9))
    wms_img = wms_img[-1]
    return wms_img[:][:size[1]]


def transform_points(bbox, size, points):
    xmin, ymin, xmax, ymax = bbox
    for x, y in points:
        x, y = transformer.transform(x, y)
        yield (max(0, min(size[0] - 1, round(size[0] * (x - xmin) / (xmax - xmin)))),
               max(0, min(size[1] - 1, round(size[1] * (y - ymin) / (ymax - ymin)))))


def get_bbox(points):
    for i in range(len(points)):
        x, y = points[i]
        points[i] = transformer.transform(x, y)

    x_min = points[0][0]
    x_max = points[0][0]

    y_min = points[0][1]
    y_max = points[0][1]

    for x, y in points:
        x_min = min(x_min, x)
        x_max = max(x_max, x)

        y_min = min(y_min, y)
        y_max = max(y_max, y)

    return x_min, y_min, x_max, y_max


if __name__ == '__main__':
    sf = shapefile.Reader("maps/Поля_Полигональные2")

    polygons = []
    cnt = 0
    recs = list(sf.iterShapeRecords())
    for shapeRecord in tqdm(recs):
        points = shapeRecord.shape.points
        bbox = (*transformer.transform(*shapeRecord.shape.bbox[2:]),
                 *transformer.transform(*shapeRecord.shape.bbox[:2]))
        # print(bbox)
        # print(bbox[0] - bbox[2], bbox[1] - bbox[3])
        betsiboka_bbox = BBox(bbox=bbox, crs=CRS.WGS84)
        betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

        polygon = tuple(transform_points(betsiboka_bbox, betsiboka_size, points))

        width, height = betsiboka_size

        if not width > 1000 and not height > 1000:
            continue

        img = Image.new('L', (width, height), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)

        # w * h
        mask = np.array(img)
        plt.imshow(mask)
        plt.show()

        # w * h * 4
        img_map = get_image(bbox, betsiboka_size, 14, dt.datetime.now())
        plt.imshow(img_map)
        plt.show()

        result = np.expand_dims(mask, -1) * img_map
        plt.imshow(result)
        plt.show()
