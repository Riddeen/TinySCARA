import numpy as np



class RobotModel:
    def __init__(self, nbr_axis: int):
        self.nbr_axis = nbr_axis
        self.joints: dict[Joint] = {}
        self. __populate_joint_array()

    def __populate_joint_array(self):
        for i in range(self.nbr_axis):
            self.joints[str(i+1)] = Joint()



class Joint:
    def __init__(self, angle=0.0, max_angle=float("inf"), min_angle=float("-inf")):
        self.__angle: float = angle
        self.__max_angle: float = max_angle
        self.__min_angle: float = min_angle

    def get_angle(self) -> float:
        """ Returns the joint angle in radian (rad)
        """
        return self.__angle

    def get_angle_degree(self) -> float:
        """ Returns the joint angle in degree (°)
        """
        return self.__angle * 180 / np.pi

    def set_angle(self, angle):
        """ Set the joint angle in radian (rad)

        raises:
            ValueError: if angle is not a number.       
        """
        try:
            self.__condition_angle(float(angle))
        except ValueError:
            print("ERROR: argument is not a number")

    def set_angle_degree(self, angle):
        """ Set the joint angle in degree (°)

        raises:
            ValueError: if angle is not a number.       
        """
        try:
            self.__condition_angle(float(angle) * np.pi / 180)
        except ValueError:
            print("ERROR: argument is not a number")

    def __condition_angle(self, angle):
        if angle > self.__max_angle:
            self.__angle = self.__max_angle
        elif angle < self.__min_angle:
            self.__angle = self.__min_angle
        else:
            self.__angle = angle 



if __name__ == "__main__":
    robot_model = RobotModel(3)
    print(robot_model.joints["1"].get_angle())
    robot_model.joints["1"].set_angle(180)
    print(robot_model.joints["1"].get_angle())
    robot_model.joints["1"].set_angle_degree(180)
    print(robot_model.joints["1"].get_angle())