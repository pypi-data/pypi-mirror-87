import math
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.fx import make_loopable, loop
from bgeditor.common.utils import get_dir
import uuid
import os
import shutil

def create_suource_can_loop_path(clip_path, is_delete = True, ext="mp4"):
    return create_source_can_loop(get_dir('download'), clip_path, is_delete = is_delete, ext=ext)
def create_source_can_loop(dir_path, clip_path, is_delete = True, ext = "mp4" ):
    tmp_clip_path_z_resync = None
    try:
        if dir_path.endswith("/"):
            dir_path = dir_path[:-1]
        clip = VideoFileClip(clip_path)
        clip = make_loopable.make_loopable(clip, 0.5)
        tmp_clip_path_z = dir_path + "/" + str(uuid.uuid4()) + '-' + os.path.basename(clip_path)
        tmp_clip_path_z_resync = dir_path + "/" + str(uuid.uuid4()) + '-re-sync-' + \
                                  os.path.basename(clip_path).split(".")[0] + "." + ext
        try:
            clip.write_videofile(tmp_clip_path_z, fps=clip.fps, codec='libx264')
            clip.close()
        except:
            pass
        cmd = "ffmpeg -y -i \"%s\" -c:v libx264 -crf 22 \"%s\"" % (tmp_clip_path_z, tmp_clip_path_z_resync)
        os.system(cmd)
        os.remove(tmp_clip_path_z)
        if is_delete:
            os.remove(clip_path)
        try:
            clip = VideoFileClip(tmp_clip_path_z_resync)
            if clip.duration is None or clip.duration < 0.1:
                tmp_clip_path_z_resync = None
        except:
            tmp_clip_path_z_resync = None
            pass
    except:
        pass
    return tmp_clip_path_z_resync

def create_loop_audio(audio_path, loop_duration):
    if loop_duration < 0 : loop_duration = 1200
    try:
        audio_clip = AudioFileClip(audio_path)
        clip_duration = audio_clip.duration
        audio_clip.close()
        if clip_duration > loop_duration:
            return audio_path
        tmp_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-' + os.path.basename(audio_path)
        shutil.copyfile(audio_path, tmp_clip_path)
        times = int(math.ceil(loop_duration / clip_duration))
        file_merg_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4())
        final_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-final-' + os.path.basename(audio_path)
        file_merg = open(file_merg_path, "a")
        for i in range(times):
            file_merg.write("file '%s'\n" % os.path.basename(tmp_clip_path))
        file_merg.close()
        cmd = "ffmpeg -y -f concat -safe 0 -i \"%s\" -codec copy \"%s\"" % (file_merg_path, final_clip_path)
        os.system(cmd)
        os.remove(tmp_clip_path)
        os.remove(file_merg_path)
        clip = AudioFileClip(final_clip_path)
        clip_duration = clip.duration
        clip.close()
        if clip_duration < loop_duration:
            return None
        return final_clip_path
    except:
        pass
    return None
def create_loop(clip_path, loop_duration, can_loopable = True):
    try:
        clip = VideoFileClip(clip_path)
        if not can_loopable:
            try:
                if clip.duration > loop_duration:
                    return clip_path
                clip = make_loopable.make_loopable(clip, 0.5)
                tmp_clip_path_z = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-' + os.path.basename(clip_path)
                #tmp_clip_path_z_resync = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-re-sync-' + os.path.basename(clip_path).split(".")[0]+".avi"
                clip.write_videofile(tmp_clip_path_z, fps=clip.fps, codec='libx264')
                clip.close()
                # cmd = "ffmpeg -y -i \"%s\" \"%s\"" % (tmp_clip_path_z, tmp_clip_path_z_resync)
                # os.system(cmd)
                # os.remove(tmp_clip_path_z)
                clip = VideoFileClip(tmp_clip_path_z)
                tmp_clip_path = tmp_clip_path_z
            except:
                pass
        else:
            tmp_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-' + os.path.basename(clip_path)
            shutil.copyfile(clip_path, tmp_clip_path)

        clip_duration = clip.duration
        clip.close()
        if clip_duration > loop_duration:
            return clip_path
        times = int(math.ceil(loop_duration / clip_duration))
        file_merg_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4())
        final_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-final-' + os.path.basename(clip_path)
        file_merg = open(file_merg_path, "a")
        for i in range(times):
            file_merg.write("file '%s'\n" % os.path.basename(tmp_clip_path))
        file_merg.close()
        cmd = "ffmpeg -y -f concat -safe 0 -i \"%s\" -codec copy \"%s\"" % (file_merg_path, final_clip_path)
        os.system(cmd)
        os.remove(tmp_clip_path)
        os.remove(file_merg_path)
        clip = VideoFileClip(final_clip_path)
        clip_duration = clip.duration
        clip.close()
        if clip_duration < loop_duration:
            return None
        return final_clip_path
    except:
        return None
