import streamlit as st
import time
import random

class HospitalPreloader:
    """Creative and funny hospital-themed preloader"""
    
    @staticmethod
    def show_preloader():
        """Display the creative hospital preloader"""
        
        # Funny hospital loading messages
        loading_messages = [
            "🏥 Sanitizing the digital stethoscope...",
            "💊 Counting pills in the virtual pharmacy...",
            "🚑 Starting the ambulance... beep beep!",
            "👩‍⚕️ Waking up the night shift nurses...",
            "🩺 Calibrating the AI doctor's bedside manner...",
            "🧬 Analyzing DNA... finding the fun gene...",
            "💉 Preparing the injection of awesomeness...",
            "🏥 Checking if the hospital wifi password is still 'password123'...",
            "👨‍⚕️ Teaching the robots to say 'It's just a flu'...",
            "🦴 Counting bones... yep, still 206!",
            "❤️ Pumping up the artificial heart...",
            "🧠 Loading brain.exe... please wait...",
            "🏥 Disinfecting the servers with digital hand sanitizer...",
            "💻 Rebooting the coffee machine (most important!)",
            "🚨 Testing emergency dad jokes...",
            "📊 Calculating how many cups of coffee = productivity...",
            "🔬 Mixing the perfect blend of AI and caffeine...",
            "🏥 Ensuring all digital patients are comfortable...",
            "💾 Saving lives... and data...",
            "⚡ Charging the defibrillator batteries..."
        ]
        
        # Create placeholder for dynamic content
        placeholder = st.empty()
        
        # Progress bar
        progress_bar = st.progress(0)
        
        # Status message placeholder
        status_placeholder = st.empty()
        
        # Total loading time
        total_steps = 20
        
        for i in range(total_steps + 1):
            # Update progress
            progress = i / total_steps
            progress_bar.progress(progress)
            
            # Random funny message
            if i < len(loading_messages):
                message = loading_messages[i]
            else:
                message = random.choice(loading_messages)
            
            # Dynamic ASCII art based on progress
            ascii_art = HospitalPreloader._get_loading_art(progress)
            
            # Update the placeholder with current state
            placeholder.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <h1 style="color: #00ff88; font-family: 'Orbitron', monospace; margin-bottom: 30px;">
                    ⚡ PULSEAI INITIALIZING ⚡
                </h1>
                
                <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid rgba(0, 255, 136, 0.3); 
                            border-radius: 15px; padding: 30px; margin: 20px 0; font-family: monospace;">
                    <pre style="color: #00ccff; font-size: 12px; line-height: 1.2;">{ascii_art}</pre>
                </div>
                
                <div style="background: linear-gradient(45deg, rgba(0, 255, 136, 0.2), rgba(0, 204, 255, 0.2)); 
                            border-radius: 10px; padding: 15px; margin: 15px 0;">
                    <h3 style="color: #ffffff; margin: 0;">{message}</h3>
                </div>
                
                <div style="margin: 20px 0;">
                    <span style="color: #00ff88; font-size: 18px; font-weight: bold;">
                        {int(progress * 100)}% Complete
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Fun status updates
            if progress < 0.3:
                status_placeholder.info("🏥 Booting up hospital systems...")
            elif progress < 0.6:
                status_placeholder.warning("⚕️ Loading medical databases...")
            elif progress < 0.9:
                status_placeholder.success("🚀 Almost ready for takeoff!")
            else:
                status_placeholder.success("✅ PulseAI is ready to save the day!")
            
            # Variable sleep time for more realistic loading
            if i < 5:
                time.sleep(0.3)  # Slower start
            elif i < 15:
                time.sleep(0.2)  # Medium speed
            else:
                time.sleep(0.1)  # Faster finish
        
        # Final celebration
        placeholder.markdown("""
        <div style="text-align: center; padding: 40px;">
            <h1 style="color: #00ff88; font-family: 'Orbitron', monospace; animation: pulse 2s infinite;">
                🎉 WELCOME TO PULSEAI! 🎉
            </h1>
            <h3 style="color: #00ccff;">Your AI-Powered Healthcare Command Center is Ready!</h3>
            
            <style>
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            </style>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(2)
        
        # Clear everything
        placeholder.empty()
        progress_bar.empty()
        status_placeholder.empty()
    
    @staticmethod
    def _get_loading_art(progress: float) -> str:
        """Get ASCII art based on loading progress"""
        
        if progress < 0.2:
            return """
    ╔══════════════════════════════════════╗
    ║           🏥 HOSPITAL LOADING...     ║
    ║                                      ║
    ║     [    ]  💊  💉  🩺              ║
    ║                                      ║
    ║          Please wait patiently       ║
    ╚══════════════════════════════════════╝
            """
        elif progress < 0.4:
            return """
    ╔══════════════════════════════════════╗
    ║        🚑 AMBULANCE ARRIVING...      ║
    ║                                      ║
    ║     [██  ]  💊  💉  🩺              ║
    ║                                      ║
    ║       Loading medical equipment      ║
    ╚══════════════════════════════════════╝
            """
        elif progress < 0.6:
            return """
    ╔══════════════════════════════════════╗
    ║       👩‍⚕️ DOCTORS ARRIVING...        ║
    ║                                      ║
    ║     [████]  💊  💉  🩺              ║
    ║                                      ║
    ║        Preparing patient rooms       ║
    ╚══════════════════════════════════════╝
            """
        elif progress < 0.8:
            return """
    ╔══════════════════════════════════════╗
    ║       ⚡ AI SYSTEMS ONLINE...        ║
    ║                                      ║
    ║     [██████]  💊  💉  🩺            ║
    ║                                      ║
    ║         Calibrating instruments      ║
    ╚══════════════════════════════════════╝
            """
        else:
            return """
    ╔══════════════════════════════════════╗
    ║       ✅ HOSPITAL READY TO SERVE!    ║
    ║                                      ║
    ║     [████████]  💊  💉  🩺          ║
    ║                                      ║
    ║          All systems operational     ║
    ╚══════════════════════════════════════╝
            """
    
    @staticmethod
    def show_mini_loader(message: str = "Processing..."):
        """Show a mini loader for quick operations"""
        with st.spinner(f"🏥 {message}"):
            time.sleep(1)