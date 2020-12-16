#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


#########################################
class teleop(object):
    """
    teleoperation
    """
    def __init__(self):

        self.sub_joy   = rospy.Subscriber("joy", Joy , self.joy_callback , queue_size=1)
        self.pub_cmd   = rospy.Publisher("ctl_ref", Twist , queue_size=1  ) 

        self.max_vel  = rospy.get_param('~max_vel',   6.0) # Max linear velocity (m/s)
        self.max_volt = rospy.get_param('~max_volt',  8)   # Max voltage is set at 6 volts   
        self.maxStAng = rospy.get_param('~max_angle', 40)  # Supposing +/- 40 degrees max for the steering angle
        self.cmd2rad   = self.maxStAng*2*3.1416/360     

    ####################################### 
        
    def joy_callback( self, joy_msg ):
        """ """
    
        propulsion_user_input = joy_msg.axes[4]    # Up-down Right joystick 
        #if (-5000 <= propulsion_user_input <= 5000)
        #    propulsion_user_input = 0

        steering_user_input   = joy_msg.axes[0]    # Left-right left joystick
        
        self.cmd_msg = Twist()             
                
        # Software deadman switch
        #If L1 is active 
        if (joy_msg.buttons[4]):
            
            #If R1 is active 
            if (joy_msg.buttons[5]):
                
                #If B button and R1 are active
                if (joy_msg.buttons[1]):
                    # Template
                    self.cmd_msg.linear.x  = 0
                    self.cmd_msg.angular.z = 0
                    self.cmd_msg.linear.z  = 8 # Control mode

                #If A button and R1 are active
                elif (joy_msg.buttons[0]):
                    # Template
                    self.cmd_msg.linear.x  = 0
                    self.cmd_msg.angular.z = 0
                    self.cmd_msg.linear.z  = 9 # Control mode

                #If X button and R1 are active
                elif (joy_msg.buttons[2]):
                    # Template
                    self.cmd_msg.linear.x  = 0
                    self.cmd_msg.angular.z = 0
                    self.cmd_msg.linear.z  = 10 # Control mode

                #If X button and R1 are active
                elif (joy_msg.buttons[3]):
                    # Template
                    self.cmd_msg.linear.x  = 0
                    self.cmd_msg.angular.z = 0
                    self.cmd_msg.linear.z  = 11 # Control mode
                
                #If only R1 is active
                else:
                    # Template
                    self.cmd_msg.linear.x  = propulsion_user_input
                    self.cmd_msg.angular.z = 0
                    self.cmd_msg.linear.z  = 7 # Control mode
                    
            # Defaults operation
            # No active button
            else:
                # Closed-loop velocity, Open-loop steering
                self.cmd_msg.linear.x  = propulsion_user_input * self.max_vel #[m/s]
                self.cmd_msg.angular.z = steering_user_input * self.cmd2rad
                self.cmd_msg.linear.z  = 0  # Control mode
        
        # Deadman is un-pressed
        else:
            
            self.cmd_msg.linear.x = 0 
            self.cmd_msg.linear.y = 0
            self.cmd_msg.linear.z = -1            
            self.cmd_msg.angular.x = 0
            self.cmd_msg.angular.y = 0
            self.cmd_msg.angular.z = 0 


        # Publish cmd msg
        self.pub_cmd.publish( self.cmd_msg )
            

#########################################
if __name__ == '__main__':
    
    rospy.init_node('teleop',anonymous=False)
    node = teleop()
    rospy.spin()

