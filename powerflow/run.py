from small_net import create_small_net
from visualize import plot_network_results

if __name__ == "__main__":
    net = create_small_net(r=0.05)
    net.pf()
    print("Bus Voltages")
    print(net.buses_t.v_mag_pu)
    plot_network_results(net)
    import pdb; pdb.set_trace()