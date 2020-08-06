import numpy as np


def check_data_color(ele_or_ver, colors):
    num_of_ver = len(ele_or_ver)/3
    num_of_colors = len(colors)
    if num_of_ver != num_of_colors:
        print("Error: Invalid data. Number of colors data unmatch.")
        return False
    else:
        return True

def check_vertices(ver):
    if len(ver)%3 != 0:
        print("Error: Vertices data invalid.")
        return False
    else:
        return True

def check_faces(fa):
    if len(fa)%3 != 0:
        print("Error: Elements data invalid.")
        return False
    else:
        return True