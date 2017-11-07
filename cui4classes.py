
from cui4charms    import *
from cui4abstracts import *
from cui4keycatch  import *

class Control(Rectangle, SelfAware): 
    def __init__(self, nametag, height, width):
        Rectangle.__init__(self, height, width)
        SelfAware.__init__(self, nametag)
        self.vps = []
        self.avp = None
        self.brds = []
        self.sbrd = None
        self.vp_mode = False

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
        if not self.vps: ViewPort(self)
        self.avp = self.vps[0]
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
        
        #TODO Сделать, чтобы доски двигались не дальше символа от существующих
        def up():
            self.abrd.pos_y -= 1
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True
        
        def down():
            self.abrd.pos_y += 1
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True
        
        def right():
            self.abrd.pos_x += 1
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True
        
        def left():
            self.abrd.pos_x -= 1
            self.abrd.layer.redraw = True
            for viewport in self.c.vps: viewport.redraw = True

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
                          'Left': left, 'Right': right, 'Up': up, 'Down': down,
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
            self.frame = self.frame.view_through(self.underlay,self.pos_y,self.pos_x)

            #self.frame = CharMap(self.c.h, self.c.w)
            #self.frame.stamp(self.underlay)
            #for layer in self.layers:
            #    self.frame.stamp(layer())
            #self.frame.stamp(self.overlay)
            #self.frame.crop(self.h, self.w, self.pos_y, self.pos_x)
            self.redraw = False
        self.frame()

########################################################################################

class Board(Rectangle, SelfAware):
    def __init__(self, control, height=10, width=30, position_y=None, position_x=None,
                 background_color=None, text_color=None, name=None):
        if position_y is None: position_y = control.h//2-height//2 
        if position_x is None: position_x = control.w//2-width//2 
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

    def __call__(self):
        if self.redraw:
            self.frame = CharMap(self.h, self.w)
            self.frame.stamp(self.b(), self.b.pos_y, self.b.pos_x)
            self.redraw = False
        return self.frame

########################################################################################

class Button(): pass

class Field(): pass

class Label(): pass


