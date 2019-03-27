from display import *
from matrix import *

import copy

def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons,x0,y0,z0)
    add_point(polygons,x1,y1,z1)
    add_point(polygons,x2,y2,z2)

def draw_polygons( matrix, screen, color ):
    if len(matrix) < 3:
        print 'Need at least 3 points to draw'
        return

    point = 0
    while point < len(matrix) - 2:
    	x0=int(matrix[point][0])
    	x1=int(matrix[point+1][0])
    	x2=int(matrix[point+2][0])
    	y0=int(matrix[point][1])
    	y1=int(matrix[point+1][1])
    	y2=int(matrix[point+2][1])
    	if ((x0-x1)*(y0-y2)-(x0-x2)*(y0-y1)<0):
    		point+= 3
    		continue
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+2][0]),
                   int(matrix[point+2][1]),
                   screen, color) 
        draw_line( int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   int(matrix[point+2][0]),
                   int(matrix[point+2][1]),
                   screen, color) 
        point+= 3

def add_quadrilateral( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3):
	add_polygon(polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2)
	add_polygon(polygons, x0, y0, z0, x2, y2, z2, x3, y3, z3)

def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    add_quadrilateral(polygons, x,y,z, x,y,z1, x,y1,z1, x,y1,z)
    add_quadrilateral(polygons, x,y,z, x,y1,z, x1,y1,z, x1,y,z)
    add_quadrilateral(polygons, x,y,z, x1,y,z, x1,y,z1, x,y,z1)
    
    x,y,z,x1,y1,z1=x1,y1,z1,x,y,z

    add_quadrilateral(polygons, x,y,z, x,y1,z, x,y1,z1, x,y,z1)
    add_quadrilateral(polygons, x,y,z, x1,y,z, x1,y1,z, x,y1,z)
    add_quadrilateral(polygons, x,y,z, x,y,z1, x1,y,z1, x1,y,z)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    n=int(step)
    m=int(n/2)
    for i in range(n):
    	for j in range(m-1):
    		ind0=((m+1)*i+j+1) % len(points)
    		ind1=((m+1)*(i+1)+j+2) % len(points)
    		ind2=((m+1)*(i+1)+j+1) % len(points)
    		ind3=((m+1)*i+j) % len(points)
    		# print(ind0,ind1,ind2,ind3,len(points))
    		add_quadrilateral(polygons, points[ind0][0], points[ind0][1], points[ind0][2]
    								, points[ind1][0], points[ind1][1], points[ind1][2]
    								, points[ind2][0], points[ind2][1], points[ind2][2]
    								, points[ind3][0], points[ind3][1], points[ind3][2])
    

def generate_sphere( cx, cy, cz, r, step ):
    n=int(step)
    semicircle=new_matrix(4,0)
    m=int(n/2.)
    for i in range(m+1):
    	x = cx + r * math.cos(math.pi*i/m)
    	y = cy + r * math.sin(math.pi*i/m)
    	z = cz
    	add_point(semicircle,x,y,z)
    sphere=new_matrix(4,0)
    rot = make_rotX(2*math.pi/n)
    for i in range(n):
    	sphere = sphere + copy.deepcopy(semicircle)
    	matrix_mult(rot,semicircle)
    return sphere

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    n=int(step)
    for i in range(n):
    	for j in range(n):
    		ind0=((n)*i+j) % len(points)
    		ind1=((n)*i+((j+1) % n)) % len(points)
    		ind2=((n)*(i+1)+((j+1) % n)) % len(points)
    		ind3=((n)*(i+1)+j) % len(points)
    		# print(ind0,ind1,ind2,ind3,len(points))
    		add_quadrilateral(polygons, points[ind0][0], points[ind0][1], points[ind0][2]
    								, points[ind1][0], points[ind1][1], points[ind1][2]
    								, points[ind2][0], points[ind2][1], points[ind2][2]
    								, points[ind3][0], points[ind3][1], points[ind3][2])

def generate_torus( cx, cy, cz, r0, r1, step ):
    n=int(step)
    circle=new_matrix(4,0)
    for i in range(n):
    	x = r1 + cx + r0 * math.cos(2*math.pi*i/n)
    	y = cy + r0 * math.sin(2*math.pi*i/n)
    	z = cz
    	add_point(circle,x,y,z)
    torus=new_matrix(4,0)
    rot = make_rotY(2*math.pi/n)
    for i in range(n):
    	torus = torus + copy.deepcopy(circle)
    	matrix_mult(rot,circle)
    return torus


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )

def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
