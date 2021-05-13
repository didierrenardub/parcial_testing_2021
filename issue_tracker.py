import os
import sys
import json
import time
import platform

def read_input():
    return input()

def print_wrapper(to_p):
    print(to_p, end='')
    sys.stdout.flush()

from ctypes import Structure, c_long, c_ulong, c_short, c_ushort, byref

class ConsoleCoord(Structure):
    _fields_ = [
    ("X", c_short),
    ("Y", c_short)]

class ConsoleRect(Structure):
    _fields_ = [
    ("Left", c_short),
    ("Top", c_short),
    ("Right", c_short),
    ("Bottom", c_short)]

class ConsoleBuffer(Structure):
    _fields_ = [
    ("dwSize", ConsoleCoord),
    ("dwCursorPosition", ConsoleCoord),
    ("wAttributes", c_ushort),
    ("srWindow", ConsoleRect),
    ("dwMaximumWindowSize", ConsoleCoord)]

class WRAP_MODE:
    TRUNCATE = 0
    WORD = 1

class ALIGNMENT:
    BEGIN = 0
    CENTER = 1
    END = 2

class COLOR:
    BLACK = 0
    BLUE = 1
    GREEN = 2
    CYAN = 3
    RED = 4
    MAGENTA = 5
    YELLOW = 6
    GRAY = 7
    DARK_GRAY = 8
    LIGHT_BLUE = 9
    LIGHT_GREEN = 10
    LIGHT_CYAN = 11
    LIGHT_RED = 12
    LIGHT_MAGENTA = 13
    LIGHT_YELLOW = 14
    WHITE = 15
    TRANSPARENT = 16

if platform.system() == 'Windows':
    class CONSOLE_COLOR_BASE:
        BLACK = 0x00
        BLUE = 0x01
        GREEN = 0x02
        CYAN = 0x03
        RED = 0x04
        MAGENTA = 0x05
        YELLOW = 0x06
        GRAY = 0x07
        INTENSITY = 0x08
else:
    class CONSOLE_COLOR_BASE:
        BLACK = 0x00
        RED = 0x01
        GREEN = 0x02
        YELLOW = 0x03
        BLUE = 0x04
        MAGENTA = 0x05
        CYAN = 0x06
        GRAY = 0x07
        INTENSITY = 0x08

class CONSOLE_COLOR(CONSOLE_COLOR_BASE):
    color = CONSOLE_COLOR_BASE.GRAY | ((CONSOLE_COLOR_BASE.BLACK << 4) & 0xF0)

    @staticmethod
    def translate(c):
        if c is COLOR.BLACK:
            return CONSOLE_COLOR.BLACK
        elif c is COLOR.BLUE:
            return CONSOLE_COLOR.BLUE
        elif c is COLOR.GREEN:
            return CONSOLE_COLOR.GREEN
        elif c is COLOR.CYAN:
            return CONSOLE_COLOR.CYAN
        elif c is COLOR.RED:
            return CONSOLE_COLOR.RED
        elif c is COLOR.MAGENTA:
            return CONSOLE_COLOR.MAGENTA
        elif c is COLOR.YELLOW:
            return CONSOLE_COLOR.YELLOW
        elif c is COLOR.GRAY:
            return CONSOLE_COLOR.GRAY
        elif c is COLOR.DARK_GRAY:
            return CONSOLE_COLOR.BLACK | CONSOLE_COLOR.INTENSITY
        elif c is COLOR.LIGHT_BLUE:
            return CONSOLE_COLOR.BLUE | CONSOLE_COLOR.INTENSITY
        elif c is COLOR.LIGHT_GREEN:
            return CONSOLE_COLOR.GREEN | CONSOLE_COLOR.INTENSITY
        elif c is COLOR.LIGHT_CYAN:
            return CONSOLE_COLOR.CYAN | CONSOLE_COLOR.INTENSITY
        elif c is COLOR.LIGHT_RED:
            return CONSOLE_COLOR.RED | CONSOLE_COLOR.INTENSITY
        elif c is COLOR.LIGHT_MAGENTA:
            return CONSOLE_COLOR.MAGENTA | CONSOLE_COLOR.INTENSITY
        elif c is COLOR.LIGHT_YELLOW:
            return CONSOLE_COLOR.YELLOW | CONSOLE_COLOR.INTENSITY
        elif c is COLOR.WHITE:
            return CONSOLE_COLOR.GRAY | CONSOLE_COLOR.INTENSITY
        
        return COLOR.TRANSPARENT

    @staticmethod
    def translate_fb(f, b):
        return CONSOLE_COLOR.translate(f) | ((CONSOLE_COLOR.translate(b) << 4) & 0xF0)

    @staticmethod
    def colors():
        return CONSOLE_COLOR.color

    @staticmethod
    def set_colors(c):
        CONSOLE_COLOR.color = c
        if platform.system() == 'Windows':
            try:
                import msvcrt
                import ctypes
                handle = msvcrt.get_osfhandle(sys.stdout.fileno())
                ctypes.windll.kernel32.SetConsoleTextAttribute(handle, c)
            except:
                pass
        else:
            bgc = 0
            fgc = 30 + (c & 0xF & ~CONSOLE_COLOR.INTENSITY)
            if (((c & 0xF0) >> 4) & CONSOLE_COLOR.INTENSITY) != 0:
                bgc = 100 + (((c & 0xF0) >> 4) & ~CONSOLE_COLOR.INTENSITY)
            else:
                bgc = 0 + ((c & 0xF0) >> 4)

            if ((c & 0xF) & CONSOLE_COLOR.INTENSITY) != 0:
                print_wrapper("\033[%d;%d;1m" % (bgc, fgc))
            else:
                print_wrapper("\033[%d;%dm" % (bgc, fgc))
            #if (c & 0xF0) is not 0:
            #print_wrapper("\033[4%d;3%dm" % (((c & 0xF0) & ~(CONSOLE_COLOR.INTENSITY << 4)) >> 4, (c & 0x0F) & ~CONSOLE_COLOR.INTENSITY))
            #print_wrapper("\033[%d;3%dm" % (102, (c & 0x0F) & ~CONSOLE_COLOR.INTENSITY))
            #else:
                #print_wrapper("\033[3%dm" % ((c & 0x0F) & ~CONSOLE_COLOR.INTENSITY))

def set_cursor_position(pos):
    if platform.system() == 'Windows':
        try:
            import msvcrt
            import ctypes
            handle = msvcrt.get_osfhandle(sys.stdout.fileno())
            ctypes.windll.kernel32.SetConsoleCursorPosition(handle, c_ulong(pos.x() + (pos.y() << 16)))
        except Exception as e:
            print(str(e))
    else:
        if pos.x() < 0 or pos.y() < 0:
            pass
        print_wrapper('\033[%d;%dH' % (pos.y() + 1, pos.x() + 1))

def set_cursor_x_y(x, y):
    set_cursor_position(Position(x, y))

class Position:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def set(self, x, y):
        self.set_x(x)
        self.set_y(y)
        return self

    def x(self):
        return self._x

    def set_x(self, x):
        self._x = x
        return self

    def y(self):
        return self._y

    def set_y(self, y):
        self._y = y
        return self

class Size:
    def __init__(self, w=0, h=0):
        self._w = w
        self._h = h

    def set(self, w, h):
        self.set_width(w)
        self.set_height(h)
        return self

    def width(self):
        return self._w

    def set_width(self, w):
        self._w = w
        return self

    def height(self):
        return self._h

    def set_height(self, h):
        self._h = h
        return self

class UIColor:
    def __init__(self, c=COLOR.TRANSPARENT):
        self._c = c
    
    def get(self):
        return self._c

    def set(self, c):
        self._c = c
        return self

    @staticmethod
    def black():
        return UIColor(COLOR.BLACK)

    @staticmethod
    def blue():
        return UIColor(COLOR.BLUE)
    
    @staticmethod
    def green():
        return UIColor(COLOR.GREEN)

    @staticmethod
    def cyan():
        return UIColor(COLOR.CYAN)

    @staticmethod
    def red():
        return UIColor(COLOR.RED)
    
    @staticmethod
    def magenta():
        return UIColor(COLOR.MAGENTA)

    @staticmethod
    def yellow():
        return UIColor(COLOR.YELLOW)

    @staticmethod
    def gray():
        return UIColor(COLOR.GRAY)

    @staticmethod
    def dark_gray():
        return UIColor(COLOR.DARK_GRAY)

    @staticmethod
    def light_blue():
        return UIColor(COLOR.LIGHT_BLUE)

    @staticmethod
    def light_green():
        return UIColor(COLOR.LIGHT_GREEN)

    @staticmethod
    def light_cyan():
        return UIColor(COLOR.LIGHT_CYAN)

    @staticmethod
    def light_red():
        return UIColor(COLOR.LIGHT_RED)

    @staticmethod
    def light_magenta():
        return UIColor(COLOR.LIGHT_MAGENTA)

    @staticmethod
    def light_yellow():
        return UIColor(COLOR.LIGHT_YELLOW)

    @staticmethod
    def white():
        return UIColor(COLOR.WHITE)

    @staticmethod
    def transparent():
        return UIColor(COLOR.TRANSPARENT)

class UIElement:
    def __init__(self):
        self._fore = UIColor.gray()
        self._back = UIColor.transparent()
        self._pos = Position()
        self._size = Size()
        self._max_size = Size()
        self._clip_pos = Position()
        self._clip_size = Size()
        self._clip_children = False
        self._clip_tl_offset = Position()
        self._clip_br_offset = Position()
        self._children = []
        self._parent = None
        self._visible = True

    def fore_color(self):
        return self._fore

    def set_fore_color(self, c):
        self._fore = c
        return self

    def back_color(self):
        return self._back
    
    def set_back_color(self, c):
        self._back = c
        return self

    def absolute_position(self):
        p = Position(self.position().x(), self.position().y())
        parent = self.parent()
        while parent is not None:
            p.set(p.x() + parent.position().x(), p.y() + parent.position().y())
            parent = parent.parent()
        return p

    def position(self):
        return self._pos

    def set_position(self, p):
        self._pos = p
        return self
        
    def set_x_y(self, x, y):
        self._pos.set_x(int(x))
        self._pos.set_y(int(y))
        return self

    def size(self):
        return self._size

    def set_size(self, s):
        self._size = s
        self._check_size()
        return self

    def set_w_h(self, w, h):
        self._size.set_width(int(w))
        self._size.set_height(int(h))
        self._check_size()
        return self

    def size_to_fit_children(self):
        max_x = 0
        max_y = 0

        for child in self.children():
            right_edge = child.position().x() + child.size().width()
            if right_edge > max_x:
                max_x = right_edge
            bottom_edge = child.position().y() + child.size().height()
            if bottom_edge > max_y:
                max_y = bottom_edge

        self.set_w_h(max_x, max_y)

    def max_size(self):
        return self._max_size

    def set_max_size(self, s):
        self._max_size = s
        self._check_size()
        return self

    def set_max_w_h(self, w, h):
        self._max_size.set_width(w)
        self._max_size.set_height(h)
        self._check_size()
        return self

    def right(self):
        return self.position().x() + self.size().width()

    def bottom(self):
        return self.position().y() + self.size().height()

    def children(self):
        return self._children

    def add_child(self, c):
        self._children.append(c)
        c._parent = self
        return self

    def remove_child(self, c):
        c._parent = None
        self._children.remove(c)

    def clear_children(self):
        for child in self.children():
            child._parent = None
        self._children = []

    def remove_from_parent(self):
        if self.parent() is not None:
            self.parent().remove_child(self)

    def render(self):
        old_colors = CONSOLE_COLOR.colors()
        colors = CONSOLE_COLOR.translate_fb(self.fore_color().get(), self.back_color().get())

        if self.back_color() == COLOR.TRANSPARENT:
            colors = CONSOLE_COLOR.translate(self.fore_color().get()) | (old_colors & 0xF0)
        if self.fore_color() == COLOR.TRANSPARENT:
            colors = CONSOLE_COLOR.translate(self.back_color().get()) & 0x0F

        set_cursor_position(self.absolute_position())
        CONSOLE_COLOR.set_colors(colors)

        self.draw()

        me_cp = self.clip_position()
        me_cp.set(me_cp.x() + self.clip_tl_offset().x(), me_cp.y() + self.clip_tl_offset().y())
        me_cs = self.clip_size()
        me_cs.set(me_cs.width() - self.clip_br_offset().x(), me_cs.height() - self.clip_br_offset().y())

        if me_cs.width() <= 0:
            me_cs.set_width(self.size().width() - self.clip_br_offset().x())
        if me_cs.height() <= 0:
            me_cs.set_height(self.size().height() - self.clip_br_offset().y())

        edge = Position(me_cs.width() + me_cp.x(), me_cs.height() + me_cp.y())

        for child in self.children():
            if not child.visible():
                continue
            c_pos = child.position()
            c_size = child.size()
            old_cp = child.clip_position()
            old_cs = child.clip_size()

            if not self.clip_children() or c_pos.x() + c_size.width() >= me_cp.x() or c_pos.x() <= self.size().width():
                if self.clip_children() and (c_pos.x() > me_cp.x() + me_cs.width() or c_pos.x() + c_size.width() < me_cp.x() or c_pos.y() > me_cp.y() + me_cs.height() or c_pos.y() + c_size.height() < me_cp.y()):
                    continue

                new_cp = Position()
                new_cs = Size()

                if c_pos.x() < me_cp.x():
                    diff = me_cp.x() - c_pos.x()
                    if diff < old_cp.x():
                        new_cp.set_x(old_cp.x())
                    else:
                        new_cp.set_x(diff)
                    
                    if old_cs.width() == 0:
                        new_cs.set_width(me_cs.width())
                    else:
                        old_right_clip = old_cp.x() + old_cs.width()
                        new_cs.set_width(old_right_clip - new_cp.x())
                
                if c_pos.x() + c_size.width() > edge.x():
                    new_cp.set_x(old_cp.x())

                    if old_cs.width() == 0 or new_cp.x() + old_cs.width() >= edge.x():
                        new_cs.set_width(edge.x() - new_cp.x())
                    else:
                        new_cs.set_width(old_cs.width())

                if c_pos.y() < me_cp.y():
                    diff = me_cp.y() - c_pos.y()
                    if diff < old_cp.y():
                        new_cp.set_y(old_cp.y())
                    else:
                        new_cp.set_y(diff)
                    
                    if old_cs.height() == 0:
                        new_cs.set_height(me_cs.height())
                    else:
                        old_bottom_clip = old_cp.y() + old_cs.height()
                        new_cs.set_height(old_bottom_clip - new_cp.y())

                if c_pos.y() + c_size.height() > edge.y():
                    new_cp.set_y(old_cp.y())

                    if old_cs.width() == 0 or new_cp.y() + old_cs.height() >= edge.y():
                        new_cs.set_height(edge.y() - new_cp.y())
                    else:
                        new_cs.set_height(old_cs.height())

                if self.clip_children():
                    child.set_clip(new_cp, new_cs)
                
                child.render()

                if self.clip_children():
                    child.set_clip(old_cp, old_cs)

        CONSOLE_COLOR.set_colors(old_colors)

    def draw(self):
        print_wrapper('UIElement::draw() NOT IMPLEMENTED!!!')

    def clip_position(self):
        return self._clip_pos

    def clip_size(self):
        return self._clip_size

    def set_clip(self, pos, size):
        self._clip_pos = pos
        self._clip_size = size
        return self

    def set_clip_area(self, x, y, w, h):
        self._clip_pos.set_x(x)
        self._clip_pos.set_y(y)
        self._clip_size.set_width(w)
        self._clip_size.set_height(h)
        return self

    def clip_children(self):
        return self._clip_children

    def set_clip_children(self, c):
        self._clip_children = c
        return self

    def clip_tl_offset(self):
        return self._clip_tl_offset

    def clip_br_offset(self):
        return self._clip_br_offset

    def set_clip_offsets(self, top, left, bottom, right):
        self._clip_tl_offset.set_x(left)
        self._clip_tl_offset.set_y(top)
        self._clip_br_offset.set_x(right)
        self._clip_br_offset.set_y(bottom)
        return self

    def visible(self):
        return self._visible

    def set_visible(self, v):
        self._visible = v
        return self

    def parent(self):
        return self._parent

    def _check_size(self):
        if self.size().width() > self.max_size().width() and self.max_size().width() > 0:
            self._size.set_width(self.max_size().width())

        if self.size().height() > self.max_size().height() and self.max_size().height() > 0:
            self._size.set_height(self.max_size().height())

class UIInterface(UIElement):
    def __init__(self):
        UIElement.__init__(self)

    def draw(self):
        if self.back_color() is not COLOR.TRANSPARENT:
            pos = self.absolute_position()

            c_pos = Position(self.clip_position().x() + pos.x(), pos.y() + self.clip_position().y())
            c_size = self.clip_size()

            if c_size.width() == 0:
                c_size.set_width(self.size().width() + pos.x() - c_pos.x())

            if c_size.height() == 0:
                c_size.set_height(self.size().height() + pos.y() - c_pos.y())
            
            buffer = ''
            for _ in range(c_pos.x() - pos.x(), c_size.width()):
                buffer = buffer + ' '
            
            if pos.y() >= c_pos.y():
                set_cursor_position(c_pos)
                print_wrapper(buffer)
                buffer = ''

            for _ in range(c_pos.x() - pos.x(), c_size.width()):
                buffer = buffer + ' '
            
            for i in range(c_pos.y() - pos.y() + 1, c_size.height()):
                set_cursor_position(Position(c_pos.x(), c_pos.y() + i))
                print_wrapper(buffer)

            buffer = ''

            for _ in range(c_pos.x() - pos.x(), c_size.width()):
                buffer = buffer + ' '

            if pos.y() + self.size().height() <= c_pos.y() + c_size.height():
                set_cursor_position(Position(pos.x(), pos.y() + self.size().height() - 1))
                print_wrapper(buffer)

class Frame(UIElement):
    def __init__(self):
        UIElement.__init__(self)
        self._v_border = '|'
        self._h_border = '-'
        self._corner = '+'
        self.set_back_color(UIColor.black())

    @staticmethod
    def with_graphics(v_b='|', h_b='-', c='+'):
        f = Frame()
        f._v_border = v_b
        f._h_border = h_b
        f._corner = c
        return f

    @staticmethod
    def with_fore(f_c):
        f = Frame()
        f.set_fore_color(f_c)
        return f

    @staticmethod
    def with_rect(pos, size):
        f = Frame()
        f.set_position(pos)
        f.set_size(size)
        return f

    @staticmethod
    def with_xywh(x, y, w, h):
        f = Frame()
        f.set_x_y(x, y)
        f.set_w_h(w, h)
        return f

    @staticmethod
    def with_fore_rect(c, pos, size):
        f = Frame()
        f.set_fore_color(c)
        f.set_position(pos)
        f.set_size(size)
        return f

    @staticmethod
    def with_fore_xywh(c, x, y, w, h):
        f = Frame()
        f.set_fore_color(c)
        f.set_x_y(x, y)
        f.set_w_h(w, h)
        return f

    def draw(self):
        pos = self.absolute_position()

        c_pos = Position(self.clip_position().x() + pos.x(), pos.y() + self.clip_position().y())
        c_size = self.clip_size()

        if c_size.width() == 0:
            c_size.set_width(self.size().width() + pos.x() - c_pos.x())

        if c_size.height() == 0:
            c_size.set_height(self.size().height() + pos.y() - c_pos.y())

        buffer = ''
        for i in range(0, self.size().width()):
            if i == 0 or i == self.size().width() - 1:
                buffer = buffer + self.corner()
            else:
                buffer = buffer + self.horizontal_border()

        set_cursor_position(Position(pos.x(), pos.y()))
        print_wrapper(buffer)
        buffer = ''

        for j in range(self.size().width()):
            if j == 0 or j == self.size().width() - 1:
                buffer = buffer + self.vertical_border()
            else:
                buffer = buffer + ' '

        for i in range(self.size().height() - 1):
            set_cursor_position(Position(pos.x(), pos.y() + i + 1))

            if self.back_color().get() is not COLOR.TRANSPARENT:
                print_wrapper(buffer)
            elif self.fore_color().get() is not COLOR.TRANSPARENT:
                print_wrapper(buffer[0])
                set_cursor_position(Position(pos.x() + len(buffer) - 1, pos.y() + i + 1))
                print_wrapper(buffer[-1])

        buffer = ''

        for i in range(self.size().width()):
            if i == 0 or i == self.size().width() - 1:
                buffer = buffer + self.corner()
            else:
                buffer = buffer + self.horizontal_border()

        set_cursor_position(Position(pos.x(), pos.y() + self.size().height() - 1))
        print_wrapper(buffer)

    def vertical_border(self):
        return self._v_border

    def set_vertical_border(self, v_b):
        self._v_border = v_b
        return self

    def horizontal_border(self):
        return self._h_border

    def set_horizontal_border(self, h_b):
        self._h_border = h_b
        return self

    def corner(self):
        return self._corner

    def set_corner(self, c):
        self._corner = c
        return self
    
    def set_graphics(self, v_b, v_h, c):
        self.set_vertical_border(v_b)
        self.set_horizontal_border(v_h)
        self.set_corner(c)
        return self

    def size_to_fit_children(self):
        UIElement.size_to_fit_children(self)
        self.set_w_h(self.size().width() + 1, self.size().height() + 1)
        return self

class Label(UIElement):
    def __init__(self):
        UIElement.__init__(self)
        self._text = ''
        self._t_v_align = ALIGNMENT.BEGIN
        self._t_h_align = ALIGNMENT.BEGIN
        self._wrap = WRAP_MODE.WORD
        self._multiline = True

    @staticmethod
    def with_text(t):
        l = Label()
        l.set_text(t)
        return l

    @staticmethod
    def with_rect(p, s):
        l = Label()
        l.set_position(p)
        l.set_size(s)
        return l

    @staticmethod
    def with_xywh(x, y, w, h):
        l = Label()
        l.set_x_y(x, y)
        l.set_w_h(w, h)
        return l

    @staticmethod
    def with_text_rect(t, p, s):
        l = Label()
        l.set_text(t)
        l.set_position(p)
        l.set_size(s)
        return l

    @staticmethod
    def with_text_xywh(t, x, y, w, h):
        l = Label()
        l.set_text(t)
        l.set_x_y(x, y)
        l.set_w_h(w, h)
        return l

    def draw(self):
        pos = self.absolute_position()
        buffer = ''

        if self.back_color().get() is not COLOR.TRANSPARENT:
            for y in range(0, self.size().height()):
                set_cursor_position(Position(pos.x() + self.clip_position().x(), pos.y() + y))

                min_x = pos.x()
                max_w = self.size().width()
                if self.clip_position().x() != 0:
                    min_x = self.clip_position().x()
                if self.clip_size().width() != 0:
                    max_w = min(self.clip_size().width(), self.size().width())
                
                for _ in range(min_x, min_x + max_w):
                    buffer = buffer + ' '
                
                if self.clip_size().height() == 0 or (y >= self.clip_position().y() and y < self.clip_position().y() + self.clip_size().height()):
                    print_wrapper(buffer)
                buffer = ''

        buffer = ''
        set_cursor_x_y(pos.x(), pos.y())

        lines = []
        last_char_idx = 0

        while last_char_idx < len(self.text()):
            if len(lines) == 0 or ((len(lines[-1]) + len(buffer) > self.size().width()) and len(lines) < self.size().height()):
                lines.append('')
            elif ((len(lines) > 0 and len(lines[-1]) + len(buffer) > self.size().width() and (not self.multiline() or len(lines) >= self.size().height()))):
                break

            next = self.text()[last_char_idx]
            if next == '\n' and self.multiline():
                if self.wrap_mode() == WRAP_MODE.WORD:
                    lines[-1] = lines[-1] + buffer
                    buffer = ''
                lines.append('')
                last_char_idx = last_char_idx + 1
                continue
            
            if self.wrap_mode() == WRAP_MODE.TRUNCATE:
                lines[-1] = lines[-1] + next
            elif self.wrap_mode() == WRAP_MODE.WORD:
                if next == ' ':
                    if len(lines) == 0:
                        lines.append(buffer)
                    else:
                        lines[-1] = lines[-1] + buffer + next
                    buffer = ''
                else:
                    buffer = buffer + next
            last_char_idx = last_char_idx + 1
        
        if not buffer == '':
            if (len(lines) == 0 or ((len(lines[-1]) + len(buffer) >= self.size().width() and self.multiline() and len(buffer) <= self.size().width() and len(lines) < self.size().height()))):
                lines.append(buffer)
            elif len(lines) > 0 and len(lines[-1]) + len(buffer) <= self.size().width() and (self.wrap_mode() == WRAP_MODE.TRUNCATE or last_char_idx >= len(self.text())):
                lines[-1] = lines[-1] + buffer

        for i in range(0, len(lines)):
            line_start_x = 0
            line_start_y = 0

            r = lines[i]
            if self.wrap_mode() == WRAP_MODE.TRUNCATE:
                r = r.rstrip()
            
            if self.text_h_align() == ALIGNMENT.CENTER:
                line_start_x = (self.size().width() / 2 - len(r) / 2)
            elif self.text_h_align() == ALIGNMENT.END:
                line_start_x = self.size().width() - len(r)

            if self.text_v_align() == ALIGNMENT.CENTER:
                line_start_y = (self.size().height() / 2 - len(lines) / 2)
            elif self.text_v_align() == ALIGNMENT.END:
                line_start_y = self.size().height() - len(lines)

            sub_idx = 0
            sub_len = len(r)
            if line_start_x <= self.clip_position().x():
                sub_idx = self.clip_position().x() - line_start_x
                line_start_x = self.clip_position().x()
                sub_len = sub_len - sub_idx

            if not self.clip_size().width() == 0 and line_start_x + sub_len >= self.clip_position().x() + self.clip_size().width():
                sub_len = sub_len - self.clip_position().x() + self.clip_size().width() - (line_start_x + sub_len)

            test_clip_y = line_start_y + i
            print_y = pos.y() + test_clip_y
            set_cursor_x_y(pos.x() + int(line_start_x), int(print_y))

            if print_y >= 0 and sub_len > 0 and (self.clip_size().height() == 0 or (test_clip_y >= self.clip_position().y() and test_clip_y < self.clip_position().y() + self.clip_size().height())):
                print_wrapper(r[int(sub_idx):(int(sub_idx) + int(sub_len))])

    def text(self):
        return self._text

    def set_text(self, t):
        self._text = t
        self.set_w_h(len(t), 1)
        return self

    def size_to_fit_text(self):
        self.set_w_h(len(self.text()), 1)
        return self

    def text_v_align(self):
        return self._t_v_align

    def set_text_v_align(self, a):
        self._t_v_align = a
        return self
    
    def text_h_align(self):
        return self._t_h_align

    def set_text_h_align(self, a):
        self._t_h_align = a
        return self

    def multiline(self):
        return self._multiline

    def set_multiline(self, m):
        self._multiline = m
        return self

    def wrap_mode(self):
        return self._wrap

    def set_wrap_mode(self, w):
        self._wrap = w
        return self

    def _check_size(self):
        UIElement._check_size(self)

        buffer = ''
        lines = []
        last_char_idx = 0

        while last_char_idx < len(self.text()):
            if len(lines) == 0 or ((len(lines[-1]) + len(buffer) >= self.size().width() and self.multiline() and (self.max_size().height() == 0 or len(lines) < self.max_size().height()))):
                lines.append('')
            elif (len(lines) > 0 and len(lines[-1]) + len(buffer) >= self.size().width() and not self.multiline()) or (len(lines) > self.max_size().height() and not self.max_size().height() == 0):
                break

            next = self.text()[last_char_idx]

            if next == '\n' and self.multiline():
                if self.wrap_mode() == WRAP_MODE.WORD:
                    lines[-1] = lines[-1] + buffer
                    buffer = ''

                lines.append('')
                last_char_idx = last_char_idx + 1
                continue
            
            if self.wrap_mode() == WRAP_MODE.TRUNCATE:
                lines[-1] = lines[-1] + next
            elif self.wrap_mode() == WRAP_MODE.WORD:
                if next == ' ':
                    lines[-1] = lines[-1] + buffer + next
                    buffer = ''
                else:
                    buffer = buffer + next
            last_char_idx = last_char_idx + 1
        
        if not buffer == '':
            fits_in_line = len(lines[-1]) + len(buffer) <= self.size().width()
            buffer_fits = len(buffer) <= self.size().width()

            if len(lines) == 0 or (not fits_in_line and self.multiline() and buffer_fits and (self.max_size().height() == 0 or len(lines) < self.max_size().height())):
                lines.append(buffer)
            elif len(lines) > 0 and fits_in_line:
                lines[-1] = lines[-1] + buffer

        if len(lines) > self.size().height():
            self._size = Size(self.size().width(), len(lines))
        else:
            self._size = Size(self.size().width(), self.size().height())

        UIElement._check_size(self)

class TextField(Label):
    def __init__(self):
        Label.__init__(self)

    @staticmethod
    def with_text(t):
        tf = TextField()
        tf.set_text(t)
        return tf

    @staticmethod
    def with_text_rect(t, p, s):
        tf = TextField()
        tf.set_text(t)
        tf.set_position(p)
        tf.set_size(s)
        return tf
    
    @staticmethod
    def with_text_xywh(t, x, y, w, h):
        tf = TextField()
        tf.set_text(t)
        tf.set_x_y(x, y)
        tf.set_w_h(w, h)
        return tf

    def focus(self):
        pos = self.absolute_position()
        set_cursor_position(Position(pos.x() + len(self.text()), pos.y()))

    def read(self):
        self.focus()
        return read_input()

##########################################################
##########################################################
##########################################################

class Message():
    def __init__(self, message_type_id: int, payload: dict = None):
        self._type_id = message_type_id
        self._payload = payload if payload is not None else {}

    def type_id(self) -> int:
        return self._type_id

    def payload(self) -> dict:
        return self._payload

    def __getattr__(self, name):
        if name in self._payload:
            return self._payload[name]
        return None


class MessageBus():
    def __init__(self):
        self._subscriptors = {}

    def subscribe(self, message_type_id: int, callback):
        if message_type_id not in self._subscriptors:
            self._subscriptors[message_type_id] = []
        if callback not in self._subscriptors[message_type_id]:
            self._subscriptors[message_type_id].append(callback)

    def unsubscribe(self, message_type_id: int, callback):
        if message_type_id in self._subscriptors and callback in self._subscriptors[message_type_id]:
            self._subscriptors[message_type_id].remove(callback)
            return True
        elif message_type_id is None and callback is not None:
            for subscriptors in self._subscriptors.values():
                if callback in subscriptors:
                    subscriptors.remove(callback)
                    return True
        return False

    def post(self, message: Message):
        if message.type_id() in self._subscriptors:
            for subscriptor in self._subscriptors[message.type_id()]:
                subscriptor(message)


class Menu(UIElement):
    def __init__(self):
        UIElement.__init__(self)
        self._entries = []
        self._input = TextField()
        self._fallback_handler = None
        self._handlers = {}
        
    @staticmethod
    def with_entries(entries: list):
        m = Menu()
        m._entries = entries
        return m

    def draw(self):
        pass

    def layout(self):
        self.clear_children()
        prev = None
        for entry, index in zip(self._entries, range(len(self._entries))):
            l = Label.with_text_xywh(f'{index + 1} - {entry}', 0, prev.bottom() if prev is not None else 0, self.size().width(), 1)
            l.set_max_w_h(self.size().width(), -1).size_to_fit_text()
            self.add_child(l)
            prev = l
        self._input.set_text('> ')
        self._input.set_fore_color(UIColor.yellow())
        self._input.set_x_y(0, (prev.bottom() + 1) if prev is not None else 0)
        self._input.set_w_h(self.size().width(), 1)
        self.add_child(self._input)

    def read(self, message_bus: MessageBus) -> str:
        opt = self._input.read()
        for entry_index in range(len(self._entries)):
            if str(entry_index + 1) == opt:
                if opt in self._handlers:
                    self._handlers[opt]()
                return
        if self._fallback_handler is not None:
            self._fallback_handler(opt)

    def set_handler(self, value: str, handler):
        self._handlers[value] = handler

    def set_fallback_handler(self, handler):
        self._fallback_handler = handler

    def set_handlers(self, handler_map: dict):
        for k, v in handler_map.items():
            self._handlers[k] = v


class MessageBusTextField(TextField):
    def __init__(self):
        TextField.__init__(self)

    @staticmethod
    def with_text_xywh(t: str, x: int, y: int, w: int, h: int):
        b = MessageBusTextField()
        b.set_text(t)
        b.set_x_y(x, y)
        b.set_w_h(w, h)
        return b

    def read(self, message_bus: MessageBus):
        user_input = TextField.read(self)
        message_bus.post(Message(MESSAGE.USER_INPUT, { 'input': user_input }))


class Modal(UIInterface):
    def __init__(self):
        UIInterface.__init__(self)
        self.set_back_color(UIColor.black())
        self.set_w_h(80, 25)
        self._frame = Frame()
        self._frame.set_fore_color(UIColor.blue())
        self.add_child(self._frame)

    @staticmethod
    def with_text(text: str, text_color: UIColor = UIColor.light_red()):
        b = Modal()
        l = Label.with_text_xywh(text, 2, 2, 25, 10)
        l.set_fore_color(text_color)
        l.set_wrap_mode(WRAP_MODE.WORD)
        l.set_text_h_align(ALIGNMENT.CENTER)
        l.set_text_v_align(ALIGNMENT.CENTER)
        l.set_max_w_h(25, 10)
        l.size_to_fit_text()
        b._frame.add_child(l)
        b._frame.set_w_h(l.size().width() + 4, l.size().height() + 4)
        return b

    @staticmethod
    def with_content(content: UIElement):
        b = Modal()
        content.set_x_y(1, 1)
        b._frame.add_child(content)
        b._frame.set_w_h(content.size().width() + 2, content.size().height() + 2)
        return b


class AutoHandler():
    def __init__(self, message_bus: MessageBus, message_type: int, handler):
        self._message_bus = message_bus
        self._message_type = message_type
        self._handler = handler
        self._message_bus.subscribe(self._message_type, self.on_message)

    def on_message(self, message: Message):
        self._message_bus.unsubscribe(self._message_type, self.on_message)
        if self._handler(message):
            self._message_bus.subscribe(self._message_type, self.on_message)


class Screen():
    def __init__(self, message_bus: MessageBus):
        self._message_bus = message_bus

    def show(self):
        raise NotImplementedError()

    def modal_text(self, text: str, text_color: UIColor=UIColor.light_red()):
        self._message_bus.post(Message(MESSAGE.REQUEST_MODAL, { 'modal': Modal.with_text(text, text_color) }))

    def modal_content(self, content: UIElement):
        self._message_bus.post(Message(MESSAGE.REQUEST_MODAL, { 'modal': Modal.with_content(content) }))

    def screen(self, screen: 'Screen'):
        self._message_bus.post(Message(MESSAGE.REQUEST_SCREEN, { 'screen': screen }))

    def handle_result(self, message: Message, success_handler, failure_handler=None):
        AutoHandler(self._message_bus, MESSAGE.SUCCESS, success_handler)
        if failure_handler is not None:
            AutoHandler(self._message_bus, MESSAGE.FAILURE, failure_handler)
        self._message_bus.post(message)


class IssueTrackerScreen(Screen):
    def __init__(self, message_bus: MessageBus):
        Screen.__init__(self, message_bus)
        self._active_input = None
        self._current_ui = None

    def show(self):
        self._current_ui.render()
        if self._active_input is not None:
            self._active_input.read(self._message_bus)


class IssueTrackerMenuScreen(IssueTrackerScreen):
    def __init__(self, message_bus: MessageBus, title: str=None):
        IssueTrackerScreen.__init__(self, message_bus)
        self._current_ui = self.init_ui(title)

    def init_ui(self, title: str=None) -> UIElement:
        interface = UIInterface()
        interface.set_w_h(80, 25)

        f = Frame()
        f.set_w_h(40, 11)
        f.set_fore_color(UIColor.blue())

        l = None
        menu_position = 1
        if title is not None and title != '':
            l = centered_label(title, f.size().width(), 4)
            menu_position = l.bottom() + 1
            f.add_child(l)

        menu_data = self.menu_data()

        self._active_input = Menu.with_entries(menu_data.keys())
        self._active_input.set_x_y(2, menu_position)
        self._active_input.set_w_h(f.size().width() - 4, 1)
        for k, v in zip(range(len(menu_data)), menu_data.values()):
            self._active_input.set_handler(str(k + 1), v)
        self._active_input.layout()
        self._active_input.size_to_fit_children()

        f.add_child(self._active_input)
        f.size_to_fit_children()

        interface.add_child(f)

        return interface

    def menu_data(self) -> dict:
        raise NotImplementedError()


class InputUI(UIInterface):
    def __init__(self, label: str, on_input_handler):
        UIInterface.__init__(self)
        self._input_handler = on_input_handler
        self.set_w_h(80, 25)

        f = Frame()
        f.set_w_h(40, 5)
        f.set_fore_color(UIColor.blue())
        
        l = Label.with_text_xywh(label, 1, 1, f.size().width(), 2)
        f.add_child(l)
        self._active_input = MessageBusTextField.with_text_xywh('> ', 1, l.bottom(), l.size().width(), 1)
        self._active_input.set_fore_color(UIColor.yellow())
        f.add_child(self._active_input)

        self.add_child(f)

    def read(self, message_bus: MessageBus):
        AutoHandler(message_bus, MESSAGE.USER_INPUT, self._input_handler)
        self._active_input.read(message_bus)


class ChoiceUI(UIInterface):
    def __init__(self, label: str, choices: list, on_choice_handler):
        UIInterface.__init__(self)
        self._choice_handler = on_choice_handler
        self.set_w_h(80, 25)

        f = Frame()
        f.set_w_h(40, 5)
        f.set_fore_color(UIColor.blue())
        
        l = Label.with_text_xywh(label, 1, 1, f.size().width(), 2)
        f.add_child(l)

        self._active_input = Menu.with_entries(choices)
        self._active_input.set_x_y(2, l.bottom() + 1)
        self._active_input.set_w_h(f.size().width() - 4, 1)
        for k in range(len(choices)):
            opt = str(k + 1)
            self._active_input.set_handler(opt, self._make_choice_handler(opt))
        self._active_input.layout()
        self._active_input.size_to_fit_children()

        f.add_child(self._active_input)

        f.size_to_fit_children()

        self.add_child(f)

    def _make_choice_handler(self, opt: str):
        def choice_handler():
            self._choice_handler(Message(MESSAGE.USER_INPUT, { 'input': opt }))
        return choice_handler

    def read(self, message_bus: MessageBus):
        self._active_input.read(message_bus)


class MESSAGE():
    EXIT = 0
    SUCCESS = 1
    FAILURE = 2
    USER_INPUT = 3
    REQUEST_SCREEN = 4
    REQUEST_MODAL = 5
    NEW_PROJECT = 6
    PROJECTS = 7
    DELETE_PROJECT = 8
    NEW_ISSUE = 9
    EDIT_ISSUE = 10
    ISSUES = 11
    DELETE_ISSUE = 12


def centered_label(text: str, max_w: int, max_h: int, color: UIColor=UIColor.cyan()):
    l = Label.with_text(text)
    l.set_fore_color(color)
    l.set_max_w_h(max_w, max_h)
    l.set_x_y(max_w / 2 - l.size().width() / 2, 1)
    l.set_wrap_mode(WRAP_MODE.WORD)
    l.set_text_h_align(ALIGNMENT.CENTER)
    l.set_text_v_align(ALIGNMENT.CENTER)
    return l


class ScreenWelcome(IssueTrackerMenuScreen):
    def __init__(self, message_bus: MessageBus):
        IssueTrackerMenuScreen.__init__(self, message_bus, 'Issue Tracker')

    def menu_data(self) -> dict:
        return {
            'Abrir proyecto': lambda: self.screen(ScreenProjectOpen(self._message_bus)),
            'Crear proyecto': lambda: self._init_new_project_ui(),
            'Eliminar proyecto': lambda: self.screen(ScreenProjectDelete(self._message_bus)),
            'Salir' : lambda: self._message_bus.post(Message(MESSAGE.EXIT))
        }

    def _init_new_project_ui(self):
        self._current_ui = self._active_input = InputUI('Ingrese el nombre del nuevo proyecto:', self.on_new_project)

    def on_new_project(self, message: Message):
        if message.input is not None and message.input != '':
            self.handle_result(Message(MESSAGE.NEW_PROJECT, { 'name': message.input }), lambda m: self.screen(ScreenProjectMain(self._message_bus, message.input)), self.on_new_project_failed)
            return False
        self.modal_text('Debe ingresar un nombre para el proyecto')
        return True

    def on_new_project_failed(self, message: Message):
        self.modal_text('Error al intentar crear el proyecto; asegurese de usar un nombre que no se repita')


class ScreenProjectList(IssueTrackerMenuScreen):
    def __init__(self, message_bus: MessageBus, title: str, project_item_handler_builder):
        self._project_item_handler_builder = project_item_handler_builder
        IssueTrackerMenuScreen.__init__(self, message_bus, title)
        
    def menu_data(self) -> dict:
        self._projects = []
        def store_projects(message: Message):
            self._projects = message.projects
        self.handle_result(Message(MESSAGE.PROJECTS), store_projects, None)
        if len(self._projects):
            handlers = {}
            for project in self._projects:
                handlers[project] = self._project_item_handler_builder(project)
            handlers['Salir'] = lambda: self.screen(ScreenWelcome(self._message_bus))
            return handlers
        self.modal_text('Debe crear al menos un proyecto')
        self.screen(ScreenWelcome(self._message_bus))
        return {}


class ScreenProjectList(IssueTrackerMenuScreen):
    def __init__(self, message_bus: MessageBus, title: str, project_item_handler_builder):
        self._project_item_handler_builder = project_item_handler_builder
        IssueTrackerMenuScreen.__init__(self, message_bus, title)
        
    def menu_data(self) -> dict:
        self._projects = []
        def store_projects(message: Message):
            self._projects = message.projects
        self.handle_result(Message(MESSAGE.PROJECTS), store_projects, None)
        if len(self._projects):
            handlers = {}
            for project in self._projects:
                handlers[project] = self._project_item_handler_builder(project)
            handlers['Salir'] = lambda: self.screen(ScreenWelcome(self._message_bus))
            return handlers
        self.modal_text('Debe crear al menos un proyecto')
        self.screen(ScreenWelcome(self._message_bus))
        return {}


class ScreenProjectOpen(ScreenProjectList):
    def __init__(self, message_bus: MessageBus):
        ScreenProjectList.__init__(self, message_bus, 'Abrir proyecto', lambda project: lambda: self.screen(ScreenProjectMain(self._message_bus, project)))


class ScreenProjectDelete(ScreenProjectList):
    def __init__(self, message_bus: MessageBus):
        ScreenProjectList.__init__(self, message_bus, 'Eliminar proyecto', self._make_delete_func)

    def _make_delete_func(self, for_project: str):
        def delete_func():
            AutoHandler(self._message_bus, MESSAGE.SUCCESS, lambda message: self.modal_text(f'Proyecto "{for_project}" eliminado correctamente', UIColor.light_green()) is not None and self.screen(ScreenProjectDelete(self._message_bus)) is not None)
            self._message_bus.post(Message(MESSAGE.DELETE_PROJECT, { 'project': for_project }))
        return delete_func


class ScreenProjectMain(IssueTrackerMenuScreen):
    def __init__(self, message_bus: MessageBus, project_name: str):
        self._project = project_name
        IssueTrackerMenuScreen.__init__(self, message_bus, project_name)

    def menu_data(self) -> dict:
        return {
            'Nuevo reporte': lambda: self.screen(ScreenIssueEdit(self._message_bus, self._project)),
            'Editar reporte': lambda: self.screen(ScreenIssueOpen(self._message_bus, self._project)),
            #'Ver reportes': None,
            'Salir': lambda: self.screen(ScreenWelcome(self._message_bus))
        }


class ScreenIssueList(IssueTrackerMenuScreen):
    def __init__(self, message_bus: MessageBus, project: str, title: str, issue_item_handler_builder):
        self._project = project
        self._issue_item_handler_builder = issue_item_handler_builder
        IssueTrackerMenuScreen.__init__(self, message_bus, title)
        
    def menu_data(self) -> dict:
        self._issues = []
        def store_issues(message: Message):
            self._issues = message.issues
        self.handle_result(Message(MESSAGE.ISSUES, { 'project': self._project }), store_issues, None)
        if len(self._issues):
            handlers = {}
            for issue in self._issues:
                handlers[issue['title']] = self._issue_item_handler_builder(issue)
            handlers['Cancelar'] = lambda: self.screen(ScreenProjectMain(self._message_bus, self._project))
            return handlers
        self.modal_text('Debe reportar al menos una falla')
        self.screen(ScreenProjectMain(self._message_bus, self._project))
        return {}


class ScreenIssueOpen(ScreenIssueList):
    def __init__(self, message_bus: MessageBus, project: str):
        ScreenIssueList.__init__(self, message_bus, project, 'Editar reporte', lambda issue: lambda: self.screen(ScreenIssueEdit(self._message_bus, project, issue)))


#class ScreenIssueOpen(ScreenIssueList):
    #def __init__(self, message_bus: MessageBus, project: str):
     #   ScreenIssueList.__init__(self, message_bus, project, 'Ver reporte', lambda issue: lambda: self.screen(ScreenIssueEdit(self._message_bus, project, issue)))


class ScreenIssueEdit(IssueTrackerMenuScreen):
    def __init__(self, message_bus: MessageBus, project: str, issue_data: dict=None):
        self._project = project
        self._choices = None
        self._new_issue = issue_data is None
        self._issue_data = issue_data if issue_data is not None else {}
        IssueTrackerMenuScreen.__init__(self, message_bus, 'Nuevo reporte' if issue_data is not None else 'Editar reporte')

    def menu_data(self) -> dict:
        if not len(self._issue_data):
            self._issue_data = { 'title': '', 'description': '', 'steps': [], 'severity': '', 'repro_rate': -1, 'version': '', 'status': '' }

        menu_issue_data = {
            'Titulo' if self._issue_data['title'] is None or self._issue_data['title'] == '' else f'Titulo: {self._issue_data["title"]}': lambda: self._init_input_ui('Ingrese el titulo para el reporte:', lambda message: self.on_issue_string_property(message, 'title', 'El titulo del reporte no puede estar vacio')),
            'Descripcion' if self._issue_data['description'] is None or self._issue_data['description'] == '' else 'Descripcion: <introducida>': lambda: self._init_input_ui('Ingrese una descripcion para el reporte:', lambda message: self.on_issue_string_property(message, 'description', 'La descripcion del reporte no puede estar vacia')),
            #'Pasos para reproducir': None,
            'Severidad' if self._issue_data['severity'] is None or self._issue_data['severity'] == '' else f'Severidad: {self._issue_data["severity"]}': lambda: self._init_select_ui('Elija una severidad para la falla encontrada:', ['Baja', 'Media', 'Alta', 'Critica', 'Bloqueante'], lambda message: self.on_issue_choice_property(message, 'severity')),
            'Tasa de reproduccion' if self._issue_data['repro_rate'] is None or self._issue_data['repro_rate'] == -1 else f'Tasa de reproduccion: {self._issue_data["repro_rate"]}': lambda: self._init_input_ui('Ingrese la tasa de reproduccion de la falla:', lambda message: self.on_issue_number_property(message, 'repro_rate')),
            'Version' if self._issue_data['version'] is None or self._issue_data['version'] == '' else f'Version: {self._issue_data["version"]}': lambda: self._init_input_ui('Ingrese la version de la aplicacion probada:', lambda message: self.on_issue_string_property(message, 'version', 'La version de la aplicacion del reporte no puede estar vacia')),
            'Estado' if self._issue_data['status'] is None or self._issue_data['status'] == '' else f'Estado: {self._issue_data["status"]}': lambda: self._init_select_ui('Elija un estado para la falla:', ['Abierta', 'Pendiente', 'Arreglada', 'Confirmada'], lambda message: self.on_issue_choice_property(message, 'status')),
            'Guardar': self.on_save,
        }

        if not self._new_issue:
            menu_issue_data['Eliminar'] = self.on_delete

        menu_issue_data['Cancelar'] = lambda: self.screen(ScreenProjectMain(self._message_bus, self._project))

        return menu_issue_data

    def _init_select_ui(self, prompt: str, options: list, handler):
        self._choices = options
        self._current_ui = self._active_input = ChoiceUI(prompt, options, handler)

    def _init_input_ui(self, prompt: str, handler):
        self._current_ui = self._active_input = InputUI(prompt, handler)

    def on_issue_choice_property(self, message: Message, issue_property_key: str):
        if message.input is not None:
            choice = -1
            try:
                choice = int(message.input)
            except ValueError:
                self.modal_text(f'Debe ingresar un valor numerico entre 1 y {len(self._choices)}')
                return True
            if choice - 1 < len(self._choices):
                self._issue_data[issue_property_key] = self._choices[choice - 1]
                self._current_ui = self.init_ui('Nuevo reporte' if self._new_issue else 'Editar reporte')
                return False
            self.modal_text(f'El valor debe ser menor a la cantidad de opciones ({len(self._choices)})')
        return True

    def on_issue_string_property(self, message: Message, issue_property_key: str, error_message: str):
        if message.input is not None and message.input != '':
            self._issue_data[issue_property_key] = message.input
            self._current_ui = self.init_ui('Nuevo reporte' if self._new_issue else 'Editar reporte')
            return False
        self.modal_text(error_message)
        return True

    def on_issue_number_property(self, message: Message, issue_property_key: str, min_value: int=0, max_value: int=100):
        if message.input is not None:
            number = -1
            try:
                number = int(message.input)
            except ValueError:
                self.modal_text(f'Debe ingresar un valor numerico entre {min_value} y {max_value}')
                return True
            if number >= min_value and number <= max_value:
                self._issue_data[issue_property_key] = number
                self._current_ui = self.init_ui('Nuevo reporte' if self._new_issue else 'Editar reporte')
                return False
            self.modal_text(f'El valor debe estar entre {min_value} y {max_value}')
        return True

    def on_delete(self):
        AutoHandler(self._message_bus, MESSAGE.SUCCESS, lambda message: self.screen(ScreenProjectMain(self._message_bus, self._project)))
        self._message_bus.post(Message(MESSAGE.DELETE_ISSUE, { 'issue': self._issue_data, 'project': self._project }))

    def on_save(self):
        if self._issue_data['title'] is None or self._issue_data['title'] == '':
            self.modal_text('El reporte debe tener un titulo')
            return True

        if self._issue_data['description'] is None or self._issue_data['description'] == '':
            self.modal_text('El reporte debe incluir una descripcion')
            return True

        #if not len(self._issue_data['steps']):
        #    self.modal_text('El reporte debe incluir pasos para su reproduccion')
        #    return True

        if self._issue_data['severity'] is None or self._issue_data['severity'] == '':
            self.modal_text('El reporte debe indicar la severidad de la falla')
            return True

        if self._issue_data['repro_rate'] is None or self._issue_data['repro_rate'] < 0 or self._issue_data['repro_rate'] > 100:
            self.modal_text('El reporte debe indicar la tasa de reproduccion de la falla')
            return True

        if self._issue_data['version'] is None or self._issue_data['version'] == '':
            self.modal_text('Debe indicarse la version de la aplicacion siendo probada')
            return True

        if self._issue_data['status'] is None or self._issue_data['status'] == '':
            self.modal_text('Debe establecerse el estado de la falla')
            return True

        AutoHandler(self._message_bus, MESSAGE.SUCCESS, lambda message: self.screen(ScreenProjectMain(self._message_bus, self._project)))
        self._message_bus.post(Message(MESSAGE.NEW_ISSUE if self._new_issue else MESSAGE.EDIT_ISSUE, { 'issue': self._issue_data, 'project': self._project }))


class IssueTracker():
    def __init__(self, message_bus: MessageBus, data_file: str = 'issue.tracker'):
        self._message_bus = message_bus
        self._data_file = data_file
        self._data = {}
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                self._data = json.loads(f.read())
                f.close()
        self._message_bus.subscribe(MESSAGE.NEW_PROJECT, self.on_new_project)
        self._message_bus.subscribe(MESSAGE.PROJECTS, self.on_projects)
        self._message_bus.subscribe(MESSAGE.DELETE_PROJECT, self.on_delete_project)
        self._message_bus.subscribe(MESSAGE.NEW_ISSUE, self.on_new_issue)
        self._message_bus.subscribe(MESSAGE.EDIT_ISSUE, self.on_edit_issue)
        self._message_bus.subscribe(MESSAGE.ISSUES, self.on_issues)
        self._message_bus.subscribe(MESSAGE.DELETE_ISSUE, self.on_delete_issue)

    def save(self):
        with open(self._data_file, 'w') as f:
            f.write(json.dumps(self._data, indent=4))
            f.close()

    def _success(self, return_data: dict=None):
        self._message_bus.post(Message(MESSAGE.SUCCESS, return_data))

    def _failure(self, return_data: dict=None):
        self._message_bus.post(Message(MESSAGE.FAILURE, return_data))

    def on_new_project(self, message: Message):
        if message.name is not None and message.name not in self._data:
            self._data[message.name] = { 'issues': [] }
            self.save()
            self._success()
        elif message.name in self._data:
            self._failure()

    def on_projects(self, message: Message):
        if len(self._data):
            self._message_bus.post(Message(MESSAGE.SUCCESS, { 'projects': self._data.keys() }))
        else:
            self._message_bus.post(Message(MESSAGE.FAILURE))

    def on_delete_project(self, message: Message):
        if message.project is not None and message.project in self._data:
            self._data.pop(message.project)
            self.save()
            self._success()
        else:
            self._failure()

    def on_new_issue(self, message: Message):
        if message.issue is not None and message.project is not None:
            self._data[message.project]['issues'].append(message.issue)
            self.save()
            self._success()
        else:
            self._failure()

    def on_edit_issue(self, message: Message):
        if message.issue is not None and message.project is not None:
            issue = dict(message.issue)
            issue.pop('index')
            self._data[message.project]['issues'][message.issue['index']] = issue
            self.save()
            self._success()
        else:
            self._failure()

    def on_issues(self, message: Message):
        if message.project is not None and message.project in self._data:
            original_issues = self._data[message.project]['issues']
            issues = []
            for index, issue in zip(range(len(original_issues)), original_issues):
                cissue = dict(issue)
                cissue['index'] = index
                issues.append(cissue)
            self._success({ 'issues': issues })
        else:
            self._failure()

    def on_delete_issue(self, message: Message):
        if message.issue is not None and message.project is not None:
            issues = self._data[message.project]['issues']
            issues = issues[:message.issue['index']] + issues[message.issue['index'] + 1:]
            self._data[message.project]['issues'] = issues
            self.save()
            self._success()
        else:
            self._failure()


class IssueTrackerApp():
    def __init__(self):
        self._running = True
        self._message_bus = MessageBus()
        self._message_bus.subscribe(MESSAGE.EXIT, self.on_exit)
        self._message_bus.subscribe(MESSAGE.REQUEST_SCREEN, self.on_screen_request)
        self._message_bus.subscribe(MESSAGE.REQUEST_MODAL, self.on_modal_request)
        self._tracker = IssueTracker(self._message_bus)
        self._current_screen = ScreenWelcome(self._message_bus)
        self._modal = None

    def on_screen_request(self, message: Message):
        if message.screen is not None:
            self._current_screen = message.screen

    def on_modal_request(self, message: Message):
        self._modal = message.modal

    def on_exit(self, message: Message):
        self._running = False

    def run(self):
        while self._running:
            if self._modal is not None:
                self._modal.render()
                TextField.with_text_xywh('', 0, self._modal.bottom(), 0, 0).read()
                self._modal = None
            self._current_screen.show()
            time.sleep(0.1)


class InputScript():
    def __init__(self, data: list, original_impl):
        self._inputs = data
        self._current_input = 0
        self._original_impl = original_impl

    def __call__(self):
        ret = ''
        if self._current_input < len(self._inputs):
            ret = self._inputs[self._current_input]
            self._current_input += 1
        else:
            ret = self._original_impl()
        return ret


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r') as f:
                read_input = InputScript(f.read().split('\n'), read_input)
                f.close()
        except:
            print(f'Error al intentar cargar el archivo de prueba "{sys.argv[1]}"; verifique que el mismo exista')
            time.sleep(3)
    IssueTrackerApp().run()
    print()
