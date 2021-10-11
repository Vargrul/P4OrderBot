from orderbot.src.bot import P4OrderBot
import orderbot.src.database_ctrl as database_ctrl

if __name__ == "__main__":
    orderBot = P4OrderBot()
    orderBot.start()
    # database_ctrl.early_test_main()
