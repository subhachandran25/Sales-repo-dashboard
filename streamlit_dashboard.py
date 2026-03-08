# streamlit_dashboard.py
"""
Sales Representative Dashboard - Streamlit Application
Light-themed interactive dashboard with comprehensive analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS FOR LIGHT THEME
# ============================================

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    /* Cards */
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    }
    
    .metric-card-blue {
        border-left-color: #2196F3;
    }
    
    .metric-card-orange {
        border-left-color: #FF9800;
    }
    
    .metric-card-purple {
        border-left-color: #9C27B0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #333333;
    }
    
    /* Metric styling */
    .big-metric {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333333;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666666;
        text-transform: uppercase;
    }
    
    /* Table styling */
    .dataframe {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING
# ============================================

@st.cache_data
def load_data():
    """Load or create sample data"""
    try:
        df = pd.read_csv('sales_data.csv')
    except FileNotFoundError:
        # Create sample data if file doesn't exist
        df = create_sample_data()
    
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%B %Y')
    df['Month_Num'] = df['Date'].dt.to_period('M')
    
    return df

def create_sample_data():
    """Create sample data if CSV not found"""
    reps_data = [
        {'Representative_ID': 'SR001', 'Representative_Name': 'Rahul Sharma', 
         'Manager_ID': 'MGR001', 'Manager_Name': 'Vikram Singh', 'Region': 'North', 'Zone': 'Delhi'},
        {'Representative_ID': 'SR002', 'Representative_Name': 'Priya Verma', 
         'Manager_ID': 'MGR001', 'Manager_Name': 'Vikram Singh', 'Region': 'North', 'Zone': 'Punjab'},
        {'Representative_ID': 'SR003', 'Representative_Name': 'Amit Kumar', 
         'Manager_ID': 'MGR001', 'Manager_Name': 'Vikram Singh', 'Region': 'North', 'Zone': 'Haryana'},
        {'Representative_ID': 'SR004', 'Representative_Name': 'Neha Gupta', 
         'Manager_ID': 'MGR002', 'Manager_Name': 'Rajesh Patel', 'Region': 'South', 'Zone': 'Karnataka'},
        {'Representative_ID': 'SR005', 'Representative_Name': 'Karthik Reddy', 
         'Manager_ID': 'MGR002', 'Manager_Name': 'Rajesh Patel', 'Region': 'South', 'Zone': 'Tamil Nadu'},
        {'Representative_ID': 'SR006', 'Representative_Name': 'Lakshmi Nair', 
         'Manager_ID': 'MGR002', 'Manager_Name': 'Rajesh Patel', 'Region': 'South', 'Zone': 'Kerala'},
        {'Representative_ID': 'SR007', 'Representative_Name': 'Sanjay Mehta', 
         'Manager_ID': 'MGR003', 'Manager_Name': 'Anita Desai', 'Region': 'West', 'Zone': 'Maharashtra'},
        {'Representative_ID': 'SR008', 'Representative_Name': 'Pooja Shah', 
         'Manager_ID': 'MGR003', 'Manager_Name': 'Anita Desai', 'Region': 'West', 'Zone': 'Gujarat'},
        {'Representative_ID': 'SR009', 'Representative_Name': 'Rohan Joshi', 
         'Manager_ID': 'MGR003', 'Manager_Name': 'Anita Desai', 'Region': 'West', 'Zone': 'Rajasthan'},
        {'Representative_ID': 'SR010', 'Representative_Name': 'Deepak Das', 
         'Manager_ID': 'MGR004', 'Manager_Name': 'Suresh Banerjee', 'Region': 'East', 'Zone': 'West Bengal'},
        {'Representative_ID': 'SR011', 'Representative_Name': 'Ananya Roy', 
         'Manager_ID': 'MGR004', 'Manager_Name': 'Suresh Banerjee', 'Region': 'East', 'Zone': 'Odisha'},
        {'Representative_ID': 'SR012', 'Representative_Name': 'Sourav Ghosh', 
         'Manager_ID': 'MGR004', 'Manager_Name': 'Suresh Banerjee', 'Region': 'East', 'Zone': 'Bihar'},
    ]
    
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='MS')
    all_data = []
    np.random.seed(42)
    
    for date in dates:
        for rep in reps_data:
            region_multiplier = {'North': 1.0, 'South': 1.15, 'West': 1.25, 'East': 0.95}
            base_revenue = 400000 * region_multiplier[rep['Region']]
            month_growth = (date.month - 1) * 0.03
            random_factor = np.random.uniform(0.85, 1.15)
            total_revenue = int(base_revenue * (1 + month_growth) * random_factor)
            
            product_a = int(total_revenue * np.random.uniform(0.30, 0.38))
            product_b = int(total_revenue * np.random.uniform(0.35, 0.42))
            product_c = total_revenue - product_a - product_b
            
            connected_leads = int(80 * region_multiplier[rep['Region']] * random_factor)
            new_leads = int(connected_leads * np.random.uniform(0.50, 0.65))
            qualified_leads = int(new_leads * np.random.uniform(0.55, 0.70))
            proposal_sent = int(qualified_leads * np.random.uniform(0.60, 0.75))
            negotiation = int(proposal_sent * np.random.uniform(0.55, 0.70))
            closed_won = int(negotiation * np.random.uniform(0.55, 0.75))
            closed_lost = int(negotiation * np.random.uniform(0.20, 0.35))
            leads_in_followup = int(connected_leads * np.random.uniform(0.35, 0.45))
            
            row = {
                **rep,
                'Total_Revenue': total_revenue,
                'Product_A_Revenue': product_a,
                'Product_B_Revenue': product_b,
                'Product_C_Revenue': product_c,
                'Connected_Leads': connected_leads,
                'Leads_In_Followup': leads_in_followup,
                'New_Leads': new_leads,
                'Qualified_Leads': qualified_leads,
                'Proposal_Sent': proposal_sent,
                'Negotiation': negotiation,
                'Closed_Won': closed_won,
                'Closed_Lost': closed_lost,
                'Date': date.strftime('%Y-%m-%d')
            }
            all_data.append(row)
    
    df = pd.DataFrame(all_data)
    df['Conversion_Ratio'] = (df['Closed_Won'] / df['Connected_Leads'] * 100).round(2)
    df['Lead_Bucket'] = df['New_Leads'] + df['Qualified_Leads'] + df['Proposal_Sent']
    df['Win_Rate'] = (df['Closed_Won'] / (df['Closed_Won'] + df['Closed_Lost']) * 100).round(2)
    
    return df

# ============================================
# CHART CONFIGURATIONS
# ============================================

# Light theme color palette
COLORS = {
    'primary': '#4CAF50',
    'secondary': '#2196F3',
    'accent': '#FF9800',
    'purple': '#9C27B0',
    'regions': {
        'North': '#5C6BC0',
        'South': '#26A69A',
        'East': '#FFA726',
        'West': '#EF5350'
    },
    'products': ['#81C784', '#64B5F6', '#FFB74D'],
    'funnel': ['#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5']
}

CHART_LAYOUT = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#333333', 'family': 'Arial'},
    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40}
}

# ============================================
# SIDEBAR
# ============================================

def render_sidebar(df):
    """Render sidebar with filters"""
    
    st.sidebar.image("https://via.placeholder.com/150x50?text=Sales+Dashboard", width=150)
    st.sidebar.title("🎛️ Filters")
    
    # User Role Selection
    user_role = st.sidebar.radio(
        "Select View",
        ["Manager View", "Sales Rep View"],
        help="Choose dashboard perspective"
    )
    
    st.sidebar.markdown("---")
    
    # Region Filter
    regions = ['All'] + list(df['Region'].unique())
    selected_region = st.sidebar.selectbox("🗺️ Region", regions)
    
    # Date Range
    st.sidebar.markdown("### 📅 Date Range")
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_range = st.sidebar.date_input(
        "Select Period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Manager/Rep specific filters
    if user_role == "Manager View":
        managers = ['All'] + list(df['Manager_Name'].unique())
        selected_manager = st.sidebar.selectbox("👔 Manager", managers)
        selected_rep = 'All'
    else:
        selected_manager = 'All'
        reps = ['All'] + list(df['Representative_Name'].unique())
        selected_rep = st.sidebar.selectbox("👤 Sales Representative", reps)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    return {
        'user_role': user_role,
        'region': selected_region,
        'date_range': date_range,
        'manager': selected_manager,
        'rep': selected_rep
    }

def filter_data(df, filters):
    """Apply filters to dataframe"""
    filtered_df = df.copy()
    
    # Region filter
    if filters['region'] != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == filters['region']]
    
    # Date filter
    if len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['Date'] >= pd.to_datetime(start_date)) & 
            (filtered_df['Date'] <= pd.to_datetime(end_date))
        ]
    
    # Manager filter
    if filters['manager'] != 'All':
        filtered_df = filtered_df[filtered_df['Manager_Name'] == filters['manager']]
    
    # Rep filter
    if filters['rep'] != 'All':
        filtered_df = filtered_df[filtered_df['Representative_Name'] == filters['rep']]
    
    return filtered_df

# ============================================
# KPI CARDS
# ============================================

def render_kpi_cards(df):
    """Render KPI metric cards"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Total_Revenue'].sum()
        st.metric(
            label="💰 Total Revenue",
            value=f"₹{total_revenue/10000000:.2f} Cr",
            delta=f"+{np.random.uniform(5, 15):.1f}%"
        )
    
    with col2:
        total_leads = df['Connected_Leads'].sum()
        st.metric(
            label="📞 Connected Leads",
            value=f"{total_leads:,}",
            delta=f"+{np.random.uniform(3, 10):.1f}%"
        )
    
    with col3:
        avg_conversion = df['Conversion_Ratio'].mean()
        st.metric(
            label="📈 Avg Conversion Rate",
            value=f"{avg_conversion:.2f}%",
            delta=f"+{np.random.uniform(0.5, 2):.1f}%"
        )
    
    with col4:
        total_closed = df['Closed_Won'].sum()
        st.metric(
            label="✅ Deals Closed",
            value=f"{total_closed:,}",
            delta=f"+{np.random.uniform(5, 12):.1f}%"
        )

# ============================================
# CHARTS
# ============================================

def create_revenue_trend_chart(df):
    """Create revenue trend line chart"""
    monthly_revenue = df.groupby(['Month', 'Region'])['Total_Revenue'].sum().reset_index()
    
    fig = px.line(
        monthly_revenue,
        x='Month',
        y='Total_Revenue',
        color='Region',
        color_discrete_map=COLORS['regions'],
        markers=True,
        title='📈 Revenue Trend by Region'
    )
    
    fig.update_layout(**CHART_LAYOUT)
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_yaxes(title='Revenue (₹)', gridcolor='#E0E0E0')
    fig.update_xaxes(title='Month', gridcolor='#E0E0E0')
    
    return fig

def create_regional_revenue_chart(df):
    """Create regional revenue bar chart"""
    regional_revenue = df.groupby('Region')['Total_Revenue'].sum().reset_index()
    
    fig = px.bar(
        regional_revenue,
        x='Region',
        y='Total_Revenue',
        color='Region',
        color_discrete_map=COLORS['regions'],
        title='🗺️ Revenue by Region'
    )
    
    fig.update_layout(**CHART_LAYOUT)
    fig.update_traces(texttemplate='₹%{y:,.0f}', textposition='outside')
    fig.update_yaxes(title='Revenue (₹)', gridcolor='#E0E0E0')
    
    return fig

def create_product_revenue_chart(df):
    """Create product revenue pie chart"""
    product_revenue = pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C'],
        'Revenue': [
            df['Product_A_Revenue'].sum(),
            df['Product_B_Revenue'].sum(),
            df['Product_C_Revenue'].sum()
        ]
    })
    
    fig = px.pie(
        product_revenue,
        values='Revenue',
        names='Product',
        color_discrete_sequence=COLORS['products'],
        title='📦 Product Revenue Distribution',
        hole=0.4
    )
    
    fig.update_layout(**CHART_LAYOUT)
    fig.update_traces(textinfo='percent+label')
    
    return fig

def create_lead_funnel_chart(df):
    """Create lead funnel chart"""
    funnel_data = pd.DataFrame({
        'Stage': ['New Leads', 'Qualified', 'Proposal Sent', 'Negotiation', 'Closed Won'],
        'Count': [
            df['New_Leads'].sum(),
            df['Qualified_Leads'].sum(),
            df['Proposal_Sent'].sum(),
            df['Negotiation'].sum(),
            df['Closed_Won'].sum()
        ]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial",
        marker=dict(color=COLORS['funnel']),
        connector=dict(line=dict(color="#E0E0E0", width=2))
    ))
    
    fig.update_layout(
        title='🔄 Lead Funnel',
        **CHART_LAYOUT
    )
    
    return fig

def create_conversion_chart(df):
    """Create conversion ratio by rep chart"""
    rep_conversion = df.groupby('Representative_Name').agg({
        'Conversion_Ratio': 'mean',
        'Region': 'first'
    }).reset_index().sort_values('Conversion_Ratio', ascending=True)
    
    fig = px.bar(
        rep_conversion,
        x='Conversion_Ratio',
        y='Representative_Name',
        color='Region',
        color_discrete_map=COLORS['regions'],
        orientation='h',
        title='📊 Conversion Ratio by Representative'
    )
    
    fig.update_layout(**CHART_LAYOUT)
    fig.update_xaxes(title='Conversion Ratio (%)', gridcolor='#E0E0E0')
    
    return fig

def create_lead_bucket_chart(df):
    """Create lead bucket analysis chart"""
    lead_bucket = df.groupby('Region').agg({
        'New_Leads': 'sum',
        'Qualified_Leads': 'sum',
        'Leads_In_Followup': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='New Leads',
        x=lead_bucket['Region'],
        y=lead_bucket['New_Leads'],
        marker_color='#81C784'
    ))
    
    fig.add_trace(go.Bar(
        name='Qualified Leads',
        x=lead_bucket['Region'],
        y=lead_bucket['Qualified_Leads'],
        marker_color='#64B5F6'
    ))
    
    fig.add_trace(go.Bar(
        name='In Follow-up',
        x=lead_bucket['Region'],
        y=lead_bucket['Leads_In_Followup'],
        marker_color='#FFB74D'
    ))
    
    fig.update_layout(
        title='📋 Lead Bucket by Region',
        barmode='group',
        **CHART_LAYOUT
    )
    fig.update_yaxes(gridcolor='#E0E0E0')
    
    return fig

def create_manager_performance_chart(df):
    """Create manager performance comparison"""
    manager_perf = df.groupby('Manager_Name').agg({
        'Total_Revenue': 'sum',
        'Closed_Won': 'sum',
        'Conversion_Ratio': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Revenue by Manager', 'Deals Closed by Manager'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(
            x=manager_perf['Manager_Name'],
            y=manager_perf['Total_Revenue'],
            marker_color='#4CAF50',
            name='Revenue'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=manager_perf['Manager_Name'],
            y=manager_perf['Closed_Won'],
            marker_color='#2196F3',
            name='Deals Closed'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title='👔 Manager Performance Comparison',
        showlegend=False,
        **CHART_LAYOUT
    )
    
    return fig

# ============================================
# DATA TABLES
# ============================================

def render_data_tables(df, user_role):
    """Render data tables based on user role"""
    
    st.markdown("### 📋 Detailed Data View")
    
    if user_role == "Manager View":
        # Team summary table
        team_summary = df.groupby(['Manager_Name', 'Representative_Name', 'Region']).agg({
            'Total_Revenue': 'sum',
            'Connected_Leads': 'sum',
            'Closed_Won': 'sum',
            'Conversion_Ratio': 'mean'
        }).reset_index()
        
        team_summary.columns = ['Manager', 'Representative', 'Region', 'Revenue', 'Leads', 'Deals', 'Conv. Rate']
        team_summary['Revenue'] = team_summary['Revenue'].apply(lambda x: f"₹{x:,.0f}")
        team_summary['Conv. Rate'] = team_summary['Conv. Rate'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(
            team_summary,
            use_container_width=True,
            hide_index=True
        )
    else:
        # Individual rep detailed view
        rep_detail = df.groupby(['Representative_Name', 'Month']).agg({
            'Total_Revenue': 'sum',
            'Product_A_Revenue': 'sum',
            'Product_B_Revenue': 'sum',
            'Product_C_Revenue': 'sum',
            'Connected_Leads': 'sum',
            'Closed_Won': 'sum'
        }).reset_index()
        
        st.dataframe(
            rep_detail,
            use_container_width=True,
            hide_index=True
        )

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Main application function"""
    
    # Load data
    df = load_data()
    
    # Render sidebar and get filters
    filters = render_sidebar(df)
    
    # Filter data
    filtered_df = filter_data(df, filters)
    
    # Sidebar quick stats
    st.sidebar.metric("Total Records", len(filtered_df))
    st.sidebar.metric("Unique Reps", filtered_df['Representative_ID'].nunique())
    
    # Main content
    st.title("📊 Sales Representative Dashboard")
    st.markdown(f"**View:** {filters['user_role']} | **Region:** {filters['region']}")
    st.markdown("---")
    
    # KPI Cards
    render_kpi_cards(filtered_df)
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_revenue_trend_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_regional_revenue_chart(filtered_df), use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_product_revenue_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_lead_funnel_chart(filtered_df), use_container_width=True)
    
    # Charts Row 3
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_lead_bucket_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_conversion_chart(filtered_df), use_container_width=True)
    
    # Manager Performance (only in Manager View)
    if filters['user_role'] == "Manager View":
        st.plotly_chart(create_manager_performance_chart(filtered_df), use_container_width=True)
    
    # Data Tables
    st.markdown("---")
    render_data_tables(filtered_df, filters['user_role'])
    
    # Download Section
    st.markdown("---")
    st.markdown("### 📥 Download Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name="sales_data_export.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="📊 Download for Power BI",
            data=csv,
            file_name="powerbi_data.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666666; padding: 20px;'>
            <p>Sales Dashboard v1.0 | Built with Streamlit</p>
            <p>© 2024 Your Company Name</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
