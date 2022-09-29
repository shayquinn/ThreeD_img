from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import numpy as np


#http://jsfiddle.net/mrbendel/6rbtde5t/1/
def centroid(pl):
	sx, sy, sz = 0, 0, 0
	for i in range(len(pl)):
		sx += pl[i].x()
		sy += pl[i].y()
		sz += pl[i].z()	
	return QVector3D(sx/len(pl), sy/len(pl), sz/len(pl))

def surface_normal(centroid, p1, p2, p3):
    a = p2-p1
    b = p3-p1
    n = np.cross(a,b)
    n = sqrt(n[0]**2 + n[1]**2 + n[2]**2)
    pmid = (p1 + p2 + p3) / 3
    dist_centroid = np.linalg.norm(pmid - centroid)
 
def calculateGeometry(subs, divs, Pixmap, vec):
	triangles = [[],[]]

	p1 = vec[1]
	p2 = vec[0]
	p3 = vec[3]
	p4 = vec[2]

	dx1 = p4.x() - p1.x()
	dy1 = p4.y() - p1.y()

	dx2 = p3.x() - p2.x()
	dy2 = p3.y() - p2.y()


	imgW = Pixmap.width()    
	imgH = Pixmap.height()

	divdiv = 0
	for sub in range(subs):
		curRow = sub / subs
		nextRow = (sub + 1) / subs

		curRowX1 = p1.x() + dx1 * curRow
		curRowY1 = p1.y() + dy1 * curRow

		curRowX2 = p2.x() + dx2 * curRow
		curRowY2 = p2.y() + dy2 * curRow

		nextRowX1 = p1.x() + dx1 * nextRow
		nextRowY1 = p1.y() + dy1 * nextRow

		nextRowX2 = p2.x() + dx2 * nextRow
		nextRowY2 = p2.y() + dy2 * nextRow

		for div in range(divs):
			curCol = div / divs
			nextCol = (div + 1) / divs

			dCurX = curRowX2 - curRowX1
			dCurY = curRowY2 - curRowY1

			dNextX = nextRowX2 - nextRowX1
			dNextY = nextRowY2 - nextRowY1

			p1x = curRowX1 + dCurX * curCol
			p1y = curRowY1 + dCurY * curCol

			p2x = curRowX1 + (curRowX2 - curRowX1) * nextCol
			p2y = curRowY1 + (curRowY2 - curRowY1) * nextCol

			p3x = nextRowX1 + dNextX * nextCol
			p3y = nextRowY1 + dNextY * nextCol

			p4x = nextRowX1 + dNextX * curCol
			p4y = nextRowY1 + dNextY * curCol

			u1 = curCol * imgW
			u2 = nextCol * imgW
			v1 = curRow * imgH
			v2 = nextRow * imgH

			p1x if p1x else 0, p1y if p1y else 0
			p2x if p2x else 0, p2y if p2y else 0
			p3x if p3x else 0, p3y if p3y else 0
			p4x if p4x else 0, p4y if p4y else 0

			u1 = u1 if u1 else 0
			u2 = u2 if u2 else 0
			v1 = v1 if v1 else 0
			v2 = v2 if v2 else 0

			triangle1 = {
			't':[QPoint(int(p1x), int(p1y)), QPoint(int(p3x), int(p3y)), QPoint(int(p4x), int(p4y))], 
			'tx':[QPoint(int(u1), int(v1)),QPoint(int(u2), int(v2)),QPoint(int(u1), int(v2))]
			}

			triangle2 = {
			't':[QPoint(int(p1x), int(p1y)), QPoint(int(p2x), int(p2y)), QPoint(int(p3x), int(p3y))], 
			'tx':[QPoint(int(u1), int(v1)),QPoint(int(u2), int(v1)),QPoint(int(u2), int(v2))]
			}

			if div<divdiv:
				triangles[1].append(triangle1)
				triangles[1].append(triangle2)
				pass
			if div>divdiv:
				triangles[0].append(triangle1)
				triangles[0].append(triangle2)
				pass
			if div==divdiv:	
				triangles[1].append(triangle1)
				triangles[0].append(triangle2)
				pass
			
		divdiv += 1
	c0 = centroid([p1, p2, p3, p4])
	c1 = centroid([p1, p2, p3])
	c2 = centroid([p1, p3, p4])
	return {'c':c0,'cz':c0.z(),'cs':[c1, c2],'p':[[p1, p2, p3],[p1, p3, p4]],'t':triangles,'pix':Pixmap}

def Tform(x0, y0, x1, y1, x2, y2, sx0, sy0, sx1, sy1, sx2, sy2):
	# TODO: eliminate common subexpressions.
	denom = sx0 * (sy2 - sy1) - sx1 * sy2 + sx2 * sy1 + (sx1 - sx2) * sy0
	if denom == 0:
		return			    
	m11 = -(sy0 * (x2 - x1) - sy1 * x2 + sy2 * x1 + (sy1 - sy2) * x0) / denom
	m12 = (sy1 * y2 + sy0 * (y1 - y2) - sy2 * y1 + (sy2 - sy1) * y0) / denom
	m21 = (sx0 * (x2 - x1) - sx1 * x2 + sx2 * x1 + (sx1 - sx2) * x0) / denom
	m22 = -(sx1 * y2 + sx0 * (y1 - y2) - sx2 * y1 + (sx2 - sx1) * y0) / denom
	dx = (sx0 * (sy2 * x1 - sy1 * x2) + sy0 * (sx1 * x2 - sx2 * x1) + (sx2 * sy1 - sx1 * sy2) * x0) / denom
	dy = (sx0 * (sy2 * y1 - sy1 * y2) + sy0 * (sx1 * y2 - sx2 * y1) + (sx2 * sy1 - sx1 * sy2) * y0) / denom
	return m11, m12, m21, m22, dx, dy
