import os
import random
import re
import shutil
import time
import zipfile


class FileUtil(object):

    @staticmethod
    def generate_file_path(file_dir, file_name=None, empty_dir=False, suffix=None):

        if os.path.exists(file_dir) and empty_dir:
            shutil.rmtree(file_dir)

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        if not file_name:
            file_name = FileUtil.generate_file_name(suffix)

        file_path = os.path.join(file_dir, file_name)

        return file_path

    @staticmethod
    def generate_file_name(suffix=None):
        file_name = time.strftime('%Y-%m-%d-%H-%M-%S') + '-' + str(time.time()).split(".")[0] + str(
            random.randrange(999999))
        if suffix:
            file_name = "{0}.{1}".format(file_name, suffix)

        return file_name

    @staticmethod
    def get_dir_file_path_list(dir, depth=1, suffix="all"):
        if not isinstance(dir, str) or not os.path.isdir(dir):
            return []

        file_list = []
        for file in os.listdir(dir):
            file = os.path.join(dir, file)

            if os.path.isdir(file) and depth > 1:
                file_list.extend(FileUtil.get_dir_file_path_list(file, depth - 1, suffix))
            elif os.path.isdir(file):
                continue
            elif not suffix == "all" and not os.path.splitext(file)[1] in suffix:
                continue
            else:
                file_list.append(file)

        return file_list

    @staticmethod
    def get_file_name_by_path(file_path):
        file_name = os.path.split(file_path)[1]
        file_name = os.path.splitext(file_name)[0]
        return file_name

    @staticmethod
    def zip_files(file_dir, zip_dir=None, zip_name=None):
        if not zip_name:
            zip_name = FileUtil.generate_file_name()

        if not zip_dir:
            zip_dir = os.path.abspath(os.path.join(file_dir, os.path.pardir))

        zip_path = os.path.join(zip_dir, "{0}.zip".format(zip_name))

        zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

        for d_path, d_names, file_names in os.walk(file_dir):
            f_path = d_path.replace(file_dir, '')
            f_path = f_path and f_path + os.sep or ''
            for filename in file_names:
                zip.write(os.path.join(d_path, filename), f_path + filename)

        zip.close()

        return zip_path

    @staticmethod
    def delete_file(path):
        if os.path.isfile(path):
            os.remove(path)
            # os.unlink(path)
            return True
        else:
            return False

    @staticmethod
    def delete_file_list(path_list):
        result = [FileUtil.delete_file(path) for path in path_list if os.path.isfile(path)]
        return result

    @staticmethod
    def delete_dir(dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
            return True
        else:
            return False

    @staticmethod
    def file_rename(origin_file_path, target_file_name):
        if not os.path.isfile(origin_file_path):
            return None

        file_suffix = os.path.splitext(origin_file_path)[1]
        target_file_path = os.path.join(os.path.dirname(origin_file_path),
                                        "{0}{1}".format(target_file_name, file_suffix))
        os.rename(origin_file_path, target_file_path)

        return target_file_path

    @staticmethod
    def format_name(file_name):
        result = []
        for s in str(file_name):
            if StringUtil.is_not_chinese(s) or re.match("^[0-9a-zA-Z_-]+$", s):
                result.append(s)
        return "".join(result)

    @staticmethod
    def file_info():
        pass


class StringUtil(object):

    @staticmethod
    def is_not_chinese(input):
        code = str(input).encode("utf-8").decode("utf-8")
        if u'\u4e00' <= code <= u'\u9fff':
            return True
        else:
            return False

    @staticmethod
    def is_not_number(input):
        return str(input).isdigit()

    @staticmethod
    def is_not_alpha(input):
        return str(input).isalpha()

    @staticmethod
    def is_not_underline(input):
        return "-" == input

    @staticmethod
    def is_not_underscore(input):
        return "_" == input


class DateUtil(object):
    pass
