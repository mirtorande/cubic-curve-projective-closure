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

def plotCurve(points, size=1, col='Blue', ax=None):
    return sns.scatterplot(x = points[:,0], y = points[:,1], legend=False,  marker='.', color=col, edgecolor=None, s=size, ax=ax)


def deprojectLine(step = 0.01, radius=1):
    points = np.arange(-radius, radius, step)
    deproj_points = np.tan(np.arcsin(points))
    return np.array(deproj_points + [0])

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


curves_topo = {
    'y = x^3':                          '1x^3 + -1y',
    'x^2y = 1':                         '1x^2y + -1',
    'y^2 = [(x-1)^2 (x-2)] / -x':       '1x^3 + 1xy^2 + -4x^2 + 5x + -2',
    'y^2 = x^2 (x-1)':                  '1x^3 + -1x^2 + -1y^2',
    'y^2 = x(x+1)(x-1)':                '1x^3 + -1y^2 + -1x',
    'y = 1 / (x^2-1)':                  '1x^2y + -1y + -1',
    'y^2 = [(x+1)^2 (x-2)] / x':        '1x^3 + -1xy^2 + -3x + -2',
    'y^2 = [(x-1)^2 (x-2)] / x':        '1x^3 + -1xy^2 + -4x^2 + 5x + -2',
    'y^2 = [(x-2)^2 (x-1)] / x':        '1x^3 + -1xy^2 + -5x^2 + 8x + -4',
    'y^2 = [(x-1)(x-2)(x-4)] / x':       '1x^3 + -1xy^2 + -7x^2 + 14x + -8',
    'x^2y - 1/4 x^2 + y^2 = 0':         '1x^2y + -.25x^2 + 1y^2',
    'x^2y + 1/4 x^2 + y^2  = 0':        '1x^2y + .25x^2 + 1y^2',
    'x^2y + 1/2 x^2 + 1/2 y^2 -2y = 0': '1x^2y + .5x^2 + .5y^2 + -2y',
    '4x^2y + 4y^2 + 3x^2 - 2x = 0':     '4x^2y + 3x^2 + 4y^2 + -2x',
    'y^2 = [(x+1)(x-1)(x-2)] / x':      '1x^3 + -1xy^2 + -2x^2 + -1x + 2',
}

curves_affine = {
    'x^3 + xy^2 + x^2 + Hx + Iy + J = 0  (H = -1, I = 2, J = -1/2)': '1x^3 + 1xy^2 + 1x^2 + -1x + 2y + -.5',
    'x^3 + xy^2 + y + Hx + J = 0': '1x^3 + 1xy^2 + .5x + 1y + -.5',
    'x^3 + xy^2 + x + J = 0': '1x^3 + 1xy^2 + 1x + 5',
    'x^3 + xy^2 + 1 = 0': '1x^3 + 1xy^2 + 1',
    'x^3 - xy^2 - x^2 + Hx + Iy + J = 0': '1x^3 + -1xy^2 + -1x^2 + 2x + -2y + 2',
    'x^3 - xy^2 + 1 = 0': '1x^3 + -1xy^2 + 1',
    'x^2y + y^2 - x + y + J = 0': '1x^2y + 1y^2 + -1x + 1y + 0',
    'x^2y + y^2 + y + J = 0': '1x^2y + 1y^2 + 1y + .25',
    'x^2y + y^2 - 1 = 0': '1x^2y + 1y^2 + -1',
    'x^2y - x + y + J = 0': '1x^2y + -1x + 1y + 3',
    'x^2y - x = 0': '1x^2y + -1x',
    'x^2y - x + 1 = 0': '1x^2y + -1x + 1',
    '$x^2y + y + 1 = 0$': '1x^2y + 1y + 1',
    'x^2y + 1 = 0': '1x^2y + 1',
    'x^3 - y^2 + x + J = 0': '1x^3 + -1y^2 + 1x + 2',
    'x^3 - y^2 - x + J = 0': '1x^3 + -1y^2 + -1x + .25',
    'x^3 - y^2 + 1 = 0': '1x^3 + -1y^2 + 1',
    'x^3 - y^2 = 0': '1x^3 + -1y^2',
    'x^3 - y = 0': '1x^3 + -1y',
    'x^3 - xy + 1 = 0': '1x^3 + -1xy + 1'
}

classification_dict = {'Classificazione affine': curves_affine, 'Classificazione topologica': curves_topo}

classification = st.selectbox(
    'Classificazione', classification_dict.keys()
)

curve = st.selectbox(
    'Curva',classification_dict[classification].keys()
)

affineLim = st.slider('Limite destro del grafico', 1, 20, 10)

with st.empty():
    lineSize = 0.25
    draw_batch_size = 200

    coefficents = parseEquation(classification_dict[classification][curve])

    points = generateFunctionPoints(coefficents, start=-affineLim, stop=affineLim, step = 0.005*affineLim)
    projected_points = projectPoints(generateFunctionOnDeprojectedPoints(coefficents, step = 0.001))

    fig, ax = plt.subplots(1,2)
    ax[0].set_aspect('equal')
    ax[0].set_xlim(-affineLim, affineLim)
    ax[0].set_ylim(-affineLim, affineLim)
    circle = plt.Circle(xy=(0, 0), radius=1, color='gold', fill=False, zorder=2.0, linewidth=2)
    ax[1].add_patch(circle)

    ax[1].set_aspect('equal')
    ax[1].set_xlim(-1.1, 1.1)
    ax[1].set_ylim(-1.1, 1.1)
    fig.tight_layout(pad=2.0)

    for i in range(0, len(points)+1, draw_batch_size):
        draw_points = points[i:i+draw_batch_size]

        ax[0].scatter(x=draw_points[:,0], y=draw_points[:,1], color='b', s=lineSize)

        st.pyplot(fig)

    for i in range(0, len(projected_points)+1, draw_batch_size*4):
        proj_points = projected_points[i:i+draw_batch_size*4]

        ax[1].scatter(x=proj_points[:,0], y=proj_points[:,1], color='b', s=lineSize)

        st.pyplot(fig)

