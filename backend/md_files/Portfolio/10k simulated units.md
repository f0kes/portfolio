This project leverages GPU compute power to handle unit behaviors and spatial queries, achieving a 10x increase in simulated unit count compared to CPU-only solutions. The use of compute shaders and efficient data structures enables complex RTS gameplay at unprecedented scale.

Key Features:

- Simulates 10,000+ individual units in real-time
- GPU-accelerated flocking and pathfinding via compute shaders
- KD-tree spatial partitioning for O(log n) unit queries
- Flexible stat system with 8+ modifiable attributes per unit
- Custom shaders for billboard rendering and terrain blending

Technologies:

- Unity Engine, C#, HLSL/Cg
- Compute shaders for parallel unit processing
- Data-oriented design for optimal cache usage

Technical Highlights:

- 60+ FPS performance with 10,000 units on mid-range GPUs
- 90% reduction in CPU usage compared to traditional methods
- Custom rendering pipeline with instanced draw calls for units

