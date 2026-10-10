#from pymavlink import mavutil
import time
import geo_fence
import drone_movements as drone

reached=False
turns=True
no_turns=False
while(turns):
    
    lat,lon=geo_fence.generate_random_point_in_polygon()
    #drone.set_waypoint(lat,lon,4)
    print("1")
    drone.send_to(lat,lon,6)
    print("2")

    while reached==False:
        drone.check_reached_target(lat,lon,6)
        print("done")
        #hi="hi"

    time.sleep(5)
    no_turns+=1
    if no_turns >=5:
        turns=False