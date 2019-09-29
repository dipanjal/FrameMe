import cv2
import pathlib
import os
import argparse
import re
from moviepy.editor import *
from PIL import Image


class Framer:
    EXTRACT_IMAGE_FROM_VIDEO = 1
    SAVE_AS_GIF = 2

    output_fixed_path = os.path.join(os.getcwd(), 'output')

    def extract_frame_from_video(self, video_path, output_path, frame2skip=0):
        try:
            vid_file_dir = pathlib.Path(video_path).name.split('.')[0]
            output_path = os.path.join(self.output_fixed_path, vid_file_dir)
            pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

            vidcap = cv2.VideoCapture(video_path)
            success, image = vidcap.read()
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            totalframes = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

            frame2skip = 50  # num of frames to skip when extracting
            outputframe = int(totalframes / frame2skip) if frame2skip > 0 else totalframes

            print('Video FPS rate is {}'.format(fps))
            print('You will get {} frames in total'.format(outputframe))

            while success:
                frameId = int(round(vidcap.get(1)))
                success, image = vidcap.read()
                file_path_to_save = os.path.join(output_path, 'frame_%d.jpg' % frameId)
                if frame2skip > 0 and frameId % frame2skip == 0:
                    cv2.imwrite(file_path_to_save, image)
                else:
                    cv2.imwrite(file_path_to_save, image)
                print('Export frame {}: '.format(frameId), success)

            vidcap.release()
            print('Extraction completed!')

        except Exception:
            print(Exception.args)

    def is_file_valid(self, path):
        file_validation_regex = re.compile(r'^(\.\/|\/)?(\/?[A-Za-z]+)*[A-Za-z]+\.mp4$')
        if file_validation_regex.match(path):
            return True
        else:
            print('invalid file path')
            return False

    def make_gif_from_video(self, video_path, start_time, end_time):
        if self.is_file_valid(video_path):
            cwd = os.getcwd()
            vid_file_dir = pathlib.Path(video_path).name.split('.')[0]
            output_path = os.path.join(self.output_fixed_path, vid_file_dir)
            pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
            subclip = VideoFileClip(video_path).subclip(start_time, end_time)
            # os.chdir(output_path)
            gif_file_name = vid_file_dir+".gif"
            gif_file_path = os.path.join(output_path, gif_file_name)
            subclip.write_gif(gif_file_path)
            # os.chdir(cwd)

    def extract_frame_with_moviepy(self, video_path, start_time, end_time):
        if self.is_file_valid(video_path):
            vid_file_dir = pathlib.Path(video_path).name.split('.')[0]
            output_path = os.path.join(self.output_fixed_path, vid_file_dir)
            pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
            myclip = VideoFileClip(video_path).subclip(start_time, end_time)

            i = 1
            for frame in myclip.iter_frames():
                file_path_to_save = os.path.join(output_path, 'frame_%d.jpg' % i)
                image = Image.fromarray(frame)
                print('saving', file_path_to_save)
                image.save(file_path_to_save)
                i = i + 1

    def __init__(self):
        # taking args from cli
        parser = argparse.ArgumentParser(prog='python3 framer.py', usage='%(prog)s [-i|-g]')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-i', '--image', nargs='?', const='action_extract_image', action='store',
                           help='extract frame from video')
        group.add_argument('-g', '--gif', nargs='?', const='action_extract_image', action='store',
                           help='make gif from video clip')
        parser.add_argument('-t', '--time', nargs='?', const='start,end', action='store',
                            help='video frame duration')

        # parser.add_argument('-o', '--out', nargs='?', const='out_file_path', action='store',
        #                     help='video source file path')
        # parser.add_argument('-n', '--skip', nargs='?', const='skip_frame', action='store', help='skip number of frames')

        args = parser.parse_args()

        time_array = args.time.split(',') if args.time else '0,0'.split(',')
        start_time = int(time_array[0])
        end_time = int(time_array[1])
        if args.image:
            print("extract image")
            self.extract_frame_with_moviepy(args.image, start_time, end_time)
        else:
            print("make gif")
            self.make_gif_from_video(args.gif, start_time, end_time)


Framer()
