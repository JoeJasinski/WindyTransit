# Algorithm bassed off of James Tauber's gradient generator: http://jtauber.com/2008/05/gradient.py


from __future__ import division
import re

hexcode = re.compile("^\#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?$")

class GradientGenerator(object):
    
    def clean_color(self, color):
        red = green = blue = 0 
        if isinstance(color, (list, tuple)) and len(color) == 3:
            red = color[0]
            green = color[1]
            blue = color[2]
        elif isinstance(color, str):
            if not hexcode.match(color):
                raise Exception("""Color is not a valid hex color code. (i.e #1234ff): %s""" % (color))
            if len(color) == 4:
                red = int(color[1] * 2, 16)
                green = int(color[2] * 2, 16) 
                blue = int(color[3] * 2, 16)
            elif len(color) == 7:
                red = int(color[1:3], 16)
                green = int(color[3:5], 16) 
                blue = int(color[5:7], 16)
        else: 
            raise Exception("Not a valid color code:%s" % (color))
        return (red, green, blue)
    
    def __init__(self, data, *args, **kwargs):
        if len(data) <= 1: 
            raise Exception("Data must contain at least two values")
        cleaned_data = []
        for element in data:
            if len(element) != 3:
                raise Exception("Data element must contain a percent, start color, and end color")
            percent, start_color, end_color = element   
            if percent > 1 or percent < 0:
                raise Exception("Value of percent must be bewteen 0 and 1 (inclusive)") 
            start_color = self.clean_color(start_color)
            end_color = self.clean_color(end_color)
            cleaned_data.append((percent, start_color, end_color))
        self.DATA = cleaned_data
    
    def linear_gradient(self, start_value, stop_value, start_offset=0.0, stop_offset=1.0):
        return lambda offset: (start_value + ((offset - start_offset) / (stop_offset - start_offset) * (stop_value - start_value))) 
    
    def gradient(self):
        def gradient_function(x, y):
            initial_offset = 0.0
            for offset, start, end in self.DATA:
                if y < offset:
                    r = self.linear_gradient(start[0], end[0], initial_offset, offset)(y)
                    g = self.linear_gradient(start[1], end[1], initial_offset, offset)(y)
                    b = self.linear_gradient(start[2], end[2], initial_offset, offset)(y)
                    return r, g, b
                initial_offset = offset
        return gradient_function
    
    def generate(self, steps=60, format='hex'):
        fh = float(steps)
        results = []
        count = 1
        for y in range(steps):
            fy = float(y)
            color_out = [int(v ) for v in self.gradient()(0, fy / fh)] 
            if format == 'hex':
                print color_out
                color_out = ["#" + "".join(map(lambda x: "%0.2X" % x,  color_out[0:3]),)]
                print color_out
            results.append( [count,] + color_out ) 
            count += 1
        return results


"""
# Usage Example
grd_data =  [
    (0.15, '#FFD3d3', '#ff3030'), 
    (0.75,  '#ff3030', '#0241fc'), 
    (1.0,  '#0241fc', '#0241fc'), 
]

grad_gen = GradientGenerator(grd_data)
grad_gen.generate()


grd_data = [
    (0.15, (0xFF, 0xD3, 0xd3), (0xff, 0x30, 0x30)), 
    (0.75, (0xff, 0x30, 0x30), (0x02, 0x41, 0xfc)), 
    (1.0,  (0x02, 0x41, 0xfc), (0x02, 0x41, 0xfc)), 
]

grad_gen = GradientGenerator(grd_data)
grad_gen.generate(format='int')

"""

