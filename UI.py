import sys
from math import cos, sin, tan, acos, asin, log, atan, pi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageColor
from PIL import ImageDraw


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 200, 620, 700)  # Размер окна
        self.setWindowTitle('Чертила')
        # For func (title)
        self.func_parameters = QLabel(self)
        self.yiszero = QLabel(self)
        self.wherexisnotz = QLabel(self)
        self.xiszero = QLabel(self)
        self.whereyisnotz = QLabel(self)
        self.func = QLineEdit(self)
        self.button_main = QPushButton(self)
        self.func_out = QLabel(self)
        self.upload = QCheckBox(self)
        self.upload_text = QLabel(self)
        self.upload_line = QLineEdit(self)
        self.second_func_box = QCheckBox(self)
        self.second_func_out = QLabel(self)
        self.second_func = QLineEdit(self)
        self.second_func_param = QLabel(self)
        # For func2 (parameters)
        self.second_func_param.setText('Here will be parameters(2)')
        self.second_func_param.move(315, 50)
        self.second_func_param.resize(500, 20)
        self.second_func_param.hide()
        # Func input
        self.func.resize(200, 25)
        self.func.move(105, 5)
        # button
        self.button_main.resize(100, 30)
        self.button_main.move(450, 625)
        self.button_main.setText('Выполнить')
        self.button_main.clicked.connect(self.output)
        # text
        self.func_out.setText('Функция: ')
        self.func_out.move(35, 7)
        # For upload box
        self.upload.move(269, 95)
        self.upload_text.move(20, 95)
        self.upload_text.setText('Скачать изображение в указанную папку')
        self.upload.clicked.connect(self.upload_it)
        self.upload_line.move(290, 95)
        self.upload_line.hide()
        self.upload_line.resize(200, 20)
        # for second func
        self.second_func_box.move(82, 50)
        self.second_func_box.clicked.connect(self.show_line)
        self.second_func_out.move(15, 50)
        self.second_func_out.setText('Функция 2:')
        self.second_func.resize(200, 25)
        self.second_func.hide()
        self.second_func.move(105, 45)
        # For func parameters
        self.func_parameters.setText('Here will be parameters')
        self.func_parameters.move(315, 10)
        self.func_parameters.resize(500, 20)
        ###########################################
        self.pixmap = QPixmap('graphic.png')
        self.imag = QLabel(self)
        self.imag.move(40, 200)
        self.imag.resize(300,
                         400)

    def show_line(self, tog):
        if tog:
            self.second_func.show()
            self.second_func_param.show()
        else:
            self.second_func.hide()
            self.second_func_param.hide()

    def upload_it(self, st):
        if st:
            self.upload_line.show()
            fname = QFileDialog.getSaveFileName(self, 'Как сохранить', '')[0]
            self.upload_line.setText(fname)
        else:
            self.upload_line.hide()

    def output(self):
        width = 400
        height = 300

        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        # Заполним все изображение белым цветом
        draw.rectangle((0, 0, width - 1, height - 1),
                       fill=ImageColor.getrgb("white"),
                       outline=ImageColor.getrgb("grey"))

        def function1(x, func):
            try:
                mtext = func
                # mo и последущие 18 строк помогают вам написать числа без знака умножения
                mo = mtext.count('x')  # количество х
                for i in range(mo):
                    mark = (mtext.find('x')) - 1  # символ, стоящий за х
                    if mark >= 0:
                        if mtext[mark] in [' ', '+', '-', '*', '/', '(', ')']:  # проверка
                            mtext = mtext.replace('^', '**')
                        else:  # если это число - делается вот это
                            x *= int(mtext[mark])
                            mtext = list(mtext)
                            mtext[mark] = ''
                            mtext = ''.join(mtext)
                            mtext = mtext.replace('^', '**')
                    else:  # если х стоит в начале
                        mtext = mtext.replace('^', '**')
                mtext = mtext.split()
                mtext = ''.join(mtext)  # сбор в одну общую да
                try:
                    return eval(mtext)
                except SyntaxError:
                    return 0
            except NameError:
                self.func.setText('Ошибка!!')

        class Point:  # класс точек (для удобства)
            def __init__(self, x, y):
                self.x = x
                self.y = y

        # задаем область значений функции

        start_x = -width / 100
        end_x = -start_x
        start_y = -height / 20
        end_y = -start_y

        points = []  # points for 1st func
        points2 = []  # points for 2nd func

        x = start_x
        step_x = 0.1

        while x <= end_x:  # проходим по всей ширине
            y = function1(x, self.func.text())  # вычисляем значение функции для текущего значения x
            y1 = function1(x, self.second_func.text())  # тоже самое
            points.append(Point(x, y))  # добавляем эту точки в список точек
            points2.append(Point(x, y1))
            x += step_x  # увеличиваем x

        def convert(p):  # конвертирование моих точек в картиночку
            scale_x = width / (end_x - start_x)
            scale_y = height / (end_y - start_y)

            local_x = p.x * scale_x
            local_y = p.y * scale_y

            local_x = (-start_x * scale_x) + local_x
            local_y = (-start_y * scale_y) + local_y

            return Point(local_x, height - local_y)

        # оси
        start_hor = convert(Point(start_x, 0))
        end_hor = convert(Point(end_x, 0))
        draw.line((start_hor.x, start_hor.y, end_hor.x, end_hor.y),
                  fill=ImageColor.getrgb("grey"))

        start_ver = convert(Point(0, start_y))
        end_ver = convert(Point(0, end_y))
        draw.line((start_ver.x, start_ver.y, end_ver.x, end_ver.y),
                  fill=ImageColor.getrgb("grey"))
        # единицы на осях
        draw.text((width / 2 + start_x * 2, height / 2 + start_y),
                  '1',
                  fill=ImageColor.getrgb('black'),
                  )
        draw.text((width / 2, height / 2 + end_x * 0.5),
                  '-1',
                  fill=ImageColor.getrgb('black'))

        # рисуем на экране все точки.

        last_point = convert(points[0])
        last_point2 = convert(points2[0])
        for point in points:
            current_point = convert(point)
            draw.line((last_point.x, last_point.y, current_point.x, current_point.y),
                      fill=ImageColor.getrgb("blue"))
            last_point = current_point
        ########## 2 func #############
        try:
            for point in points2:
                current_point = convert(point)
                draw.line((last_point2.x, last_point2.y, current_point.x, current_point.y),
                          fill=ImageColor.getrgb("red"))
                last_point2 = current_point
        except SyntaxError:
            return None
        #########################
        if len(self.upload_line.text()) == 0:
            image.save("graphic.png", "PNG")
            self.update()
        else:
            image.save(f"{self.upload_line.text()}.png", "PNG")
            self.update()

        #########################

        def func_parameters(func):  # что за функция блин
            if '**' in func or '^' in func:
                return [0, 'Квадратичная функция, график - парабола']
            elif '/' in func and func.find('/') < func.find('x'):
                return [1, 'Степенная функция, график - гипербола']
            elif "log" in func:
                return [2, 'Логарифмическая функция, график - логарифмика']
            elif "sin" in func:
                return [3, 'Тригонометрическая функция, график - синусоид']
            elif "cos" in func:
                return [4, 'Тригонометрическая функция, график - косинусоид']
            elif "tan" in func:
                return [5, 'Тригонометрическая функция, график - тангенсоид']
            elif "atan" in func:
                return [6, 'Тригонометрическая функция, график - котангенсоид']
            elif "asin" in func:
                return [7, 'Тригонометрическая функция, график - арксинусойд']
            elif "acos" in func:
                return [8, 'Тригонометрическая функция, график - арккосинусоид']
            else:
                return [9, 'Линейная функция, график - прямая']

        self.func_parameters.setText(func_parameters(self.func.text())[1])
        self.second_func_param.setText(func_parameters(self.second_func.text())[1])

    def update(self):
        self.pixmap = QPixmap('graphic.png')
        self.imag.setText('')
        self.imag.setPixmap(self.pixmap)
        self.imag.resize(400,
                         300)


def except_hook(cls, exception, traceback):
    return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
