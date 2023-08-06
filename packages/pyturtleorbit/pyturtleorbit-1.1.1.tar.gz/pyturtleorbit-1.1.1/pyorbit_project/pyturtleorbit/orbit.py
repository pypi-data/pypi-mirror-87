import math,turtle
def rad(x):
	return math.pi*x/180

def orbit(turt,originx,originy,radius,dangle,angle=None):
	if angle==None:
		try:
			angle=turt.angle
		except:
			angle=0
	turt.goto(originx+radius*math.cos(rad(angle)),originy+radius *math.sin(rad(angle)))
	turt.angle=(angle+dangle) % 360