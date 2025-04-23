from OpenGL.GL import *

class Score:
    def __init__(self, x=0.0, y=0.7, width=0.08, height=0.13, spacing=0.02,
                 color=(1.0,1.0,1.0), thickness=4.0):
        self.value = 0
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.spacing = spacing
        self.color = color
        self.thickness = thickness
        half_h = height/2
        w, h = width, height
        # 7 segmentos (start,end) relativos
        self._segments = [
            ((0,h),(w,h)),       # top
            ((0,half_h),(w,half_h)),# middle
            ((0,0),(w,0)),       # bottom
            ((0,half_h),(0,h)),  # top-left
            ((w,half_h),(w,h)),  # top-right
            ((0,0),(0,half_h)),  # bottom-left
            ((w,0),(w,half_h))   # bottom-right
        ]
        self._digit_map = {
            0: [0,2,3,4,5,6],
            1: [4,6],
            2: [0,1,2,5,4],
            3: [0,1,2,4,6],
            4: [1,3,4,6],
            5: [0,1,2,3,6],
            6: [0,1,2,3,5,6],
            7: [0,4,6],
            8: list(range(7)),
            9: [0,1,2,3,4,6],
        }

    def reset(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def draw(self):
        s = str(self.value)
        total_w = len(s)*(self.width+self.spacing)-self.spacing
        start = self.x - total_w/2

        glColor3f(*self.color)
        glLineWidth(self.thickness)
        glBegin(GL_LINES)
        for i, ch in enumerate(s):
            d = int(ch)
            dx = start + i*(self.width+self.spacing)
            for seg in self._digit_map[d]:
                (x0,y0),(x1,y1) = self._segments[seg]
                glVertex2f(dx + x0, self.y + y0)
                glVertex2f(dx + x1, self.y + y1)
        glEnd()
        glLineWidth(1.0)
