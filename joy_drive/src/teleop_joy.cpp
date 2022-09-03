#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/String.h>


class TeleopTurtle
{
public:

  TeleopTurtle();

private:

  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);
  ros::NodeHandle nh_;

  int linear_x_,linear_y_, angular_;
  double l_scale_, a_scale_;
  ros::Publisher vel_pub_;
  ros::Subscriber joy_sub_;
  ros::Publisher bot_vel_pub;
};


TeleopTurtle::TeleopTurtle():

  linear_x_(1),
  linear_y_(1),
  angular_(1)

{

  nh_.param("axis_linear_x", linear_x_, linear_x_);
  nh_.param("axis_linear_y", linear_y_, linear_y_);
  nh_.param("axis_angular", angular_, angular_);
  nh_.param("scale_angular", a_scale_, a_scale_);
  nh_.param("scale_linear", l_scale_, l_scale_);

  vel_pub_ = nh_.advertise<geometry_msgs::Twist>("turtle1/cmd_vel", 1);
  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 10, &TeleopTurtle::joyCallback, this);
  bot_vel_pub = nh_.advertise<geometry_msgs::Twist>("drive_bot", 10);
}

void TeleopTurtle::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
  geometry_msgs::Twist twist;

  twist.angular.z = a_scale_*joy->axes[angular_];
  twist.linear.x = l_scale_*joy->axes[linear_x_];
  twist.linear.y = l_scale_*joy->axes[linear_y_];
  vel_pub_.publish(twist);
  bot_vel_pub.publish(twist);
}


int main(int argc, char** argv)
{
  ros::init(argc, argv, "teleop_turtle");
  TeleopTurtle teleop_turtle;

  ros::spin();
}