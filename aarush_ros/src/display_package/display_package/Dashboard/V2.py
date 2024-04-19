import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette, QBrush, QPainter, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRect, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setFixedSize(1024, 600)

        pixmap = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Bg.png")
        self.central_widget.setAutoFillBackground(True)
        palette = self.central_widget.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.central_widget.setPalette(palette)

        self.camera_label = QLabel(self)
        self.cam = Camera()

        self.dist_label = QLabel(self)
        self.dist_label.setGeometry(QRect(840, 24, 150, 50))
        self.dist_label.setAlignment(Qt.AlignCenter)
        self.dist_label.setStyleSheet("font-family: 'Good Times'; font-size: 25px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.dist_label.setText("DISTANCE")

        self.solar1 = QLabel(self)
        self.solar1.setGeometry(QRect(218, 57, 200, 36))
        self.solar1.setAlignment(Qt.AlignCenter)
        self.solar1.setStyleSheet("font-family: 'Good Times'; font-size: 32px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.solar1.setText("COCKPIT")
        self.solar1.hide()

        self.solar1_ul = QLabel(self)
        self.solar1_ul.setGeometry(212, 100 , 220, 9)
        self.solar1_ul.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/underline.png").scaled(220, 9))
        self.solar1_ul.hide()

        self.solar3 = QLabel(self)
        self.solar3.setGeometry(QRect(744,57,200,36))
        self.solar3.setAlignment(Qt.AlignCenter)
        self.solar3.setStyleSheet("font-family: 'Good Times'; font-size: 32px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.solar3.setText("MOTOR")
        self.solar3.hide()

        self.solar3_ul = QLabel(self)
        self.solar3_ul.setGeometry(744,100, 220, 9)
        self.solar3_ul.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/underline.png").scaled(220, 9))
        self.solar3_ul.hide()


        self.solar4 = QLabel(self)
        self.solar4.setGeometry(QRect(218, 337, 450, 36))
        self.solar4.setAlignment(Qt.AlignCenter)
        self.solar4.setStyleSheet("font-family: 'Good Times'; font-size: 32px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.solar4.setText("MOTOR CONTROLLER")
        self.solar4.hide()

        self.solar4_ul = QLabel(self)
        self.solar4_ul.setGeometry(218,376, 450, 9)
        self.solar4_ul.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/underline.png").scaled(450, 9))
        self.solar4_ul.hide()

        self.mppt_temp = QLabel(self)
        self.mppt_temp.setGeometry(QRect(754, 337, 200, 36))
        self.mppt_temp.setAlignment(Qt.AlignCenter)
        self.mppt_temp.setStyleSheet("font-family: 'Good Times'; font-size: 32px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.mppt_temp.setText("BATTERY")
        self.mppt_temp.hide()

        self.mppt_temp_ul = QLabel(self)
        self.mppt_temp_ul.setGeometry(744,380, 220, 9)
        self.mppt_temp_ul.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/underline.png").scaled(220, 9))
        self.mppt_temp_ul.hide()

        self.motor_current = QLabel(self)
        self.motor_current.setGeometry(QRect(430, 50, 200, 36))
        self.motor_current.setAlignment(Qt.AlignCenter)
        self.motor_current.setStyleSheet("font-family: 'Good Times'; font-size: 32px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.motor_current.setText("MOTOR")
        self.motor_current.hide()

        self.motor_current_ul = QLabel(self)
        self.motor_current_ul.setGeometry(430,90, 200, 9)
        self.motor_current_ul.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/underline.png").scaled(220, 9))
        self.motor_current_ul.hide()

        self.motor_current_fr = QLabel(self)
        self.motor_current_fr.setGeometry(450,130, 173, 63)
        self.motor_current_fr.hide()

        self.motorctrl_current = QLabel(self)
        self.motorctrl_current.setGeometry(QRect(310, 220, 450, 36))
        self.motorctrl_current.setAlignment(Qt.AlignCenter)
        self.motorctrl_current.setStyleSheet("font-family: 'Good Times'; font-size: 32px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.motorctrl_current.setText("MOTOR CONTROLLER")
        self.motorctrl_current.hide()

        self.motorctrl_current_ul = QLabel(self)
        self.motorctrl_current_ul.setGeometry(310,260, 450, 9)
        self.motorctrl_current_ul.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/underline.png").scaled(450, 9))
        self.motorctrl_current_ul.hide()

        self.motorctrl_current_fr = QLabel(self)
        self.motorctrl_current_fr.setGeometry(450,300, 173, 63)
        self.motorctrl_current_fr.hide()

        self.battery_current = QLabel(self)
        self.battery_current.setGeometry(QRect(430, 390, 200, 36))
        self.battery_current.setAlignment(Qt.AlignCenter)
        self.battery_current.setStyleSheet("font-family: 'Good Times'; font-size: 32px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.battery_current.setText("BATTERY")
        self.battery_current.hide()

        self.battery_current_ul = QLabel(self)
        self.battery_current_ul.setGeometry(430,430, 200, 9)
        self.battery_current_ul.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/underline.png").scaled(220, 9))
        self.battery_current_ul.hide()

        self.battery_current_fr = QLabel(self)
        self.battery_current_fr.setGeometry(450,470, 173, 63)
        self.battery_current_fr.hide()

        self.time_label = QLabel(self)
        self.time_label.setGeometry(QRect(825, 150, 180, 50))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-family: 'Good Times'; font-size: 25px; font-weight: 400; "
                                        "line-height: 48px; letter-spacing: 0em; color: #F97110; "
                                        "background-color: #161F28")
        self.time_label.setText("DRIVE TIME")

        self.mapfr = QLabel(self)
        self.mapfr.setGeometry(185, 27 , 631, 300)
        self.mapfr.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Map display frame.png").scaled(631, 300, Qt.AspectRatioMode.KeepAspectRatio))

        self.distfr = QLabel(self)
        self.distfr.setGeometry(830, 80, 173, 63)

        self.timefr = QLabel(self)
        self.timefr.setGeometry(830, 203, 173, 63)
        # self.timefr.setPixmap(QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Drive time frame.png").scaled(173, 63, Qt.AspectRatioMode.KeepAspectRatio))
                
        button1_image = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/map.png")
        button2_image = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Temprature.png")
        button3_image = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/current.png")
        button4_image = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Controls.png")

        self.button1 = QPushButton(self)
        self.button1.setIcon(QIcon(button1_image))
        self.button1.setIconSize(button1_image.size())
        self.button1.setGeometry(27, 50, int(button1_image.width()), int(button1_image.height()))
        self.button1.setStyleSheet("QPushButton { border: none; background-color: transparent; }")
        self.button1.clicked.connect(self.Mainwindow)

        self.button2 = QPushButton(self)
        self.button2.setIcon(QIcon(button2_image))
        self.button2.setIconSize(button2_image.size())
        self.button2.setGeometry(27, 190, button2_image.width(), button2_image.height())
        self.button2.setStyleSheet("QPushButton { border: none; background-color: transparent; }")
        self.button2.clicked.connect(self.Temps)

        self.button3 = QPushButton(self)
        self.button3.setIcon(QIcon(button3_image))
        self.button3.setIconSize(button3_image.size())
        self.button3.setGeometry(27, 330, button3_image.width(), button3_image.height())
        self.button3.setStyleSheet("QPushButton { border: none; background-color: transparent; }")
        self.button3.clicked.connect(self.Current)

        self.button4 = QPushButton(self)
        self.button4.setIcon(QIcon(button4_image))
        self.button4.setIconSize(button4_image.size())
        self.button4.setGeometry(27, 470, button4_image.width(), button4_image.height())
        self.button4.setStyleSheet("QPushButton { border: none; background-color: transparent; }")
        self.button4.clicked.connect(self.CPanel)

        self.battery = 0
        self.temps = 0
        self.distance = 0
        self.motorcurrent_value = 0
        self.mtrctrl_value = 0
        self.batcurrent_value = 0
        self.time_str = "00:00:00"
        self.seconds = 0
        self.battery_images = ['/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/battery0.png',
            '/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Battery20.png',  
            '/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Battery40.png',
            '/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/battery60.png',
            '/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Battery80.png',
            '/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Battery100.png'
        ]
        self.temp_images = ['/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Tempcool.png',
                            '/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/tempok.png',
                            '/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/temphot.png'
                            ]

        self.camera_label.show()
        self.cam.ImageUpdate.connect(self.ImageUpdateSlot)
        self.cam.start()
        self.camera_label.setGeometry(QRect(185, 340, 631 , 230))
        self.load_html_file("http://127.0.0.1:5500/GUI/Beaglebone/Dashboard/mapV2.html")

        self.battery_label = QLabel(self)
        self.battery_label.setGeometry(848,347,143,216)

        self.temp1_label = QLabel(self)
        self.temp1_label.setGeometry(286,138,71,157)
        self.temp1_label.hide()
        self.temp2_label = QLabel(self)
        self.temp2_label.setGeometry(818,138,71,157)
        self.temp2_label.hide()
        self.temp3_label = QLabel(self)
        self.temp3_label.setGeometry(286,410,71,157)
        self.temp3_label.hide()
        self.temp4_label = QLabel(self)
        self.temp4_label.setGeometry(818,410,71,157)
        self.temp4_label.hide()


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_variable)
        self.timer.start(1000) 

        self.button1_clicked = False
        self.button2_clicked = False
        self.button3_clicked = False
        self.button4_clicked = False

    def hide(self):
        if self.button1_clicked:
            self.camera_label.show()
            self.cam.ImageUpdate.connect(self.ImageUpdateSlot)
            self.cam.start()
            self.camera_label.setGeometry(QRect(185, 340, 631 , 230))
            self.dist_label.show()
            self.time_label.show()
            self.timefr.show()
            self.distfr.show()
            self.mapfr.show()
            self.battery_label.show()
            self.solar1.hide()
            self.solar3.hide()
            self.solar4.hide()
            self.motor_current.hide()
            self.mppt_temp.hide()
            self.solar1_ul.hide()
            self.solar3_ul.hide()
            self.solar4_ul.hide()
            self.motor_current_ul.hide()
            self.mppt_temp_ul.hide()
            self.temp1_label.hide()
            self.temp2_label.hide()
            self.temp3_label.hide()
            self.temp4_label.hide()
            self.motor_current_fr.hide()
            self.motorctrl_current.hide()
            self.motorctrl_current_ul.hide()
            self.motorctrl_current_fr.hide()
            self.battery_current.hide()
            self.battery_current_ul.hide()
            self.battery_current_fr.hide()
            
        if self.button2_clicked:
            self.solar1.show()
            self.solar3.show()
            self.solar4.show()
            self.mppt_temp.show()
            self.solar1_ul.show()
            self.solar3_ul.show()
            self.solar4_ul.show()
            self.mppt_temp_ul.show()
            self.temp1_label.show()
            self.temp2_label.show()
            self.temp3_label.show()
            self.temp4_label.show()
            self.camera_label.hide()
            self.cam.stop()
            self.dist_label.hide()
            self.time_label.hide()
            self.timefr.hide()
            self.distfr.hide()
            self.mapfr.hide()
            self.web_view.hide()
            self.battery_label.hide()
            self.motor_current.hide()
            self.motor_current_ul.hide()
            self.motor_current_fr.hide()
            self.motorctrl_current.hide()
            self.motorctrl_current_ul.hide()
            self.motorctrl_current_fr.hide()
            self.battery_current.hide()
            self.battery_current_ul.hide()
            self.battery_current_fr.hide()
            

        if self.button3_clicked:
            self.motor_current.show()
            self.motor_current_ul.show()
            self.motor_current_fr.show()
            self.motorctrl_current.show()
            self.motorctrl_current_ul.show()
            self.motorctrl_current_fr.show()
            self.battery_current.show()
            self.battery_current_ul.show()
            self.battery_current_fr.show()
            self.camera_label.hide()
            self.cam.stop()
            self.dist_label.hide()
            self.time_label.hide()
            self.timefr.hide()
            self.distfr.hide()
            self.mapfr.hide()
            self.web_view.hide()
            self.battery_label.hide()
            self.solar1.hide()
            self.solar3.hide()
            self.solar4.hide()
            self.mppt_temp.hide()
            self.solar1_ul.hide()
            self.solar3_ul.hide()
            self.solar4_ul.hide()
            self.mppt_temp_ul.hide()
            self.temp1_label.hide()
            self.temp2_label.hide()
            self.temp3_label.hide()
            self.temp4_label.hide()
            

        if self.button4_clicked:
            self.camera_label.hide()
            self.cam.stop()
            self.dist_label.hide()
            self.time_label.hide()
            self.timefr.hide()
            self.distfr.hide()
            self.mapfr.hide()
            self.web_view.hide()
            self.battery_label.hide()
            self.solar1.hide()
            self.solar3.hide()
            self.solar4.hide()
            self.mppt_temp.hide()
            self.solar1_ul.hide()
            self.solar3_ul.hide()
            self.solar4_ul.hide()
            self.mppt_temp_ul.hide()
            self.temp1_label.hide()
            self.temp2_label.hide()
            self.temp3_label.hide()
            self.temp4_label.hide()
            self.motor_current.hide()
            self.motor_current_ul.hide()
            self.motor_current_fr.hide()
            self.motorctrl_current.hide()
            self.motorctrl_current_ul.hide()
            self.motorctrl_current_fr.hide()
            self.battery_current.hide()
            self.battery_current_ul.hide()
            self.battery_current_fr.hide()


    def update_variable(self):
        self.battery += 1
        self.temps += 1
        self.distance += 1
        self.motorcurrent_value += 1
        self.mtrctrl_value += 1
        self.batcurrent_value += 1
        self.seconds += 1        
        hours, rem = divmod(self.seconds, 3600)
        minutes, remaining_seconds = divmod(rem, 60)
        self.time_str = f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        print(self.time_str, end='\r')
        self.display_image()
        if self.battery >100:
            self.battery = 0
        if self.temps > 80:
            self.temps = 0 
        if self.distance > 3050:
            self.distance = 0
        if self.motorcurrent_value > 20:
            self.motorcurrent_value = 0
        if self.mtrctrl_value > 25:
            self.mtrctrl_value = 0
        if self.batcurrent_value > 30:
            self.batcurrent_value = 0

    def display_image(self):
        image_index = self.battery // 20 % len(self.battery_images)
        pixmap = QPixmap(self.battery_images[image_index])

        # Create a painter object for the battery image
        painter = QPainter(pixmap)
        painter.setFont(QFont('Good Times', 20))  
        painter.setPen(Qt.white)  

        # Draw the battery variable text on the battery image
        text_width = painter.fontMetrics().width(str(self.battery))
        text_height = painter.fontMetrics().height()
        x = (pixmap.width() - text_width) // 2
        y = (pixmap.height() - text_height) // 2
        painter.drawText(x, y, str(self.battery))
        painter.end()

        # Display the battery image
        self.battery_label.setPixmap(pixmap.scaled(143, 216))

        # Determine the index for the temperature image
        temp_index = 0
        if self.temps > 45 and self.temps < 60:
            temp_index = 1
        elif self.temps >= 60 and self.temps < 80:
            temp_index = 2

        #Cocpit Temperature
        pixmap_temp = QPixmap(self.temp_images[temp_index])
        painter_temp = QPainter(pixmap_temp)
        painter_temp.setFont(QFont('Good Times', 20))  
        painter_temp.setPen(Qt.white)  
        text_width_temp = painter_temp.fontMetrics().width(str(self.temps))
        x_temp = (pixmap_temp.width() - text_width_temp) // 2
        painter_temp.drawText(x_temp, 145, str(self.temps))
        painter_temp.end()
        self.temp1_label.setPixmap(pixmap_temp.scaled(71, 157))

        #Motor Temperature
        pixmap_temp2 = QPixmap(self.temp_images[temp_index])
        painter_temp2 = QPainter(pixmap_temp2)
        painter_temp2.setFont(QFont('Good Times', 20))
        painter_temp2.setPen(Qt.white)  
        text_width_temp2 = painter_temp2.fontMetrics().width(str(self.temps))
        x_temp = (pixmap_temp2.width() - text_width_temp2) // 2
        painter_temp2.drawText(x_temp, 145, str(self.temps))
        painter_temp2.end()
        self.temp2_label.setPixmap(pixmap_temp.scaled(71, 157))

        #Motor Controller Temperature
        pixmap_temp3 = QPixmap(self.temp_images[temp_index])
        painter_temp3 = QPainter(pixmap_temp3)
        painter_temp3.setFont(QFont('Good Times', 20)) 
        painter_temp3.setPen(Qt.white)  
        text_width_temp3 = painter_temp3.fontMetrics().width(str(self.temps))
        x_temp = (pixmap_temp3.width() - text_width_temp3) // 2
        painter_temp3.drawText(x_temp, 145, str(self.temps))
        painter_temp3.end()
        self.temp3_label.setPixmap(pixmap_temp.scaled(71, 157))

        #Battery Temperature
        pixmap_temp4 = QPixmap(self.temp_images[temp_index])
        painter_temp4 = QPainter(pixmap_temp4)
        painter_temp4.setFont(QFont('Good Times', 20)) 
        painter_temp4.setPen(Qt.white)  
        text_width_temp4 = painter_temp4.fontMetrics().width(str(self.temps))
        x_temp = (pixmap_temp4.width() - text_width_temp4) // 2
        painter_temp4.drawText(x_temp, 145, str(self.temps))
        painter_temp4.end()
        self.temp4_label.setPixmap(pixmap_temp.scaled(71, 157))

        #Current of motor 
        pixmap_motor = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Drive time frame.png")
        painter_motor = QPainter(pixmap_motor)
        painter_motor.setFont(QFont('Good Times', 20))  
        painter_motor.setPen(Qt.white)  
        text_width_motor = painter_motor.fontMetrics().width(str(self.motorcurrent_value)+ " AMP")
        x_temp = (pixmap_motor.width() - text_width_motor) // 2
        painter_motor.drawText(x_temp, 43, str(self.motorcurrent_value)+ " AMP")
        painter_motor.end()
        self.motor_current_fr.setPixmap(pixmap_motor.scaled(173, 63))

        #Current of motor controller
        pixmap_motorctrl = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Drive time frame.png")
        painter_motorctrl = QPainter(pixmap_motorctrl)
        painter_motorctrl.setFont(QFont('Good Times', 20))  # Set the font and size of the variable text
        painter_motorctrl.setPen(Qt.white)  # Set the color of the variable text
        text_width_motorctrl = painter_motorctrl.fontMetrics().width(str(self.mtrctrl_value) + " AMP")
        x_temp = (pixmap_motorctrl.width() - text_width_motorctrl) // 2
        painter_motorctrl.drawText(x_temp, 43, str(self.mtrctrl_value) + " AMP")
        painter_motorctrl.end()
        self.motorctrl_current_fr.setPixmap(pixmap_motorctrl.scaled(173, 63))

        #Current of battery 
        pixmap_battery = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Drive time frame.png")
        painter_battery = QPainter(pixmap_battery)
        painter_battery.setFont(QFont('Good Times', 20))  # Set the font and size of the variable text
        painter_battery.setPen(Qt.white)  # Set the color of the variable text
        text_width_battery = painter_battery.fontMetrics().width(str(self.batcurrent_value)+ " AMP")
        x_temp = (pixmap_battery.width() - text_width_battery) // 2
        painter_battery.drawText(x_temp, 43, str(self.batcurrent_value)+ " AMP")
        painter_battery.end()
        self.battery_current_fr.setPixmap(pixmap_battery.scaled(173, 63))

        #Distance Travelled
        pixmap_distance = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Drive time frame.png")
        painter_distance = QPainter(pixmap_distance)
        painter_distance.setFont(QFont('Good Times', 20))  # Set the font and size of the variable text
        painter_distance.setPen(Qt.white)  # Set the color of the variable text
        text_width_distance = painter_distance.fontMetrics().width(str(self.distance)+"KM")
        x_temp = (pixmap_distance.width() - text_width_distance) // 2
        painter_distance.drawText(x_temp, 43, str(self.distance)+" KM")
        painter_distance.end()
        self.distfr.setPixmap(pixmap_distance.scaled(173, 63))

        #Time
        # print(time_str, end='\r')
        pixmap_time = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Drive time frame.png")
        painter_time = QPainter(pixmap_time)
        painter_time.setFont(QFont('Good Times', 15))  # Set the font and size of the variable text
        painter_time.setPen(Qt.white)  # Set the color of the variable text
        text_width_time = painter_time.fontMetrics().width(self.time_str +" HRs")
        x_temp = (pixmap_time.width() - text_width_time) // 2
        painter_time.drawText(x_temp, 43, self.time_str + " HRs")
        painter_time.end()
        self.timefr.setPixmap(pixmap_time.scaled(173, 63))

    def load_html_file(self, url):
            self.web_view = QWebEngineView(self)
            self.web_view.setGeometry(QRect(191, 33, 619, 288))
            self.web_view.setUrl(QUrl(url))
            self.web_view.show()

    def ImageUpdateSlot(self, image):
        frame_image = QPixmap("/home/veadesh/Agnirath/GUI/Beaglebone/Dashboard/assets/Rearviewframe.png")
        overlay_image = QImage(frame_image.size(), QImage.Format_ARGB32)
        # overlay_image.fill(Qt.transparent)

        painter = QPainter(overlay_image)
        painter.drawPixmap(0, 0, frame_image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.drawImage(5, 5, image)
        painter.end()

        self.camera_label.setPixmap(QPixmap.fromImage(overlay_image))

    def Mainwindow(self):
        self.button1_clicked = True
        self.load_html_file("http://127.0.0.1:5500/GUI/Beaglebone/Dashboard/mapV2.html")
        self.camera_label.setGeometry(QRect(185, 340, 631 , 230))
        self.hide()
        self.button1_clicked = False

    def Temps(self):
        self.button2_clicked = True
        self.hide()
        self.button2_clicked = False
        

    def Current(self):
        self.button3_clicked = True
        self.hide()
        self.button3_clicked = False
        
    def CPanel(self):
        self.button4_clicked = True
        self.hide()
        self.button4_clicked = False

class Camera(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_image = cv2.flip(image, 1)
                convert_to_qt_format = QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0],
                                              QImage.Format_RGB888)
                pic = convert_to_qt_format.scaled(620, 215)
                self.ImageUpdate.emit(pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
