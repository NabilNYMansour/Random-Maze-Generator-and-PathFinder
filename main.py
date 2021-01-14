from PIL import Image, ImageDraw
import random

size_x = 101
size_y = size_x

img = Image.new("RGB", (size_x, size_y), "white")
draw = ImageDraw.Draw(img)

vertices = []
edges = []
for i in range(size_x):
    draw.point((i, 0), "black")
    draw.point((i, size_x - 1), "black")
    if i % 2 == 1:
        draw.point((i, 0), "green")
        draw.point((i, size_x - 1), "green")
        edges.append((i, 0))
        edges.append((i, size_x - 1))
    for j in range(size_y):
        if j % 2 == 1:
            edges.append((0, j))
            edges.append((size_y - 1, j))
        if i % 2 == 0:
            draw.point((i, j), "black")
        if j % 2 == 0:
            draw.point((i, j), "black")
        elif i % 2 == 1 and j % 2 == 1:
            vertices.append((i, j))

graph = []
for currentVertex in vertices:
    newRow = []
    for compareVertex in vertices:
        if compareVertex != currentVertex:
            if compareVertex[0] == currentVertex[0] and abs(compareVertex[1] - currentVertex[1]) == 2:
                if compareVertex[1] > currentVertex[1]:
                    newRow.append((currentVertex[0], currentVertex[1]+1))
                    edges.append((currentVertex[0], currentVertex[1]+1))
                else:
                    newRow.append((currentVertex[0], currentVertex[1]-1))
                    edges.append((currentVertex[0], currentVertex[1]-1))
            elif compareVertex[1] == currentVertex[1] and abs(compareVertex[0] - currentVertex[0]) == 2:
                if compareVertex[0] > currentVertex[0]:
                    newRow.append((currentVertex[0]+1, currentVertex[1]))
                    edges.append((currentVertex[0]+1, currentVertex[1]))
                else:
                    newRow.append((currentVertex[0]-1, currentVertex[1]))
                    edges.append((currentVertex[0]-1, currentVertex[1]))
            else:
                newRow.append(False)
        else:
            newRow.append(False)
    graph.append(newRow)


def DFS(graph, row, usedEdges, usedVertices):
    rowCopy = row.copy()
    random.shuffle(rowCopy)
    for edge in rowCopy:
        if edge not in usedEdges and row.index(edge) not in usedVertices and edge != False:
            draw.point(edge[::-1], "white")
            # img.save("img.png")
            usedEdges.append(edge)
            usedVertices.append(graph.index(row))
            DFS(graph, graph[row.index(edge)], usedEdges, usedVertices)
            break


def IsStuck(vertex, usedEdges):
    if (vertex[0]+1, vertex[1]) in usedEdges:
        if (vertex[0]-1, vertex[1]) in usedEdges:
            if (vertex[0], vertex[1]+1) in usedEdges:
                if (vertex[0], vertex[1]-1) in usedEdges:
                    return True
    return False



def Demolish(RIGHT, LEFT, UP, DOWN, vertex, usedEdges, usedVertices, draw):
    toReturn = False

    if vertex+1 in usedVertices and RIGHT:
        draw.point(
            (vertices[vertex][0], vertices[vertex][1]+1)[::-1], "white")
        usedEdges.append((vertices[vertex][0], vertices[vertex][1]+1))
        usedVertices.append(vertex)
        toReturn = True

    elif vertex-1 in usedVertices and LEFT:
        draw.point(
            (vertices[vertex][0], vertices[vertex][1]-1)[::-1], "white")
        usedEdges.append((vertices[vertex][0], vertices[vertex][1]-1))
        usedVertices.append(vertex)
        toReturn = True

    elif vertex-((size_x-1)//2) in usedVertices and UP:
        draw.point(
            (vertices[vertex][0]-1, vertices[vertex][1])[::-1], "white")
        usedEdges.append((vertices[vertex][0]-1, vertices[vertex][1]))
        usedVertices.append(vertex)
        toReturn = True

    elif vertex+((size_x-1)//2) in usedVertices and DOWN:
        draw.point(
            (vertices[vertex][0]+1, vertices[vertex][1])[::-1], "white")
        usedEdges.append((vertices[vertex][0]+1, vertices[vertex][1]))
        usedVertices.append(vertex)
        toReturn = True

    return toReturn

usedEdges = []
usedVertices = []
previousVertex = None
DFS(graph, graph[(((size_x-1)//2)**2//2)], usedEdges, usedVertices)

while len(usedVertices) + 1 != len(vertices):
    for vertex in range(len(vertices)):
        if vertex not in usedVertices and IsStuck(vertices[vertex], set(edges) - set(usedEdges)):

            row = (vertex)//((size_x-1)//2)
            column = vertex - row * ((size_x-1)//2)

            performDFS = False

            if row == 0 and column == 0:  # RIGHT and DOWN
                performDFS = Demolish(True, False, False, True, vertex,
                         usedEdges, usedVertices, draw)

            elif row == 0 and column == ((size_x-1)//2)-1:  # LEFT and DOWN
                performDFS = Demolish(False, True, False, True, vertex,
                         usedEdges, usedVertices, draw)


            elif row == ((size_x-1)//2)-1 and column == 0:  # RIGHT and UP
                performDFS = Demolish(True, False, True, False, vertex,
                         usedEdges, usedVertices, draw)

            elif row == ((size_x-1)//2)-1 and column == ((size_x-1)//2)-1:  # LEFT and UP
                performDFS = Demolish(False, True, True, False, vertex,
                         usedEdges, usedVertices, draw)

            elif row == 0:  # RIGHT, LEFT, and DOWN
                performDFS = Demolish(True, True, False, True, vertex,
                         usedEdges, usedVertices, draw)

            elif column == 0:  # UP, DOWN, and RIGHT
                performDFS = Demolish(True, False, True, True, vertex,
                         usedEdges, usedVertices, draw)

            elif row == ((size_x-1)//2)-1:  # RIGHT, LEFT, and UP
                performDFS = Demolish(True, True, True, False, vertex,
                         usedEdges, usedVertices, draw)

            elif column == ((size_x-1)//2)-1:  # UP, DOWN, and LEFT
                performDFS = Demolish(False, True, True, True, vertex,
                         usedEdges, usedVertices, draw)

            else:
                performDFS = Demolish(True, True, True, True, vertex,
                         usedEdges, usedVertices, draw)

            if performDFS:
                # img.save("img.png")
                DFS(graph, graph[vertex], usedEdges, usedVertices)

img = img.resize((size_x*10, size_y*10), Image.BOX)
img.save("img.png")