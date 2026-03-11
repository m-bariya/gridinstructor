from small_net import create_small_net
from visualize import plot_bus_quantities, visualize_network

if __name__ == "__main__":
    """Take a look at the code in small_net.py to understand how you can pass parameters to create the network"""
    net = create_small_net(r=0.05)

    """This line solves the power flow"""
    net.pf()

    """Print the bus voltages from the power flow solution"""
    print("Bus Voltages")
    print(net.buses_t.v_mag_pu)

    """visualize.py contains some plotting utilities - feel free to use them or write your own"""
    plot_bus_quantities(net)
    visualize_network(net)