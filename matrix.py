"""
A matrix will be an N sized list of 4 element lists.
Each individual list will represent an [x, y, z, 1] point.
For multiplication purposes, consider the lists like so:
x0  x1      xn
y0  y1      yn
z0  z1  ... zn
1  1        1
"""
import math

def dist(x1,y1,z1,x2,y2,z2):
	return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**0.5

def crossC(x1,y1,z1,x2,y2,z2):
	return [y1*z2-y2*z1,z1*x2-z2*x1,x1*y2-x2*y1]

def cross(v1,v2):
	return crossC(v1[0],v1[1],v1[2],v2[0],v2[1],v2[2])

def normalized(v):
	if len(v)!=3:
		print("bad vector length")
		return
	else:
		mag = dist(v[0],v[1],v[2],0,0,0)
		if mag==0:
			return v
		else:
			return [w/mag for w in v]


def make_bezier():
    return [
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0]
    ]


def make_hermite():
    return [
        [2, -3, 0, 1],
        [-2, 3, 0, 0],
        [1, -2, 1, 0],
        [1, -1, 0, 0]
    ]

def generate_curve_coefs( p0, p1, p2, p3, t ):
    coefs = [[p0, p1, p2, p3]]
    if t == 'hermite':
        curve = make_hermite()
    else:
        curve = make_bezier()

    matrix_mult(curve, coefs)
    return coefs


def make_translate( x, y, z ):
    t = new_matrix()
    ident(t)
    t[3][0] = x
    t[3][1] = y
    t[3][2] = z
    return t

def make_scale( x, y, z ):
    t = new_matrix()
    ident(t)
    t[0][0] = x
    t[1][1] = y
    t[2][2] = z
    return t

def make_dilate( r ):
    return make_scale(r,r,r)

def make_rotX( theta ):
    t = new_matrix()
    ident(t)
    t[1][1] = math.cos(theta)
    t[2][1] = -1 * math.sin(theta)
    t[1][2] = math.sin(theta)
    t[2][2] = math.cos(theta)
    return t

def make_rotY( theta ):
    t = new_matrix()
    ident(t)
    t[0][0] = math.cos(theta)
    t[0][2] = -1 * math.sin(theta)
    t[2][0] = math.sin(theta)
    t[2][2] = math.cos(theta)
    return t

def make_rotZ( theta ):
    t = new_matrix()
    ident(t)
    t[0][0] = math.cos(theta)
    t[1][0] = -1 * math.sin(theta)
    t[0][1] = math.sin(theta)
    t[1][1] = math.cos(theta)
    return t

#print the matrix such that it looks like
#the template in the top comment
def print_matrix( matrix ):
    s = ''
    for r in range( len( matrix[0] ) ):
        for c in range( len(matrix) ):
            s+= str(matrix[c][r]) + ' '
        s+= '\n'
    print s
    
#turn the paramter matrix into an identity matrix
#you may assume matrix is square
def ident( matrix ):
    for r in range( len( matrix[0] ) ):
        for c in range( len(matrix) ):
            if r == c:
                matrix[c][r] = 1
            else:
                matrix[c][r] = 0

#multiply m1 by m2, modifying m2 to be the product
#m1 * m2 -> m2
def matrix_mult( m1, m2 ):

    point = 0
    for row in m2:
        #get a copy of the next point
        tmp = row[:]

        for r in range(4):
            m2[point][r] = (m1[0][r] * tmp[0] +
                            m1[1][r] * tmp[1] +
                            m1[2][r] * tmp[2] +
                            m1[3][r] * tmp[3])
        point+= 1


def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m
