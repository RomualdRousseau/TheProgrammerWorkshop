# Project Interaction History

1. Create a new skill for a game developer.
2. In the game project structure, wehre to put the physic engine? /dev
3. Create a new skill for a gameplay designer that will write the user story to implement. I want him to manage the TODO.md, with a backlop, story/task to be developed, story/task done
4. Create a game based on a grid NxN (N should be a constants):
   - A ball is positioned on this grid at a random location.
   - A rectangle of 3x3 is positioned randomly on the grid.
   - The ball moved toward a random location in the rectangle.
   - Using Euler integration, the ball moved with an initial speed random, has a weight and have friction.
   / tic
5. Remove src from the import as src is not part of the import for uv and pytest
6. Avoid import with *
7. check code with ruff and ty
8. not pyright but ty from astral
9. put all code in the module permanance_env and make the module executable with a __main__.py
10. Always use import with absolute name
11. Import pyray as pr
12. put all constants in its own file. And also add a config.py to handle configuration that can be chnaged by environment variable or config file. Propose a project structure where to put those files at best. Maybe also need a util module to put shared utilities? Propose but do not change.
13. I mean core should be a module with config inside. and util should me module with constant inside
14. yes
15. the size of the rectangle of 3 should be a symbolic constant
16. Rename N by GRID_SIZE
17. windows title is a constant not a configurable item
18. Based on our discussion, update the TODO, also write the README /tic
19. Complete doc string if necessary /tac
20. Write a justfile
21. add a rule to format, clean should use pyclean
22. I manually edited the project. Do not changes. Update documentation /tac
23. Exclude UI from tests
24. Below code should be in a update function within the game module:
    - # Logic: Accelerate ball towards target
    - accelerate_towards(state.ball, state.target.target_pos, initial_speed, dt)
    - # Physics: Update ball state
    - apply_physics(state.ball, dt)
    - Propose a change
25. as the update will update the entire game play, it should be update_game and gameplay file? what do you think?
26. The ball shoudl go toward the target but not stop at it, just continue. /tac
27. to avoid division by 0 in accelerate_toward, just add an EPSILON constant
28. I manually edited the project
29. constants and helpers mut be singular
30. I manually edited teh tac skill but based on our discussion update the tac skill about prject structure, import practices, module naming ...
31. Update the pyproject decsription
32. Propose a plan for tests /tac
33. Update the README to use just in priority
34. Implement the tests and also add coverage. Update the justfile
35. Exclude UI from tests
36. Write all my prompts in a file.
37. The init_game should move in the gameplay
38. the update_game also return the GameState
39. For the physics, I want to have apply_gravity, apply_frictionm apply_toward, each take a force parameter and return a force vector sumed up with the effect, and finally apply_physics, take the force vector and do euler integration.
40. Remove gravity effcet as gravity as no effect on th eplane, void by the tension force of the plane
41. in physics, prefer calculation using pyray vector2 facilities (vector2_add, vector2_scale ...)
42. do a just check and fix
43. in the renderer, the rectangle is filled and draw after the ball
44. The renderer shoudl render 2 layers: 1) Draw the grid, the rectangle, and for the ball fill the cell where the ball is, and for the target, fill the cell where the target is. 2) On the top, draw the ball, the target and the rectangle again
45. I manually edited the code. I think the grid_x and grid_y in the target state are not necessary
46. ok, then create 2 state, one for the rectangle and one fo the target
47. I want to be able to toggle the layer 2 visibility with the keyboard
48. Based on discussion, update TODO /tic
49. where to put the assets. Propose but no changes. /tac
50. ok, so organize assets
51. I will add a folder for tileset and tilemap
52. Using pytmx, load the room map and render it in layer 2 /tac
53. For the tile rendering, write a function that take a tile in parameter, return on raylib Image. A tile is defined by ('assets/tilemaps/../tilesets/../images/interior.png', (0, 0, 16, 16), TileFlags(flipped_horizontally=0, flipped_vertically=0, flipped_diagonally=0)). When the image return, draw it.
54. I manually edited the project. fill the pr.draw_texture_pro with the correct arguments in renderer
55. I manually edited the project. Use @cache decorator for the get_tile_texture /tac
56. add in the prompt.md all my prompts for this discussion. Also update TODO and README. /tic
57. Move physics in core /tac
58. I want to replace the drawing of the rectangle by a sprite "table" in assets/images. I also want to replace the ball by an animated sprite "ball" from assets/images. The image is a 3 frame animation at say 3 frames per second.
59. the screen width has a border of 1 cell at each side, and the screen height has a boder of 4 cell on top and 1 cell on bottom. the tilemap cover all the screen but the grid is within the borders. /tac
60. Do a just check and just coverage, fix and add missing tests /tac
61. I manually edited the project.
62. I manaully fixed the types error. The table is randomly located but within a 2 cells border.
63. Update TODO and documentation based on our discussion /tic
64. Make the ball rebound on the border of the grid /tac
65. The rebound should take inton account the size of the ball, the ball has a radisu of half a grid cell.
66. Update TODO, Update Readme and fill the prompt.md with this last discussion /tic
