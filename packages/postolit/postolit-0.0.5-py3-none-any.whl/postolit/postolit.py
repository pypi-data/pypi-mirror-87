###########################################
# Design By Anatoly Postolit              #
# Doctor of technical Sciences, Professor #
# E-mail: anat_post@ mail.ru              #
##################################################
# Postoperative Library for Image Transformation #
#               PostoLIT                         #
##################################################

import os
import cv2


#####################################
# Changing the image size %         #
# Изменение размера изображения в % #
#####################################
def resize_percent(image, percent):
    width = int(image.shape[1] * percent / 100)  # пересчет ширины
    height = int(image.shape[0] * percent / 100)  # пересчет высоты
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


#######################################
# Changing only the image width       #
# Изменение только ширины изображения #
#######################################
def resize_width(image, width):
    height = image.shape[0]  # Получение оригинальной высоты
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


#######################################
# Changing only the image height      #
# Изменение только высоты изображения #
#######################################
def resize_height(image, height):
    width = image.shape[1]  # Получение оригинальной ширины
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


#########################################
# Changing the image width, height      #
# Изменение ширины и высоты изображения #
#########################################
def resize_wh(image, width, height):
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


##################################
# Image to grayscale             #
# Изображение в градациях серого #
##################################
def gray_image(image):
    gr_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gr_image


###########################
# Image to black          #
# Черно-белое изображение #
###########################
def black_image(image):
    gray = gray_image(image)
    ret, bl_image = cv2.threshold(gray, 127, 255, 0)
    return bl_image


#########################################
# Rotation by a specified angle         #
# while preserving the frame size       #
# Вращение изображения на заданный угол #
# с сохранением размеров кадра          #
#########################################
def rotate_image_fs(image, corner):
    (h, w, d) = image.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, -corner, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


#########################################
# Rotation by a specified angle         #
# with image size preserved             #
# Вращение изображения на заданный угол #
# с сохранением размера изображения     #
#########################################
def rotate_image_is(mat, angle):
    height, width = mat.shape[:2]  # высота и ширина изображения
    image_center = (width // 2, height // 2)  # центр изображения
    rotation_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.)  # поворот
    abs_cos = abs(rotation_mat[0, 0])  # абсолютные значения sin угла поворота
    abs_sin = abs(rotation_mat[0, 1])  # абсолютные значения cos угла поворота
    bound_w = int(height * abs_sin + width * abs_cos)  # новые границы ширины
    bound_h = int(height * abs_cos + width * abs_sin)  # новые границы высоты
    # новые координаты центра изображения
    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]
    # поворот изображения с новыми границами и переведенной матрицей вращения
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat


################################################
# The detection of boundary edges of the image #
# Обнаружение границы края изображения         #
################################################
def canny_edge_detector(image):
    # Преобразование цвета изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Уменьшите шум от изображения
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


###########################
# Image segmentation      #
# Сегментация изображений #
###########################
def segment_image(image):
    r, threshold = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)
    return threshold


##################################################
# Creating parameters for recording a video file #
# Формирование параметров для записи видео файла #
##################################################
def get_video_param(file_input):
    file_name, file_ext = os.path.splitext(file_input)  # имя файла и расширение
    file_output = file_name + "_out" + file_ext
    cap = cv2.VideoCapture(file_input)  # Захватить исходное видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Ширина кадра исходного видео
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Высота кадра исходного видео
    if file_ext == '.mp4':
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    elif file_ext == '.avi':
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        print(file_ext, 'Ошибка в расширении имени файла (замените на .mp4 или .avi)')
    out = cv2.VideoWriter(file_output, fourcc, 25.0, (width, height))
    return out


##################################################################
# Setting parameters for changing the frame size of a video file #
# Задание параметров для изменения зармера кадра видео файла     #
##################################################################
def set_video_param(file_input, width, height):
    file_name, file_ext = os.path.splitext(file_input)  # имя файла и расширение
    file_output = file_name + "_out" + file_ext
    if file_ext == '.mp4':
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    elif file_ext == '.avi':
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        print(file_ext, 'Ошибка в расширении имени файла (замените на .mp4 или .avi)')
    out = cv2.VideoWriter(file_output, fourcc, 25.0, (width, height))
    return out

# https://pypi.org/project/postolit/0.0/
# https://github.com/APostolit
# Инструкция по загрузке
# https://yandex.ru/turbo/nuancesprog.ru/s/p/9911/

# команды для формирования дистрибутива
# pip install twine - один раз

###################################################################
# python setup.py sdist bdist_wheel  # формирование дистрибутива  #
###################################################################
# twine upload --repository testpypi dist/*  Для тестового репозитария
#      https://upload.pypi.org/legacy/  - удачная загрузка

############################################################################
# twine upload --repository pypi dist/*    Загрузка в основной репозитарий #
############################################################################

#      https://pypi.org/project/postolit/0.0.1/  - удачная загрузка

# twine upload dist/*   или такой для основного
# https://pypi.org/project/postolit/1.0.0/

