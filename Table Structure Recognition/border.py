
from Functions.borderFunc import extract_table,extractText,span
import lxml.etree as etree
import cv2

def border(table,image):
    image_np = image[table[1]-10:table[3]+10,table[0]-10:table[2]+10]
    imag = image_np.copy()
    final = extract_table(image_np,1)

    X = []
    Y = []
    for x1,y1,x2,y2,x3,y3,x4,y4 in final:
        if x1 not in X:
            X.append(x1)
        if x3 not in X:
            X.append(x3)
        if y1 not in Y:
            Y.append(y1)
        if y2 not in Y:
            Y.append(y2)

    X.sort()
    Y.sort()
    # print("X = ",X)
    # print("Y = ",Y)

    tableXML = etree.Element("table")
    Tcoords = etree.Element("Coords", points=str(table[0])+","+str(table[1])+" "+str(table[0])+","+str(table[3])+" "+str(table[2])+","+str(table[3])+" "+str(table[2])+","+str(table[1]))
    tableXML.append(Tcoords)
    for box in final:
      # cv2.rectangle(imag,(table[0]+box[0]-10,table[1]+box[1]-10),(table[0]+box[4]-10,table[1]+box[3]-10),(255,0,0),2)
      cellBox = extractText(imag[box[1]:box[3],box[0]:box[4]])
      if cellBox is None:
          continue
      cv2.rectangle(imag,(table[0]+cellBox[0]+box[0]-10,table[1]+cellBox[1]+box[1]-10),(table[0]+cellBox[2]+box[0]-10,table[1]+cellBox[3]+box[1]-10),(255,0,0),1)
      cell = etree.Element("cell")
      end_col,end_row,start_col,start_row = span(box,X,Y)
      cell.set("end-col",str(end_col))
      cell.set("end-row",str(end_row))
      cell.set("start-col",str(start_col))
      cell.set("start-row",str(start_row))

      # print(cellBox)
      one = str(cellBox[0]+table[0]+box[0]-10)+","+str(cellBox[1]+table[1]+box[1]-10)
      two = str(cellBox[0]+table[0]+box[0]-10)+","+str(cellBox[3]+table[1]+box[1]-10)
      three = str(cellBox[2]+table[0]+box[0]-10)+","+str(cellBox[3]+table[1]+box[1]-10)
      four = str(cellBox[2]+table[0]+box[0]-10)+","+str(cellBox[1]+table[1]+box[1]-10)
      # print(one)
      coords = etree.Element("Coords", points=one+" "+two+" "+three+" "+four)

      cell.append(coords)
      tableXML.append(cell)
    
    # groot.append(tableXML)
    # cv2_imshow(imag)
    return tableXML
    # cv2.imwrite('visual'+imgpath[1:],imag)