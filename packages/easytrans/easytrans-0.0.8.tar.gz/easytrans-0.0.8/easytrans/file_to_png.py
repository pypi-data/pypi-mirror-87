import os
import fitz

from easytrans.file_to_pdf import DocToPdf
from easytrans.constant import FAILURE_STATUS, SUCCESS_STATUS, PDF_FORMAT
from easytrans.utils import FileUtil


class DocToPng(object):

    @staticmethod
    def single_doc_to_png(doc_path, libreoffice_version=7.0, img_dir=None, img_name=None, zoom_x=8, zoom_y=8,
                          rotation_angle=0):
        status, result = DocToPdf.single_doc_to_pdf(doc_path, pdf_dir="/tmp/", pdf_name=None,
                                                    libreoffice_version=libreoffice_version)
        if status == FAILURE_STATUS:
            return FAILURE_STATUS, result

        return PdfToPng.single_pdf_to_img(result, img_dir, img_name, zoom_x, zoom_y, rotation_angle)

    @staticmethod
    def multiple_doc_to_png_by_file_dir(doc_dir, libreoffice_version=7.0, img_dir=None, zoom_x=8, zoom_y=8,
                                        rotation_angle=0):
        try:
            status, result = DocToPdf.multiple_doc_to_pdf_by_file_dir(doc_dir, pdf_dir="/tmp/",
                                                                      libreoffice_version=libreoffice_version)

            if status != SUCCESS_STATUS:
                return status, result

            return PdfToPng.multiple_pdf_to_img_by_file_list(result, img_dir, zoom_x, zoom_y, rotation_angle)

        except Exception as e:
            return FAILURE_STATUS, repr(e)

    @staticmethod
    def multiple_doc_to_png_by_file_list(doc_path_list=[], libreoffice_version=7.0, img_dir=None, zoom_x=8, zoom_y=8,
                                         rotation_angle=0):
        try:
            status, result = DocToPdf.multiple_doc_to_pdf_by_file_list(doc_path_list, pdf_dir="/tmp/",
                                                                       libreoffice_version=libreoffice_version)

            if status != SUCCESS_STATUS:
                return status, result

            return PdfToPng.multiple_pdf_to_img_by_file_list(result, img_dir, zoom_x, zoom_y, rotation_angle)

        except Exception as e:
            return FAILURE_STATUS, repr(e)


class PdfToPng(object):

    @staticmethod
    def single_pdf_to_img(pdf_path, img_dir=None, img_name=None, zoom_x=8, zoom_y=8, rotation_angle=0):
        try:

            if not os.path.isfile(pdf_path) or not os.path.splitext(pdf_path)[1] in PDF_FORMAT:
                return FAILURE_STATUS, "file format error!"

            pdf = fitz.open(pdf_path)

            if not img_name:
                img_name = FileUtil.get_file_name_by_path(pdf_path)

            if not img_dir:
                img_dir = os.path.dirname(pdf_path)

            img_list = []
            pg_count = pdf.pageCount

            for pg in range(0, pg_count):
                page = pdf[pg]
                trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
                pm = page.getPixmap(matrix=trans, alpha=False)
                if pg_count == 1:
                    img_path = os.path.join(img_dir, "{0}.png".format(img_name))
                else:
                    img_path = os.path.join(img_dir, "{0}{1}.png".format(img_name, str(pg)))
                pm.writePNG(img_path)
                img_list.append(img_path)

            pdf.close()

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, img_list

    @staticmethod
    def multiple_pdf_to_img_by_file_list(pdf_path_list, img_dir=None, zoom_x=8, zoom_y=8, rotation_angle=0):
        try:

            if not isinstance(pdf_path_list, list) or not len(pdf_path_list) > 0:
                return FAILURE_STATUS, "file list is none!"

            img_list = []
            for pdf_path in pdf_path_list:
                status, result = PdfToPng.single_pdf_to_img(pdf_path, img_dir, None, zoom_x, zoom_y, rotation_angle)
                if status == FAILURE_STATUS:
                    return status, result
                else:
                    img_list.append(result)

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, img_list

    @staticmethod
    def multiple_pdf_to_img_by_file_dir(pdf_dir, img_dir=None, zoom_x=8, zoom_y=8, rotation_angle=0):
        try:
            if not isinstance(pdf_dir, str) or not os.path.isdir(pdf_dir):
                return FAILURE_STATUS, "'{}' is not a directory!".format(pdf_dir)

            file_list = FileUtil.get_dir_file_path_list(pdf_dir, suffix=PDF_FORMAT)

            return PdfToPng.multiple_pdf_to_img_by_file_list(file_list, img_dir, zoom_x, zoom_y, rotation_angle)

        except Exception as e:
            return FAILURE_STATUS, repr(e)

    @staticmethod
    def cut_pdf_to_img_by_position(pdf_path, img_dir=None, img_name=None, zoom_x=8, zoom_y=8, rect_tl=0, rect_bl=0,
                                   rotation_angle=0):

        try:
            if not os.path.isfile(pdf_path) or not os.path.splitext(pdf_path)[1] in PDF_FORMAT:
                return FAILURE_STATUS, "file format error!"

            pdf = fitz.open(pdf_path)

            if not img_name:
                img_name = FileUtil.get_file_name_by_path(pdf_path)

            if not img_dir:
                img_dir = os.path.dirname(pdf_path)

            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            img_list = []
            pg_count = pdf.pageCount
            for pg in range(pg_count):
                page = pdf[pg]

                # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像
                # 此处若是不做设置，默认图片大小为：792X612, dpi=72
                mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
                # 页面大小
                rect = page.rect
                # 矩形区域
                # mp = rect.tl + (rect.bl - (0, 75 / zoom_x))
                mp = rect_tl + rect_bl
                # 想要截取的区域
                clip = fitz.Rect(mp, rect.br)
                # 将页面转换为图像
                pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)

                if pg_count == 1:
                    img_path = os.path.join(img_dir, "{0}.png".format(img_name))
                else:
                    img_path = os.path.join(img_dir, "{0}{1}.png".format(img_name, str(pg)))

                pix.writePNG(img_path)
                img_list.append(img_path)

            pdf.close()

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, img_list
