# Project Plan: Beaver Agent MVP

**Project Goal:** To create a simulation with a single agent (a beaver) that can learn a basic survival loop: maintaining its energy by successfully gathering and consuming resources from its environment. This serves as the foundational MVP before tackling complex multi-agent behaviors like dam building.

---

### **Phase 0: Ideation & Scoping (The Blueprint)**

* **Objective:** Define the simplest possible mechanics for the world and the agent to establish a clear scope and prevent over-engineering.
* **Key Decisions:**
    1.  **Energy System:** An agent's `energy` (0-100) depletes by 1 point per time step.
    2.  **Core Actions:**
        * `eat`: Restores 50 energy.
        * `sleep`: Inactive for 10 steps, restores 20 energy.
        * `fell_tree`: Requires 3 "hits" to fell a tree.
    3.  **Resources:** A felled `TREE` becomes one `LOG` item.
    4.  **Tech Stack:**
        * **Environment:** Custom 2D world using NumPy.
        * **RL Algorithm:** PPO or DQN for the single agent.
* **Success Metric:** A one-page design document is finalized, outlining these core mechanics.

---

### **Phase 1: Environment MVP ("The Sandbox")**

* **Objective:** Build the static, non-interactive world for the agent.
* **Key Results:**
    1.  A 2D NumPy array represents the world grid.
    2.  Tile types for `LAND`, `WATER`, and `TREE` are defined.
    3.  A simple visualization tool (e.g., matplotlib, pygame) is created to render the grid state.
    4.  A basic game loop manages the progression of time (ticks).
* **Success Metric:** A script can generate and display a static world with trees and water. No agents are present yet.

---

### **Phase 2: Single-Agent Life Cycle ("The Survivor")**

* **Objective:** Introduce a single agent and train it to manage its energy by eating and sleeping, using pre-placed food.
* **Key Results:**
    1.  A `Beaver` agent class is created with `energy` and `inventory` attributes.
    2.  Agent actions `move`, `eat`, and `sleep` are implemented.
    3.  A V1 Reward Function is designed to incentivize survival (eating/sleeping when energy is low).
    4.  An RL training loop connects the agent, environment, and reward function.
* **Success Metric:** The agent autonomously navigates to pre-placed `LOG`s to eat and uses `sleep` to avoid starvation indefinitely.

---

### **Phase 3: Agent-Environment Interaction ("The Lumberjack")**

* **Objective:** Train the agent to create its own food by interacting with the environment.
* **Key Results:**
    1.  `TREE` tiles are made interactive, with a "hit count" attribute.
    2.  The `fell_tree` action is implemented to reduce a tree's hit count.
    3.  The V2 Reward Function is updated to include a small intermediate reward for hitting a tree, guiding the agent's learning process.
    4.  All pre-placed `LOG`s are removed from the world.
* **Success Metric:** A hungry agent, placed in a world with only trees, successfully learns to chop down a tree and eat the resulting log to survive. This completes the MVP.
