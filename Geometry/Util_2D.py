'''
2d vector (from a to b) = orthogonal components w.r.t origin
'''
def toVec(a, b):
    return (b[0]-a[0],b[1]-a[1])


'''
Scale of 2d vector v w.r.t. a factor s (this return v*s)
'''
def scale(v, s):
    return (v[0]*s, v[1]*s)


'''
Translation of 2d vector w.r.t. a point p
'''
def translate(p,v)
    return (p[0]+v[0], p[1]+v[1])


'''
Dot product of 2 vectors
'''
def dot(v,w)
    return p[0]*v[0] + p[1]*v[1]


'''
(norm)^2 of a vector live in toVec
(translated w.r.t origin)
'''
def norm_sq(v):
    return v[0]*v[0] + v[1]*v[1]


'''
Distance between 2 points
(norm of the vector between them)
'''
def dist(p1, p2):
    return math.sqrt(norm_sq((p1[0]-p2[0], p1[1]-p2[1])))


'''
Distance from point p to a line
(described by 2 points a, b on the line)
'''
def distToLine(p, a, b):
    # Formula: c = a + u * ab
    ap, ab = toVec(a, p), toVec(a, b)
    u = dot(ap, ab) / norm_sq(ab)
    c = translate(a, scale(ab, u))
    return dist(p, c)


'''
Check if three line segments of lengths a, b, c can form
a triangle
'''
def is_triangle(a, b, c):
    return((a+b > c) and (a+c > b) and (b+c > a))


'''
Perimeter of a triangle given the length of the segments
that compose it
'''
def perimeter(a, b, c):
    return a + b + c


'''
Area of a triangle (Heron’s formula) given the length of
the segments that compose it
'''
def area_heron(a, b, c):
    s = 0.5 * perimeter(a,b,c)
    return math.sqrt(s * (s-a) * (s-b) * (s-c))


'''
Given three points, returns
0 if they are collinear (no turn),
a positive number if they form a left (counter-clockwise) turn,
a negative number if they form a right (clockwise) turn.
'''
def turn(pt1, pt2, pt3):
    #Graham scan
    (x1, y1), (x2, y2), (x3, y3) = pt1, pt2, pt3
    return (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)


'''
Returns the perimeter of a polygon specified by a list P of
vertices given in some order (clockwise or counter-clockwise).
Works for both convex and concave polygons.
(First vertex = Last vertex)
'''
def perimeter(P):
    result = 0.0
    for i in range(len(P)-1):
    result += dist(P[i], P[i+1])
    return result


'''
Shoelace formula
Returns the area of a polygon specified by a list P of vertices
given in some order (either clockwise or counter-clockwise).
Works for both convex and concave polygons.
(First vertex = Last vertex)
'''
def area(P):
    result = 0.0
    for i in range(len(P)-1):
    (x1, y1) = P[i]
    (x2, y2) = P[i+1]
    result += (x1*y2 - x2*y1)
    return abs(result) / 2.0


'''
Returns angle aob in radians.
(Using formula with cos and vectorial product)
'''
def angle(a, o, b):
    oa = toVec(o,a)
    ob = toVec(o,b)
    return math.acos(dot(oa,ob) / math.sqrt(norm_sq(oa)*norm_sq(ob)))


'''
Returns True if point pt is inside polygon P, False otherwise
P is specified by a list of vertices in counter-clockwise order.
Works for both convex and concave polygons.
'''
def inPolygon(pt, P):
    if len(P) == 0:
        return False

    sum = 0.0

    #I'm going to sum all the angles with sign (turn-right <0, turn-left >0)
    #that the point created with couple of consecutives vertices of the poligon
    for i in range(len(P)-1):
        if turn(P[i], pt, P[i+1]) >=0:
            # left turn/ccw
            sum += angle(P[i], pt, P[i+1])
        else:
            # right turn/cw
            sum -= angle(P[i], pt, P[i+1])

    #if the sum is 2pi or -2pi, the point is in the poligon
    return math.fabs(math.fabs(sum) - 2*math.pi) < eps



'''
Given a set of points P, it return the Convex Hull of all
these points, that contains also some of them
it returns, in counter-clockwise order, the vertex of the
polygon that composes the convex-hull
'''
def andrew_hull(P):
    if len(P) < 2:
        return P #I cannot define a polygon that contains other points

    P = sorted(P) #sort P for increasing x (if they have the same x, increasing order of y)

    L = [] #the lower part of the convex hull
    U = [] #the upper part of the convex hall

    for pt in P:
        '''
        every time that I had a point, I need to verify if that
        forms a right turn with the previous 2 points in L
        if so, remove the element in the middle of the turn
        '''
        while len(L) > 1 and turn(L[-2], L[-1], pt) <= 0:
            L.pop()

        #add the new point aniway
        L.append(pt)

    #reversed(P) = reverse order w.r.t. sorted(P)
    for pt in reversed(P):
        '''
        every time that I had a point, I need to verify if that
        forms a right turn with the previous 2 points in L
        if so, remove the element in the middle of the turn
        '''
        while len(U) > 1 and turn(U[-2], U[-1], pt) <= 0:
            U.pop()

        U.append(pt)

    '''
    If a make together lower part and upper part, the last
    point and the first one are surely the same and they not have to be considered twice
    first(L)=last(U) and first(U)=last(L)
    so I remove only the last of L and the last of U
    '''
    return L[:-1] + U[:-1]
