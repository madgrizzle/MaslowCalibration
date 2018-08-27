import math
import random

y = 0.32
z = 1 + y/100

print (str(z))

workspaceHeight = 1219.2
workspaceWidth = 2438.4
gearTeeth = 10
chainPitch = 6.35


#default parameters used during calibration cut
motorSpacing = 3602.6
motorYoffsetEst = 468.4
rotationRadiusEst = 133
chainSagCorrectionEst = 27.394023
chainOverSprocket = 1
leftChainTolerance = 1.0+0.347900203615/100.0
rightChainTolerance =1.0+0.360479822602/100.0


#default cut parameters
distBetweenCuts12 = 1928.8
distBetweenCuts34 = 1927.2
distWorkareaTopToCut5 = 236.536
bitDiameter = 6.35

#optimization parameters
acceptableTolerance = .05
numberOfIterations = 10000000
motorYcoordCorrectionScale = 0.3
chainSagCorrectionCorrectionScale = 0.2
motorXcoordCorrectionScale = 0.001
rotationRadiusCorrectionScale = 0.001
chainCompensationCorrectionScale = 0.003
desiredRotationalRadius = 139.1

#optional adjustments
adjustmotorYcoord = True
adjustChainSag = True
adjustMotorSpacing = True
adjustRotationalRadius = True
adjustChainCompensation = True

print " -- Machine Parameters During Calibration Cut --"
x = raw_input ("Enter Motor Spacing in mm (enter for "+str(motorSpacing)+"):")
if (x <> ""):
	motorSpacing = float(x)
x = raw_input ("Enter Height of Motors Above WorkArea in mm (enter for "+str(motorYoffsetEst)+"):")
if (x <> ""):
	motorYoffsetEst = float(x)
x = raw_input ("Enter Rotational Radius in mm (enter for "+str(rotationRadiusEst)+"):")
if (x <> ""):
	rotationRadiusEst = float(x)
x = raw_input ("Enter Chain Sag Correction (enter for "+str(chainSagCorrectionEst)+"):")
if (x <> ""):
	chainSagCorrectionEst = float(x)
x = raw_input ("Enter 1 for Chain Over Sprocket or 0 for Chain Under Sprocket (enter for "+str(chainOverSprocket)+" or [1/0]):")
if (x <> ""):
	chainOverSprocket = int(x)
x = raw_input ("Enter Left Chain Tolerance (enter for "+str((leftChainTolerance-1.0)*100)+"):")
if (x <> ""):
	leftChainTolerance = 1+float(x)/100.0
x = raw_input ("Enter Right Chain Tolerance (enter for "+str((rightChainTolerance-1.0)*100)+"):")
if (x <> ""):
	rightChainTolerance = 1+float(x)/100.0

print
print " -- Cut Measurements --"
x = raw_input ("Enter Distance Between Cuts 1 and 2 in mm (enter for "+str(distBetweenCuts12)+"):")
if (x <> ""):
	distBetweenCuts12 = float(x)

x = raw_input ("Enter Distance Between Cuts 3 and 4 in mm (enter for "+str(distBetweenCuts34)+"):")
if (x <> ""):
	distBetweenCuts34 = float(x)

x = raw_input ("Enter Distance From Top of Board to Top of Cut 5 in mm (enter for "+str(distWorkareaTopToCut5)+"):")
if (x <> ""):
	distWorkareaTopToCut5 = float(x)

x = raw_input ("Enter Bit Diameter in mm (enter for "+str(bitDiameter)+"):")
if (x <> ""):
	bitDiameter = float(x)


print
print " -- Optimization Parameters --"

x = raw_input ("Acceptable Tolerance in mm (enter for "+str(acceptableTolerance)+"):")
if (x <> ""):
	acceptableTolerance = float(x)

x = raw_input ("Number of Iterations (enter for "+str(numberOfIterations)+"):")
if (x <> ""):
	numberOfIterations = int(x)

x = raw_input ("motorYcoord Correction scale (enter for "+str(motorYcoordCorrectionScale)+"):")
if (x <> ""):
	motorYcoordCorrectionScale = float(x)

x = raw_input ("Chain Sag Correction scale (enter for "+str(chainSagCorrectionCorrectionScale)+"):")
if (x <> ""):
	chainSagCorrectionCorrectionScale = float(x)

x = raw_input ("Desired Rotational Radius (enter for "+str(desiredRotationalRadius)+"):")
if (x <> ""):
	desiredRotationalRadius = float(x)

x = raw_input ("Adjust Rotational Radius (enter for "+str(adjustRotationalRadius)+" or [y/n]):")
if (x == "y" or (x == "" and adjustRotationalRadius)):
	adjustRotationalRadius = True
	x = raw_input ("Rotation Radius Correction scale (enter for "+str(rotationRadiusCorrectionScale)+"):")
	if x <> "":
		rotationRadiusCorrectionScale = float(x)
else:
	adjustRotationalRadius = False

x = raw_input ("Adjust Motor Spacing (enter for "+str(adjustMotorSpacing)+" or [y/n]):")
if (x == "y" or ( x=="" and adjustMotorSpacing)):
	adjustMotorSpacing = True
	x = raw_input ("Motor Spacing Correction scale (enter for "+str(motorXcoordCorrectionScale)+"):")
	if x <> "":
		motorXcoordCorrectionScale = float(x)
else:
	adjustMotorSpacing = False

# Gather current machine parameters

motorXcoord = motorSpacing/2
motorYcoordEst = (workspaceHeight/2) + motorYoffsetEst+.25
sprocketRadius = (gearTeeth*chainPitch / 2.0 / 3.14159 + chainPitch/math.sin(3.14159 / gearTeeth)/2.0)/2.0
leftChainMaslowMeasuredLength = motorSpacing / leftChainTolerance
rightChainMaslowMeasuredLength = motorSpacing / rightChainTolerance

# Calculate the actual chain lengths for each cut location

MotorDistanceCut1 = math.sqrt(math.pow(motorXcoord - ((workspaceWidth/2)-254),2) + math.pow(motorYcoordEst - ((workspaceHeight/2)-254),2))
MotorDistanceCut2 = math.sqrt(math.pow(motorXcoord + ((workspaceWidth/2)-254),2) + math.pow(motorYcoordEst - ((workspaceHeight/2)-254),2))
MotorDistanceCut3 = math.sqrt(math.pow(motorXcoord - ((workspaceWidth/2)-254),2) + math.pow(motorYcoordEst + ((workspaceHeight/2)-254),2))
MotorDistanceCut4 = math.sqrt(math.pow(motorXcoord + ((workspaceWidth/2)-254),2) + math.pow(motorYcoordEst + ((workspaceHeight/2)-254),2))

#Calculate the chain angles from horizontal, based on if the chain connects to the sled from the top or bottom of the sprocket
if chainOverSprocket == 1:
	ChainAngleCut1 = math.asin((motorYcoordEst - ((workspaceHeight/2)-254)) / MotorDistanceCut1) + math.asin(sprocketRadius/MotorDistanceCut1)
	ChainAngleCut2 = math.asin((motorYcoordEst - ((workspaceHeight/2)-254)) / MotorDistanceCut2) + math.asin(sprocketRadius/MotorDistanceCut2)
	ChainAngleCut3 = math.asin((motorYcoordEst + ((workspaceHeight/2)-254)) / MotorDistanceCut3) + math.asin(sprocketRadius/MotorDistanceCut3)
	ChainAngleCut4 = math.asin((motorYcoordEst + ((workspaceHeight/2)-254)) / MotorDistanceCut4) + math.asin(sprocketRadius/MotorDistanceCut4)

	ChainAroundSprocketCut1 = sprocketRadius * ChainAngleCut1
	ChainAroundSprocketCut2 = sprocketRadius * ChainAngleCut2
	ChainAroundSprocketCut3 = sprocketRadius * ChainAngleCut3
	ChainAroundSprocketCut4 = sprocketRadius * ChainAngleCut4
else:
	ChainAngleCut1 = math.asin((motorYcoordEst - ((workspaceHeight/2)-254)) / MotorDistanceCut1) - math.asin(sprocketRadius/MotorDistanceCut1)
	ChainAngleCut2 = math.asin((motorYcoordEst - ((workspaceHeight/2)-254)) / MotorDistanceCut2) - math.asin(sprocketRadius/MotorDistanceCut2)
	ChainAngleCut3 = math.asin((motorYcoordEst + ((workspaceHeight/2)-254)) / MotorDistanceCut3) - math.asin(sprocketRadius/MotorDistanceCut3)
	ChainAngleCut4 = math.asin((motorYcoordEst + ((workspaceHeight/2)-254)) / MotorDistanceCut4) - math.asin(sprocketRadius/MotorDistanceCut4)

	ChainAroundSprocketCut1 = sprocketRadius * (3.14159 - ChainAngleCut1)
	ChainAroundSprocketCut2 = sprocketRadius * (3.14159 - ChainAngleCut2)
	ChainAroundSprocketCut3 = sprocketRadius * (3.14159 - ChainAngleCut3)
	ChainAroundSprocketCut4 = sprocketRadius * (3.14159 - ChainAngleCut4)

#Calculate the straight chain length from the sprocket to the bit
ChainStraightCut1 = math.sqrt(math.pow(MotorDistanceCut1,2) - math.pow(sprocketRadius,2))
ChainStraightCut2 = math.sqrt(math.pow(MotorDistanceCut2,2) - math.pow(sprocketRadius,2))
ChainStraightCut3 = math.sqrt(math.pow(MotorDistanceCut3,2) - math.pow(sprocketRadius,2))
ChainStraightCut4 = math.sqrt(math.pow(MotorDistanceCut4,2) - math.pow(sprocketRadius,2))

#Correct the straight chain lengths to account for chain sag
ChainStraightCut1 *= (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut1),2) * math.pow(ChainStraightCut1,2) * math.pow((math.tan(ChainAngleCut2) * math.cos(ChainAngleCut1)) + math.sin(ChainAngleCut1),2)))
ChainStraightCut2 *= (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut2),2) * math.pow(ChainStraightCut2,2) * math.pow((math.tan(ChainAngleCut1) * math.cos(ChainAngleCut2)) + math.sin(ChainAngleCut2),2)))
ChainStraightCut3 *= (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut3),2) * math.pow(ChainStraightCut3,2) * math.pow((math.tan(ChainAngleCut4) * math.cos(ChainAngleCut3)) + math.sin(ChainAngleCut3),2)))
ChainStraightCut4 *= (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut4),2) * math.pow(ChainStraightCut4,2) * math.pow((math.tan(ChainAngleCut3) * math.cos(ChainAngleCut4)) + math.sin(ChainAngleCut4),2)))

#Calculate total chain lengths accounting for sprocket geometry and chain sag
LChainLengthCut1 = (ChainAroundSprocketCut1 + ChainStraightCut1*leftChainTolerance)-rotationRadiusEst
LChainLengthCut2 = (ChainAroundSprocketCut2 + ChainStraightCut2*leftChainTolerance)-rotationRadiusEst
LChainLengthCut3 = (ChainAroundSprocketCut3 + ChainStraightCut3*leftChainTolerance)-rotationRadiusEst
LChainLengthCut4 = (ChainAroundSprocketCut4 + ChainStraightCut4*leftChainTolerance)-rotationRadiusEst
RChainLengthCut1 = (ChainAroundSprocketCut1 + ChainStraightCut1*rightChainTolerance)-rotationRadiusEst
RChainLengthCut2 = (ChainAroundSprocketCut2 + ChainStraightCut2*rightChainTolerance)-rotationRadiusEst
RChainLengthCut3 = (ChainAroundSprocketCut3 + ChainStraightCut3*rightChainTolerance)-rotationRadiusEst
RChainLengthCut4 = (ChainAroundSprocketCut4 + ChainStraightCut4*rightChainTolerance)-rotationRadiusEst

# Set up the iterative algorithm

print "Previous machine parameters:"
print "Motor Spacing: " + str(motorSpacing) + ", Motor Y Offset: " + str(motorYoffsetEst) + ", Rotation Disk Radius: " + str(rotationRadiusEst) + ", Chain Sag Correction Value: " + str(chainSagCorrectionEst)

motorYcoordEst = motorYcoordEst - ((workspaceHeight/2)-254) #distWorkareaTopToCut5 + (bitDiameter / 2) + 12.7
motorXcoordEst = motorXcoord
leftChainToleranceEst = leftChainTolerance
rightChainToleranceEst = rightChainTolerance
rotationRadiusEst = desiredRotationalRadius  # Not affected by chain compensation
chainSagCorrectionEst= chainSagCorrectionEst
cut34YoffsetEst = 0
LChainErrorCut1 = acceptableTolerance
LChainErrorCut2 = acceptableTolerance
LChainErrorCut3 = acceptableTolerance
LChainErrorCut4 = acceptableTolerance
RChainErrorCut1 = acceptableTolerance
RChainErrorCut2 = acceptableTolerance
RChainErrorCut3 = acceptableTolerance
RChainErrorCut4 = acceptableTolerance
previousErrorMagnitude = 99999999.9
bestErrorMagnitude = 99999999.9
revertCounter = 0
scaleMultiplier = 1.0
n = 0

print "Iterating for new machine parameters"

# Iterate until error tolerance is achieved or maximum number of iterations occurs
errorMagnitude = 99999
while(errorMagnitude > acceptableTolerance and n < numberOfIterations):
	n += 1

	# Calculate chain lengths for current estimated parameters

	MotorDistanceCut1Est = math.sqrt(math.pow(motorXcoordEst - (distBetweenCuts12 / 2),2) + math.pow(motorYcoordEst,2))
	MotorDistanceCut2Est = math.sqrt(math.pow(motorXcoordEst + (distBetweenCuts12 / 2),2) + math.pow(motorYcoordEst,2))
	MotorDistanceCut3Est = math.sqrt(math.pow(motorXcoordEst - (distBetweenCuts34 / 2),2) + math.pow(motorYcoordEst + (workspaceHeight-508),2))
	MotorDistanceCut4Est = math.sqrt(math.pow(motorXcoordEst + (distBetweenCuts34 / 2),2) + math.pow(motorYcoordEst + (workspaceHeight-508),2))

	#Calculate the chain angles from horizontal, based on if the chain connects to the sled from the top or bottom of the sprocket
	if chainOverSprocket == 1:
		ChainAngleCut1Est = math.asin(motorYcoordEst / MotorDistanceCut1Est) + math.asin(sprocketRadius / MotorDistanceCut1Est)
		ChainAngleCut2Est = math.asin(motorYcoordEst / MotorDistanceCut2Est) + math.asin(sprocketRadius / MotorDistanceCut2Est)
		ChainAngleCut3Est = math.asin((motorYcoordEst + (workspaceHeight-508) - cut34YoffsetEst) / MotorDistanceCut3Est) + math.asin(sprocketRadius / MotorDistanceCut3Est)
		ChainAngleCut4Est = math.asin((motorYcoordEst + (workspaceHeight-508) - cut34YoffsetEst) / MotorDistanceCut4Est) + math.asin(sprocketRadius / MotorDistanceCut4Est)

		ChainAroundSprocketCut1Est = sprocketRadius * ChainAngleCut1Est
		ChainAroundSprocketCut2Est = sprocketRadius * ChainAngleCut2Est
		ChainAroundSprocketCut3Est = sprocketRadius * ChainAngleCut3Est
		ChainAroundSprocketCut4Est = sprocketRadius * ChainAngleCut4Est
	else:
		ChainAngleCut1Est = math.asin(motorYcoordEst / MotorDistanceCut1Est) - math.asin(sprocketRadius / MotorDistanceCut1Est)
		ChainAngleCut2Est = math.asin(motorYcoordEst / MotorDistanceCut2Est) - math.asin(sprocketRadius / MotorDistanceCut2Est)
		ChainAngleCut3Est = math.asin((motorYcoordEst + (workspaceHeight-508) - cut34YoffsetEst) / MotorDistanceCut3Est) - math.asin(sprocketRadius / MotorDistanceCut3Est)
		ChainAngleCut4Est = math.asin((motorYcoordEst + (workspaceHeight-508) - cut34YoffsetEst) / MotorDistanceCut4Est) - math.asin(sprocketRadius / MotorDistanceCut4Est)

		ChainAroundSprocketCut1Est = sprocketRadius * (3.14159 - ChainAngleCut1Est)
		ChainAroundSprocketCut2Est = sprocketRadius * (3.14159 - ChainAngleCut2Est)
		ChainAroundSprocketCut3Est = sprocketRadius * (3.14159 - ChainAngleCut3Est)
		ChainAroundSprocketCut4Est = sprocketRadius * (3.14159 - ChainAngleCut4Est)

	#Calculate the straight chain length from the sprocket to the bit
	ChainStraightCut1Est = math.sqrt(math.pow(MotorDistanceCut1Est,2) - math.pow(sprocketRadius,2))
	ChainStraightCut2Est = math.sqrt(math.pow(MotorDistanceCut2Est,2) - math.pow(sprocketRadius,2))
	ChainStraightCut3Est = math.sqrt(math.pow(MotorDistanceCut3Est,2) - math.pow(sprocketRadius,2))
	ChainStraightCut4Est = math.sqrt(math.pow(MotorDistanceCut4Est,2) - math.pow(sprocketRadius,2))

	#Correct the straight chain lengths to account for chain sag
	LChainStraightCut1Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut1Est),2) * math.pow(ChainStraightCut1Est,2) * math.pow((math.tan(ChainAngleCut2Est) * math.cos(ChainAngleCut1Est)) + math.sin(ChainAngleCut1Est),2)))
	LChainStraightCut2Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut2Est),2) * math.pow(ChainStraightCut2Est,2) * math.pow((math.tan(ChainAngleCut1Est) * math.cos(ChainAngleCut2Est)) + math.sin(ChainAngleCut2Est),2)))
	LChainStraightCut3Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut3Est),2) * math.pow(ChainStraightCut3Est,2) * math.pow((math.tan(ChainAngleCut4Est) * math.cos(ChainAngleCut3Est)) + math.sin(ChainAngleCut3Est),2)))
	LChainStraightCut4Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut4Est),2) * math.pow(ChainStraightCut4Est,2) * math.pow((math.tan(ChainAngleCut3Est) * math.cos(ChainAngleCut4Est)) + math.sin(ChainAngleCut4Est),2)))

	RChainStraightCut1Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut1Est),2) * math.pow(ChainStraightCut1Est,2) * math.pow((math.tan(ChainAngleCut2Est) * math.cos(ChainAngleCut1Est)) + math.sin(ChainAngleCut1Est),2)))
	RChainStraightCut2Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut2Est),2) * math.pow(ChainStraightCut2Est,2) * math.pow((math.tan(ChainAngleCut1Est) * math.cos(ChainAngleCut2Est)) + math.sin(ChainAngleCut2Est),2)))
	RChainStraightCut3Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut3Est),2) * math.pow(ChainStraightCut3Est,2) * math.pow((math.tan(ChainAngleCut4Est) * math.cos(ChainAngleCut3Est)) + math.sin(ChainAngleCut3Est),2)))
	RChainStraightCut4Est = ChainStraightCut1Est * (1 + ((chainSagCorrectionEst / 1000000000000) * math.pow(math.cos(ChainAngleCut4Est),2) * math.pow(ChainStraightCut4Est,2) * math.pow((math.tan(ChainAngleCut3Est) * math.cos(ChainAngleCut4Est)) + math.sin(ChainAngleCut4Est),2)))

	#Calculate total chain lengths accounting for sprocket geometry and chain sag
	LChainLengthCut1Est = (ChainAroundSprocketCut1Est + ChainStraightCut1Est*leftChainToleranceEst)-rotationRadiusEst
	LChainLengthCut2Est = (ChainAroundSprocketCut2Est + ChainStraightCut2Est*leftChainToleranceEst)-rotationRadiusEst
	LChainLengthCut3Est = (ChainAroundSprocketCut3Est + ChainStraightCut3Est*leftChainToleranceEst)-rotationRadiusEst
	LChainLengthCut4Est = (ChainAroundSprocketCut4Est + ChainStraightCut4Est*leftChainToleranceEst)-rotationRadiusEst

	RChainLengthCut1Est = (ChainAroundSprocketCut1Est + ChainStraightCut1Est*rightChainToleranceEst)-rotationRadiusEst
	RChainLengthCut2Est = (ChainAroundSprocketCut2Est + ChainStraightCut2Est*rightChainToleranceEst)-rotationRadiusEst
	RChainLengthCut3Est = (ChainAroundSprocketCut3Est + ChainStraightCut3Est*rightChainToleranceEst)-rotationRadiusEst
	RChainLengthCut4Est = (ChainAroundSprocketCut4Est + ChainStraightCut4Est*rightChainToleranceEst)-rotationRadiusEst

	# Determine chain length errors for current estimated machine parameters versus the measured parameters

	LChainErrorCut1 = LChainLengthCut1Est - LChainLengthCut1
	LChainErrorCut2 = LChainLengthCut2Est - LChainLengthCut2
	LChainErrorCut3 = LChainLengthCut3Est - LChainLengthCut3
	LChainErrorCut4 = LChainLengthCut4Est - LChainLengthCut4
	RChainErrorCut1 = RChainLengthCut1Est - RChainLengthCut1
	RChainErrorCut2 = RChainLengthCut2Est - RChainLengthCut2
	RChainErrorCut3 = RChainLengthCut3Est - RChainLengthCut3
	RChainErrorCut4 = RChainLengthCut4Est - RChainLengthCut4

	errorMagnitude = math.sqrt( (LChainErrorCut1*LChainErrorCut1 + LChainErrorCut2*LChainErrorCut2 + LChainErrorCut3*LChainErrorCut3 + LChainErrorCut4*LChainErrorCut4 + RChainErrorCut1*RChainErrorCut1 + RChainErrorCut2*RChainErrorCut2 + RChainErrorCut3*RChainErrorCut3 + RChainErrorCut4*RChainErrorCut4) / 8.0)
	#raw_input("press key")
	if (errorMagnitude > previousErrorMagnitude):
		motorYcoordEst = previousmotorYcoordEst
		motorXcoordEst = previousmotorXcoordEst
		rotationRadiusEst = previousrotationRadiusEst
		chainSagCorrectionEst = previouschainSagCorrectionEst
		leftChainToleranceEst = previousleftChainToleranceEst
		rightChainToleranceEst = previousrightChainToleranceEst
		revertCounter += 1
		#print "N: "+str(n)
		if revertCounter == 100:
			#scaleMultiplier = 1.5
			#previousErrorMagnitude = 9999999.9
			revertCounter = 0
		else:
			scaleMultiplier = 1.0
	else:
		#print "N (better): "+str(n)+", Error Magnitude="+str(errorMagnitude)
		#scaleMultiplier *= 1/1.1
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
			bestLChainErrorCut1 = LChainErrorCut1
			bestLChainErrorCut2 = LChainErrorCut2
			bestLChainErrorCut3 = LChainErrorCut3
			bestLChainErrorCut4 = LChainErrorCut4
			bestRChainErrorCut1 = RChainErrorCut1
			bestRChainErrorCut2 = RChainErrorCut2
			bestRChainErrorCut3 = RChainErrorCut3
			bestRChainErrorCut4 = RChainErrorCut4

			bestmotorYoffsetEstPrint = bestmotorYcoordEst - distWorkareaTopToCut5 - (bitDiameter / 2) - 12.7
			print "---------------------------------------------------------------------------------------------"
			print "N: " + str(n) + ", Error Magnitude: " + str(round(bestErrorMagnitude, 3)) + ", Motor Y Offset: " + str(round(bestmotorYoffsetEstPrint, 3)) + ", Rotation Disk Radius: " + str(round(bestrotationRadiusEst, 3)) + ", Chain Sag Correction Value: " + str(round(bestchainSagCorrectionEst, 6)) + ", MotorX: "+str(round(bestmotorXcoordEst,3)) + ", Left Chain:"+str(round(bestleftChainToleranceEst,5))+", Right Chain:"+str(round(bestrightChainToleranceEst,5))
			print "  LChain Error Cut 1: " + str(round(bestLChainErrorCut1,4)) + ", LChain Error Cut 2: " + str(round(bestLChainErrorCut2,4)) + ", LChain Error Cut 3: " + str(round(bestLChainErrorCut3,4)) + ", LChain Error Cut 4: " + str(round(bestLChainErrorCut4,4))
			print "  RChain Error Cut 1: " + str(round(bestRChainErrorCut1,4)) + ", RChain Error Cut 2: " + str(round(bestRChainErrorCut2,4)) + ", RChain Error Cut 3: " + str(round(bestRChainErrorCut3,4)) + ", RChain Error Cut 4: " + str(round(bestRChainErrorCut4,4))

	#pick a random variable to adjust


	direction = random.randint(0,1)
	adjustValue = random.randint(1, 100)
	Completed = False # trick value to enter while
	while (Completed == False):
		picked = random.randint(1,6)
		if (direction == 0):
			scaleMultiplier *= -1
		scaleMultiplier *= float(adjustValue)/100.0
		if (picked == 1 and adjustmotorYcoord):
			motorYcoordEst += errorMagnitude*motorYcoordCorrectionScale*scaleMultiplier
			Completed = True
		if (picked == 2 and adjustChainSag):
			chainSagCorrectionEst += errorMagnitude*chainSagCorrectionCorrectionScale*scaleMultiplier
			Completed = True
		if (picked == 3 and adjustMotorSpacing):
			motorXcoordEst += errorMagnitude*motorXcoordCorrectionScale*scaleMultiplier
			Completed = True
		if (picked == 4 and adjustRotationalRadius):
			rotationRadiusEst += errorMagnitude*rotationRadiusCorrectionScale*scaleMultiplier
			Completed = True
		if (picked == 5 and adjustChainCompensation):
			leftChainToleranceEst += errorMagnitude*chainCompensationCorrectionScale*scaleMultiplier
			Completed = True
		if (picked == 6 and adjustChainCompensation):
			rightChainToleranceEst += errorMagnitude*chainCompensationCorrectionScale*scaleMultiplier
			Completed = True

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
bestmotorYoffsetEstPrint = bestmotorYcoordEst - distWorkareaTopToCut5 - (bitDiameter / 2) - 12.7

print "N: " + str(n) + ", Error Magnitude: " + str(round(bestErrorMagnitude, 3)) + ", Motor Y Offset: " + str(round(bestmotorYoffsetEstPrint, 3)) + ", Rotation Disk Radius: " + str(round(bestrotationRadiusEst, 3)) + ", Chain Sag Correction Value: " + str(round(bestchainSagCorrectionEst, 6)) + ", MotorX: "+str(round(bestmotorXcoordEst,3)) + ", Left Chain:"+str(round(bestleftChainToleranceEst,5))+", Right Chain:"+str(round(bestrightChainToleranceEst,5))
print "  LChain Error Cut 1: " + str(round(bestLChainErrorCut1,4)) + ", LChain Error Cut 2: " + str(round(bestLChainErrorCut2,4)) + ", LChain Error Cut 3: " + str(round(bestLChainErrorCut3,4)) + ", LChain Error Cut 4: " + str(round(bestLChainErrorCut4,4))
print "  RChain Error Cut 1: " + str(round(bestRChainErrorCut1,4)) + ", RChain Error Cut 2: " + str(round(bestRChainErrorCut2,4)) + ", RChain Error Cut 3: " + str(round(bestRChainErrorCut3,4)) + ", RChain Error Cut 4: " + str(round(bestRChainErrorCut4,4))

print "---------------------------------------------------------------------------------------------"

x="n"
while (x<>"x"):
   x = raw_input ("Press 'x' to exit")
