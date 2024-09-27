This project showcases my ability to leverage cutting-edge AI tools, 3D modeling techniques, and custom software development to create a robust pipeline for game character animation. By combining various technologies and developing custom solutions, I've created a workflow that significantly streamlines the process of generating high-quality, multi-directional character animations for games.

A technique for generating 8 directional character animations for games using ComfyUI, Stable Diffusion, CRM, AnimateDiff.

1. Using dreamshaper and t-pose controlnet we generate a base reference![[Pasted image 20240927183908.png]]
![[../Pasted image 20240927184013.png]]
2. With IClight, remove all lighting
 ![[../Pasted image 20240927184025.png]]
 3. using controlnet tile we generate 4k version of image
 4. with CRM we generate both character from different angles which we will use later, and a 3d model

![[../Pasted image 20240927184332.png]]
![[../Pasted image 20240927184348.png]]
![[../Pasted image 20240927184355.png]]
6. Go to mixamo, autorig, download rigged models and animations, import to blender
7. Using [my plugin](ttps://github.com/f0kes/blender_eight_directions), render diffuse and depth animations from 8 directions. ![[../Pasted image 20240927184825.png]] ![[../Pasted image 20240927184832.png]] ![[../Pasted image 20240927184841.png]]
8. Go through each animation with animatediff+ipadapter using my script. Use the 4 directions from step 4 for ip adapter, changing it depending on what animation is being rendered. [My script](https://github.com/f0kes/anim_renderer) automates this process
9. If i'd continue this project, i'd  generate normal maps for animations using ICLight