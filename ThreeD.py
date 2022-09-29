from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import math
from operator import itemgetter

scale = 0.5
perspective = 1400

def convertPoint(vec, sw, sh):
	scale = 0.5
	x3d = vec.y() * scale
	y3d = vec.z() * scale
	depth = vec.x() * scale
	newVal = setScale(x3d, y3d, depth)
	x2d = int(sw / 2 + newVal[0])
	y2d = int(sh / 2 - newVal[1])
	return QPoint(x2d, y2d);

def convertPoints(vec, sw, sh):
	scale = 0.5
	pp2d = []
	for i in range(len(vec)):
		x3d = vec[i].y() * scale
		y3d = vec[i].z() * scale
		depth = vec[i].x() * scale
		newVal = setScale(x3d, y3d, depth)
		x2d = int(sw / 2 + newVal[0])
		y2d = int(sh / 2 - newVal[1])
		pp2d.append(QPoint(x2d, y2d))
	return pp2d;

def convertPoints3D(vec, sw, sh):
	scale = 0.5
	pp2d = []
	for i in range(len(vec)):
		x3d = vec[i].y() * scale
		y3d = vec[i].z() * scale
		depth = int(vec[i].x() * scale)
		newVal = setScale(x3d, y3d, depth)
		x2d = int(sw / 2 + newVal[0])
		y2d = int(sh / 2 - newVal[1])
		pp2d.append(QVector3D(x2d, y2d, depth))
	return pp2d;

def setScale(x3d, y3d, depth):
	perspective = 1400
	dist = math.sqrt(x3d * x3d + y3d * y3d) #distance from oragin
	theta = math.atan2(y3d, x3d)
	depth2 = 15 - depth
	localScale = abs(perspective / (depth2 + perspective))
	dist *= localScale
	newVal = [dist * math.cos(theta), dist * math.sin(theta)]
	return newVal;

def rotateAxisX(p, cp, ang):
	return QVector3D(
	 	p.x(),
	 	cp.y() + ((p.y() - cp.y()) * math.cos(ang) - (p.z() - cp.z()) * math.sin(ang)),
	 	cp.z() + ((p.z() - cp.z()) * math.cos(ang) + (p.y() - cp.y()) * math.sin(ang))
	 	)
    
def rotateAxisY(p, cp, ang):
	return QVector3D(
		cp.x() + ((p.x() - cp.x()) * math.cos(ang) - (p.z() - cp.z()) * math.sin(ang)),
		p.y(),
		cp.z() + ((p.z() - cp.z()) * math.cos(ang) + (p.x() - cp.x()) * math.sin(ang))
		)

def rotateAxisZ(p, cp, ang):
	return QVector3D(
		cp.x() + ((p.x() - cp.x()) * math.cos(ang) - (p.y() - cp.y()) * math.sin(ang)),
		cp.y() + ((p.y() - cp.y()) * math.cos(ang) + (p.x() - cp.x()) * math.sin(ang)),
		p.z()
		)
