import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def plot_response(name, env, task, perf, during_training=False, failure=None, FDD=False, broken=False):

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(
    #     x=env.time, y=env.ref_signal[0, :], name=r'$h [m]$',
    #     line=dict(color='#EF553B', dash='dashdot')))
    #

    subplot_indices = {0: [1, 2], 1: [1, 1], 3: [2, 2], 4: [2, 1], 5: [4, 2],
                       6: [3, 2], 7: [3, 1], 8: [7, 1], 9: [5, 1], 10: [7, 2], 11: [7, 2]}

    fig = make_subplots(rows=6, cols=2, vertical_spacing=0.2/6, horizontal_spacing=0.17/2)

    if broken:
        env.time = env.time[:env.step_count-2]
        env.state_history = env.state_history[:env.step_count-2]

    if env.external_ref_signal is not None:
        fig.append_trace(go.Scatter(
            x=env.time, y=env.external_ref_signal.T, name=r'$h [m]$',
            line=dict(color='#EF553B', dash='dashdot')), row=5, col=1)

        fig.append_trace(go.Scatter(
            x=env.time, y=env.ref_signal[0, :],
            line=dict(color='#EF553B')),
            row=3, col=1)

        fig.append_trace(go.Scatter(
            x=env.time, y=env.ref_signal[1, :],
            line=dict(color='#EF553B', dash='dashdot')),
            row=3, col=2)

        fig.append_trace(go.Scatter(
            x=env.time, y=env.ref_signal[2, :],
            line=dict(color='#EF553B', dash='dashdot')),
            row=4, col=2)

        fig.append_trace(go.Scatter(
            x=env.time, y=env.state_history[9, :].T - env.external_ref_signal.T, name=r'$h [m]$',
            line=dict(color='#636EFA')), row=4, col=1)
        fig.update_yaxes(title_text=r'$\Delta h \:\: [\text{m}]$', row=4, col=1, title_standoff=8,
                         # tickmode='array',
                         # tickvals=np.arange(-15, 5 + 5, 5),
                         # ticktext=['-15', ' ', '-5', ' ', '5'],
                         tickfont=dict(size=11),
                         # range=[-10, 10],
                         titlefont=dict(size=13)
                         )

    else:
        for sig_index, state_index in enumerate(task[1]):
            fig.append_trace(go.Scatter(
                x=env.time, y=env.ref_signal[sig_index, :],
                line=dict(color='#EF553B', dash='dashdot')),
                row=subplot_indices[state_index][0], col=subplot_indices[state_index][1])

    if env.task_fun()[4] == 'altitude_2attitude':

        fig.append_trace(go.Scatter(
            x=env.time, y=env.state_history[9, :].T-env.ref_signal[0, :], name=r'$h [m]$',
            line=dict(color='#636EFA')), row=4, col=1)

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[0, :].T, name=r'$p [\frac{deg}{s}]$',
        line=dict(color='#636EFA')), row=1, col=2)
    fig.update_yaxes(title_text=r'$p\:\: [\frac{\text{deg}}{\text{s}}]$', row=1, col=2, title_standoff=7,
                     tickfont=dict(size=11),
                     titlefont=dict(size=13),
                     tickmode='array',
                     tickvals=np.arange(-10, 10 + 5, 5),
                     ticktext=['-10', ' ', '0', ' ', '10'],
                     # range=[87,90.5],
                     )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[1, :].T, name=r'$q [^\circ/s]$',
        line=dict(color='#636EFA')), row=1, col=1)
    fig.update_yaxes(title_text=r'$q\:\: [\frac{\text{deg}}{\text{s}}]$', row=1, col=1, title_standoff=13,
                     tickmode='array',
                     tickvals=np.arange(-5, 5+2.5, 2.5),
                     ticktext=['-5',' ', '0',' ', '5'],
                     range=[-5, 5.5],
                     tickfont=dict(size=11),
                     titlefont=dict(size=13)
                     )

    # fig.append_trace(go.Scatter(
    #     x=env.time, y=env.state_history[2, :].T, name=r'$r [^\circ/s]$',
    #     line=dict(color='#636EFA')), row=2, col=2)
    # fig.update_yaxes(row=2, col=2, title_standoff=14,
    #                  tickmode='array',
    #                  tickvals=np.arange(-5, 5 + 2.5, 2.5),
    #                  range=[-5,7],
    #                  ticktext=['-5', ' ', '0', ' ', '5'],
    #                  title_text=r'$r\:\: [\frac{\text{deg}}{s}]$',
    #                  tickfont=dict(size=11),
    #                  titlefont=dict(size=13)
    #                  )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[3, :].T, name=r'$V [m/s]$',
        line=dict(color='#636EFA')), row=2, col=2)
    fig.update_yaxes(title_text=r'$V\:\: [\frac{\text{m}}{\text{s}}]$', row=2, col=2, title_standoff=13,
                     # tickmode='array',
                     # tickvals=np.arange(88, 90+1, 1),
                     # ticktext=['88', '89', '90'],
                     tickfont=dict(size=11),
                     # range=[87,90.5],
                     titlefont=dict(size=13)
                     )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[4, :].T, name=r'$\alpha [^\circ]$',
        line=dict(color='#636EFA')), row=2, col=1)
    fig.update_yaxes(title_text=r'$\alpha\:\: [\text{deg}]$', row=2, col=1, title_standoff=18,
                     # tickmode='array',
                     # tickvals=np.arange(2, 6+1, 1),
                     # ticktext=['2', ' ','4', ' ', '6'],
                     # range=[1.5, 6],
                     tickfont=dict(size=11),
                     titlefont=dict(size=13)
                     )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[5, :].T, name=r'$\beta [^\circ]$',
        line=dict(color='#636EFA')), row=4, col=2)
    fig.update_yaxes(title_text=r'$\beta\:\: [\text{deg}]$', row=4, col=2, title_standoff=14,
                     tickmode='array',
                     tickvals=np.arange(-1, 1 + 0.5, 0.5),
                     ticktext=['-1', ' ', '0', ' ', '1'],
                     range=[-1, 1],
                     tickfont=dict(size=11),
                     titlefont=dict(size=13)
                     )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[6, :].T, name=r'$\phi [^\circ]$',
        line=dict(color='#636EFA')), row=3, col=2)
    fig.update_yaxes(title_text=r'$\phi\:\: [\text{deg}]$', row=3, col=2, title_standoff=6,
                     tickmode='array',
                     tickvals=np.arange(-20, 20 + 10, 10),
                     ticktext=['-20', ' ', '0', ' ', '20'],
                     tickfont=dict(size=11),
                     range=[-23, 23],
                     titlefont=dict(size=13)
                     )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[7, :].T, name=r'$\theta [^\circ]$',
        line=dict(color='#636EFA')), row=3, col=1)
    fig.update_yaxes(title_text=r'$\theta\:\: [\text{deg}]$', row=3, col=1,
                     # tickmode='array',
                     # tickvals=np.arange(0, 10 + 2.5, 2.5),
                     # ticktext=['0', ' ', '5 ', ' ', '10'],
                     # range=[-16, 20.5],
                     tickfont=dict(size=11),
                     titlefont=dict(size=13)
                     )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.state_history[9, :].T, name=r'$h [m]$',
        line=dict(color='#636EFA')), row=5, col=1)
    fig.update_yaxes(title_text=r'$h\:\: [\text{m}]$', row=5, col=1, title_standoff=5,
                     tickmode='array',
                     tickvals=np.arange(2000, 2400 + 100, 100),
                     ticktext=['2000', ' ', '2200 ', ' ', '2400'],
                     range=[1980, 2400],
                     tickfont=dict(size=11),
                     titlefont=dict(size=13)
                     )

    # env.action_history = env.action_history_filtered

    fig.append_trace(go.Scatter(
        x=env.time, y=env.action_history[0, :].T,
        name=r'$\delta_e [^\circ]$', line=dict(color='#00CC96')), row=6, col=1)
    fig.update_yaxes(title_text=r'$\delta_\text{e} \:\:  [\text{deg}]$', row=6, col=1, title_standoff=20,
                     # tickmode='array',
                     # tickvals=np.arange(-4, 0 + 1, 1),
                     # ticktext=['-4', ' ', '-2', ' ', '0'],
                     tickfont=dict(size=11),
                     range=[-6, 0],
                     titlefont=dict(size=13)
                     )

    fig.append_trace(go.Scatter(
        x=env.time, y=env.action_history[1, :].T,
        name='&#948; [&deg;]', line=dict(color='#00CC96')), row=5, col=2)
    fig.update_yaxes(title_text=r'$\delta_\text{a} \:\:   [\text{deg}]$', row=5, col=2, title_standoff=8,
                     # tickmode='array',
                     # tickvals=np.arange(-5, 5 + 2.5, 2.5),
                     # ticktext=['-5', ' ', '0', ' ', '5'],
                     tickfont=dict(size=11),
                     # range=[-10, 7],
                     titlefont=dict(size=13)
                     )
    fig.append_trace(go.Scatter(
        x=env.time, y=env.action_history[2, :].T,
        name=r'$\delta_r [^\circ]$', line=dict(color='#00CC96')), row=6, col=2)
    fig.update_yaxes(title_text=r'$\delta_\text{r} \:\: [\text{deg}]$', row=6, col=2, title_standoff=13,
                     # tickmode='array',
                     # tickvals=np.arange(-5, 5 + 2.5, 2.5),
                     # ticktext=['-5', ' ', '0', ' ', '5'],
                     tickfont=dict(size=11),
                     # range=[-4, 3],
                     titlefont=dict(size=13)
                     )

    if failure != 'normal' and not during_training:
        fig.add_vline(x=env.failure_time, row='all', col="all", line=dict(color="Grey", width=1.5))

    if FDD:
        fig.add_vline(x=env.FDD_switch_time, row='all', col="all", line=dict(color="Grey", width=1.5, dash='dot'))

    fig.update_layout(showlegend=False, width=800, height=480, margin=dict(
        l=10,
        r=2,
        b=5,
        t=0,
    ))

    fig.layout.font.family = 'Arial'

    end_time = env.time[-1] + env.dt * 2

    if 9 in task[1]:
        tick_interval = 40
    else:
        tick_interval = 10

    fig.update_xaxes(title_text=r'$t \:\: \text{[s]}$', range=[0, end_time], tickmode='array',
                     tickvals=np.arange(0, end_time, tick_interval), tickfont=dict(size=11), row=6, col=1,
                     titlefont=dict(size=13), title_standoff=11)
    fig.update_xaxes(title_text=r'$t \:\: \text{[s]}$', range=[0, end_time], tickmode='array',
                     tickvals=np.arange(0, end_time, tick_interval), tickfont=dict(size=11), row=6, col=2,
                     titlefont=dict(size=13), title_standoff=11)

    for row in range(6):
        for col in range(3):
            fig.update_xaxes(showticklabels=False, tickmode='array',
                             tickvals=np.arange(0, end_time, tick_interval), row=row, col=col)

    fig.update_traces(mode='lines')
    if during_training:
        fig.write_image(f"figures/during_training/{env.task_fun()[4]}_r{abs(int(perf))}.eps")
    elif failure != 'normal':
        fig.write_image(f"figures/{name}_{failure}_r{abs(int(perf))}.pdf")
    else:
        fig.write_image(f"figures/{name}_r{abs(int(perf))}.pdf")
