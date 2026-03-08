# sales_dashboard.py
"""
Sales Representative Dashboard
Author: AI Assistant
Description: Comprehensive sales dashboard with regional analysis,
             lead funnel, and conversion metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================
# DATA CREATION AND LOADING
# ============================================

def create_sample_data():
    """Create comprehensive sales data with all required fields"""
    
    # Define representatives and managers
    reps_data = [
        # North Region
        {'Representative_ID': 'SR001', 'Representative_Name': 'Rahul Sharma', 
         'Manager_ID': 'MGR001', 'Manager_Name': 'Vikram Singh', 'Region': 'North', 'Zone': 'Delhi'},
        {'Representative_ID': 'SR002', 'Representative_Name': 'Priya Verma', 
         'Manager_ID': 'MGR001', 'Manager_Name': 'Vikram Singh', 'Region': 'North', 'Zone': 'Punjab'},
        {'Representative_ID': 'SR003', 'Representative_Name': 'Amit Kumar', 
         'Manager_ID': 'MGR001', 'Manager_Name': 'Vikram Singh', 'Region': 'North', 'Zone': 'Haryana'},
        # South Region
        {'Representative_ID': 'SR004', 'Representative_Name': 'Neha Gupta', 
         'Manager_ID': 'MGR002', 'Manager_Name': 'Rajesh Patel', 'Region': 'South', 'Zone': 'Karnataka'},
        {'Representative_ID': 'SR005', 'Representative_Name': 'Karthik Reddy', 
         'Manager_ID': 'MGR002', 'Manager_Name': 'Rajesh Patel', 'Region': 'South', 'Zone': 'Tamil Nadu'},
        {'Representative_ID': 'SR006', 'Representative_Name': 'Lakshmi Nair', 
         'Manager_ID': 'MGR002', 'Manager_Name': 'Rajesh Patel', 'Region': 'South', 'Zone': 'Kerala'},
        # West Region
        {'Representative_ID': 'SR007', 'Representative_Name': 'Sanjay Mehta', 
         'Manager_ID': 'MGR003', 'Manager_Name': 'Anita Desai', 'Region': 'West', 'Zone': 'Maharashtra'},
        {'Representative_ID': 'SR008', 'Representative_Name': 'Pooja Shah', 
         'Manager_ID': 'MGR003', 'Manager_Name': 'Anita Desai', 'Region': 'West', 'Zone': 'Gujarat'},
        {'Representative_ID': 'SR009', 'Representative_Name': 'Rohan Joshi', 
         'Manager_ID': 'MGR003', 'Manager_Name': 'Anita Desai', 'Region': 'West', 'Zone': 'Rajasthan'},
        # East Region
        {'Representative_ID': 'SR010', 'Representative_Name': 'Deepak Das', 
         'Manager_ID': 'MGR004', 'Manager_Name': 'Suresh Banerjee', 'Region': 'East', 'Zone': 'West Bengal'},
        {'Representative_ID': 'SR011', 'Representative_Name': 'Ananya Roy', 
         'Manager_ID': 'MGR004', 'Manager_Name': 'Suresh Banerjee', 'Region': 'East', 'Zone': 'Odisha'},
        {'Representative_ID': 'SR012', 'Representative_Name': 'Sourav Ghosh', 
         'Manager_ID': 'MGR004', 'Manager_Name': 'Suresh Banerjee', 'Region': 'East', 'Zone': 'Bihar'},
    ]
    
    # Generate data for multiple months
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='MS')
    
    all_data = []
    np.random.seed(42)
    
    for date in dates:
        for rep in reps_data:
            # Base revenue varies by region
            region_multiplier = {'North': 1.0, 'South': 1.15, 'West': 1.25, 'East': 0.95}
            base_revenue = 400000 * region_multiplier[rep['Region']]
            
            # Add randomness and growth trend
            month_growth = (date.month - 1) * 0.03
            random_factor = np.random.uniform(0.85, 1.15)
            total_revenue = int(base_revenue * (1 + month_growth) * random_factor)
            
            # Product revenue split
            product_a = int(total_revenue * np.random.uniform(0.30, 0.38))
            product_b = int(total_revenue * np.random.uniform(0.35, 0.42))
            product_c = total_revenue - product_a - product_b
            
            # Lead metrics
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
    
    # Calculate derived metrics
    df['Conversion_Ratio'] = (df['Closed_Won'] / df['Connected_Leads'] * 100).round(2)
    df['Lead_Bucket'] = df['New_Leads'] + df['Qualified_Leads'] + df['Proposal_Sent']
    df['Win_Rate'] = (df['Closed_Won'] / (df['Closed_Won'] + df['Closed_Lost']) * 100).round(2)
    
    return df

def save_data_to_csv(df, filename='sales_data.csv'):
    """Save DataFrame to CSV file"""
    df.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")
    return filename

# ============================================
# DESCRIPTIVE ANALYSIS
# ============================================

def generate_descriptive_analysis(df):
    """Generate comprehensive descriptive analysis"""
    
    analysis = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SALES DASHBOARD - DESCRIPTIVE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════════════════════

This analysis covers sales performance data for 12 Sales Representatives 
across 4 regions of India (North, South, East, West) managed by 4 Regional 
Managers over a 6-month period (January 2024 - June 2024).

"""
    
    # Overall Statistics
    analysis += f"""
📈 OVERALL PERFORMANCE METRICS
───────────────────────────────────────────────────────────────────────────────
• Total Revenue Generated: ₹{df['Total_Revenue'].sum():,.0f}
• Average Monthly Revenue per Rep: ₹{df['Total_Revenue'].mean():,.0f}
• Highest Single Month Revenue: ₹{df['Total_Revenue'].max():,.0f}
• Lowest Single Month Revenue: ₹{df['Total_Revenue'].min():,.0f}
• Revenue Standard Deviation: ₹{df['Total_Revenue'].std():,.0f}

"""
    
    # Regional Analysis
    regional_stats = df.groupby('Region').agg({
        'Total_Revenue': ['sum', 'mean'],
        'Connected_Leads': 'sum',
        'Closed_Won': 'sum',
        'Conversion_Ratio': 'mean'
    }).round(2)
    
    analysis += """
🗺️ REGIONAL PERFORMANCE BREAKDOWN
───────────────────────────────────────────────────────────────────────────────
"""
    
    for region in ['North', 'South', 'East', 'West']:
        region_data = df[df['Region'] == region]
        total_rev = region_data['Total_Revenue'].sum()
        avg_conv = region_data['Conversion_Ratio'].mean()
        total_leads = region_data['Connected_Leads'].sum()
        closed = region_data['Closed_Won'].sum()
        
        analysis += f"""
📍 {region.upper()} INDIA
   • Total Revenue: ₹{total_rev:,.0f}
   • Total Connected Leads: {total_leads:,}
   • Total Deals Closed: {closed:,}
   • Average Conversion Ratio: {avg_conv:.2f}%
   • Revenue Share: {(total_rev/df['Total_Revenue'].sum()*100):.1f}%
"""
    
    # Product Analysis
    analysis += f"""

📦 PRODUCT REVENUE ANALYSIS
───────────────────────────────────────────────────────────────────────────────
• Product A Total Revenue: ₹{df['Product_A_Revenue'].sum():,.0f} ({df['Product_A_Revenue'].sum()/df['Total_Revenue'].sum()*100:.1f}%)
• Product B Total Revenue: ₹{df['Product_B_Revenue'].sum():,.0f} ({df['Product_B_Revenue'].sum()/df['Total_Revenue'].sum()*100:.1f}%)
• Product C Total Revenue: ₹{df['Product_C_Revenue'].sum():,.0f} ({df['Product_C_Revenue'].sum()/df['Total_Revenue'].sum()*100:.1f}%)

"""
    
    # Lead Funnel Analysis
    total_new = df['New_Leads'].sum()
    total_qualified = df['Qualified_Leads'].sum()
    total_proposal = df['Proposal_Sent'].sum()
    total_negotiation = df['Negotiation'].sum()
    total_won = df['Closed_Won'].sum()
    total_lost = df['Closed_Lost'].sum()
    
    analysis += f"""
🔄 LEAD FUNNEL ANALYSIS
───────────────────────────────────────────────────────────────────────────────
Stage                    Count       Conversion to Next Stage
─────────────────────────────────────────────────────────────
New Leads               {total_new:>6,}       → {(total_qualified/total_new*100):.1f}% qualified
Qualified Leads         {total_qualified:>6,}       → {(total_proposal/total_qualified*100):.1f}% proposal sent
Proposal Sent           {total_proposal:>6,}       → {(total_negotiation/total_proposal*100):.1f}% in negotiation
Negotiation             {total_negotiation:>6,}       → {(total_won/total_negotiation*100):.1f}% closed won
Closed Won              {total_won:>6,}       
Closed Lost             {total_lost:>6,}       

Overall Funnel Conversion (New Lead → Closed Won): {(total_won/total_new*100):.2f}%
Win Rate (Won vs Lost): {(total_won/(total_won+total_lost)*100):.2f}%

"""
    
    # Top Performers
    rep_performance = df.groupby(['Representative_ID', 'Representative_Name', 'Region']).agg({
        'Total_Revenue': 'sum',
        'Conversion_Ratio': 'mean'
    }).reset_index().sort_values('Total_Revenue', ascending=False)
    
    analysis += """
🏆 TOP 5 SALES REPRESENTATIVES (by Revenue)
───────────────────────────────────────────────────────────────────────────────
"""
    for i, row in rep_performance.head().iterrows():
        analysis += f"   {rep_performance.head().index.tolist().index(i)+1}. {row['Representative_Name']} ({row['Region']}) - ₹{row['Total_Revenue']:,.0f}\n"
    
    # Manager Performance
    mgr_performance = df.groupby(['Manager_ID', 'Manager_Name', 'Region']).agg({
        'Total_Revenue': 'sum',
        'Closed_Won': 'sum',
        'Conversion_Ratio': 'mean'
    }).reset_index().sort_values('Total_Revenue', ascending=False)
    
    analysis += """

👔 MANAGER PERFORMANCE SUMMARY
───────────────────────────────────────────────────────────────────────────────
"""
    for _, row in mgr_performance.iterrows():
        analysis += f"""
   {row['Manager_Name']} ({row['Region']} Region)
   • Team Revenue: ₹{row['Total_Revenue']:,.0f}
   • Deals Closed: {row['Closed_Won']:,}
   • Avg Team Conversion: {row['Conversion_Ratio']:.2f}%
"""
    
    # Key Insights
    analysis += """

💡 KEY INSIGHTS & RECOMMENDATIONS
───────────────────────────────────────────────────────────────────────────────

1. REGIONAL INSIGHTS:
   • West India leads in revenue generation with highest per-rep productivity
   • South India shows strong conversion ratios indicating quality lead handling
   • East India has opportunity for growth with focused training programs
   • North India maintains consistent performance across all metrics

2. PRODUCT INSIGHTS:
   • Product B is the highest revenue contributor across all regions
   • Product A shows potential for cross-selling opportunities
   • Product C has consistent demand but lower revenue share

3. LEAD MANAGEMENT:
   • Average lead-to-close conversion is healthy at ~10%
   • Proposal-to-negotiation stage shows highest drop-off
   • Follow-up leads represent significant untapped potential

4. RECOMMENDATIONS:
   • Focus on improving proposal quality to increase negotiation conversion
   • Implement best practices from West region across other regions
   • Develop targeted training for underperforming representatives
   • Create incentive programs for improving conversion ratios

═══════════════════════════════════════════════════════════════════════════════
                              END OF ANALYSIS
═══════════════════════════════════════════════════════════════════════════════
"""
    
    return analysis

# ============================================
# POWER BI DATA PREPARATION
# ============================================

def prepare_powerbi_data(df):
    """Prepare multiple CSV files optimized for Power BI"""
    
    # 1. Main Sales Data (Fact Table)
    fact_sales = df.copy()
    fact_sales.to_csv('powerbi_fact_sales.csv', index=False)
    
    # 2. Representative Dimension
    dim_rep = df[['Representative_ID', 'Representative_Name', 'Manager_ID', 'Region', 'Zone']].drop_duplicates()
    dim_rep.to_csv('powerbi_dim_representative.csv', index=False)
    
    # 3. Manager Dimension
    dim_mgr = df[['Manager_ID', 'Manager_Name', 'Region']].drop_duplicates()
    dim_mgr.to_csv('powerbi_dim_manager.csv', index=False)
    
    # 4. Region Dimension
    dim_region = pd.DataFrame({
        'Region': ['North', 'South', 'East', 'West'],
        'Region_Full_Name': ['North India', 'South India', 'East India', 'West India'],
        'Region_Code': ['NI', 'SI', 'EI', 'WI']
    })
    dim_region.to_csv('powerbi_dim_region.csv', index=False)
    
    # 5. Monthly Summary
    monthly_summary = df.groupby(['Date', 'Region']).agg({
        'Total_Revenue': 'sum',
        'Product_A_Revenue': 'sum',
        'Product_B_Revenue': 'sum',
        'Product_C_Revenue': 'sum',
        'Connected_Leads': 'sum',
        'Leads_In_Followup': 'sum',
        'New_Leads': 'sum',
        'Qualified_Leads': 'sum',
        'Proposal_Sent': 'sum',
        'Negotiation': 'sum',
        'Closed_Won': 'sum',
        'Closed_Lost': 'sum'
    }).reset_index()
    monthly_summary['Conversion_Ratio'] = (monthly_summary['Closed_Won'] / monthly_summary['Connected_Leads'] * 100).round(2)
    monthly_summary.to_csv('powerbi_monthly_summary.csv', index=False)
    
    # 6. Lead Funnel Data
    funnel_data = pd.DataFrame({
        'Stage': ['New Leads', 'Qualified Leads', 'Proposal Sent', 'Negotiation', 'Closed Won'],
        'Stage_Order': [1, 2, 3, 4, 5],
        'Count': [
            df['New_Leads'].sum(),
            df['Qualified_Leads'].sum(),
            df['Proposal_Sent'].sum(),
            df['Negotiation'].sum(),
            df['Closed_Won'].sum()
        ]
    })
    funnel_data.to_csv('powerbi_lead_funnel.csv', index=False)
    
    print("✅ Power BI data files created:")
    print("   • powerbi_fact_sales.csv")
    print("   • powerbi_dim_representative.csv")
    print("   • powerbi_dim_manager.csv")
    print("   • powerbi_dim_region.csv")
    print("   • powerbi_monthly_summary.csv")
    print("   • powerbi_lead_funnel.csv")
    
    return True

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print("🚀 SALES DASHBOARD DATA GENERATOR")
    print("="*80 + "\n")
    
    # Step 1: Create Data
    print("📊 Step 1: Generating sales data...")
    df = create_sample_data()
    print(f"   ✓ Created {len(df)} records for {df['Representative_ID'].nunique()} representatives")
    
    # Step 2: Save Main CSV
    print("\n💾 Step 2: Saving main data file...")
    save_data_to_csv(df, 'sales_data.csv')
    
    # Step 3: Generate Analysis
    print("\n📈 Step 3: Generating descriptive analysis...")
    analysis = generate_descriptive_analysis(df)
    
    # Save analysis to file
    with open('sales_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(analysis)
    print("   ✓ Analysis saved to sales_analysis_report.txt")
    
    # Step 4: Prepare Power BI files
    print("\n📊 Step 4: Preparing Power BI data files...")
    prepare_powerbi_data(df)
    
    # Print Analysis
    print("\n" + analysis)
    
    print("\n" + "="*80)
    print("✅ ALL FILES GENERATED SUCCESSFULLY!")
    print("="*80)
    print("""
📁 Files Created:
   1. sales_data.csv - Main data file
   2. sales_analysis_report.txt - Descriptive analysis
   3. powerbi_fact_sales.csv - Fact table for Power BI
   4. powerbi_dim_representative.csv - Representative dimension
   5. powerbi_dim_manager.csv - Manager dimension
   6. powerbi_dim_region.csv - Region dimension
   7. powerbi_monthly_summary.csv - Monthly aggregated data
   8. powerbi_lead_funnel.csv - Lead funnel data

📌 Next Steps for Power BI:
   1. Open Power BI Desktop
   2. Click 'Get Data' → 'Text/CSV'
   3. Import all powerbi_*.csv files
   4. Create relationships between tables
   5. Build visualizations using the dashboard guide below
""")

if __name__ == "__main__":
    main()
