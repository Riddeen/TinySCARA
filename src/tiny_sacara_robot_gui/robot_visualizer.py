import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib._enums import JoinStyle


#Arm geometry
ORIGIN = np.array([0,0])
L1 = 20
L2 = 20
L3 = 5
ARM_LINK_LENGTH = np.array([L1,L2,L3])

class RobotPlot:
    def __init__(self):
        self._origin: np.array[float] = ORIGIN
        self._arm_geometry: list[float] = ARM_LINK_LENGTH
        self.fig = plt.figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(111, aspect="equal", autoscale_on=False, xlim=(-50,50), ylim=(-50,50))

        # Major ticks every 10, minor ticks every 1
        self.major_ticks = np.arange(-50, 51, 10)
        self.minor_ticks = np.arange(-50, 51, 2)

        self.ax.set_xticks(self.major_ticks)
        self.ax.set_xticks(self.minor_ticks, minor=True)
        self.ax.set_yticks(self.major_ticks)
        self.ax.set_yticks(self.minor_ticks, minor=True)

        # And a corresponding grid
        self.ax.grid(which='minor', alpha=0.2)
        self.ax.grid(which='major', alpha=0.5)
        self.ax.set_axisbelow(True)


    def compute_position(self, arm_geometry: np.array, joints_value: np.array=([0,0,0]), origin: np.array=([0,0])):
        a = origin
        b = np.array([arm_geometry[0] * np.cos(joints_value[0]), arm_geometry[0] * np.sin(joints_value[0])])
        c = np.array([arm_geometry[0] * np.cos(joints_value[0]) 
                    + arm_geometry[1] * np.cos(joints_value[0] + joints_value[1]),
                    arm_geometry[0] * np.sin(joints_value[0])
                    + arm_geometry[1] * np.sin(joints_value[0] + joints_value[1])])
        d = np.array([arm_geometry[0] * np.cos(joints_value[0]) 
                    + arm_geometry[1] * np.cos(joints_value[0] + joints_value[1])
                    + arm_geometry[2] * np.cos(joints_value[0] + joints_value[1] + joints_value[2]),
                    arm_geometry[0] * np.sin(joints_value[0])
                    + arm_geometry[1] * np.sin(joints_value[0] + joints_value[1])
                    + arm_geometry[2] * np.sin(joints_value[0] + joints_value[1] + joints_value[2])])

        jointX = np.array([a[0],b[0],c[0],d[0]])
        jointY = np.array([a[1],b[1],c[1],d[1]])
        return jointX, jointY


    def update_pose(self, joints_value: np.array):
        plt.clf()
        jointX, jointY = self.compute_position(self._arm_geometry, joints_value, self._origin)
        plt.xlim(-50,50)
        plt.ylim(-50,50)
        plt.plot(jointX, jointY, lw=12, color='tab:blue', solid_capstyle="round")
        plt.plot(jointX, jointY, 'o', color='tab:red', markersize=8)
        plt.show()

        # for tenth in range(100):
        #     jointX, jointY = self.compute_position(ARM_LINK_LENGTH, ([tenth/20,tenth/50,-tenth/100]), ORIGIN)
        #     plt.xlim(-50,50)
        #     plt.ylim(-50,50)
        #     plt.plot(jointX, jointY, lw=12, color='tab:blue', solid_capstyle="round")
        #     plt.plot(jointX, jointY, 'o', color='tab:red', markersize=8)
        #     plt.draw()
        #     plt.pause(0.01)
        # plt.show()

if __name__ == "__main__":
    robot = RobotPlot()
    robot.update_pose([0,1,0])