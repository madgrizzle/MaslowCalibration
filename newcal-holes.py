import math
import random

workspaceHeight = 1219.2
workspaceWidth = 2438.4
gearTeeth = 10
chainPitch = 6.35

aH1x = (workspaceWidth/2.0-254.0)*-1.0
aH1y = (workspaceHeight/2.0-254.0)*-1.0
aH2x = aH1x
aH2y = aH1y*-1.0
aH3x = aH1x*-1.0
aH3y = aH2y
aH4x = aH3x
aH4y = aH1y

#default parameters used during calibration cut
motorSpacing = 3602.6
motorYoffsetEst = 468.4
rotationRadiusEst = 139.1
chainSagCorrectionEst = 35.0
chainOverSprocket = 1
leftChainTolerance = 1.0+0.347900203615/100.0
rightChainTolerance =1.0+0.360479822602/100.0

#default cut parameters
dH0H1 = 1028.6216
dH0H2 = 1028.6216
dH0H3 = 1028.6216
dH0H4 = 1028.6216
dH1H2 = 711.2
dH1H4 = 1930.4
dH2H3 = 1930.4
dH3H4 = 711.2
dH0M5 = 355.6
dH2M5 = 965.2

#optimization parameters
acceptableTolerance = .05
numberOfIterations = 10000000
motorYcoordCorrectionScale = 0.1
chainSagCorrectionCorrectionScale = 0.1
motorXcoordCorrectionScale = 0.001
rotationRadiusCorrectionScale = 0.001
chainCompensationCorrectionScale = 0.003
desiredRotationalRadius = rotationRadiusEst #

#optional adjustments
adjustmotorYcoord = True
adjustChainSag = True
adjustMotorSpacing = True
adjustRotationalRadius = True
adjustChainCompensation = True

# Gather current machine parameters
motorXcoord = motorSpacing/2
motorYcoordEst = (workspaceHeight/2) + motorYoffsetEst
sprocketRadius = (gearTeeth*chainPitch / 2.0 / 3.14159 + chainPitch/math.sin(3.14159 / gearTeeth)/2.0)/2.0

#Calculate x,y coordinates for each hole
H0x = 0
H0y = 0
M5x = 0
M5y = dH0M5
H2y = (dH0M5*dH0M5+dH0H2*dH0H2-dH2M5*dH2M5)/(2*dH0M5)
H2x = math.sqrt( (dH0M5+dH0H2+dH2M5) * (dH0M5+dH0H2-dH2M5) * (dH0M5-dH0H2+dH2M5) * (-dH0M5+dH0H2+dH2M5) )/(2*dH0M5)*-1.0
#print "H2x:"+str(H2x)+", H2y:"+str(H2y)

H3y = (dH0M5*dH0M5+dH0H3*dH0H3-(dH2H3-dH2M5)*(dH2H3-dH2M5))/(2*dH0M5)
H3x = math.sqrt( (dH0M5+dH0H3+(dH2H3-dH2M5)) * (dH0M5+dH0H3-(dH2H3-dH2M5)) * (dH0M5-dH0H3+(dH2H3-dH2M5)) * (-dH0M5+dH0H3+(dH2H3-dH2M5)) )/(2*dH0M5)
#print "H3x:"+str(H3x)+", H3y:"+str(H3y)

theta = math.atan2(H3y,H3x)
#print "Theta:"+str(theta)
rH4x = (dH0H3*dH0H3-dH3H4*dH3H4+dH0H4*dH0H4)/(2*dH0H3)
rH4y = math.sqrt( (dH0H3+dH3H4+dH0H4) * (dH0H3+dH3H4-dH0H4) *(dH0H3-dH3H4+dH0H4) * (-dH0H3+dH3H4+dH0H4) )/(2*dH0H3)
#print "rH4x:"+str(rH4x)+", rH4y:"+str(rH4y)

H4x = (rH4x*math.cos(-theta))-(rH4y*math.sin(-theta))
H4y = ((rH4x*math.sin(-theta))+(rH4y*math.cos(-theta)))*-1.0
#print "H4x:"+str(H4x)+", H4y:"+str(H4y)
# Calculate the actual chain lengths for each cut location

theta = math.atan2(H2y,H2x*-1.0)
#print "Theta:"+str(theta)
rH1x = (dH0H2*dH0H2-dH1H2*dH1H2+dH0H1*dH0H1)/(2*dH0H2)
rH1y = math.sqrt( (dH0H2+dH1H2+dH0H1) * (dH0H2+dH1H2-dH0H1) *(dH0H2-dH1H2+dH0H1) * (-dH0H2+dH1H2+dH0H1) )/(2*dH0H2)
#print "rH1x:"+str(rH1x)+", rH1y:"+str(rH1y)

H1x = ((rH1x*math.cos(-theta))-(rH1y*math.sin(-theta)))*-1.0
H1y = ((rH1x*math.sin(-theta))+(rH1y*math.cos(-theta)))*-1.0
print "H1x:"+str(H1x)+", H1y:"+str(H1y)
print "H2x:"+str(H2x)+", H2y:"+str(H2y)
print "H3x:"+str(H3x)+", H3y:"+str(H3y)
print "H4x:"+str(H4x)+", H4y:"+str(H4y)

# Calculate the actual chain lengths for each hole location based upon inputted model
x=raw_input("")

MotorDistanceHole1 = math.sqrt(math.pow(motorXcoord + aH1x,2) + math.pow(motorYcoordEst + aH1y ,2))
MotorDistanceHole2 = math.sqrt(math.pow(motorXcoord + aH2x,2) + math.pow(motorYcoordEst + aH2y ,2))
MotorDistanceHole3 = math.sqrt(math.pow(motorXcoord + aH3x,2) + math.pow(motorYcoordEst + aH3y ,2))
MotorDistanceHole4 = math.sqrt(math.pow(motorXcoord + aH4x,2) + math.pow(motorYcoordEst + aH4y ,2))

#Calculate the chain angles from horizontal, based on if the chain connects to the sled from the top or bottom of the sprocket
if chainOverSprocket == 1:
	ChainAngleHole1 = math.asin((motorYcoordEst + aH1y) / MotorDistanceHole1) + math.asin(sprocketRadius/MotorDistanceHole1)
	ChainAngleHole2 = math.asin((motorYcoordEst + aH2y) / MotorDistanceHole2) + math.asin(sprocketRadius/MotorDistanceHole2)
	ChainAngleHole3 = math.asin((motorYcoordEst + aH3y) / MotorDistanceHole3) + math.asin(sprocketRadius/MotorDistanceHole3)
	ChainAngleHole4 = math.asin((motorYcoordEst + aH4y) / MotorDistanceHole4) + math.asin(sprocketRadius/MotorDistanceHole4)

	ChainAroundSprocketHole1 = sprocketRadius * ChainAngleHole1
	ChainAroundSprocketHole2 = sprocketRadius * ChainAngleHole2
	ChainAroundSprocketHole3 = sprocketRadius * ChainAngleHole3
	ChainAroundSprocketHole4 = sprocketRadius * ChainAngleHole4
else:
	ChainAngleHole1 = math.asin((motorYcoordEst + aH1y) / MotorDistanceHole1) - math.asin(sprocketRadius/MotorDistanceHole1)
	ChainAngleHole2 = math.asin((motorYcoordEst + aH2y) / MotorDistanceHole2) - math.asin(sprocketRadius/MotorDistanceHole2)
	ChainAngleHole3 = math.asin((motorYcoordEst + aH3y) / MotorDistanceHole3) - math.asin(sprocketRadius/MotorDistanceHole3)
	ChainAngleHole4 = math.asin((motorYcoordEst + aH4y) / MotorDistanceHole4) - math.asin(sprocketRadius/MotorDistanceHole4)

	ChainAroundSprocketHole1 = sprocketRadius * (3.14159 - ChainAngleHole1)
	ChainAroundSprocketHole2 = sprocketRadius * (3.14159 - ChainAngleHole2)
	ChainAroundSprocketHole3 = sprocketRadius * (3.14159 - ChainAngleHole3)
	ChainAroundSprocketHole4 = sprocketRadius * (3.14159 - ChainAngleHole4)

#Calculate the straight chain length from the sprocket to the bit
ChainStraightHole1 = math.sqrt(math.pow(MotorDistanceHole1,2) - math.pow(sprocketRadius,2))
ChainStraightHole2 = math.sqrt(math.pow(MotorDistanceHole2,2) - math.pow(sprocketRadius,2))
ChainStraightHole3 = math.sqrt(math.pow(MotorDistanceHole3,2) - math.pow(sprocketRadius,2))
ChainStraightHole4 = math.sqrt(math.pow(MotorDistanceHole4,2) - math.pow(sprocketRadius,2))

#Correct the straight chain lengths to account for chain sag
ChainSag1 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole1),2) * math.pow(ChainStraightHole1,2) * math.pow((math.tan(ChainAngleHole2) * math.cos(ChainAngleHole1)) + math.sin(ChainAngleHole1),2)))
ChainSag2 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole2),2) * math.pow(ChainStraightHole2,2) * math.pow((math.tan(ChainAngleHole1) * math.cos(ChainAngleHole2)) + math.sin(ChainAngleHole2),2)))
ChainSag3 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole3),2) * math.pow(ChainStraightHole3,2) * math.pow((math.tan(ChainAngleHole4) * math.cos(ChainAngleHole3)) + math.sin(ChainAngleHole3),2)))
ChainSag4 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole4),2) * math.pow(ChainStraightHole4,2) * math.pow((math.tan(ChainAngleHole3) * math.cos(ChainAngleHole4)) + math.sin(ChainAngleHole4),2)))


#Calculate total chain lengths accounting for sprocket geometry and chain sag
LChainLengthHole1 = (ChainAroundSprocketHole1 + ChainStraightHole1*ChainSag1*leftChainTolerance)-rotationRadiusEst
LChainLengthHole2 = (ChainAroundSprocketHole2 + ChainStraightHole2*ChainSag2*leftChainTolerance)-rotationRadiusEst
LChainLengthHole3 = (ChainAroundSprocketHole3 + ChainStraightHole3*ChainSag3*leftChainTolerance)-rotationRadiusEst
LChainLengthHole4 = (ChainAroundSprocketHole4 + ChainStraightHole4*ChainSag4*leftChainTolerance)-rotationRadiusEst
RChainLengthHole1 = (ChainAroundSprocketHole1 + ChainStraightHole1*ChainSag1*rightChainTolerance)-rotationRadiusEst
RChainLengthHole2 = (ChainAroundSprocketHole2 + ChainStraightHole2*ChainSag2*rightChainTolerance)-rotationRadiusEst
RChainLengthHole3 = (ChainAroundSprocketHole3 + ChainStraightHole3*ChainSag3*rightChainTolerance)-rotationRadiusEst
RChainLengthHole4 = (ChainAroundSprocketHole4 + ChainStraightHole4*ChainSag4*rightChainTolerance)-rotationRadiusEst


print "Previous machine parameters:"
print "Motor Spacing: " + str(motorSpacing) + ", Motor Y Offset: " + str(motorYoffsetEst) + ", Rotation Disk Radius: " + str(rotationRadiusEst) + ", Chain Sag Correction Value: " + str(chainSagCorrectionEst)
print "LHole1: "+str(LChainLengthHole1)+", RHole1: "+str(RChainLengthHole1)
print "LHole2: "+str(LChainLengthHole2)+", RHole2: "+str(RChainLengthHole2)
print "LHole3: "+str(LChainLengthHole3)+", RHole3: "+str(RChainLengthHole3)
print "LHole4: "+str(LChainLengthHole4)+", RHole4: "+str(RChainLengthHole4)

x = raw_input("")

motorYcoordEst = (workspaceHeight/2) + motorYoffsetEst
motorXcoordEst = motorXcoord
leftChainToleranceEst = leftChainTolerance
rightChainToleranceEst = rightChainTolerance
rotationRadiusEst = desiredRotationalRadius  # Not affected by chain compensation
chainSagCorrectionEst= chainSagCorrectionEst

LChainErrorHole1 = acceptableTolerance
LChainErrorHole2 = acceptableTolerance
LChainErrorHole3 = acceptableTolerance
LChainErrorHole4 = acceptableTolerance
RChainErrorHole1 = acceptableTolerance
RChainErrorHole2 = acceptableTolerance
RChainErrorHole3 = acceptableTolerance
RChainErrorHole4 = acceptableTolerance
previousErrorMagnitude = 99999999.9

bestErrorMagnitude = 99999999.9
bestmotorYcoordEst = 0.0
bestmotorXcoordEst = 0.0
bestrotationRadiusEst = 0.0
bestchainSagCorrectionEst = 0.0
bestleftChainToleranceEst = 0.0
bestrightChainToleranceEst = 0.0
bestLChainErrorHole1 = 0.0
bestLChainErrorHole2 = 0.0
bestLChainErrorHole3 = 0.0
bestLChainErrorHole4 = 0.0
bestRChainErrorHole1 = 0.0
bestRChainErrorHole2 = 0.0
bestRChainErrorHole3 = 0.0
bestRChainErrorHole4 = 0.0

revertCounter = 0
scaleMultiplier = 1.0
n = 0

print "Iterating for new machine parameters"

# Iterate until error tolerance is achieved or maximum number of iterations occurs
errorMagnitude = 99999
while(errorMagnitude > acceptableTolerance and n < numberOfIterations):
	n += 1
	MotorDistanceHole1 = math.sqrt(math.pow(motorXcoord + H1x,2) + math.pow(motorYcoordEst + H1y ,2))
	MotorDistanceHole2 = math.sqrt(math.pow(motorXcoord + H2x,2) + math.pow(motorYcoordEst + H2y ,2))
	MotorDistanceHole3 = math.sqrt(math.pow(motorXcoord + H3x,2) + math.pow(motorYcoordEst + H3y ,2))
	MotorDistanceHole4 = math.sqrt(math.pow(motorXcoord + H4x,2) + math.pow(motorYcoordEst + H4y ,2))

	#Calculate the chain angles from horizontal, based on if the chain connects to the sled from the top or bottom of the sprocket
	if chainOverSprocket == 1:
		ChainAngleHole1 = math.asin((motorYcoordEst + H1y) / MotorDistanceHole1) + math.asin(sprocketRadius/MotorDistanceHole1)
		ChainAngleHole2 = math.asin((motorYcoordEst + H2y) / MotorDistanceHole2) + math.asin(sprocketRadius/MotorDistanceHole2)
		ChainAngleHole3 = math.asin((motorYcoordEst + H3y) / MotorDistanceHole3) + math.asin(sprocketRadius/MotorDistanceHole3)
		ChainAngleHole4 = math.asin((motorYcoordEst + H4y) / MotorDistanceHole4) + math.asin(sprocketRadius/MotorDistanceHole4)

		ChainAroundSprocketHole1 = sprocketRadius * ChainAngleHole1
		ChainAroundSprocketHole2 = sprocketRadius * ChainAngleHole2
		ChainAroundSprocketHole3 = sprocketRadius * ChainAngleHole3
		ChainAroundSprocketHole4 = sprocketRadius * ChainAngleHole4
	else:
		ChainAngleHole1 = math.asin((motorYcoordEst + H1y) / MotorDistanceHole1) - math.asin(sprocketRadius/MotorDistanceHole1)
		ChainAngleHole2 = math.asin((motorYcoordEst + H2y) / MotorDistanceHole2) - math.asin(sprocketRadius/MotorDistanceHole2)
		ChainAngleHole3 = math.asin((motorYcoordEst + H3y) / MotorDistanceHole3) - math.asin(sprocketRadius/MotorDistanceHole3)
		ChainAngleHole4 = math.asin((motorYcoordEst + H4y) / MotorDistanceHole4) - math.asin(sprocketRadius/MotorDistanceHole4)

		ChainAroundSprocketHole1 = sprocketRadius * (3.14159 - ChainAngleHole1)
		ChainAroundSprocketHole2 = sprocketRadius * (3.14159 - ChainAngleHole2)
		ChainAroundSprocketHole3 = sprocketRadius * (3.14159 - ChainAngleHole3)
		ChainAroundSprocketHole4 = sprocketRadius * (3.14159 - ChainAngleHole4)

	#Calculate the straight chain length from the sprocket to the bit
	ChainStraightHole1 = math.sqrt(math.pow(MotorDistanceHole1,2) - math.pow(sprocketRadius,2))
	ChainStraightHole2 = math.sqrt(math.pow(MotorDistanceHole2,2) - math.pow(sprocketRadius,2))
	ChainStraightHole3 = math.sqrt(math.pow(MotorDistanceHole3,2) - math.pow(sprocketRadius,2))
	ChainStraightHole4 = math.sqrt(math.pow(MotorDistanceHole4,2) - math.pow(sprocketRadius,2))

	#Correct the straight chain lengths to account for chain sag
	ChainSag1 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole1),2) * math.pow(ChainStraightHole1,2) * math.pow((math.tan(ChainAngleHole2) * math.cos(ChainAngleHole1)) + math.sin(ChainAngleHole1),2)))
	ChainSag2 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole2),2) * math.pow(ChainStraightHole2,2) * math.pow((math.tan(ChainAngleHole1) * math.cos(ChainAngleHole2)) + math.sin(ChainAngleHole2),2)))
	ChainSag3 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole3),2) * math.pow(ChainStraightHole3,2) * math.pow((math.tan(ChainAngleHole4) * math.cos(ChainAngleHole3)) + math.sin(ChainAngleHole3),2)))
	ChainSag4 = (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleHole4),2) * math.pow(ChainStraightHole4,2) * math.pow((math.tan(ChainAngleHole3) * math.cos(ChainAngleHole4)) + math.sin(ChainAngleHole4),2)))


	#Calculate total chain lengths accounting for sprocket geometry and chain sag
	LChainLengthHole1Est = (ChainAroundSprocketHole1 + ChainStraightHole1*ChainSag1*leftChainToleranceEst)-rotationRadiusEst
	LChainLengthHole2Est = (ChainAroundSprocketHole2 + ChainStraightHole2*ChainSag2*leftChainToleranceEst)-rotationRadiusEst
	LChainLengthHole3Est = (ChainAroundSprocketHole3 + ChainStraightHole3*ChainSag3*leftChainToleranceEst)-rotationRadiusEst
	LChainLengthHole4Est = (ChainAroundSprocketHole4 + ChainStraightHole4*ChainSag4*leftChainToleranceEst)-rotationRadiusEst
	RChainLengthHole1Est = (ChainAroundSprocketHole1 + ChainStraightHole1*ChainSag1*rightChainToleranceEst)-rotationRadiusEst
	RChainLengthHole2Est = (ChainAroundSprocketHole2 + ChainStraightHole2*ChainSag2*rightChainToleranceEst)-rotationRadiusEst
	RChainLengthHole3Est = (ChainAroundSprocketHole3 + ChainStraightHole3*ChainSag3*rightChainToleranceEst)-rotationRadiusEst
	RChainLengthHole4Est = (ChainAroundSprocketHole4 + ChainStraightHole4*ChainSag4*rightChainToleranceEst)-rotationRadiusEst

	# Determine chain length errors for current estimated machine parameters versus the measured parameters

	LChainErrorHole1 = LChainLengthHole1Est - LChainLengthHole1
	LChainErrorHole2 = LChainLengthHole2Est - LChainLengthHole2
	LChainErrorHole3 = LChainLengthHole3Est - LChainLengthHole3
	LChainErrorHole4 = LChainLengthHole4Est - LChainLengthHole4
	RChainErrorHole1 = RChainLengthHole1Est - RChainLengthHole1
	RChainErrorHole2 = RChainLengthHole2Est - RChainLengthHole2
	RChainErrorHole3 = RChainLengthHole3Est - RChainLengthHole3
	RChainErrorHole4 = RChainLengthHole4Est - RChainLengthHole4

	errorMagnitude = math.sqrt( (LChainErrorHole1*LChainErrorHole1 + LChainErrorHole2*LChainErrorHole2 + LChainErrorHole3*LChainErrorHole3 + LChainErrorHole4*LChainErrorHole4 + RChainErrorHole1*RChainErrorHole1 + RChainErrorHole2*RChainErrorHole2 + RChainErrorHole3*RChainErrorHole3 + RChainErrorHole4*RChainErrorHole4) / 8.0)
	#raw_input("press key")
	if (errorMagnitude >= previousErrorMagnitude):
		#print "N: "+str(n) + " Error: "+str(round(errorMagnitude,4)) + ", Chain Sag:"+str(round(chainSagCorrectionEst,4))+", scale Multiplier:"+str(scaleMultiplier)
		motorYcoordEst = previousmotorYcoordEst
		motorXcoordEst = previousmotorXcoordEst
		rotationRadiusEst = previousrotationRadiusEst
		chainSagCorrectionEst = previouschainSagCorrectionEst
		leftChainToleranceEst = previousleftChainToleranceEst
		rightChainToleranceEst = previousrightChainToleranceEst
		revertCounter += 1
		if revertCounter == 10000:
			#scaleMultiplier *= 1.001
			#previousErrorMagnitude = 9999999.9
			#revertCounter = 0
			adjustChainCompensation = True
			adjustChainSag = False
			adjustmotorYcoord = False
		#else:
			#scaleMultiplier = 1.0
	else:
		#print "N (better): "+str(n)+", Error Magnitude="+str(errorMagnitude)
		#scaleMultiplier *= 1/1.1
		revertCount = 0
		previousErrorMagnitude = errorMagnitude
		previousmotorYcoordEst = motorYcoordEst
		previousmotorXcoordEst = motorXcoordEst
		previousrotationRadiusEst = rotationRadiusEst
		previouschainSagCorrectionEst = chainSagCorrectionEst
		previousleftChainToleranceEst = leftChainToleranceEst
		previousrightChainToleranceEst = rightChainToleranceEst
		if (errorMagnitude < bestErrorMagnitude):
			bestErrorMagnitude = errorMagnitude
			bestmotorYcoordEst = motorYcoordEst
			bestmotorXcoordEst = motorXcoordEst
			bestrotationRadiusEst = rotationRadiusEst
			bestchainSagCorrectionEst = chainSagCorrectionEst
			bestleftChainToleranceEst = leftChainToleranceEst
			bestrightChainToleranceEst = rightChainToleranceEst
			bestLChainErrorHole1 = LChainErrorHole1
			bestLChainErrorHole2 = LChainErrorHole2
			bestLChainErrorHole3 = LChainErrorHole3
			bestLChainErrorHole4 = LChainErrorHole4
			bestRChainErrorHole1 = RChainErrorHole1
			bestRChainErrorHole2 = RChainErrorHole2
			bestRChainErrorHole3 = RChainErrorHole3
			bestRChainErrorHole4 = RChainErrorHole4

			print "---------------------------------------------------------------------------------------------"
			print "N: " + str(n) + ", Error Magnitude: " + str(round(bestErrorMagnitude, 3)) + ", Motor Y Offset: " + str(round(bestmotorYcoordEst-workspaceHeight/2.0, 3)) + ", Rotation Disk Radius: " + str(round(bestrotationRadiusEst, 3)) + ", Chain Sag Correction Value: " + str(round(bestchainSagCorrectionEst, 6)) + ", MotorX: "+str(round(bestmotorXcoordEst,3)) + ", Left Chain:"+str(round(bestleftChainToleranceEst,5))+", Right Chain:"+str(round(bestrightChainToleranceEst,5))
			print "  LChain Error Hole 1: " + str(round(bestLChainErrorHole1,4)) + ", LChain Error Hole 2: " + str(round(bestLChainErrorHole2,4)) + ", LChain Error Hole 3: " + str(round(bestLChainErrorHole3,4)) + ", LChain Error Hole 4: " + str(round(bestLChainErrorHole4,4))
			print "  RChain Error Hole 1: " + str(round(bestRChainErrorHole1,4)) + ", RChain Error Hole 2: " + str(round(bestRChainErrorHole2,4)) + ", RChain Error Hole 3: " + str(round(bestRChainErrorHole3,4)) + ", RChain Error Hole 4: " + str(round(bestRChainErrorHole4,4))

	#pick a random variable to adjust
	#x = raw_input("")

	direction = random.randint(0,1)
	adjustValue = random.randint(1, 100)
	Completed = False # trick value to enter while
	while (Completed == False):
		picked = random.randint(1,6)
		tscaleMultiplier = scaleMultiplier * float(adjustValue)/100.0
		if (direction == 0):
			tscaleMultiplier *= -1.0
		if (picked == 1 and adjustmotorYcoord):
			motorYcoordEst += errorMagnitude*motorYcoordCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 2 and adjustChainSag):
			chainSagCorrectionEst += errorMagnitude*chainSagCorrectionCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 3 and adjustMotorSpacing):
			motorXcoordEst += errorMagnitude*motorXcoordCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 4 and adjustRotationalRadius):
			rotationRadiusEst += errorMagnitude*rotationRadiusCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 5 and adjustChainCompensation):
			leftChainToleranceEst += errorMagnitude*chainCompensationCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 6 and adjustChainCompensation):
			rightChainToleranceEst += errorMagnitude*chainCompensationCorrectionScale*tscaleMultiplier
			Completed = True

	if (False):
		if (rotationRadiusEst<desiredRotationalRadius-2):
			rotationRadiusEst = desiredRotationalRadius-2
		if (rotationRadiusEst>desiredRotationalRadius+2):
			rotationRadiusEst = desiredRotationalRadius+2
		if (motorXcoordEst<motorXcoord-2):
			motorXcoordEst = motorXcoord - 2
		if (motorXcoordEst>motorXcoord+2):
			motorXcoordEst = motorXcoord +2
		if (chainSagCorrectionEst < 10):
			chainSagCorrectionEst = 10
		if (chainSagCorrectionEst > 60):
			chainSagCorrectionEst = 60
		if (leftChainToleranceEst > 1.006):
			leftChainToleranceEst = 1.006
		if (leftChainToleranceEst < 1.001):
			leftChainToleranceEst = 1.001
		if (rightChainToleranceEst > 1.006):
			rightChainToleranceEst = 1.006
		if (rightChainToleranceEst < 1.001):
			rightChainToleranceEst = 1.001



print "---------------------------------------------------------------------------------------------"
if n == numberOfIterations:
	print "Machine parameters could no solve to your desired tolerance, but did you really expect to be able to?"
else:
	print "Solved!"

print "N: " + str(n) + ", Error Magnitude: " + str(round(bestErrorMagnitude, 3)) + ", Motor Y Offset: " + str(round(bestmotorYcoordEst-workspaceHeight/2.0, 3)) + ", Rotation Disk Radius: " + str(round(bestrotationRadiusEst, 3)) + ", Chain Sag Correction Value: " + str(round(bestchainSagCorrectionEst, 6)) + ", MotorX: "+str(round(bestmotorXcoordEst,3)) + ", Left Chain:"+str(round(bestleftChainToleranceEst,5))+", Right Chain:"+str(round(bestrightChainToleranceEst,5))
print "  LChain Error Hole 1: " + str(round(bestLChainErrorHole1,4)) + ", LChain Error Hole 2: " + str(round(bestLChainErrorHole2,4)) + ", LChain Error Hole 3: " + str(round(bestLChainErrorHole3,4)) + ", LChain Error Hole 4: " + str(round(bestLChainErrorHole4,4))
print "  RChain Error Hole 1: " + str(round(bestRChainErrorHole1,4)) + ", RChain Error Hole 2: " + str(round(bestRChainErrorHole2,4)) + ", RChain Error Hole 3: " + str(round(bestRChainErrorHole3,4)) + ", RChain Error Hole 4: " + str(round(bestRChainErrorHole4,4))

print "---------------------------------------------------------------------------------------------"

x="n"
while (x<>"x"):
   x = raw_input ("Press 'x' to exit")
