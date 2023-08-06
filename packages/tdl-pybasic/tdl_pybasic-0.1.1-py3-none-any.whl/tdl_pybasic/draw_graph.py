import matplotlib.pyplot as plt

# A list to store numbers
NUMS = []

def store_data(data):
    """
    A function to store data to NUMS, 
        to draw a graph.
    """
    NUMS.append(data)


def draw_graph():
    """
    A function to draw a graph
      using stored data in NUMS.
    """
    global NUMS
    plt.plot(NUMS)
    NUMS = []

