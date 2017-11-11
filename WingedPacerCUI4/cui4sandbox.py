
from cui4colors  import *
from cui4cursor  import *
from cui4charms  import *
from cui4classes import *


c = Control('Main', H, W)

Board(c, background_color=OL_)
c.sbrd = c.brds[0]
c.brds[0].own_keys['F1'] = ()
Board(c, 4, 60, TL_, BK, 'Teal Board')

c()