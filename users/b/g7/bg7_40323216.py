# 各組分別在各自的 .py 程式中建立應用程式 (第1步/總共3步)
from flask import Blueprint, render_template, make_response, request

# 利用 Blueprint建立 ag1, 並且 url 前綴為 /ag1, 並設定 template 存放目錄
bg7_40323216 = Blueprint('bg7_40323216', __name__, url_prefix='/bg7_40323216', template_folder='templates')
 
head_str = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 鏈條繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
 
</head>
<body>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id="plotarea" width="800" height="800"></canvas>
'''
 
tail_str = '''
</script>
</body>
</html>
'''
 
chain_str = '''
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為 class variable
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    def __init__(self, fillcolor="green", border=True, strokecolor= "tan", linewidth=2, scale=1):
        self.fillcolor = fillcolor
        self.border = border
        self.strokecolor = strokecolor
        self.linewidth = linewidth
        self.scale = scale
 
    # 利用鏈條起點與終點定義繪圖
    def basic(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, self.scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, v=False):
        # 若 v 為 True 則為虛擬 chain, 不 render
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.v = v
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)*self.scale
        y2 = y1 + 20*math.sin(rot*deg)*self.scale
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        if v == False:
            cgo.render(basic1, x1, y1, self.scale, 0)
 
        return x2, y2
'''


def circle36(x, y, degree):
    # 20 為鏈條輪廓之圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
    
    outstring = '''
mychain = chain()
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''

    for i in range(2, int(repeat)+1):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"

    return outstring
    
def circle35(x, y, degree,a,b,degree2):
    # 20 為鏈條輪廓之圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
    sec_degree = 90 - degree2
    repeat2 = 360 / degree2
    outstring1 = '''
mychain = chain()
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    outstring2 = '''
mychain = chain()
x1, y1 = mychain.basic_rot('''+str(a)+","+str(b)+", "+str(sec_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring1 += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
    for e in range(2, int(repeat2)+1):
        outstring2 += "x"+str(e)+", y"+str(e)+"=mychain.basic_rot(x"+str(e-1)+", y"+str(e-1)+", 90-"+str(e*degree2)+") \n"
            
    outstring = outstring1 + outstring2 
    
    return outstring
    
@bg7_40323216.route('/circle36/<degree>', defaults={'x': 0, 'y': 0})
@bg7_40323216.route('/circle36/<x>/<degree>', defaults={'y': 0})
@bg7_40323216.route('/circle36/<x>/<y>/<degree>')

def drawcircle36(x, y, degree):
    return head_str + chain_str + circle36(int(x), int(y), int(degree)) + tail_str
    




    


    
    
@bg7_40323216.route('/circle35/<x>/<y>/<degree>/<a>/<b>/<degree2>')
def drawcircle35(x, y, degree, a, b, degree2):
    return head_str + chain_str + circle35(int(x), int(y), int(degree), int(a), int(b), int(degree2)) + tail_str
    
# 傳繪 A 函式內容

def a(x, y, scale=1, color="green"):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain(scale='''+str(scale)+''', fillcolor="'''+str(color)+'''")
 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1)
'''

    return outstring

def a2(a, b, scale=1, color="green"):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain(scale='''+str(scale)+''', fillcolor="'''+str(color)+'''")
 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot('''+str(a)+","+str(b)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1)
'''

    return outstring


@bg7_40323216.route('/a')
def draw_a():
    return head_str + chain_str + a(0, 0) + tail_str
@bg7_40323216.route('/task16_1')
def task16_1():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
</head>
<body>
<script>
window.onload=function(){
brython(1);
}
</script>
<canvas id="plotarea" width="800" height="800"></canvas>
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  

class chain():
    # 輪廓的外型設為成員變數
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    # 利用鏈條起點與終點定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic(self, x1, y1, x2, y2, color="green", border=True, linewidth=4, scale=1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.border = border
        self.linewidth = linewidth
        self.scale = scale
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": color,
                "border": border,
                "strokeColor": "tan",
                "lineWidth": linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, color="green", border=True, linewidth=4, scale=1):
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.color = color
        self.border = border
        self.linewidth = linewidth
        self.scale = scale
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": color,
                "border": border,
                "strokeColor": "tan",
                "lineWidth": linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)
        y2 = y1 + 20*math.sin(rot*deg)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, scale, 0)
 
        return x2, y2
 
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1, color="green")


cgo.setWorldCoords(-315, -250, 500, 500) 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1, color="blue")

cgo.setWorldCoords(-385, -250, 500, 500) 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1, color="red")

cgo.setWorldCoords(-445, -250, 500, 500) 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1, color="green")
</script>
</body></html>
'''
    return outstring
    

@bg7_40323216.route('/task16_2')
def task16_2():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
</head>
<body>
<script>
window.onload=function(){
brython(1);
}
</script>
<canvas id="plotarea" width="800" height="800"></canvas>
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-40, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  

class chain():
    # 輪廓的外型設為成員變數
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    # 利用鏈條起點與終點定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic(self, x1, y1, x2, y2, color="green", border=True, linewidth=4, scale=1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.border = border
        self.linewidth = linewidth
        self.scale = scale
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": color,
                "border": border,
                "strokeColor": "tan",
                "lineWidth": linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, color="green", border=True, linewidth=4, scale=1):
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.color = color
        self.border = border
        self.linewidth = linewidth
        self.scale = scale
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": color,
                "border": border,
                "strokeColor": "tan",
                "lineWidth": linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)
        y2 = y1 + 20*math.sin(rot*deg)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, scale, 0)
 
        return x2, y2
 
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 畫 B
# 左邊四個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 右上垂直向下單元
x7, y7 = mychain.basic_rot(x6, y6, -90)
# 右斜 240 度
x8, y8 = mychain.basic_rot(x7, y7, 210)
# 中間水平
mychain.basic(x8, y8, x2, y2)
# 右下斜 -30 度
x10, y10 = mychain.basic_rot(x8, y8, -30)
# 右下垂直向下單元
x11, y11 = mychain.basic_rot(x10, y10, -90)
# 右下斜 240 度
x12, y12 = mychain.basic_rot(x11, y11, 210)
# 水平接回起點
mychain.basic(x12,y12, 0, 0, color="green")

cgo.setWorldCoords(-107.5, -250, 500, 500) 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1, color="green")

cgo.setWorldCoords(-50, -250, 500, 500) 
# 畫 C
# 上半部
# 左邊中間垂直起點, 圓心位於線段中央, y 方向再向上平移兩個鏈條圓心距單位
x1, y1 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), 90)
# 上方轉 80 度
x2, y2 = mychain.basic_rot(x1, y1, 80)
# 上方轉 30 度
x3, y3 = mychain.basic_rot(x2, y2, 30)
# 上方水平
x4, y4 = mychain.basic_rot(x3, y3, 0)
# 下半部, 從起點開始 -80 度
x5, y5 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), -80)
# 下斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 下方水平單元
x7, y7 = mychain.basic_rot(x6, y6, -0, color="green")

cgo.setWorldCoords(-55, -250, 500, 500) 
# 畫 D
# 左邊四個垂直單元
x1, y1 = mychain.basic_rot(0+65*3, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -40 度
x6, y6 = mychain.basic_rot(x5, y5, -40)
x7, y7 = mychain.basic_rot(x6, y6, -60)
# 右中垂直向下單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
# -120 度
x9, y9 = mychain.basic_rot(x8, y8, -120)
# -140
x10, y10 = mychain.basic_rot(x9, y9, -140)
# 水平接回原點
mychain.basic(x10, y10, 0+65*3, 0, color="green")

</script>
</body></html>
'''
    return outstring



@bg7_40323216.route('/task16_3')
def task16_3():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
</head>
<body>
<script>
window.onload=function(){
brython(1);
}
</script>
<canvas id="plotarea" width="800" height="800"></canvas>
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為成員變數
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    # 利用鏈條起點與終點定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic(self, x1, y1, x2, y2, color="green", border=True, linewidth=4, scale=1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.border = border
        self.linewidth = linewidth
        self.scale = scale
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": color,
                "border": border,
                "strokeColor": "tan",
                "lineWidth": linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, color="green", border=True, linewidth=4, scale=1):
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.color = color
        self.border = border
        self.linewidth = linewidth
        self.scale = scale
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": color,
                "border": border,
                "strokeColor": "tan",
                "lineWidth": linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)
        y2 = y1 + 20*math.sin(rot*deg)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, scale, 0)
 
        return x2, y2
 
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 畫 B
# 左邊四個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 右上垂直向下單元
x7, y7 = mychain.basic_rot(x6, y6, -90)
# 右斜 240 度
x8, y8 = mychain.basic_rot(x7, y7, 210)
# 中間水平
mychain.basic(x8, y8, x2, y2)
# 右下斜 -30 度
x10, y10 = mychain.basic_rot(x8, y8, -30)
# 右下垂直向下單元
x11, y11 = mychain.basic_rot(x10, y10, -90)
# 右下斜 240 度
x12, y12 = mychain.basic_rot(x11, y11, 210)
# 水平接回起點
mychain.basic(x12,y12, 0, 0, color="green")


cgo.setWorldCoords(-247.5, -350, 500, 500) 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot(0, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1, color="green")

cgo.setWorldCoords(-55, -50, 500, 500) 
# 畫 D
# 左邊四個垂直單元
x1, y1 = mychain.basic_rot(0+65*3, 0, 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -40 度
x6, y6 = mychain.basic_rot(x5, y5, -40)
x7, y7 = mychain.basic_rot(x6, y6, -60)
# 右中垂直向下單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
# -120 度
x9, y9 = mychain.basic_rot(x8, y8, -120)
# -140
x10, y10 = mychain.basic_rot(x9, y9, -140)
# 水平接回原點
mychain.basic(x10, y10, 0+65*3, 0, color="green")

cgo.setWorldCoords(-120, -150, 500, 500) 
# 畫 C
# 上半部
# 左邊中間垂直起點, 圓心位於線段中央, y 方向再向上平移兩個鏈條圓心距單位
x1, y1 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), 90)
# 上方轉 80 度
x2, y2 = mychain.basic_rot(x1, y1, 80)
# 上方轉 30 度
x3, y3 = mychain.basic_rot(x2, y2, 30)
# 上方水平
x4, y4 = mychain.basic_rot(x3, y3, 0)
# 下半部, 從起點開始 -80 度
x5, y5 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), -80)
# 下斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 下方水平單元
x7, y7 = mychain.basic_rot(x6, y6, -0, color="green")
</script>
'''
    return outstring

@bg7_40323216.route('/task16_19')
def task16_19():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id="plotarea" width="800" height="800"></canvas>
 
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180 
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為 class variable
    chamber = "M -6.8397, -1.4894             A 7, 7, 0, 1, 0, 6.8397, -1.4894             A 40, 40, 0, 0, 1, 6.8397, -18.511             A 7, 7, 0, 1, 0, -6.8397, -18.511             A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    #chamber = "M 0, 0 L 0, -20 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    def __init__(self, fillcolor="green", border=True, strokecolor= "tan", linewidth=2, scale=1):
        self.fillcolor = fillcolor
        self.border = border
        self.strokecolor = strokecolor
        self.linewidth = linewidth
        self.scale = scale
 
    # 利用鏈條起點與終點定義繪圖
    def basic(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, self.scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, v=False):
        # 若 v 為 True 則為虛擬 chain, 不 render
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.v = v
        # 注意, cgoChamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole0 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)*self.scale
        y2 = y1 + 20*math.sin(rot*deg)*self.scale
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        if v == False:
            cgo.render(basic1, x1, y1, self.scale, 0)
 
        return x2, y2
 
mychain = chain()
 
x1, y1 = mychain.basic_rot(-133.06,49.48, 20.78)
 
x2, y2=mychain.basic_rot(x1, y1,0.7800000000000011, True) 
x3, y3=mychain.basic_rot(x2, y2,-19.22, True) 
x4, y4=mychain.basic_rot(x3, y3,-39.22, True) 
x5, y5=mychain.basic_rot(x4, y4,-59.22, True) 
x6, y6=mychain.basic_rot(x5, y5,-79.22, True) 
x7, y7=mychain.basic_rot(x6, y6,-99.22, True) 
x8, y8=mychain.basic_rot(x7, y7,-119.22, True) 
x9, y9=mychain.basic_rot(x8, y8,-139.22, True) 
x10, y10=mychain.basic_rot(x9, y9,-159.22, True) 
x11, y11=mychain.basic_rot(x10, y10,-179.22, True) 
x12, y12=mychain.basic_rot(x11, y11,-199.22) 
x13, y13=mychain.basic_rot(x12, y12,-219.22) 
x14, y14=mychain.basic_rot(x13, y13,-239.22) 
x15, y15=mychain.basic_rot(x14, y14,-259.22) 
x16, y16=mychain.basic_rot(x15, y15,-279.22) 
x17, y17=mychain.basic_rot(x16, y16,-299.22) 
x18, y18=mychain.basic_rot(x17, y17,-319.22) 
 
#mychain = chain()
 
p1, k1 = mychain.basic_rot(82.11,93.98, 4.78)
p2, k2=mychain.basic_rot(p1, k1,-7.219999999999999) 
p3, k3=mychain.basic_rot(p2, k2,-19.22) 
p4, k4=mychain.basic_rot(p3, k3,-31.22) 
p5, k5=mychain.basic_rot(p4, k4,-43.22) 
p6, k6=mychain.basic_rot(p5, k5,-55.22) 
p7, k7=mychain.basic_rot(p6, k6,-67.22) 
p8, k8=mychain.basic_rot(p7, k7,-79.22) 
p9, k9=mychain.basic_rot(p8, k8,-91.22) 
p10, k10=mychain.basic_rot(p9, k9,-103.22) 
p11, k11=mychain.basic_rot(p10, k10,-115.22) 
p12, k12=mychain.basic_rot(p11, k11,-127.22) 
p13, k13=mychain.basic_rot(p12, k12,-139.22) 
p14, k14=mychain.basic_rot(p13, k13,-151.22) 
p15, k15=mychain.basic_rot(p14, k14,-163.22) 
p16, k16=mychain.basic_rot(p15, k15,-175.22) 
p17, k17=mychain.basic_rot(p16, k16,-187.22) 
p18, k18=mychain.basic_rot(p17, k17,-199.22, True) 
p19, k19=mychain.basic_rot(p18, k18,-211.22, True) 
p20, k20=mychain.basic_rot(p19, k19,-223.22, True) 
p21, k21=mychain.basic_rot(p20, k20,-235.22, True) 
p22, k22=mychain.basic_rot(p21, k21,-247.22, True) 
p23, k23=mychain.basic_rot(p22, k22,-259.22, True) 
p24, k24=mychain.basic_rot(p23, k23,-271.22, True) 
p25, k25=mychain.basic_rot(p24, k24,-283.22, True) 
p26, k26=mychain.basic_rot(p25, k25,-295.22, True) 
p27, k27=mychain.basic_rot(p26, k26,-307.22, True) 
p28, k28=mychain.basic_rot(p27, k27,-319.22, True) 
p29, k29=mychain.basic_rot(p28, k28,-331.22, True) 
p30, k30=mychain.basic_rot(p29, k29,-343.22, True) 
 
m1, n1 = mychain.basic_rot(x1, y1, 10.78)
m2, n2=mychain.basic_rot(m1, n1, 10.78)
m3, n3=mychain.basic_rot(m2, n2, 10.78)
m4, n4=mychain.basic_rot(m3, n3, 10.78)
m5, n5=mychain.basic_rot(m4, n4, 10.78)
m6, n6=mychain.basic_rot(m5, n5, 10.78)
m7, n7=mychain.basic_rot(m6, n6, 10.78)
m8, n8=mychain.basic_rot(m7, n7, 10.78)
m9, n9=mychain.basic_rot(m8, n8, 10.78)
m10, n10=mychain.basic_rot(m9, n9, 10.78)
 
r1, s1 = mychain.basic_rot(x11, y11, -10.78)
r2, s2=mychain.basic_rot(r1, s1, -10.78)
r3, s3=mychain.basic_rot(r2, s2, -10.78)
r4, s4=mychain.basic_rot(r3, s3, -10.78)
r5, s5=mychain.basic_rot(r4, s4, -10.78)
r6, s6=mychain.basic_rot(r5, s5, -10.78)
r7, s7=mychain.basic_rot(r6, s6, -10.78)
r8, s8=mychain.basic_rot(r7, s7, -10.78)
r9, s9=mychain.basic_rot(r8, s8, -10.78)
r10, s10=mychain.basic_rot(r9, s9, -10.78)
</script>
</body></html>
'''
    return outstring

from flask import Blueprint, request
 
bg7_40323216 = Blueprint('bg7_40323216', __name__, url_prefix='/bg7_40323216', template_folder='templates')
 
head_str = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
 
</head>
<body>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id="plotarea" width="800" height="800"></canvas>
'''
 
tail_str = '''
</script>
</body>
</html>
'''
 
chain_str = '''
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為 class variable
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    #chamber = "M 0, 0 L 0, -20 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    def __init__(self, fillcolor="green", border=True, strokecolor= "tan", linewidth=2, scale=1):
        self.fillcolor = fillcolor
        self.border = border
        self.strokecolor = strokecolor
        self.linewidth = linewidth
        self.scale = scale
 
    # 利用鏈條起點與終點定義繪圖
    def basic(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, self.scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, v=False):
        # 若 v 為 True 則為虛擬 chain, 不 render
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.v = v
        # 注意, cgoChamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole0 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)*self.scale
        y2 = y1 + 20*math.sin(rot*deg)*self.scale
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        if v == False:
            cgo.render(basic1, x1, y1, self.scale, 0)
 
        return x2, y2
'''
 
# 傳繪 A 函式內容
def a(x, y, scale=1, color="green"):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain(scale='''+str(scale)+''', fillcolor="'''+str(color)+'''")
 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1)
'''
 
    return outstring
 
 
# 傳繪 B 函式內容
def b(x, y):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 畫 B
# 左邊四個垂直單元
# 每一個字元間隔為 65 pixels
#x1, y1 = mychain.basic_rot(0+ 65, 0, 90)
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 右上垂直向下單元
x7, y7 = mychain.basic_rot(x6, y6, -90)
# 右斜 240 度
x8, y8 = mychain.basic_rot(x7, y7, 210)
# 中間水平
mychain.basic(x8, y8, x2, y2)
# 右下斜 -30 度
x10, y10 = mychain.basic_rot(x8, y8, -30)
# 右下垂直向下單元
x11, y11 = mychain.basic_rot(x10, y10, -90)
# 右下斜 240 度
x12, y12 = mychain.basic_rot(x11, y11, 210)
# 水平接回起點
mychain.basic(x12,y12, '''+str(x)+","+str(y)+''')
'''
 
    return outstring
 
# 傳繪 C 函式內容
def c(x, y):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 上半部
# 左邊中間垂直起點, 圓心位於線段中央, y 方向再向上平移兩個鏈條圓心距單位
#x1, y1 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), 90)
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+'''-10+10+20*math.sin(80*deg)+20*math.sin(30*deg), 90)
# 上方轉 80 度
x2, y2 = mychain.basic_rot(x1, y1, 80)
# 上方轉 30 度
x3, y3 = mychain.basic_rot(x2, y2, 30)
# 上方水平
x4, y4 = mychain.basic_rot(x3, y3, 0)
# 下半部, 從起點開始 -80 度
#x5, y5 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), -80)
x5, y5 = mychain.basic_rot('''+str(x)+","+str(y)+'''-10+10+20*math.sin(80*deg)+20*math.sin(30*deg), -80)
# 下斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 下方水平單元
x7, y7 = mychain.basic_rot(x6, y6, -0)
'''
 
    return outstring
 
 
# 傳繪 D 函式內容
def d(x, y):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 左邊四個垂直單元
#x1, y1 = mychain.basic_rot(0+65*3, 0, 90)
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -40 度
x6, y6 = mychain.basic_rot(x5, y5, -40)
x7, y7 = mychain.basic_rot(x6, y6, -60)
# 右中垂直向下單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
# -120 度
x9, y9 = mychain.basic_rot(x8, y8, -120)
# -140
x10, y10 = mychain.basic_rot(x9, y9, -140)
# 水平接回原點
#mychain.basic(x10, y10, 0+65*3, 0, color="red")
mychain.basic(x10, y10, '''+str(x)+","+str(y)+''')
'''
 
    return outstring
 
def circle(x, y):
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 50)
'''
    for i in range(2, 10):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*40)+") \n"
    return outstring
 
def circle1(x, y, degree=10):
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
    return outstring
 
 
def circle2(x, y, degree=10):
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
 
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
    return outstring
 
 
def twocircle(x, y):
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    x = 50
    y = 0
    degree = 12
    # 78, 66, 54, 42, 30, 18, 6度
    #必須有某些 chain 算座標但是不 render
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節也是 virtual chain
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''', True)
#x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    # 這裡要上下各多留一節虛擬 chain, 以便最後進行連接 (x7, y7) 與 (x22, y22)
    for i in range(2, int(repeat)+1):
        #if i < 7 or i > 23:        
        if i <= 7 or i >= 23:
            # virautl chain
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+", True) \n"
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
    p = -150
    k = 0
    degree = 20
    # 70, 50, 30, 10
    # 從 i=5 開始, 就是 virautl chain
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
p1, k1 = mychain.basic_rot('''+str(p)+","+str(k)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        if i >= 5 and i <= 13:
            # virautl chain
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+", True) \n"
            #outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
    # 上段連接直線
    # 從 p5, k5 作為起點
    first_degree = 10
    repeat = 11
    outstring += '''
m1, n1 = mychain.basic_rot(p4, k4, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "m"+str(i)+", n"+str(i)+"=mychain.basic_rot(m"+str(i-1)+", n"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 下段連接直線
    # 從 p12, k12 作為起點
    first_degree = -10
    repeat = 11
    outstring += '''
r1, s1 = mychain.basic_rot(p13, k13, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "r"+str(i)+", s"+str(i)+"=mychain.basic_rot(r"+str(i-1)+", s"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 上段右方接點為 x7, y7, 左側則為 m11, n11
    outstring += "mychain.basic(x7, y7, m11, n11)\n"
    # 下段右方接點為 x22, y22, 左側則為 r11, s11
    outstring += "mychain.basic(x22, y22, r11, s11)\n"
 
    return outstring
def eighteenthirty(x, y):
    '''
從圖解法與符號式解法得到的兩條外切線座標點
(-203.592946177111, 0.0), (0.0, 0.0), (-214.364148466539, 56.5714145924675), (-17.8936874260919, 93.9794075692901)
(-203.592946177111, 0.0), (0.0, 0.0), (-214.364148466539, -56.5714145924675), (-17.8936874260919, -93.9794075692901)
左邊關鍵鍊條起點 (-233.06, 49.48), 角度 20.78, 圓心 (-203.593, 0.0)
右邊關鍵鍊條起點 (-17.89, 93.9), 角度 4.78, 圓心 (0, 0)
    '''
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    x = 50
    y = 0
    degree = 20
    first_degree = 20.78
    startx = -233.06+100
    starty = 49.48
    repeat = 360 / degree
    # 先畫出左邊第一關鍵節
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(startx)+","+str(starty)+", "+str(first_degree)+''')
 
'''
    # 接著繪製左邊的非虛擬鍊條
    for i in range(2, int(repeat)+1):
        if i >=2 and i <=11:
            # virautl chain
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+", True) \n"
        else:
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
 
    # 接著處理右邊的非虛擬鍊條
    # 先畫出右邊第一關鍵節
 
    p = -17.89+100
    k = 93.98
    degree = 12
    first_degree = 4.78
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
p1, k1 = mychain.basic_rot('''+str(p)+","+str(k)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        if i >=18:
            # virautl chain
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+", True) \n"
            #outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
        else:
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
 
    # 上段連接直線
    # 從 x1, y1 作為起點
    first_degree = 10.78
    repeat = 10
    outstring += '''
m1, n1 = mychain.basic_rot(x1, y1, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "m"+str(i)+", n"+str(i)+"=mychain.basic_rot(m"+str(i-1)+", n"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 下段連接直線
    # 從 x11, y11 作為起點
    first_degree = -10.78
    repeat = 10
    outstring += '''
r1, s1 = mychain.basic_rot(x11, y11, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "r"+str(i)+", s"+str(i)+"=mychain.basic_rot(r"+str(i-1)+", s"+str(i-1)+", "+str(first_degree)+")\n"
 
    return outstring
    
    
    
    
    
@bg7_40323216.route('/snap_gear')
def snap_gear():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
    <script type="text/javascript" src="/static/snap.svg-min.js"></script>
 
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
 
<svg width="800" height="800" viewBox="0 0 800 800" id="svgout"></svg>
 
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window, document
 
# 透過 window 與 JSConstructor 從 Brython 物件 snap 擷取 Snap 物件的內容
snap = JSConstructor(window.Snap)
 
s = snap("#svgout")
# 畫直線
s.line(0, 0, 100, 100).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "1"  }).attr({ 'id': 'line1' })
</script>
</body>
</html>
'''
    return outstring
 
