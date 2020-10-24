import warnings
import signal
import pandas as pd
import numpy as np

from agent.sac import SAC
from agent.policy import LnMlpPolicy
from agent.callback import SaveOnBestReturn
from tools.get_task import AltitudeTask, AttitudeTask, BodyRateTask
from tools.schedule import schedule_kink, constant
from tools.identifier import get_ID
from tools.plot_training import plot_training
from tools.plot_weights import plot_weights

warnings.filterwarnings("ignore", category=FutureWarning, module='tensorflow')
warnings.filterwarnings("ignore", category=UserWarning, module='gym')

task = AttitudeTask
# task = AltitudeTask

# from envs.citation import CitationElevRange as Citation
# from envs.citation import CitationAileronEff as Citation
# from envs.citation import CitationRudderStuck as Citation
# from envs.citation import CitationHorzTail as Citation
# from envs.citation import CitationVertTail as Citation
from envs.citation import CitationIcing as Citation
# from envs.citation import CitationCgShift as Citation


def learn():

    env_train = Citation(task=task)
    env_eval = env_train.get_cousin()

    callback = SaveOnBestReturn(eval_env=env_eval, eval_freq=2000, log_path="agent/trained/tmp/",
                                best_model_save_path="agent/trained/tmp/")

    agent = SAC(LnMlpPolicy, env_train, verbose=1,
                ent_coef='auto', batch_size=512,
                learning_rate=constant(0.0003),
                train_freq=100,
                policy_kwargs=dict(layers=[32, 32]),
                )
    # agent = SAC.load(f"agent/trained/{get_task_tr_fail()[4]}_9VZ5VE.zip", env=env_train)
    agent.learn(total_timesteps=int(2e6), log_interval=50, callback=callback)
    agent.ID = get_ID(6) + f'_{env_eval.failure_input[0]}'
    training_log = pd.read_csv('agent/trained/tmp/monitor.csv')
    training_log.to_csv(f'agent/trained/{env_eval.task_fun()()[4]}_{agent.ID}.csv')
    plot_weights(agent.ID, env_eval.task_fun()()[4])
    plot_training(agent.ID, env_eval.task_fun()()[4])
    agent = SAC.load("agent/trained/tmp/best_model.zip", env=env_eval)
    agent.save(f'agent/trained/{env_eval.task_fun()()[4]}_{agent.ID}.zip')
    env_eval = Citation(evaluation=True)
    env_eval.render(agent=agent)

    return


def run_preexisting(ID=None):

    env_eval = Citation(evaluation=True, task=task)

    if ID is None:
        env_eval.render()
    else:
        agent = SAC.load(f"agent/trained/{env_eval.task_fun()()[4]}_{ID}.zip", env=env_eval)
        agent.ID = ID
        env_eval.render(agent=agent)


def keyboardInterruptHandler(signal, frame):
    print('')
    print('Early stopping. Getting last results...')
    run_preexisting()
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)
# learn()
# run_preexisting('9VZ5VE') # general, robust
# run_preexisting('R0EV0V_ht')

# run_preexisting('last')

# os.system('say "your program has finished"')
