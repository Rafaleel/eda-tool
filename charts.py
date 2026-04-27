import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def _to_html(fig) -> str:
    return fig.to_html(full_html=False, include_plotlyjs=False)


def _apply_dark(fig):
    """Aplica tema escuro sem quebrar configurações de eixos existentes."""
    fig.update_layout(
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#0f0f1a",
        font=dict(color="#e0e0e0"),
    )
    fig.update_xaxes(gridcolor="#2a2a4a", linecolor="#2a2a4a", zerolinecolor="#2a2a4a")
    fig.update_yaxes(gridcolor="#2a2a4a", linecolor="#2a2a4a", zerolinecolor="#2a2a4a")
    return fig


def plot_missing(df: pd.DataFrame) -> str:
    missing = df.isnull().mean().mul(100).round(2)
    missing = missing[missing > 0].sort_values(ascending=True)

    x_vals = missing.values.tolist()
    y_vals = missing.index.tolist()

    fig = go.Figure(go.Bar(
        x=x_vals,
        y=y_vals,
        orientation="h",
        marker_color=["#e94560" if v > 50 else "#4361ee" for v in x_vals],
        text=[f"{v}%" for v in x_vals],
        textposition="outside",
    ))
    fig.update_layout(
        title="Missing Values (%)",
        xaxis_title="Missing %",
        xaxis=dict(range=[0, 110]),
    )
    _apply_dark(fig)
    return _to_html(fig)


def plot_distributions(df: pd.DataFrame, numeric_cols: list) -> list:
    charts = []
    for col in numeric_cols:
        data = df[col].dropna().tolist()

        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=30,
            marker_color="#4361ee",
            opacity=0.85,
            name=col,
        ))
        fig.update_layout(
            title=f"Distribution — {col}",
            xaxis_title=col,
            yaxis_title="Count",
            bargap=0.05,
            paper_bgcolor="#1a1a2e",
            plot_bgcolor="#0f0f1a",
            font=dict(color="#e0e0e0"),
            xaxis=dict(gridcolor="#2a2a4a", linecolor="#2a2a4a"),
            yaxis=dict(gridcolor="#2a2a4a", linecolor="#2a2a4a"),
        )
        charts.append({"column": col, "chart": _to_html(fig)})
    return charts


def plot_correlation(corr_columns: list, corr_values: list) -> str:
    if not corr_columns:
        return ""

    n = len(corr_columns)
    cell_size = 80
    fig_size = n * cell_size + 100

    font_colors = []
    for row in corr_values:
        row_colors = []
        for v in row:
            row_colors.append("#111111" if abs(v) < 0.4 else "#ffffff")
        font_colors.append(row_colors)

    fig = ff.create_annotated_heatmap(
        z=corr_values,
        x=corr_columns,
        y=corr_columns,
        colorscale="RdBu",
        reversescale=True,
        showscale=True,
        zmid=0,
        annotation_text=[[f"{v:.2f}" for v in row] for row in corr_values],
    )

    for i, annotation in enumerate(fig.layout.annotations):
        row = i // n
        col = i % n
        annotation.font.size = 12
        annotation.font.color = font_colors[row][col]

    fig.update_layout(
        title="Correlation Matrix",
        width=fig_size,
        height=fig_size,
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#0f0f1a",
        font=dict(color="#e0e0e0", size=13),
    )
    return _to_html(fig)


def plot_categoricals(categorical: list) -> list:
    charts = []
    for cat in categorical:
        fig = go.Figure(go.Bar(
            x=cat["top_counts"],
            y=cat["top_values"],
            orientation="h",
            marker_color="#4361ee",
        ))
        fig.update_layout(
            title=f"Top Values — {cat['column']}",
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Count",
        )
        _apply_dark(fig)
        charts.append({"column": cat["column"], "chart": _to_html(fig)})
    return charts


def generate_all_charts(df: pd.DataFrame, analysis: dict) -> dict:
    charts = {}

    if analysis["nulls"]:
        charts["missing"] = plot_missing(df)
    else:
        charts["missing"] = ""

    charts["distributions"] = plot_distributions(df, analysis["numeric_cols"])

    charts["correlation"] = plot_correlation(
        analysis["corr_columns"],
        analysis["corr_values"]
    )

    charts["categoricals"] = plot_categoricals(analysis["categorical"])

    return charts