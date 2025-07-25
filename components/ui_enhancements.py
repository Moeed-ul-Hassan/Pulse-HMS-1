import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

class UIEnhancements:
    """Enhanced UI Components with Poppins Font"""
    
    @staticmethod
    def add_platform_branding():
        """Platform branding removed per user request"""
        pass
    
    @staticmethod
    def create_enhanced_metric_card(title, value, icon, color="#2563eb", subtitle=None):
        """Create minimalist metric card"""
        subtitle_html = f"<p style='color: #64748b; font-size: 0.8rem; margin: 8px 0 0 0; font-weight: 300;'>{subtitle}</p>" if subtitle else ""
        return f"""
        <div style="background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.03); font-family: 'Poppins', sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px;">
                <div>
                    <h3 style="color: #64748b; margin: 0; font-size: 0.95rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">{title}</h3>
                    {subtitle_html}
                </div>
                <div style="font-size: 1.7rem; opacity: 0.7;">{icon}</div>
            </div>
            <h2 style="font-size: 2.3rem; font-weight: 400; margin: 0; color: {color};">{value}</h2>
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
        """Create minimalist info card"""
        return f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0,204,255,0.2); 
                    border-radius: 20px; padding: 2rem; margin: 1.5rem 0; backdrop-filter: blur(20px); 
                    font-family: 'Poppins', sans-serif; position: relative; overflow: hidden;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 1.5rem; margin-right: 1rem; opacity: 0.8;">{icon}</div>
                <h3 style="color: {color}; margin: 0; font-weight: 400; font-size: 1.1rem;">{title}</h3>
            </div>
            <div style="color: #e2e8f0; line-height: 1.6; font-weight: 300;">{content}</div>
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
        """Create minimalist feature showcase card"""
        features_html = "".join([f"<li style='margin: 8px 0; color: #94a3b8; font-weight: 300;'>• {feature}</li>" for feature in features])
        
        return f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0,255,136,0.2); 
                    border-radius: 20px; padding: 2.5rem; margin: 2rem 0; backdrop-filter: blur(20px); 
                    font-family: 'Poppins', sans-serif; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    position: relative; overflow: hidden;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.9;">{icon}</div>
                <h3 style="color: #00ff88; margin: 0; font-weight: 400; font-size: 1.3rem;">{title}</h3>
            </div>
            <p style="color: #00ccff; text-align: center; margin-bottom: 1.5rem; font-size: 1rem; font-weight: 300; line-height: 1.6;">{description}</p>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {features_html}
            </ul>
        </div>
        """
    
    @staticmethod
    def add_footer():
        """Add minimalist footer"""
        return """
        <div style="margin-top: 4rem; padding: 2rem; text-align: center; 
                    border-top: 1px solid rgba(0,255,136,0.1); font-family: 'Poppins', sans-serif;">
            <div style="margin-bottom: 1.5rem;">
                <h3 style="color: #00ff88; margin: 0; font-weight: 300; font-size: 1.2rem;">PulseAI Hospital Management System</h3>
                <p style="color: #64748b; margin: 0.5rem 0; font-weight: 300; font-size: 0.9rem;">
                    Crafted with precision | Developed by Moeed ul Hassan @The legend
                </p>
            </div>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <div style="padding: 0.5rem 1rem; background: rgba(15, 23, 42, 0.8); 
                           border: 1px solid rgba(0,255,136,0.2); border-radius: 12px; 
                           font-size: 0.8rem; color: #00ff88; backdrop-filter: blur(10px);">
                    ⚡ PulseAI v2.0
                </div>
                <div style="padding: 0.5rem 1rem; background: rgba(15, 23, 42, 0.8); 
                           border: 1px solid rgba(0,204,255,0.2); border-radius: 12px; 
                           font-size: 0.8rem; color: #00ccff; backdrop-filter: blur(10px);">
                    🏥 Healthcare Tech
                </div>
                <div style="padding: 0.5rem 1rem; background: rgba(15, 23, 42, 0.8); 
                           border: 1px solid rgba(255,164,0,0.2); border-radius: 12px; 
                           font-size: 0.8rem; color: #ffa500; backdrop-filter: blur(10px);">
                    🔬 Advanced Analytics
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def create_minimalist_header(title, subtitle=None, icon=None):
        """Create minimalist section header"""
        subtitle_html = f"<p style='color: #64748b; margin: 0.5rem 0; font-weight: 300; font-size: 0.9rem;'>{subtitle}</p>" if subtitle else ""
        icon_html = f"<div style='font-size: 1.5rem; margin-right: 1rem; opacity: 0.8;'>{icon}</div>" if icon else ""
        return f"""
        <div style="margin: 2rem 0 1.5rem 0; padding: 1.2rem; background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; font-family: 'Poppins', sans-serif;">
            <div style="display: flex; align-items: center;">
                {icon_html}
                <div>
                    <h2 style="color: #2563eb; margin: 0; font-weight: 400; font-size: 1.4rem;">{title}</h2>
                    {subtitle_html}
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def create_glass_card(content, padding="2rem"):
        """Create glass morphism card"""
        return f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0,255,136,0.2); 
                    border-radius: 20px; padding: {padding}; margin: 1rem 0; 
                    backdrop-filter: blur(20px); font-family: 'Poppins', sans-serif;
                    position: relative; overflow: hidden;">
            <div style="position: relative; z-index: 1;">
                {content}
            </div>
        </div>
        """