import networkx as nx

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

def plot_network_results(n):
    """
    Simple matplotlib plot of a PyPSA network power flow.
    Node size = voltage magnitude, color = angle, line width = real power flow.
    """

    # --- Bus positions ---
    bus_coords = {bus: (np.random.rand(), np.random.rand()) for bus in n.buses.index}

    # --- Extract results ---
    snapshot = 0
    v_mag = n.buses_t.v_mag_pu.iloc[snapshot]
    v_ang = n.buses_t.v_ang.iloc[snapshot]

    # --- Compute net injections per bus ---
    # initialize with zeros
    p_inj = pd.Series(0.0, index=n.buses.index)
    q_inj = pd.Series(0.0, index=n.buses.index)

    # Generators
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

    # --- Plot lines ---
    import pdb; pdb.set_trace()
    plt.figure(figsize=(10,8))
    for idx, line in n.lines.iterrows():
        b0, b1 = line["bus0"], line["bus1"]
        x0, y0 = bus_coords[b0]
        x1, y1 = bus_coords[b1]
        # line width = real power flow magnitude
        flow = abs(n.lines_t.p0.iloc[snapshot][idx])
        plt.plot([x0,x1],[y0,y1], color='k', lw=max(flow/20, 0.5), alpha=0.7)  # minimum width 0.5

    # --- Plot buses ---
    xs = [bus_coords[bus][0] for bus in n.buses.index]
    ys = [bus_coords[bus][1] for bus in n.buses.index]
    sizes = [v*2000 for v in v_mag]  # node size
    colors = v_ang                 # node color = voltage angle

    sc = plt.scatter(xs, ys, s=sizes, c=colors, cmap='coolwarm', zorder=3)
    plt.colorbar(sc, label='Voltage angle [rad]')

    # --- Add labels ---
    for bus in n.buses.index:
        x, y = bus_coords[bus]
        label = f"{v_mag[bus]:.2f} pu\n{np.degrees(v_ang[bus]):.1f}°\nP={p_inj[bus]:.1f}, Q={q_inj[bus]:.1f}"
        plt.text(x, y, label, ha='center', va='center', fontsize=8, zorder=4)

    plt.axis('off')
    plt.title("PyPSA Network Power Flow\nNode size = voltage magnitude, color = angle, line width = real power")
    plt.show()