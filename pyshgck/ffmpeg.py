""" Interface for using some FFmpeg utilities. Requires a FFmpeg bin. """

import os.path
import subprocess
import tempfile


class FfmpegApi(object):
    """ FFmpeg interface. Requires a FFmpeg bin to use; if FFmpeg is in your
    PATH, providing "ffmpeg" as the ffmpeg_bin argument will do it. """

    FILTERS       = "fps={fps},scale={scale}:-1:flags=lanczos"
    DEFAULT_FPS   = 15
    DEFAULT_SCALE = 320

    def __init__(self, ffmpeg_bin):
        self.bin = ffmpeg_bin

    def version(self):
        """ Call FFmpeg to print version informations. """
        version_command = [self.bin, "-version"]
        subprocess.call(version_command)

    def convert_video_to_gif(self, video_path, gif_path,
            fps = None, scale = None):
        """ Convert the provided video into a good quality GIF. Return True on
        presumable success. """
        if fps is None:
            fps = FfmpegApi.DEFAULT_FPS
        if scale is None:
            scale = FfmpegApi.DEFAULT_SCALE

        filters = FfmpegApi.FILTERS.format(fps = fps, scale = scale)
        with tempfile.TemporaryDirectory() as temp_dir:
            palette_path = self._v2g_create_palette( video_path, temp_dir
                                                   , filters )
            if not os.path.isfile(palette_path):
                print("Couldn't locate created palette.")
                return False

            self._v2g_gen_gif(video_path, palette_path, filters, gif_path)
            if not os.path.isfile(gif_path):
                print("Couldn't locate created GIF.")
                return False

        return True

    def _v2g_create_palette(self, video_path, temp_dir, filters):
        palette_path = os.path.join(temp_dir, "palette.png")
        video_filters = "{},palettegen".format(filters)
        palette_command = [ self.bin, "-i", video_path
                          , "-vf", video_filters
                          , "-y"
                          , palette_path ]
        subprocess.call(palette_command)
        return palette_path

    def _v2g_gen_gif(self, video_path, palette_path, filters, gif_path):
        filtergraph = "{} [x]; [x][1:v] paletteuse".format(filters)
        convert_command = [ self.bin, "-i", video_path, "-i", palette_path
                          , "-lavfi", filtergraph
                          , "-y"
                          , gif_path ]
        subprocess.call(convert_command)
