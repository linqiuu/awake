import json
import os
import shutil
import sys
from datetime import datetime
from time import sleep

from PyQt5.QtWidgets import QApplication, QWidget
from ui import awake, pre

score_map = {'left': 5, 'middle': 3, 'right': 1}
default_wait_time = 30 * 60
close_per_wait_time = 60 * 60
init_file = "data/display.json"
summary_file = "data/summary.txt"


def reminder_init():
    with open(init_file, encoding="utf-8") as f:
        res = json.load(f)['reminder']
    awake_ui.display1.append(res['left'])
    awake_ui.display2.append(res['middle'])
    awake_ui.display3.append(res['right'])


def clear_reminder_count():
    awake_ui.spinBox.setValue(0)
    awake_ui.spinBox_2.setValue(0)
    awake_ui.spinBox_3.setValue(0)


def input_init():
    with open(init_file, encoding="utf-8") as f:
        res = json.load(f)['input_template']
    awake_ui.plainTextEdit.setPlainText(res)


def calc_score():
    score = awake_ui.spinBox.value() * score_map['left'] + awake_ui.spinBox_2.value() * score_map[
        'middle'] + awake_ui.spinBox_3.value() * score_map['right']
    awake_ui.scoreLcdNumber.display(score)


def get_score():
    return awake_ui.scoreLcdNumber.value()


def clear_score():
    awake_ui.scoreLcdNumber.display(0)


def save_summary():
    cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = awake_ui.plainTextEdit.toPlainText()
    with open(summary_file, mode="a", encoding="utf-8") as f:
        f.write(f"{cur_time}\n{text}\n\n")
    input_init()


def close_pre():
    global show_flag
    show_flag = True
    preWindow.close()


def close_and_wait():
    global wait_time
    preWindow.close()
    count = pre_ui.waitCount.value()
    if count > 0:
        wait_time = count * close_per_wait_time


def pre_ui_clear():
    global show_flag, wait_time
    show_flag = False
    wait_time = default_wait_time
    pre_ui.waitCount.setValue(0)


def save_summary_and_clear(date_time):
    score = get_score()
    with open(summary_file, mode="a", encoding="utf-8") as f:
        f.write(f"总分数：{score}\n")
    name, suffix = os.path.splitext(summary_file)
    shutil.move(summary_file, f'{name}_{date_time.strftime("%Y-%m-%d")}{suffix}')
    clear_reminder_count()
    clear_score()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wait_time = default_wait_time
    show_flag = False
    pre_day = datetime.now().date()

    mainWindow = QWidget()
    awake_ui = awake.Ui_Form()
    awake_ui.setupUi(mainWindow)

    awake_ui.spinBox.valueChanged.connect(calc_score)
    awake_ui.spinBox_2.valueChanged.connect(calc_score)
    awake_ui.spinBox_3.valueChanged.connect(calc_score)
    awake_ui.pushButton.clicked.connect(save_summary)

    preWindow = QWidget()
    pre_ui = pre.Ui_Form()
    pre_ui.setupUi(preWindow)

    pre_ui.buttonOpen.clicked.connect(close_pre)
    pre_ui.buttonClose.clicked.connect(close_and_wait)

    reminder_init()
    input_init()

    while True:
        preWindow.show()
        app.exec()
        if show_flag:
            cur_day = datetime.now().date()
            if cur_day != pre_day:
                save_summary_and_clear(pre_day)
                pre_day = cur_day
            mainWindow.show()
            app.exec()
        sleep(wait_time)
        pre_ui_clear()
