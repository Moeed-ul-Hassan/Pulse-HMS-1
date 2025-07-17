import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict
import json
import os

class NotificationManager:
    """Real-time notification and alert system"""
    
    def __init__(self, notifications_file: str = "data/notifications.json"):
        self.notifications_file = notifications_file
        self.notifications = self._load_notifications()
    
    def _load_notifications(self) -> List[Dict]:
        """Load notifications from file"""
        if os.path.exists(self.notifications_file):
            try:
                with open(self.notifications_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_notifications(self):
        """Save notifications to file"""
        os.makedirs(os.path.dirname(self.notifications_file), exist_ok=True)
        with open(self.notifications_file, 'w') as f:
            json.dump(self.notifications, f, indent=2, default=str)
    
    def add_notification(self, title: str, message: str, type: str = "info", 
                        patient_id: str = None, priority: str = "normal"):
        """Add a new notification"""
        notification = {
            "id": len(self.notifications) + 1,
            "title": title,
            "message": message,
            "type": type,  # info, warning, error, success
            "priority": priority,  # low, normal, high, critical
            "patient_id": patient_id,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        self.notifications.insert(0, notification)
        self._save_notifications()
    
    def mark_as_read(self, notification_id: int):
        """Mark notification as read"""
        for notif in self.notifications:
            if notif["id"] == notification_id:
                notif["read"] = True
                break
        self._save_notifications()
    
    def get_unread_count(self) -> int:
        """Get count of unread notifications"""
        return sum(1 for n in self.notifications if not n["read"])
    
    def get_recent_notifications(self, limit: int = 10) -> List[Dict]:
        """Get recent notifications"""
        return self.notifications[:limit]
    
    def display_notifications_sidebar(self):
        """Display notifications in sidebar"""
        unread_count = self.get_unread_count()
        
        if unread_count > 0:
            st.sidebar.markdown(f"""
            <div style="background: linear-gradient(45deg, #ff4444, #ff0088); 
                        padding: 10px; border-radius: 10px; margin: 10px 0;">
                <h4 style="color: white; margin: 0;">🔔 Notifications ({unread_count})</h4>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
            <div style="background: linear-gradient(45deg, #00ff88, #00ccff); 
                        padding: 10px; border-radius: 10px; margin: 10px 0;">
                <h4 style="color: white; margin: 0;">✅ All Caught Up!</h4>
            </div>
            """, unsafe_allow_html=True)
        
        recent = self.get_recent_notifications(5)
        for notif in recent:
            icon = self._get_notification_icon(notif["type"])
            bg_color = self._get_notification_color(notif["type"])
            
            if not notif["read"]:
                st.sidebar.markdown(f"""
                <div style="background: {bg_color}; border-left: 4px solid #ff4444; 
                            padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>{icon} {notif['title']}</strong><br>
                    <small>{notif['message'][:50]}...</small><br>
                    <small style="opacity: 0.7;">{self._format_time(notif['timestamp'])}</small>
                </div>
                """, unsafe_allow_html=True)
    
    def _get_notification_icon(self, type: str) -> str:
        """Get icon for notification type"""
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅",
            "critical": "🚨"
        }
        return icons.get(type, "📢")
    
    def _get_notification_color(self, type: str) -> str:
        """Get background color for notification type"""
        colors = {
            "info": "rgba(0, 204, 255, 0.1)",
            "warning": "rgba(255, 165, 0, 0.1)",
            "error": "rgba(255, 68, 68, 0.1)",
            "success": "rgba(0, 255, 136, 0.1)",
            "critical": "rgba(255, 0, 136, 0.1)"
        }
        return colors.get(type, "rgba(255, 255, 255, 0.1)")
    
    def _format_time(self, timestamp: str) -> str:
        """Format timestamp for display"""
        dt = datetime.fromisoformat(timestamp)
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "Just now"
    
    def create_critical_alert(self, patient_name: str, vital_sign: str, value: str):
        """Create critical value alert"""
        self.add_notification(
            title="🚨 CRITICAL VALUE ALERT",
            message=f"Patient {patient_name}: {vital_sign} = {value}",
            type="critical",
            priority="critical"
        )
    
    def create_appointment_reminder(self, patient_name: str, appointment_time: str):
        """Create appointment reminder"""
        self.add_notification(
            title="📅 Appointment Reminder",
            message=f"Upcoming appointment: {patient_name} at {appointment_time}",
            type="info",
            priority="normal"
        )