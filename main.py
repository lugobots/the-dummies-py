from my_bot import MyBot
from lugo4py import NewDefaultStarter

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
    # config = starter.get_config()
    # mapper = mapper.Mapper(20, 12, config.get_bot_team_side())
    #
    # initialRegion = mapper.get_region(
    #     8,
    #     4,
    # )
    # starter.set_initial_position(position)
    # starter.set_mapper(mapper)

    def on_join():
        print("I may run it when the bot is connected to the server")

    starter.run(MyBot(
        starter.get_config().get_bot_team_side(),
        starter.get_config().get_bot_number(),
        starter.get_initial_position(),
        starter.get_mapper()
    ), on_join)
