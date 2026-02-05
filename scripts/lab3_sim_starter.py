#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Pose, Quaternion
from gazebo_msgs.msg import ModelStates
import tf
import math


class OdometryPublisher:
    def __init__(self):
        rospy.init_node("odometry_publisher", anonymous=True)

        # Publisher to the /custom_odom topic
        self.odom_pub = rospy.Publisher("/custom_odom", Odometry, queue_size=10)

        # Subscriber to the /gazebo/model_states topic.
        # see https://docs.ros.org/en/noetic/api/gazebo_msgs/html/msg/ModelStates.html
        self.model_states_sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.model_states_callback)

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.vx = 0.0
        self.vy = 0.0
        self.vth = 0.0

        self.current_time = rospy.Time.now()
        self.last_time = rospy.Time.now()

    def model_states_callback(self, msg):
        self.vx = msg.twist[1].linear.x
        self.vy = msg.twist[1].linear.y
        self.vth = msg.twist[1].angular.z

    def update_odometry(self):
        self.current_time = rospy.Time.now()
        dt = (self.current_time - self.last_time).to_sec()

        ######### Your code starts here #########
        # add odometry equations to calculate robot's self.x, self.y, self.theta given encoder values
        # Update theta first
        delta_theta = self.vth * dt
        theta_mid = self.theta + delta_theta / 2.0

        # Calculate change in position using mid-point theta for better accuracy
        delta_theta = self.vth *dt
        delta_x = (self.vx * math.cos(self.theta)* dt) #change in x
        delta_y = (self.vx * math.sin(self.theta)* dt) #change in y
        self.theta += delta_theta
        self.x+=delta_x# update both and theta
        self.y+=delta_y
        print(f"x: {self.x:.2f}, y: {self.y:.2f}, theta: {self.theta:.2f}")
        ######### Your code ends here #########
        
        odom_quat = tf.transformations.quaternion_from_euler(0, 0, self.theta)

        odom = Odometry()
        odom.header.stamp = self.current_time
        odom.header.frame_id = "odom"

        odom.pose.pose = Pose()
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = Quaternion(*odom_quat)

        odom.child_frame_id = "base_link"
        odom.twist.twist = Twist()
        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.linear.y = self.vy
        odom.twist.twist.angular.z = self.vth


        self.odom_pub.publish(odom)
        self.last_time = self.current_time

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            self.update_odometry()
            rate.sleep()


if __name__ == "__main__":
    try:
        print("Publishing odometry under /custom_odom...")
        odom_pub = OdometryPublisher()
        odom_pub.run()
    except rospy.ROSInterruptException:
        pass
