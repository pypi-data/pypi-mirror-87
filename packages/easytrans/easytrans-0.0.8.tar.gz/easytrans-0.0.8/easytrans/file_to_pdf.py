import os

from easytrans.constant import FAILURE_STATUS, SUCCESS_STATUS, DOC_FORMAT
from easytrans.utils import FileUtil


class DocToPdf(object):

    @staticmethod
    def single_doc_to_pdf(doc_path, pdf_dir=None, pdf_name=None, libreoffice_version=7.0):

        try:

            if not os.path.isfile(doc_path) or not os.path.splitext(doc_path)[1] in DOC_FORMAT:
                return FAILURE_STATUS, "file format error!"

            if libreoffice_version:
                libreoffice = "libreoffice{0}".format(libreoffice_version)
            else:
                libreoffice = "libreoffice"

            if pdf_dir:
                cmd = "{0} --headless --convert-to pdf --outdir {1} {2}".format(libreoffice, pdf_dir, doc_path)
            else:
                cmd = "{0} --headless --convert-to pdf {1}".format(libreoffice, doc_path)
                pdf_dir = os.path.dirname(doc_path)

            res = os.system(cmd)
            if res != 0:
                return FAILURE_STATUS, "file convert failed!"

            origin_file_name = FileUtil.get_file_name_by_path(doc_path)
            origin_file_path = os.path.join(pdf_dir, "{0}.pdf".format(origin_file_name))
            if pdf_name:
                destin_file_path = os.path.join(pdf_dir, "{0}.pdf".format(pdf_name))
                os.rename(origin_file_path, destin_file_path)
                file_path = destin_file_path
            else:
                file_path = origin_file_path

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, file_path

    @staticmethod
    def multiple_doc_to_pdf_by_file_dir(doc_dir, pdf_dir=None, libreoffice_version=7.0):
        try:

            if not isinstance(doc_dir, str) or not os.path.isdir(doc_dir):
                return FAILURE_STATUS, "'{0}' is not a directory!".format(doc_dir)

            file_list = FileUtil.get_dir_file_path_list(doc_dir, suffix=DOC_FORMAT)
            status, result = DocToPdf.multiple_doc_to_pdf_by_file_list(file_list, pdf_dir, libreoffice_version)

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return status, result

    @staticmethod
    def multiple_doc_to_pdf_by_file_list(doc_path_list, pdf_dir=None, libreoffice_version=7.0):
        pdf_path_list = []
        try:
            if not isinstance(doc_path_list, list) or not len(doc_path_list) > 0:
                return FAILURE_STATUS, "file list is none!"

            for doc_path in doc_path_list:
                status, result = DocToPdf.single_doc_to_pdf(doc_path, pdf_dir, None, libreoffice_version)
                if status == SUCCESS_STATUS:
                    pdf_path_list.append(result)
                else:
                    return status, result

        except Exception as e:
            return FAILURE_STATUS, repr(e)

        else:
            return SUCCESS_STATUS, pdf_path_list


class TxtToPdf(object):

    @staticmethod
    def single_txt_to_pdf(txt_path, pdf_dir=None, pdf_name=None):
        pass

    @staticmethod
    def txt_transfer_pdf(file_list=[], pdf_name_list=None, libreoffice_version=7.0):
        pass
