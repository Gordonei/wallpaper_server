# README
Intended as an accompaniment to [RandomWallpaperGnome3](https://github.com/ifl0w/RandomWallpaperGnome3), this micro-ish
service serves up the wallpaper images from a local directory.

Currently it will resize images on the fly, as well as add a border to the image that is the mean colour in the image.

# Use
## Wallpaper Server
### Docker
As simple as:
```bash
docker run \
  -p <Port on host machine>:5000 \
  -v <Path to directory of backgrounds>:/data/backgrounds \
  --detach --restart always \
  --name wallpaper_server \
  gordonei/wallpaper_server:latest
```
### Directly
1. Change to this directory.
2. Install python dependencies: `pip3 install -r requirements.txt`
3. Run the service `PYTHONPATH=. python3 wallpaper_server/server.py`

**NB** this will serve up to any host that contacts it on port `5000`.

## Random Wallpaper Settings
1. Open the `Settings` menu, go to the `Wallpaper Sources` table.
2. Fill in the following settings:
    1. Select the `Generc JSON` option from the drop down menu.
    2. Make the `Request URL` field `http://127.0.0.1:<port on host machine>/?resolution=<desired resolution, e.g. 3840x2160>`
    3. Make the `JSON Path` field `$.backgrounds[@random]`
    4. Make the `Image URL prefix` field `http://127.0.0.1:<port on host machine>/backgrounds/`