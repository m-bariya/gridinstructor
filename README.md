## gridinstructor

**gridinstructor** provides some simple teaching tools for introductory power systems courses; these were made for ER254 at UC Berkeley.

Topics: 
- power flow under `powerfow/`

### Installation

- **Prerequisites**: Python **3.12+**

Create and activate a virtual environment, then install the project using `uv` (recommended) or plain `pip`.

Using `uv`:

```bash
uv sync
```

Using `pip`:

```bash
pip install -e .
```

This will install the dependencies listed in `pyproject.toml` (including `pypsa`, `pandas`, `numpy`, `matplotlib`, and `networkx`).

### Power Flow
The power flow tools are in `powerflow/`. The main example script is `powerflow/run.py`. These examples are built around [PyPSA](https://pypsa.org/).  

- `create_small_net` builds a small network in PyPSA with some adjustable parameter specifications. 
- A few simple solution visualization options are available in `powerflow/visualize.py`. 

