from PIL import Image, ImageDraw
import random

size_x = 7
size_y = size_x

img = Image.new("RGB", (size_x, size_y), "white")
draw = ImageDraw.Draw(img)

vertices = []
flag = True
for i in range(size_x):
    draw.point((i, 0), "black")
    draw.point((i, size_x - 1), "black")
    for j in range(size_y):
        draw.point((0, j), "black")
        draw.point((size_y - 1, j), "black")
        if i % 2 == 0 and j % 2 == 0:
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
                else:
                    newRow.append((currentVertex[0], currentVertex[1]-1))
            elif compareVertex[1] == currentVertex[1] and abs(compareVertex[0] - currentVertex[0]) == 2:
                if compareVertex[0] > currentVertex[0]:
                    newRow.append((currentVertex[0]+1, currentVertex[1]))
                else:
                    newRow.append((currentVertex[0]-1, currentVertex[1]))
            else:
                newRow.append(False)
        else:
            newRow.append(False)
    graph.append(newRow)

    # print(currentVertex, ": ", newRow)

for row in graph:
    for edge in row:
        if edge != False:
            draw.point(edge, "red")



img = img.resize((size_x*10, size_y*10), Image.BOX)
img.save("img.png")
