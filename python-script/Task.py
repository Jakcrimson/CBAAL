"""
@author : Pierre Lague
"""
import numpy as np

"""
For general purpose of object oriented programming only.
"""
class Task():
    def __init__(self, task_num) -> None:
        self.position = np.random.uniform(low=0, high=1, size=(task_num, 2))

    def get_position(self):
        return self.position