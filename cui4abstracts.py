
from cui4colors import color_dic

class SelfAware:
    def __init__(self, nametag=None):
        self.nametag = nametag if nametag else 'unnamed'

    def genealogy(self):
        ancestors_types = type(self).mro()[1:-2]
        ancestors_names = [getattr(each, '__name__') for each in ancestors_types]
        return (type(self).__name__ +
                ', descendant of '*bool(ancestors_names)+', '.join(ancestors_names))

    def about(self):
        print(self.nametag+'\n'+self.genealogy()+
              ('\n'+str(self))*(not str(self).endswith('>')))

    def __repr__(self):
        return type(self).__name__+'('+self.nametag+')'
        
    def __str__(self):
        return '"no strings attached"'

########################################################################################

class Rectangle:
    def __init__(self, height, width, position_y=0, position_x=0,
                 location=None, limit_y=None, limit_x=None,
                 background_color=None, text_color=None):
        self.h     = height
        self.w     = width
        self.pos_y = position_y
        self.pos_x = position_x
        self.loc   = location
        self.lim_y = limit_y
        self.lim_x = limit_x
        self.col_b = background_color
        self.col_t = text_color

        if location and not limit_y: self.lim_y = location.h
        if location and not limit_x: self.lim_x = location.w


    def __repr__(self):
        
        class_name = type(self).__name__
        height     = str(self.h)
        width      = str(self.w)
        position_y = str(self.pos_y)
        position_x = str(self.pos_x)

        if not self.loc: location = 'None'
        else: location = (type(self.loc).__name__ +'('+ str(self.loc.h)
                                                 +', '+ str(self.loc.w) +')')
        limit_y = str(self.lim_y)
        limit_x = str(self.lim_x)
        background_color = color_dic[self.col_b]
        text_color       = color_dic[self.col_t]

        return class_name +'('+ ', '.join([height, width, position_y, position_x,
                                           location, limit_y, limit_x, 
                                           background_color, text_color]) +')'

########################################################################################

class Movable:

    #def up(self, step=1):
    #    if step == 1:
    #        cur_time = time()
    #        if self.prev_move == 'u' and cur_time-self.prev_time<3 and self.turbo_counter > 4:
    #            step = 2
    #        if self.prev_move == 'u': self.turbo_counter += 1
    #        else: self.turbo_counter = 0
    #        self.prev_time = cur_time
    #        self.last_move = 'u'
    #    self.pos_y = self.pos_y-step if self.pos_y-step>=0 else 0

    def up(self, step=1):
        self.pos_y -= step
        self.layer.redraw = True

    def down(self, step=1):
        self.pos_y += step
        self.layer.redraw = True

    def right(self, step=1):
        self.pos_x += step
        self.layer.redraw = True

    def left(self, step=1):
        self.pos_x -= step
        self.layer.redraw = True
