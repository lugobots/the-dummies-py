from my_bot import MyBot
from lugo4py.client import NewClientFromConfig
from lugo4py.mapper import Mapper
from lugo4py.loader import EnvVarLoader
from concurrent.futures import ThreadPoolExecutor
from settings import PLAYER_POSITIONS, MAPPER_COLS, MAPPER_ROWS

if __name__ == "__main__":

    config = EnvVarLoader()

    # The map will help us to see the field in quadrants (called regions) instead of working with coordinates
    mapper = Mapper(MAPPER_COLS, MAPPER_ROWS, config.get_bot_team_side())

    # Our bot strategy defines our bot initial position based on its number
    initialRegion = mapper.get_region(PLAYER_POSITIONS[config.get_bot_number()]['Col'],
                                      PLAYER_POSITIONS[config.get_bot_number()]['Row'])

    lugo_client = NewClientFromConfig(config, initialRegion.get_center())

    my_bot = MyBot(config.get_bot_team_side(),
                   config.get_bot_number(), initialRegion.get_center(), mapper)

    def on_join():
        print("Bot is connected to the server")

    executor = ThreadPoolExecutor()
    lugo_client.play_as_bot(executor, my_bot, on_join)
