import matplotlib.pyplot as plt
import pandas as pd
import pickle
from itertools import product


def one_square_cutout(n, m, y, z=0):
    pt1 = [[0 + 20 * n, 0 + 20 * m, z], 
           [0 + 20 * n, 5 + 20 * m, z], 
           [10 + 20 * n, 5 + 20 * m, z], [10 + 20 * n, 15 + 20 * m, z], 
           [5 + 20 * n, 15 + 20 * m, z], [5 + 20 * n, 10 + 20 * m, z], 
           [0 + 20 * n, 10 + 20 * m, z], 
           [0 + 20 * n, 20 + 20 * m, z], [20 + 20 * n, 20 + 20 * m, z], 
           [20 + 20 * n, 0 + 20 * m, z]]
    df1 = pd.DataFrame(pt1, columns=['x0', 'y0', 'z0'])
    df1['x1'], df1['y1'], df1['z1'] = 0, 0, 0
    df1.loc[:, ('x1', 'y1', 'z1')] = pt1[1:] + pt1[:1]
    df1['depth'], df1['name'] = 1, n * 3 + 0 + m * y * 3
    df1['nx'], df1['ny'], df1['nz'] = 0, 0, 1
    return df1

def one_square(n, m, y, z=0):
    pt1 = [[0 + 20 * n, 0 + 20 * m, z], 
           [0 + 20 * n, 20 + 20 * m, z], 
           [20 + 20 * n, 20 + 20 * m, z], 
           [20 + 20 * n, 0 + 20 * m, z]]
    df1 = pd.DataFrame(pt1, columns=['x0', 'y0', 'z0'])
    df1['x1'], df1['y1'], df1['z1'] = 0, 0, 0
    df1.loc[:, ('x1', 'y1', 'z1')] = pt1[1:] + pt1[:1]
    df1['depth'], df1['name'] = 1, n * 3 + 0 + m * y * 3
    df1['nx'], df1['ny'], df1['nz'] = 0, 0, 1
    return df1

def vertical_y(n, m, y):
    pt1 = [[10 + 20 * n, 10 + 20 * m, 0], 
           [10 + 20 * n, 30 + 20 * m, 0], 
           [10 + 20 * n, 30 + 20 * m, 20], 
           [10 + 20 * n, 10 + 20 * m, 20]]
    df1 = pd.DataFrame(pt1, columns=['x0', 'y0', 'z0'])
    df1['x1'], df1['y1'], df1['z1'] = 0, 0, 0
    df1.loc[:, ('x1', 'y1', 'z1')] = pt1[1:] + pt1[:1]
    df1['depth'], df1['name'] = 1, n * 3 + 1 + m * y * 3
    df1['nx'], df1['ny'], df1['nz'] = -1, 0, 0
    return df1

def vertical_x(n, m, y):
    pt1 = [[-5 + 20 * n, 10 + 20 * m, 0], 
           [15 + 20 * n, 10 + 20 * m, 0], 
           [15 + 20 * n, 10 + 20 * m, 20], 
           [-5 + 20 * n, 10 + 20 * m, 20]]
    df1 = pd.DataFrame(pt1, columns=['x0', 'y0', 'z0'])
    df1['x1'], df1['y1'], df1['z1'] = 0, 0, 0
    df1.loc[:, ('x1', 'y1', 'z1')] = pt1[1:] + pt1[:1]
    df1['depth'], df1['name'] = 1, n * 3 + 2 + m * y * 3
    df1['nx'], df1['ny'], df1['nz'] = 0, 1, 0
    return df1

def create_dummy_parts(simple=True, x=2, y=2):
    parts = []
    if simple:
        parts += [one_square(i, j, y) for i, j in product(range(x), range(y))]
    else:
        parts += [one_square_cutout(i, j, y) for i, j in product(range(x), range(y))]
    parts += [vertical_y(i, j, y) for i, j in product(range(x), range(y))]
    parts += [vertical_x(i, j, y) for i, j in product(range(x), range(y))]
    df = pd.concat(parts, sort=False).reset_index(drop=True)
    return df

def save_df(df, path):
    with open(path, 'wb') as f:
        pickle.dump(df, f)

def load_df(path):
    with open(path, 'rb') as f:
        df = pickle.load(f)
    return df

def plot(df):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    lwr = min([df['x0'].min(), df['y0'].min(), df['z0'].min()])
    upr = max([df['x0'].max(), df['y0'].max(), df['z0'].max()])
    ax.set_xlim3d(lwr, upr)
    ax.set_ylim3d(lwr, upr)
    ax.set_zlim3d(lwr, upr)

    for i, g in df.groupby('name'):
        g = g.append(g.iloc[0])
        x, y, z = g['x0'], g['y0'], g['z0']
        ax.plot(x, y, z, label=i)

    ax.legend()
    plt.show()
