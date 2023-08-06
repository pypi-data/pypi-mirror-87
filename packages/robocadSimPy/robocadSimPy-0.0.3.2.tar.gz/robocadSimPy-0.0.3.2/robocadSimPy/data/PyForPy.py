import tempfile
import os
import cv2


class RobocadSim:

    def __init__(self):
        # getting temp folder
        self.__path_TMP = tempfile.gettempdir()

        # creating channels folder if it does not exists
        if not os.path.exists(self.__path_TMP + r"\RCADChannels"):
            try:
                os.mkdir(self.__path_TMP + r"\RCADChannels")
            except OSError:
                os.makedirs(self.__path_TMP + r"\RCADChannels")

        # creating paths to channels
        self.__path_to_motors = self.__path_TMP + r"\RCADChannels\motors.rcadch"
        self.__path_to_oms = self.__path_TMP + r"\RCADChannels\oms.rcadch"
        self.__path_to_encs = self.__path_TMP + r"\RCADChannels\encs.rcadch"
        self.__path_to_leds = self.__path_TMP + r"\RCADChannels\leds.rcadch"
        self.__path_to_sensors = self.__path_TMP + r"\RCADChannels\sensors.rcadch"
        self.__path_to_buttons = self.__path_TMP + r"\RCADChannels\buttons.rcadch"
        self.__path_to_reset = self.__path_TMP + r"\RCADChannels\reset.rcadch"
        self.__path_to_camera = self.__path_TMP + r"\RCADChannels\camera.rcadch"
        self.__path_to_other_set = self.__path_TMP + r"\RCADChannels\otherSet.rcadch"
        self.__path_to_other_get = self.__path_TMP + r"\RCADChannels\otherGet.rcadch"

        # other variables
        self.__self_is_not_used = True  # just for SINU

        # for IO funcs
        self.__last_encs_read = "0.0;0.0;0.0;0.0"
        self.__last_sensors_read = "0.0;0.0;0.0;0.0;0.0"
        self.__last_buttons_read = "0;0;0"

    #
    #
    #
    #                            NON VOID FUNCTIONS
    #
    #
    #

    def write_motors(self, right: float, left: float, back: float):
        try:
            f = open(self.__path_to_motors, "w+")
            f.write(str(right) + ";" + str(left) + ";" + str(back))
            f.close()
        except (Exception, IOError):
            pass

    def write_oms(self, lift: float, big: float, small: float):
        try:
            f = open(self.__path_to_oms, "w+")
            f.write(str(lift) + ";" + str(big) + ";" + str(small))
            f.close()
        except (Exception, IOError):
            pass

    def write_reset(self, right: bool, left: bool, back: bool, lift: bool, gyro: bool):
        try:
            f = open(self.__path_to_reset, "w+")
            f.write(("1" if right else "0") + ";" + ("1" if left else "0") + ";"
                    + ("1" if back else "0") + ";" + ("1" if lift else "0") + ";"
                    + ("1" if gyro else "0"))
            f.close()
        except (Exception, IOError):
            pass

    def read_encs(self):
        __encs_file_txt = "0.0;0.0;0.0;0.0"
        if not os.path.exists(self.__path_to_encs):
            f = open(self.__path_to_encs, "w+")
            f.close()
        else:
            f = open(self.__path_to_encs, "r")
            __encs_file_txt = f.readline()
            if __encs_file_txt is None:
                __encs_file_txt = self.__last_encs_read
            self.__last_encs_read = __encs_file_txt

        return self.__parse_float_channel(__encs_file_txt)

    def read_sensors(self):
        __sensors_file_txt = "0.0;0.0;0.0;0.0;0.0"
        if not os.path.exists(self.__path_to_sensors):
            f = open(self.__path_to_sensors, "w+")
            f.close()
        else:
            f = open(self.__path_to_sensors, "r")
            __sensors_file_txt = f.readline()
            if __sensors_file_txt is None:
                __sensors_file_txt = self.__last_sensors_read
            self.__last_sensors_read = __sensors_file_txt

        return self.__parse_float_channel(__sensors_file_txt)

    def read_buttons(self):
        __buttons_file_txt = "0;0;0"
        if not os.path.exists(self.__path_to_buttons):
            f = open(self.__path_to_buttons, "w+")
            f.close()
        else:
            f = open(self.__path_to_buttons, "r")
            __buttons_file_txt = f.readline()
            if __buttons_file_txt is None:
                __buttons_file_txt = self.__last_buttons_read
            self.__last_buttons_read = __buttons_file_txt

        return self.__parse_bool_channel(__buttons_file_txt)

    def read_camera(self):
        try:
            return cv2.imread(self.__path_to_camera, cv2.IMREAD_COLOR)
        except (Exception, IOError):
            return None

    def read_camera_bytes(self):
        try:
            return open(self.__path_to_camera, "rb").read()
        except (Exception, IOError):
            return None

    def __parse_float_channel(self, txt: str):
        self.__self_is_not_used = True

        try:
            return map(lambda s: float(s), txt.split(";"))
        except (Exception, IOError):
            return None

    def __parse_bool_channel(self, txt: str):
        self.__self_is_not_used = True

        try:
            return map(lambda s: bool(s), map(lambda s: int(s), txt.split(";")))
        except (Exception, IOError):
            return None
