import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial

class JointStateListener(Node):
    def __init__(self):
        super().__init__('joint_state_listener')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        self.serial_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Change port if needed
        self.last_command = None  # Stores the last sent command

    def joint_state_callback(self, msg):
        positions = msg.position  # Get joint positions
        
        if all(pos == 0.0 for pos in positions):
            if self.last_command != "OPEN":  # Send only if different from last command
                self.serial_port.write(b'OPEN\n')
                self.get_logger().info('Sent: OPEN')
                self.last_command = "OPEN"  # Update last command
        elif all(pos == -0.785 for pos in positions):
            if self.last_command != "CLOSE":  # Send only if different from last command
                self.serial_port.write(b'CLOSE\n')
                self.get_logger().info('Sent: CLOSE')
                self.last_command = "CLOSE"  # Update last command

def main(args=None):
    rclpy.init(args=args)
    node = JointStateListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
