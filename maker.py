from tkinter import Tk
from tkinter.ttk import Combobox
from tkinter import filedialog, Button, Entry, Label

import imageio
from moviepy.editor import VideoFileClip
from PIL import Image
from skimage.transform import resize

from glob import glob
import os

#pyinstall audio_fadein 관련 오류
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
#pyinstall video / crop 관련 오류
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

def image_opener():
    img = filedialog.askopenfilenames(filetypes=[('images', '*.jpg;*.jpeg;*.png'), ('any file', '*.*')], initialdir='./source/')

    image2gif(img)
def video_opener():
    img = filedialog.askopenfilename(filetypes=[('video', '*.mp4'), ('any file', '*.*')], initialdir='./source/')

    video2gif(img)

def image2gif(img):
    save_name = output_name.get()

    scale_sel = image_sclae.get()
    frame = image_fps.get()
    features = {'duration':frame}

    scale = []
    for file_name in img:
        reading = imageio.imread(file_name)
        #print(reading.shape[0], ', ', reading.shape[1])
        scale.append([reading.shape[0], reading.shape[1]])


    max_scale = max(scale)
    min_scale = min(scale)
    #print(max_scale)
    #print(min_scale)


    images = []
    if scale_sel == 'max':
        for file_name in img:
            reading = imageio.imread(file_name)
            resized = resize(reading, (max_scale[0], max_scale[1]))
            images.append(resized)
    if scale_sel == 'min':
        for file_name in img:
            reading = imageio.imread(file_name)
            resized = resize(reading, (min_scale[0], min_scale[1]))
            images.append(resized)

    imageio.mimsave('./output/{}&img={}.gif'.format(save_name, len(img)), images, **features)

    print('all done!')
    done1 = Label(window, text='done!')
    done1.grid(row=6, column=2)


def video2gif(vid):
    save_name = output_name.get()

    clip = VideoFileClip(vid).subclip(vid_btw_str.get(), vid_btw_stp.get())#sec

    duration = int(clip.duration)
    if vid_fps.get() == 'fps':
        frames = round(clip.fps)
    else:
        frames = round(int(vid_fps.get()))

    for i in range(0, duration*round(frames)):      #임시 프레임 이미지 생성
        frame = clip.get_frame(i/frames)
        fps = Image.fromarray(frame)
        if i < 10:                                  #glob에서 1, 10, 11, 2.. 순서로 읽어서 00을 추가
            ii = '000' + str(i)
        elif i < 100:
            ii = '00' + str(i)
        elif i < 1000:
            ii = '0' + str(i)

        fps.save('./dodo/' + ii + '.jpg')

    print('extraction done!')
    done1 = Label(window, text='extraction')
    done1.grid(row=6, column=2)
    done1_1 = Label(window, text='done!')
    done1_1.grid(row=6, column=3)

    dodo = glob('./dodo/*')                         #임시 저장된 프레임 이미지로 gif 생성

    frame_rate = 1/frames

    features = {'duration':frame_rate}
    images = []
    for file_name in dodo:
        reading = imageio.imread(file_name)
        images.append(reading)

    imageio.mimsave('./output/{}&fps={}.gif'.format(save_name, frames), images, **features)

    print('conversion done!')
    done2 = Label(window, text='conversion')
    done2.grid(row=7, column=2)
    done2_1 = Label(window, text='done!')
    done2_1.grid(row=7, column=3)

    to_delet = glob('./dodo/*')                     #임시 프레임 이미지 삭제
    for fi in to_delet:
        os.remove(fi)

    print('cleaning done!')
    done3 = Label(window, text='cleaning')
    done3.grid(row=8, column=2)
    done3_1 = Label(window, text='done!')
    done3_1.grid(row=8, column=3)


window = Tk()
window.title('GIF Maker 1.0.0')
window.geometry('350x250+150+150')
window.resizable(False, False)
window.iconbitmap('./icon.ico')


output_lbl = Label(window, text='output name : ')
output_lbl.grid(row=0, column=0, columnspan=2)
output_name = Entry(window, width=20)
output_name.insert(0, 'output')
output_name.grid(row=0, column=2, columnspan=5)

img_lbl = Label(window, text='--image2gif--')
img_lbl.grid(row=1, column=0, columnspan=2)
image_fps_lbl = Label(window, text='fps : ')
image_fps_lbl.grid(row=2, column=0)
image_fps = Combobox(window, values=[0.1, 0.2, 0.5, 0.8, 1.0, 2.0], width=5)
image_fps.current(2)
image_fps.grid(row=2, column=1)
image_scale_lbl = Label(window, text='scale : ')
image_scale_lbl.grid(row=2, column=2)
image_sclae = Combobox(window, values=['max', 'min'], width=10)
image_sclae.current(0)
image_sclae.grid(row=2, column=3, columnspan=3)
img_btn = Button(text='Open and Gif', command=image_opener, width=10)
img_btn.grid(row=2, column=7)

vid_lbl = Label(window, text='--video2gif--')
vid_lbl.grid(row=3, column=0, columnspan=2)
vid_fps_lbl = Label(window, text='fps : ')
vid_fps_lbl.grid(row=4, column=0)
vid_fps = Combobox(window, values=['fps', 20, 12, 10, 6, 5, 3], width=5)
vid_fps.current(0)
vid_fps.grid(row=4, column=1)
vid_btw_label = Label(window, text='section : ')
vid_btw_label.grid(row=4, column=2)
vid_btw_str = Entry(window, width=5)
vid_btw_str.grid(row=4, column=3)
vid_btw_ = Label(window, text='~')
vid_btw_.grid(row=4, column=4)
vid_btw_stp = Entry(window, width=5)
vid_btw_stp.grid(row=4, column=5)
vid_btw_unit = Label(window, text='[sec]')
vid_btw_unit.grid(row=5, column=5)
vid_btn = Button(window, text='Open and Gif', command=video_opener, width=10)
vid_btw_str.insert(0, 0)
vid_btw_stp.insert(0, 30)
vid_btn.grid(row=4, column=7)


window.mainloop()