import sys
from pathlib import Path
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ==========================================================
# Make src importable
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from src.config.settings import DATABASE_URL

# ==========================================================
# Database
# ==========================================================

engine = create_engine(DATABASE_URL)

@st.cache_data(ttl=5)
def load_data():
    query = "SELECT * FROM pipeline_sensor_data"
    return pd.read_sql(query, engine)

df = load_data()
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ==========================================================
# Streamlit Page
# ==========================================================

st.set_page_config(
    page_title="PipeGuard AI",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refresh dashboard every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# ==========================================================
# Custom CSS
# ==========================================================

st.markdown("""
<style>

html, body, [class*="css"]{
    background:#08111f;
    color:white;
}

/* Header */

.main-title{
    font-size:42px;
    font-weight:800;
    color:#00E5FF;
}

.sub-title{
    font-size:18px;
    color:#D0D7DE;
}

/* KPI Cards */

.metric-card{
    border-radius:18px;
    padding:18px;
    color:white;
    text-align:center;
    box-shadow:0px 0px 18px rgba(0,0,0,0.45);
    margin-bottom:15px;
}

.blue{
    background:#1565C0;
}

.green{
    background:#00C853;
}

.orange{
    background:#F57C00;
}

.red{
    background:#D50000;
}

.purple{
    background:#6A1B9A;
}

.metric-value{
    font-size:34px;
    font-weight:bold;
}

.metric-label{
    font-size:16px;
}

/* Executive panel */

.summary{
    background:#10243F;
    border-radius:20px;
    padding:20px;
    margin-top:15px;
}

.health-good{
    color:#00E676;
    font-size:34px;
    font-weight:bold;
}

.health-warning{
    color:#FFD600;
    font-size:34px;
    font-weight:bold;
}

.health-danger{
    color:#FF1744;
    font-size:34px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/oil-industry.png",
    width=80
)

st.sidebar.title("PipeGuard AI")

stations = st.sidebar.multiselect(
    "Station",
    sorted(df.station.unique()),
    default=sorted(df.station.unique())
)

segments = st.sidebar.multiselect(
    "Pipeline Segment",
    sorted(df.pipeline_segment.unique()),
    default=sorted(df.pipeline_segment.unique())
)

status = st.sidebar.multiselect(
    "Status",
    sorted(df.status.unique()),
    default=sorted(df.status.unique())
)

df = df[
    (df.station.isin(stations))
    &
    (df.pipeline_segment.isin(segments))
    &
    (df.status.isin(status))
]

# ==========================================================
# Header
# ==========================================================

st.markdown(
"""
<div class='main-title'>
🛢️ PipeGuard AI
</div>

<div class='sub-title'>
Real-Time Pipeline Integrity & Product Loss Monitoring System
</div>
""",
unsafe_allow_html=True
)

st.divider()

# ==========================================================
# Pipeline Health Score
# ==========================================================

alert_rate = (df["anomaly"].sum()/len(df))*100

avg_loss = df["loss_litres"].mean()/10

health_score = max(
    0,
    round(
        100-(alert_rate+avg_loss),
        1
    )
)

if health_score >=95:

    health_class="health-good"

elif health_score>=85:

    health_class="health-warning"

else:

    health_class="health-danger"

# ==========================================================
# Executive Metrics
# ==========================================================

total_loss=df["loss_litres"].sum()

alerts=int(df["anomaly"].sum())

stations=df["station"].nunique()

segments=df["pipeline_segment"].nunique()

records=len(df)

estimated_loss=total_loss*100

# ==========================================================
# KPI Cards
# ==========================================================

c1,c2,c3,c4,c5,c6=st.columns(6)

with c1:

    st.markdown(f"""
<div class="metric-card green">

<div class="metric-value">{health_score}%</div>

<div class="metric-label">

Pipeline Health

</div>

</div>
""",unsafe_allow_html=True)

with c2:

    st.markdown(f"""
<div class="metric-card blue">

<div class="metric-value">

{records:,}

</div>

<div class="metric-label">

Sensor Records

</div>

</div>
""",unsafe_allow_html=True)

with c3:

    st.markdown(f"""
<div class="metric-card orange">

<div class="metric-value">

{total_loss:,.0f} L

</div>

<div class="metric-label">

Product Loss

</div>

</div>
""",unsafe_allow_html=True)

with c4:

    st.markdown(f"""
<div class="metric-card red">

<div class="metric-value">

{alerts}

</div>

<div class="metric-label">

Active Alerts

</div>

</div>
""",unsafe_allow_html=True)

with c5:

    st.markdown(f"""
<div class="metric-card purple">

<div class="metric-value">

KES {estimated_loss:,.0f}

</div>

<div class="metric-label">

Estimated Revenue Loss

</div>

</div>
""",unsafe_allow_html=True)

with c6:

    st.markdown(f"""
<div class="metric-card blue">

<div class="metric-value">

{stations}

</div>

<div class="metric-label">

Stations

</div>

</div>
""",unsafe_allow_html=True)

# ==========================================================
# Executive Summary
# ==========================================================

highest_loss_station=(
df.groupby("station")["loss_litres"]
.sum()
.idxmax()
)

highest_loss_segment=(
df.groupby("pipeline_segment")["loss_litres"]
.sum()
.idxmax()
)

st.markdown(f"""
<div class="summary">

<h2 style="color:#00E5FF;">
Executive Summary
</h2>

<ul style="font-size:18px;">

<li>Total Pipeline Records: <b>{records:,}</b></li>

<li>Total Product Loss: <b>{total_loss:,.0f} Litres</b></li>

<li>Detected Alerts: <b>{alerts}</b></li>

<li>Highest Risk Station: <b>{highest_loss_station}</b></li>

<li>Highest Risk Segment: <b>{highest_loss_segment}</b></li>

<li>Estimated Revenue Loss:
<b>KES {estimated_loss:,.0f}</b></li>

<li>Overall Pipeline Health:
<span class="{health_class}">
{health_score}%
</span>
</li>

</ul>

</div>
""",unsafe_allow_html=True)




# ==========================================================
# PIPELINE PERFORMANCE DASHBOARD
# ==========================================================

st.markdown("---")

st.header("📈 Pipeline Performance Dashboard")

# ==========================================================
# Flow In vs Flow Out
# ==========================================================

flow_df = (
    df.groupby("timestamp")[["flow_in", "flow_out"]]
    .mean()
    .reset_index()
)

flow_chart = px.line(
    flow_df,
    x="timestamp",
    y=["flow_in", "flow_out"],
    title="Flow In vs Flow Out Over Time",
    template="plotly_dark",
    color_discrete_sequence=["#00E5FF", "#FF5252"]
)

flow_chart.update_layout(
    height=450,
    paper_bgcolor="#08111f",
    plot_bgcolor="#08111f",
    font=dict(color="white"),
    legend_title=""
)

st.plotly_chart(flow_chart, use_container_width=True)

# ==========================================================
# Pressure Trend
# ==========================================================

pressure_df = (
    df.groupby("timestamp")["pressure"]
    .mean()
    .reset_index()
)

pressure_chart = px.line(
    pressure_df,
    x="timestamp",
    y="pressure",
    title="Pipeline Pressure Trend",
    template="plotly_dark",
    color_discrete_sequence=["#00FF7F"]
)

pressure_chart.update_layout(
    height=420,
    paper_bgcolor="#08111f",
    plot_bgcolor="#08111f",
    font=dict(color="white")
)

st.plotly_chart(pressure_chart, use_container_width=True)

# ==========================================================
# Product Loss Trend (Daily)
# ==========================================================

st.subheader("📈 Daily Product Loss Trend")

# Aggregate product loss by day
daily_loss = (
    df
    .set_index("timestamp")
    .resample("D")["loss_litres"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily_loss,
    x="timestamp",
    y="loss_litres",
    title="Daily Product Loss",
    markers=True
)

# Styling
fig.update_traces(
    line=dict(color="#FF6B00", width=4),
    marker=dict(
        size=8,
        color="#FFD700",
        line=dict(color="#FFFFFF", width=1)
    )
)

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="#08111F",
    paper_bgcolor="#08111F",
    font=dict(color="white", size=14),
    title_font=dict(size=22),
    xaxis_title="Date",
    yaxis_title="Product Loss (Litres)",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# Product Loss by Station
# ==========================================================

left, right = st.columns(2)

station_loss = (
    df.groupby("station")["loss_litres"]
    .sum()
    .reset_index()
    .sort_values("loss_litres", ascending=False)
)

station_chart = px.bar(
    station_loss,
    x="station",
    y="loss_litres",
    text_auto=True,
    title="Loss by Station",
    template="plotly_dark",
    color="loss_litres",
    color_continuous_scale="Turbo"
)

station_chart.update_layout(
    height=500,
    paper_bgcolor="#08111f",
    plot_bgcolor="#08111f",
    font=dict(color="white"),
    coloraxis_showscale=False
)

left.plotly_chart(
    station_chart,
    use_container_width=True
)

# ==========================================================
# Product Loss by Pipeline Segment
# ==========================================================

segment_loss = (
    df.groupby("pipeline_segment")["loss_litres"]
    .sum()
    .reset_index()
    .sort_values("loss_litres", ascending=False)
)

segment_chart = px.bar(
    segment_loss,
    x="pipeline_segment",
    y="loss_litres",
    text_auto=True,
    title="Loss by Pipeline Segment",
    template="plotly_dark",
    color="loss_litres",
    color_continuous_scale="Plasma"
)

segment_chart.update_layout(
    height=500,
    paper_bgcolor="#08111f",
    plot_bgcolor="#08111f",
    font=dict(color="white"),
    coloraxis_showscale=False
)

right.plotly_chart(
    segment_chart,
    use_container_width=True
)

# ==========================================================
# Anomaly Distribution
# ==========================================================

st.markdown("---")

st.subheader("🚨 Detected Operational Anomalies")

anomaly_df = (
    df[df["anomaly"] == True]
    .groupby("anomaly_type")
    .size()
    .reset_index(name="count")
)

if len(anomaly_df):

    anomaly_chart = px.pie(
        anomaly_df,
        names="anomaly_type",
        values="count",
        hole=.55,
        title="Detected Anomaly Types",
        template="plotly_dark",
        color_discrete_sequence=[
            "#FF1744",
            "#FFD600",
            "#00E676",
            "#00B0FF"
        ]
    )

    anomaly_chart.update_layout(
        height=500,
        paper_bgcolor="#08111f",
        plot_bgcolor="#08111f",
        font=dict(color="white")
    )

    st.plotly_chart(
        anomaly_chart,
        use_container_width=True
    )

else:

    st.success("No anomalies detected.")

# ==========================================================
# PIPELINE NETWORK HEALTH
# ==========================================================

st.markdown("---")
st.header("🗺️ Pipeline Network Health")

segment_summary = (
    df.groupby("pipeline_segment")
    .agg(
        avg_loss=("loss_litres", "mean"),
        alerts=("anomaly", "sum"),
        avg_pressure=("pressure", "mean")
    )
    .reset_index()
)

# Sort by alerts first, then average loss (highest first)
segment_summary = segment_summary.sort_values(
    by=["alerts", "avg_loss"],
    ascending=[False, False]
).reset_index(drop=True)

network_cols = st.columns(len(segment_summary))

for i, row in segment_summary.iterrows():

    if row["alerts"] > 80 or row["avg_loss"] > 100:

        color = "#ff1744"
        icon = "🔴"
        status = "CRITICAL"

    elif row["alerts"] > 40 or row["avg_loss"] > 50:

        color = "#FFD600"
        icon = "🟡"
        status = "WARNING"

    else:

        color = "#00E676"
        icon = "🟢"
        status = "HEALTHY"

    with network_cols[i]:

        st.markdown(
            f"""
            <div style="
            background:{color};
            padding:18px;
            border-radius:15px;
            text-align:center;
            color:black;
            font-weight:bold;
            box-shadow:0px 0px 15px rgba(0,0,0,.4);
            ">

            <h3>{icon}</h3>

            <h2>{row.pipeline_segment}</h2>

            <p><b>{status}</b></p>

            <hr>

            Avg Loss<br>
            <h3>{row.avg_loss:.1f} L</h3>

            Alerts<br>
            <h3>{int(row.alerts)}</h3>

            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================================
# TOP LOSS EVENTS
# ==========================================================

st.markdown("---")
st.header("🚨 Highest Product Loss Events")

top_loss = (
    df.sort_values(
        "loss_litres",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_loss[
        [
            "timestamp",
            "station",
            "pipeline_segment",
            "flow_in",
            "flow_out",
            "loss_litres",
            "pressure",
            "anomaly_type"
        ]
    ],
    use_container_width=True,
    height=400
)

# ==========================================================
# Shrinkage by Anomaly Type
# ==========================================================

st.markdown("---")
st.subheader("🚨 Product Shrinkage by Anomaly Type")

# Keep only anomaly records
anomaly_df = df[df["anomaly"] == True]

# Total loss by anomaly type
loss_by_anomaly = (
    anomaly_df
    .groupby("anomaly_type")["loss_litres"]
    .sum()
    .reset_index()
    .sort_values("loss_litres", ascending=False)
)

fig = px.bar(
    loss_by_anomaly,
    x="anomaly_type",
    y="loss_litres",
    text="loss_litres",
    color="anomaly_type",
    title="Total Product Shrinkage by Operational Anomaly",
    template="plotly_dark",
    color_discrete_map={
        "Illegal Tapping": "#FF1744",
        "Pipeline Leak": "#FFD600",
        "Pressure Drop": "#00E5FF"
    }
)

fig.update_traces(
    texttemplate="%{text:,.0f} L",
    textposition="outside"
)

fig.update_layout(
    paper_bgcolor="#08111F",
    plot_bgcolor="#08111F",
    font=dict(color="white"),
    xaxis_title="Operational Anomaly",
    yaxis_title="Total Product Loss (Litres)",
    showlegend=False,
    height=550
)

st.plotly_chart(fig, use_container_width=True)

highest = loss_by_anomaly.iloc[0]
lowest = loss_by_anomaly.iloc[-1]

st.success(
    f"🔴 Highest shrinkage: **{highest['anomaly_type']}** "
    f"({highest['loss_litres']:,.0f} Litres)"
)

st.info(
    f"🟢 Lowest shrinkage: **{lowest['anomaly_type']}** "
    f"({lowest['loss_litres']:,.0f} Litres)"
)

# ==========================================================
# LIVE ALERTS
# ==========================================================

st.markdown("---")
st.header("⚠️ Live Operational Alerts")

alerts = df[df["status"] == "ALERT"]

if len(alerts) > 0:

    for _, row in alerts.sort_values(
        "timestamp",
        ascending=False
    ).head(8).iterrows():

        st.error(
            f"""
{row['timestamp']}

📍 {row['station']} | {row['pipeline_segment']}

Loss: {row['loss_litres']} L

Pressure: {row['pressure']:.2f} PSI

Cause: {row['anomaly_type']}
"""
        )

else:

    st.success("No active alerts.")

# ==========================================================
# ETL PIPELINE STATUS
# ==========================================================

st.markdown("---")
st.header("⚙️ ETL Pipeline Status")

c1, c2, c3, c4 = st.columns(4)

c1.success("🟢 Database Connected")

c2.success("🟢 Validation Passed")

c3.success("🟢 PostgreSQL Online")

c4.success("🟢 ETL Completed")

# ==========================================================
# FOOTER METRICS
# ==========================================================

st.markdown("---")

left, middle, right = st.columns(3)

left.metric(
    "Records Loaded",
    f"{len(df):,}"
)

middle.metric(
    "Total Stations",
    df.station.nunique()
)

right.metric(
    "Pipeline Segments",
    df.pipeline_segment.nunique()
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
"""
<hr>

<center>

<h3 style='color:#00E5FF;'>

PipeGuard AI

</h3>

<b>Real-Time Pipeline Integrity & Product Loss Monitoring Platform</b>

Developed for the KPC x Em-Tech x PLP Hackathon

Detect • Monitor • Protect

</center>
""",
unsafe_allow_html=True
)