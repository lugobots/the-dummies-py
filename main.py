from my_bot import MyBot
import lugo4py
import lugo4py.mapper as mapper

from concurrent.futures import ThreadPoolExecutor
from settings import PLAYER_INITIAL_POSITIONS, MAPPER_COLS, MAPPER_ROWS

if __name__ == "__main__":
    #################################################################################
    #################################################################################
    #                You do not need to change this file                            #
    #                       Work on my_bot.py file                                  #
    #################################################################################
    #################################################################################

    # first we need to load the env vars that will identify the bot position and field side
    config = lugo4py.EnvVarLoader()

    # Instead of working with the field coordinates (that may change based on the field side we play
    # The map will help us to see the field in quadrants (called regions) instead of working with coordinates
    mapper = mapper.Mapper(MAPPER_COLS, MAPPER_ROWS, config.get_bot_team_side())

    # Our bot strategy defines our bot initial position based on its number
    initialRegion = mapper.get_region(PLAYER_INITIAL_POSITIONS[config.get_bot_number()]['Col'],
                                      PLAYER_INITIAL_POSITIONS[config.get_bot_number()]['Row'])

    lugo_client = lugo4py.NewClientFromConfig(config, initialRegion.get_center())

    my_bot = MyBot(config.get_bot_team_side(),
                   config.get_bot_number(), initialRegion.get_center(), mapper)

    def on_join():
        print("Bot is connected to the server")

    executor = ThreadPoolExecutor()
    lugo_client.play_as_bot(executor, my_bot, on_join)
