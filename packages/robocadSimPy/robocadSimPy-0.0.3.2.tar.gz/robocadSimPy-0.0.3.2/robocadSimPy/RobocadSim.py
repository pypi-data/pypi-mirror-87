# from .data import PycForPy
from .data import PyForPy


class RE21mini:

    def __init__(self):
        # create RobocadSim class from .pyc file
        self.rc = PyForPy.RobocadSim()

        # for user
        self.right_motor_speed = 0.0
        self.left_motor_speed = 0.0
        self.back_motor_speed = 0.0

        self.lift_motor_speed = 0.0
        self.angle_for_big = 0.0
        self.dir_for_small = 0.0

        self.right_motor_enc = 0.0
        self.left_motor_enc = 0.0
        self.back_motor_enc = 0.0
        self.lift_motor_enc = 0.0

        self.reset_right_enc = False
        self.reset_left_enc = False
        self.reset_back_enc = False
        self.reset_lift_enc = False

        self.reset_gyro = False

        self.button_ems = False
        self.button_start = False
        self.button_limit = False

        self.right_us = 0.0
        self.left_us = 0.0
        self.right_ir = 0.0
        self.left_ir = 0.0
        self.navX = 0.0

        self.image_from_camera = None
        self.bytes_from_camera = None

    #
    #
    #
    #                            NON VOID FUNCTIONS
    #
    #
    #

    def write_motors(self, right: float, left: float, back: float):
        self.rc.write_motors(right, left, back)

    def write_oms(self, lift: float, big: float, small: float):
        self.rc.write_oms(lift, big, small)

    def write_reset(self, right: bool, left: bool, back: bool, lift: bool, gyro: bool):
        self.rc.write_reset(right, left, back, lift, gyro)

    def read_encs(self):
        return self.rc.read_encs()

    def read_sensors(self):
        return self.rc.read_sensors()

    def read_buttons(self):
        return self.rc.read_buttons()

    def read_camera(self):
        return self.rc.read_camera()

    def read_camera_bytes(self):
        return self.rc.read_camera_bytes()

    #
    #
    #
    #                            VOID FUNCTIONS
    #
    #
    #

    def write_motors_void(self):
        self.rc.write_motors(self.right_motor_speed, self.left_motor_speed, self.back_motor_speed)

    def write_oms_void(self):
        self.rc.write_oms(self.lift_motor_speed, self.angle_for_big, self.dir_for_small)

    def write_reset_void(self):
        self.rc.write_reset(self.reset_right_enc, self.reset_left_enc, self.reset_back_enc, self.reset_lift_enc,
                            self.reset_gyro)

    def read_encs_void(self):
        (self.right_motor_enc, self.left_motor_enc, self.back_motor_enc, self.lift_motor_enc) = self.rc.read_encs()

    def read_sensors_void(self):
        (self.right_us, self.left_us, self.right_ir, self.left_ir, self.navX) = self.rc.read_sensors()

    def read_buttons_void(self):
        (self.button_ems, self.button_start, self.button_limit) = self.rc.read_buttons()

    def read_camera_void(self):
        self.image_from_camera = self.rc.read_camera()

    def read_camera_bytes_void(self):
        self.bytes_from_camera = self.rc.read_camera_bytes()
