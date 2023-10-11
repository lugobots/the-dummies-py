import traceback
from abc import ABC

import lugo4py
import lugo4py.mapper as mapper
from settings import get_my_expected_position


class MyBot(lugo4py.Bot, ABC):
    def on_disputing(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            # the reader helps us to read the game state
            (reader, me) = self.make_reader(snapshot)
            ball_position = reader.get_ball().position

            # try the auto complet for reader.make_order_... there are other options
            move_order = reader.make_order_move_max_speed(me.position, ball_position)

            # Try other methods to create Move Orders:
            # move_order = reader.make_order_move_by_direction(lugo4py.DIRECTION_FORWARD)
            # move_order = reader.make_order_move_from_vector(lugo4py.sub_vector(vector_a, vector_b))

            # we can ALWAYS try to catch the ball
            catch_order = reader.make_order_catch()

            # the debug_message helps us to see that was the order sent by this bot
            order_set.debug_message = "Disputing: trying to get the ball"
            order_set.orders.extend([move_order, catch_order])
            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_defending(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)
            ball_position = reader.get_ball().position

            move_order = reader.make_order_move_max_speed(me.position, ball_position)
            # we can ALWAYS try to catch the ball
            catch_order = reader.make_order_catch()

            order_set.debug_message = "Disputing: trying to get the ball"
            order_set.orders.extend([move_order, catch_order])
            return order_set
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)

            # "point" is an X and Y raw coordinate referecend by the field, so the side of the field matters!
            # "region" is a mapped area of the field create by your mapper! so the side of the field DO NOT matter!
            opponent_goal_point = reader.get_opponent_goal().get_center()
            goal_region = self.mapper.get_region_from_point(opponent_goal_point)
            my_region = self.mapper.get_region_from_point(me.position)

            if self.is_near(my_region, goal_region):
                my_order = reader.make_order_kick_max_speed(snapshot.ball, opponent_goal_point)
            else:
                my_order = reader.make_order_move_max_speed(me.position, opponent_goal_point)

            order_set.debug_message = "attack!"
            order_set.orders.append(my_order)
            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_supporting(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)

            ball_holder_position = snapshot.ball.position

            # "point" is an X and Y raw coordinate refereciend by the field, so the side of the field matters!
            # "region" is a mapped area of the field create by your mapper! so the side of the field DO NOT matter!
            ball_holder_region = self.mapper.get_region_from_point(ball_holder_position)
            my_region = self.mapper.get_region_from_point(me.position)

            if self.is_near(ball_holder_region, my_region):
                move_dest = ball_holder_position
                order_set.debug_message = "supporting"
            else :
                move_dest = get_my_expected_position(reader, self.mapper, self.number)
                order_set.debug_message = "keeping position"

            move_order = reader.make_order_move_max_speed(me.position, move_dest)
            order_set.orders.append(move_order)
            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def as_goalkeeper(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot, state: lugo4py.PLAYER_STATE) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)
            position = snapshot.ball.position

            if state != lugo4py.PLAYER_STATE.DISPUTING_THE_BALL:
                position = reader.get_my_goal().get_center()

            my_order = reader.make_order_move_max_speed(me.position, position)

            order_set.turn = snapshot.turn
            order_set.debug_message = "defending the goal"
            order_set.orders.extend([my_order, reader.make_order_catch()])
            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')


    def is_near(self, region_origin: mapper.Region, dest_origin: mapper.Region) -> bool:
        max_distance = 2
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance