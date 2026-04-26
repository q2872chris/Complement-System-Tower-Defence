import pyglet as py
from windows import GameController

if __name__ == "__main__":
    GameController(width=900, height=600, resizable=False, fullscreen=False,
                   caption="Pyglet - Complement System Tower Defence 4")
    py.app.run()



# Include activation:
    # Maybe can't be upgraded/combinable while not activated
    # Just a simple boolean switch
    # Need to allow movement/shop placement to work with it
# Screens:
    # Start new game instantly clicks on second press only
    # Find a better way than bouncing initialisation functions around
# Enemies/Towers:
    # Vector maths for shooting (around corners)
    # Add second info toggle (none/combinations/tower type)!    *
    # Engineer type tower
    # Overclock aura tower
    # Dartling gun tower
    # Sort out tower spawn_projectile and projectile_generator
# Leaderboard upon death (multiple screens)
# Reorganise code/neaten/simplify/etc
# Combine protein/enemy data readers better (excel_data.py)
# Speed fixes:
    # Sprite pooling for enemies
    # Huge numpy array for all enemy positions (vectorise)
    # Cells along the track for bullet collisions
    # Somehow only draw top of stacked enemies
    # Put enemies in cells and only check within cells for towers






















