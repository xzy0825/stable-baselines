import subprocess

import gym
import numpy as np

from baselines.common.running_mean_std import RunningMeanStd
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from baselines.common.vec_env.vec_normalize import VecNormalize
from baselines.common.tests.test_common import _assert_eq

ENV_ID = 'BreakoutNoFrameskip-v4'

def test_runningmeanstd():
    """Test RunningMeanStd object"""
    for (x1, x2, x3) in [
         (np.random.randn(3), np.random.randn(4), np.random.randn(5)),
         (np.random.randn(3, 2), np.random.randn(4, 2), np.random.randn(5, 2))]:

        rms = RunningMeanStd(epsilon=0.0, shape=x1.shape[1:])

        x = np.concatenate([x1, x2, x3], axis=0)
        ms1 = [x.mean(axis=0), x.var(axis=0)]
        rms.update(x1)
        rms.update(x2)
        rms.update(x3)
        ms2 = [rms.mean, rms.var]

        assert np.allclose(ms1, ms2)

def test_vec_env():
    """Test VecNormalize Object"""
    def make_env():
        return gym.make(ENV_ID)

    env = DummyVecEnv([make_env])
    env = VecNormalize(env, ob=True, ret=True, clipob=10., cliprew=10.)
    _, done = env.reset(), [False]
    while not done[0]:
        actions = [env.action_space.sample()]
        obs, _, done, _ = env.step(actions)
    assert np.max(obs) <= 10

def test_mpi_runningmeanstd():
    """Test RunningMeanStd object for MPI"""
    return_code = subprocess.call(['mpirun', '--allow-run-as-root', '-np', '2', 'python', '-m', 'baselines.common.mpi_running_mean_std'])
    _assert_eq(return_code, 0)