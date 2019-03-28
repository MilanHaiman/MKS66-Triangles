from display import *
from draw import *
from parser import *
from matrix import *
import math

screen = new_screen()
green = [0,255,0]
blue = [0,0,255]
red = [255,0,0]
pink = [255,100,100]
white = [255,255,255]
grey = [150,150,150]
yellow = [255,255,0]
light_blue = [100,100,255]

sphere_color = blue
circle_color = red
tangent_color = circle_color
line_color = yellow



edges = []
polygons = []
transform = new_matrix()

# parse_file( 'script2', edges, polygons, transform, screen, green )
edges = []
polygons = []
clear_screen(screen)
# centers
x1=0
y1=0
z1=0
x2=100
y2=200
z2=0
x3=200
y3=100
z3=0
# radii
r1=20
r2=40
r3=72

inc = 7
step = 200
step3d=30
k=2
tol = 0

def swirl(x1,y1,z1,r1,x2,y2,z2,r2,inc,step):
	if r1>r2:
		return swirl(x2,y2,z2,r2,x1,y1,z1,r1,inc,step)
		
	if r1==r2:
		return
	# WLOG r2>r1

	dx=x1-x2
	dy=y1-y2
	dz=z1-z2

	v1 = normalized([-dy,dx,0])
	axis = normalized([dx,dy,dz])
	v2 = cross(v1,axis)

	match = [v1[:]+[0],v2[:]+[0],axis[:]+[0],[0,0,0,1]]

	circle = []

	add_culled_circle(circle,0,0,0,r2,step)
	# add_circle(circle,0,0,0,r2,step)

	matrix_mult(match,circle)

	matrix_mult(make_translate( x2, y2, z2 ),circle)

	# center of homothety
	xc=x2+dx*r2/(r2-r1)
	yc=y2+dy*r2/(r2-r1)
	zc=z2+dz*r2/(r2-r1)

	cone = []
	n = int(dist(xc,yc,zc,x2,y2,z2)/inc)

	for i in range(1,n+1)[::-1]:
		toadd = copy.deepcopy(circle)
		matrix_mult(make_translate(-xc,-yc,-zc),toadd)
		matrix_mult(make_dilate(i*1./n),toadd)
		matrix_mult(make_translate(xc,yc,zc),toadd)
		cone = cone + toadd[:]

	return [cone,[xc,yc,zc], len(circle),[x2,y2,z2]]

add_sphere(polygons,x1,y1,z1,r1,int(k*r1))
add_sphere(polygons,x2,y2,z2,r2,int(k*r2))
add_sphere(polygons,x3,y3,z3,r3,int(k*r3))

transform = new_matrix()
ident(transform)
matrix_mult(make_rotZ(math.pi/6),transform)
matrix_mult(make_rotX(-math.pi/4),transform)
# matrix_mult(make_rotY(20),transform)
matrix_mult(make_dilate(1.2),transform)
matrix_mult(make_translate(240,220,0),transform)
matrix_mult(transform,polygons)

draw_polygons(polygons,screen,sphere_color)

centers=[]
circlelengths=[]
swirllengths=[0]
spherecenters=[]
# print(99)
out = swirl(x1,y1,z1,r1,x2,y2,z2,r2,inc,step)
edges = edges + out[0]
centers = centers + [out[1]+[1]]
circlelengths = circlelengths + [out[2]]
swirllengths = swirllengths + [len(edges)]
spherecenters = spherecenters + [out[3]+[1]]

out = swirl(x2,y2,z2,r2,x3,y3,z3,r3,inc,step)
edges = edges + out[0]
centers = centers + [out[1]+[1]]
circlelengths = circlelengths + [out[2]]
swirllengths = swirllengths + [len(edges)]
spherecenters = spherecenters + [out[3]+[1]]

out = swirl(x3,y3,z3,r3,x1,y1,z1,r1,inc,step)
edges = edges + out[0]
centers = centers + [out[1]+[1]]
circlelengths = circlelengths + [out[2]]
swirllengths = swirllengths + [len(edges)]
spherecenters = spherecenters + [out[3]+[1]]

matrix_mult(transform,edges)
draw_culled_circles(edges,screen,circle_color)
# draw_lines(edges,screen,blue)


resultE = []
resultP = []
for i in range(3):
	x1,y1,z1,x2,y2,z2=centers[i][0],centers[i][1],centers[i][2],centers[(i+1)%3][0],centers[(i+1)%3][1],centers[(i+1)%3][2]
	add_sphere(resultP,x1,y1,z1,2.5,step3d)
	add_edge(resultE,x1-2,y1,z1,x1+2,y1,z1)
	add_edge(resultE,x1,y1-2,z1,x1,y1+2,z1)
	add_edge(resultE,x1,y1,z1-2,x1,y1,z1+2)
	add_edge(resultE,x1,y1,z1,x2,y2,z2)
matrix_mult(transform,resultE)
matrix_mult(transform,resultP)


#find tangency points

matrix_mult(transform,centers)
matrix_mult(transform,spherecenters)

tangents = []
for i in range(3):
	minval = 1
	bestindex = -1
	currentindex = swirllengths[i]
	while currentindex < swirllengths[i]+circlelengths[i]-2:
		v = edges[currentindex+2][:]
		v = normalized(v[:3])
		currentval = abs(v[2])
		if currentval < minval:
			minval = currentval
			bestindex = currentindex
		currentindex +=3
	x1,y1,z1=edges[bestindex][0],edges[bestindex][1],edges[bestindex][2]
	x2,y2,z2=2*spherecenters[i][0]-x1,2*spherecenters[i][1]-y1,2*spherecenters[i][2]-z1
	add_edge(tangents,centers[i][0],centers[i][1],centers[i][2],x1,y1,z1)
	add_edge(tangents,centers[i][0],centers[i][1],centers[i][2],x2,y2,z2)

draw_lines(tangents,screen,tangent_color)

draw_lines(resultE,screen,line_color)
draw_polygons(resultP,screen,line_color)

save_extension(screen, "monge.png")


