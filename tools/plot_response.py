import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from get_task import get_task


def plot_response(name, env, task, perf):
    subplot_indices = {0: [1, 2], 1: [1, 1], 2: [2, 2], 3: [4, 1], 4: [2, 1], 5: [4, 2],
                       6: [3, 2], 7: [3, 1], 8: [7, 1], 9: [5, 1], 10: [7, 2], 11: [7, 2]}

    fig = make_subplots(rows=6, cols=2)

    for sig_index, state_index in enumerate(task[1]):
        fig.append_trace(go.Scatter(
            x=env.time, y=env.ref_signal[sig_index, :],
            line=dict(color='#EF553B', dash='dashdot')),
            row=subplot_indices[state_index][0], col=subplot_indices[state_index][1])

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[0, :].T, name=r'$p [^\circ/s]$',
        line=dict(color='#636EFA')), row=1, col=2)
    fig.update_yaxes(title_text='p [&deg;/s]', row=1, col=2, title_standoff=0)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[1, :].T, name=r'$q [^\circ/s]$',
        line=dict(color='#636EFA')), row=1, col=1)
    fig.update_yaxes(title_text='q [&deg;/s]', row=1, col=1)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[2, :].T, name=r'$r [^\circ/s]$',
        line=dict(color='#636EFA')), row=2, col=2)
    fig.update_yaxes(title_text='r [&deg;/s]', row=2, col=2, title_standoff=6)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[3, :].T, name=r'$V [m/s]$',
        line=dict(color='#636EFA')), row=4, col=1)
    fig.update_yaxes(title_text='V [m/s]', row=4, col=1, title_standoff=23)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[4, :].T, name=r'$\alpha [^\circ]$',
        line=dict(color='#636EFA')), row=2, col=1)
    fig.update_yaxes(title_text='&#945; [&deg;]', row=2, col=1)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[5, :].T, name=r'$\beta [^\circ]$',
        line=dict(color='#636EFA')), row=4, col=2)
    fig.update_yaxes(title_text='&#946; [&deg;]', row=4, col=2, range=[-0.5, 0.5], title_standoff=0)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[6, :].T, name=r'$\phi [^\circ]$',
        line=dict(color='#636EFA')), row=3, col=2)
    fig.update_yaxes(title_text='&#966; [&deg;]', row=3, col=2, title_standoff=16)
    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[7, :].T, name=r'$\theta [^\circ]$',
        line=dict(color='#636EFA')), row=3, col=1)
    fig.update_yaxes(title_text='&#952; [&deg;]', row=3, col=1)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[9, :].T, name=r'$h [m]$',
        line=dict(color='#636EFA')), row=5, col=1)
    fig.update_yaxes(title_text='h [m]', row=5, col=1, title_standoff=8)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.action_history[0, :].T,
        name=r'$\delta_e [^\circ]$', line=dict(color='#00CC96')), row=6, col=1)
    fig.update_yaxes(title_text='&#948;<sub>e</sub> [&deg;]', row=6, col=1)
    fig.append_trace(go.Scatter(
        x=env.time, y=env.action_history[1, :].T,
        name='&#948; [&deg;]', line=dict(color='#00CC96')), row=5, col=2)
    fig.update_yaxes(title_text='&#948;<sub>a</sub> [&deg;]', row=5, col=2, title_standoff=5)
    fig.append_trace(go.Scatter(
        x=env.time, y=env.action_history[2, :].T,
        name=r'$\delta_r [^\circ]$', line=dict(color='#00CC96')), row=6, col=2)
    fig.update_yaxes(title_text='&#948;<sub>r</sub> [&deg;]', row=6, col=2, title_standoff=5)

    fig.update_layout(showlegend=False, width=800, height=500, margin=dict(
        l=10,
        r=10,
        b=10,
        t=10,
    ))

    end_time = env.time[-1] + env.dt * 2
    fig.update_xaxes(title_text="Time [s]", range=[0, end_time], tickmode='array',
                     tickvals=np.arange(0, end_time, 2.5), row=6, col=1)
    fig.update_xaxes(title_text="Time [s]", range=[0, end_time], tickmode='array',
                     tickvals=np.arange(0, end_time, 2.5), row=6, col=2)

    for row in range(6):
        for col in range(3):
            fig.update_xaxes(showticklabels=False, nticks=7, row=row, col=col)

    fig.update_traces(mode='lines')
    fig.write_image(f"figures/{get_task()[4]}_{name}_r{abs(int(perf))}.eps")


def get_response(env, agent, ID=None, during_training=False, verbose = 1):

    if during_training:
        ID = 'during_training'
        verbose = 0
    elif ID is None:
        agent.save(f'agent/trained/{get_task()[4]}_last.zip')
        ID = 'last'

    obs = env.reset()
    return_a = 0

    for i, current_time in enumerate(env.time):
        action, _ = agent.predict(obs, deterministic=True)
        if verbose > 0:
            print(action * 180 / np.pi)
        obs, reward, done, info = env.step(action)
        return_a += reward
        if current_time == env.time[-1]:
            plot_response(ID, env, get_task(), return_a)
            if verbose > 0:
                print(f"Goal reached! Return = {return_a:.2f}")
                print('')
            break