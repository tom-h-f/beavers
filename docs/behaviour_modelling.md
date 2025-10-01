# Modelling Beaver Behaviours

Key Beaver behaviours to Replicate
The primary behaviours you should model can be broken down into resource management, construction, and survival.

Felling Trees: This is the foundational action. Beavers cut down trees for two reasons: food (eating the nutritious inner bark) and building materials.

Dam Building: The most iconic behavior. Agents must cooperatively gather materials (wood, mud) and place them in a water flow (a river) to block it. This is a sequential, cooperative task.

Lodge Construction: Agents build a shelter within the pond created by their dam. The lodge serves as a safe zone from predators and the elements.

Food Caching: Beavers create underwater stockpiles of branches to eat during the winter. This is a crucial long-term planning behavior.

Cooperation: These tasks are rarely done alone. Agents should ideally learn to work together, such as one agent felling a tree while others transport the branches to the dam.

Environment and Agent Setup
Your MARL environment needs specific components to facilitate these behaviours.

State Space: The environment should include:

A grid-world with different terrain types (land, water source, riverbed).

Resources: Trees that can be felled and depleted.

Dynamic Water: This is critical. The water level must rise behind a dam as it's being built. The dam's integrity should directly impact the pond's existence.

Blueprint Sites: Designated areas for the dam and lodge where agents must place materials.

Agent Actions: Each agent should have a simple set of actions:

move (up, down, left, right)

gather_wood (when next to a tree)

place_material (when at a blueprint site with wood)

eat (when at a food cache)

Agent Observations: Each beaver should have a partial view of the world, seeing its immediate surroundings, its own inventory (e.g., carrying wood), its energy level, and maybe the status of the dam/lodge blueprints.

Reward Engineering for Emergent Behavior
The reward structure is the most important part of encouraging realistic behavior. You need to balance individual incentives with shared goals. A purely individual reward (e.g., +1 for placing a branch) can lead to selfish, inefficient behavior.

Shared Team Rewards (Primary Driver)
These rewards are given to all agents in the colony and are crucial for fostering cooperation.

🏆 Pond Creation Bonus: A large, one-time shared reward when the dam is completed and the water level reaches a target height. This is the main objective.

💧 Pond Maintenance Reward: A small, continuous shared reward for every time step that the pond's water level is maintained above a certain threshold. This incentivizes dam repair.

🏠 Lodge Completion Bonus: A significant shared reward for completing the lodge, creating a "safe zone."

stockpile Reward:** A shared reward that scales with the amount of wood stored in the underwater food cache. This promotes foresight and resource management.

Individual Rewards (Secondary Driver)
These rewards guide the agent's basic actions and ensure its own survival.

Positive Rewards (+):

+ Small reward for successfully gathering wood.

+ Small reward for successfully placing a piece of wood on a blueprint (this is much smaller than the shared completion bonus).

+ Reward for eating when energy is low.

Negative Rewards (-):

- A small penalty for every action taken (an "existence penalty") to encourage efficiency.

- A larger penalty for having low energy (hunger).

- A penalty for being outside the lodge/pond area if predators are included in the model.

By making the shared rewards significantly larger than the individual ones, the agents' optimal strategy will be to cooperate to build the dam and lodge. They'll learn that felling trees and placing materials (individual actions) are necessary steps to achieve the highly-valued shared goal of creating a thriving wetland ecosystem.


Sources

