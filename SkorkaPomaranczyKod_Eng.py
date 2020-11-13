# -*- coding: utf-8 -*-
#Import required libraries:
import turtle
import random
import matplotlib.pyplot as plt
import math


#Functions:
def drawCircle(radius):
  drawingTool.up()
  drawingTool.right(90)
  drawingTool.forward(radius)
  drawingTool.left(90)
  drawingTool.down()
  drawingTool.circle(radius)
  drawingTool.up()
  drawingTool.left(90)
  drawingTool.forward(radius)
  drawingTool.right(90)   

class Point3D:
    def __init__(self, x=0, y=0, z=0):
      self.x = x
      self.y = y
      self.z = z
    
    def print(self):
        print("(x={0}, y={1}, z={2})".format(self.x, self.y, self.z))
    
    def getDistanceFromPoint(self, anotherPoint):
        return math.sqrt(math.pow((self.x - anotherPoint.x), 2) 
                         + math.pow((self.y - anotherPoint.y), 2) 
                         + math.pow((self.z - anotherPoint.z), 2))
    
    def drowDotWithTurtle(self, drawingTurtle, color):
        drawingTurtle.color(color)
        drawingTurtle.up()
        drawingTurtle.setposition(self.x, self.y)
        drawingTurtle.up()
        drawingTurtle.dot()
        drawingTurtle.up()
        drawingTurtle.color("black")
        
        
#Variables:
testOrangeRadius = 300
orangeRindRadiusPercent = 10
startingPoint = Point3D(0,0,0)
numOfSteps = 11000
notifyWithEvery = 500
ifDrawPoints = False

orangeRindRadiusFracture = orangeRindRadiusPercent/100
orangePulpRadiusFracture = 1 - orangeRindRadiusFracture

testOrangePulpRadius = (orangePulpRadiusFracture)*testOrangeRadius

pulpVolToRindVolRatio = math.pow(orangePulpRadiusFracture, 3) / (1 - math.pow(orangePulpRadiusFracture, 3))

#Main:

#Draw orange cross-section    
drawingTool = turtle.Turtle()
drawingTool.hideturtle()
drawingTool.up()
drawingTool.setposition(startingPoint.x, startingPoint.y)
drawingTool.speed(0)
drawCircle(testOrangeRadius)
drawCircle(testOrangePulpRadius)

#Print work data
print('Promien pomaranczy: ' + str(testOrangeRadius))
print('Promien miazszu, gdy skorka ma grubosc '+ str(orangeRindRadiusPercent) +'% promienia owocu: ' + str(testOrangePulpRadius))
print('Stosunek objetosci miazszu do objetosci skorki wylicozny ze wzoru: ' + str(pulpVolToRindVolRatio))

#Calculating approximates:
count_inOrangePulp = 0
count_inOrangeRind = 0

ratioApproximations = []

print("Rozpoczecie estymacji: ")
for i in range(numOfSteps):
    x = random.randrange(-testOrangeRadius, testOrangeRadius)
    y = random.randrange(-testOrangeRadius, testOrangeRadius)
    z = random.randrange(-testOrangeRadius, testOrangeRadius)
    
    randomPoint = Point3D(x,y,z)
    distanceFromStart = randomPoint.getDistanceFromPoint(startingPoint)
    if (distanceFromStart <= testOrangePulpRadius):
        if(ifDrawPoints):
            randomPoint.drowDotWithTurtle(drawingTool, "orange")
        count_inOrangePulp = count_inOrangePulp+1
    elif(distanceFromStart <= testOrangeRadius):
        if(ifDrawPoints):
            randomPoint.drowDotWithTurtle(drawingTool, "black")
        count_inOrangeRind = count_inOrangeRind+1
     
    #print(str(count_inOrangePulp) + " " + str(count_inOrangeRind))
    if(count_inOrangePulp == 0 or count_inOrangeRind == 0):
        ratioApproximationForThisStep = 0 
    else:
        ratioApproximationForThisStep = count_inOrangePulp/count_inOrangeRind
    
    ratioApproximations.append(ratioApproximationForThisStep)
    
    if(i%notifyWithEvery == 0):
        print("   Krok i={0}, wartosc estymacji: {1}".format(i,ratioApproximationForThisStep))

print("Koniec estymacji.")

errorsOfApproximations = [abs(pulpVolToRindVolRatio - ratio) for ratio in ratioApproximations]

# Print results
print('Koncowa wyestymowana wartosc stosunku objetosci miazszu do objetosci skorki: ' + str(ratioApproximations[-1]))

#Ploting data
plt.axhline(y=pulpVolToRindVolRatio, color='g', linestyle='-')
plt.plot(ratioApproximations)
plt.xlabel("Ilosc iteracji")
plt.ylabel("Wartosc proporcji Vm/Vs")
plt.show()

plt.axhline(y=0.0, color='g', linestyle='-')
plt.plot(errorsOfApproximations)
plt.xlabel("Ilosc iteracji")
plt.ylabel("Odchylenie od oczekiwanej wartoci")
plt.show()

#end Main
turtle.done()
try:
    turtle.bye()   
except turtle.Terminator:
    pass



