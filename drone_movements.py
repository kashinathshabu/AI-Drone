
from pymavlink import mavutil
import math
import time

# Set up connection to the simulator (SITL)

#master = mavutil.mavlink_connection('udp:192.168.1.4:14550')  # ==> mobile ip
master = mavutil.mavlink_connection('tcp:localhost:5763') # ==> drone stimulator
#master = mavutil.mavlink_connection('udp:192.168.1.4:14550') #  ==> pg ip

#########################################################################################################


def send_command():
    # Send command to arm the drone
    master.arducopter_arm()
    print("Arming Pixhawk")

def disarm_drone():
    # Send command to disarm the drone
    master.arducopter_disarm()
    print("Disarming Pixhawk")

def takeoff(altitude):
    # Command drone to take off to a specified altitude
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, altitude)
    print(f"Taking off to {altitude} meters")

def land():
    # Command drone to land
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)
    print("Landing")


def send_to(latitude, longitude, altitude):   
    type_mask = (mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
             mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
             mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
             mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
             mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
             mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
             mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE |
             mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE)

        # Create MAVLink GPS message
    msg = master.mav.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        master.target_system, master.target_component, # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000000111000111, #   [0b0000111111000111] type_mask (only speeds enabled)
        int(latitude * 1e7), # lat_int - X Position in WGS84 frame in 1e7 * meters
        int(longitude * 1e7), # lon_int - Y Position in WGS84 frame in 1e7 * meters
        altitude, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
        1, # X velocity in NED frame in m/s
        1, # Y velocity in NED frame in m/s
        0, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

    # send command to vehicle
    master.mav.send(msg)
    #master.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GENERIC, mavutil.mavlink.MAV_AUTOPILOT_GENERIC, 0, 0, 0)




def get_current_location():

    try:
        # Fetch current drone state
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            # Convert from 1E7 degrees to degrees for latitude and longitude
            current_lat = msg.lat / 1e7
            current_lon = msg.lon / 1e7
            # Convert from mm to meters for altitude
            current_alt = msg.alt / 1000.0
            return (current_lat, current_lon, current_alt)
        else:
            print("No position information could be fetched.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def check_reached_target(latitude, longitude, altitude, tolerance=1.0):


    # Fetch current drone state
    while True:
        # Get current position
        #print("1")
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        current_lat = msg.lat / 1e7
        current_lon = msg.lon / 1e7
        current_alt = msg.alt / 1000.0  # Convert from mm to m

        # Calculate the distance to the target
        distance = get_distance_metres(current_lat, current_lon, latitude, longitude)
        #print("8")
        # Check if the current position is within the tolerance of the target position
        if distance <= tolerance and abs(current_alt - altitude) <= tolerance:
            return True
        else:
            return False

        time.sleep(2)  # Sleep for a short time to prevent excessive CPU usage

def get_distance_metres(lat1, lon1, lat2, lon2):

    from math import radians, cos, sin, asin, sqrt

    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r * 1000  # Convert to meters


def set_waypoint( latitude, longitude, altitude):

    # Convert latitude and longitude to MAVLink format (degrees * 1E7)
    lat = int(latitude * 1e7)
    lon = int(longitude * 1e7)

    # Send the command to the drone
    master.mav.mission_item_send(
        master.target_system,
        master.target_component,
        0,  # Sequence number
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # The coordinate frame
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,  # The command id
        2,  # Current waypoint, 2 means this is the mission's target
        0,  # Autocontinue to next waypoint
        0,  # Param1, Hold time in decimal seconds
        0,  # Param2, Acceptance radius in meters
        0,  # Param3, 0 to pass through the WP, if > 0 radius in meters to pass by WP
        math.nan,  # Param4, Desired yaw angle at waypoint (NaN for don't care)
        lat,  # X, latitude
        lon,  # Y, longitude
        altitude  # Z, altitude
    )

    print(f"Waypoint set to latitude {latitude}, longitude {longitude}, altitude {altitude}")

send_command()
takeoff(2)
set_waypoint(4,6,4)

'''x,y,z=get_current_location()
print(x , y, z)
print(check_reached_target(x,y,z))'''