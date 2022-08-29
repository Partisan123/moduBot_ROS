#!/usr/bin/env python3

import rospy
import time
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty



def poseCallback(pose_message):
    global x
    global y, yaw
    
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta
    
def move(vel_pub , speed , dist, is_fwd):
        
    #declare a Twist message to send velocity commands
    vel_msg = Twist()
    
    #get current location
    global x , y
   
    x0 = x 
    y0 = y
    

    if(is_fwd):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    dist_moved = 0.0
    loop_rate = rospy.Rate(20) #freq of publish 20Hz
    
    while True:
        rospy.loginfo_once("Bot moves forward")
        vel_pub.publish(vel_msg)
        loop_rate.sleep()
        # print(x , y)
        dist_moved = abs(math.sqrt(((x-x0)**2) + ((y-y0)**2)))
        print(dist_moved)
        if not (dist_moved < dist):
            rospy.loginfo("Target reached")
            break
    vel_msg.linear.x = 0
    vel_pub.publish(vel_msg)

def rotate(vel_pub, angular_speed_deg, relative_angle_deg , clockwise):
    
    vel_msg = Twist()

    angular_speed = math.radians(abs(angular_speed_deg))

    if(clockwise):
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)

    loop_rate = rospy.Rate(20)
    t0 = rospy.Time.now().to_sec()

    while True:
        rospy.loginfo_once("Bot Rotates")
        vel_pub.publish(vel_msg)

        t1 = rospy.Time.now().to_sec()
        current_deg = (t1-t0)*angular_speed_deg
        loop_rate.sleep()
        print(current_deg)
        if(current_deg >relative_angle_deg):
            rospy.loginfo_once("Reached the angle")
            break
    vel_msg.angular.z = 0
    vel_pub.publish(vel_msg) 

def go_to_goal(vel_pub , goal_x , goal_y):
    global x 
    global y , yaw

    vel_msg = Twist()

    while True:
        k_lin = 0.5
        dist = abs(math.sqrt(((goal_x - x)**2) + ((goal_y - y)**2)))
        linear_speed = dist*k_lin

        k_angle = 4.0
        des_angle = math.atan2(goal_y-y, goal_x-x)
        ang_speed = (des_angle-yaw)*k_angle
        print(des_angle)
        vel_msg.linear.x = linear_speed
        vel_msg.angular.z = ang_speed

        vel_pub.publish(vel_msg)

        # print("x=", x, "| y=",y ,"| dist_to_goal: ", dist)

        if(dist < 0.05):
            break
    
def set_Orientation(publisher , speed_deg, desired_angle_deg):
    relative_angle = math.radians(desired_angle_deg) - yaw
    clockwise = 0

    if relative_angle < 0:
        clockwise = 1
    else:
        clockwise = 0
    rel_deg = math.degrees(abs(relative_angle))
    rotate(publisher, speed_deg, rel_deg ,clockwise)

def drive(vel_y, vel_x, ang__vel_z):

    vel_msg = Twist()

    # vel_msg.linear.y = 



if __name__ == '__main__':
    try:
        global x , y 
        rospy.init_node("motion_pose", anonymous=True)

        #declare velocity pub
        cmd_vel_topic = '/turtle1/cmd_vel'
        vel_pub = rospy.Publisher(cmd_vel_topic , Twist , queue_size=10)
        vel_y = rospy.Publisher("/lin_y" , Twist, queue_size=10 )
        vel_x = rospy.Publisher("/lin_x" , Twist, queue_size=10 )
        ang_vel_z = rospy.Publisher("/ang_z" , Twist, queue_size=10 )

        #sub position
        pos_topic = '/turtle1/pose'
        pose_sub = rospy.Subscriber(pos_topic , Pose , poseCallback)
        time.sleep(2)
        
        # Get ROS Params


        # move(vel_pub , 1.0 , 4.0, True)
        # rotate(vel_pub , 30 , 90 , True)
        # go_to_goal(vel_pub,1.0,1.0)
        # set_Orientation(vel_pub ,30 , -180)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated.")

