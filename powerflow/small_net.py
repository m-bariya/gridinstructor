import pypsa
import numpy as np

def create_small_net(ngenerators=2, nloads=2, vnom=100, r=0.01, x=0.05, p_mu=100, connectivity=None):
    n = pypsa.Network()
    # must set a "snapshot" for pypsa
    # we could set many snapshots to solve time series power flows
    n.set_snapshots([0])

    # total buses = generators + loads + slack bus
    nbuses = ngenerators + nloads + 1
    for i in range(nbuses):
        n.add("Bus", f"Bus{i}", v_nom=vnom)
    
    if connectivity is None:
    # if no connectivity is provided, create a fully connected network
        for i in range(nbuses):
            for j in range(i+1, nbuses):
                if i != j:
                    n.add("Line", f"L{i}{j}", bus0=f"Bus{i}", bus1=f"Bus{j}", r=r, x=x, s_nom=p_mu)
    else:
        for i in range(nbuses):
            for j in range(i+1, nbuses):
                if connectivity[i][j]:
                    n.add("Line", f"L{i}{j}", bus0=f"Bus{i}", bus1=f"Bus{j}", r=r, x=x, s_nom=p_mu)

    busidx = 0
    # add slack bus - V, theta fixed
    n.add("Generator", "SlackGen", bus=f"Bus{busidx}", p_set=0, control="Slack", vm_pu=1.0)
    busidx += 1

    # add generators - P, V fixed
    p_gen = np.random.normal(loc=p_mu, scale=0.1*p_mu, size=ngenerators)
    for g in range(ngenerators):
        n.add("Generator", f"Gen{g}", bus=f"Bus{busidx}", p_set=p_gen[g], control="PV", vm_pu=1.0)
        print(f"Generator {g} added to bus {busidx} with power {p_gen[g]} MW")
        busidx += 1
    
    # add loads - P, Q fixed
    p_load = np.random.normal(loc=p_mu, scale=0.1*p_mu, size=nloads)
    q_load = np.random.normal(loc=p_mu, scale=0.1*p_mu, size=nloads)
    for l in range(nloads):
        n.add("Load", f"Load{l}", bus=f"Bus{busidx}", p_set=p_load[l], q_set=q_load[l])
        print(f"Load {l} added to bus {busidx} with power {p_load[l]} MW and reactive power {q_load[l]} MVAr")
        busidx += 1

    return n