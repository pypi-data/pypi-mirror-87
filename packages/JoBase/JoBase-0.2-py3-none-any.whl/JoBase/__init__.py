"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import arcade, random, math, os

class Screen(arcade.Window):
    def __init__(screen, width, height, title):
        screen.resize = 0
        screen._color = WHITE
        screen._rate = 60
        screen._fullscreen = 0
        screen._visible = 1
        super().__init__(width, height, title, resizable = True)
        arcade.set_background_color(WHITE)
        screen.set_update_rate(1 / 60)
        
        for name in dir(screen):
            if name.startswith('CURSOR_'): globals()[name[7:]] = getattr(screen, name)
        print('Welcome to JoBase. Visit \'http://jobase.org\' for tutorials and documentation.\n')
        
    def collide(screen, other):
        return collision(screen.boundary(), other.boundary())
        
    def boundary(screen):
        return {'left': 0, 'top': screen.height, 'right': screen.width, 'bottom': 0, 'type': 'rect'}
    
    def getvisible(screen):
        return screen._visible
    def setvisible(screen, boolean):
        screen.set_visible(boolean)
        screen._visible = boolean
    visible = property(getvisible, setvisible)
    
    def getx(screen):
        return screen.get_location()[0]
    def setx(screen, x):
        screen.set_location(x, screen.y)
    x = property(getx, setx)
        
    def gety(screen):
        return screen.get_location()[1]
    def sety(screen, y):
        screen.set_location(screen.x, y)
    y = property(gety, sety)
    
    def gettitle(screen):
        return screen.caption
    def settitle(screen, caption):
        screen.set_caption(caption)
    title = property(gettitle, settitle)
    
    def getfullscreen(screen):
        return screen._fullscreen
    def setfullscreen(screen, boolean):
        screen.set_fullscreen(boolean)
        screen.resize = 1
    fullscreen = property(getfullscreen, setfullscreen)
    
    def getrate(screen):
        return screen._rate
    def setrate(screen, frame):
        screen.set_update_rate(1 / frame)
        screen._rate = frame
    rate = property(getrate, setrate)
    
    def getcolor(screen):
        return screen._color
    def setcolor(screen, color):
        arcade.set_background_color(color)
        screen._color = color
    color = property(getcolor, setcolor)
        
    def centralize(screen):
        screen.center_window()
        
    def on_mouse_motion(screen, x, y, dx, dy):
        MOUSE._x = x
        MOUSE._y = y
        MOUSE.move = 1

    def on_mouse_scroll(screen, x, y, button, direction):
        MOUSE.scroll = 1
        if direction == 1.0: MOUSE.up = 1
        elif direction == -1.0: MOUSE.down = 1

    def on_mouse_press(screen, x, y, button, modifiers):
        MOUSE.press = 1
        if button == 1:
            MOUSE.left = 1
        elif button == 4:
            MOUSE.right = 1
        elif button == 2:
            MOUSE.middle = 1

    def on_mouse_release(screen, x, y, button, modifiers):
        MOUSE.release = 1

    def on_resize(screen, width, height):
        super().on_resize(width, height)
        screen.resize = 1

    def on_key_press(screen, key, modifiers):
        KEY.press = 1
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key, str(keys)):
                keys = keys.lower()
                setattr(KEY, str(keys), 1)

    def on_key_release(screen, key, modifiers):
        KEY.release = 1
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key, str(keys)):
                keys = keys.lower()
                setattr(KEY, str(keys), 0)

class Key:
    def __init__(key):
        key.press = 0
        key.release = 0        
        for keys in dir(arcade.key):
            if not keys.startswith('__'):
                keys = keys.lower()
                setattr(key, str(keys), 0)
        
class Mouse:
    def __init__(mouse):
        mouse.press = 0
        mouse.release = 0
        mouse.left = 0
        mouse.right = 0
        mouse.middle = 0
        mouse.up = 0
        mouse.down = 0
        mouse.move = 0
        mouse.scroll = 0
        mouse._x = 0
        mouse._y = 0
        mouse._visible = True
        mouse._cursor = None
        
    def collide(mouse, other):
        return collision(other.boundary(), mouse.boundary())
        
    def boundary(mouse):
        return {'x': mouse._x, 'y': mouse._y, 'type': 'point'}
    
    def angle(mouse, other):
        return Angle(mouse.x, mouse.y, other.x, other.y)

    def distance(mouse, other):
        return Distance(mouse.x, mouse.y, other.x, other.y)
    
    def getvisible(mouse):
        return mouse._visible
    def setvisible(mouse, boolean):
        SCREEN.set_mouse_visible(boolean)
        mouse._visible = boolean
    visible = property(getvisible, setvisible)
    
    def getcursor(mouse):
        return mouse._cursor
    def setcursor(mouse, name):
        SCREEN.set_mouse_cursor(SCREEN.get_system_mouse_cursor(name))
        mouse._cursor = name
    cursor = property(getcursor, setcursor)
        
    def getx(mouse):
        return mouse._x
    def setx(mouse, value):
        SCREEN.set_mouse_position(value, mouse._y)
    x = property(getx, setx)
    
    def gety(mouse):
        return mouse._y
    def sety(mouse, value):
        SCREEN.set_mouse_position(mouse._x, value)
    y = property(gety, sety)
                
class Point:
    def __init__(point, x, y, color, size):
        point.x = x
        point.y = y
        point.color = color
        point.size = size
        
    def draw(point):
        arcade.draw_point(point.x, point.y, point.color, point.size)
        
    def collide(point, other):
        return collision(point.boundary(), other.boundary())
        
    def boundary(point):
        return {'left': point.left, 'top': point.top, 'right': point.right, 'bottom': point.bottom, 'type': 'rect'}
    
    def angle(point, other):
        return Angle(point.x, point.y, other.x, other.y)

    def distance(point, other):
        return Distance(point.x, point.y, other.x, other.y)
        
    def gettop(point):
        return point.y + point.size / 4
    def settop(point, value):
        point.y = value - point.size / 4
    top = property(gettop, settop)
    
    def getbottom(point):
        return point.y - point.size / 4
    def setbottom(point, value):
        point.y = value + point.size / 4
    bottom = property(getbottom, setbottom)
    
    def getleft(point):
        return point.x - point.size / 4
    def setleft(point, value):
        point.x = value + point.size / 4
    left = property(getleft, setleft)
    
    def getright(point):
        return point.x + point.size / 4
    def setright(point, value):
        point.x = value - point.size / 4
    right = property(getright, setright)
       
class Line:
    def __init__(line, x1, y1, x2, y2, color, thickness):
        line.x1 = x1
        line.y1 = y1
        line.x2 = x2
        line.y2 = y2
        line.color = color
        line.thickness = thickness
        
        line._rotation = 0
        
    def draw(line):
        arcade.draw_line(line.x1, line.y1, line.x2, line.y2, line.color, line.thickness)
        
    def collide(line, other):
        return collision(line.boundary(), other.boundary())
        
    def boundary(line):
        return {'left': line.left, 'top': line.top, 'right': line.right, 'bottom': line.bottom, 'type': 'rect'}
    
    def angle(line, other):
        return Angle(line.x, line.y, other.x, other.y)

    def distance(line, other):
        return Distance(line.x, line.y, other.x, other.y)    
    
    def getx(line):
        return find_center_x_of_points(line.points)
    def setx(line, value):
        difference = value - find_center_x_of_points(line.points)
        for point in line.points:
            point[0] += difference
    x = property(getx, setx)

    def gety(line):
        return find_center_y_of_points(line.points)
    def sety(line, value):
        difference = value - find_center_y_of_points(line.points)
        for point in line.points:
            point[1] += difference
    y = property(gety, sety)    
    
    def getwidth(line):
        return line.right - line.left
    def setwidth(line, value):
        if not value == line.right - line.left:
            center_x = (line.x2 + line.x1) / 2
            x_scale = value / (line.right - line.left)
            
            distance_1 = line.x1 - center_x
            line.x1 = center_x + distance_1 * x_scale
            
            distance_2 = line.x2 - center_x
            line.x2 = center_x + distance_2 * x_scale            
    width = property(getwidth, setwidth)

    def getheight(line):
        return line.top - line.bottom
    def setheight(line, value):
        if not value == line.top - line.bottom:
            center_y = (line.y2 + line.y1) / 2
            y_scale = value / (line.top - line.bottom)
            
            distance_1 = line.y1 - center_y
            line.y1 = center_y + distance_1 * y_scale
            
            distance_2 = line.y2 - center_y
            line.y2 = center_y + distance_2 * y_scale
    height = property(getheight, setheight)    
        
    def getrotation(line):
        return line._rotation
    def setrotation(line, value):
        if not value == line._rotation:
            center_x = (line.x2 + line.x1) / 2
            center_y = (line.y2 + line.y1) / 2
            
            angle_1 = Angle(center_x, center_y, line.x1, line.y1)
            distance_1 = Distance(center_x, center_y, line.x1, line.y1)
            x, y = Direction(distance_1, angle_1 + value - line._rotation)
            line.x1, line.y1 = x + center_x, y + center_y
            
            angle_2 = Angle(center_x, center_y, line.x2, line.y2)
            distance_2 = Distance(center_x, center_y, line.x2, line.y2)
            x, y = Direction(distance_2, angle_2 + value - line._rotation)
            line.x2, line.y2 = x + center_x, y + center_y
            
            line._rotation = value
    rotation = property(getrotation, setrotation)

    def gettop(line):
        if line.y1 > line.y2:
            return line.y1
        else:
            return line.y2
    def settop(line, value):
        if line.y1 > line.y2:
            top = line.y1
        else:
            top = line.y2        
        distance = value - top
        line.y1 += distance
        line.y2 += distance
    top = property(gettop, settop)

    def getbottom(line):
        if line.y1 < line.y2:
            return line.y1
        else:
            return line.y2
    def setbottom(line, value):
        if line.y1 < line.y2:
            bottom = line.y1
        else:
            bottom = line.y2        
        distance = value - bottom
        line.y1 += distance
        line.y2 += distance
    bottom = property(getbottom, setbottom)

    def getleft(line):
        if line.x1 < line.x2:
            return line.x1
        else:
            return line.x2
    def setleft(line, value):
        if line.x1 < line.x2:
            left = line.x1
        else:
            left = line.x2        
        distance = value - left
        line.x1 += distance
        line.x2 += distance
    left = property(getleft, setleft)

    def getright(line):
        if line.x1 > line.x2:
            return line.x1
        else:
            return line.x2
    def setright(line, value):
        if line.x1 > line.x2:
            right = line.x1
        else:
            right = line.x2        
        distance = value - right
        line.x1 += distance
        line.x2 += distance
    right = property(getright, setright)
    
class Strip:
    def __init__(strip, points, color, thickness):
        strip.points = [list(point) for point in points]
        strip.color = color
        strip.thickness = thickness
        
        strip._rotation = 0
        
    def draw(strip):
        arcade.draw_line_strip(strip.points, strip.color, strip.thickness)
        
    def collide(strip, other):
        return collision(strip.boundary(), other.boundary())
        
    def boundary(strip):
        return {'left': strip.left, 'top': strip.top, 'right': strip.right, 'bottom': strip.bottom, 'type': 'rect'}
    
    def angle(strip, other):
        return Angle(strip.x, strip.y, other.x, other.y)

    def distance(strip, other):
        return Distance(strip.x, strip.y, other.x, other.y) 
    
    def getx(strip):
        return find_center_x_of_points(strip.points)
    def setx(strip, value):
        difference = value - find_center_x_of_points(strip.points)
        for point in strip.points:
            point[0] += difference
    x = property(getx, setx)

    def gety(strip):
        return find_center_y_of_points(strip.points)
    def sety(strip, value):
        difference = value - find_center_y_of_points(strip.points)
        for point in strip.points:
            point[1] += difference
    y = property(gety, sety)      
    
    def getwidth(strip):
        return strip.right - strip.left
    def setwidth(strip, value):
        if not value == strip.right - strip.left:
            center_x = find_center_x_of_points(strip.points)
            x_scale = value / (strip.right - strip.left)
            scale_x(strip.points, center_x, x_scale)
    width = property(getwidth, setwidth)

    def getheight(strip):
        return strip.top - strip.bottom
    def setheight(strip, value):
        if not value == strip.top - strip.bottom:
            center_y = find_center_y_of_points(strip.points)
            y_scale = value / (strip.top - strip.bottom)
            scale_y(strip.points, center_y, y_scale)
    height = property(getheight, setheight)    
                  
    def getrotation(strip):
        return strip._rotation
    def setrotation(strip, value):
        if not value == strip._rotation:
            center_x = find_center_x_of_points(strip.points)
            center_y = find_center_y_of_points(strip.points)
            rotate(strip.points, value - strip._rotation, center_x, center_y)
            strip._rotation = value
    rotation = property(getrotation, setrotation)
    
    def gettop(strip):
        return find_top_of_points(strip.points)
    def settop(strip, value):
        distance = value - find_top_of_points(strip.points)
        for point in strip.points:
            point[1] += distance
    top = property(gettop, settop)
    
    def getbottom(strip):
        return find_bottom_of_points(strip.points)
    def setbottom(strip, value):
        distance = value - find_bottom_of_points(strip.points)
        for point in strip.points:
            point[1] += distance
    bottom = property(getbottom, setbottom)
    
    def getleft(strip):
        return find_left_of_points(strip.points)
    def setleft(strip, value):
        distance = value - find_left_of_points(strip.points)
        for point in strip.points:
            point[0] += distance
    left = property(getleft, setleft)
    
    def getright(strip):
        return find_right_of_points(strip.points)
    def setright(strip, value):
        distance = value - find_right_of_points(strip.points)
        for point in strip.points:
            point[0] += distance
    right = property(getright, setright)        
        
class Shape:
    def __init__(shape, points, color):
        shape.points = [list(point) for point in points]
        shape.color = color
        shape.outline = 0
        
        shape._rotation = 0
        
    def draw(shape):
        if shape.outline == 0:
            arcade.draw_polygon_filled(shape.points, shape.color)
        else:
            arcade.draw_polygon_outline(shape.points, shape.color, shape.outline)
            
    def collide(shape, other):
        return collision(shape.boundary(), other.boundary())
        
    def boundary(shape):
        return {'left': shape.left, 'top': shape.top, 'right': shape.right, 'bottom': shape.bottom, 'type': 'rect'}
    
    def angle(shape, other):
        return Angle(shape.x, shape.y, other.x, other.y)

    def distance(shape, other):
        return Distance(shape.x, shape.y, other.x, other.y)

    def getx(shape):
        return find_center_x_of_points(shape.points)
    def setx(shape, value):
        difference = value - find_center_x_of_points(shape.points)
        for point in shape.points:
            point[0] += difference
    x = property(getx, setx)

    def gety(shape):
        return find_center_y_of_points(shape.points)
    def sety(shape, value):
        difference = value - find_center_y_of_points(shape.points)
        for point in shape.points:
            point[1] += difference
    y = property(gety, sety)      
    
    def getwidth(shape):
        return shape.right - shape.left
    def setwidth(shape, value):
        if not value == shape.right - shape.left:
            center_x = find_center_x_of_points(shape.points)
            x_scale = value / (shape.right - shape.left)
            scale_x(shape.points, center_x, x_scale)
    width = property(getwidth, setwidth)

    def getheight(shape):
        return shape.top - shape.bottom
    def setheight(shape, value):
        if not value == shape.top - shape.bottom:
            center_y = find_center_y_of_points(shape.points)
            y_scale = value / (shape.top - shape.bottom)
            scale_y(shape.points, center_y, y_scale)
    height = property(getheight, setheight)    
                  
    def getrotation(shape):
        return shape._rotation
    def setrotation(shape, value):
        if not value == shape._rotation:
            center_x = find_center_x_of_points(shape.points)
            center_y = find_center_y_of_points(shape.points)
            rotate(shape.points, value - shape._rotation, center_x, center_y)
            shape._rotation = value
    rotation = property(getrotation, setrotation)
    
    def gettop(shape):
        return find_top_of_points(shape.points)
    def settop(shape, value):
        distance = value - find_top_of_points(shape.points)
        for point in shape.points:
            point[1] += distance
    top = property(gettop, settop)
    
    def getbottom(shape):
        return find_bottom_of_points(shape.points)
    def setbottom(shape, value):
        distance = value - find_bottom_of_points(shape.points)
        for point in shape.points:
            point[1] += distance
    bottom = property(getbottom, setbottom)
    
    def getleft(shape):
        return find_left_of_points(shape.points)
    def setleft(shape, value):
        distance = value - find_left_of_points(shape.points)
        for point in shape.points:
            point[0] += distance
    left = property(getleft, setleft)
    
    def getright(shape):
        return find_right_of_points(shape.points)
    def setright(shape, value):
        distance = value - find_right_of_points(shape.points)
        for point in shape.points:
            point[0] += distance
    right = property(getright, setright)    
            
class Circle:
    def __init__(circle, x, y, size, color):
        circle.x = x
        circle.y = y
        circle.size = size
        circle.color = color
        circle.outline = 0
        
    def draw(circle):
        if circle.outline == 0:
            arcade.draw_circle_filled(circle.x, circle.y, circle.size / 2, circle.color)
        else:
            arcade.draw_circle_outline(circle.x, circle.y, circle.size / 2, circle.color, circle.outline)
            
    def collide(circle, other):
        return collision(circle.boundary(), other.boundary())
        
    def boundary(circle):
        return {'x': circle.x, 'y': circle.y, 'rad': circle.size / 2, 'type': 'circle'}
            
    def angle(circle, other):
        return Angle(circle.x, circle.y, other.x, other.y)

    def distance(circle, other):
        return Distance(circle.x, circle.y, other.x, other.y)
 
    def gettop(circle):
        return circle.y + circle.size / 2
    def settop(circle, value):
        circle.y = value - circle.size / 2
    top = property(gettop, settop)
    
    def getbottom(circle):
        return circle.y - circle.size / 2
    def setbottom(circle, value):
        circle.y = value + circle.size / 2
    bottom = property(getbottom, setbottom)
    
    def getleft(circle):
        return circle.x - circle.size / 2
    def setleft(circle, value):
        circle.x = value + circle.size / 2
    left = property(getleft, setleft)
    
    def getright(circle):
        return circle.x + circle.size / 2
    def setright(circle, value):
        circle.x = value - circle.size / 2
    right = property(getright, setright)     
            
class Ellipse:
    def __init__(ellipse, x, y, width, height, color):
        ellipse.x = x
        ellipse.y = y
        ellipse.width = width
        ellipse.height = height
        ellipse.color = color
        ellipse.outline = 0
        ellipse.rotation = 0
        
    def draw(ellipse):
        if ellipse.outline == 0:
            arcade.draw_ellipse_filled(ellipse.x, ellipse.y, ellipse.width, ellipse.height, ellipse.color, ellipse.rotation)
        else:
            arcade.draw_ellipse_outline(ellipse.x, ellipse.y, ellipse.width, ellipse.height, ellipse.color, ellipse.outline, ellipse.rotation)
            
    def collide(ellipse, other):
        return collision(ellipse.boundary(), other.boundary())
        
    def boundary(ellipse):
        return {'left': ellipse.left, 'top': ellipse.top, 'right': ellipse.right, 'bottom': ellipse.bottom, 'type': 'rect'}               
            
    def angle(ellipse, other):
        return Angle(ellipse.x, ellipse.y, other.x, other.y)

    def distance(ellipse, other):
        return Distance(ellipse.x, ellipse.y, other.x, other.y)
    
    def gettop(ellipse):
        return ellipse.y + ellipse.height / 2
    def settop(ellipse, value):
        ellipse.y = value - ellipse.height / 2
    top = property(gettop, settop)
    
    def getbottom(ellipse):
        return ellipse.y - ellipse.height / 2
    def setbottom(ellipse, value):
        ellipse.y = value + ellipse.height / 2
    bottom = property(getbottom, setbottom)
    
    def getleft(ellipse):
        return ellipse.x - ellipse.width / 2
    def setleft(ellipse, value):
        ellipse.x = value + ellipse.width / 2
    left = property(getleft, setleft)
    
    def getright(ellipse):
        return ellipse.x + ellipse.width / 2
    def setright(ellipse, value):
        ellipse.x = value - ellipse.width / 2
    right = property(getright, setright)
            
class Arc:
    def __init__(arc, x, y, width, height, color, start, end):
        arc.x = x
        arc.y = y
        arc.width = width
        arc.height = height
        arc.color = color
        arc.start = start
        arc.end = end
        arc.outline = 0
        arc.rotation = 0
        
    def draw(arc):
        if arc.outline == 0:
            arcade.draw_arc_filled(arc.x, arc.y, arc.width, arc.height, arc.color, arc.start, arc.end, arc.rotation)
        else:
            arcade.draw_arc_outline(arc.x, arc.y, arc.width, arc.height, arc.color, arc.start, arc.end, arc.outline, arc.rotation)
            
    def collide(arc, other):
        return collision(arc.boundary(), other.boundary())
        
    def boundary(arc):
        return {'left': arc.left, 'top': arc.top, 'right': arc.right, 'bottom': arc.bottom, 'type': 'rect'}            
            
    def angle(arc, other):
        return Angle(arc.x, arc.y, other.x, other.y)

    def distance(arc, other):
        return Distance(arc.x, arc.y, other.x, other.y)

    def gettop(arc):
        return arc.y + arc.height / 2
    def settop(arc, value):
        arc.y = value - arc.height / 2
    top = property(gettop, settop)
    
    def getbottom(arc):
        return arc.y - arc.height / 2
    def setbottom(arc, value):
        arc.y = value + arc.height / 2
    bottom = property(getbottom, setbottom)
    
    def getleft(arc):
        return arc.x - arc.width / 2
    def setleft(arc, value):
        arc.x = value + arc.width / 2
    left = property(getleft, setleft)
    
    def getright(arc):
        return arc.x + arc.width / 2
    def setright(arc, value):
        arc.x = value - arc.width / 2
    right = property(getright, setright)    
            
class Rectangle:
    def __init__(rect, x, y, width, height, color):
        rect.x = x
        rect.y = y
        rect.width = width
        rect.height = height
        rect.color = color
        rect.outline = 0
        rect.rotation = 0
        
    def draw(rect):
        if rect.outline == 0:
            arcade.draw_rectangle_filled(rect.x, rect.y, rect.width, rect.height, rect.color, rect.rotation)
        else:
            arcade.draw_rectangle_outline(rect.x, rect.y, rect.width, rect.height, rect.color, rect.outline, rect.rotation)
            
    def collide(rect, other):
        return collision(rect.boundary(), other.boundary())
        
    def boundary(rect):
        return {'left': rect.left, 'top': rect.top, 'right': rect.right, 'bottom': rect.bottom, 'type': 'rect'}
    
    def angle(rect, other):
        return Angle(rect.x, rect.y, other.x, other.y)

    def distance(rect, other):
        return Distance(rect.x, rect.y, other.x, other.y)

    def gettop(rect):
        return rect.y + rect.height / 2
    def settop(rect, value):
        rect.y = value - rect.height / 2
    top = property(gettop, settop)
    
    def getbottom(rect):
        return rect.y - rect.height / 2
    def setbottom(rect, value):
        rect.y = value + rect.height / 2
    bottom = property(getbottom, setbottom)
    
    def getleft(rect):
        return rect.x - rect.width / 2
    def setleft(rect, value):
        rect.x = value + rect.width / 2
    left = property(getleft, setleft)
    
    def getright(rect):
        return rect.x + rect.width / 2
    def setright(rect, value):
        rect.x = value - rect.width / 2
    right = property(getright, setright)       
            
class Image:
    def __init__(image, x, y, name, **flip):
        horizontally = 'False'
        vertically = 'False'
        
        if flip.get('flip_horizontal'): horizontally = 'True'
        if flip.get('flip_vertical'): vertically = 'True'

        image.texture = arcade.load_texture(str(name), flipped_horizontally = eval(horizontally), flipped_vertically = eval(vertically))
                    
        image.x = x
        image.y = y
        image.name = name
        image.rotation = 0
        image.width = image.texture.width
        image.height = image.texture.height        
        
    def draw(image):
        arcade.draw_texture_rectangle(image.x, image.y, image.width, image.height, image.texture, image.rotation)
        
    def collide(image, other):
        return collision(image.boundary(), other.boundary())
        
    def boundary(image):
        return {'left': image.left, 'top': image.top, 'right': image.right, 'bottom': image.bottom, 'type': 'rect'}
    
    def angle(image, other):
        return Angle(image.x, image.y, other.x, other.y)

    def distance(image, other):
        return Distance(image.x, image.y, other.x, other.y)

    def gettop(image):
        return image.y + image.height / 2
    def settop(image, value):
        image.y = value - image.height / 2
    top = property(gettop, settop)
    
    def getbottom(image):
        return image.y - image.height / 2
    def setbottom(image, value):
        image.y = value + image.height / 2
    bottom = property(getbottom, setbottom)
    
    def getleft(image):
        return image.x - image.width / 2
    def setleft(image, value):
        image.x = value + image.width / 2
    left = property(getleft, setleft)
    
    def getright(image):
        return image.x + image.width / 2
    def setright(image, value):
        image.x = value - image.width / 2
    right = property(getright, setright)
    
    
class Sprite:
    def __init__(sprite, x, y, **names):
        
        for name in names:
            horizontally = 'False'
            vertically = 'False'
            
            if names[str(name)].flip.get('flip_horizontal'): horizontally = 'True'
            if names[str(name)].flip.get('flip_vertical'): vertically = 'True'
                
            setattr(sprite, str(name), arcade.load_texture(names[str(name)].name, flipped_horizontally = eval(horizontally), flipped_vertically = eval(vertically)))
                
        sprite.texture = getattr(sprite, next(iter(names)))
        sprite.x = x
        sprite.y = y
        sprite.rotation = 0  
        sprite.width = sprite.texture.width
        sprite.height = sprite.texture.height
        
    def draw(sprite):
        arcade.draw_texture_rectangle(sprite.x, sprite.y, sprite.width, sprite.height, sprite.texture, sprite.rotation)
    
    def collide(sprite, other):
        return collision(sprite.boundary(), other.boundary())
        
    def boundary(sprite):
        return {'left': sprite.left, 'top': sprite.top, 'right': sprite.right, 'bottom': sprite.bottom, 'type': 'rect'}
    
    def angle(sprite, other):
        return Angle(sprite.x, sprite.y, other.x, other.y)

    def distance(sprite, other):
        return Distance(sprite.x, sprite.y, other.x, other.y)
    
    def getimage(sprite):
        return getattr(sprite, 'texture')
    def setimage(sprite, name):
        sprite.texture = name
        sprite.width = sprite.texture.width
        sprite.height = sprite.texture.height
    image = property(getimage, setimage)    

    def gettop(sprite):
        return sprite.y + sprite.height / 2
    def settop(sprite, value):
        sprite.y = value - sprite.height / 2
    top = property(gettop, settop)
    
    def getbottom(sprite):
        return sprite.y - sprite.height / 2
    def setbottom(sprite, value):
        sprite.y = value + sprite.height / 2
    bottom = property(getbottom, setbottom)
    
    def getleft(sprite):
        return sprite.x - sprite.width / 2
    def setleft(sprite, value):
        sprite.x = value + sprite.width / 2
    left = property(getleft, setleft)
    
    def getright(sprite):
        return sprite.x + sprite.width / 2
    def setright(sprite, value):
        sprite.x = value - sprite.width / 2
    right = property(getright, setright)    
    
class Frame:
    def __init__(frame, name, **flip):
        frame.name = name
        frame.flip = flip
                
class Text:
    def __init__(text, word, x, y, color, size):
        
        text.word = word
        text.x = x
        text.y = y
        text.color = color
        text.size = size
        text.rotation = 0
        
        text.data = arcade.draw_text(str(text.word), text.x, text.y, text.color, text.size, rotation = text.rotation)
        
    def getcenter_x(text):
        return text.x + text.data.width / 2
    def setcenter_x(text, value):
        text.x = value - text.width / 2
    center_x = property(getcenter_x, setcenter_x)
    
    def getcenter_y(text):
        return text.y + text.data.height / 2
    def setcenter_y(text, value):
        text.y = value - text.height / 2
    center_y = property(getcenter_y, setcenter_y)    
        
    def getwidth(text):
        return text.data.width
    def setwidth(text, value):
        text.data.width = value
    width = property(getwidth, setwidth)
    
    def getheight(text):
        return text.data.height
    def setheight(text, value):
        text.data.height = value
    height = property(getheight, setheight)
        
    def draw(text):
        text.data = arcade.draw_text(str(text.word), text.x, text.y, text.color, text.size, rotation = text.rotation)
        
    def collide(text, other):
        return collision(text.boundary(), other.boundary())
        
    def boundary(text):
        return {'left': text.left, 'top': text.top, 'right': text.right, 'bottom': text.bottom, 'type': 'rect'}
    
    def angle(text, other):
        return Angle(text.x, text.y, other.x, other.y)

    def distance(text, other):
        return Distance(text.x, text.y, other.x, other.y)

    def gettop(text):
        return text.y + text.height
    def settop(text, value):
        text.y = value - text.height
    top = property(gettop, settop)
    
    def getbottom(text):
        return text.y
    def setbottom(text, value):
        text.y = value
    bottom = property(getbottom, setbottom)
    
    def getleft(text):
        return text.x
    def setleft(text, value):
        text.x = value
    left = property(getleft, setleft)
    
    def getright(text):
        return text.x + text.width
    def setright(text, value):
        text.x = value - text.width
    right = property(getright, setright)
    
class Sound:
    def __init__(sound, name):
        sound.name = name
        sound.sound = arcade.load_sound(name)
        
    def play(sound):
        arcade.play_sound(sound.sound)
        
    def loop(sound):
        pass
            
def scale_x(points, center_x, x_scale):
    for point in points:
        distance_x = point[0] - center_x
        point[0] = center_x + distance_x * x_scale
        
def scale_y(points, center_y, y_scale):
    for point in points:
        distance_y = point[1] - center_y
        point[1] = center_y + distance_y * y_scale
            
def rotate(points, rotation, center_x, center_y):
    for point in points:
        angle = Angle(center_x, center_y, point[0], point[1])
        distance = Distance(center_x, center_y, point[0], point[1])
        x, y = Direction(distance, angle - rotation)
        point[0], point[1] = x + center_x, y + center_y
        
def find_center_x_of_points(points):
    center_x = 0
    for point in points:
        center_x += point[0]
    center_x /= len(points)
    return center_x

def find_center_y_of_points(points):
    center_y = 0
    for point in points:
        center_y += point[1]
    center_y /= len(points)
    return center_y    
            
def find_left_of_points(points):
    left = 0
    for point in points:
        if not points.index(point) == 0:
            if point[0] < left:
                left = point[0]
        else:
            left = point[0]
    return left

def find_top_of_points(points):
    top = 0
    for point in points:
        if not points.index(point) == 0:
            if point[1] > top:
                top = point[1]
        else:
            top = point[1]
    return top

def find_right_of_points(points):
    right = 0  
    for point in points:
        if not points.index(point) == 0:
            if point[0] > right:
                right = point[0]
        else:
            right = point[0]
    return right

def find_bottom_of_points(points):
    bottom = 0    
    for point in points:
        if not points.index(point) == 0:
            if point[1] < bottom:
                bottom = point[1]
        else:
            bottom = point[1]
    return bottom
            
def collision(type1, type2):
    if type1['type'] == 'rect' and type2['type'] == 'rect':
        if rect_to_rect_collision(type1['left'], type1['top'], type1['right'], type1['bottom'], type2['left'], type2['top'], type2['right'], type2['bottom']):
            return True
        return False
        
    elif type1['type'] == 'point' and type2['type'] == 'point':
        if rect_to_point_collision(type1['x'], type1['y'], type2['x'], type2['y']):
            return True
        return False
    
    elif type1['type'] == 'circle' and type2['type'] == 'circle':
        if circle_to_circle_collision(type1['x'], type1['y'], type1['rad'], type2['x'], type2['y'], type2['rad']):
            return True
        return False    
        
    elif type1['type'] == 'rect' and type2['type'] == 'point':
        if rect_to_point_collision(type1['left'], type1['top'], type1['right'], type1['bottom'], type2['x'], type2['y']):
            return True
        return False
    
    elif type1['type'] == 'point' and type2['type'] == 'rect':
        if rect_to_point_collision(type2['left'], type2['top'], type2['right'], type2['bottom'], type1['x'], type1['y']):
            return True
        return False    
    
    elif type1['type'] == 'rect' and type2['type'] == 'circle':
        if rect_to_circle_collision(type1['left'], type1['top'], type1['right'], type1['bottom'], type2['x'], type2['y'], type2['rad']):
            return True
        return False
    
    elif type1['type'] == 'circle' and type2['type'] == 'rect':
        if rect_to_circle_collision(type2['left'], type2['top'], type2['right'], type2['bottom'], type1['x'], type1['y'], type1['rad']):
            return True
        return False    
    
    elif type1['type'] == 'point' and type2['type'] == 'circle':
        if point_to_circle_collision(type1['x'], type1['y'], type2['x'], type2['y'], type2['rad']):
            return True
        return False
    
    elif type1['type'] == 'circle' and type2['type'] == 'point':
        if point_to_circle_collision(type2['x'], type2['y'], type1['x'], type1['y'], type1['rad']):
            return True
        return False
            
def rect_to_rect_collision(left1, top1, right1, bottom1, left2, top2, right2, bottom2):
    if left1 < right2 and right1 > left2 and top1 > bottom2 and bottom1 < top2:
        return True
    return False
    
def point_to_point_collision(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return True
    return False
    
def circle_to_circle_collision(x1, y1, rad1, x2, y2, rad2):
    if Distance(x1, y1, x2, y2) < rad1 + rad2:
        return True
    return False
    
def rect_to_point_collision(left1, top1, right1, bottom1, x2, y2):
    if x2 < right1 and x2 > left1 and y2 > bottom1 and y2 < top1:
        return True
    return False
    
def rect_to_circle_collision(left1, top1, right1, bottom1, x2, y2, rad2):
    test_x = x2
    test_y = y2
    
    if x2 < left1: test_x = left1
    elif x2 > right1: test_x = right1
    if y2 > top1: test_y = top1
    elif y2 < bottom1: test_y = bottom1

    dist_x = x2 - test_x
    dist_y = y2 - test_y
    distance = math.sqrt((dist_x * dist_x) + (dist_y * dist_y))

    if distance < rad2:
        return True
    return False
    
def point_to_circle_collision(x1, y1, x2, y2, rad2):
    if Distance(x1, y1, x2, y2) < rad2:
        return True
    return False    

def set_colors():
    for name in dir(arcade.color):
        if not name.startswith('__'):
            globals()[name] = getattr(arcade.color, str(name))
            
def Distance(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

def Angle(x1, y1, x2, y2):
    x, y = x2 - x1, y2 - y1
    radians = math.atan2(y, x)
    radians %= 2 * math.pi
    degrees = math.degrees(radians)
    return degrees

def Direction(length, angle):
    x = length * math.cos(math.radians(angle))
    y = length * math.sin(math.radians(angle))
    return x, y

def Random(int1, int2):
    if int1 > int2: return random.randint(int(int2), int(int1))
    else: return random.randint(int(int1), int(int2))

def Write(name, *words):
    file = open('text_files/' + str(name), 'w')
    for word in words:
        file.write(str(word) + '\n')
    file.close()
    
def Read(name):
    file = open('text_files/' + str(name), 'r')
    read = file.readlines()
    file_list = []
    for element in read:
        element = element.strip()
        element = eval(element)
        file_list.append(element)
    file.close()

set_colors()
KEY = Key()
MOUSE = Mouse()
SCREEN = Screen(800, 600, "JoBase")