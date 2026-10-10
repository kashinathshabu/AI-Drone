#import drone_movements as drone
from pymavlink import mavutil
import time
master = mavutil.mavlink_connection('tcp:localhost:5763')
#vehicle=drone.master
####################################################################################
# Function to send velocity command
def send_body_ned_velocity(velocity_x, velocity_y, velocity_z):
    msg = master.mav.set_position_target_local_ned_encode(
        0, 0, 0,  # time_boot_ms, target_system, target_component
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame
        0b0000111111000111,  # type_mask (only velocities enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # m/s
        0, 0, 0,  # x, y, z acceleration (not used)
        0, 0)  # yaw, yaw_rate (not used)
    master.mav.send(msg)

def condition_yaw_slow(yaw_rate , side):

    msg = master.mav.command_long_encode(
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
        0,  # confirmation
        yaw_rate,  # param 1, yaw angle (not used)
        10,  # param 2, yaw speed (not used)
        side,  # param 3, direction -1 = ccw, 1 = cw
        1,  # param 4, relative or absolute (relative in this case)
        0, 0, 0  # param 5 ~ 7 not used
        )  # param 8, yaw rate
    master.mav.send(msg)


##########################################################################
#send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
def d_m_left():
    send_body_ned_velocity(0, -0.2, 0)
    time.sleep(1)
def d_m_right():
    send_body_ned_velocity(0, 0.2, 0)
    time.sleep(1)
def d_m_foreward():
    send_body_ned_velocity(0.3, 0, 0)
    time.sleep(1)
def d_m_backward():
    send_body_ned_velocity(-0.3, 0, 0)
    time.sleep(1)
def d_m_up():
    send_body_ned_velocity(0, 0, 0.2)
    time.sleep(1)
def d_m_down():
    send_body_ned_velocity(0, 0, -0.2)
    time.sleep(1)

    

def d_t_left():
    # Turn the drone left slowly at 1 degree/left
    condition_yaw_slow(5 ,-1)
    time.sleep(1)

def d_t_right():
    # Turn the drone left slowly at 1 degree/right
    condition_yaw_slow(5,1)
    time.sleep(1)

##########################################################################

