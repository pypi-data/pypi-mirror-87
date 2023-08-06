# def setup_env(config_path: str, env_name: str = DYNAMIC_ENV_ID) -> gym.core.Env:
#     """Create a dynamic Polycraft AI Lab environment.
#
#     This is used to automatically register an environment in OpenAI Gym before
#     instantiating an instance of it.
#
#     Args:
#         config_path (str): The path to the experiment's configuration file
#         env_name (str): By default, 'PALDynamicEnv-0', the standard Polycraft
#                         dynamic experiment environment. This is used to load
#                         custom experiment environments.
#     """
#     if env_name is not DYNAMIC_ENV_ID:  # Prevent duplicate registration
#         register(
#             id=env_name,
#             kwargs={'config_path': config_path}
#         )
#     env = gym.make(env_name, config_path=config_path)  # Only create env after registration
#     log.info('Registered new environment %s using config at %s', env_name, config_path)
#     return env
from typing import List

import numpy as np

DEFAULT_TASKS = ['pogo-stick', 'hunter-gatherer']


class PolycraftEnv:

    action_space = np.ndarray([])

    def __init__(self, task: str):
        self.client = ...
        self._task = task

    def _start_client(self):
        self.client.start()

    def __enter__(self):
        # Initialize game with task
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: Check type of error
        self._ensure_client_exited()

    def set_task(self, task: str):
        self._task = task

    def start(self):
        pass

    def step(self, action):
        """Simulate an action in the environment."""

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        """Shut down the client"""
        self._ensure_client_exited()

    def _ensure_client_exited(self):
        pass


def create_env(task: str) -> PolycraftEnv:
    env = PolycraftEnv(task)
    if task not in get_tasks():
        raise InvalidTaskError
    env.start()
    return env


def get_tasks() -> List[str]:
    """Return a list of all supported tasks"""
    return DEFAULT_TASKS


class InvalidTaskError(ValueError):
    """Raised when a given task is not one of the available tasks."""
