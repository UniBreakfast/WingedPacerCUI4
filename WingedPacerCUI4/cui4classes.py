
from cui4charms    import *
from cui4abstracts import *
from cui4keycatch  import *

class Control(Rectangle, SelfAware):
    def __init__(self, nametag, height, width):
        Rectangle.__init__(self, height, width)
        SelfAware.__init__(self, nametag)
        self.vps = []           # все вьюпорты
        self.brds = []          # все доски
        ViewPort(self)          # вьюпорт по умолчанию
        self.avp = self.vps[0]  # активный вьюпорт
        self.sbrd = None        # стартовая доска
        self.vp_mode = False    # режим управлению активным вьюпортом

        def switch_mode():
            if self.avp.brd_mode: self.avp('F4')
            if self.vp_mode:
                self.avp.overlay = CharMap(1, 1)
            else:
                self.avp.overlay = CharMap(self.h, self.w).inscribe(
                ' ViewPort control mode: Tab, Ctrl+Tab, Left, Right, Up, Down, Esc,'
                ' Enter ', 48, 0, None, GN)
            self.avp.redraw = True
            self.vp_mode = not self.vp_mode

        self.vp_keys = ['F4']
        self.own_keys = {'F3': switch_mode, 'F2': (print, '\a')}
        self.mode_keys = {'Tab': (), 'Ctrl+Tab': (), 'Left': (), 'Right': (), 'Up': (),
                          'Down': (), 'F3': switch_mode, 'Esc': switch_mode,
                          'Enter': switch_mode, 'F2': ()}



    def __call__(self):
        self.avp()
        while True:
            if self.vp_mode: own_keys = self.mode_keys
            else:            own_keys = self.own_keys

            key = catch_key(list(own_keys) + self.vp_keys)
            if key in list(own_keys):
                if type(own_keys[key]) is tuple:
                    own_keys[key][0] ( own_keys[key][1] )
                else: own_keys[key] ()
            else:
                self.vp_keys = self.avp(key)
            self.avp()

    def change_keys(set): pass

    def resize(self, side=('up','down','left','right'), amount=1):
        if side == 'up':
            self.h += amount
            for each in self.vps + self.brds:
                each.pos_y += amount
                if type(each) is Board:    each.layer.redraw = True
        elif side == 'down':
            self.h += amount
            for each in self.brds:    each.layer.redraw = True
        elif side == 'left':
            self.w += amount
            for each in self.vps + self.brds:
                each.pos_x += amount
                if type(each) is Board:    each.layer.redraw = True
        elif side == 'right':
            self.w += amount
            for each in self.brds:    each.layer.redraw = True



########################################################################################

class ViewPort(Rectangle, SelfAware):
    def __init__(self, control):
        Rectangle.__init__(self, H, W, control.h//2-H//2, control.w//2-W//2, control)
        SelfAware.__init__(self, 'ViewPort '+str(len(control.vps)))
        control.vps.append(self)
        self.c = control
        self.brds = control.brds
        self.abrd = self.brds[0] if self.brds else None
        self.redraw = True
        self.brd_mode = False
        self.layers = [board.layer for board in control.brds]
        self.overlay = CharMap(1, 1)
        self.underlay = CharMap(control.h, control.w, str(len(control.vps)),
                                BK_, GR, ' ', 4, 7)
        def switch_mode():
            if self.c.vp_mode: self.c.vp_mode = False
            if self.brd_mode:
                self.overlay = CharMap(1, 1)
            else:
                self.overlay = CharMap(self.h, self.w).inscribe(
                ' Board control mode: Tab, Ctrl+Tab, Left, Right, Up, Down, Esc,'
                ' Enter ', 48, 0, None, YL)
            self.redraw = True
            self.brd_mode = not self.brd_mode

        def next():
            current = self.brds.index(self.abrd)
            if self.brds.index(self.abrd):
                self.abrd = self.brds[current-1]
            else: self.abrd = self.brds[-1]
            self.layers = [self.abrd.layer]+self.layers[:current]+self.layers[current:]
            self.redraw = True

        self.brd_keys = []
        self.own_keys = {'F4': switch_mode, 'F2': (print, '\a')}
        self.mode_keys = {'Tab': next, 'Ctrl+Tab': (),
                          'Left': (self.move, 'left'), 'Right': (self.move, 'right'),
                          'Up': (self.move, 'up'), 'Down': (self.move, 'down'),
                          'F4': switch_mode, 'Esc': switch_mode, 'Enter': switch_mode,
                          'F2': ()}



    def __call__(self, key=None):
        if key:
            self.do(key)
            if self.brd_mode: return list(self.mode_keys) + self.brd_keys
            else:             return list(self.own_keys)  + self.brd_keys
        else:    self.show()

    def do(self, key):
        own_keys = self.mode_keys if self.brd_mode else self.own_keys
        if key in list(own_keys):
            if type(own_keys[key]) is tuple:
                own_keys[key][0] ( own_keys[key][1] )
            else: own_keys[key] ()
        else:
            self.brd_keys = self.abrd(key)

    def show(self):
        if self.redraw:
            self.frame = CharMap(self.h, self.w).stamp(self.overlay)
            for layer in self.layers:
                self.frame = self.frame.view_through(layer(),self.pos_y,self.pos_x)
            try: self.frame = self.frame.view_through(self.underlay,self.pos_y,self.pos_x)
            except:
                self.underlay = CharMap(self.c.h, self.c.w, str(self.c.vps.index(self)+1),
                                        BK_, GR, ' ', 4, 7)
                self.frame = self.frame.view_through(self.underlay,self.pos_y,self.pos_x)

            #self.frame = CharMap(self.c.h, self.c.w)
            #self.frame.stamp(self.underlay)
            #for layer in self.layers:
            #    self.frame.stamp(layer())
            #self.frame.stamp(self.overlay)
            #self.frame.crop(self.h, self.w, self.pos_y, self.pos_x)
            self.redraw = False
        self.frame()

    def move(self, side=('up','down','left','right'), amount=1):
        if side == 'up':
            self.abrd.pos_y -= amount
            if self.abrd.pos_y < 0:
                shift = 0-self.abrd.pos_y
                self.c.resize('up', shift);    self.abrd.pos_y = 0
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True
        elif side == 'down':
            self.abrd.pos_y += amount
            if self.abrd.pos_y + amount + self.abrd.h >= self.c.h:
                self.c.resize('down', self.abrd.pos_y + amount + self.abrd.h - self.c.h)
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True
        elif side == 'left':
            self.abrd.pos_x -= amount
            if self.abrd.pos_x < 0:
                self.c.resize('left', -self.abrd.pos_x);    self.abrd.pos_x = 0
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True
        elif side == 'right':
            self.abrd.pos_x += amount
            if self.abrd.pos_x + amount + self.abrd.w >= self.c.w:
                self.c.resize('right', self.abrd.pos_x + amount + self.abrd.w - self.c.w)
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True
########################################################################################

class Board(Rectangle, SelfAware):
    def __init__(self, control, height=10, width=30, background_color=None,
                 text_color=None, name=None, title=None, centered=False):
        if not len(control.brds) or centered:
            position_y = control.avp.h//2 - height//2 + control.avp.pos_y
            position_x = control.avp.w//2 -  width//2 + control.avp.pos_x
        else:
            mask = CharMap(control.h, control.w)
            for board in control.brds:
                mask.stamp(board.layer())
            position_y, position_x = mask.nearby(control.avp.abrd.pos_y,
                control.avp.abrd.pos_x, control.avp.abrd.h, control.avp.abrd.w,
                height, width)
            if position_y < 0:
                control.resize('up', -position_y);   position_y = 0
            if position_x < 0:
                control.resize('left', -position_x); position_x = 0
            if position_y + height > control.h:
                control.resize('down', position_y + height - control.h)
            if position_x + width > control.w:
                control.resize('right', position_x + width - control.w)

        Rectangle.__init__(self, height, width, position_y, position_x, control,
                           None, None, background_color, text_color)
        SelfAware.__init__(self, name)

        control.brds.append(self)
        for viewport in control.vps:
            if not viewport.abrd: viewport.abrd = self
        self.c = control
        self.own_keys = {}

        self.layer = Layer(self)
        self.redraw = True

        #TODO Сделать, чтобы новые доски появлялись либо в центре, либо в нужном месте
        #TODO рядом с текущей

    def __call__(self, key=None):
        if key:
            self.do(key)
            return list(self.own_keys)
        else:    return self.render()

    def do(self, key):
        function  = self.own_keys[key][0]
        arguments = self.own_keys[key][1]
        function(arguments)

    def render(self):
        if self.redraw:
            self.frame = CharMap(self.h, self.w, ' ', self.col_b, self.col_t)
            self.frame.inscribe(self.nametag)
            self.redraw = False
        return self.frame

########################################################################################

class Layer(Rectangle, SelfAware):
    def __init__(self, board):
        Rectangle.__init__(self, board.c.h, board.c.w)
        SelfAware.__init__(self, 'layer for '+board.nametag)
        self.b = board
        self.redraw = True
        # будучи созданным, слой добавляет себя во все вьюпорты
        for vieport in board.c.vps:
            vieport.layers.append(self)

    def __call__(self):
        if self.redraw:
            self.h = self.b.c.h;    self.w = self.b.c.w
            self.frame = CharMap(self.h, self.w)
            self.frame.stamp(self.b(), self.b.pos_y, self.b.pos_x)
            self.redraw = False
        return self.frame

########################################################################################

class Button(): pass

class Field(): pass

class Label(): pass


