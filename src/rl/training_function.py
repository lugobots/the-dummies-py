from datetime import datetime

from stable_baselines3 import PPO

from .bot_trainer import MAX_STEPS_PER_EPISODE
from .env import StubEnv
from lugo4py.rl import TrainingController

episodes = 1_000

def my_training_function(training_ctrl: TrainingController) -> None:
    print("Let's train")

    env = StubEnv(training_ctrl)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=episodes*MAX_STEPS_PER_EPISODE, reset_num_timesteps=False)

    # vec_env = model.get_env()
    # obs = vec_env.reset()
    # for i in range(100):
    #     action, _states = model.predict(obs, deterministic=True)
    #     obs, reward, done, info = vec_env.step(action)
    #
    #     resets automatically
    #     if done:
        #   env.reset()

    print("that's all ")
    model.save(datetime.now().strftime('model-%Y-%m-%d-%H-%M'))
    print("model saved")
    env.close()


