import sys, os, serial, datetime, time
import numpy as np
from configparser import ConfigParser
import scipy
from scipy.interpolate import interp1d
import fileinput
from simple_pid import PID
from wlm import *

# shouldn't need this -> from Fiber import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Super Laser Locker'
        self.left = 0
        self.top = 0
        self.width = 1500
        self.height = 400
        self.set_point = 0 # THz
        self.update_interval = 1 # ms
        self.no_of_points = 100
        self.no_of_arduinos = 1

        self.wlm = WavelengthMeter()
        

        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(self.update_interval)
        

    def tick(self):
        all_freq_reads = self.wlm.frequencies

        for laser in self.laser_objs.keys():
            freq_read = all_freq_reads[int(self.laser_objs[laser].chan) - 1]
            if freq_read >= 0:
                freq_mess = freq_read
                if self.laser_objs[laser].lockable and self.laser_objs[laser].lock_check.isChecked():
                    control = self.laser_objs[laser].my_pid(freq_mess)
                    ard_num = int(4095.0/20 * control + 4095.0/2.0)
                    mystr = '{:04d}'.format(ard_num).encode('utf-8')
                    self.laser_objs[laser].my_ard.ser.write(mystr)

            elif freq_read == -3.0:
                freq_mess = 'UNDER'
            elif freq_read == -4.0: 
                freq_mess = 'OVER'
            else:
                freq_mess = 'ERROR'

            self.laser_objs[laser].update_frequency(freq_mess)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_layout = QHBoxLayout()

        self.laser_objs = {}
        self.lasers = read_config()

        for las in self.lasers.keys():
            newlas = Laser()
            newlas.update_name(las)
            newlas.update_lockable(self.lasers[las]['lockable'])
            newlas.update_channel(self.lasers[las]['chan'])
            newlas.filename = self.lasers[las]['setfile']
            # if newlas.lockable:
            #     newlas.my_ard = Arduino(self.lasers[las]['com_port'])
            # else:
            #     print('arduino not created')
            newlas.get_setpoint()
            self.main_layout.addWidget(newlas)
            self.laser_objs[las] = newlas

        self.setLayout(self.main_layout)
        self.show()


class Laser(QWidget):
    def __init__(self):
        super().__init__()

        self.name = ''
        self.type = ''
        self.chan = 0
        self.lockable = True
        self.locking = False
        self.frequency = 0
        self.setpoint = 0
        self.p = 100
        self.i = 1000
        self.d = 0
        self.ard_mess = 2048
        self.offset = 0
        self.fstep = 50
        self.filename = ''
        self.basefolder = 'z:\\'
        self.my_pid = PID(self.p,self.i,self.d,self.setpoint,sample_time = 0.01, output_limits = [-10,10])
        self.my_ard = ''

        self.layout = QGridLayout()

        self.name_label = QLabel(self.name)
        name_font = QFont("Times",30,QFont.Bold)
        self.name_label.setFont(name_font)
        self.set_label = QLabel('Setpoint (THz):')
        self.ard_label = QLabel('Control Value:')
        self.off_label = QLabel('Set Offset (THz):')
        self.step_label = QLabel('Step Size (MHz):')
        self.p_label = QLabel('P:')
        self.i_label = QLabel('I:')
        self.d_label = QLabel('D:')

        self.freq_value = QLabel("{0:.6f}".format(self.frequency))
        self.set_value = QLineEdit("{0:.6f}".format(self.setpoint))
        self.ard_value = QLabel(str(self.ard_mess))
        self.off_value = QLineEdit("{0:.6f}".format(self.offset))
        self.step_value = QLineEdit(str(self.fstep))
        self.p_value = QLineEdit(str(self.p))
        self.i_value = QLineEdit(str(self.i))
        self.d_value = QLineEdit(str(self.d))

        self.scan_label = QLabel('Frequency Shift (MHz):')

        self.laser_scan = QSpinBox()
        self.laser_scan.setMinimum(-5000)
        self.laser_scan.setMaximum(5000)
        self.laser_scan.setSingleStep(np.int(self.fstep))

        self.laser_scan.valueChanged.connect(self.set_setpoint)
        self.laser_scan.valueChanged.connect(self.set_fstep)
        self.p_value.returnPressed.connect(self.update_p)
        self.i_value.returnPressed.connect(self.update_i)
        self.d_value.returnPressed.connect(self.update_d)

        self.pid_label = QLabel('PID Values')
        self.lock_check = QCheckBox('Lock')

        self.layout.addWidget(self.name_label,0,0)
        self.layout.addWidget(QLabel('THz'),0,2)
        self.layout.addWidget(self.freq_value,0,1)
        self.layout.addWidget(self.lock_check,1,0)
        self.layout.addWidget(self.ard_label,2,0)
        self.layout.addWidget(self.ard_value,2,1)
        self.layout.addWidget(self.set_label,3,0)
        self.layout.addWidget(self.set_value,3,1)
        self.layout.addWidget(self.scan_label,4,0)
        self.layout.addWidget(self.laser_scan,4,1)
        self.layout.addWidget(self.off_label,5,0)
        self.layout.addWidget(self.off_value,5,1)
        self.layout.addWidget(self.step_label,6,0)
        self.layout.addWidget(self.step_value,6,1)
        self.layout.addWidget(self.pid_label,7,0)
        self.layout.addWidget(self.p_label,8,0)
        self.layout.addWidget(self.p_value,8,1)
        self.layout.addWidget(self.i_label,9,0)
        self.layout.addWidget(self.i_value,9,1)
        self.layout.addWidget(self.d_label,10,0)
        self.layout.addWidget(self.d_value,10,1)
        
        self.setLayout(self.layout)

    def update_frequency(self,new_freq):
        nf = new_freq
        self.frequency = nf
        try:
            self.freq_value.setText("{0:.6f}".format(nf))
        except:
            self.freq_value.setText(nf)

    def update_name(self,new_name):
        nn = str(new_name)
        self.name = nn
        self.name_label.setText(nn)

    def update_channel(self,new_chan):
        nc = int(new_chan)
        self.chan = new_chan

    def update_p(self):
        self.p = np.float(self.p_value.text())
        self.my_pid.Kp = self.p

    def update_i(self):
        self.i = np.float(self.i_value.text())
        self.my_pid.Ki = self.i

    def update_d(self):
        self.d = np.float(self.d_value.text())
        self.my_pid.Kd = self.d

    # def update_type(self,new_type):
    #   nt = str(new_type)
    #   self.type = nt
    #   self.type_label.setText(nt)


    def update_lockable(self,new_lockable):
        if new_lockable == 'True':
            nl = True
        else:
            nl = False
        self.lockable = nl
        if not self.lockable:
            self.ard_label.hide()
            self.ard_value.hide()
            self.scan_label.hide()
            self.laser_scan.hide()
            self.off_label.hide()
            self.off_value.hide()
            self.step_label.hide()
            self.step_value.hide()
            self.pid_label.hide()
            self.p_label.hide()
            self.p_value.hide()
            self.i_label.hide()
            self.i_value.hide()
            self.d_value.hide()
            self.d_label.hide()
            self.lock_check.hide()

    def set_fstep(self):
        new_fstep = np.int(self.step_value.text())
        self.laser_scan.setSingleStep(new_fstep)
        self.fstep = new_fstep


    def set_setpoint(self):
        ns = np.float(self.offset) + np.float(self.fstep)*1e-6
        filepath = self.basefolder + self.filename
        file = open(filepath,'w')
        file.write(str(ns))
        file.close()
        self.setpoint = ns
        self.set_value.setText("{0:.6f}".format(ns))
        self.my_pid.setpoint = self.setpoint


    def get_setpoint(self):
        filepath = self.basefolder + self.filename
        file = open(filepath,'r')
        new_set = np.float(file.readline())
        file.close()

        self.setpoint = new_set
        self.set_value.setText("{0:.6f}".format(new_set))
        self.off_value.setText("{0:.6f}".format(new_set))


    def update_ardmess(self,new_mess):
        nm = new_mess
        self.ard_mess = new_mess
        self.ard_label.setText(new_mess)


class Arduino():
    def __init__(self,com_port):
        serial_port = com_port
        baud_rate = 9600;

        try:
            self.ser = serial.Serial(serial_port, baud_rate, 
                            bytesize=serial.SEVENBITS, 
                            parity=serial.PARITY_ODD, 
                            stopbits=serial.STOPBITS_ONE, 
                            timeout=1)
        except:
            try:
                ser.close()
            except:
                print ("Serial port already closed" )
                self.ser = serial.Serial(serial_port, baud_rate, 
                            bytesize=serial.SEVENBITS, 
                            parity=serial.PARITY_ODD, 
                            stopbits=serial.STOPBITS_ONE, 
                            timeout=1)





def read_config(filename = 'laser_config.ini'):
    config = ConfigParser()
    config.read(filename)

    laser_ids = config.sections()
    # make dictionary out of config

    lasers = {}

    for l in laser_ids:
        opts = config.options(l)
        
        lasers[l] = {}
        for o in opts:
            lasers[l][o] = config.get(l, o)

    return lasers


def set_dark(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    set_dark(app)
    ex = App()
    sys.exit(app.exec_())