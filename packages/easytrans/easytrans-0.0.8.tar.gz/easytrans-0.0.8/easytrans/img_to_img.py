import os
from PIL import Image
import fitz

from easytrans.constant import FAILURE_STATUS, SUCCESS_STATUS, IMAGE_FORMAT
from easytrans.utils import FileUtil


class ImagesToLongImage(object):

    @staticmethod
    def to_long_image_by_file_list(image_path_list, save_name=None, save_dir=None, del_origin_img=False,
                                   background_color=None):

        try:
            if not isinstance(image_path_list, list) or not len(image_path_list) > 0:
                return FAILURE_STATUS, "file list is none!"

            if not save_dir:
                save_dir = os.path.dirname(image_path_list[0])

            if not save_name:
                save_name = FileUtil.generate_file_name()

            save_path = os.path.join(save_dir, "{0}.png".format(save_name))

            image_list = [Image.open(img) for img in image_path_list]

            width = 0
            height = 0
            for img in image_list:
                # 单幅图像尺⼨
                w, h = img.size
                height += h
                # 取最⼤的宽度作为拼接图的宽度
                width = max(width, w)

            # 创建空⽩⻓图
            # background_color: 0xffffff (white color)
            if background_color:
                result = Image.new(image_list[0].mode, (width, height), background_color)
            else:
                result = Image.new(image_list[0].mode, (width, height))

            # 拼接图⽚
            height = 0
            for img in image_list:
                w, h = img.size
                # 图⽚⽔平居中
                result.paste(img, box=(round(width / 2 - w / 2), height))
                height += h

            result.save(save_path)

            if del_origin_img:
                FileUtil.delete_file_list(image_path_list)

            return SUCCESS_STATUS, save_path

        except Exception as e:
            return FAILURE_STATUS, repr(e)

    @staticmethod
    def to_long_image_by_file_dir(image_dir, save_name=None, save_dir=None, del_origin_img=False,
                                  background_color=None):

        try:

            if not isinstance(image_dir, str) or not os.path.isdir(image_dir):
                return FAILURE_STATUS, "'{}' is not a directory!".format(image_dir)

            image_path_list = FileUtil.get_dir_file_path_list(image_dir, suffix=IMAGE_FORMAT)
            return ImagesToLongImage.to_long_image_by_file_list(image_path_list, save_name, save_dir, del_origin_img,
                                                                background_color)

        except Exception as e:
            return FAILURE_STATUS, repr(e)


class JpgToPng(object):
    pass


class ImageToPsd(object):
    @staticmethod
    def single_img_to_psd(img_path, psd_dir=None, psd_name=None):
        try:
            if not os.path.isfile(img_path) or not os.path.splitext(img_path)[1] in IMAGE_FORMAT:
                return FAILURE_STATUS, "file format error!"

            if not psd_dir:
                psd_dir = os.path.dirname(img_path)

            if not psd_name:
                psd_name = FileUtil.generate_file_name()

            psd_path = os.path.join(psd_dir, "{0}.psd".format(psd_name))
            pix = fitz.Pixmap(img_path)
            pix.writeImage(psd_path)

            return SUCCESS_STATUS, psd_path

        except Exception as e:
            return FAILURE_STATUS, repr(e)


class ImageToJpg(object):
    @staticmethod
    def single_img_to_jpg(img_path, jpg_dir=None, jpg_name=None):
        try:
            if not os.path.isfile(img_path) or not os.path.splitext(img_path)[1] in IMAGE_FORMAT:
                return FAILURE_STATUS, "file format error!"

            if not jpg_dir:
                jpg_dir = os.path.dirname(img_path)

            if not jpg_name:
                jpg_name = FileUtil.generate_file_name()

            jpg_path = os.path.join(jpg_dir, "{0}.jpg".format(jpg_name))
            pix = fitz.Pixmap(img_path)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(jpg_path, "JPEG")

            return SUCCESS_STATUS, jpg_path

        except Exception as e:
            return FAILURE_STATUS, repr(e)
