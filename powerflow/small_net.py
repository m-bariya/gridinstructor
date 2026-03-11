import pypsa

def create_small_net(ngenerators=2, nloads=2, vnom=100, r=0.01, x=0.05):
    n = pypsa.Network()
    # must set a "snapshot" for pypsa
    # we could set many snapshots to solve time series power flows
    n.set_snapshots([0])

    # total buses = generators + loads + slack bus
    nbuses = ngenerators + nloads + 1
    for i in range(nbuses):
        n.add("Bus", f"Bus{i}", v_nom=vnom)

    # lines
    lines = [
        ("Bus0","Bus1"),
        ("Bus1","Bus2"),
        ("Bus2","Bus3"),
        ("Bus3","Bus4"),
        ("Bus4","Bus0"),
        ("Bus1","Bus3")
    ]

    for i,(b0,b1) in enumerate(lines):
        n.add(
            "Line",
            f"L{i}",
            bus0=b0,
            bus1=b1,
            r=r,      # resistance
            x=x,      # reactance
            s_nom=100
        )

    # -------------------------
    # GENERATORS
    # -------------------------

    # slack bus generator
    n.add(
        "Generator",
        "SlackGen",
        bus="Bus0",
        p_set=0,
        control="Slack",
        vm_pu=1.0
    )

    # PV generators
    n.add(
        "Generator",
        "Gen1",
        bus="Bus1",
        p_set=80,
        control="PV",
        vm_pu=1.02
    )

    n.add(
        "Generator",
        "Gen2",
        bus="Bus2",
        p_set=60,
        control="PV",
        vm_pu=1.01
    )

    # -------------------------
    # LOADS
    # -------------------------

    n.add("Load","Load1",bus="Bus3",p_set=90,q_set=30)
    n.add("Load","Load2",bus="Bus4",p_set=40,q_set=15)

    return n