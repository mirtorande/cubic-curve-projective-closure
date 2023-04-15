import streamlit as st
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import re

def generateFunctionPoints(coefficients, start=-10, stop=10, step=0.01, showTqdm=True):
    '''
    a*x^3 + b*x^2y + c*xy^2 + d*y^3 + e*x^2 + f*xy + g*y^2 + h*x + i*y + j*1 = 0
    '''
    points = []
    a, b, c, d, e, f, g, h, i ,j = coefficients
    for v in np.arange(start, stop, step):
        yCoefficients = [d, g + c*v, i + b*(v**2)+f*v, j + a*(v**3)+e*(v**2)+h*v]
        xCoefficients = [a, e + b*v, h + c*(v**2)+f*v, j + d*(v**3)+g*(v**2)+i*v]
        for y in cubicSolve(yCoefficients):
            points.append((v,y))
        for x in cubicSolve(xCoefficients):
            points.append((x,v))
    return np.array(points)

def cubicSolve(coefficients):
    '''
    Solves for ax^3+bx^2+cx+d=0
    '''
    polinomial = np.polynomial.Polynomial(coefficients[::-1])
    return [root.real for root in polinomial.roots() if abs(root.imag)<1e-5]

def projectPoints(points):
    proj_alpha = np.arctan2([y for _, y in points], [x for x, _ in points])
    proj_radius = [sqrt(x**2+y**2)/sqrt(x**2+y**2+1) for x, y in points]
    proj_x = np.cos(proj_alpha) * proj_radius
    proj_y = np.sin(proj_alpha) * proj_radius
    return np.array(list(zip(proj_x, proj_y)))

def generateProjectedPoints(functionCoefficients, step = 0.0025, start=-30, stop=30):
    points = generateFunctionPoints(functionCoefficients, start=start, stop=stop, step=step)
    return projectPoints(points)

def plotCurve(points, size=1, col='Blue', ax=None):
    return sns.scatterplot(x = points[:,0], y = points[:,1], legend=False,  marker='.', color=col, edgecolor=None, s=size, ax=ax)

def generateGridPoints(step=0.01, radius=1):
    points = []
    for x in np.arange(-radius, radius, step):
        for y in np.arange(-radius, radius, step):
            if x**2+y**2 > radius**2: continue
            points.append((x,y))
    return np.array(points)

def generateDeprojectedGrid(step = 0.01):
    points = generateGridPoints(step=step)
    proj_alpha = np.arctan2([y for _, y in points], [x for x, _ in points])
    deproj_radius = np.tan(np.arcsin([sqrt(x**2 + y**2) for x, y in points]))
    proj_x = np.cos(proj_alpha) * deproj_radius
    proj_y = np.sin(proj_alpha) * deproj_radius
    return np.array(list(zip(proj_x, proj_y)))

def testPoints(coefficients, points):
    testedPoints = []
    a, b, c, d, e, f, g, h, i ,j = coefficients
    for x, y in points:
        yCoefficients = [d, g + c*x, i + b*(x**2)+f*x, j + a*(x**3)+e*(x**2)+h*x]
        for y_coeff in cubicSolve(yCoefficients):
            if np.isclose(y_coeff, y, rtol=.01):
                testedPoints.append((x,y))
    for y, x in points:
        xCoefficients = [a, e + b*y, h + c*(y**2)+f*y, j + d*(y**3)+g*(y**2)+i*y]
        for x_coeff in cubicSolve(xCoefficients):
            if np.isclose(x_coeff, x, rtol=.01):
                testedPoints.append((x,y))
    return np.array(testedPoints)

def deprojectLine(step = 0.01, radius=1):
    points = np.arange(-radius, radius, step)
    deproj_points = np.tan(np.arcsin(points))
    return np.array(deproj_points)

def generateFunctionOnDeprojectedPoints(coefficients, radius=1, step=0.01, showTqdm=True):
    '''
    a*x^3 + b*x^2y + c*xy^2 + d*y^3 + e*x^2 + f*xy + g*y^2 + h*x + i*y + j*1 = 0
    '''
    points = deprojectLine(step=step, radius=radius)
    validPoints = []
    a, b, c, d, e, f, g, h, i ,j = coefficients
    for v in points:
        yCoefficients = [d, g + c*v, i + b*(v**2)+f*v, j + a*(v**3)+e*(v**2)+h*v]
        xCoefficients = [a, e + b*v, h + c*(v**2)+f*v, j + d*(v**3)+g*(v**2)+i*v]
        for y in cubicSolve(yCoefficients):
            validPoints.append((v,y))
        for x in cubicSolve(xCoefficients):
            validPoints.append((x,v))
    return np.array(validPoints)

def parseEquation(equation):
    coeffs = re.search(r'(?:(-?\d*\.*\d+)x\^3)?(?: \+ )?(?:(-?\d*\.*\d+)x\^2y)?(?: \+ )?(?:(-?\d*\.*\d+)xy\^2)?(?: \+ )?(?:(-?\d*\.*\d+)y\^3)?(?: \+ )?(?:(-?\d*\.*\d+)x\^2)?(?: \+ )?(?:(-?\d*\.*\d+)xy)?(?: \+ )?(?:(-?\d*\.*\d+)y\^2)?(?: \+ )?(?:(-?\d*\.*\d+)x)?(?: \+ )?(?:(-?\d*\.*\d+)y)?(?: \+ )?(?:(-?\d*\.*\d+))?', equation)
    return [0 if c is None else float(c) for c in coeffs.groups()]

def drawAffineAndProjected(equation, lineResolution = 0.0025, lineSize = 1.5, affineLim=5, showTdqm = False):
    coefficents = parseEquation(equation)

    fig, ax = plt.subplots(1,2)
    #Affine
    plotCurve(generateFunctionPoints(coefficents, step=lineResolution, showTqdm=showTdqm), size = lineSize, col = 'crimson', ax=ax[0])

    ax[0].set_aspect('equal')
    ax[0].set_xlim(-affineLim, affineLim)
    ax[0].set_ylim(-affineLim, affineLim)

    #Projected
    plotCurve(projectPoints(generateFunctionOnDeprojectedPoints(coefficents, step=lineResolution, showTqdm=showTdqm)), size = lineSize, col = 'crimson', ax=ax[1])
    circle = plt.Circle(xy=(0, 0), radius=1, color='gold', fill=False)
    ax[1].add_patch(circle)

    ax[1].set_aspect('equal')
    ax[1].set_xlim(-1.1, 1.1)
    ax[1].set_ylim(-1.1, 1.1)

    return plt


option = st.selectbox(
    'Che curva vuoi proiettare?',
    ('Curva Pene', 'Curva Culo', 'Curva Baseball'))

curves_dic = {'Curva Pene':'1x^2y + 1y^2 + -1', 'Curva Culo':'1x^3 + -1y^2', 'Curva Baseball':'1xy^2 + 1y^2 + -1x + 1y + 0'}

#st.write('You selected:', option)

with st.empty():
    lineSize = 0.25
    step = 200

    coefficents = parseEquation(curves_dic[option])

    source = generateFunctionPoints(coefficents, start=-5, stop=5, step = 0.05)
    source2 = projectPoints(generateFunctionOnDeprojectedPoints(coefficents, step = 0.0035))

    fig, ax = plt.subplots(1,2)
    ax[0].set_aspect('equal')
    ax[0].set_xlim(-5, 5)
    ax[0].set_ylim(-5, 5)
    circle = plt.Circle(xy=(0, 0), radius=1, color='gold', fill=False, zorder=2.0, linewidth=2)
    ax[1].add_patch(circle)

    ax[1].set_aspect('equal')
    ax[1].set_xlim(-1.1, 1.1)
    ax[1].set_ylim(-1.1, 1.1)
    fig.tight_layout(pad=2.0)

    for i in np.arange(start=0, stop=len(source2), step=step):
        points = source[i:i+step]
        proj_points = source2[i:i+step]

        ax[0].scatter(x=points[:,0], y=points[:,1], color='b', s=lineSize)
        ax[1].scatter(x=proj_points[:,0], y=proj_points[:,1], color='b', s=lineSize)

        st.pyplot(fig)
