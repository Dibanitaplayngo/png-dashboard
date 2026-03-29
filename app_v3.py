import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import sqlite3
import json

st.set_page_config(page_title="PNG Intelligence Platform", page_icon="🎰", layout="wide")

def init_db():
    conn = sqlite3.connect("png_intelligence.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS weekly_briefs (id INTEGER PRIMARY KEY, created_at TEXT, brief TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS message_tests (id INTEGER PRIMARY KEY, created_at TEXT, original TEXT, variations TEXT, predicted_winner TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS budget_history (id INTEGER PRIMARY KEY, created_at TEXT, allocation TEXT)""")
    conn.commit()
    conn.close()

init_db()

random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=30)
platforms = ["Twitter/X", "LinkedIn", "Instagram", "Facebook", "Twitch", "Snapchat"]
eng_rates = [6.1, 4.2, 7.4, 2.8, 3.6, 2.1]
followers = [82000, 61000, 94000, 28000, 12000, 7000]
competitors = ["Pragmatic Play", "NetEnt", "Playtech", "Merkur Gaming", "Play'n GO"]
comp_followers = [412000, 198000, 289000, 87000, 284000]
comp_eng = [3.1, 5.4, 2.8, 1.9, 4.7]
comp_freq = [14, 9, 11, 5, 12]

def rand_series(base, noise=0.15):
    return [round(base * (1 + random.uniform(-noise, noise)), 2) for _ in range(30)]

# MOCK DATASETS
games_data = pd.DataFrame({
    "Game": ["Book of Dead","Reactoonz","Fire Joker","Rise of Olympus","Moon Princess","Cat Wilde","Solar Temple","Banana Rock","Legacy of Dead","Elephant King"],
    "Social Engagement Score": [9.4,8.8,7.2,8.1,7.9,7.4,6.8,6.2,8.5,5.9],
    "Search Demand Index": [95,82,71,78,74,69,58,52,88,44],
    "Affiliate Visibility": [92,78,65,71,68,62,54,48,84,41],
    "Casino Distribution": [88,74,69,76,72,65,58,51,82,45],
    "Revenue Proxy Score": [94,81,68,75,71,64,57,50,83,43],
    "Lifecycle Stage": ["Mature","Mature","Growth","Mature","Growth","Growth","Launch","Launch","Mature","Decline"],
    "Trend": ["Stable","Rising","Rising","Stable","Rising","Rising","Hot","Emerging","Stable","Declining"],
})

casino_data = pd.DataFrame({
    "Casino": ["Bet365","LeoVegas","888 Casino","Casumo","Unibet","Mr Green","William Hill","Betway","PokerStars","Rizk"],
    "Play'n GO Featured": [True,True,True,True,False,True,True,False,True,True],
    "Homepage Placement": ["Yes","Yes","No","Yes","No","Yes","No","No","Yes","Yes"],
    "Pragmatic Featured": [True,True,True,True,True,True,True,True,True,True],
    "NetEnt Featured": [True,True,True,False,True,True,True,True,False,True],
    "PNG Game Count": [45,38,29,41,0,35,27,0,31,42],
    "Comp Avg Game Count": [62,58,51,54,48,55,49,52,47,53],
    "Market": ["UK","UK/SE","UK","SE","EU","SE/UK","UK","Global","Global","SE"],
})

player_insights = pd.DataFrame({
    "Theme": ["Bonus Buy Feature","High Volatility Slots","Free Spins Rounds","Multipliers","Megaways Mechanic","Retrigger Potential","RTP Transparency","Mobile Experience","Load Speed","Sound Design"],
    "Sentiment Score": [8.9,8.4,8.7,8.2,7.9,7.6,7.1,8.5,7.8,7.3],
    "Volume (mentions)": [12400,10800,9600,8900,7400,6200,5800,9100,6700,4300],
    "PNG Delivers": ["⚠️ Partial","✅ Strong","✅ Strong","✅ Strong","⚠️ Partial","✅ Strong","⚠️ Partial","✅ Strong","✅ Strong","✅ Strong"],
    "Competitor Advantage": ["Pragmatic","None","None","None","Big Time Gaming","None","NetEnt","None","None","None"],
})

search_trends = pd.DataFrame({
    "Keyword": ["bonus buy slots","high volatility slots 2025","best megaways slots","book of dead free spins","reactoonz strategy","pragmatic play new slots","png slots","slot rtp list","mobile casino slots","no wagering slots"],
    "Search Volume": [8900,7200,6800,5400,4200,9800,3100,5600,8100,6400],
    "Trend": ["+45%","+38%","+29%","+12%","+18%","+67%","+8%","+22%","+41%","+55%"],
    "PNG Relevance": ["🔴 Gap","✅ Strong","⚠️ Partial","✅ Strong","✅ Strong","❌ Competitor","⚠️ Low vol","⚠️ Partial","✅ Strong","🔴 Gap"],
    "Opportunity": ["High","Low","Medium","Low","Low","Monitor","Low","Medium","Low","High"],
})

bonus_intel = pd.DataFrame({
    "Casino/Affiliate": ["LeoVegas","888 Casino","Casumo","Unibet","Mr Green","Rizk","Betway","PokerStars"],
    "Offer Type": ["Free Spins - Book of Dead","No Wagering Bonus","Reload + Spins","Welcome + Spins","Bonus Buy Promo","Race + Spins","High Vol Pack","Megaways Bundle"],
    "PNG Featured": ["✅ Yes","✅ Yes","⚠️ Partial","❌ No","❌ No","✅ Yes","❌ No","❌ No"],
    "Competitor Featured": ["Pragmatic","NetEnt","Pragmatic","Pragmatic","Pragmatic","NetEnt","Pragmatic","BTG"],
    "Est. Player Reach": [42000,38000,29000,51000,34000,22000,44000,31000],
    "Promo Frequency": ["Weekly","Monthly","Bi-weekly","Weekly","Monthly","Weekly","Bi-weekly","Monthly"],
})

streaming_data = pd.DataFrame({
    "Creator": ["Roshtein","CasinoGrounds","LetsGiveItASpin","ClassyBeef","Xposed","NickSlots","SlotLady","Brian Christopher","Casinodaddy","DeuceAce"],
    "Platform": ["Twitch","YouTube","YouTube","Twitch","YouTube","YouTube","YouTube","YouTube","Twitch","Twitch"],
    "Monthly Views": [8400000,6200000,5100000,4800000,3900000,3400000,2800000,2600000,2200000,1900000],
    "PNG Coverage": ["High","High","Medium","Low","Medium","Low","Medium","Low","High","Medium"],
    "Top PNG Game": ["Book of Dead","Book of Dead","Reactoonz","Rise of Olympus","Book of Dead","Legacy of Dead","Fire Joker","Book of Dead","Reactoonz","Moon Princess"],
    "Competitor Preference": ["Neutral","Neutral","Pragmatic","Pragmatic","Neutral","Pragmatic","Neutral","Pragmatic","Neutral","Neutral"],
})

affiliate_data = pd.DataFrame({
    "Affiliate Site": ["AskGamblers","Casino Guru","OLBG","Bojoko","Casinomeister","TopCasino","SlotCatalog","LCB","CasinoFever","NonStopCasino"],
    "Domain Authority": [82,79,74,71,68,65,72,69,61,58],
    "PNG Visibility Score": [78,82,65,71,58,62,88,69,54,71],
    "Pragmatic Score": [92,89,84,87,79,81,91,82,76,83],
    "PNG Games Listed": [180,195,142,161,128,138,210,155,119,148],
    "Comp Avg Listed": [220,235,198,214,186,195,248,201,174,192],
    "Review Sentiment": ["Positive","Very Positive","Positive","Positive","Neutral","Positive","Very Positive","Positive","Neutral","Positive"],
})

geo_data = pd.DataFrame({
    "Market": ["UK","Sweden","Germany","Spain","Canada","Netherlands","Finland","Denmark","Norway","Portugal"],
    "Market Size (M players)": [8.4,2.1,6.8,3.9,4.2,2.8,1.4,1.2,1.1,1.8],
    "PNG Market Share": [18,24,12,15,9,16,28,22,25,11],
    "Growth Rate": ["+4%","+12%","+28%","+18%","+22%","+35%","+8%","+9%","+11%","+41%"],
    "Competitor Dominance": ["Pragmatic","NetEnt","Pragmatic","Pragmatic","Pragmatic","Pragmatic","NetEnt","NetEnt","NetEnt","Pragmatic"],
    "Regulatory Status": ["Stable","Stable","Expanding","Stable","Expanding","New","Stable","Stable","Stable","New"],
    "Opportunity Score": [6,7,9,7,8,9,6,6,7,9],
})

regulatory_data = pd.DataFrame({
    "Market": ["Brazil","USA (Michigan)","India","Japan","UAE","Colombia","Mexico","Greece","Romania","South Africa"],
    "Status": ["Opening 2025","Live - Expanding","Watching","Long-term","Exploratory","Expanding","Expanding","Stable","Expanding","Watching"],
    "Market Size Est.": ["$2.1B","$890M","$1.4B","$3.2B","$680M","$420M","$580M","$310M","$270M","$490M"],
    "PNG Presence": ["❌ None","⚠️ Limited","❌ None","❌ None","❌ None","✅ Active","✅ Active","✅ Active","✅ Active","❌ None"],
    "Priority": ["🔴 High","🔴 High","🟡 Medium","🟡 Medium","🟡 Medium","🟢 Monitor","🟢 Monitor","🟢 Monitor","🟢 Monitor","🟡 Medium"],
    "Action": ["Prepare launch","Scale","Research","Watch","Partner explore","Grow","Grow","Maintain","Maintain","Research"],
})

fatigue_data = pd.DataFrame({
    "Game": ["Book of Dead","Fire Joker","Gemix","Wild Falls","Flame Busters","Dark Vortex","Sakura Fortune","Champion of the Track","Ninja Fruits","Tower Quest"],
    "Peak Engagement": [9.4,7.2,7.8,6.4,6.1,7.9,6.8,5.9,5.4,5.1],
    "Current Engagement": [9.1,5.8,4.2,3.1,2.8,6.4,3.9,2.4,2.1,1.8],
    "Decline %": [-3,-19,-46,-52,-54,-19,-43,-59,-61,-65],
    "Status": ["✅ Healthy","⚠️ Watch","🔴 Fatigued","🔴 Fatigued","🔴 Fatigued","✅ Healthy","🔴 Fatigued","🔴 Fatigued","🔴 Fatigued","🔴 Fatigued"],
    "Recommended Action": ["Maintain","New promo push","Archive/relaunch","Retire","Retire","Feature more","Archive","Retire","Retire","Retire"],
})

attribution_data = {
    "social_reach": 500000,
    "social_ctr": 1.8,
    "affiliate_conv": 8.5,
    "interest_conv": 3.2,
    "ftd_conv": 12.0,
}

# SIDEBAR
with st.sidebar:
    st.markdown("## 🎰 PNG Intelligence")
    st.caption("Play'n GO · Business Platform v3.0")
    st.markdown("---")
    cmo_mode = st.toggle("👔 CMO Executive Mode", value=False)
    if cmo_mode:
        st.success("CMO View Active")
    st.markdown("---")

    section = st.radio("Section", [
        "📊 Marketing",
        "💼 Business Intelligence",
        "🌍 Market Intelligence",
        "👥 Player Insights",
    ])

    if section == "📊 Marketing":
        page = st.radio("Page", [
            "👔 CMO Brief",
            "📊 Dashboard",
            "🤖 AI Generator",
            "🕵️ Competitors",
            "💰 Paid Ads",
            "🤝 Affiliates",
            "📉 Gap Analysis",
            "🧠 Insights",
            "🔮 Predictions",
            "💸 Budget Advisor",
            "🎨 Creative Intel",
            "📡 Trend Radar",
            "🗺️ Brand Map",
            "🧪 Message Lab",
            "🚨 Missed Opportunities",
            "🔀 Funnel Simulator",
        ])
    elif section == "💼 Business Intelligence":
        page = st.radio("Page", [
            "🎮 Game Performance",
            "🏦 Casino Distribution",
            "📺 Streaming Intel",
            "🔗 Affiliate Intel",
            "🎁 Bonus Intelligence",
            "📉 Fatigue Detection",
            "🔄 Game Lifecycle",
            "📡 Cross-Channel Attribution",
        ])
    elif section == "🌍 Market Intelligence":
        page = st.radio("Page", [
            "🌍 Geo Markets",
            "⚖️ Regulatory Signals",
            "🔍 Search Demand",
        ])
    elif section == "👥 Player Insights":
        page = st.radio("Page", [
            "👥 Player Behavior",
        ])

    st.markdown("---")
    st.caption("🟢 v3.0 · Mock Data")

def apply_theme():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { background: #0d0f12; }
    .stMetric { background: #111318; border: 1px solid #1e2330; border-radius: 10px; padding: 12px; }
    div[data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; }
    </style>""", unsafe_allow_html=True)

apply_theme()

# ══════════════════════════════════════════════════════════
# MARKETING PAGES
# ══════════════════════════════════════════════════════════

if page == "👔 CMO Brief":
    st.title("Weekly CMO Intelligence Brief")
    st.caption(f"Auto-generated · {datetime.today().strftime('%B %d, %Y')}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Health Score", "74/100", "+6 vs last week")
    col2.metric("Competitive Position", "#2 of 5", "↑ from #3")
    col3.metric("Urgent Actions", "3", "2 new")
    st.markdown("---")
    st.markdown("### 🔴 Risks")
    st.error("🔴 HIGH — Pragmatic Play launched a high-spend Meta campaign targeting our core audience. Estimated 2.4M reach. No PNG counter-campaign active.")
    st.warning("🟡 MEDIUM — Instagram engagement dropped 1.2pp week-over-week. Short-form video frequency 62% below competitor average.")
    st.info("🟢 LOW — LinkedIn post frequency fell to 2/week vs Playtech 5/week.")
    st.markdown("### ✅ Wins")
    st.success("🟢 CasinoGrounds PNG feature — 48K views in 24h. Highest affiliate traffic in 6 weeks.")
    st.success("🟢 Twitch presence leads category. 12% above nearest competitor.")
    st.success("🟢 Instagram engagement 7.4% leads all tracked competitors.")
    st.markdown("### ⚡ Top 3 Actions")
    st.dataframe(pd.DataFrame({
        "Priority": ["1 URGENT","2 HIGH","3 MEDIUM"],
        "Action": ["Launch Meta retargeting. Book of Dead big win creative. Budget: €15K test.","Post 3x Instagram Reels this week. Vertical format. New game teasers.","Publish LinkedIn thought leadership. Topic: AI in slot game design."],
        "Owner": ["Paid Media","Social","Content"],
        "Deadline": ["Wed","Fri","Fri"],
    }), use_container_width=True, hide_index=True)

elif page == "📊 Dashboard":
    st.title("📊 Analytics Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Followers","284K","+3.2%")
    c2.metric("Avg Engagement","4.7%","+0.8pp")
    c3.metric("Total Reach","1.2M","+12%")
    c4.metric("Posts This Month","47","-4 vs target")
    st.markdown("---")
    df_trend = pd.DataFrame({"Date":dates,"Twitter/X":rand_series(6.1),"Instagram":rand_series(7.4),"LinkedIn":rand_series(4.2),"Twitch":rand_series(3.6)})
    fig = px.line(df_trend, x="Date", y=["Twitter/X","Instagram","LinkedIn","Twitch"], title="Engagement Trend (30 days)", color_discrete_sequence=["#00e5a0","#fb7185","#60a5fa","#a78bfa"])
    fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#0a0b0e",font_color="#e8eaf0")
    st.plotly_chart(fig, use_container_width=True)
    col1,col2 = st.columns(2)
    with col1:
        fig2 = px.bar(x=platforms,y=eng_rates,title="Engagement by Platform",color=eng_rates,color_continuous_scale=["#252b38","#00e5a0"])
        fig2.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        fig3 = px.pie(names=platforms,values=followers,title="Follower Split",color_discrete_sequence=["#00e5a0","#60a5fa","#fb7185","#a78bfa","#9146ff","#fef08a"])
        fig3.update_layout(paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig3, use_container_width=True)
    st.markdown("### Top Posts")
    st.dataframe(pd.DataFrame({"Post":["Book of Dead hits 5M spins","Play'n GO named #1 supplier","Solar Temple Megaways drop"],"Platform":["Twitter/X","LinkedIn","Instagram"],"Likes":[4821,2190,8442],"Reach":["94K","61K","128K"],"Eng. Rate":["6.8%","5.1%","9.2%"]}), use_container_width=True, hide_index=True)

elif page == "🤖 AI Generator":
    st.title("🤖 AI Content Generator")
    col1,col2,col3 = st.columns(3)
    platform = col1.selectbox("Platform",["Twitter/X","LinkedIn","Instagram","Snapchat","Twitch"])
    content_type = col2.selectbox("Type",["Game Launch","Brand Story","B2B","Viral Hook","Engagement"])
    topic = col3.text_input("Topic","Book of Dead summer campaign")
    if st.button("Generate Content",type="primary"):
        if platform=="Twitter/X":
            out=f"🔥 {topic} — this is the moment you have been waiting for.\n\nThe game that changed everything is back.\n\nDrop a 🎰 if you are in.\n\n#PlaynGO #iGaming #Slots\n\nENGAGEMENT: 8/10 | HOOK: 9/10 | VIRAL: High"
        elif platform=="LinkedIn":
            out=f"At Play'n GO, every game starts with one question: what will players remember forever?\n\n{topic} is that answer.\n\n18 months of design. 1 billion spins later.\n\n#iGaming #GameDesign #PlaynGO\n\nENGAGEMENT: 7/10 | HOOK: 7/10 | VIRAL: Medium"
        else:
            out=f"✨ {topic} ✨\n\nSome games are played. Some become legends. 🎰\n\nTag someone who needs to see this 👇\n\n#PlaynGO #Slots #iGaming\n\nENGAGEMENT: 9/10 | HOOK: 8/10 | VIRAL: High"
        st.text_area("Generated Content",out,height=200)
        c1,c2,c3=st.columns(3)
        c1.success("Engagement: 8/10")
        c2.info("Hook: 9/10")
        c3.warning("Viral: High")

elif page == "🕵️ Competitors":
    st.title("🕵️ Competitor Intelligence")
    df=pd.DataFrame({"Company":competitors,"Followers":comp_followers,"Eng Rate %":comp_eng,"Posts/Week":comp_freq})
    st.dataframe(df, use_container_width=True, hide_index=True)
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(df,x="Company",y="Eng Rate %",title="Engagement Rates",color="Eng Rate %",color_continuous_scale=["#252b38","#00e5a0"])
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2=px.scatter(df,x="Posts/Week",y="Eng Rate %",size="Followers",color="Company",text="Company",title="Frequency vs Engagement")
        fig2.update_traces(textposition="top center")
        fig2.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("### Platform Presence")
    st.dataframe(pd.DataFrame({"Company":["Pragmatic","NetEnt","Playtech","Merkur","Play'n GO"],"Twitter":["✅","✅","✅","⚠️","✅"],"LinkedIn":["✅","✅","✅","✅","✅"],"Instagram":["✅","⚠️","✅","⚠️","✅"],"Twitch":["⚠️","❌","❌","❌","✅"],"Snapchat":["❌","❌","❌","❌","⚠️"]}), use_container_width=True, hide_index=True)

elif page == "💰 Paid Ads":
    st.title("💰 Paid Ads Intelligence")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Active Competitor Ads","23","+6 this week")
    c2.metric("Top Format","Video 16:9","62% of all")
    c3.metric("Top Platform","Meta","FB + IG")
    c4.metric("Top CTA","Play Now","41% of ads")
    st.markdown("---")
    with st.expander("📢 Pragmatic Play — Meta Video — HIGH SPEND"):
        st.markdown("**Copy:** Gates of Olympus 2 is HERE. Chase the multiplier madness.")
        st.success("CTA: Play Now | Est Reach: 2.4M")
    with st.expander("📢 NetEnt — Meta Carousel — MEDIUM"):
        st.markdown("**Copy:** Starburst XXXtreme. The universe is yours.")
        st.success("CTA: Find Casino | Est Reach: 980K")
    with st.expander("📢 Playtech — LinkedIn — B2B"):
        st.markdown("**Copy:** Power your casino with Age of the Gods. Book a demo.")
        st.info("CTA: Book Demo | Audience: B2B")
    st.success("📹 Short video 10-15s gets 3.8x more engagement than static images")
    st.info("🎯 Big win reveal in first 3 seconds = 2.1x higher CTR")
    st.warning("💡 PNG should test: UGC-style Book of Dead megawin clips on Meta retargeting")

elif page == "🤝 Affiliates":
    st.title("🤝 Affiliate and Influencer Intel")
    st.dataframe(pd.DataFrame({"Affiliate":["CasinoGrounds","Roshtein","AskGamblers","SlotsMillion TikTok","Casino.org"],"Channel":["YouTube","Twitch","Review Site","TikTok/Snapchat","Blog/SEO"],"Monthly Reach":["12.8M","8.4M","6.1M","4.2M","2.1M"],"Top Competitor":["Pragmatic","Multi","All","All","All"],"PNG Coverage":["✅ Good","✅ Active","✅ Listed","❌ Missing","⚠️ Weak"]}), use_container_width=True, hide_index=True)
    fig=px.bar(x=["YouTube Reviews","TikTok Wins","Twitch","Snapchat","Blog SEO"],y=[88,71,58,28,65],title="Affiliate Format Effectiveness",color=[88,71,58,28,65],color_continuous_scale=["#252b38","#00e5a0"])
    fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
    st.plotly_chart(fig, use_container_width=True)
    st.warning("💡 TikTok affiliates underutilized — first mover opportunity for PNG")

elif page == "📉 Gap Analysis":
    st.title("📉 Gap Analysis Engine")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Organic Gaps","4","High priority")
    c2.metric("Paid Gaps","3","Critical")
    c3.metric("Affiliate Gaps","5","Opportunity")
    c4.metric("AI Recs","12","+3 new")
    col1,col2=st.columns(2)
    with col1:
        fig=go.Figure()
        fig.add_bar(name="Play'n GO",x=["Short Video","Snapchat","LinkedIn","Twitch"],y=[38,20,72,97],marker_color="#00e5a0")
        fig.add_bar(name="Competitor Avg",x=["Short Video","Snapchat","LinkedIn","Twitch"],y=[80,15,85,65],marker_color="#ef4444")
        fig.update_layout(barmode="group",title="PNG vs Competitors",plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### AI Recommendations")
        st.error("🎬 Increase short-form video by 3x")
        st.warning("👻 Expand Snapchat NOW — no competitor owns this")
        st.info("🤝 Partner with TikTok affiliates")
        st.success("📋 Add posts Tue/Thu evenings")

elif page == "🧠 Insights":
    st.title("🧠 Smart Insights Panel")
    st.error("🔴 Pragmatic Play viral post — Gates of Olympus 2 hit 340K impressions in 6h")
    st.warning("🟡 New Meta ad — NetEnt Starburst retargeting. Est 50K+ weekly spend")
    st.success("🟢 CasinoGrounds PNG video — 48K views in 24h")
    st.info("💡 MegawaysMonday trending — competitors not using it")
    st.markdown("---")
    col1,col2=st.columns(2)
    with col1:
        st.markdown("### Best Posting Times")
        st.dataframe(pd.DataFrame({"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],"Best Time UTC":["18:00","19:00","18:00","19:00","17:00","14:00","15:00"],"Avg Engagement":[4.2,5.1,4.6,4.9,5.4,3.8,3.2]}), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("### Emerging Trends")
        st.markdown("🔥 AI slot art gets 5x organic reach\n\n🎬 Dev diary drives high engagement\n\n📱 Vertical 9:16 outperforms 16:9 by 3.8x\n\n🎮 Streamer collabs trending")

elif page == "🔮 Predictions":
    st.title("🔮 Predictive Analytics Engine")
    forecast_df=pd.DataFrame({"Platform":platforms,"Current Eng %":eng_rates,"Predicted Next Week":[round(e+random.uniform(-0.3,0.5),2) for e in eng_rates],"Confidence":["High","Medium","High","Low","Medium","Low"],"Trend":["↑","↑","↑","↓","→","↑"]})
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
    st.markdown("---")
    st.markdown("### Pre-Post Engagement Predictor")
    col1,col2,col3=st.columns(3)
    pred_platform=col1.selectbox("Platform",platforms,key="pred_plat")
    pred_format=col2.selectbox("Format",["Reel 9:16","Static Image","Carousel","Story","Text"])
    pred_topic=col3.selectbox("Topic",["Game Launch","Big Win","Brand Story","B2B","Event"])
    pred_time=col1.selectbox("Time",["08:00","12:00","18:00","19:00","21:00"])
    pred_hashtags=col2.slider("Hashtags",0,15,5)
    if st.button("Predict Engagement",type="primary"):
        base={"Twitter/X":6.1,"LinkedIn":4.2,"Instagram":7.4,"Facebook":2.8,"Twitch":3.6,"Snapchat":2.1}
        fmt={"Reel 9:16":1.3,"Static Image":0.9,"Carousel":1.1,"Story":1.0,"Text":0.8}
        top={"Game Launch":1.2,"Big Win":1.4,"Brand Story":1.1,"B2B":0.9,"Event":1.0}
        tim={"08:00":0.9,"12:00":1.0,"18:00":1.2,"19:00":1.3,"21:00":1.1}
        predicted=round(base.get(pred_platform,4.0)*fmt.get(pred_format,1.0)*top.get(pred_topic,1.0)*tim.get(pred_time,1.0)*(1.0+min(pred_hashtags,8)*0.02),2)
        benchmark=base.get(pred_platform,4.0)
        delta=round(predicted-benchmark,2)
        ca,cb,cc=st.columns(3)
        ca.metric("Predicted Engagement",f"{predicted}%",f"{delta:+}% vs avg")
        cb.metric("Platform Avg",f"{benchmark}%")
        cc.metric("Rating","🔥 Excellent" if predicted>benchmark*1.2 else "✅ Good" if predicted>benchmark else "⚠️ Below Avg")

elif page == "💸 Budget Advisor":
    st.title("💸 Budget Allocation Advisor")
    total=st.number_input("Monthly Budget (€)",min_value=1000,max_value=500000,value=50000,step=1000)
    alloc={"Meta (IG+FB)":0.38,"LinkedIn":0.22,"Twitter/X":0.15,"Snapchat Ads":0.12,"Twitch":0.08,"TikTok Test":0.05}
    amounts=[round(total*v) for v in alloc.values()]
    fig=px.pie(names=list(alloc.keys()),values=amounts,title=f"Budget Split — €{total:,}",color_discrete_sequence=["#00e5a0","#60a5fa","#a78bfa","#fef08a","#9146ff","#fb7185"])
    fig.update_layout(paper_bgcolor="#111318",font_color="#e8eaf0")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(pd.DataFrame({"Channel":list(alloc.keys()),"Allocation %":[f"{round(v*100)}%" for v in alloc.values()],"Budget":[f"€{a:,}" for a in amounts]}), use_container_width=True, hide_index=True)

elif page == "🎨 Creative Intel":
    st.title("🎨 Creative Intelligence Engine")
    col1,col2=st.columns(2)
    with col1:
        hooks=["Question Hook","Shock Stat","Big Win Reveal","Behind Scenes","Product Tease","Story Arc"]
        scores=[7.2,8.8,9.4,7.9,6.8,7.1]
        fig=px.bar(x=hooks,y=scores,title="Hook Effectiveness Score",color=scores,color_continuous_scale=["#252b38","#00e5a0"])
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        vf=["Vertical Video","Square Video","Landscape","Static Image","Carousel","GIF"]
        vs=[9.1,7.8,5.2,4.3,5.8,6.1]
        fig2=px.bar(x=vf,y=vs,title="Visual Format Score",color=vs,color_continuous_scale=["#252b38","#fb7185"])
        fig2.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    st.error("🚀 Big Win Reveal hooks score 9.4/10 — use in first 3s of every video")
    st.warning("📱 Vertical video is 1.75x more effective — shift all production to 9:16")
    st.info("🎭 Teaser/mystery tone underused by PNG — competitors use it 3x more")

elif page == "📡 Trend Radar":
    st.title("📡 Trend Radar")
    col1,col2,col3=st.columns(3)
    with col1:
        st.markdown("### Trending Hashtags")
        st.dataframe(pd.DataFrame({"Hashtag":["#MegawaysMonday","#iGamingAI","#SlotDrop","#BigWin","#CasinoDesign"],"Growth":["+340%","+280%","+190%","+140%","+120%"],"PNG Using":["❌","❌","✅","✅","❌"]}), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("### Rising Formats")
        st.dataframe(pd.DataFrame({"Format":["AI Art Process","Dev Diary","UGC Win Clips","Collab Streams","Meme Templates"],"Growth":["+520%","+310%","+280%","+190%","+160%"],"PNG Active":["❌","❌","⚠️","✅","❌"]}), use_container_width=True, hide_index=True)
    with col3:
        st.markdown("### Content Styles")
        st.dataframe(pd.DataFrame({"Style":["Behind-the-reel","Nostalgia retro","Hyper-casual clips","CEO storytelling","Game math explainer"],"Momentum":["🔥 Hot","📈 Rising","🔥 Hot","📈 Rising","📈 Rising"]}), use_container_width=True, hide_index=True)

elif page == "🗺️ Brand Map":
    st.title("🗺️ Brand Positioning Map")
    brand_df=pd.DataFrame({"Brand":["Pragmatic Play","NetEnt","Playtech","Merkur Gaming","Play'n GO"],"B2C Strength":[9.2,7.8,6.5,4.2,8.1],"B2B Strength":[7.8,8.2,9.1,6.8,7.4],"Innovation Score":[7.5,8.8,7.2,5.1,9.2],"Social Presence":[8.8,7.2,7.8,4.5,7.9],"Followers (K)":[412,198,289,87,284]})
    col1,col2=st.columns(2)
    with col1:
        fig=px.scatter(brand_df,x="B2C Strength",y="B2B Strength",size="Followers (K)",color="Brand",text="Brand",title="B2C vs B2B Positioning",size_max=60)
        fig.update_traces(textposition="top center")
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        categories=["B2C","B2B","Innovation","Social","Content","Affiliate"]
        fig3=go.Figure()
        fig3.add_trace(go.Scatterpolar(r=[8.1,7.4,9.2,7.9,8.3,6.8]+[8.1],theta=categories+[categories[0]],fill="toself",name="Play'n GO",line_color="#00e5a0"))
        fig3.add_trace(go.Scatterpolar(r=[9.2,7.8,7.5,8.8,7.9,9.1]+[9.2],theta=categories+[categories[0]],fill="toself",name="Pragmatic",line_color="#ef4444",opacity=0.6))
        fig3.update_layout(polar=dict(bgcolor="#111318"),paper_bgcolor="#111318",font_color="#e8eaf0",title="PNG vs Pragmatic Play")
        st.plotly_chart(fig3, use_container_width=True)

elif page == "🧪 Message Lab":
    st.title("🧪 Message Testing Lab")
    original=st.text_area("Your message idea","Book of Dead just crossed 1 billion spins. The legend lives on.",height=80)
    if st.button("Generate Variations",type="primary"):
        variations=[
            {"style":"Bold/Stat-led","copy":f"1,000,000,000 spins. One game. Book of Dead is not just a slot — it is a cultural moment. 🎰 #PlaynGO","score":8.9,"verdict":"🏆 Predicted Winner"},
            {"style":"Story-driven","copy":f"It started with a single spin. Then a million. Then a billion. Book of Dead — why players never stopped. 🧵","score":7.8,"verdict":"✅ Strong"},
            {"style":"Question Hook","copy":f"What does 1 billion spins sound like? That is Book of Dead. What was YOUR most memorable spin? 👇","score":7.4,"verdict":"✅ Good engagement"},
            {"style":"Minimal/Bold","copy":f"1 billion spins.\n\nBook of Dead.\n\nEnough said. 🎰","score":8.2,"verdict":"✅ High shareability"},
        ]
        for i,v in enumerate(variations):
            with st.expander(f"Variation {i+1}: {v['style']} — Score {v['score']}/10 {v['verdict']}"):
                st.markdown(f"**Copy:**\n\n{v['copy']}")
                col_a,col_b=st.columns(2)
                col_a.metric("Predicted Score",f"{v['score']}/10")
                col_b.metric("Verdict",v["verdict"])

elif page == "🚨 Missed Opportunities":
    st.title("🚨 Missed Opportunities Engine")
    st.dataframe(pd.DataFrame({"Opportunity":["#MegawaysMonday series","AI art content","G2E recap thread","Snapchat behind-the-scenes","UGC player big win reposts"],"Who Used It":["Pragmatic, NetEnt","NetEnt","Playtech, NetEnt","None — pure gap","Pragmatic"],"Est. Reach Missed":["480K","310K","190K","0 — gap","540K"],"PNG Acted":["❌","❌","❌","❌","⚠️"],"Priority":["🔴 High","🔴 High","🟡 Medium","🟢 Low","🔴 High"]}), use_container_width=True, hide_index=True)
    col1,col2,col3=st.columns(3)
    col1.metric("Est. Reach Missed","1.74M","organic")
    col2.metric("Missed Affiliate Touches","~38K","UGC gap")
    col3.metric("Brand Mention Ratio","1:3.2","PNG vs Pragmatic")
    st.error("🔴 Start #MegawaysMonday this week. Zero cost. Est 80K+ reach in 4 weeks.")
    st.error("🔴 Repost top player wins weekly. Pragmatic gets 540K reach/month from UGC.")

elif page == "🔀 Funnel Simulator":
    st.title("🔀 Funnel Simulator")
    col1,col2,col3=st.columns(3)
    reach=col1.number_input("Social Reach",value=500000,step=10000)
    ctr=col2.slider("Social CTR %",0.1,5.0,1.8)
    aff_conv=col3.slider("Affiliate Conv %",1.0,20.0,8.5)
    col4,col5=st.columns(2)
    interest_conv=col4.slider("Interest-to-Reg %",0.5,10.0,3.2)
    reg_conv=col5.slider("Reg-to-FTD %",1.0,20.0,12.0)
    sc=int(reach*(ctr/100)); ai=int(sc*(aff_conv/100)); reg=int(ai*(interest_conv/100)); ftd=int(reg*(reg_conv/100))
    f1,f2,f3,f4,f5=st.columns(5)
    f1.metric("Reach",f"{reach:,}"); f2.metric("Clicks",f"{sc:,}"); f3.metric("Interest",f"{ai:,}"); f4.metric("Registrations",f"{reg:,}"); f5.metric("FTD Proxy",f"{ftd:,}")
    fig=go.Figure(go.Funnel(y=["Reach","Clicks","Interest","Registrations","FTD"],x=[reach,sc,ai,reg,ftd],textinfo="value+percent initial",marker={"color":["#00e5a0","#60a5fa","#a78bfa","#f59e0b","#ef4444"]}))
    fig.update_layout(paper_bgcolor="#111318",font_color="#e8eaf0",title="Campaign Funnel")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════
# BUSINESS INTELLIGENCE PAGES
# ══════════════════════════════════════════════════════════

elif page == "🎮 Game Performance":
    st.title("🎮 Game Performance & Revenue Intelligence")
    st.caption("Cross-signal scoring: Social + Search + Affiliate + Distribution")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Games Tracked","10","PNG portfolio")
    c2.metric("Top Revenue Proxy","Book of Dead","Score: 94/100")
    c3.metric("Fastest Rising","Moon Princess","+18% search")
    c4.metric("Urgent Review","Elephant King","Score: 43 — Declining")
    st.markdown("---")
    st.markdown("### Full Game Scorecard")
    st.dataframe(games_data, use_container_width=True, hide_index=True)
    st.markdown("---")
    col1,col2=st.columns(2)
    with col1:
        fig=px.scatter(games_data,x="Search Demand Index",y="Casino Distribution",size="Revenue Proxy Score",color="Lifecycle Stage",text="Game",title="High Demand vs Low Distribution = Opportunity",size_max=40,color_discrete_sequence=["#00e5a0","#60a5fa","#f59e0b","#ef4444"])
        fig.update_traces(textposition="top center")
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        fig.add_hline(y=70,line_dash="dash",line_color="#ef4444",annotation_text="Distribution threshold")
        fig.add_vline(x=70,line_dash="dash",line_color="#ef4444",annotation_text="Demand threshold")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🔴 Top-right quadrant = high demand, good distribution. Bottom-right = high demand but UNDER-distributed = push harder here.")
    with col2:
        fig2=px.bar(games_data.sort_values("Revenue Proxy Score",ascending=True),x="Revenue Proxy Score",y="Game",orientation="h",title="Revenue Proxy Ranking",color="Revenue Proxy Score",color_continuous_scale=["#ef4444","#f59e0b","#00e5a0"])
        fig2.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("### Key Opportunities")
    st.error("🚀 Cat Wilde & Moon Princess: High social growth, lower distribution — push to more operators NOW")
    st.warning("⚠️ Solar Temple & Banana Rock: New launches with low search demand — need marketing push")
    st.success("✅ Book of Dead & Legacy of Dead: Mature but stable — maintain featuring deals")

elif page == "🏦 Casino Distribution":
    st.title("🏦 Casino Operator Distribution Intelligence")
    st.caption("Where Play'n GO appears vs competitors — and where we are missing")
    c1,c2,c3,c4=st.columns(4)
    png_featured=casino_data["Play'n GO Featured"].sum()
    c1.metric("Casinos Featuring PNG",f"{png_featured}/10","tracked operators")
    c2.metric("Homepage Placements",str(casino_data[casino_data["Homepage Placement"]=="Yes"].shape[0]),"of 10 casinos")
    c3.metric("Avg PNG Games Listed","32","vs comp avg 51")
    c4.metric("Distribution Gap","37%","below competitor avg")
    st.markdown("---")
    st.markdown("### Operator Coverage Map")
    display=casino_data.copy()
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.markdown("---")
    col1,col2=st.columns(2)
    with col1:
        fig=go.Figure()
        fig.add_bar(name="PNG Games",x=casino_data["Casino"],y=casino_data["PNG Game Count"],marker_color="#00e5a0")
        fig.add_bar(name="Comp Avg",x=casino_data["Casino"],y=casino_data["Comp Avg Game Count"],marker_color="#ef4444")
        fig.update_layout(barmode="group",title="PNG vs Competitor Games Listed per Casino",plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### Distribution Gaps")
        gaps=casino_data[casino_data["Play'n GO Featured"]==False]
        if len(gaps)>0:
            st.error(f"🔴 NOT featured at: {', '.join(gaps['Casino'].tolist())}")
        no_homepage=casino_data[casino_data["Homepage Placement"]=="No"]
        st.warning(f"⚠️ No homepage placement at: {', '.join(no_homepage['Casino'].tolist())}")
        st.info("💡 Average PNG games per casino is 37% below competitor average. Priority: increase game count at Bet365, LeoVegas, Casumo.")
        st.error("🚀 Betway and Unibet: PNG completely absent. Pragmatic Play fully featured. Immediate business development opportunity.")

elif page == "📺 Streaming Intel":
    st.title("📺 Streaming & YouTube Intelligence")
    st.caption("Creator-driven visibility for Play'n GO games")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Creators Tracked","10","Twitch + YouTube")
    c2.metric("Total Monthly Views","41.3M","across all creators")
    c3.metric("High PNG Coverage","3 creators","Roshtein, CasinoGrounds, Casinodaddy")
    c4.metric("Low/No Coverage","4 creators","Opportunity")
    st.markdown("---")
    st.dataframe(streaming_data, use_container_width=True, hide_index=True)
    st.markdown("---")
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(streaming_data.sort_values("Monthly Views"),x="Monthly Views",y="Creator",orientation="h",color="PNG Coverage",title="Creator Reach vs PNG Coverage",color_discrete_map={"High":"#00e5a0","Medium":"#f59e0b","Low":"#ef4444"})
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### Recommendations")
        low=streaming_data[streaming_data["PNG Coverage"]=="Low"]
        for _,row in low.iterrows():
            st.warning(f"⚠️ **{row['Creator']}** ({row['Platform']}) — {row['Monthly Views']:,} monthly views — LOW PNG coverage. Prefers: {row['Competitor Preference']}. Target for seeding.")
        st.error("🚀 ClassyBeef (4.8M views/mo) has low PNG coverage and prefers Pragmatic. Priority outreach + game seeding.")

elif page == "🔗 Affiliate Intel":
    st.title("🔗 Affiliate Intelligence Platform")
    st.caption("How Play'n GO appears across major affiliate and review sites")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Sites Tracked","10","affiliate platforms")
    c2.metric("Avg PNG Visibility","69.8/100","vs Pragmatic 83.4")
    c3.metric("Avg PNG Games Listed","167","vs comp avg 206")
    c4.metric("Visibility Gap","-16%","vs Pragmatic Play")
    st.markdown("---")
    st.dataframe(affiliate_data, use_container_width=True, hide_index=True)
    col1,col2=st.columns(2)
    with col1:
        fig=go.Figure()
        fig.add_bar(name="PNG Visibility",x=affiliate_data["Affiliate Site"],y=affiliate_data["PNG Visibility Score"],marker_color="#00e5a0")
        fig.add_bar(name="Pragmatic Score",x=affiliate_data["Affiliate Site"],y=affiliate_data["Pragmatic Score"],marker_color="#ef4444")
        fig.update_layout(barmode="group",title="PNG vs Pragmatic Affiliate Visibility",plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2=go.Figure()
        fig2.add_bar(name="PNG Games Listed",x=affiliate_data["Affiliate Site"],y=affiliate_data["PNG Games Listed"],marker_color="#00e5a0")
        fig2.add_bar(name="Comp Avg Listed",x=affiliate_data["Affiliate Site"],y=affiliate_data["Comp Avg Listed"],marker_color="#ef4444")
        fig2.update_layout(barmode="group",title="Games Listed: PNG vs Competitor Avg",plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig2, use_container_width=True)
    st.warning("💡 SlotCatalog has highest PNG game count (210) but visibility gap vs Pragmatic remains 3 points. Optimise listing quality.")
    st.error("🔴 AskGamblers and OLBG: PNG visibility well below Pragmatic. Priority for SEO/affiliate partnership improvement.")

elif page == "🎁 Bonus Intelligence":
    st.title("🎁 Bonus & Promotion Intelligence")
    st.caption("How Play'n GO games appear in casino promotions vs competitors")
    c1,c2,c3,c4=st.columns(4)
    png_in_promos=bonus_intel[bonus_intel["PNG Featured"].str.contains("Yes")].shape[0]
    c1.metric("Casinos Running Promos","8","tracked")
    c2.metric("PNG Featured in Promos",f"{png_in_promos}/8","operators")
    c3.metric("Most Promoted PNG Game","Book of Dead","free spins focus")
    c4.metric("Competitor Promo Share","Pragmatic dominates","5 of 8 operators")
    st.markdown("---")
    st.dataframe(bonus_intel, use_container_width=True, hide_index=True)
    st.markdown("---")
    st.markdown("### Promo Gap Analysis")
    st.error("🔴 Unibet and William Hill: PNG has zero presence in bonus promos. Pragmatic Play featured in both. Immediate commercial opportunity.")
    st.error("🔴 Betway: No PNG promo presence. High player volume operator. Negotiate a Book of Dead free spins package.")
    st.warning("⚠️ Bonus Buy promos: Pragmatic dominates this fast-growing promo type. PNG needs a bonus buy game to compete in this segment.")
    st.success("✅ Book of Dead free spins continue to drive promo placements at LeoVegas and Rizk. Leverage for new game launches.")

elif page == "📉 Fatigue Detection":
    st.title("📉 Customer Fatigue Detection")
    st.caption("Detecting declining engagement patterns across PNG game portfolio")
    healthy=fatigue_data[fatigue_data["Status"]=="✅ Healthy"].shape[0]
    watch=fatigue_data[fatigue_data["Status"]=="⚠️ Watch"].shape[0]
    fatigued=fatigue_data[fatigue_data["Status"]=="🔴 Fatigued"].shape[0]
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Games Monitored","10")
    c2.metric("Healthy",str(healthy),"stable engagement")
    c3.metric("Watch",str(watch),"declining trend")
    c4.metric("Fatigued",str(fatigued),"action required")
    st.markdown("---")
    st.dataframe(fatigue_data, use_container_width=True, hide_index=True)
    col1,col2=st.columns(2)
    with col1:
        fig=go.Figure()
        fig.add_bar(name="Peak Engagement",x=fatigue_data["Game"],y=fatigue_data["Peak Engagement"],marker_color="#00e5a0")
        fig.add_bar(name="Current Engagement",x=fatigue_data["Game"],y=fatigue_data["Current Engagement"],marker_color="#ef4444")
        fig.update_layout(barmode="group",title="Peak vs Current Engagement",plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2=px.bar(fatigue_data,x="Game",y="Decline %",title="Engagement Decline %",color="Decline %",color_continuous_scale=["#ef4444","#f59e0b","#00e5a0"])
        fig2.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    st.error("🔴 7 games showing significant fatigue (>40% decline). Recommend: remove from featured placement, replace with new launches.")
    st.warning("⚠️ Fire Joker declining 19% — consider a 'Fire Joker: Extreme' sequel or promotional push to extend lifecycle.")

elif page == "🔄 Game Lifecycle":
    st.title("🔄 Game Lifecycle Classification")
    st.caption("Where each PNG game sits in its commercial lifecycle")
    for stage,color,desc in [("Launch","#00e5a0","New games needing marketing push"),("Growth","#60a5fa","Rising games to accelerate"),("Mature","#f59e0b","Established games to maintain"),("Decline","#ef4444","Aging games to phase out")]:
        games_in_stage=games_data[games_data["Lifecycle Stage"]==stage]["Game"].tolist()
        if games_in_stage:
            st.markdown(f"### {stage} Stage")
            st.caption(desc)
            cols=st.columns(len(games_in_stage))
            for i,game in enumerate(games_in_stage):
                row=games_data[games_data["Game"]==game].iloc[0]
                cols[i].metric(game,f"Rev: {row['Revenue Proxy Score']}",row["Trend"])
            st.markdown("---")
    st.markdown("### Strategic Actions by Stage")
    st.dataframe(pd.DataFrame({
        "Stage":["Launch","Growth","Mature","Decline"],
        "Games":["Solar Temple, Banana Rock","Fire Joker, Moon Princess, Cat Wilde","Book of Dead, Rise of Olympus, Legacy of Dead, Reactoonz","Elephant King"],
        "Action":["Aggressive social push, streamer seeding, affiliate outreach","Increase featuring deals, bonus promos, paid amplification","Maintain operator deals, use as hero game in promos","Phase out promotions, reduce marketing spend, plan replacement"],
    }), use_container_width=True, hide_index=True)

elif page == "📡 Cross-Channel Attribution":
    st.title("📡 Cross-Channel Attribution Model")
    st.caption("Simulated model: Social → Affiliate → Interest → Conversion")
    col1,col2=st.columns(2)
    with col1:
        st.markdown("### Configure Model")
        reach=st.number_input("Social Reach",value=500000,step=10000,key="attr_reach")
        social_ctr=st.slider("Social CTR %",0.1,5.0,1.8,key="attr_ctr")
        aff_pick=st.slider("Affiliate Pickup %",1.0,30.0,8.5,key="attr_aff")
        reg_rate=st.slider("Interest-to-Registration %",0.5,10.0,3.2,key="attr_reg")
        ftd_rate=st.slider("Registration-to-FTD %",1.0,20.0,12.0,key="attr_ftd")
        channel_split=st.multiselect("Active Channels",["Instagram","Twitter/X","LinkedIn","Twitch","Snapchat"],default=["Instagram","Twitter/X","Twitch"])
    sc=int(reach*(social_ctr/100)); ai=int(sc*(aff_pick/100)); reg=int(ai*(reg_rate/100)); ftd=int(reg*(ftd_rate/100))
    with col2:
        st.markdown("### Attribution Output")
        m1,m2=st.columns(2)
        m1.metric("Social Reach",f"{reach:,}")
        m2.metric("Social Clicks",f"{sc:,}",f"{social_ctr}% CTR")
        m1.metric("Affiliate Interest",f"{ai:,}",f"{aff_pick}% pickup")
        m2.metric("Registrations",f"{reg:,}",f"{reg_rate}%")
        m1.metric("FTD Proxy",f"{ftd:,}",f"{ftd_rate}%")
        overall=round((ftd/reach)*100,4) if reach>0 else 0
        m2.metric("End-to-End Conv.",f"{overall}%")
    fig=go.Figure(go.Funnel(y=["Social Reach","Clicks","Affiliate Interest","Registrations","FTD"],x=[reach,sc,ai,reg,ftd],textinfo="value+percent initial",marker={"color":["#00e5a0","#60a5fa","#a78bfa","#f59e0b","#ef4444"]}))
    fig.update_layout(paper_bgcolor="#111318",font_color="#e8eaf0",title="Full Attribution Funnel")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("### Channel Contribution (Simulated)")
    ch_data={"Channel":channel_split,"Contribution %":[round(100/len(channel_split)+random.uniform(-5,5),1) for _ in channel_split],"Avg Eng":[round(random.uniform(3,8),1) for _ in channel_split]}
    st.dataframe(pd.DataFrame(ch_data), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# MARKET INTELLIGENCE PAGES
# ══════════════════════════════════════════════════════════

elif page == "🌍 Geo Markets":
    st.title("🌍 Geographic Market Intelligence")
    st.caption("Regional performance and growth opportunities for Play'n GO")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Markets Tracked","10","key regions")
    c2.metric("Highest PNG Share","Finland","28% market share")
    c3.metric("Fastest Growing","Portugal","+41% YoY")
    c4.metric("Biggest Opportunity","Germany","28% growth + low PNG share")
    st.markdown("---")
    st.dataframe(geo_data, use_container_width=True, hide_index=True)
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(geo_data,x="Market",y="PNG Market Share",title="PNG Market Share by Region (%)",color="PNG Market Share",color_continuous_scale=["#ef4444","#f59e0b","#00e5a0"])
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2=px.scatter(geo_data,x="Market Size (M players)",y="PNG Market Share",size="Opportunity Score",color="Market",text="Market",title="Market Size vs PNG Share (bubble = opportunity)",size_max=40)
        fig2.update_traces(textposition="top center")
        fig2.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("### Strategic Market Priorities")
    st.error("🔴 Germany: Largest EU market, 28% growth rate, only 12% PNG share. Pragmatic dominant. Priority market for commercial and marketing push.")
    st.error("🔴 Portugal: +41% YoY growth, new regulation opening, PNG at 11% share. First-mover opportunity.")
    st.warning("⚠️ Netherlands: New regulated market, 35% growth, PNG at 16%. Increase operator deals urgently.")
    st.success("✅ Finland + Norway + Denmark: PNG strong here (22-28% share). Defend and grow.")

elif page == "⚖️ Regulatory Signals":
    st.title("⚖️ Regulatory Intelligence")
    st.caption("Market openings, policy changes, and strategic expansion signals")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Markets Monitored","10","global")
    c2.metric("High Priority","2","Brazil + USA")
    c3.metric("PNG Active","4","of 10 markets")
    c4.metric("Immediate Gaps","6","no PNG presence")
    st.markdown("---")
    st.dataframe(regulatory_data, use_container_width=True, hide_index=True)
    st.markdown("---")
    st.error("🔴 BRAZIL: Market opening 2025. Estimated $2.1B market. PNG has zero presence. Immediate action: regulatory preparation + operator partnerships.")
    st.error("🔴 USA (Michigan): Live and expanding. $890M market. PNG limited presence. Scale urgently — Pragmatic already established.")
    st.warning("🟡 INDIA: $1.4B estimated market. Long regulatory uncertainty but worth watching. Begin research phase.")
    st.warning("🟡 UAE: Exploratory phase. High-value market. Begin partner exploration.")
    st.success("🟢 Colombia + Mexico + Romania: PNG active. Continue growing existing position.")

elif page == "🔍 Search Demand":
    st.title("🔍 Search Demand Intelligence")
    st.caption("Keyword trends revealing what players are searching for — and where PNG can win")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Keywords Tracked","10","iGaming focus")
    c2.metric("Biggest Trend","Pragmatic Play terms","+67% search growth")
    c3.metric("PNG Opportunities","3","high/medium opportunity")
    c4.metric("Critical Gap","No wagering + Bonus buy","PNG underrepresented")
    st.markdown("---")
    st.dataframe(search_trends, use_container_width=True, hide_index=True)
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(search_trends,x="Keyword",y="Search Volume",title="Keyword Search Volume",color="Opportunity",color_discrete_map={"High":"#00e5a0","Medium":"#f59e0b","Low":"#6b7280","Monitor":"#ef4444"})
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### Keyword Opportunity Actions")
        high_opp=search_trends[search_trends["Opportunity"]=="High"]
        for _,row in high_opp.iterrows():
            st.error(f"🚀 **{row['Keyword']}** — {row['Search Volume']:,} searches, {row['Trend']} growth. PNG status: {row['PNG Relevance']}. Action required.")
        med_opp=search_trends[search_trends["Opportunity"]=="Medium"]
        for _,row in med_opp.iterrows():
            st.warning(f"⚠️ **{row['Keyword']}** — {row['Search Volume']:,} searches, {row['Trend']} growth. Partial PNG presence — improve content targeting.")

# ══════════════════════════════════════════════════════════
# PLAYER INSIGHTS PAGES
# ══════════════════════════════════════════════════════════

elif page == "👥 Player Behavior":
    st.title("👥 Player Behavior Insights")
    st.caption("Simulated from reviews, Reddit, YouTube comments, and community data")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Themes Tracked","10","player preference signals")
    c2.metric("Top Player Want","Bonus Buy Feature","sentiment 8.9/10")
    c3.metric("PNG Delivering Well","Free Spins + Multipliers","player satisfaction high")
    c4.metric("PNG Gap","Bonus Buy + RTP Transparency","vs competitor offering")
    st.markdown("---")
    st.dataframe(player_insights, use_container_width=True, hide_index=True)
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(player_insights.sort_values("Sentiment Score"),x="Sentiment Score",y="Theme",orientation="h",title="Player Sentiment by Feature",color="Sentiment Score",color_continuous_scale=["#ef4444","#f59e0b","#00e5a0"])
        fig.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0",showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2=px.scatter(player_insights,x="Volume (mentions)",y="Sentiment Score",color="PNG Delivers",text="Theme",title="Volume vs Sentiment (where to act)",color_discrete_map={"✅ Strong":"#00e5a0","⚠️ Partial":"#f59e0b"},size_max=20)
        fig2.update_traces(textposition="top center")
        fig2.update_layout(plot_bgcolor="#111318",paper_bgcolor="#111318",font_color="#e8eaf0")
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("### Player Intelligence Actions")
    st.error("🔴 BONUS BUY: Highest player demand (8.9/10, 12,400 mentions). Pragmatic Play dominates this. PNG needs a Bonus Buy feature in next major game release.")
    st.warning("⚠️ RTP TRANSPARENCY: Growing player demand (7.1/10). NetEnt leads here with visible RTP. PNG should make RTP information more prominent in all game descriptions.")
    st.success("✅ FREE SPINS + MULTIPLIERS: PNG delivers strongly. Continue and amplify in marketing messaging — players love it and PNG does it well.")
    st.success("✅ MOBILE EXPERIENCE: High sentiment (8.5/10) and PNG delivers. Use this as a differentiator in B2B operator pitches.")

