from controller import Robot

robot = Robot()

timestep = int(robot.getBasicTimeStep())

last_error=I=D=P=error=0
kp=2
ki=0
kd=0.3

updateCalibration = 15
max_speed = 4.5

#motor
left_motor = robot.getDevice('wheel1')
right_motor = robot.getDevice('wheel2')
back_left_motor = robot.getDevice('wheel3')
back_right_motor = robot.getDevice('wheel4')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
back_left_motor.setPosition(float('inf'))
back_right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
back_left_motor.setVelocity(0.0)
back_right_motor.setVelocity(0.0)

#Ir sensor
rightIR = robot.getDevice('ds_right')
rightIR.enable(updateCalibration)
midIR = robot.getDevice('ds_mid')
midIR.enable(updateCalibration)
leftIR = robot.getDevice('ds_left')
leftIR.enable(updateCalibration)

#mainloop
while robot.step(timestep) != -1:

    #functions
    rightIR_val = rightIR.getValue()
    midIR_val = midIR.getValue()
    leftIR_val = leftIR.getValue()

    print("left: {} mid: {} right: {}".format(leftIR_val, midIR_val, rightIR_val))
    
    left_speed = max_speed
    right_speed = max_speed

    if leftIR_val < 350 and rightIR_val < 350 and midIR_val >= 350:
        error=0

    elif leftIR_val < 350 and rightIR_val >= 350 and midIR_val >= 350:
        error=-1

    elif leftIR_val >= 350 and rightIR_val < 350 and midIR_val >= 350:
        error=1


    elif leftIR_val >= 350 and rightIR_val < 350 and midIR_val < 350:
        error=2

    elif leftIR_val < 350 and rightIR_val >= 350 and midIR_val < 350:
        error=-2

    P=error
    print("P: {}".format(P))
    I=error+I
    print("I: {}".format(I))
    D=error-last_error
    print("D: {}".format(D))
    balance=int((kp*P)+(ki*I)+(kd*D))
    print("balamce: {}".format(balance))
    last_error=error   
    print("last_error: {}".format(last_error))
    
    left_Speed=max_speed-balance
    print("left_Speed: {}".format(left_Speed))
    right_Speed=max_speed+balance
    print("right_Speed: {}".format(right_Speed))
    #processing of sensor data

    if left_Speed> max_speed :
        left_motor.setVelocity(left_Speed)
        right_motor.setVelocity(0)
        back_left_motor.setVelocity(left_Speed)
        back_right_motor.setVelocity(0) 
    if right_Speed> max_speed :
        left_motor.setVelocity(0)
        right_motor.setVelocity(right_Speed)
        back_left_motor.setVelocity(0)
        back_right_motor.setVelocity(right_Speed)  
    if left_Speed < 0:
        left_motor.setVelocity(0)
        right_motor.setVelocity(right_Speed)
        back_left_motor.setVelocity(0)
        back_right_motor.setVelocity(right_Speed)

    if right_Speed < 0:
        left_motor.setVelocity(left_Speed)
        right_motor.setVelocity(0)
        back_left_motor.setVelocity(left_Speed)
        back_right_motor.setVelocity(0)
    if right_Speed ==  max_speed:
        left_motor.setVelocity(left_Speed)
        right_motor.setVelocity(right_Speed)
        back_left_motor.setVelocity(left_Speed)
        back_right_motor.setVelocity(right_Speed)

    pass