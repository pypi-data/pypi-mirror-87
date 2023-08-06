import os
#os.environ["IMAGEMAGICK_BINARY"] = "magick"
import uuid
from bgeditor.dao.FFmpeg import create_source_can_loop, create_loop
from bgeditor.dao.Lyric import Lyric
from bgeditor.common.utils import download_file
import tempfile
from bgeditor.dao.Component import create_video

class BGEditor():
    def __init__(self):
        self.root_dir = tempfile.TemporaryDirectory()

    def create_source_can_loop_by_file(self, ori_file, is_delete=True):
        if ori_file:
            path_loop = create_source_can_loop(self.root_dir.name, ori_file, is_delete)
            return path_loop
        else:
            return None

    def download_video(self, url):
        return download_file(url, self.root_dir.name)


    def loop_video(self, ori_file, duration, can_loopable):
        return create_loop(ori_file, duration, can_loopable)


    def create_lyric_bg_video(self, lyric_data, font_url, font_size, color, duration, is_optimize= False, w=1920, h=1080):
        lyric = Lyric(lyric_data, font_url, font_size, color, duration, w, h)
        if lyric.init():
            if is_optimize:
                lyric.optimize_font()
            return lyric.make()
        return None

    def create_video_json(self, list_comp_data,job_id):
        path_vid = self.root_dir.name + "/final-vid-" + str(uuid.uuid4()) + ".avi"
        create_video(list_comp_data, path_vid, job_id)
        return path_vid

    def close(self):
        self.root_dir.cleanup()




