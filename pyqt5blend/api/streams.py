import cv2
import numpy as np

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QImage

from .common import Time, Writer, OS, Logger

__all__ = ['VideoStream']


class VideoStream(QThread):

    status = 1

    def __init__(self, parent, callback, shape=None, fix_color=False,
                 flip=False, cache_dir=None, *args, **kwargs):

        super(VideoStream, self).__init__(*args, **kwargs)

        self.setParent(parent)

        self.change_frame = callback

        self.shape = shape
        self.fix_color = fix_color
        self.flip = flip

        self.__current_frame__ = np.empty(self.shape, order='C', dtype='float32')
        self.__cache_dir__ = cache_dir

        if not OS.dir_exists(self.__cache_dir__):

            Logger.warning('Working Directory :', OS.cwd, end='\n')
            Logger.warning('Directory doesn\'t exist :',  self.__cache_dir__, end='\n')

            OS.make_dirs(self.__cache_dir__)

        if self.shape is not None:

            self.shape = tuple(reversed(self.shape))

    def run(self):

        cap = cv2.VideoCapture(0)

        while True:

            if VideoStream.status == 1:

                ret, frame = cap.read()

                if ret:

                    image = np.array(frame.data)

                    if self.shape is not None:

                        image = cv2.resize(image, self.shape)

                    if self.fix_color:

                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    if self.flip:

                        image = cv2.flip(image, 1)

                    # cache frame
                    self.__current_frame__ = image

                    h, w, ch = image.shape
                    bytes_per_line = ch * w

                    qt_frame = QImage(image, w, h, bytes_per_line, QImage.Format_RGB888)
                    qt_frame = qt_frame.scaled(w, h, Qt.KeepAspectRatio)

                    self.change_frame(qt_frame)

            elif VideoStream.status == 0:

                cap.release()

                break

    @property
    def current_frame(self):

        return self.__current_frame__

    @property
    def cache_dir(self):

        return self.__cache_dir__

    def save_current_frame(self, to_path=None):

        cache_dir = self.__cache_dir__

        if to_path is not None:

            cache_dir = to_path

        image = cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR)

        shape = tuple(reversed(image.shape[0:2]))

        image = cv2.resize(image, shape)

        filename = 'image_' + Time.now(sep='_') + '.jpg'
        Writer.write_image(cache_dir, filename, image)

        Logger.info('Current frame has been saved :', f'{shape[0]}x{shape[1]}')

    def start(self, *args, **kwargs):

        VideoStream.status = 1

        super().start(*args, **kwargs)

    def stop(self):

        VideoStream.status = 0

        self.wait()
        self.exit()
