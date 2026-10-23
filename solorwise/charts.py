"""Small Plotly chart builders kept separate from the Streamlit interface."""

import plotly.graph_objects as go

from calculator import HORIZON_YEARS, SolarScenario

GREEN = "#17634B"
GOLD = "#A27300"


def _style(figure: go.Figure, height: int) -> go.Figure:
    figure.update_layout(
        height=height,
        margin=dict(l=12, r=16, t=22, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=13, color="#183C31"),
        legend=dict(orientation="h", y=-0.22, x=0),
        hoverlabel=dict(bgcolor="white", font_color="#183C31"),
    )
    figure.update_xaxes(showgrid=False, zeroline=False)
    figure.update_yaxes(gridcolor="#E2E8DD", zeroline=False, rangemode="tozero")
    return figure


def monthly_bill_chart(scenario: SolarScenario) -> go.Figure:
    figure = go.Figure(go.Bar(
        x=["Current bill", "After solar · assumed"],
        y=[scenario.monthly_bill, scenario.new_monthly_bill],
        marker_color=["#7D8F82", GREEN],
        text=[f"RM {scenario.monthly_bill:,.2f}", f"RM {scenario.new_monthly_bill:,.2f}"],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{x}<br>RM %{y:,.2f} / month<extra></extra>",
    ))
    figure.update_layout(showlegend=False, bargap=0.5)
    figure.update_yaxes(title="Monthly bill (RM)", range=[0, max(scenario.monthly_bill * 1.25, 1)])
    return _style(figure, 320)


def cumulative_savings_chart(scenario: SolarScenario) -> go.Figure:
    years = list(range(HORIZON_YEARS + 1))
    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=years,
        y=scenario.cumulative_savings(),
        name="Cumulative gross savings",
        mode="lines",
        line=dict(color=GREEN, width=3),
        fill="tozeroy",
        fillcolor="rgba(23,99,75,0.08)",
        hovertemplate="Year %{x}<br>Gross savings: RM %{y:,.2f}<extra></extra>",
    ))
    figure.add_trace(go.Scatter(
        x=years,
        y=[scenario.installation_cost] * len(years),
        name="Upfront installation cost",
        mode="lines",
        line=dict(color=GOLD, width=2, dash="dash"),
        hovertemplate="Upfront cost: RM %{y:,.2f}<extra></extra>",
    ))
    payback = scenario.simple_payback_years
    if payback is not None and 0 <= payback <= HORIZON_YEARS:
        figure.add_trace(go.Scatter(
            x=[payback], y=[scenario.installation_cost],
            name="Simple payback", mode="markers",
            marker=dict(color=GREEN, size=11, symbol="diamond"),
            hovertemplate="Simple payback: %{x:.2f} years<extra></extra>",
        ))
    figure.update_xaxes(title="Years from installation", dtick=5, range=[0, HORIZON_YEARS])
    figure.update_yaxes(title="Amount (RM)")
    return _style(figure, 390)
