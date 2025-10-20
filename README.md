# Overwatch Ban Simulator

This project simulates the hero banning phase of a competitive Overwatch match. It allows users to model different ban strategies and observe their outcomes.

## Overview

The simulation operates as follows:

1.  **Vote Tallying**: Each player on both teams casts votes for the heroes they want to see banned. These votes are weighted and tallied.
2.  **Ban Nomination**: Teams take turns nominating heroes to ban from the pool of voted heroes.
3.  **Role Limits**: A maximum of two heroes per role (Tank, Damage, Support) can be banned in total.
4.  **Conclusion**: The ban phase concludes when each team has banned two heroes or when no more valid nominations can be made.

## Getting Started

### Prerequisites

*   Python 3.x

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/overwatch-ban-sim.git
    cd overwatch-ban-sim
    ```

2.  (Optional) Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

### Usage

To run the simulation, execute the `OverwatchBanSim.py` script:

```bash
python OverwatchBanSim.py
```

The script will print the results of the ban phase, including which heroes were banned and by which team.

## Project Structure

*   `OverwatchBanSim.py`: The main script that runs the simulation. It defines the `Overwatch` game class and its specific ban logic.
*   `ban_sim.py`: A generic module for simulating the banning phase of a MOBA-style game. It provides the base `Game`, `Team`, `Player`, and `Character` classes.
*   `Overwatch_Heroes.json`: A JSON file containing the list of Overwatch heroes and their roles.
