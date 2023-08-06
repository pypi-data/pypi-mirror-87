
from moviepy.editor import *
from moviepy.video.fx import loop, mask_color
from bgeditor.common.utils import cache_file, download_file, upload_file
from bgeditor.dao.Lyric import Lyric
from bgeditor.dao.Matrix import Matrix
from PIL import Image
import numpy as np
import requests, time
from bgeditor.dao.FFmpeg import create_suource_can_loop_path, create_loop, create_loop_audio
from proglog import ProgressBarLogger
class MyBarLogger(ProgressBarLogger):
    def __init__(self,job_id):
      self.is_final_vid=False
      self.old_index_frame=0
      self.start_count_time_30=0
      self.job_id=job_id
      self.MF_SERVER= "http://api-magicframe.automusic.win/"
      super().__init__()

    def update_progress(self, total, index, rate):
        try:
            if "error" in requests.get(self.MF_SERVER + "job/progress/%s/%s/%s/%s" %
                         (str(self.job_id), str(total), str(index), str(rate))).text:
                return False
        except:
            pass
        return True
    def callback(self, **changes):
        # Every time the logger is updated, this function is called with
        # the `changes` dictionnary of the form `parameter: new value`.
        for (parameter, new_value) in changes.items():
            if "final-vid" in new_value and "Writing video" in new_value:
              self.is_final_vid=True
              self.old_index_frame = 0
              self.start_count_time_30= time.time()
              print("Start Render main Video")
              self.update_progress(999, 999, 999)
            print ('Parameter %s is now %s' % (parameter, new_value))
    def bars_callback(self, bar, attr, value, old_value):
        if self.is_final_vid:
          if time.time() - self.start_count_time_30 > 30:
            rate = (self.bars[bar]['index']-self.old_index_frame)/30
            self.old_index_frame= self.bars[bar]['index']
            print("Speed: "+str(rate))
            self.update_progress(self.bars[bar]['total'], self.bars[bar]['index'], rate)
            self.start_count_time_30= time.time()

def create_video(list_comp_data, path_video, job_id):
    print('get list')
    arr_comps=[]
    for comp_data in list_comp_data:
        arr_comps.append(Component.convert(comp_data))
    arr_comps.sort(key=lambda obj: obj.index)
    arr_composite = []
    max_duration = 0
    for comp in arr_comps:
        if comp.type == "element":
            #audio_tmp = CompositeVideoClip(arr_composite.copy()).audio
            comp.set_bg_clip(CompositeVideoClip(arr_composite.copy()))
            #arr_composite = [comp.make().set_audio(audio_tmp)]
            arr_composite = [comp.make()]
        else:
            arr_composite.append(comp.make())
        if comp.duration + comp.start_time > max_duration:
            max_duration = comp.duration + comp.start_time
    logger = MyBarLogger(job_id)
    CompositeVideoClip(arr_composite).subclip(0, max_duration).write_videofile(path_video, fps=24, codec='libx264', logger=logger)


class Component:
    def __init__(self, json_data):
        self.index = json_data['index']
        self.position = json_data['position']
        self.start_time = json_data['startTime']
        self.duration = json_data['duration']
        self.audio_url = json_data['audio_url']
        self.audio_ext = json_data['audio_ext']
        self.audio_loop= json_data['audio_loop']
        self.type = json_data['type']
        print("init")
    @staticmethod
    def convert(json_data):
        if json_data['type'] == "text":
            return TextComp(json_data)
        if json_data['type'] == "image":
            return ImageComp(json_data)
        if json_data['type'] == "video":
            return VideoComp(json_data)
        if json_data['type'] == "lyric":
            return LyricComp(json_data)
        if json_data['type'] == "element":
            return ElementComp(json_data)
    def setup(self):
        print('setup')
    def order(self):
        print('order')
    def get_clip(self):
        print('get clip')
    def set_bg_clip(self,bg_clip):
        print('set bg clip')
    def get_audio(self):
        self.audio_path=None
        self.audio_moviepy=None
        if self.audio_url and self.audio_ext:
            self.audio_path = download_file(self.audio_url, ext=self.audio_ext)
            if self.audio_loop:
                self.audio_path = create_loop_audio(self.audio_path, self.duration)
            self.audio_moviepy = AudioFileClip(self.audio_path)

    def make(self):
        self.get_audio()
        rs = self.get_clip()
        if self.audio_moviepy:
           rs = rs.set_audio(self.audio_moviepy)
        if self.type !='element':
            rs = rs.set_position((self.position['x'], self.position['y']))
        if self.duration > 0:
            rs = rs.set_duration(self.duration).crossfadeout(0.5)
        if self.duration > 0 and self.start_time > 0:
            rs = rs.set_start(self.start_time).crossfadein(0.5)
        if self.duration < 0 and self.start_time > 0:
            rs = rs.set_duration(1200).set_start(self.start_time).crossfadein(0.5)
        if self.type !='element' and self.position['rotation'] != 0:
            rs = rs.rotate(self.position['rotation'])
        return rs


class ElementComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.rate_summon = json_data['rate_summon']
        self.arr_summon_template =  json_data['arr_summon_template']
        self.arr_direction =  np.array(json_data['arr_direction'])
        self.rang_locx =  np.array(json_data['rang_locx'])
        self.rang_locy =  np.array(json_data['rang_locy'])
        self.rang_speedx = np.array(json_data['rang_speedx'])*2
        self.rang_speedy = np.array(json_data['rang_speedy'])*2
        self.rang_opacity =  np.array(json_data['rang_opacity'])
        self.rang_size =  np.array(json_data['rang_size'])
        self.delay= json_data['delay']
        self.arr_color = json_data['arr_color']
        self.bg_clip= None
        self.arr_local_template=[]
    def set_bg_clip(self,bg_clip):
        self.bg_clip=bg_clip
    def cache_summon(self):
        for template in self.arr_summon_template:
            self.arr_local_template.append(cache_file(template))
    def get_clip(self):
        self.cache_summon()
        matrix = Matrix (self.bg_clip, self.rate_summon,  self.arr_local_template, self.arr_direction, self.rang_locx,
                         self.rang_locy,self.rang_speedx ,self.rang_speedy , self.rang_opacity, self.rang_size, self.arr_color, self.delay)
        matrix.setup()
        rs = matrix.make()
        return rs

class TextComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        self.bg_color = json_data['backgroundColor']
        if self.bg_color is None or self.bg_color == "":
            self.bg_color="transparent"
        self.color = json_data['color']
        self.text = json_data['text']
        self.stroke_color = json_data['stroke_color']
        self.stroke_width = json_data['stroke_width']

    def get_clip(self):
        self.font_path = cache_file(self.font_url)
        rs = TextClip(txt=self.text, font = self.font_path, fontsize=self.font_size, color=self.color,
                        bg_color = self.bg_color, #size=(self.position['width'], self.position['height']),
                        stroke_color = self.stroke_color, stroke_width=self.stroke_width)
        return rs



class ImageComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.image_url = json_data['image_url']
        self.ext = json_data['ext']
        self.isMask = json_data['isMask']
        self.maskColor = json_data['maskColor']
        self.opacity = json_data['opacity']
    def get_clip(self):
        self.image_path = download_file(self.image_url, ext=self.ext)
        im = Image.open(self.image_path)

        width, height = im.size
        if width != self.position['width'] or height != self.position['height']:
            im1 = im.resize((self.position['width'], self.position['height']))
            rs = ImageClip(np.asarray(im1))
        else:
            rs = ImageClip(self.image_path)
        if self.isMask:
            rs = mask_color.mask_color(rs, self.maskColor)
        if self.opacity < 1.0:
            rs = rs.set_opacity(self.opacity)
        return rs


class VideoComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.video_url = json_data['video_url']
        self.ext = json_data['ext']
        self.isMute = json_data['isMute']
        self.isLoop = json_data['isLoop']
        self.isMask = json_data['isMask']
        self.maskColor = json_data['maskColor']
        self.md5 = json_data['md5']
        self.opacity = json_data['opacity']
        self.is_canva = json_data['isCanva']
        self.kind = "video"
        if self.is_canva:
            self.kind = "canva"
    def get_clip(self):
        if self.isLoop and self.ext != "gif":
            obj = requests.get("http://api-magicframe.automusic.win/resource/get-md5/"+self.kind+"/"+self.md5).json()
            if "id" in obj:
                if "loop_link" in obj and obj['loop_link'] is not None and "gdrive" in obj['loop_link']:
                    self.video_path = download_file(obj['loop_link'], ext=self.ext)
                else:
                    self.video_path = download_file(self.video_url, ext=self.ext)
                    path_loop = create_suource_can_loop_path(self.video_path, True, ext=self.ext)
                    if path_loop is None:
                        raise Exception(" Error create source loop")
                    else:
                        drive_id = upload_file(path_loop)
                    requests.get("http://api-magicframe.automusic.win/resource/set-md5/"+self.kind+"/" + self.md5+"/"+ drive_id)
                    self.video_path = path_loop
        else:
            self.video_path = download_file(self.video_url, ext=self.ext)

        rs = VideoFileClip(self.video_path, audio=not self.isMute)
        if (self.index == 0 or self.isLoop) and rs.duration < 1200: #max 20 mins loop
            rs.close()
            self.video_path = create_loop(self.video_path, 1200)
        rs = VideoFileClip(self.video_path, audio=not self.isMute)
        if self.isMask:
            rs = mask_color.mask_color(rs, self.maskColor, thr=30, s=3)
        if self.opacity < 1.0:
            rs = rs.set_opacity(self.opacity)
        w, h = rs.size
        if self.position['width'] != w or self.position['height'] != h:
            rs = rs.resize((self.position['width'], self.position['height']))
        return rs


class LyricComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        self.bg_color = json_data['backgroundColor']
        if self.bg_color is None or self.bg_color == "":
            self.bg_color="transparent"
        self.color = json_data['color']
        self.stroke_color = json_data['stroke_color']
        self.stroke_width = json_data['stroke_width']
        self.audio_url = json_data['audio_url']
        self.audio_ext = json_data['audio_ext']
        self.lyric_sync = json_data['lyric_sync']
        self.wrap_width = json_data['wrap_width']
        self.lyric_moving = json_data['lyric_moving']
        self.fade_in = json_data['fade_in']
        self.fade_out = json_data['fade_out']

    def get_clip(self):
        self.lyric = Lyric(self.lyric_sync, self.font_url, self.font_size, self.color,
                           self.audio_moviepy.duration, self.stroke_color, self.stroke_width, self.bg_color,
                           self.lyric_moving, self.fade_in, self.fade_out, self.wrap_width, self.position['width'], self.position['height'])
        self.duration = self.audio_moviepy.duration
        self.lyric.init()
        self.lyric.optimize_font()
        return self.lyric.make()
