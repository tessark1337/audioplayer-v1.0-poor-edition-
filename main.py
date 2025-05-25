import sys
import os
import pygame
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsBlurEffect, QWidget
from PyQt5.QtCore import QTimer, QTime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design/audioplayer.ui', self) 

        self.blurOverlay = QWidget(self)
        self.blurOverlay.setGeometry(self.rect())
        self.blurOverlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
        self.blurOverlay.setVisible(False)

        pygame.mixer.init()
        self.playing = False
        self.last_url = None 
        
        self.lcdtimer = QTimer()
        self.lcdtimer.timeout.connect(self.lcd_timer)
        self.lcdtimer.timeout.connect(self.update_slider)
        self.time_counter = 1

        self.recordPlayer.setHidden(True)

        self.add.clicked.connect(self.add_music)

        self.play.clicked.connect(self.play_music)
        self.stop.clicked.connect(self.stop_music)

        self.prev.clicked.connect(self.prev_music)
        self.next.clicked.connect(self.next_music)

        self.temporaryTrack.setRange(0, 100)
        self.temporaryTrack.valueChanged.connect(self.change_music_position)

        self.closeWidget.clicked.connect(self.close)

        self.musicList.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.audioVolume.valueChanged.connect(self.set_volume)

    def lcd_timer(self):
        time = QTime(self.time_counter // 3600, self.time_counter // 60,
                     self.time_counter % 60)
        text = time.toString('hh:mm:ss')
        self.timer.display(text)
        self.time_counter += 1 

        if self.time_counter == round(self.sound.get_length()):
            self.time_counter = 0
            self.playing = False
            self.last_url = None

            self.lcdtimer.stop()
    
    def add_music(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, 'Выберите музыку', ':\\',
            'Аудио (*.mp3;*.mpeg;*.ogg)')
        if files:
            for file in files:
                self.musicList.addItem(file)
    
    def on_item_double_clicked(self):
        self.recordPlayer.setHidden(False)
        music = self.musicList.selectedItems()

        if music:
            new_url = music[0].text()
            self.musicName.setText(new_url)
 

    def play_music(self):
        music = self.musicName.text()
        if music != self.last_url:
            pygame.mixer.music.load(music)
            self.last_url = music
            pygame.mixer.music.play()
            self.sound = pygame.mixer.Sound(music) 

            self.time_counter = 1
        else:
            pygame.mixer.music.unpause()
        self.lcdtimer.start(1000)
        self.playing = True   
        

    def stop_music(self):
        if self.playing:
            self.lcdtimer.stop()
            pygame.mixer.music.pause()      

    def prev_music(self):
        current_element = self.musicList.currentRow()
        self.musicList.setCurrentRow(current_element - 1)
        if (current_element - 1) != -1:
            prev_item = self.musicList.item(current_element - 1)

            if prev_item:
                new_url = prev_item.text()
                self.musicName.setText(new_url)
                self.play_music()

    def next_music(self):
        current_element = self.musicList.currentRow()
        self.musicList.setCurrentRow(current_element + 1)
        if (current_element + 1) != -1:
            next_item = self.musicList.item(current_element + 1)

            if next_item:
                new_url = next_item.text()
                self.musicName.setText(new_url)
                self.play_music()

    def update_slider(self): 
        percentage = int((self.time_counter / self.sound.get_length()) * 100)
        self.temporaryTrack.setValue(percentage)       

    def change_music_position(self, pos):
        self.temporaryTrack.setValue(pos)
       

    def set_volume(self):
        volume = round(self.audioVolume.value() / 100, 3)
        pygame.mixer.music.set_volume(volume)   

    def close(self):
        self.recordPlayer.setHidden(True)   
        self.lcdtimer.stop()    
        if self.playing:  
            pygame.mixer.music.pause()
              

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())        