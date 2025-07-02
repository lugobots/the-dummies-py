import random
import time
from typing import Any, Tuple
import math
import numpy as np

from lugo4py import GameSnapshot, GameSnapshotInspector, Mapper, Point, PlayerProperties, GameProperties, Player, Remote, Team, specs, new_velocity, Velocity
from lugo4py.rl import BotTrainer, PlayersOrders, TurnOutcome, PlayerOrdersOnRLSession

MAX_STEPS_PER_EPISODE = 300

class MyBotTrainer(BotTrainer):
    def __init__(self, bot_trainer_num, remote_control: Remote):
        self.bot_trainer_num = bot_trainer_num
        self.remote_control = remote_control
        self.Mapper = Mapper(12, 12, Team.Side.HOME)
        self.sensor_area_granularity = 7
        self.sensor_area_width = specs.PLAYER_SIZE * self.sensor_area_granularity * 2 # three ahead and three behind

    def create_new_initial_state(self, data: Any) -> GameSnapshot:
        
        game_prop = GameProperties()
        game_prop.turn = 1
        self.remote_control.SetGameProperties(game_prop)

        for i in range(11):
            x = random.randint(specs.FIELD_WIDTH//2, specs.FIELD_WIDTH - specs.GOAL_ZONE_RANGE)
            y = random.randint(specs.FIELD_HEIGHT//5, specs.FIELD_HEIGHT-(specs.FIELD_HEIGHT//5))
            p = Point()
            p.x = x
            p.y = y
            self._set_player_position(i + 1, p, Team.AWAY)

        p = Point()
        p.x = specs.FIELD_WIDTH//2
        p.y = random.randint(specs.FIELD_HEIGHT//5, specs.FIELD_HEIGHT-(specs.FIELD_HEIGHT//5))
        response = self._set_player_position(self.bot_trainer_num, p, Team.HOME)


        return response.game_snapshot

    def get_training_state(self, snapshot: GameSnapshot) -> Any:
        inspector = GameSnapshotInspector(Team.Side.HOME, self.bot_trainer_num, snapshot)
        me = inspector.get_me()

        sensors = scan_area(me.position, self.sensor_area_width, inspector.get_opponent_players(), self.sensor_area_granularity)
        state = np.array(sensors, dtype=np.float32).flatten()
        dist = self._dist_to_goal(me)

        dist_to_goal = np.array([dist], dtype=np.float32)  # shape (1,)
        return np.concatenate([state, dist_to_goal])

    def play(self, game_snapshot: GameSnapshot, action: Any) -> PlayersOrders:
        inspector = GameSnapshotInspector(Team.Side.HOME, self.bot_trainer_num, game_snapshot)
        orders = inspector.make_order_move_by_direction(action)

        player_orders = PlayerOrdersOnRLSession(
            team_side=Team.Side.HOME,
            number=self.bot_trainer_num,
        )
        player_orders.orders.append(orders)

        response = PlayersOrders()
        response.default_behaviour = "zombies"
        response.players_orders.append(player_orders)
        return response

    def evaluate(self, previous_game_snapshot: GameSnapshot, new_game_snapshot: GameSnapshot, turn_outcome: TurnOutcome    ) -> Tuple[float, bool]:
        previous_inspector = GameSnapshotInspector(Team.Side.HOME, self.bot_trainer_num, previous_game_snapshot)
        previous_me = previous_inspector.get_me()

        new_inspector = GameSnapshotInspector(Team.Side.HOME, self.bot_trainer_num, new_game_snapshot)
        new_me = new_inspector.get_me()

        previous_sensors = scan_area(previous_me.position, self.sensor_area_width, previous_inspector.get_opponent_players(), self.sensor_area_granularity)
        new_sensors = scan_area(new_me.position, self.sensor_area_width, new_inspector.get_opponent_players(), self.sensor_area_granularity)

        previous_score = compute_reward(previous_sensors)
        new_score = compute_reward(new_sensors)

        if math.isinf(new_score):
            return -1, True

        reward = new_score - previous_score

        previous_goal_dist = abs(self._dist_to_goal(previous_me))
        new_goal_dist = abs(self._dist_to_goal(new_me))
        if previous_goal_dist > new_goal_dist:
            reward += 1 - previous_goal_dist

        if not np.isfinite(reward):
            return 0, True

        return reward, new_inspector.get_turn() >= MAX_STEPS_PER_EPISODE


    def _set_player_position(self, player_number: int, position: Point, side)  :
        prop = PlayerProperties()
        prop.number = player_number
        prop.side = side

        prop.position.x = position.x
        prop.position.y = position.y
        return self.remote_control.SetPlayerProperties(prop)

    def _dist_to_goal(self, me: Player):
        goal = self.Mapper.get_attack_goal().get_center()
        dist_goal_x = (goal.x - me.position.x) / specs.FIELD_WIDTH
        # dist_goal_y = (goal.y - me.position.y) / specs.FIELD_HEIGHT
        # return math.sqrt(dist_goal_x**2 + dist_goal_y**2)
        return dist_goal_x


def _create_velocity(speed: float, direction) -> Velocity:
    velocity = new_velocity(direction)
    velocity.speed = speed
    return velocity


def delay(ms: float) -> None:
    time.sleep(ms / 1000)


def random_integer(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)

def scan_area(point, distance, players, granularity):
    # Initialize matrix
    matrix = [[0 for _ in range(granularity)] for _ in range(granularity)]

    # Calculate square boundaries
    half = distance // 2
    min_x = point.x - half
    max_x = point.x + half
    min_y = point.y - half
    max_y = point.y + half

    # Calculate size of each quadrant
    quad_width = distance / granularity
    quad_height = distance / granularity

    for player in players:
        px = player.position.x
        py = player.position.y

        if min_x <= px <= max_x and min_y <= py <= max_y:
            # Normalize position within the area
            rel_x = px - min_x
            rel_y = py - min_y

            # Determine which cell the player is in
            col = int(rel_x // quad_width)
            row = int(rel_y // quad_height)

            # Clamp indices to avoid overflow
            col = min(col, granularity - 1)
            row = min(row, granularity - 1)

            matrix[row][col] = 1

    # print(matrix)
    return matrix


def compute_reward(scan_matrix):
    reward = 0
    g = len(scan_matrix)  # granularity
    center = (g - 1) / 2  # center cell (can be non-integer if even granularity)

    for row in range(g):
        for col in range(g):
            if scan_matrix[row][col] == 1:
                # Euclidean distance from center
                dx = col - center
                dy = row - center
                dist = math.sqrt(dx**2 + dy**2)

                # Avoid division by zero
                if dist < 0.5:
                    return -float('inf')  # player on top of agent
                reward -= 1 / dist  # the closer the player, the worse

    return reward
