# author:	prof. Anatoly Postolit
# e-mail:	anat_post@ mail.ru

# set the version number
__version__ = "0.0.7"
# Changing the image size % # Изменение размера изображения в %
from .postolit import resize_percent

# Changing only the image width # Изменение только ширины изображения
from .postolit import resize_width

# Changing only the image height # Изменение только высоты изображения
from .postolit import resize_height

# Changing the image width, height # Изменение ширины и высоты изображения
from .postolit import resize_wh

# Image to grayscale # Изображение в градациях серого
from .postolit import gray_image

# Image to black # Черно-белое изображение
from .postolit import black_image

# Rotation by a specified angle while preserving the frame size
# Вращение изображения на заданный угол с сохранением размеров кадра
from .postolit import rotate_image_fs

# Rotation by a specified angle with image size preserved
# Вращение изображения на заданный угол с сохранением размера изображения
from .postolit import rotate_image_is

# The detection of boundary edges of the image # Обнаружение границы края изображения
from .postolit import canny_edge_detector

# Image segmentation # Сегментация изображений
from .postolit import segment_image

# Creating parameters for recording a video file
# Формирование параметров для записи видео файла
from .postolit import get_video_param

# Setting parameters for changing the frame size of a video file#
# Задание параметров для изменения зармера кадра видео файла
from .postolit import set_video_param

# line detector # детектор линий
from .postolit import line_detect
