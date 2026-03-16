import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

# ---------------- GPIO PINS ----------------
# Right motor driver
RPWM_R = 18
LPWM_R = 19

# Left motor driver
RPWM_L = 12
LPWM_L = 13

PWM_FREQ = 1000


class MotorController(Node):

    def __init__(self):
        super().__init__('motor_controller')

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(RPWM_R, GPIO.OUT)
        GPIO.setup(LPWM_R, GPIO.OUT)
        GPIO.setup(RPWM_L, GPIO.OUT)
        GPIO.setup(LPWM_L, GPIO.OUT)

        # PWM objects
        self.pwm_r_forward = GPIO.PWM(RPWM_R, PWM_FREQ)
        self.pwm_r_reverse = GPIO.PWM(LPWM_R, PWM_FREQ)

        self.pwm_l_forward = GPIO.PWM(RPWM_L, PWM_FREQ)
        self.pwm_l_reverse = GPIO.PWM(LPWM_L, PWM_FREQ)

        self.pwm_r_forward.start(0)
        self.pwm_r_reverse.start(0)

        self.pwm_l_forward.start(0)
        self.pwm_l_reverse.start(0)

        self.wheel_base = 0.25   # distance between wheels (meters)

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.get_logger().info("Motor controller started")

    def cmd_callback(self, msg):

        v = msg.linear.x
        w = msg.angular.z

        v_left = v - (w * self.wheel_base / 2)
        v_right = v + (w * self.wheel_base / 2)

        self.drive(v_left, v_right)

    def drive(self, left, right):

        left_speed = min(abs(left), 1.0)
        right_speed = min(abs(right), 1.0)

        left_pwm = left_speed * 100
        right_pwm = right_speed * 100
        # LEFT SIDE
        if left > 0:
            print(f"LEFT MOTOR: forward at {left_pwm:.1f}% speed")

            self.pwm_l_forward.ChangeDutyCycle(left_pwm)
            self.pwm_l_reverse.ChangeDutyCycle(0)

        elif left < 0:
            print(f"LEFT MOTOR: reverse at {left_pwm:.1f}% speed")

            self.pwm_l_forward.ChangeDutyCycle(0)
            self.pwm_l_reverse.ChangeDutyCycle(left_pwm)

        else:
            print("LEFT MOTOR: stop")

            self.pwm_l_forward.ChangeDutyCycle(0)
            self.pwm_l_reverse.ChangeDutyCycle(0)


        # RIGHT SIDE
        if right > 0:
            print(f"RIGHT MOTOR: forward at {right_pwm:.1f}% speed")

            self.pwm_r_forward.ChangeDutyCycle(right_pwm)
            self.pwm_r_reverse.ChangeDutyCycle(0)

        elif right < 0:
            print(f"RIGHT MOTOR: reverse at {right_pwm:.1f}% speed")

            self.pwm_r_forward.ChangeDutyCycle(0)
            self.pwm_r_reverse.ChangeDutyCycle(right_pwm)

        else:
            print("RIGHT MOTOR: stop")

            self.pwm_r_forward.ChangeDutyCycle(0)
            self.pwm_r_reverse.ChangeDutyCycle(0)

    def destroy_node(self):
        GPIO.cleanup()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = MotorController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()