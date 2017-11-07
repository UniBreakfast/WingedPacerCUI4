
# импортирую функцию для быстрого преобразования
# двухмерной последовательности в одномерную
from itertools import chain


# импортирую свои модули для работы с цветами и позиционирования курсора в консоли
from cui4colors import *
from cui4cursor import *


# 2 константы (и алиасы для них), задающие пропорции окна консоли по умолчанию
H=MAX_HEIGHT = 50;     W=MAX_WIDTH = 80

# альтернатива: пропорции задаёт пользователь перед началом работы с программой
#try: H=MAX_HEIGHT = int(input(' введите целое положительное число, по умолчанию 50\n'
#                              'Высота окна консоли в строках = '))
#except: print('выбор непонятен, взято значение по умолчанию 50')
#try: W=MAX_WIDTH = int(input(' введите целое положительное число, по умолчанию 80\n'
#                             'Ширина окна консоли в символах = '))
#except: print('выбор непонятен, взято значение по умолчанию 80')


# Класс посимвольных карт изображения (прямоугольников) для консольного интерфейса
# Кайждая символьная карта может быть измененеа в памяти и затем выведена на экран
class CharMap(list):
    
    # Символьная карта может быть создана несколькими вариантами:
    # - без параметров - прозрачный прямоугольник предполагаемых размеров экрана
    # - с указанием заполнителя - надписи, которой он будет покрыт
    # - с указанием цвета надписи и фона - без них будут цвета по умолчанию
    # - с указанием расстояния между образцами заполнителя и символа,
    #   которым это расстояние будет заполнено, можно с указанием его цвета
    def __init__(self, height=MAX_HEIGHT, width=MAX_WIDTH,
                 filler=None, background_color=None, text_color=None, spacing=None,
                 vertical_spacing=0, horizontal_spacing=0, spacing_color=None):
        self.h = height
        self.w = width
        if not spacing_color: spacing_color = text_color

        if not (spacing or vertical_spacing or horizontal_spacing): 
            no_spacing = True
        else: 
            no_spacing = False

        if not filler:
            charmap = [[(None, None, None)]*width for row in range(height)]

        elif len(filler)==1 and no_spacing:
            charmap = [[(background_color, text_color, filler)]*width 
                       for row in range(height)]

        elif len(filler)>1 and no_spacing:
            charmap = CharMap(height, width)
            for row in range(height):
                for pattern in range(0, width, len(filler)):
                    charmap.inscribe(filler, row, pattern, 
                                     background_color, text_color, 'crop')
        else: 
            charmap = CharMap(height, width, spacing, background_color, spacing_color)
            for row in range(vertical_spacing, height, vertical_spacing+1):
                for pattern in range(horizontal_spacing, width, len(filler)+
                                     horizontal_spacing):
                    charmap.inscribe(filler, row, pattern, 
                                     background_color, text_color, 'skip')





        list.__init__(self, charmap)

    # Метод создаёт копию данной символьной карты, являющуюся другим объектом
    def copy(self):
        return CharMap(self.h, self.w).stamp(self)


    # Метод позволяет сделать на карте надпись в указанном месте, с заданным
    # цветом и фоном. Также можно указать, как быть, если надпись не помещается:
    # обрезать, перенести на следующую строку, перенести под начало этой строки,
    # расширить карту на сколько нужно, уместить, начав писать раньше, пропустить
    def inscribe(self, text, position_y=0, position_x=0,
                 background_color=None, text_color=None,
                 exceeds=('crop', 'wrap', 'indent', 'extend', 'fit', 'skip')):
        y=position_y;   b_col=background_color
        x=position_x;   t_col=text_color

        if exceeds == 'fit' and x+len(text) > self.w and len(text) <= self.w:
            x = self.w-len(text)

        elif exceeds == 'skip' and x+len(text) > self.w: return self

        elif exceeds == 'extend':
            extended_self = CharMap(self.h, x+len(text))
            extended_self.stamp(self)
            extended_self.inscribe(text, y, x, b_col, text_color)
            self.clear()
            self+=extended_self
            self.w = extended_self.w
            return self

        if background_color and text_color:
            for i, char in enumerate(text):
                try:
                    self[y][x+i] = (b_col, t_col, char)
                except:
                    if exceeds == 'crop': break
                    elif exceeds == 'wrap': y+=1; x=0-i
                    elif exceeds == 'indent': y+=1; x=position_x-i
                    self[y][x+i] = (b_col, t_col, char)

        elif background_color:
            for i, char in enumerate(text):
                try:
                    self[y][x+i] = (b_col, self[y][x+i][1], char)
                except:
                    if exceeds == 'crop': break
                    elif exceeds == 'wrap': y+=1; x=0-i
                    elif exceeds == 'indent': y+=1; x=position_x-i
                    self[y][x+i] = (b_col, self[y][x+i][1], char)
                
        elif text_color:
            for i, char in enumerate(text):
                try:
                    self[y][x+i] = (self[y][x+i][0], t_col, char)
                except:
                    if exceeds == 'crop': break
                    elif exceeds == 'wrap': y+=1; x=0-i
                    elif exceeds == 'indent': y+=1; x=position_x-i
                    self[y][x+i] = (self[y][x+i][0], t_col, char)

        else:
            for i, char in enumerate(text):
                try:
                    self[y][x+i] = (self[y][x+i][0], self[y][x+i][1], char)
                except:
                    if exceeds == 'crop': break
                    elif exceeds == 'wrap': y+=1; x=0-i
                    elif exceeds == 'indent': y+=1; x=position_x-i
                    self[y][x+i] = (self[y][x+i][0], self[y][x+i][1], char)
        return self

    # Метод позволяет сделать на карте отпечаток другой карты в указанном месте
    # Также можно указать, как быть, если отпечаток не помещается:
    # обрезать, расширить карту на сколько нужно, уместить, поместив отпечаток раньше,
    # пропустить, не делая непомещающийся отпечаток
    def stamp(self, charmap, position_y=0, position_x=0,
              exceeds=('crop', 'extend', 'fit', 'skip')):
        y=position_y; x=position_x
        
        if exceeds == 'fit':
            if y+charmap.h > self.h and charmap.h <= self.h:
               y = self.h - charmap.h
            if x+charmap.w > self.w and charmap.w <= self.w:
               x = self.w - charmap.w

        elif exceeds == 'skip' and (y+charmap.h>self.h or x+charmap.w>self.w): 
            return self

        elif exceeds == 'extend':
            extended_self = CharMap(y+charmap.h, x+charmap.w)
            extended_self.stamp(self)
            extended_self.stamp(charmap, y, x)
            self.clear()
            self+=extended_self
            self.h = extended_self.h;   self.w = extended_self.w
            return self

        for j, line in enumerate(charmap):
            for i, char in enumerate(line):
                try:
                    if not char[2]: pass
                    elif char[0]: self[y+j][x+i] = char
                    else: self[y+j][x+i] = (self[y+j][x+i][0], char[1], char[2])
                except:
                    if exceeds == 'crop': break
                    raise IndexError('charmap does not fit')
        return self

    # Метод возвращает новую символьную карту, являющуюся снимком сверху для
    # данной символьной карты, положенной сверху на переданную в качестве параметра
    def topview(self, charmap):
        tvc_h = self.h if self.h>=charmap.h else charmap.h
        tvc_w = self.w if self.w>=charmap.w else charmap.w
        tv_charm = CharMap(tvc_h, tvc_w)
        tv_charm.stamp(charmap)
        tv_charm.stamp(self)
        return tv_charm


    # Метод возвращает новую символьную карту, являющуюся снимком сверху для
    # данной символьной карты, положенной сверху на переданную в качестве параметра
    # и обрезанную по размерам и положению верхней
    def view_through(self, charmap, position_y=0, position_x=0):
        return charmap.copy().crop(self.h, self.w, position_y, position_x).stamp(self)


    # Метод обрезает карту до указанного размера (или какой получится, если не указан)
    # Левым верхним углом оставшейся части будет символ с указанными координатами
    def crop(self, new_height=None, new_width=None, position_y=0, position_x=0):
        y=position_y;   x=position_x
        
        new_height = new_height if new_height else self.h-y
        new_width  = new_width  if new_width  else self.w-x

        y_cropped_charm = self[y:y+new_height]
        cropped_charm = []
        for line in y_cropped_charm: cropped_charm.append(line[x:x+new_width])
        self.clear()
        self+=cropped_charm
        self.h = len(self);     self.w = len(self[0])
        return self


    # Метод обрезает карту с каждой стороны на сколько указано
    def crop_edge(self, top=0, bottom=0, left=0, right=0):
        y_cropped_charm = self[top:self.h-bottom]
        cropped_charm = []
        for line in y_cropped_charm: cropped_charm.append(line[left:self.w-right])
        self.clear()
        self+=cropped_charm
        self.h = len(self);     self.w = len(self[0])
        return self


    # Метод расширяет карту, дотачивая прозрачными краями до указанного размера
    # (или какой получится, если не указан)
    # Левый верхний угол будет в указанных координатах
    def extend(self, new_height=None, new_width=None, position_y=0, position_x=0):
        y=position_y;   x=position_x

        new_height = new_height if new_height else self.h+y
        new_width  = new_width  if new_width  else self.w+x

        extended_charm = CharMap(new_height, new_width)
        extended_charm.stamp(self, y, x)
        self.clear()
        self+=extended_charm
        return self


    # Метод расширяет карту с каждой стороны на сколько указано, дотачивая прозрачным
    def extend_edge(self, top=0, bottom=0, left=0, right=0):

        new_height = self.h + top + bottom
        new_width  = self.w + left + right

        extended_charm = CharMap(new_height, new_width)
        extended_charm.stamp(self, top, left)
        self.clear()
        self+=extended_charm
        return self

        
    # Метод выводит карту в консоль поверх того, что уже выведено, в указанном месте
    # или в начале, если место не указано. Позиционирование вывода может быть
    # относительно начала следующей строки за позицией курсора.
    def show(self, position_y=0, position_x=0, relative=False):
        y=position_y;   x=position_x

        preshow = self
        if y or x:
            preshow = CharMap(y+self.h, x+self.w)
            preshow.stamp(self, y, x)
        
        if preshow.w<W:
            extended_preshow = CharMap(preshow.h, W)
            extended_preshow.stamp(preshow)
            preshow = extended_preshow
        
        if preshow.h<H:
            extended_preshow = CharMap(H, preshow.w)
            extended_preshow.stamp(preshow)
            preshow = extended_preshow

        if preshow.w-W or preshow.h-H: preshow.crop(H, W)

        linear = list(chain(*preshow))
        first_match=True
        for i, char in enumerate(linear[1:]):
            if first_match:
                if char[0] == linear[i][0] and char[1] == linear[i][1]:
                    linear[i+1] = [linear[i+1][2]]
                    first_match=False
                    j = i
            else:
                if char[0] == linear[j][0] and char[1] == linear[j][1]:
                    linear[i+1] = [linear[i+1][2]]
                else:
                    first_match=True
        char_list=[]
        
        right=0; down=0; cur_x=0
        for char in linear:
            
            if char[0] is None:
                if   right<W-1-cur_x: right+=1
                else: down+=1; right=0; cur_x=0
            else: 
                charstring = (d(down)+'\r')*bool(down)+r(right)*bool(right)+''.join(char)
                cur_x = cur_x+right+1
                if cur_x==80: cur_x=0
                right=0; down=0
                char_list.append(charstring)

        if not relative: curto()
        else: print()
        
        print(end=''.join(char_list))
        

    # Метод выводит карту в консоль полноэкранным кадром, замещая прежний вывод
    # Карта может быть выведена в указанном месте экрана.
    def show_instead(self, position_y=0, position_x=0):
        y=position_y;   x=position_x
        
        preshow = self
        if y or x:
            preshow = CharMap(y+self.h, x+self.w)
            preshow.stamp(self, y, x)
        
        if preshow.w<W:
            extended_preshow = CharMap(preshow.h, W)
            extended_preshow.stamp(preshow)
            preshow = extended_preshow
        
        if preshow.h<H:
            extended_preshow = CharMap(H, preshow.w)
            extended_preshow.stamp(preshow)
            preshow = extended_preshow

        if preshow.w-W or preshow.h-H: preshow.crop(H, W)

        linear = list(chain(*preshow))
        first_match=True
        for i, char in enumerate(linear[1:]):
            if first_match:
                if char[0] == linear[i][0] and char[1] == linear[i][1]:
                    linear[i+1] = [linear[i+1][2]]
                    first_match=False
                    j = i
            else:
                if char[0] == linear[j][0] and char[1] == linear[j][1]:
                    linear[i+1] = [linear[i+1][2]]
                else:
                    first_match=True
        char_list=[]
        first_None=True
        for char in linear:
            charstring = ''.join((cell for cell in char if not cell is None))
            if charstring:
                first_None=True
            elif first_None: 
                charstring = RC+' '
                first_None=False
            else: charstring = ' '
            char_list.append(charstring)
        
        del char_list[-1]
        
        curto()
        print(end=''.join(char_list))
        curto()


    # Вызов карты по умолчанию будет выводить её полноэкранным кадром
    def __call__(self, position_y=0, position_x=0):
        self.show_instead(position_y, position_x)



####   участок для тестирования   ####################################################

if __name__ == '__main__':
    pass

