import networkx as nx

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

def plot_bus_quantities(n, snapshot=0):
    """
    Plot four bar charts in one figure:
        1) Voltage magnitude
        2) Voltage angle
        3) Real power injection
        4) Reactive power injection

    Bus order:
        PV (generator buses) -> Slack -> PQ (load buses)
    """

    # ----------------------------
    # Voltage data
    # ----------------------------
    v_mag = n.buses_t.v_mag_pu.iloc[snapshot]
    v_ang = n.buses_t.v_ang.iloc[snapshot]

    # ----------------------------
    # Power injections
    # ----------------------------
    p_inj = pd.Series(0.0, index=n.buses.index)
    q_inj = pd.Series(0.0, index=n.buses.index)

    # generators
    if len(n.generators) > 0:
        p_gen = n.generators_t.p.iloc[snapshot]
        q_gen = n.generators_t.q.iloc[snapshot]

        for g, p in p_gen.items():
            bus = n.generators.loc[g, "bus"]
            p_inj[bus] += p

        for g, q in q_gen.items():
            bus = n.generators.loc[g, "bus"]
            q_inj[bus] += q

    # loads
    if len(n.loads) > 0:
        p_load = n.loads_t.p.iloc[snapshot]
        q_load = n.loads_t.q.iloc[snapshot]

        for l, p in p_load.items():
            bus = n.loads.loc[l, "bus"]
            p_inj[bus] -= p

        for l, q in q_load.items():
            bus = n.loads.loc[l, "bus"]
            q_inj[bus] -= q

    # ----------------------------
    # Bus type classification
    # ----------------------------
    slack_buses = n.buses.index[n.buses.control == "Slack"].tolist()
    pv_buses = n.buses.index[n.buses.control == "PV"].tolist()
    pq_buses = n.buses.index[n.buses.control == "PQ"].tolist()

    ordered_buses = pv_buses + slack_buses + pq_buses

    # reorder quantities
    v_mag = v_mag[ordered_buses]
    v_ang = v_ang[ordered_buses]
    p_inj = p_inj[ordered_buses]
    q_inj = q_inj[ordered_buses]

    x = np.arange(len(ordered_buses))

    # ----------------------------
    # Plot
    # ----------------------------
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True)

    # voltage magnitude axis limits should be between 0.9 and 1.1
    axs[0,0].set_ylim(0.9, 1.1)
    axs[0,0].bar(x, v_mag)
    axs[0,0].set_title("Voltage Magnitude [pu]")

    axs[0,1].bar(x, v_ang)
    axs[0,1].set_title("Voltage Angle [rad]")

    axs[1,0].bar(x, p_inj)
    axs[1,0].set_title("Real Power Injection P [MW]")

    axs[1,1].bar(x, q_inj)
    axs[1,1].set_title("Reactive Power Injection Q [MVAr]")

    for ax in axs.flat:
        ax.grid(True, alpha=0.3)

    pv_buses = [f"{bus} (PV)" for bus in pv_buses]
    slack_buses = [f"{bus} (Slack)" for bus in slack_buses]
    pq_buses = [f"{bus} (PQ)" for bus in pq_buses]
    bus_labels = pv_buses + slack_buses + pq_buses
    plt.xticks(x, bus_labels)

    plt.suptitle("Power Flow Results")
    plt.tight_layout()
    plt.show()

def visualize_network(n):
    """
    Node size = voltage magnitude, color = angle, line width = real power flow.
    """

    # bus locations
    bus_coords = {bus: (np.random.rand(), np.random.rand()) for bus in n.buses.index}

    # voltages
    snapshot = 0
    v_mag = n.buses_t.v_mag_pu.iloc[snapshot]
    v_ang = n.buses_t.v_ang.iloc[snapshot]

    # get power injections at each bus
    p_inj = pd.Series(0.0, index=n.buses.index)
    q_inj = pd.Series(0.0, index=n.buses.index)

    # generators
    if len(n.generators) > 0:
        p_inj_gen = n.generators_t.p.iloc[snapshot]
        q_inj_gen = n.generators_t.q.iloc[snapshot]
        for gen, p in p_inj_gen.items():
            bus = n.generators.loc[gen, "bus"]
            p_inj[bus] += p
        for gen, q in q_inj_gen.items():
            bus = n.generators.loc[gen, "bus"]
            q_inj[bus] += q

    # Loads
    if len(n.loads) > 0:
        p_load = n.loads_t.p.iloc[snapshot]
        q_load = n.loads_t.q.iloc[snapshot]
        for load, p in p_load.items():
            bus = n.loads.loc[load, "bus"]
            p_inj[bus] -= p
        for load, q in q_load.items():
            bus = n.loads.loc[load, "bus"]
            q_inj[bus] -= q

    # draw lines
    plt.figure(figsize=(10,8))
    for idx, line in n.lines.iterrows():
        b0, b1 = line["bus0"], line["bus1"]
        x0, y0 = bus_coords[b0]
        x1, y1 = bus_coords[b1]
        # line width = real power flow magnitude
        flow = abs(n.lines_t.p0.iloc[snapshot][idx])
        plt.plot([x0,x1],[y0,y1], color='k', lw=max(flow/20, 0.5), alpha=0.7)  # minimum width 0.5

    # draw buses
    xs = [bus_coords[bus][0] for bus in n.buses.index]
    ys = [bus_coords[bus][1] for bus in n.buses.index]
    sizes = [v*2000 for v in v_mag]  # node size
    colors = v_ang                 # node color = voltage angle

    sc = plt.scatter(xs, ys, s=sizes, c=colors, cmap='coolwarm', zorder=3)
    plt.colorbar(sc, label='Voltage angle [rad]')

    # add labels
    for bus in n.buses.index:
        x, y = bus_coords[bus]
        label = f"{v_mag[bus]:.2f} pu\n{np.degrees(v_ang[bus]):.1f}°\nP={p_inj[bus]:.1f}, Q={q_inj[bus]:.1f}"
        plt.text(x, y, label, ha='center', va='center', fontsize=8, zorder=4)

    plt.axis('off')
    plt.title("PyPSA Network Power Flow\nNode size = voltage magnitude, color = angle, line width = real power")
    plt.show()