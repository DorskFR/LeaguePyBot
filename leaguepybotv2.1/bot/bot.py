from .. import *
from time import time



class LeaguePyBot:
    def __init__(self):
        self.client = Client()
        self.game = Game()
        self.minimap = Vision()
        self.screen = Vision()
        self.controller = Controller()
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.bot_loop())

    async def bot_loop(self):
        loop_time = time()
        while True:

            # computer vision
            await self.vision.compute()
            # update data
            await self.game.update()
            # determine actions
            await self.brain.think()
            # send actions to controller
            await self.controller.execute()

            self.FPS = round(float(1 / (time() - loop_time)), 2)
            loop_time = time()

        pass


    # misc
        - reset
        - update_FPS

    # actions:
        - fall_back
        - heal
        - recall
        - cast_spells
        - attack
        - attack_building
        - attack_champion
        - attack_tower
        - follow_allies
        - move_minimap / go_to_lane
        - buy items
    
    # calculations:
        - get_closest_enemy_building_position
        - get_closest_enemy_champion_position
        - get_closest_enemy_position
        - get_average_enemy_position
        - get_safest_ally_position
        - get_riskiest_ally_position
        - find_closest_ally_zone
        - find_closest_zone

        - get_units_position(units, function)
            - ally_minions
            - enemy_minions
            - enemy_champions
            - enemy_buildings
            - riskiest_position
            - safest_position
            - average_position

    # computer vision:
        - locate_game_objects_AND_update
        - locate_champions_on_minimap_AND_update