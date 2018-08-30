import math
import random

def CalculateChainLengths(leftMotorX, leftMotorY, rightMotorX, rightMotorY, targetX, targetY, chainOverSprocket, rotationRadius, chainSagCorrection, leftChainTolerance, rightChainTolerance):
	leftMotorDistanceTarget = math.sqrt(math.pow(leftMotorX - targetX,2) + math.pow(leftMotorY - targetY ,2))
	rightMotorDistanceTarget = math.sqrt(math.pow(rightMotorX - targetX,2) + math.pow(rightMotorY - targetY ,2))
	#Calculate the chain angles from horizontal, based on if the chain connects to the sled from the top or bottom of the sprocket
	if chainOverSprocket == 1:
		leftChainAngleTarget = (math.asin((leftMotorY - targetY) / leftMotorDistanceTarget) + math.asin(sprocketRadius/leftMotorDistanceTarget))*-1.0
		rightChainAngleTarget = (math.asin((rightMotorY - targetY) / rightMotorDistanceTarget) + math.asin(sprocketRadius/rightMotorDistanceTarget))*-1.0

		leftChainAroundSprocketTarget = sprocketRadius * leftChainAngleTarget
		rightChainAroundSprocketTarget = sprocketRadius * rightChainAngleTarget

	else:
		leftChainAngleTarget = (math.asin((leftMotorY - targetY) / leftMotorDistanceTarget) - math.asin(sprocketRadius/leftMotorDistanceTarget))*-1.0
		rightChainAngleTarget = (math.asin((rightMotorY - targetY) / rightMotorDistanceTarget) - math.asin(sprocketRadius/rightMotorDistanceTarget))*-1.0

		leftChainAroundSprocketTarget = sprocketRadius * (3.14159 - leftChainAngleTarget)
		rightChainAroundSprocketTarget = sprocketRadius * (3.14159 - rightChainAngleTarget)

	#Calculate the straight chain length from the sprocket to the bit
	leftChainStraightTarget = math.sqrt(math.pow(leftMotorDistanceTarget,2) - math.pow(sprocketRadius,2))
	rightChainStraightTarget = math.sqrt(math.pow(rightMotorDistanceTarget,2) - math.pow(sprocketRadius,2))

	#Correct the straight chain lengths to account for chain sag
	leftChainSag = (1 + ((chainSagCorrection / 1000000000000) * math.pow(math.cos(leftChainAngleTarget),2) * math.pow(leftChainStraightTarget,2) * math.pow((math.tan(rightChainAngleTarget) * math.cos(leftChainAngleTarget)) + math.sin(leftChainAngleTarget),2)))
	rightChainSag = (1 + ((chainSagCorrection / 1000000000000) * math.pow(math.cos(rightChainAngleTarget),2) * math.pow(rightChainStraightTarget,2) * math.pow((math.tan(leftChainAngleTarget) * math.cos(rightChainAngleTarget)) + math.sin(rightChainAngleTarget),2)))

	#Calculate total chain lengths accounting for sprocket geometry and chain sag
	LChainLengthTarget = (leftChainAroundSprocketTarget + leftChainStraightTarget*leftChainSag*leftChainTolerance)-rotationRadius
	RChainLengthTarget = (rightChainAroundSprocketTarget + rightChainStraightTarget*rightChainSag*rightChainTolerance)-rotationRadius

	return LChainLengthTarget, RChainLengthTarget

def CalculateCoordinates(dH0H1, dH0H2, dH0H3, dH0H4, dH1H2, dH1H4, dH2H3, dH3H4, dH0M5, dH2M5 ):
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
	return H0x, H0y, H1x, H1y, H2x, H2y, H3x, H3y, H4x, H4y

# adjust based upon machine settings
workspaceHeight = 1219.2
workspaceWidth = 2438.4
gearTeeth = 10
chainPitch = 6.35

# adjust in the event the hole pattern is changed
aH1x = (workspaceWidth/2.0-254.0)*-1.0
aH1y = (workspaceHeight/2.0-254.0)*-1.0
aH2x = aH1x
aH2y = aH1y*-1.0
aH3x = aH1x*-1.0
aH3y = aH2y
aH4x = aH3x
aH4y = aH1y

#parameters used during calibration cut.. currently assumes motors are level and 0,0 is centered
##---CHANGE THESE TO MATCH YOUR MACHINE WHEN YOU RAN THE HOLE PATTERN---##
motorSpacing = 3601.2
desiredMotorSpacing = 3602.6 #this allows you to change from motor spacing you cut with and make it a fixed value
motorYoffset = 468.4
rotationRadius = 139.1
chainSagCorrection = 31.865887
chainOverSprocket = 1
leftChainTolerance = 1.0 # can't use current values .. value must be less than or equal to 1
rightChainTolerance =1.0 # can't use current values .. value must be less than or equal to 1
desiredRotationalRadius = 139.1 #this allows you to change from rotation radius you cut with and make it a fixed value

#measured distances of hole pattern
##---CHANGE THESE TO WHAT YOU MEASURED---##
##---USE MILLIMETERS ONLY---##
##---My tape measure was off by 101 mm so the -101.0 adjust for it---##
##---CHANGE IT BECAUSE YOURS IS LIKELY DIFFERENT---###
dH0H1 = 1133.0-101.0
dH0H2 = 1133.0-101.0
dH0H3 = 1129.0-101.0
dH0H4 = 1133.0-101.0
dH1H2 = 814.0-101.0
dH1H4 = 2037.0-101.0
dH2H3 = 2036.0-101.0
dH3H4 = 812.0-101.0
dH0M5 = 466.0-101.0
dH2M5 = 1070.0-101.0

#optimization parameters.. this really does affect how well you can arrive at a solution and how good of a solution it is
acceptableTolerance = .05
numberOfIterations = 10000000
motorYcoordCorrectionScale = 0.01
motorXcoordCorrectionScale = 0.05
chainSagCorrectionCorrectionScale = 0.01
motorXcoordCorrectionScale = 0.001
rotationRadiusCorrectionScale = 0.001
chainCompensationCorrectionScale = 0.003

#optional adjustments
adjustMotorYcoord = True  # this allows raising lowering of top beam
adjustMotorTilt = True  # this allows tilting of top beam
adjustMotorXcoord = True  # this allows shifting of top beam
adjustChainSag = True
adjustRotationalRadius = False
adjustChainCompensation = True

# Gather current machine parameters
leftMotorX = motorSpacing/-2.0 #based on current method since gc/firmware doesn't allow for indpendent x,y of motors
rightMotorX = motorSpacing/2.0
leftMotorY = ((workspaceHeight/2.0) + motorYoffset)*-1.0
rightMotorY = ((workspaceHeight/2.0) + motorYoffset)*-1.0
sprocketRadius = (gearTeeth*chainPitch / 2.0 / 3.14159 + chainPitch/math.sin(3.14159 / gearTeeth)/2.0)/2.0 # new way to calculate.. needs validation

#calculate coordinates of the holes based upon distance measurements
H0x, H0y, H1x, H1y, H2x, H2y, H3x, H3y, H4x, H4y = CalculateCoordinates(dH0H1, dH0H2, dH0H3, dH0H4, dH1H2, dH1H4, dH2H3, dH3H4, dH0M5, dH2M5)

print "H1x:"+str(H1x)+", H1y:"+str(H1y)
print "H2x:"+str(H2x)+", H2y:"+str(H2y)
print "H3x:"+str(H3x)+", H3y:"+str(H3y)
print "H4x:"+str(H4x)+", H4y:"+str(H4y)
x=raw_input("") #pause for review

# Calculate the chain lengths for each hole location based upon inputted model

LChainLengthHole1, RChainLengthHole1 = CalculateChainLengths(leftMotorX, leftMotorY, rightMotorX, rightMotorY, aH1x, aH1y, chainOverSprocket, rotationRadius, chainSagCorrection, leftChainTolerance, rightChainTolerance)
LChainLengthHole2, RChainLengthHole2 = CalculateChainLengths(leftMotorX, leftMotorY, rightMotorX, rightMotorY, aH2x, aH2y, chainOverSprocket, rotationRadius, chainSagCorrection, leftChainTolerance, rightChainTolerance)
LChainLengthHole3, RChainLengthHole3 = CalculateChainLengths(leftMotorX, leftMotorY, rightMotorX, rightMotorY, aH3x, aH3y, chainOverSprocket, rotationRadius, chainSagCorrection, leftChainTolerance, rightChainTolerance)
LChainLengthHole4, RChainLengthHole4 = CalculateChainLengths(leftMotorX, leftMotorY, rightMotorX, rightMotorY, aH4x, aH4y, chainOverSprocket, rotationRadius, chainSagCorrection, leftChainTolerance, rightChainTolerance)

print "Machine parameters:"
print "Rotation Disk Radius: " + str(rotationRadius) + ", Chain Sag Correction Value: " + str(chainSagCorrection)
print "leftMotorX: "+str(leftMotorX) + ", leftMotorY: "+str(leftMotorY)+", rightMotorX: "+str(rightMotorX)+", rightMotorY:"+str(rightMotorY)
print "LHole1: "+str(LChainLengthHole1)+", RHole1: "+str(RChainLengthHole1)
print "LHole2: "+str(LChainLengthHole2)+", RHole2: "+str(RChainLengthHole2)
print "LHole3: "+str(LChainLengthHole3)+", RHole3: "+str(RChainLengthHole3)
print "LHole4: "+str(LChainLengthHole4)+", RHole4: "+str(RChainLengthHole4)

x=raw_input("") #pause for review

leftMotorXEst = leftMotorX-(desiredMotorSpacing-motorSpacing)/2.0 #adjusts motor x based upon change in motor spacing
leftMotorYEst = leftMotorY
rightMotorXEst = rightMotorX+(desiredMotorSpacing-motorSpacing)/2.0
rightMotorYEst = rightMotorY
leftChainToleranceEst = leftChainTolerance
rightChainToleranceEst = rightChainTolerance
rotationRadiusEst = desiredRotationalRadius  # Not affected by chain compensation
chainSagCorrectionEst= chainSagCorrection

LChainErrorHole1 = acceptableTolerance #this just makes it a float really
LChainErrorHole2 = acceptableTolerance
LChainErrorHole3 = acceptableTolerance
LChainErrorHole4 = acceptableTolerance
RChainErrorHole1 = acceptableTolerance
RChainErrorHole2 = acceptableTolerance
RChainErrorHole3 = acceptableTolerance
RChainErrorHole4 = acceptableTolerance
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

	# calculate chain lengths based upon estimated parameters and actual hole locations
	LChainLengthHole1Est, RChainLengthHole1Est = CalculateChainLengths(leftMotorXEst, leftMotorYEst, rightMotorXEst, rightMotorYEst, H1x, H1y, chainOverSprocket, rotationRadiusEst, chainSagCorrectionEst, leftChainToleranceEst, rightChainToleranceEst)
	LChainLengthHole2Est, RChainLengthHole2Est = CalculateChainLengths(leftMotorXEst, leftMotorYEst, rightMotorXEst, rightMotorYEst, H2x, H2y, chainOverSprocket, rotationRadiusEst, chainSagCorrectionEst, leftChainToleranceEst, rightChainToleranceEst)
	LChainLengthHole3Est, RChainLengthHole3Est = CalculateChainLengths(leftMotorXEst, leftMotorYEst, rightMotorXEst, rightMotorYEst, H3x, H3y, chainOverSprocket, rotationRadiusEst, chainSagCorrectionEst, leftChainToleranceEst, rightChainToleranceEst)
	LChainLengthHole4Est, RChainLengthHole4Est = CalculateChainLengths(leftMotorXEst, leftMotorYEst, rightMotorXEst, rightMotorYEst, H4x, H4y, chainOverSprocket, rotationRadiusEst, chainSagCorrectionEst, leftChainToleranceEst, rightChainToleranceEst)

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

	if (errorMagnitude >= previousErrorMagnitude):
		#print "N: "+str(n) + " Error: "+str(round(errorMagnitude,4)) + ", Chain Sag:"+str(round(chainSagCorrectionEst,4))+", scale Multiplier:"+str(scaleMultiplier)
		leftMotorXEst = previousleftMotorXEst
		leftMotorYEst = previousleftMotorYEst
		rightMotorXEst = previousrightMotorXEst
		rightMotorYEst = previousrightMotorYEst
		rotationRadiusEst = previousrotationRadiusEst
		chainSagCorrectionEst = previouschainSagCorrectionEst
		leftChainToleranceEst = previousleftChainToleranceEst
		rightChainToleranceEst = previousrightChainToleranceEst
		revertCounter += 1
		if revertCounter == 10000:
			revertCounter = 0 # currently doesn't do anything.  Can use this to make adjustments if process gets stuck
	else:
		revertCount = 0
		previousErrorMagnitude = errorMagnitude
		previousrotationRadiusEst = rotationRadiusEst
		previouschainSagCorrectionEst = chainSagCorrectionEst
		previousleftChainToleranceEst = leftChainToleranceEst
		previousrightChainToleranceEst = rightChainToleranceEst
		previousleftMotorXEst = leftMotorXEst
		previousleftMotorYEst = leftMotorYEst
		previousrightMotorXEst = rightMotorXEst
		previousrightMotorYEst = rightMotorYEst
		if (errorMagnitude < bestErrorMagnitude):
			bestErrorMagnitude = errorMagnitude
			bestrotationRadiusEst = rotationRadiusEst
			bestchainSagCorrectionEst = chainSagCorrectionEst
			bestleftChainToleranceEst = leftChainToleranceEst
			bestrightChainToleranceEst = rightChainToleranceEst
			bestleftMotorXEst = leftMotorXEst
			bestleftMotorYEst = leftMotorYEst
			bestrightMotorXEst = rightMotorXEst
			bestrightMotorYEst = rightMotorYEst
			bestLChainErrorHole1 = LChainErrorHole1
			bestLChainErrorHole2 = LChainErrorHole2
			bestLChainErrorHole3 = LChainErrorHole3
			bestLChainErrorHole4 = LChainErrorHole4
			bestRChainErrorHole1 = RChainErrorHole1
			bestRChainErrorHole2 = RChainErrorHole2
			bestRChainErrorHole3 = RChainErrorHole3
			bestRChainErrorHole4 = RChainErrorHole4

			#report better findings
			distanceBetweenMotors = math.sqrt( math.pow(leftMotorXEst-rightMotorXEst,2)+math.pow(leftMotorYEst-rightMotorYEst,2))
			print "---------------------------------------------------------------------------------------------"
			print "N: " + str(n) + ", Error Magnitude: " + str(round(bestErrorMagnitude, 3)) + ", MotorSpacingX: "+str(distanceBetweenMotors)+", Rotation Disk Radius: " + str(round(bestrotationRadiusEst, 3)) + ", Chain Sag Correction Value: " + str(round(bestchainSagCorrectionEst, 6)) + ", Left Chain:"+str(round(bestleftChainToleranceEst,7))+", Right Chain:"+str(round(bestrightChainToleranceEst,7))
			print "leftMotorX: "+str(bestleftMotorXEst) + ", leftMotorY: "+str(bestleftMotorYEst)
			print "rightMotorX: "+str(bestrightMotorXEst)+", rightMotorY:"+str(bestrightMotorYEst)
			print "  LChain Error Hole 1: " + str(round(bestLChainErrorHole1,4)) + ", LChain Error Hole 2: " + str(round(bestLChainErrorHole2,4)) + ", LChain Error Hole 3: " + str(round(bestLChainErrorHole3,4)) + ", LChain Error Hole 4: " + str(round(bestLChainErrorHole4,4))
			print "  RChain Error Hole 1: " + str(round(bestRChainErrorHole1,4)) + ", RChain Error Hole 2: " + str(round(bestRChainErrorHole2,4)) + ", RChain Error Hole 3: " + str(round(bestRChainErrorHole3,4)) + ", RChain Error Hole 4: " + str(round(bestRChainErrorHole4,4))
			print "  RMS Error Hole 1: "+str(round(math.sqrt(math.pow(bestLChainErrorHole1,2)+math.pow(bestRChainErrorHole1,2)),4))
			print "  RMS Error Hole 2: "+str(round(math.sqrt(math.pow(bestLChainErrorHole2,2)+math.pow(bestRChainErrorHole2,2)),4))
			print "  RMS Error Hole 3: "+str(round(math.sqrt(math.pow(bestLChainErrorHole3,2)+math.pow(bestRChainErrorHole3,2)),4))
			print "  RMS Error Hole 4: "+str(round(math.sqrt(math.pow(bestLChainErrorHole4,2)+math.pow(bestRChainErrorHole4,2)),4))
			#x = raw_input("")

	#pick a random variable to adjust
	#direction = random.randint(0,1)  # determine if its an increase or decrease
	adjustValue = random.randint(-100, 100)
	Completed = False # trick value to enter while
	while (Completed == False):
		picked = random.randint(1,6)
		tscaleMultiplier = scaleMultiplier * float(adjustValue)/100.0 #avoid altering scaleMultiplier
		if (picked == 1):
			motor = random.randint(0,2) #pick which motor (or both) to adjust
			if (motor == 0 and adjustMotorTilt): #tilt left motor up or down
				leftMotorYEst += motorYcoordCorrectionScale*tscaleMultiplier
				# because left motor mover, change x coordinate of right motor to keep distance between motors fixed
				rightMotorXEst = leftMotorXEst - math.sqrt(math.pow(desiredMotorSpacing,2) - math.pow((leftMotorYEst-rightMotorYEst),2))
				Completed = True
			if (motor == 1 and adjustMotorTilt ): #tilt right motor up or down
				rightMotorYEst += motorYcoordCorrectionScale*tscaleMultiplier
				# because right motor mover, change x coordinate of left motor to keep distance between motors fixed
				leftMotorXEst = rightMotorXEst - math.sqrt(math.pow(desiredMotorSpacing,2) - math.pow((rightMotorYEst-leftMotorYEst),2))
				Completed = True
			if (motor ==2 and adjustMotorYcoord): # moves both motors up or down in unison
				leftMotorYEst += motorYcoordCorrectionScale*tscaleMultiplier
				rightMotorYEst += motorYcoordCorrectionScale*tscaleMultiplier
				Completed = True
		if (picked == 2 and adjustMotorXcoord): #all x moves are in unison to keep distance between motors fixed
			leftMotorXEst += errorMagnitude*motorXcoordCorrectionScale*tscaleMultiplier
			rightMotorXEst += errorMagnitude*motorXcoordCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 3 and adjustChainSag):
			chainSagCorrectionEst += errorMagnitude*chainSagCorrectionCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 4 and adjustRotationalRadius): #recommend against this one if at all possible
			rotationRadiusEst += errorMagnitude*rotationRadiusCorrectionScale*tscaleMultiplier
			Completed = True
		if (picked == 5 and adjustChainCompensation):
			leftChainToleranceEst += errorMagnitude*chainCompensationCorrectionScale*tscaleMultiplier
			#make sure chain tolerance doesn't go over 1 (i.e., chain is shorter than should be.. this can cause optimization to go bonkers)
			if (leftChainToleranceEst>= 1.0):
				leftChainToleranceEst = 1.0
			Completed = True
		if (picked == 6 and adjustChainCompensation):
			rightChainToleranceEst += errorMagnitude*chainCompensationCorrectionScale*tscaleMultiplier
			#make sure chain tolerance doesn't go over 1 (i.e., chain is shorter than should be.. this can cause optimization to go bonkers)
			if (rightChainToleranceEst>= 1.0):
				rightChainToleranceEst = 1.0
			Completed = True

	#make sure values aren't too far out of whack.
	if (False): # will never be run if False
		if (rotationRadiusEst<desiredRotationalRadius-2):
			rotationRadiusEst = desiredRotationalRadius-2
		if (rotationRadiusEst>desiredRotationalRadius+2):
			rotationRadiusEst = desiredRotationalRadius+2
		if (chainSagCorrectionEst < 10):
			chainSagCorrectionEst = 10
		if (chainSagCorrectionEst > 60):
			chainSagCorrectionEst = 60


print "---------------------------------------------------------------------------------------------"
if n == numberOfIterations:
	print "Machine parameters could no solve to your desired tolerance, but did you really expect to be able to?"
else:
	print "Solved!"
print "---------------------------------------------------------------------------------------------"

x="n"
while (x<>"x"):
   x = raw_input ("Press 'x' to exit")


#this was here for testing.  typed a lot so I'm saving it.
#print "leftMotorDistanceHole1: "+str(leftMotorDistanceHole1)+", leftMotorDistanceHole2: "+str(leftMotorDistanceHole2)+", leftMotorDistanceHole3: "+str(leftMotorDistanceHole3)+", leftMotorDistanceHole4: "+str(leftMotorDistanceHole4)
#print "rightMotorDistanceHole1: "+str(rightMotorDistanceHole1)+", rightMotorDistanceHole2: "+str(rightMotorDistanceHole2)+", rightMotorDistanceHole3: "+str(rightMotorDistanceHole3)+", leftMotorDistanceHole4: "+str(rightMotorDistanceHole4)
#print "leftChainAngleHole1: "+str(leftChainAngleHole1)+", leftChainAngleHole2: "+str(leftChainAngleHole2)+", leftChainAngleHole3: "+str(leftChainAngleHole3)+", leftChainAngleHole4: "+str(leftChainAngleHole4)
#print "rightChainAngleHole1: "+str(rightChainAngleHole1)+", rightChainAngleHole2: "+str(rightChainAngleHole2)+", rightChainAngleHole3: "+str(rightChainAngleHole3)+", rightChainAngleHole4: "+str(rightChainAngleHole4)
#print "leftChainSag1: "+str(leftChainSag1)+", leftChainSag2: "+str(leftChainSag2)+", leftChainSag3: "+str(leftChainSag3)+", leftChainSag4: "+str(leftChainSag4)
#print "rightChainSag1: "+str(rightChainSag1)+", rightChainSag2: "+str(rightChainSag2)+", rightChainSag3: "+str(rightChainSag3)+", rightChainSag4: "+str(rightChainSag4)
