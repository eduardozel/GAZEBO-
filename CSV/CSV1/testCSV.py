import math
import rospy
from clover import srv
from std_srvs.srv import Trigger
import csv

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)

def navigate_wait(x=0, y=0, z=1, yaw=float('nan'), speed=1, frame_id='body', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

rospy.init_node('test_CSV')
navigate_wait(z=0.5, auto_arm=True)
rospy.sleep(2)
# Использование конструкции with…as позволяет программисту быть уверенным, 
# что файл будет закрыт, даже если при выполнении кода произойдет какая-то ошибка.
with open('testCSV.csv', 'r', newline='') as csvfile:
    csvDATA = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for data in csvDATA:
        x=data[0]
        y=data[1]
        z=data[2]
        print('x='+f'{x:.1f}'+' y='+f'{y:.1f}'+' z='+f'{z:.1f}')
        navigate_wait(  x, y, z)
        rospy.sleep(2)
rospy.sleep(5)
navigate_wait( frame_id='aruco_map')
rospy.sleep(5)
land()
