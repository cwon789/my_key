#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32MultiArray

import sys, select, termios, tty

ROSCAR_MAX_ACCELL_VEL = 255
ROSCAR_MAX_STEERING_VEL = 180
BALLSCREW_MAX_VEL = 180

ROSCAR_MIN_ACCELL_VEL = 0
ROSCAR_MIN_STEERING_VEL = 0
BALLSCREW_MIN_VEL = 180

msg = """
Control Your ROSCAR!
---------------------------
Moving around:
 
        w        t
        
   a    s    d   g
      
        x        b

w/x : increase/decrease accell velocity
a/d : increase/decrease steering velocity
t/b : ballscrew control
g   : ballscrew stop

space key, s : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
         key = sys.stdin.read(1)
    else:
        key = ''
        
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(target_accell_vel, target_angular_vel, target_ballscrew_vel):
    return "currently: \n accell vel    %s\n steering vel  %s\n ballscrew vel %s " % (target_accell_vel,target_steering_vel,target_ballscrew_vel)


#def constrain(input, low, high):
#    if input < low:
#        input = low
#    elif input > high:
#        input = high
 #   else:
 #       input = input
 #      
    
 #   return input


#def checkACCELLLimitVelocity(vel):
#    vel = constrain(vel, -ROSCAR_MIN_ACCELL_VEL, ROSCAR_MAX_ACCELL_VEL)
#    return vel

#def checkSTEERINGLimitVelocity(vel):
#    vel = constrain(vel, -ROSCAR_MIN_STEERING_VEL, ROSCAR_MAX_STEERING_VEL)
#    return vel


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    
    
    pub = rospy.Publisher('cmd_vel', Int32MultiArray, queue_size=10)
    rospy.init_node('roscar_teleop',anonymous=True)
    
    teleop_int = Int32MultiArray()
    teleop_int.data = [0,0,0]
    
    status = 0
    target_accell_vel = 0
    target_steering_vel = 0
    target_ballscrew_vel = 0
    
    try:
        print (msg)
        while(1):
            key = getKey()
            if key == 'w' :
                target_accell_vel +=1 
                #target_accell_vel = checkACCELLLimitVelocity(target_accell_vel)
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 'x' :
                target_accell_vel -=1
                #target_accell_vel = checkACCELLLimitVelocity(target_accell_vel)
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 'a' :
                target_steering_vel -=1
                #target_steering_vel = checkSTEERINGLimitVelocity(target_steering_vel)
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 'd' :
                target_steering_vel +=1
                #target_steering_vel = checkSTEERINGLimitVelocity(target_steering_vel)
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 's'  :
                target_accell_vel   = 0
                target_steering_vel  = 0
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
            elif key == 't':
                target_ballscrew_vel +=1
                status +=1
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
            elif key == 'b' :
                target_ballscrew_vel -=1
                status +=1
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
            elif key == 'g' :
                target_ballscrew_vel =0
                status +=1
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
           # elif target_accell_vel > 255 :
           #     target_accell_vel = 254
           # elif target_accell_vel < 0 :
           #     target_accell_vel = 1
            else:
                if (key == '\x03'):
                    break
            if status == 20 :
                print (msg)
                status = 0
                
            teleop_int.data[0] = target_accell_vel
            teleop_int.data[1] = target_steering_vel
            teleop_int.data[2] = target_ballscrew_vel
            pub.publish(teleop_int)
            
    except rospy.ROSInterruptException:
        pass
    
    finally:
        pub.publish(teleop_int)
        
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)







