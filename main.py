import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Superinvestor Analytics Dashboard | BQuantFinance",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 0rem;
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Card styling */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: white !important;
        font-weight: bold;
        font-size: 1.8rem;
    }
    
    /* Headers styling */
    h1 {
        background: linear-gradient(90deg, #00d2ff 0%, #3a47d5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        padding: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    h2 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    h3 {
        color: #667eea;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #667eea;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 12px 30px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        font-weight: 700;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: 2px solid white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Attribution styling */
    .attribution {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* SelectBox styling */
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Radio button styling */
    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px;
        transition: all 0.3s ease;
    }
    
    div[role="radiogroup"] label:hover {
        background: rgba(102, 126, 234, 0.3);
        transform: translateX(5px);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    """Load and preprocess the data"""
    df = pd.read_csv('dataroma_holdings_complete.csv')
    
    # Clean numeric columns
    numeric_cols = ['% of Portfolio', 'Shares']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Clean Value column (remove $ and commas)
    if 'Value' in df.columns:
        df['Value_Clean'] = df['Value'].str.replace(r'[$,]', '', regex=True)
        df['Value_Clean'] = pd.to_numeric(df['Value_Clean'], errors='coerce')
    
    # Extract activity type and percentage
    df['Activity_Type'] = df['RecentActivity'].apply(lambda x: 
        'Buy' if pd.isna(x) else 
        'Buy' if x == 'Buy' else
        'Add' if 'Add' in str(x) else 
        'Reduce' if 'Reduce' in str(x) else 
        'Hold'
    )
    
    df['Activity_Percentage'] = df['RecentActivity'].apply(lambda x: 
        float(re.findall(r'[\d.]+', str(x))[0]) if pd.notna(x) and re.findall(r'[\d.]+', str(x)) else 0
    )
    
    # Extract stock ticker
    df['Ticker'] = df['Stock'].apply(lambda x: x.split(' - ')[0] if pd.notna(x) and ' - ' in x else x)
    df['Company'] = df['Stock'].apply(lambda x: x.split(' - ')[1] if pd.notna(x) and ' - ' in x else x)
    
    return df

# Load the data
df = load_data()

# Title with gradient and attribution
st.markdown("<h1>🚀 Superinvestor Portfolio Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
    <div class='attribution'>
        Made by @Gsnchez - BQuantFinance.com 📈
    </div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0; font-size: 1.3rem; margin-bottom: 2rem;'>Analyzing holdings from 81 legendary investors with advanced visualizations</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎨 Dashboard Controls")
    st.markdown("---")
    
    # View selection with icons
    view_mode = st.radio(
        "Select Analysis View",
        ["🌐 3D Overview", "🎯 Portfolio Intelligence", "🔥 Hot Stocks Matrix", 
         "📊 Advanced Analytics", "🕸️ Network Analysis", "👤 Investor Deep Dive", "🎭 Comparative Analysis"],
        index=0
    )
    
    st.markdown("---")
    
    # Filter controls based on view
    if view_mode == "👤 Investor Deep Dive":
        selected_investor = st.selectbox(
            "🎯 Select Investor",
            sorted(df['Investor'].unique()),
            index=0
        )
    
    if view_mode == "🎭 Comparative Analysis":
        selected_investors = st.multiselect(
            "📊 Select Investors to Compare",
            sorted(df['Investor'].unique()),
            default=sorted(df['Investor'].unique())[:3]
        )
    
    # Activity filter
    st.markdown("### 🔧 Global Filters")
    activity_filter = st.multiselect(
        "Filter by Activity Type",
        ["Buy", "Add", "Reduce", "Hold"],
        default=["Buy", "Add", "Reduce", "Hold"]
    )
    
    # Portfolio size filter
    min_portfolio = st.slider(
        "Minimum Portfolio %",
        0.0, 50.0, 0.0, 0.5
    )
    
    # Add info
    st.markdown("---")
    st.info("💡 Tip: Use 3D plots to explore multi-dimensional relationships in the data!")

# Filter data based on sidebar selections
filtered_df = df[df['Activity_Type'].isin(activity_filter)]
filtered_df = filtered_df[filtered_df['% of Portfolio'] >= min_portfolio]

# Main content area based on view selection
if view_mode == "🌐 3D Overview":
    # 3D Overview with multiple advanced visualizations
    st.markdown("## 🌐 3D Portfolio Universe", unsafe_allow_html=True)
    
    # Key metrics with gradient cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Investors", f"{df['Investor'].nunique()}", delta="📊")
    with col2:
        st.metric("Unique Stocks", f"{df['Stock'].nunique()}", delta="📈")
    with col3:
        total_value = df['Value_Clean'].sum() / 1e9
        st.metric("Total Value", f"${total_value:.1f}B", delta="💰")
    with col4:
        avg_holdings = len(df) / df['Investor'].nunique()
        st.metric("Avg Holdings", f"{avg_holdings:.0f}", delta="🎯")
    with col5:
        concentration = df.groupby('Investor')['% of Portfolio'].apply(lambda x: x.nlargest(5).sum()).mean()
        st.metric("Avg Top5 Conc.", f"{concentration:.1f}%", delta="🔥")
    
    st.markdown("---")
    
    # Create tabs for different 3D visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🌌 3D Scatter Universe", "🎨 Sunburst Chart", "🌍 3D Surface Plot", "🎪 Funnel Analysis"])
    
    with tab1:
        st.markdown("### 🌌 3D Portfolio Universe - Interactive Explorer")
        
        # Prepare data for 3D scatter
        investor_stats = filtered_df.groupby('Investor').agg({
            'Stock': 'count',
            'Value_Clean': 'sum',
            '% of Portfolio': lambda x: x.nlargest(1).values[0] if len(x) > 0 else 0,
            'Activity_Type': lambda x: (x == 'Buy').sum() + (x == 'Add').sum()
        }).rename(columns={
            'Stock': 'Num_Holdings',
            'Value_Clean': 'Total_Value',
            '% of Portfolio': 'Top_Holding_Pct',
            'Activity_Type': 'Buy_Add_Count'
        })
        
        # Create 3D scatter plot
        fig_3d = px.scatter_3d(
            investor_stats.reset_index(),
            x='Num_Holdings',
            y='Top_Holding_Pct',
            z='Total_Value',
            color='Buy_Add_Count',
            size='Total_Value',
            hover_data=['Investor'],
            color_continuous_scale='Viridis',
            title='3D Investor Universe (Size = Portfolio Value)',
            labels={
                'Num_Holdings': 'Number of Holdings',
                'Top_Holding_Pct': 'Top Holding %',
                'Total_Value': 'Portfolio Value',
                'Buy_Add_Count': 'Recent Buys/Adds'
            }
        )
        
        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="white", showbackground=True),
                yaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="white", showbackground=True),
                zaxis=dict(backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="white", showbackground=True),
            ),
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)
    
    with tab2:
        st.markdown("### 🎨 Portfolio Composition Sunburst")
        
        # Get top investors and their top holdings
        top_investors = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index
        sunburst_data = filtered_df[filtered_df['Investor'].isin(top_investors)].copy()
        sunburst_data = sunburst_data.groupby(['Investor', 'Stock']).agg({
            'Value_Clean': 'sum',
            '% of Portfolio': 'first'
        }).reset_index()
        
        # Filter top holdings per investor for clarity
        sunburst_filtered = []
        for investor in top_investors:
            investor_data = sunburst_data[sunburst_data['Investor'] == investor].nlargest(10, 'Value_Clean')
            sunburst_filtered.append(investor_data)
        sunburst_final = pd.concat(sunburst_filtered)
        
        fig_sunburst = px.sunburst(
            sunburst_final,
            path=['Investor', 'Stock'],
            values='Value_Clean',
            color='% of Portfolio',
            color_continuous_scale='RdYlBu_r',
            title='Interactive Portfolio Sunburst (Click to Zoom)',
        )
        
        fig_sunburst.update_layout(
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    with tab3:
        st.markdown("### 🌍 3D Surface - Portfolio Concentration Landscape")
        
        # Create concentration matrix
        concentration_matrix = filtered_df.pivot_table(
            values='% of Portfolio',
            index='Investor',
            columns='Activity_Type',
            aggfunc='mean',
            fill_value=0
        )
        
        # Create surface plot
        fig_surface = go.Figure(data=[go.Surface(
            z=concentration_matrix.values,
            x=concentration_matrix.columns,
            y=concentration_matrix.index,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Avg Portfolio %")
        )])
        
        fig_surface.update_layout(
            title='Activity Concentration Surface',
            scene=dict(
                xaxis_title='Activity Type',
                yaxis_title='Investor',
                zaxis_title='Avg Portfolio %',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_surface, use_container_width=True)
    
    with tab4:
        st.markdown("### 🎪 Portfolio Funnel Analysis")
        
        # Create funnel data
        funnel_data = filtered_df.groupby('Activity_Type')['Value_Clean'].sum().reset_index()
        funnel_data = funnel_data.sort_values('Value_Clean', ascending=False)
        
        fig_funnel = px.funnel(
            funnel_data,
            y='Activity_Type',
            x='Value_Clean',
            color='Activity_Type',
            color_discrete_map={
                'Buy': '#10B981',
                'Add': '#60A5FA',
                'Reduce': '#F87171',
                'Hold': '#9CA3AF'
            },
            title='Activity Value Funnel'
        )
        
        fig_funnel.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True)

elif view_mode == "🎯 Portfolio Intelligence":
    st.markdown("## 🎯 Advanced Portfolio Intelligence", unsafe_allow_html=True)
    
    # Create sub-tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["🎨 Portfolio Diversity", "📊 Concentration Analysis", "🔮 Pattern Recognition"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🍕 Top 20 Stocks - Enhanced Pie")
            
            top_stocks = filtered_df.groupby('Stock').agg({
                'Investor': 'nunique',
                'Value_Clean': 'sum'
            }).nlargest(20, 'Value_Clean')
            
            fig_pie = px.pie(
                values=top_stocks['Value_Clean'],
                names=top_stocks.index,
                title='Top 20 Stocks by Total Value',
                hole=0.4
            )
            
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Value: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
            )
            
            fig_pie.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Investor Diversity Score")
            
            # Calculate diversity score
            diversity_scores = filtered_df.groupby('Investor').apply(
                lambda x: pd.Series({
                    'Num_Stocks': x['Stock'].nunique(),
                    'HHI': (x['% of Portfolio'] ** 2).sum(),  # Herfindahl index
                    'Top5_Concentration': x.nlargest(5, '% of Portfolio')['% of Portfolio'].sum()
                })
            ).reset_index()
            
            diversity_scores['Diversity_Score'] = (
                (diversity_scores['Num_Stocks'] / diversity_scores['Num_Stocks'].max()) * 40 +
                ((1 - diversity_scores['HHI'] / 10000) * 100) * 30 +
                ((100 - diversity_scores['Top5_Concentration']) / 100 * 100) * 30
            )
            
            fig_diversity = px.scatter(
                diversity_scores.nlargest(20, 'Diversity_Score'),
                x='Num_Stocks',
                y='Diversity_Score',
                size='Top5_Concentration',
                color='Diversity_Score',
                hover_data=['Investor'],
                color_continuous_scale='Turbo',
                title='Portfolio Diversity Analysis'
            )
            
            fig_diversity.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_diversity, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 Advanced Concentration Metrics")
        
        # Create radar chart for top investors
        top_investors_radar = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(6).index
        
        radar_data = []
        for investor in top_investors_radar:
            investor_df = filtered_df[filtered_df['Investor'] == investor]
            radar_data.append({
                'Investor': investor,
                'Holdings': min(investor_df['Stock'].nunique() / 50 * 100, 100),
                'Top1': investor_df['% of Portfolio'].max(),
                'Avg_Position': investor_df['% of Portfolio'].mean() * 10,
                'Buy_Activity': (investor_df['Activity_Type'].isin(['Buy', 'Add'])).sum() / len(investor_df) * 100,
                'Value': min(investor_df['Value_Clean'].sum() / 1e8, 100)  # Scale to 100
            })
        
        fig_radar = go.Figure()
        
        categories = ['Holdings', 'Top1', 'Avg_Position', 'Buy_Activity', 'Value']
        
        for item in radar_data:
            fig_radar.add_trace(go.Scatterpolar(
                r=[item[cat] for cat in categories],
                theta=categories,
                fill='toself',
                name=item['Investor'][:20]
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Investor Profile Radar Chart",
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab3:
        st.markdown("### 🔮 Trading Pattern Recognition")
        
        # Analyze trading patterns
        pattern_data = filtered_df.groupby(['Investor', 'Activity_Type']).size().unstack(fill_value=0)
        pattern_data['Aggressiveness'] = (pattern_data.get('Buy', 0) + pattern_data.get('Add', 0)) / (pattern_data.sum(axis=1) + 1) * 100
        pattern_data = pattern_data.sort_values('Aggressiveness', ascending=False).head(20)
        
        fig_pattern = px.bar(
            pattern_data.reset_index(),
            x='Investor',
            y='Aggressiveness',
            color='Aggressiveness',
            color_continuous_scale='RdYlGn',
            title='Trading Aggressiveness Score (Buy+Add Activity %)'
        )
        
        fig_pattern.update_layout(
            height=500,
            xaxis_tickangle=-45,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=10)
        )
        
        st.plotly_chart(fig_pattern, use_container_width=True)

elif view_mode == "🔥 Hot Stocks Matrix":
    st.markdown("## 🔥 Advanced Hot Stocks Matrix", unsafe_allow_html=True)
    
    # Calculate comprehensive metrics
    stock_metrics = filtered_df.groupby('Stock').agg({
        'Investor': 'nunique',
        'Value_Clean': 'sum',
        '% of Portfolio': ['mean', 'max'],
        'Activity_Type': lambda x: (x.isin(['Buy', 'Add'])).sum(),
        'Activity_Percentage': 'mean'
    })
    
    stock_metrics.columns = ['Num_Investors', 'Total_Value', 'Avg_Portfolio', 'Max_Portfolio', 'Buy_Add_Count', 'Avg_Activity']
    
    # Calculate heat score with multiple factors
    stock_metrics['Heat_Score'] = (
        stock_metrics['Num_Investors'] / stock_metrics['Num_Investors'].max() * 30 +
        stock_metrics['Total_Value'] / stock_metrics['Total_Value'].max() * 25 +
        stock_metrics['Avg_Portfolio'] / stock_metrics['Avg_Portfolio'].max() * 20 +
        stock_metrics['Buy_Add_Count'] / stock_metrics['Buy_Add_Count'].max() * 15 +
        stock_metrics['Max_Portfolio'] / stock_metrics['Max_Portfolio'].max() * 10
    ) * 100
    
    hot_stocks = stock_metrics.sort_values('Heat_Score', ascending=False).head(30)
    
    # Create 3D bubble chart
    fig_3d_bubble = px.scatter_3d(
        hot_stocks.reset_index(),
        x='Num_Investors',
        y='Avg_Portfolio',
        z='Total_Value',
        size='Heat_Score',
        color='Heat_Score',
        hover_data=['Stock', 'Buy_Add_Count'],
        color_continuous_scale='Hot_r',
        title='3D Hot Stocks Universe'
    )
    
    fig_3d_bubble.update_layout(
        scene=dict(
            xaxis_title='Number of Investors',
            yaxis_title='Avg Portfolio %',
            zaxis_title='Total Value',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
        ),
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_3d_bubble, use_container_width=True)
    
    # Heatmap of top stocks vs top investors
    st.markdown("### 🌡️ Stock-Investor Heatmap")
    
    top_stocks_hm = hot_stocks.head(20).index
    top_investors_hm = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(15).index
    
    heatmap_data = filtered_df[
        (filtered_df['Stock'].isin(top_stocks_hm)) & 
        (filtered_df['Investor'].isin(top_investors_hm))
    ].pivot_table(
        values='% of Portfolio',
        index='Stock',
        columns='Investor',
        fill_value=0
    )
    
    fig_heatmap = px.imshow(
        heatmap_data,
        color_continuous_scale='Turbo',
        title='Portfolio Weight Heatmap (Top Stocks vs Top Investors)',
        labels=dict(color="Portfolio %"),
        aspect='auto'
    )
    
    fig_heatmap.update_layout(
        height=600,
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=9)
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

elif view_mode == "📊 Advanced Analytics":
    st.markdown("## 📊 Advanced Statistical Analysis", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "🎲 Distribution Analysis", "🔄 Correlation Matrix"])
    
    with tab1:
        st.markdown("### 📈 Activity Trend Analysis")
        
        # Create activity timeline
        activity_summary = filtered_df.groupby(['Investor', 'Activity_Type']).size().unstack(fill_value=0)
        
        # Calculate trend metrics
        trend_data = pd.DataFrame({
            'Investor': activity_summary.index,
            'Buy_Ratio': (activity_summary.get('Buy', 0) + activity_summary.get('Add', 0)) / activity_summary.sum(axis=1) * 100,
            'Total_Actions': activity_summary.sum(axis=1)
        })
        
        fig_trend = px.scatter(
            trend_data,
            x='Total_Actions',
            y='Buy_Ratio',
            size='Total_Actions',
            color='Buy_Ratio',
            hover_data=['Investor'],
            color_continuous_scale='RdYlGn',
            title='Buy/Add Sentiment vs Activity Level'
        )
        
        fig_trend.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with tab2:
        st.markdown("### 🎲 Portfolio Distribution Analysis")
        
        # Create violin plot for portfolio distributions
        top_investors_dist = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index
        dist_data = filtered_df[filtered_df['Investor'].isin(top_investors_dist)]
        
        fig_violin = px.violin(
            dist_data,
            y='Investor',
            x='% of Portfolio',
            color='Activity_Type',
            box=True,
            title='Portfolio Weight Distribution by Investor',
            orientation='h'
        )
        
        fig_violin.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_violin, use_container_width=True)
    
    with tab3:
        st.markdown("### 🔄 Investor Correlation Matrix")
        
        # Create correlation matrix based on common holdings
        top_investors_corr = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(15).index
        
        corr_pivot = filtered_df[filtered_df['Investor'].isin(top_investors_corr)].pivot_table(
            values='% of Portfolio',
            index='Stock',
            columns='Investor',
            fill_value=0
        )
        
        correlation_matrix = corr_pivot.corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            color_continuous_scale='RdBu',
            title='Investor Portfolio Correlation',
            labels=dict(color="Correlation"),
            zmin=-1,
            zmax=1
        )
        
        fig_corr.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)

elif view_mode == "🕸️ Network Analysis":
    st.markdown("## 🕸️ Investor Network Analysis", unsafe_allow_html=True)
    
    # Create network data
    st.markdown("### 🌐 Common Holdings Network")
    
    # Find stocks held by multiple investors
    multi_investor_stocks = filtered_df.groupby('Stock')['Investor'].nunique()
    multi_investor_stocks = multi_investor_stocks[multi_investor_stocks >= 2].index
    
    network_data = filtered_df[filtered_df['Stock'].isin(multi_investor_stocks)]
    
    # Create chord diagram data
    chord_data = []
    investors = network_data['Investor'].unique()[:20]  # Limit to top 20 for clarity
    
    for i, inv1 in enumerate(investors):
        for j, inv2 in enumerate(investors):
            if i < j:
                inv1_stocks = set(network_data[network_data['Investor'] == inv1]['Stock'])
                inv2_stocks = set(network_data[network_data['Investor'] == inv2]['Stock'])
                common = len(inv1_stocks.intersection(inv2_stocks))
                if common > 0:
                    chord_data.append({'source': inv1, 'target': inv2, 'value': common})
    
    # Create Sankey diagram
    chord_df = pd.DataFrame(chord_data)
    
    if not chord_df.empty:
        # Get unique nodes
        nodes = list(set(chord_df['source'].unique()) | set(chord_df['target'].unique()))
        node_indices = {node: i for i, node in enumerate(nodes)}
        
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color='rgba(102, 126, 234, 0.8)'
            ),
            link=dict(
                source=[node_indices[s] for s in chord_df['source']],
                target=[node_indices[t] for t in chord_df['target']],
                value=chord_df['value'],
                color='rgba(102, 126, 234, 0.3)'
            )
        )])
        
        fig_sankey.update_layout(
            title="Investor Common Holdings Network",
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=10)
        )
        
        st.plotly_chart(fig_sankey, use_container_width=True)

elif view_mode == "👤 Investor Deep Dive":
    # Individual investor analysis with advanced visualizations
    investor_df = filtered_df[filtered_df['Investor'] == selected_investor].copy()
    
    st.markdown(f"## 🎭 {selected_investor} - Complete Portfolio Analysis", unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Holdings", f"{len(investor_df)}")
    with col2:
        total_value = investor_df['Value_Clean'].sum() / 1e6
        st.metric("Portfolio Value", f"${total_value:.1f}M")
    with col3:
        top_holding = investor_df.nlargest(1, '% of Portfolio')['% of Portfolio'].values[0]
        st.metric("Top Holding", f"{top_holding:.1f}%")
    with col4:
        concentration = investor_df.nlargest(5, '% of Portfolio')['% of Portfolio'].sum()
        st.metric("Top 5 Conc.", f"{concentration:.1f}%")
    with col5:
        buy_ratio = (investor_df['Activity_Type'].isin(['Buy', 'Add'])).sum() / len(investor_df) * 100
        st.metric("Buy/Add Ratio", f"{buy_ratio:.1f}%")
    
    st.markdown("---")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🍩 Portfolio Donut", "📊 3D Composition", "🎯 Activity Analysis", "📈 Holdings Table"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced donut chart
            fig_donut = px.pie(
                investor_df.nlargest(15, '% of Portfolio'),
                values='% of Portfolio',
                names='Stock',
                title=f'Top 15 Holdings',
                hole=0.6
            )
            
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Portfolio: %{percent}<br>Value: %{value:.2f}%<extra></extra>'
            )
            
            # Add center text
            fig_donut.add_annotation(
                text=f"{len(investor_df)}<br>Holdings",
                x=0.5, y=0.5,
                font=dict(size=20, color='white'),
                showarrow=False
            )
            
            fig_donut.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        
        with col2:
            # Activity breakdown pie
            activity_counts = investor_df['Activity_Type'].value_counts()
            
            fig_activity = px.pie(
                values=activity_counts.values,
                names=activity_counts.index,
                title='Activity Distribution',
                color_discrete_map={
                    'Buy': '#10B981',
                    'Add': '#60A5FA',
                    'Reduce': '#F87171',
                    'Hold': '#9CA3AF'
                },
                hole=0.4
            )
            
            fig_activity.update_traces(
                textposition='inside',
                textinfo='percent+label'
            )
            
            fig_activity.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_activity, use_container_width=True)
    
    with tab2:
        # 3D bar chart
        top_3d = investor_df.nlargest(20, '% of Portfolio')
        
        fig_3d_bar = px.bar(
            top_3d,
            x='Stock',
            y='% of Portfolio',
            color='Activity_Type',
            title='Top 20 Holdings with Activity',
            color_discrete_map={
                'Buy': '#10B981',
                'Add': '#60A5FA',
                'Reduce': '#F87171',
                'Hold': '#9CA3AF'
            }
        )
        
        fig_3d_bar.update_layout(
            height=500,
            xaxis_tickangle=-45,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=9)
        )
        
        st.plotly_chart(fig_3d_bar, use_container_width=True)
    
    with tab3:
        # Treemap of portfolio
        fig_treemap = px.treemap(
            investor_df,
            path=['Activity_Type', 'Stock'],
            values='% of Portfolio',
            color='Activity_Percentage',
            color_continuous_scale='RdYlGn',
            title='Portfolio Treemap by Activity'
        )
        
        fig_treemap.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    with tab4:
        # Enhanced table
        display_cols = ['Stock', '% of Portfolio', 'Shares', 'Value', 'RecentActivity', 'Activity_Type']
        display_df = investor_df[display_cols].sort_values('% of Portfolio', ascending=False)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=500,
            hide_index=True,
            column_config={
                "% of Portfolio": st.column_config.ProgressColumn(
                    "Portfolio %",
                    format="%.2f%%",
                    min_value=0,
                    max_value=display_df['% of Portfolio'].max(),
                ),
                "Shares": st.column_config.NumberColumn(
                    "Shares",
                    format="%d",
                ),
            }
        )

elif view_mode == "🎭 Comparative Analysis":
    st.markdown("## 🎭 Comparative Portfolio Analysis", unsafe_allow_html=True)
    
    if selected_investors:
        comparison_df = filtered_df[filtered_df['Investor'].isin(selected_investors)]
        
        # Comparison metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Portfolio size comparison
            portfolio_sizes = comparison_df.groupby('Investor').agg({
                'Stock': 'nunique',
                'Value_Clean': 'sum'
            })
            
            fig_comparison = px.bar(
                portfolio_sizes.reset_index(),
                x='Investor',
                y=['Stock', 'Value_Clean'],
                title='Portfolio Size Comparison',
                barmode='group',
                labels={'value': 'Count/Value', 'variable': 'Metric'}
            )
            
            fig_comparison.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)
        
        with col2:
            # Common holdings Venn diagram approximation
            st.markdown("### 🔗 Common Holdings Analysis")
            
            common_holdings = {}
            for investor in selected_investors:
                holdings = set(comparison_df[comparison_df['Investor'] == investor]['Stock'])
                common_holdings[investor] = holdings
            
            # Calculate overlaps
            if len(selected_investors) == 2:
                overlap = len(common_holdings[selected_investors[0]] & common_holdings[selected_investors[1]])
                unique_1 = len(common_holdings[selected_investors[0]] - common_holdings[selected_investors[1]])
                unique_2 = len(common_holdings[selected_investors[1]] - common_holdings[selected_investors[0]])
                
                st.metric("Common Holdings", overlap)
                st.metric(f"Unique to {selected_investors[0][:20]}", unique_1)
                st.metric(f"Unique to {selected_investors[1][:20]}", unique_2)
            elif len(selected_investors) >= 3:
                all_common = set.intersection(*common_holdings.values())
                st.metric("Holdings in All Portfolios", len(all_common))
                
                for investor in selected_investors[:3]:
                    unique = len(common_holdings[investor] - set.union(*[h for k, h in common_holdings.items() if k != investor]))
                    st.metric(f"Unique to {investor[:20]}", unique)

# Footer with attribution
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-top: 3rem;'>
        <h3 style='color: white; margin-bottom: 1rem;'>📊 Superinvestor Analytics Dashboard</h3>
        <p style='color: white; font-size: 1.2rem; font-weight: bold;'>
            Made with ❤️ by @Gsnchez - BQuantFinance.com
        </p>
        <p style='color: rgba(255,255,255,0.8); margin-top: 1rem;'>
            Data from Dataroma.com | Updated: August 2025 | Tracking 81 Legendary Investors
        </p>
        <p style='color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 1rem;'>
            Advanced 3D visualizations, AI-powered insights, and real-time portfolio analytics
        </p>
    </div>
""", unsafe_allow_html=True)
