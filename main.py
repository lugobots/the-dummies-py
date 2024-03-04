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

    def on_join():
        print("I may run it when the bot is connected to the server")
    
    # starter.set_config(config)
    # starter.set_initial_position(position)
    # starter.set_mapper(mapper)

    starter.run(MyBot(
        starter.get_config().get_bot_team_side(),
        starter.get_config().get_bot_number(),
        starter.get_initial_position(),
        starter.get_mapper()
    ), on_join)

    # first we need to load the env vars that will identify the bot position and field side
    # config = lugo4py.EnvVarLoader()

    # # Instead of working with the field coordinates (that may change based on the field side we play
    # # The map will help us to see the field in quadrants (called regions) instead of working with coordinates
    # mapper = mapper.Mapper(MAPPER_COLS, MAPPER_ROWS, config.get_bot_team_side())

    # # Our bot strategy defines our bot initial position based on its number
    # initialRegion = mapper.get_region(
    #     PLAYER_INITIAL_POSITIONS[config.get_bot_number()]["Col"],
    #     PLAYER_INITIAL_POSITIONS[config.get_bot_number()]["Row"],
    # )

    # lugo_client = lugo4py.NewClientFromConfig(config, initialRegion.get_center())

    # my_bot = MyBot(
    #     config.get_bot_team_side(),
    #     config.get_bot_number(),
    #     initialRegion.get_center(),
    #     mapper,
    # )

    # def on_join():
    #     print("Bot is connected to the server")

    # executor = ThreadPoolExecutor()
    # signal.signal(signal.SIGINT, lambda: executor.shutdown())
    # lugo_client.play_as_bot(executor, my_bot, on_join)
