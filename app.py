"""
Securities Fraud Prevention System - Streamlit Demo
Integrates URL detection with SEBI Safe Space initiative
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random
import hashlib
from typing import Dict, List, Optional, Tuple
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass, asdict
import time

# Configure page
st.set_page_config(
    page_title="SEBI Fraud Prevention System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for better UI/UX
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f2937;
        --secondary-color: #3b82f6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --bg-light: #f8fafc;
        --text-light: #64748b;
    }
    
    /* Custom badges */
    .risk-high {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 2px solid #fca5a5;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(239, 68, 68, 0.1);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        color: #92400e;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 2px solid #fdba74;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 2px solid #6ee7b7;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1);
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    /* Alert boxes */
    .alert-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #10b981;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
        color: #065f46;
        font-weight: 500;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        border-left: 5px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
        color: #92400e;
        font-weight: 500;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #ef4444;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
        color: #991b1b;
        font-weight: 500;
    }
    
    /* Live monitoring styles */
    .live-threat {
        background: #1e293b;
        color: #e2e8f0;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #3b82f6;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.9rem;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .threat-high { border-left-color: #ef4444; }
    .threat-medium { border-left-color: #f59e0b; }
    .threat-low { border-left-color: #10b981; }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    
    /* Progress bars */
    .progress-bar {
        width: 100%;
        height: 8px;
        background-color: #e5e7eb;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 50%, #ef4444 100%);
        transition: width 0.3s ease;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom containers */
    .main-container {
        padding: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .status-active { background-color: #10b981; }
    .status-warning { background-color: #f59e0b; }
    .status-error { background-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# ============= Data Models =============
@dataclass
class MediaRef:
    type: str
    hash: Optional[str] = None

@dataclass
class Context:
    channel: Optional[str] = None
    message_id: Optional[str] = None
    text: Optional[str] = None
    mentions: Optional[List[str]] = None
    tickers: Optional[List[str]] = None
    media: Optional[List[MediaRef]] = None
    detected_app: Optional[str] = None

# ============= Core URL Detector (Your Module) =============
class URLDetector:
    """Simulates your existing URL detection module"""
    
    def __init__(self):
        self.suspicious_patterns = [
            'guaranteed-return', 'double-money', 'insider-tip',
            'free-advice', 'hot-stock', 'pump-profit', 'quick-rich'
        ]
        self.malicious_domains = [
            'scam-broker.com', 'fake-sebi.in', 'phish-trade.net'
        ]
        
    def score_url(self, url: str) -> dict:
        """Your existing URL scoring function"""
        risk_score = 0.1
        signals = {}
        
        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if pattern in url.lower():
                risk_score += 0.15
                signals['suspicious_pattern'] = True
                
        # Check domain age (simulated)
        domain = url.split('/')[2] if '/' in url else url
        if any(mal in domain for mal in self.malicious_domains):
            risk_score += 0.5
            signals['known_malicious'] = True
            
        # Calculate entropy
        entropy = self._calculate_entropy(url)
        signals['entropy'] = round(entropy, 2)
        if entropy > 4.5:
            risk_score += 0.2
            signals['high_entropy'] = True
            
        # Check for typosquatting
        if self._check_typosquat(domain):
            risk_score += 0.25
            signals['typosquat'] = True
            
        risk_score = min(risk_score, 1.0)
        
        label = 'benign' if risk_score < 0.3 else ('suspicious' if risk_score < 0.7 else 'malicious')
        
        return {
            'risk': risk_score,
            'label': label,
            'signals': signals,
            'model_version': 'v2.1.0'
        }
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy"""
        if not text:
            return 0
        entropy = 0
        for char in set(text):
            p = text.count(char) / len(text)
            entropy -= p * np.log2(p)
        return entropy
    
    def _check_typosquat(self, domain: str) -> bool:
        """Check for tynosquatting patterns"""
        legitimate = ['sebi', 'nse', 'bse', 'zerodha', 'groww', 'upstox']
        for legit in legitimate:
            if legit in domain and not domain.startswith(legit):
                return True
        return False

# ============= Enrichment Functions =============
def check_advisor_identity(context: dict) -> Tuple[float, dict]:
    """Check against SEBI registered advisor database"""
    evidence = {'checked': False, 'matched': False, 'registry_id': None}
    
    if context.get('mentions'):
        evidence['checked'] = True
        if random.random() > 0.7:
            evidence['matched'] = True
            evidence['registry_id'] = f"SEBI/RA/{random.randint(1000,9999)}"
            return 0.1, evidence
        return 0.6, evidence
    
    return 0.1, evidence

def social_coordination_score(context: dict) -> Tuple[float, dict]:
    """Detect coordinated campaigns across channels"""
    evidence = {'cluster_size': 0, 'time_window_minutes': 0}
    
    if context.get('tickers'):
        cluster_size = random.randint(1, 50)
        evidence['cluster_size'] = cluster_size
        evidence['time_window_minutes'] = random.randint(5, 60)
        
        if cluster_size > 20:
            return 0.8, evidence
        elif cluster_size > 10:
            return 0.5, evidence
    
    return 0.1, evidence

def app_impersonation_score(context: dict) -> Tuple[float, dict]:
    """Detect fake trading app promotions"""
    evidence = {'app_detected': False, 'legitimate': False}
    
    if context.get('detected_app'):
        evidence['app_detected'] = True
        legitimate_apps = ['Zerodha', 'Groww', 'Upstox', 'Angel One', 'ICICI Direct']
        
        if context['detected_app'] not in legitimate_apps:
            evidence['legitimate'] = False
            return 0.7, evidence
        else:
            evidence['legitimate'] = True
            return 0.05, evidence
    
    return 0.05, evidence

def media_fabrication_score(context: dict) -> Tuple[float, dict]:
    """Check for deepfakes and manipulated media"""
    evidence = {'media_count': 0, 'deepfake_detected': False}
    
    if context.get('media'):
        evidence['media_count'] = len(context['media'])
        if random.random() > 0.85:
            evidence['deepfake_detected'] = True
            return 0.8, evidence
        return 0.2, evidence
    
    return 0.0, evidence

def announcement_credibility_score(context: dict) -> Tuple[float, dict]:
    """Cross-verify against official exchange announcements"""
    evidence = {'announcement_type': None, 'verified': False}
    
    if context.get('text') and any(word in context['text'].lower() for word in ['ipo', 'dividend', 'split', 'bonus']):
        evidence['announcement_type'] = 'corporate_action'
        evidence['verified'] = random.random() > 0.6
        
        if not evidence['verified']:
            return 0.7, evidence
        return 0.05, evidence
    
    return 0.05, evidence

# ============= Risk Scoring Engine =============
class RiskScoringEngine:
    def __init__(self):
        self.url_detector = URLDetector()
        self.weights = {
            'url': 0.45,
            'identity': 0.15,
            'social': 0.15,
            'app_impersonation': 0.10,
            'media': 0.10,
            'announcement': 0.05
        }
    
    def score(self, url: str, context: Optional[Context] = None) -> dict:
        url_result = self.url_detector.score_url(url)
        ctx = asdict(context) if context else {}
        
        s_url = url_result['risk']
        s_identity, e_identity = check_advisor_identity(ctx)
        s_social, e_social = social_coordination_score(ctx)
        s_app, e_app = app_impersonation_score(ctx)
        s_media, e_media = media_fabrication_score(ctx)
        s_ann, e_ann = announcement_credibility_score(ctx)
        
        final = (
            self.weights['url'] * s_url +
            self.weights['identity'] * s_identity +
            self.weights['social'] * s_social +
            self.weights['app_impersonation'] * s_app +
            self.weights['media'] * s_media +
            self.weights['announcement'] * s_ann
        )
        
        label = 'low' if final < 0.45 else ('medium' if final < 0.75 else 'high')
        
        explanations = []
        if s_url > 0.5:
            explanations.append({'signal': 'url_risk', 'value': s_url, 'weight': self.weights['url']})
        if s_identity > 0.3:
            explanations.append({'signal': 'unregistered_advisor', 'value': s_identity, 'weight': self.weights['identity']})
        if s_social > 0.3:
            explanations.append({'signal': 'coordinated_campaign', 'value': s_social, 'weight': self.weights['social']})
        if s_app > 0.3:
            explanations.append({'signal': 'app_impersonation', 'value': s_app, 'weight': self.weights['app_impersonation']})
        if s_media > 0.3:
            explanations.append({'signal': 'media_manipulation', 'value': s_media, 'weight': self.weights['media']})
        if s_ann > 0.3:
            explanations.append({'signal': 'false_announcement', 'value': s_ann, 'weight': self.weights['announcement']})
        
        return {
            'url': url,
            'scores': {
                'url': round(s_url, 3),
                'identity': round(s_identity, 3),
                'social': round(s_social, 3),
                'app_impersonation': round(s_app, 3),
                'media': round(s_media, 3),
                'announcement': round(s_ann, 3),
                'final': round(final, 3)
            },
            'label': label,
            'explanations': sorted(explanations, key=lambda x: x['value'], reverse=True)[:3],
            'evidence': {
                'url_signals': url_result['signals'],
                'advisor': e_identity,
                'social': e_social,
                'app': e_app,
                'media': e_media,
                'announcement': e_ann
            },
            'model_versions': {
                'url_model': url_result['model_version'],
                'fusion': 'v1.0.0'
            },
            'created_at': datetime.now().isoformat()
        }

# ============= Session State Management =============
if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'engine' not in st.session_state:
    st.session_state.engine = RiskScoringEngine()
if 'alerts_sent' not in st.session_state:
    st.session_state.alerts_sent = 0
if 'live_monitoring' not in st.session_state:
    st.session_state.live_monitoring = False
if 'threat_feed' not in st.session_state:
    st.session_state.threat_feed = []

# ============= Helper Functions =============
def generate_sample_data(n=20):
    """Generate sample fraud cases for demonstration"""
    channels = ['telegram', 'whatsapp', 'twitter', 'facebook', 'discord']
    sample_urls = [
        'https://guaranteed-returns.in/invest',
        'https://sebi-approved.fake/register',
        'https://insider-tips.club/premium',
        'https://legitimate-broker.com/login',
        'https://pump-profit.net/join',
        'https://double-money.biz/scheme',
        'https://nse.in/announcements',
        'https://fake-zerodha.in/open-account',
        'https://hot-stocks-2025.com/buy-now',
        'https://crypto-pump.org/signals'
    ]
    
    sample_texts = [
        "Guaranteed 30% monthly returns! Join now",
        "SEBI registered advisor sharing insider tips",
        "This stock will double tomorrow, buy NOW!",
        "Free demat account with bonus",
        "Pump and dump group - 1000% profits",
        "Legitimate investment opportunity",
        "Official NSE announcement",
        "Download our trading app for hot tips"
    ]
    
    cases = []
    for _ in range(n):
        url = random.choice(sample_urls) + f"/{random.randint(100,999)}"
        context = Context(
            channel=random.choice(channels),
            message_id=f"msg_{random.randint(10000,99999)}",
            text=random.choice(sample_texts),
            mentions=[f"@advisor_{random.randint(100,999)}"] if random.random() > 0.5 else None,
            tickers=[f"STOCK{random.randint(1,100)}"] if random.random() > 0.6 else None,
            media=[MediaRef(type='image', hash=hashlib.md5(str(random.random()).encode()).hexdigest())] if random.random() > 0.7 else None,
            detected_app=random.choice(['FakeTradePro', 'Zerodha', 'ScamBroker', None])
        )
        
        result = st.session_state.engine.score(url, context)
        result['channel'] = context.channel
        result['message_text'] = context.text[:50] + '...' if context.text and len(context.text) > 50 else context.text
        cases.append(result)
    
    return cases

def render_risk_badge(label):
    """Render enhanced risk badge"""
    return f'<span class="risk-{label}">{label.upper()}</span>'

def generate_live_threat():
    """Generate a simulated live threat"""
    threats = [
        f"https://scam-{random.randint(100,999)}.fake/offer",
        f"https://pump-group-{random.randint(100,999)}.net/join",
        f"https://fake-advisor-{random.randint(100,999)}.in/tips",
        f"https://guarantee-profit-{random.randint(100,999)}.com/scheme",
        f"https://insider-{random.randint(100,999)}.club/premium"
    ]
    
    url = random.choice(threats)
    context = Context(
        channel=random.choice(['telegram', 'whatsapp', 'twitter', 'discord']),
        text=f"Live threat detected at {datetime.now().strftime('%H:%M:%S')}"
    )
    
    result = st.session_state.engine.score(url, context)
    result['timestamp'] = datetime.now().strftime('%H:%M:%S')
    result['channel'] = context.channel
    
    return result

# ============= Main App =============
def main():
    # Header with enhanced styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">🛡️ SEBI Securities Fraud Prevention</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Real-time URL Risk Detection & Fraud Prevention System</p>
        <div style="margin-top: 1rem;">
            <span class="status-indicator status-active"></span>
            <span style="font-size: 0.9rem;">System Status: Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions Bar
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🔍 Quick Scan", use_container_width=True):
            st.session_state.active_tab = "scanner"
    
    with col2:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.active_tab = "dashboard"
    
    with col3:
        monitoring_text = "⏹️ Stop Monitor" if st.session_state.get('live_monitoring', False) else "🚨 Start Monitor"
        if st.button(monitoring_text, use_container_width=True):
            st.session_state.live_monitoring = not st.session_state.get('live_monitoring', False)
            st.rerun()
    
    with col4:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.active_tab = "analytics"
    
    with col5:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.active_tab = "settings"
    
    st.divider()
    
    # Main Content Area with Live Monitoring Integrated
    col_main, col_sidebar = st.columns([3, 1])
    
    with col_main:
        # URL Scanner Section
        st.markdown("### 🔍 URL Risk Scanner")
        
        with st.container():
            st.markdown('<div class="main-container">', unsafe_allow_html=True)
            
            url_input = st.text_input(
                "Enter URL to analyze:",
                placeholder="https://suspicious-investment-site.com/offer",
                help="Paste any suspicious URL to get instant fraud risk assessment"
            )
            
            # Enhanced context input in expandable section
            with st.expander("🎯 Add Context for Better Analysis", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    channel = st.selectbox("Source Channel", 
                        ["None", "Telegram", "WhatsApp", "Twitter", "Facebook", "Discord", "Email"],
                        help="Where was this URL found?"
                    )
                    
                    text = st.text_area(
                        "Message Content", 
                        placeholder="Enter the message text that contained this URL...",
                        height=80
                    )
                    
                    mentions = st.text_input(
                        "Mentioned Users/Advisors", 
                        placeholder="@trading_guru, @stock_expert"
                    )
                
                with col2:
                    tickers = st.text_input(
                        "Stock Tickers Mentioned", 
                        placeholder="RELIANCE, TCS, INFY, ADANIENT"
                    )
                    
                    detected_app = st.text_input(
                        "App/Platform Mentioned", 
                        placeholder="Zerodha, Groww, custom trading app"
                    )
                    
                    has_media = st.checkbox("Contains Media Files", help="Images, videos, or documents")
            
            # Scan button with enhanced styling
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                scan_clicked = st.button("🔍 ANALYZE URL FOR FRAUD", type="primary", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Analysis Results
            if scan_clicked and url_input:
                with st.spinner("🔄 Analyzing URL for fraud indicators..."):
                    # Build context
                    context = Context(
                        channel=channel.lower() if channel != "None" else None,
                        text=text if text else None,
                        mentions=mentions.split(',') if mentions else None,
                        tickers=tickers.split(',') if tickers else None,
                        media=[MediaRef(type='image', hash='sample_hash')] if has_media else None,
                        detected_app=detected_app if detected_app else None
                    )
                    
                    # Score URL
                    result = st.session_state.engine.score(url_input, context)
                    st.session_state.cases.insert(0, result)
                    
                    time.sleep(1.5)  # Simulate processing
                    
                    # Results Display
                    st.markdown("### 📊 Analysis Results")
                    
                    # Alert based on risk level
                    if result['scores']['final'] >= 0.75:
                        st.markdown(f'<div class="alert-danger">🚨 <strong>HIGH RISK DETECTED!</strong> This URL poses significant fraud risk. Auto-alert has been triggered.</div>', unsafe_allow_html=True)
                        st.session_state.alerts_sent += 1
                    elif result['scores']['final'] >= 0.45:
                        st.markdown(f'<div class="alert-warning">⚠️ <strong>MEDIUM RISK</strong> Manual review recommended for this URL.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="alert-success">✅ <strong>LOW RISK</strong> This URL appears to be legitimate.</div>', unsafe_allow_html=True)
                    
                    # Risk Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "🎯 Risk Level", 
                            result['label'].upper(),
                            help="Overall risk classification"
                        )
                    
                    with col2:
                        st.metric(
                            "📊 Final Score", 
                            f"{result['scores']['final']:.3f}",
                            help="Composite risk score (0-1)"
                        )
                    
                    with col3:
                        st.metric(
                            "🔍 URL Risk", 
                            f"{result['scores']['url']:.3f}",
                            help="Base URL analysis score"
                        )
                    
                    with col4:
                        st.metric(
                            "👥 Social Risk", 
                            f"{result['scores']['social']:.3f}",
                            help="Coordinated campaign indicators"
                        )
                    
                    # Component Analysis Chart
                    st.markdown("#### 📈 Risk Component Breakdown")
                    
                    scores_df = pd.DataFrame([result['scores']])
                    scores_df = scores_df.drop('final', axis=1)
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=list(scores_df.columns), 
                            y=scores_df.iloc[0].values,
                            marker_color=[
                                '#ef4444' if v > 0.7 else '#f59e0b' if v > 0.4 else '#10b981' 
                                for v in scores_df.iloc[0].values
                            ],
                            text=[f'{v:.3f}' for v in scores_df.iloc[0].values],
                            textposition='auto',
                        )
                    ])
                    
                    fig.update_layout(
                        title="Risk Component Analysis",
                        xaxis_title="Risk Components",
                        yaxis_title="Risk Score",
                        showlegend=False,
                        height=350,
                        template="plotly_white"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Top Risk Signals
                    if result['explanations']:
                        st.markdown("#### 🚩 Top Risk Signals")
                        for i, exp in enumerate(result['explanations'], 1):
                            st.markdown(f"**{i}.** {exp['signal'].replace('_', ' ').title()}: `{exp['value']:.3f}` (Weight: {exp['weight']:.2f})")
                    
                    # Evidence Details
                    with st.expander("🔬 Detailed Evidence & Technical Details"):
                        st.json(result['evidence'])
            
            elif scan_clicked and not url_input:
                st.error("⚠️ Please enter a URL to analyze")
    
    with col_sidebar:
        # Live Monitoring Panel
        st.markdown("### 🚨 Live Threat Monitor")
        
        # System Status
        if st.session_state.get('live_monitoring', False):
            st.markdown('<span class="status-indicator status-active"></span> **ACTIVE** - Monitoring enabled', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-error"></span> **INACTIVE** - Click start to monitor', unsafe_allow_html=True)
        
        st.divider()
        
        # Quick Stats
        total_cases = len(st.session_state.cases)
        high_risk = len([c for c in st.session_state.cases if c['label'] == 'high'])
        
        st.metric("📈 Total Analyzed", total_cases, delta=f"+{random.randint(2,8)}")
        st.metric("🚨 High Risk", high_risk, delta=f"+{random.randint(0,3)}")
        st.metric("📤 Alerts Sent", st.session_state.alerts_sent)
        
        st.divider()
        
        # Live Threat Feed
        st.markdown("#### 🔄 Live Threat Feed")
        
        threat_container = st.container()
        
        # Auto-refresh for live monitoring
        if st.session_state.get('live_monitoring', False):
            # Generate new threats periodically
            if random.random() > 0.7:  # 30% chance each refresh
                new_threat = generate_live_threat()
                st.session_state.threat_feed.insert(0, new_threat)
                st.session_state.threat_feed = st.session_state.threat_feed[:10]  # Keep last 10
            
            # Display threats
            for threat in st.session_state.threat_feed[:5]:
                risk_class = f"threat-{threat['label']}"
                
                threat_container.markdown(f"""
                <div class="live-threat {risk_class}">
                    <strong>{threat['timestamp']}</strong> | {threat['channel']}<br>
                    <span style="font-size: 0.8rem;">{threat['url'][:30]}...</span><br>
                    <span style="color: #64748b;">Risk: {threat['scores']['final']:.3f}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Auto-refresh every 3 seconds
            time.sleep(3)
            st.rerun()
        else:
            st.info("🔘 Start monitoring to see live threat feed")
        
        st.divider()
        
        # Quick Actions
        st.markdown("#### ⚡ Quick Actions")
        
        if st.button("📋 Generate Sample Data", use_container_width=True):
            st.session_state.cases.extend(generate_sample_data(10))
            st.success("Sample data added!")
            
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.cases = []
            st.session_state.threat_feed = []
            st.success("Data cleared!")
        
        if st.button("📊 View Full Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
    
    # Recent Analysis History
    if st.session_state.cases:
        st.markdown("### 📝 Recent Analysis History")
        
        with st.container():
            st.markdown('<div class="main-container">', unsafe_allow_html=True)
            
            # Search and filter
            search_term = st.text_input("🔎 Search URLs or content...", placeholder="Enter search term")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                risk_filter = st.selectbox("Filter by Risk", ["All", "High", "Medium", "Low"])
            with col2:
                channel_filter = st.selectbox("Filter by Channel", ["All"] + list(set([c.get('channel', 'unknown') for c in st.session_state.cases])))
            with col3:
                limit = st.selectbox("Show Results", [10, 25, 50, 100])
            
            # Filter data
            filtered_cases = st.session_state.cases.copy()
            
            if search_term:
                filtered_cases = [c for c in filtered_cases if search_term.lower() in c['url'].lower()]
            
            if risk_filter != "All":
                filtered_cases = [c for c in filtered_cases if c['label'] == risk_filter.lower()]
            
            if channel_filter != "All":
                filtered_cases = [c for c in filtered_cases if c.get('channel') == channel_filter]
            
            # Display results
            for i, case in enumerate(filtered_cases[:limit]):
                with st.expander(f"#{i+1} - {case['url'][:60]}... | {render_risk_badge(case['label'])}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**URL:** {case['url']}")
                        if case.get('message_text'):
                            st.write(f"**Context:** {case['message_text']}")
                        st.write(f"**Channel:** {case.get('channel', 'Unknown')}")
                        st.write(f"**Timestamp:** {case['created_at'][:19]}")
                    
                    with col2:
                        st.metric("Final Score", f"{case['scores']['final']:.3f}")
                        st.metric("URL Risk", f"{case['scores']['url']:.3f}")
                        
                        if case['explanations']:
                            st.write("**Top Signal:**")
                            st.write(f"• {case['explanations'][0]['signal']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

