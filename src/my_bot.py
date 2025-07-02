import traceback
from abc import ABC
from typing import List

import lugo4py
from stable_baselines3 import PPO

from settings import get_my_expected_position
from rl.bot_trainer import MyBotTrainer


class MyBot(lugo4py.Bot, ABC):

    def load_models(self):
        self.model_move = PPO.load("model-2025-06-30-17-48")

    def on_disputing(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:

            # You have three sources of data about the game
            #
            # 1. inspector - provides real time data about the game elements.
            # You bot receives an inspector every turn. You may read all data about the elements of the game, time,
            # score, and everything else that changes during the game
            # The inspector also helps you to create orders:
            # inspector.get_my_team_players() # returns an array
            # inspector.get_me() # return the bot itself
            # inspector.get_ball().position
            # inspector.make_order_move_by_direction(lugo4py.DIRECTION.FORWARD)
            # inspector.make_order_move_from_point(ball_position)
            #
            # 2. self.mapper - Provides data about field coordinates, such as the location of the goals.
            # The Mapper views the field as a set of "regions" relative to your team’s side, rather than using fixed
            # coordinates. This means you don’t need to worry about which side you’re playing on—these coordinates
            # will always make sense from your team’s perspective.
            # Example: self.mapper.get_region_from_point(me.position).get_center()
            #
            # 3. specs - brings all the game specification.
            # Example:
            # lugo4py.specs.MAX_Y_COORDINATE
            # lugo4py.specs.BALL_MAX_SPEED

            ball_position = inspector.get_ball().position

            # try the auto complete for reader.make_order_... there are other options
            move_order = inspector.make_order_move_max_speed(ball_position)
            my_region = self.mapper.get_region_from_point(inspector.get_me().position)

            # Try other methods to create Move Orders:
            # move_order = reader.make_order_move_by_direction(lugo4py.DIRECTION_FORWARD)
            # move_order = reader.make_order_move_from_vector(lugo4py.sub_vector(vector_a, vector_b))

            # we can ALWAYS try to catch the ball
            catch_order = inspector.make_order_catch()

            if self.am_i_closest(inspector, ball_position, 2):
                return [move_order, catch_order]
            else:
                if self.is_near(my_region, self.mapper.get_region_from_point(self.initPosition)) is False:
                    move_order = inspector.make_order_move_max_speed(self.initPosition)
                    return [move_order, catch_order]
                return [catch_order]



        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_defending(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:

            ball_position = inspector.get_ball().position
            # we can ALWAYS try to catch the ball
            catch_order = inspector.make_order_catch()

            move_order = inspector.make_order_move_max_speed(ball_position)
            my_region = self.mapper.get_region_from_point(inspector.get_me().position)

            if self.am_i_closest(inspector, ball_position, 2):
                return [move_order, catch_order]
            else:
                if self.is_near(my_region, self.mapper.get_region_from_point(self.initPosition)) is False:
                    move_order = inspector.make_order_move_max_speed(self.initPosition)
                    return [move_order, catch_order]
                else:
                    move_order = inspector.make_order_move_to_stop()
                    return [move_order, catch_order]
            return [catch_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:

            # # "point" is an X and Y raw coordinate referenced by the field, so the side of the field matters!
            # # "region" is a mapped area of the field create by your mapper! so the side of the field DO NOT matter!
            # opponent_goal_point = self.mapper.get_attack_goal()
            # goal_region = self.mapper.get_region_from_point(opponent_goal_point.get_center())
            # my_region = self.mapper.get_region_from_point(inspector.get_me().position)
            #
            # if self.is_near(my_region, goal_region):
            #     my_order = inspector.make_order_kick_max_speed(opponent_goal_point.get_center())
            # else:
            #     my_order = inspector.make_order_move_max_speed(opponent_goal_point.get_center())
            trainer = MyBotTrainer(self.number,None)
            sts = trainer.get_training_state(inspector.get_snapshot())

            action, _ = self.model_move.predict(sts, deterministic=True)
            my_order = inspector.make_order_move_by_direction(action)
            return [my_order]

        except Exception as e:
            print(f'did not play this turn due to exception. {e}')
            traceback.print_exc()

    def on_supporting(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            ball_holder_position = inspector.get_ball().position

            # "point" is an X and Y raw coordinate referenced by the field, so the side of the field matters!
            # "region" is a mapped area of the field create by your mapper! so the side of the field DO NOT matter!
            ball_holder_region = self.mapper.get_region_from_point(ball_holder_position)
            my_region = self.mapper.get_region_from_point(inspector.get_me().position)

            if self.is_near(ball_holder_region, my_region):
                move_dest = ball_holder_position
            else:
                move_dest = get_my_expected_position(inspector, self.mapper, self.number)

            move_order = inspector.make_order_move_max_speed(move_dest)
            return [move_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def as_goalkeeper(self, inspector: lugo4py.GameSnapshotInspector, state: lugo4py.PLAYER_STATE) -> List[lugo4py.Order]:
        try:
            position = inspector.get_ball().position

            if state != lugo4py.PLAYER_STATE.DISPUTING_THE_BALL:
                position = self.mapper.get_attack_goal().get_center()

            my_order = inspector.make_order_move_max_speed(position)

            return [my_order, inspector.make_order_catch()]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')

    def is_near(self, region_origin: lugo4py.mapper.Region, dest_origin: lugo4py.mapper.Region) -> bool:
        max_distance = 2
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance

    def am_i_closest(self, inspector: lugo4py.GameSnapshotInspector, point, num_closest) -> bool:
        my_player = inspector.get_me()
        my_dist = (my_player.position.x - point.x) ** 2 + (my_player.position.y - point.y) ** 2

        closer_players_count = 0
        for player in inspector.get_my_team_players():
            if player.number == my_player.number or player.number == 1:
                continue  # skip self
            dist = (player.position.x - point.x) ** 2 + (player.position.y - point.y) ** 2
            if dist < my_dist:
                closer_players_count += 1
                if closer_players_count >= num_closest:
                    return False

        return True