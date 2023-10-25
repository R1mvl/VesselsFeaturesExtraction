import plotly.graph_objects as go

color = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'lime', 'teal', 'navy']
fig = go.Figure()
fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))

def showGraphExtremities(extremities):

    exx = []
    exy = []
    exz = []
    for i in range(0, len(extremities)):
        exx.append(extremities[i][0])
        exy.append(extremities[i][1])
        exz.append(extremities[i][2])
    fig.add_trace(go.Scatter3d(x=exx, y=exy, z=exz, mode='markers', marker=dict(color='green', size=10)))

def showGraphIntersection(intersection):

    itx = []
    ity = []
    itz = []
    for i in range(0, len(intersection)):
        itx.append(intersection[i][0])
        ity.append(intersection[i][1])
        itz.append(intersection[i][2])
    fig.add_trace(go.Scatter3d(x=itx, y=ity, z=itz, mode='markers', marker=dict(color='blue', size=10)))

def showGraphCenterline(graph):

    for i in range(0, len(graph)):
        for j in range(0, len(graph[i][1])):
            # add the label of the edge
            fig.add_trace(go.Scatter3d(x=[graph[i][0][0], graph[graph[i][1][j]][0][0]], y=[graph[i][0][1], graph[graph[i][1][j]][0][1]], z=[graph[i][0][2], graph[graph[i][1][j]][0][2]], mode='lines', line=dict(color=color[graph[i][2] % len(color)], width=6), name='edge' + str(graph[i][2])))
    

def showGraphLine(graph):
    for i in range(0, len(graph)):
        for j in graph[i][1]:
            fig.add_trace(go.Scatter3d(x=[graph[i][0][0], graph[j][0][0]], y=[graph[i][0][1], graph[j][0][1]], z=[graph[i][0][2], graph[j][0][2]], mode='lines', line=dict(color='black', width=10, dash='dash')))

def showMatrix(matrix, point_assignment, points = None):
    x = []
    y = []
    z = []
    c = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            for k in range(matrix.shape[2]):
                if matrix[i,j,k] > 0:
                    x.append(i)
                    y.append(j)
                    z.append(k)
                    if points == None or point_assignment[i,j,k] in points:
                        c.append(point_assignment[i,j,k])

    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=4, color=c, opacity=0.8)))

def show():
    fig.show()