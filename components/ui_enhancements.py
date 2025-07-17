import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

class UIEnhancements:
    """Enhanced UI Components with Poppins Font and Replit Branding"""
    
    @staticmethod
    def add_replit_branding():
        """Add Replit branding to the application"""
        st.markdown("""
        <div class="replit-badge">
            🔗 Built on Replit
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_enhanced_metric_card(title, value, icon, color="#00ff88", subtitle=None):
        """Create enhanced metric card with animations"""
        subtitle_html = f"<p style='color: #888; font-size: 0.9rem; margin: 5px 0 0 0;'>{subtitle}</p>" if subtitle else ""
        
        return f"""
        <div class="metric-card enhanced-card" style="font-family: 'Poppins', sans-serif;">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">{icon}</span>
                <h3 style="color: #00ccff; margin: 0; font-size: 1.1rem; font-weight: 500;">{title}</h3>
            </div>
            <h2 style="color: {color}; font-size: 2.5rem; font-weight: 700; margin: 0; text-shadow: 0 0 10px {color};">{value}</h2>
            {subtitle_html}
        </div>
        """
    
    @staticmethod
    def create_enhanced_pie_chart(data, title="Distribution", colors=None):
        """Create enhanced pie chart with better styling"""
        if colors is None:
            colors = {'Low': '#00ff88', 'Moderate': '#ffa500', 'High': '#ff4444'}
        
        # Filter out zero values for better visualization
        filtered_data = {k: v for k, v in data.items() if v > 0}
        
        if not filtered_data:
            # Create a placeholder chart
            fig = go.Figure(data=[go.Pie(
                labels=['No Data'],
                values=[1],
                marker=dict(colors=['#333333']),
                textinfo='label',
                textposition='inside'
            )])
        else:
            fig = px.pie(
                values=list(filtered_data.values()),
                names=list(filtered_data.keys()),
                color_discrete_map=colors,
                title=title
            )
        
        fig.update_layout(
            font=dict(family="Poppins, sans-serif", size=12),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            title_font_color='#00ff88',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            marker=dict(line=dict(color='#000000', width=2))
        )
        
        return fig
    
    @staticmethod
    def create_responsive_columns(num_columns, gap="1rem"):
        """Create responsive columns that stack on mobile"""
        return st.columns(num_columns, gap=gap)
    
    @staticmethod
    def create_info_card(title, content, icon="ℹ️", color="#00ccff"):
        """Create styled info card"""
        return f"""
        <div style="background: linear-gradient(135deg, rgba(0,204,255,0.1) 0%, rgba(0,255,136,0.1) 100%); 
                    border: 1px solid rgba(0,204,255,0.3); border-radius: 15px; padding: 20px; 
                    margin: 15px 0; backdrop-filter: blur(10px); font-family: 'Poppins', sans-serif;">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">{icon}</span>
                <h3 style="color: {color}; margin: 0; font-weight: 600;">{title}</h3>
            </div>
            <div style="color: #fff; line-height: 1.6;">{content}</div>
        </div>
        """
    
    @staticmethod
    def create_success_alert(message):
        """Create success alert"""
        return f"""
        <div style="background: linear-gradient(135deg, rgba(0,255,136,0.2) 0%, rgba(0,204,255,0.2) 100%); 
                    border: 1px solid rgba(0,255,136,0.5); border-radius: 10px; padding: 15px; 
                    margin: 10px 0; backdrop-filter: blur(10px); font-family: 'Poppins', sans-serif;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.2rem; margin-right: 10px; color: #00ff88;">✅</span>
                <p style="color: #00ff88; margin: 0; font-weight: 500;">{message}</p>
            </div>
        </div>
        """
    
    @staticmethod
    def create_error_alert(message):
        """Create error alert"""
        return f"""
        <div style="background: linear-gradient(135deg, rgba(255,68,68,0.2) 0%, rgba(255,136,136,0.2) 100%); 
                    border: 1px solid rgba(255,68,68,0.5); border-radius: 10px; padding: 15px; 
                    margin: 10px 0; backdrop-filter: blur(10px); font-family: 'Poppins', sans-serif;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.2rem; margin-right: 10px; color: #ff4444;">❌</span>
                <p style="color: #ff4444; margin: 0; font-weight: 500;">{message}</p>
            </div>
        </div>
        """
    
    @staticmethod
    def create_feature_card(title, description, icon, features):
        """Create feature showcase card"""
        features_html = "".join([f"<li style='margin: 5px 0; color: #ccc;'>• {feature}</li>" for feature in features])
        
        return f"""
        <div style="background: linear-gradient(135deg, rgba(0,255,136,0.1) 0%, rgba(0,204,255,0.1) 100%); 
                    border: 1px solid rgba(0,255,136,0.3); border-radius: 15px; padding: 25px; 
                    margin: 20px 0; backdrop-filter: blur(10px); font-family: 'Poppins', sans-serif;
                    transition: all 0.3s ease;">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
                <h3 style="color: #00ff88; margin: 0; font-weight: 600;">{title}</h3>
            </div>
            <p style="color: #00ccff; text-align: center; margin-bottom: 20px; font-size: 1.1rem;">{description}</p>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {features_html}
            </ul>
        </div>
        """
    
    @staticmethod
    def add_footer():
        """Add footer with Replit branding"""
        return """
        <div style="margin-top: 50px; padding: 20px; text-align: center; 
                    border-top: 1px solid rgba(0,255,136,0.3); font-family: 'Poppins', sans-serif;">
            <p style="color: #888; margin: 10px 0;">
                <strong>PulseAI Hospital Management System</strong><br>
                Built with ❤️ on Replit | Crafted by Moeed ul Hassan @The legend
            </p>
            <div style="margin-top: 15px;">
                <span style="display: inline-block; margin: 0 10px; padding: 5px 15px; 
                           background: linear-gradient(45deg, #667881, #4a5568); color: white; 
                           border-radius: 20px; font-size: 12px;">
                    🔗 Powered by Replit
                </span>
                <span style="display: inline-block; margin: 0 10px; padding: 5px 15px; 
                           background: linear-gradient(45deg, #00ff88, #00ccff); color: black; 
                           border-radius: 20px; font-size: 12px;">
                    ⚡ PulseAI v2.0
                </span>
            </div>
        </div>
        """