from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import numpy as np
import sys 
import ThreeD_PointConverter as PointConverter
import ThreeD_Warp
import ThreeD_Warp2
class Window(QMainWindow):
	cw, ch = 1000, 700
	rotX, rotY, rotZ = 0, 0, 0
	rotation = QVector3D(0, 0, 0) 
	cp = QVector3D(50, 50, 0)
	xycp = None
	boxW, boxH, boxD = 200, 400, 600
	boxx, boxy = cp.x()-(boxW/2), cp.y()-(boxH/2)
	vec = [
		QVector3D(boxx, boxy, boxD/2),
	 	QVector3D(boxx+boxW, boxy, boxD/2),
	  	QVector3D(boxx+boxW, boxy+boxH, boxD/2),
	   	QVector3D(boxx, boxy+boxH, boxD/2),
	   	QVector3D(boxx, boxy, -abs(boxD/2)),
	 	QVector3D(boxx+boxW, boxy, -abs(boxD/2)),
	  	QVector3D(boxx+boxW, boxy+boxH, -abs(boxD/2)),
	   	QVector3D(boxx, boxy+boxH, -abs(boxD/2))
	   ]

	xyVec = None
	triangles = None
	Pixmap = None
	cenp = None
	draw_order = None
	order = None
	tick = 100
	curr_time = None
	timer = None

	subs = 12 
	divs = 12 

	RX,RY,RZ = False,False,False
	pic, poly, smallPoly, centroid, centroids =  False, True, False, False, False
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):	
		self.setWindowTitle("App :)")
		self.setGeometry(50, 50, self.cw, self.ch)
		#self.showMaximized() 
		self.setMouseTracking(True)
		# creating canvas 
		self.image = QImage(self.size(), QImage.Format_RGB32)
		# setting canvas color to white
		self.image.fill(Qt.gray)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("File")

		RXAction = QAction("Rotate X", self)
		RXAction.setShortcut("Ctrl + X")
		fileMenu.addAction(RXAction)
		RXAction.triggered.connect(self.rotatex)

		RYAction = QAction("Rotate Y", self)
		RYAction.setShortcut("Ctrl + Y")
		fileMenu.addAction(RYAction)
		RYAction.triggered.connect(self.rotatey)

		RZAction = QAction("Rotate Z", self)
		RZAction.setShortcut("Ctrl + Z")
		fileMenu.addAction(RZAction)
		RZAction.triggered.connect(self.rotatez)


		PicAction = QAction("Image", self)
		PicAction.setShortcut("Ctrl + I")
		fileMenu.addAction(PicAction)
		PicAction.triggered.connect(self.picture)

		PolyAction = QAction("Larg Poly", self)
		PolyAction.setShortcut("Ctrl + L")
		fileMenu.addAction(PolyAction)
		PolyAction.triggered.connect(self.poly_L)

		SmallPolyAction = QAction("Small Poly", self)
		SmallPolyAction.setShortcut("Ctrl + S")
		fileMenu.addAction(SmallPolyAction)
		SmallPolyAction.triggered.connect(self.poly_S)

		CentroidAction = QAction("Centroid", self)
		CentroidAction.setShortcut("Ctrl + 1")
		fileMenu.addAction(CentroidAction)
		CentroidAction.triggered.connect(self.centroid_1)

		CentroidsAction = QAction("Centroid 2", self)
		CentroidsAction.setShortcut("Ctrl + 2")
		fileMenu.addAction(CentroidsAction)
		CentroidsAction.triggered.connect(self.centroid_2)


#rotatex rotatey rotatez pic poly_L poly_S Centroid_1 Centroid_2

		quitAction = QAction("Quit", self)
		quitAction.setShortcut("Ctrl + Q")
		fileMenu.addAction(quitAction)
		quitAction.triggered.connect(self.quit)

		timer = QTimer(self)
		timer.timeout.connect(self.showTime)
		timer.start(self.tick) # update every second

		self.Pixmap = [
		QPixmap("img/m11.png"),
		QPixmap("img/m12.png"),
		QPixmap("img/img2.png"),
		QPixmap("img/img1.png"),
		QPixmap("img/m14.png"),
		QPixmap("img/m15.png")
		]


	def contextMenuEvent(self, event):
		cmenu = QMenu(self)
		rotatexAct = cmenu.addAction("Rotate X")
		rotateyAct = cmenu.addAction("Rotate Y")
		rotatezAct = cmenu.addAction("Rotate Y")
		picAct = cmenu.addAction("Image")
		poly_LAct = cmenu.addAction("Larg Poly")
		poly_SAct = cmenu.addAction("Small Poly")
		Centroid_1Act = cmenu.addAction("Centroid")
		Centroid_2Act = cmenu.addAction("Centroid 2")
		quitAct = cmenu.addAction("Quit")
		action = cmenu.exec_(self.mapToGlobal(event.pos()))
		if action == rotatexAct:
			self.rotatex()
		elif action == rotateyAct:
			self.rotatey()
		elif action == rotatezAct:
			self.rotatez()
		elif action == picAct:
			self.picture()
		elif action == poly_LAct:
			self.poly_L()
		elif action == poly_SAct:
			self.poly_S()
		elif action == Centroid_1Act:
			self.centroid_1()
		elif action == Centroid_2Act:
			self.centroid_2()
		elif action == quitAct:
			self.quit()

	#rotatex rotatey rotatez pic poly_L poly_S Centroid_1 Centroid_2

	def quit(self):
		qApp.quit()

	def rotatex(self):
		if self.rotation.x():
			self.rotation.setX(0)
		else:
			self.rotation.setX(0.1)
		pass
	def rotatey(self):
		if self.rotation.y():
			self.rotation.setY(0)
		else:
			self.rotation.setY(0.1)
		pass
	def rotatez(self):
		if self.rotation.z():
			self.rotation.setZ(0)
		else:
			self.rotation.setZ(0.1)
		pass

	def picture(self):
		if self.pic:
			self.pic = False
		else:
			self.pic = True
		self.update()

	def poly_L(self):
		if self.poly:
			self.poly = False
		else:
			self.poly = True
		self.update()	 	

	def poly_S(self):
		if self.smallPoly:
			self.smallPoly = False
		else:
			self.smallPoly = True
		self.update()

	def centroid_1(self):
		if self.centroid:
			self.centroid = False
		else:
			self.centroid = True
		self.update()	

	def centroid_2(self):
		if self.centroids:
			self.centroids = False
		else:
			self.centroids = True
		self.update()	


	def setAntialiasing(self, p):
		#p.setRenderHint(p.Antialiasing, True)
		p.setRenderHint(p.HighQualityAntialiasing, True)
		#p.setRenderHint(p.SmoothPixmapTransform, True)
		#p.setRenderHint(p.TextAntialiasing, True)
		#p.setRenderHint(p.NonCosmeticDefaultPen, True)
		pass

	# paintEvent for creating blank canvas 
	def paintEvent(self, event):
		canvasPainter = QPainter(self)
		canvasPainter.drawImage(self.rect(), self.image, self.image.rect())


	def drawTriangleSegments(self, list):
		for tr in list:
			if self.pic:		
				for t in tr['t']:
					for e in t:	
						x0, y0 = e['t'][0].x(), e['t'][0].y()
						x1, y1 = e['t'][1].x(), e['t'][1].y()
						x2, y2 = e['t'][2].x(), e['t'][2].y()
						sx0, sy0 = e['tx'][0].x(), e['tx'][0].y()
						sx1, sy1 = e['tx'][1].x(), e['tx'][1].y()
						sx2, sy2 = e['tx'][2].x(), e['tx'][2].y()			
						painter = QPainter(self.image)
						#self.setAntialiasing(painter)
						path = QPainterPath()
						path.moveTo (x0, y0)
						path.lineTo (x1, y1)
						path.lineTo (x2, y2)
						path.lineTo (x0, y0)
						painter.setClipPath(path)		
						re = ThreeD_Warp2.Tform(x0, y0, x1, y1, x2, y2, sx0, sy0, sx1, sy1, sx2, sy2)
						transform = QTransform(re[0], re[1], re[2], re[3], re[4], re[5])
						painter.setTransform(transform)
						painter.drawPixmap(0, 0, tr['pix'])
						painter.end()

			if self.smallPoly:
				lt = 0
				for t in tr['t']:
					for e in t:				
						painter = QPainter(self.image)
						self.setAntialiasing(painter)	
						pen = QPen()				
						pen.setWidth(1)
						if lt == 0:
							pen.setColor(QColor("red"))  # r, g, b
						else:
							pen.setColor(QColor("green"))  # r, g, b
						path = QPainterPath()
						path.moveTo (e['t'][0].x(), e['t'][0].y())	
						path.lineTo (e['t'][1].x(), e['t'][1].y())
						path.lineTo (e['t'][2].x(), e['t'][2].y())
						path.lineTo (e['t'][0].x(), e['t'][0].y())
						painter.setPen(pen)
						painter.drawPath(path)
						painter.end()
					lt+=1	

			if self.poly:
				for p in tr['p']:
					painter = QPainter(self.image)
					self.setAntialiasing(painter)	
					pen = QPen()				
					pen.setWidth(2)
					pen.setColor(QColor("blue"))  # r, g, b
					path = QPainterPath()
					path.moveTo (p[0].x(), p[0].y())	
					path.lineTo (p[1].x(), p[1].y())
					path.lineTo (p[2].x(), p[2].y())
					path.lineTo (p[0].x(), p[0].y())
					painter.setPen(pen)
					painter.drawPath(path)
					painter.end()

			if self.centroids:
				i = 0
				for c in tr['cs']:
					painter = QPainter(self.image)
					self.setAntialiasing(painter)
					brush = QBrush()
					if i:
						color = 'green'
					else:
						color = 'red'		
					brush.setColor(QColor(color))
					brush.setStyle(Qt.SolidPattern)
					painter.setBrush(brush)
					painter.drawEllipse(int(c.x())-4, int(c.y())-4, 8, 8)					
					painter.end()
					i+=1

			if self.centroid:
				painter = QPainter(self.image)
				self.setAntialiasing(painter)
				brush = QBrush()
				color = 'white'
				brush.setColor(QColor(color))
				brush.setStyle(Qt.SolidPattern)
				painter.setBrush(brush)
				painter.drawEllipse(int(tr['c'].x())-5, int(tr['c'].y())-5, 10, 10)					
				painter.end()

		self.update()
	

	def showTime(self):
		#print(QTime.currentTime())
		self.rotate(self.vec, self.cp, self.rotation)
			
		
		self.xycp = PointConverter.convertPoint(self.cp, self.cw, self.ch)
		self.xyVec = PointConverter.convertPoints3D(self.vec, self.cw, self.ch)
		self.triangles = []
		nv = [
		[self.xyVec[0],	self.xyVec[1], self.xyVec[2], self.xyVec[3]],
		[self.xyVec[4],	self.xyVec[5], self.xyVec[6], self.xyVec[7]],
		[self.xyVec[0],	self.xyVec[3], self.xyVec[7], self.xyVec[4]],
		[self.xyVec[1],	self.xyVec[2], self.xyVec[6], self.xyVec[5]],
		[self.xyVec[0],	self.xyVec[1], self.xyVec[5], self.xyVec[4]],
		[self.xyVec[3],	self.xyVec[2], self.xyVec[6], self.xyVec[7]]
		]

		for i in range(len(nv)):
			self.triangles.append(ThreeD_Warp2.calculateGeometry(self.subs, self.divs, self.Pixmap[i], nv[i]))
		self.draw_order = []
		self.triangles = sorted(self.triangles, key = lambda i: i['cz'],reverse=False)
		self.image.fill(Qt.gray)
		self.drawTriangleSegments(self.triangles)

	def rotate(self, vec, cp, rotation):
		self.rotX += rotation.x()
		self.rotY += rotation.y()
		self.rotZ += rotation.z()
		for i in range(len(vec)):	
			vec[i]=PointConverter.rotateAxisX(vec[i], self.cp, rotation.x())
			vec[i]=PointConverter.rotateAxisY(vec[i], self.cp, rotation.y())
			vec[i]=PointConverter.rotateAxisZ(vec[i], self.cp, rotation.z())
	


# main method 
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Window()
	window.show()   
	# looping for window
	sys.exit(app.exec())

