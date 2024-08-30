from my_bot import MyBot
from lugo4py import NewDefaultStarter, Mapper

from settings import MAPPER_COLS, MAPPER_ROWS, PLAYER_INITIAL_POSITIONS

if __name__ == "__main__":
    #################################################################################
    #################################################################################
    #                You do not need to change this file                            #
    #                       Work on my_bot.py file                                  #
    #################################################################################
    #################################################################################
    
    starter = NewDefaultStarter()

    # The default mapper uses a 10x6 map
    # you may replace the default mapper, but it will also affect the initial positions!
    #
    config = starter.get_config()
    mapper = Mapper(MAPPER_COLS, MAPPER_ROWS, config.get_bot_team_side())

    position = PLAYER_INITIAL_POSITIONS[config.get_bot_number()]

    initialRegion = mapper.get_region(
        position['Col'],
        position['Row'],
    )
    starter.set_initial_position(initialRegion.get_center())
    starter.set_mapper(mapper)

    def on_join():
        print("I may run it when the bot is connected to the server")

    starter.run(MyBot(
        starter.get_config().get_bot_team_side(),
        starter.get_config().get_bot_number(),
        starter.get_initial_position(),
        starter.get_mapper()
    ), on_join)
