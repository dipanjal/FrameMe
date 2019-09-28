import cv2
import pathlib
import os
import argparse
import re


class Framer:

    output_fixed_path = os.path.join(os.getcwd(), 'output');

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


# taking args from cli
parser = argparse.ArgumentParser(prog='python3 framer.py', usage='%(prog)s [-v|-s]')
parser.add_argument('-s', '--source', nargs='?', const='source_file_path', action='store',
                    help='video source file path')
# parser.add_argument('-o', '--out', nargs='?', const='out_file_path', action='store',
#                     help='video source file path')
parser.add_argument('-n', '--skip', nargs='?', const='skip_frame', action='store', help='skip number of frames')
args = parser.parse_args()
file_validation_regex = re.compile(r'^(\.\/|\/)?(\/?[A-Za-z]+)*[A-Za-z]+\.mp4$')

if file_validation_regex.match(args.source):
    skip_frame = args.skip if args.skip else 0
    Framer().extract_frame_from_video(args.source, '', skip_frame)
else:
    print('invalid file path')
