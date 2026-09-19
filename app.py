import streamlit as st
import random
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Lemonade Empire",
    page_icon="🍋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# VISUAL SYSTEM
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --lemon: #F6D84A;
        --lemon-dark: #D8B92E;
        --leaf: #2F6B3B;
        --leaf-light: #EAF4E8;
        --sky: #DDF2FA;
        --cream: #FFFDF5;
        --ink: #263328;
        --muted: #718071;
        --orange: #F28C28;
        --danger: #B84A39;
        --border: #E7E2CA;
        --shadow: 0 8px 24px rgba(48, 61, 41, 0.08);
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 0%, rgba(246,216,74,.22), transparent 22%),
            linear-gradient(180deg, #F7FBF7 0%, #FFFDF7 38%, #FFFDF7 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: var(--ink) !important;
        letter-spacing: -0.02em;
    }

    .hero {
        background: linear-gradient(135deg, #FFF4A9 0%, #FDEB6A 48%, #DDEFAE 100%);
        border: 1px solid rgba(90, 90, 40, .12);
        border-radius: 28px;
        padding: 28px 30px 22px 30px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        margin-bottom: 18px;
    }

    .hero::before,
    .hero::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        background: rgba(255,255,255,.33);
    }
    .hero::before { width: 150px; height: 150px; right: 6%; top: -70px; }
    .hero::after { width: 80px; height: 80px; right: 16%; top: 18px; }

    .eyebrow {
        font-size: .82rem;
        font-weight: 800;
        color: var(--leaf);
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .hero-title {
        font-size: clamp(2.3rem, 5vw, 4rem);
        line-height: .95;
        font-weight: 900;
        margin: 0;
        color: #27412C;
    }

    .hero-subtitle {
        margin: 12px 0 0;
        max-width: 720px;
        font-size: 1.05rem;
        color: #45614B;
    }

    .hud {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 10px;
        margin: 14px 0 20px;
    }

    .hud-card {
        background: rgba(255,255,255,.82);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 13px 14px;
        min-height: 82px;
        box-shadow: 0 4px 12px rgba(40,50,40,.04);
    }

    .hud-icon { font-size: 1.25rem; }
    .hud-label { font-size: .73rem; color: var(--muted); font-weight: 700; margin-top: 3px; }
    .hud-value { font-size: 1.28rem; font-weight: 850; margin-top: 2px; }

    .section-kicker {
        display: inline-block;
        font-size: .76rem;
        font-weight: 900;
        letter-spacing: .09em;
        text-transform: uppercase;
        color: var(--leaf);
        margin-bottom: 2px;
    }

    .card {
        background: rgba(255,255,255,.93);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 20px;
        box-shadow: var(--shadow);
        margin-bottom: 16px;
    }

    .town-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FBF2 100%);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 22px;
        min-height: 205px;
        box-shadow: var(--shadow);
        text-align: center;
    }

    .town-icon { font-size: 3.2rem; line-height: 1; margin-bottom: 8px; }
    .town-title { font-size: 1.18rem; font-weight: 850; }
    .town-copy { color: var(--muted); font-size: .9rem; min-height: 42px; margin-top: 5px; }

    .price-panel {
        background: linear-gradient(145deg, #FFFFFF 0%, #FFF9D5 100%);
        border: 1px solid #E8DB8C;
        border-radius: 24px;
        padding: 24px;
        box-shadow: var(--shadow);
    }

    .price-label { color: var(--muted); font-size: .84rem; font-weight: 700; }
    .price-number { font-size: 3.2rem; font-weight: 900; line-height: 1; margin: 3px 0 8px; }
    .price-copy { color: #556453; font-size: .9rem; }

    .last-day {
        background: linear-gradient(135deg, #EEF8EF 0%, #FBFFF4 100%);
        border: 1px solid #D8E8D4;
        border-radius: 20px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }

    .last-day-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 12px;
    }

    .last-day-stat {
        background: rgba(255,255,255,.75);
        border-radius: 14px;
        padding: 11px 12px;
    }
    .last-day-stat .label { font-size: .72rem; color: var(--muted); font-weight: 750; }
    .last-day-stat .value { font-size: 1.1rem; font-weight: 850; margin-top: 3px; }

    .stand-scene {
        background: linear-gradient(180deg, #DDF4FF 0%, #DDF4FF 55%, #B9D997 55%, #A4CA7D 100%);
        border-radius: 24px;
        min-height: 260px;
        position: relative;
        overflow: hidden;
        border: 1px solid #D2DCC7;
        margin-bottom: 16px;
    }

    .sun {
        position: absolute;
        right: 28px;
        top: 22px;
        font-size: 3rem;
        animation: floaty 3.5s ease-in-out infinite;
    }

    .cloud {
        position: absolute;
        font-size: 2.2rem;
        opacity: .8;
        animation: drift 16s linear infinite;
    }
    .cloud.one { left: 18px; top: 28px; }
    .cloud.two { left: 48%; top: 52px; animation-duration: 21s; }

    .stand {
        position: absolute;
        left: 50%;
        bottom: 20px;
        transform: translateX(-50%);
        text-align: center;
        font-size: 5rem;
        filter: drop-shadow(0 9px 7px rgba(70,90,50,.17));
    }

    .stand-label {
        position: absolute;
        left: 50%;
        bottom: 23px;
        transform: translateX(-50%);
        background: #FFF7BC;
        border: 1px solid #D4BE53;
        color: #5A4D11;
        font-weight: 900;
        padding: 5px 10px;
        border-radius: 8px;
        white-space: nowrap;
        font-size: .85rem;
    }

    .empire-bar {
        margin-top: 10px;
        height: 11px;
        background: #E8EAD9;
        border-radius: 999px;
        overflow: hidden;
    }
    .empire-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--lemon-dark), #79AE54);
        border-radius: 999px;
    }

    .event {
        border-radius: 16px;
        padding: 13px 15px;
        margin: 8px 0;
        border: 1px solid var(--border);
        background: #FFF;
    }
    .event.good { background: #EEF8EF; border-color: #D8E8D4; }
    .event.bad { background: #FFF1EE; border-color: #F1CEC7; }
    .event.warning { background: #FFF7DE; border-color: #EDD99A; }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 10px;
        border-radius: 999px;
        background: #EDF3E7;
        color: var(--leaf);
        font-size: .74rem;
        font-weight: 800;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .upgrade-card {
        background: rgba(255,255,255,.95);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 20px;
        box-shadow: var(--shadow);
        min-height: 205px;
    }
    .upgrade-icon { font-size: 2.4rem; }
    .upgrade-name { font-size: 1.1rem; font-weight: 850; margin-top: 7px; }
    .upgrade-copy { font-size: .86rem; color: var(--muted); min-height: 45px; }

    .intro-rules {
        background: rgba(255,255,255,.88);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 19px 22px;
        box-shadow: var(--shadow);
    }

    .game-over {
        background: linear-gradient(145deg, #FFF4F0, #FFFDF8);
        border: 1px solid #F0CEC6;
        border-radius: 26px;
        padding: 34px;
        text-align: center;
        box-shadow: var(--shadow);
    }

    @keyframes floaty { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    @keyframes drift { 0% { transform: translateX(0); } 50% { transform: translateX(24px); } 100% { transform: translateX(0); } }
    @keyframes pop { 0% { transform: scale(.94); opacity: .3; } 100% { transform: scale(1); opacity: 1; } }
    .animate-pop { animation: pop .35s ease-out; }

    @media (max-width: 900px) {
        .hud { grid-template-columns: repeat(3, 1fr); }
        .last-day-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
        .hud { grid-template-columns: repeat(2, 1fr); }
        .hero { padding: 22px; }
        .hero-title { font-size: 2.45rem; }
        .last-day-grid { grid-template-columns: 1fr 1fr; }
    }

    /* Streamlit controls */
    div.stButton > button {
        border-radius: 13px;
        min-height: 45px;
        font-weight: 800;
        border: 1px solid #DDDCCF;
        transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 16px rgba(40,50,40,.09);
        border-color: #C8C6B4;
    }
    div.stButton > button[kind="primary"] {
        background: var(--leaf);
        color: white;
        border-color: var(--leaf);
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.8);
        border: 1px solid var(--border);
        padding: 12px 14px;
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def ensure_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default


ensure_state("game_started", False)
ensure_state("game_over", False)
ensure_state("player_name", "")
ensure_state("current_screen", "main_menu")


def init_game_state(name):
    st.session_state.player_name = name
    st.session_state.cash = 100.0
    st.session_state.maxcash = 100.0
    st.session_state.maxcashsav = 100.0

    st.session_state.marketingEffect = 0
    st.session_state.account = 0.00
    st.session_state.maxAccount = 0.00
    st.session_state.lemons = 0
    st.session_state.sugar = 0.0
    st.session_state.cups = 0

    st.session_state.day = 1
    st.session_state.locations = 1

    st.session_state.yestLemPrice = 0.65
    st.session_state.yestSugPrice = 1.25
    st.session_state.yestCupPrice = 0.23

    # Remember the last selling price so it persists between days.
    st.session_state.sale_price = 0.50
    st.session_state.oldDemand = 4
    st.session_state.rotFact = 1
    st.session_state.rent = 10
    st.session_state.yestCash = 100.0

    st.session_state.loan = 0
    st.session_state.loanAmount = 0.00
    st.session_state.savingsInterest = 0.02
    st.session_state.loansInterest = 0.03
    st.session_state.loanDays = 0

    st.session_state.coolers = 0
    st.session_state.canopies = 0
    st.session_state.wages = 0
    st.session_state.searchEngineCampaignDays = 0
    st.session_state.socialMediaCampaignDays = 0
    st.session_state.billboardCampaignDays = 0
    st.session_state.radioCampaignDays = 0

    # New presentation/history state.
    st.session_state.sales_history = []
    st.session_state.market_history = []
    st.session_state.summary = None
    st.session_state.current_screen = "main_menu"
    st.session_state.game_started = True
    st.session_state.game_over = False

    update_prices()


def update_prices():
    """Generate today's market prices. Prices are never used as a forecast."""
    lem_change = random.uniform(-0.08, 0.11)
    sug_change = random.uniform(-0.07, 0.10)
    cup_change = random.uniform(-0.03, 0.04)

    st.session_state.lemPrice = max(0.05, round(st.session_state.yestLemPrice + lem_change, 2))
    st.session_state.sugPrice = max(0.05, round(st.session_state.yestSugPrice + sug_change, 2))
    st.session_state.cupPrice = max(0.05, round(st.session_state.yestCupPrice + cup_change, 2))

    st.session_state.yestLemPrice = st.session_state.lemPrice
    st.session_state.yestSugPrice = st.session_state.sugPrice
    st.session_state.yestCupPrice = st.session_state.cupPrice

    st.session_state.coolerPrice = 35 + random.randint(-10, 10)
    st.session_state.canopyPrice = 50 + random.randint(-15, 15)
    st.session_state.standPrice = 115 + random.randint(-30, 30)

    st.session_state.radioPrice = 235 + random.randint(-15, 75)
    st.session_state.searchEnginePrice = 30 + random.randint(-5, 15)
    st.session_state.socialMediaPrice = 55 + random.randint(-10, 25)
    st.session_state.billboardPrice = 650 + random.randint(-25, 85)

    # Keep a bounded market history for the price chart.
    st.session_state.market_history.append(
        {
            "day": st.session_state.day,
            "lemons": st.session_state.lemPrice,
            "sugar": st.session_state.sugPrice,
            "cups": st.session_state.cupPrice,
        }
    )
    st.session_state.market_history = st.session_state.market_history[-30:]


# ============================================================
# GAME HELPERS
# ============================================================
def current_marketing_effect():
    effect = 0
    if st.session_state.searchEngineCampaignDays > 0:
        effect = 10
        if st.session_state.socialMediaCampaignDays > 0:
            effect = 30
            if st.session_state.radioCampaignDays > 0:
                effect = 60
                if st.session_state.billboardCampaignDays > 0:
                    effect = 100
            elif st.session_state.billboardCampaignDays > 0:
                effect = 80
        elif st.session_state.radioCampaignDays > 0:
            effect = 40
            if st.session_state.billboardCampaignDays > 0:
                effect = 80
        elif st.session_state.billboardCampaignDays > 0:
            effect = 50
    elif st.session_state.socialMediaCampaignDays > 0:
        effect = 15
        if st.session_state.radioCampaignDays > 0:
            effect = 45
            if st.session_state.billboardCampaignDays > 0:
                effect = 85
        elif st.session_state.billboardCampaignDays > 0:
            effect = 60
    elif st.session_state.radioCampaignDays > 0:
        effect = 25
        if st.session_state.billboardCampaignDays > 0:
            effect = 65
    elif st.session_state.billboardCampaignDays > 0:
        effect = 35
    return effect


def format_money(value):
    return f"${value:,.2f}"


def empire_level():
    # Visual progression only; it does not change gameplay.
    points = (
        (st.session_state.locations - 1) * 3
        + st.session_state.coolers
        + st.session_state.canopies
        + max(0, int(st.session_state.maxcash // 200))
    )
    return min(5, 1 + points // 3)


def empire_level_name(level):
    names = {
        1: "Street Stand",
        2: "Popular Stand",
        3: "Lemonade Business",
        4: "Growing Empire",
        5: "Lemonade Empire",
    }
    return names[level]


def empire_progress():
    level = empire_level()
    if level >= 5:
        return 100, 5, "MAX LEVEL"
    points = (
        (st.session_state.locations - 1) * 3
        + st.session_state.coolers
        + st.session_state.canopies
        + max(0, int(st.session_state.maxcash // 200))
    )
    current_threshold = (level - 1) * 3
    next_threshold = level * 3
    pct = int(100 * (points - current_threshold) / max(1, next_threshold - current_threshold))
    return max(0, min(100, pct)), level, f"Level {level + 1} → {empire_level_name(level + 1)}"


def render_hero(title, subtitle=None):
    subtitle_html = f'<p class="hero-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div class="hero animate-pop">
            <div class="eyebrow">Lemonade Empire · Day {st.session_state.day}</div>
            <div class="hero-title">{title}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hud():
    cards = [
        ("💵", "Cash", format_money(st.session_state.cash)),
        ("🏦", "Bank", format_money(st.session_state.account)),
        ("🍋", "Lemons", f"{st.session_state.lemons}"),
        ("🍬", "Sugar", f"{st.session_state.sugar:.1f} kg"),
        ("🥤", "Cups", f"{st.session_state.cups}"),
        ("📍", "Locations", f"{st.session_state.locations}"),
    ]
    html = '<div class="hud">'
    for icon, label, value in cards:
        html += f'<div class="hud-card"><div class="hud-icon">{icon}</div><div class="hud-label">{label}</div><div class="hud-value">{value}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def show_recipe():
    with st.popover("📖 Recipe", use_container_width=True):
        st.markdown("### 🍋 Lemonade Recipe")
        st.markdown(
            """
            **One Jug of Lemonade**

            🍋 **5 Lemons**  
            🍬 **0.5 kg Sugar**  
            🥤 **Makes 8 Cups**

            ---

            | Ingredient | Per Jug |
            |---|---:|
            | 🍋 Lemons | 5 |
            | 🍬 Sugar | 0.5 kg |
            | 🥤 Cups | 8 |
            """
        )


def render_stand_scene():
    level = empire_level()
    stand_icon = "🛖"
    if level >= 2:
        stand_icon = "🍋🏪"
    if level >= 3:
        stand_icon = "🍋🏬"
    if level >= 5:
        stand_icon = "🏙️🍋"

    extras = ""
    if st.session_state.coolers:
        extras += " 🧊" * min(3, st.session_state.coolers)
    if st.session_state.canopies:
        extras += " ⛱️" * min(2, st.session_state.canopies)

    st.markdown(
        f"""
        <div class="stand-scene">
            <div class="cloud one">☁️</div>
            <div class="cloud two">☁️</div>
            <div class="sun">☀️</div>
            <div class="stand">{stand_icon}{extras}</div>
            <div class="stand-label">{empire_level_name(level)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empire_progress():
    pct, level, next_label = empire_progress()
    st.markdown(
        f"""
        <div class="card">
            <div class="section-kicker">YOUR EMPIRE</div>
            <h3 style="margin:2px 0 4px;">{empire_level_name(level)}</h3>
            <div style="display:flex;justify-content:space-between;gap:12px;color:#718071;font-size:.82rem;">
                <span>Level {level}</span><span>{next_label}</span>
            </div>
            <div class="empire-bar"><div class="empire-fill" style="width:{pct}%;"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_last_day():
    if not st.session_state.sales_history:
        st.markdown(
            """
            <div class="last-day">
                <div class="section-kicker">NO SALES HISTORY YET</div>
                <h3 style="margin:2px 0 4px;">This is your first day.</h3>
                <div style="color:#5F6E60;font-size:.9rem;">Set a price, stock the stand, and see what the market actually does.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    last = st.session_state.sales_history[-1]
    st.markdown(
        f"""
        <div class="last-day">
            <div class="section-kicker">YESTERDAY'S RESULTS · DAY {last['day']}</div>
            <h3 style="margin:2px 0 0;">Use history, not a forecast.</h3>
            <div style="color:#5F6E60;font-size:.9rem;">The game keeps tomorrow's demand uncertain. You only see what happened after the day is over.</div>
            <div class="last-day-grid">
                <div class="last-day-stat"><div class="label">PRICE</div><div class="value">{format_money(last['price'])}</div></div>
                <div class="last-day-stat"><div class="label">DEMAND</div><div class="value">{last['demand']} cups</div></div>
                <div class="last-day-stat"><div class="label">SOLD</div><div class="value">{last['cups_sold']} cups</div></div>
                <div class="last-day-stat"><div class="label">REVENUE</div><div class="value">{format_money(last['revenue'])}</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_price_history():
    if len(st.session_state.sales_history) < 2:
        return
    st.markdown('<div class="section-kicker">PRICE HISTORY</div>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.sales_history)[["day", "price", "demand", "cups_sold"]].copy()
    df = df.set_index("day")
    df.columns = ["Sale Price", "Demand", "Cups Sold"]
    st.line_chart(df, height=260)


def render_market_chart():
    if len(st.session_state.market_history) < 2:
        return
    st.markdown('<div class="section-kicker">MARKET HISTORY</div>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.market_history)[["day", "lemons", "sugar", "cups"]].copy()
    df = df.set_index("day")
    df.columns = ["Lemons", "Sugar", "Cups"]
    st.line_chart(df, height=240)


def buy_lemons(quantity, discount=0):
    cost = round(quantity * st.session_state.lemPrice * (1 - discount), 2)
    if cost <= st.session_state.cash:
        st.session_state.cash -= cost
        st.session_state.lemons += quantity
        st.toast(f"🍋 Bought {quantity} lemons for {format_money(cost)}")
        st.rerun()
    else:
        st.error("Not enough cash!")


def buy_sugar(quantity, discount=0):
    cost = round(quantity * st.session_state.sugPrice * (1 - discount), 2)
    if cost <= st.session_state.cash:
        st.session_state.cash -= cost
        st.session_state.sugar += quantity
        st.toast(f"🍬 Bought {quantity:g}kg sugar for {format_money(cost)}")
        st.rerun()
    else:
        st.error("Not enough cash!")


def buy_cups(quantity, discount=0):
    cost = round(quantity * st.session_state.cupPrice * (1 - discount), 2)
    if cost <= st.session_state.cash:
        st.session_state.cash -= cost
        st.session_state.cups += quantity
        st.toast(f"🥤 Bought {quantity} cups for {format_money(cost)}")
        st.rerun()
    else:
        st.error("Not enough cash!")


def go(screen):
    st.session_state.current_screen = screen
    st.rerun()


def simulate_day(sale_price):
    cash_start = st.session_state.cash
    marketing_effect = current_marketing_effect()
    st.session_state.marketingEffect = marketing_effect

    # Demand remains hidden until the day is simulated.
    if (5.85 - sale_price) < 0:
        sales_demand = 0
    else:
        sales_demand = int(1.45 * (5.85 - sale_price) ** 2)

    demand = int(
        sales_demand
        * random.uniform(0.72, 1.45)
        * st.session_state.locations
        * random.uniform(0.85, 1.2)
        * (1 + marketing_effect / 50)
    )

    max_jugs = min(
        int(st.session_state.lemons // 5),
        int(st.session_state.sugar // 0.5),
    )

    cups_sold = min(min(max_jugs * 8, demand), st.session_state.cups)
    jugs_made = int((cups_sold + 7) // 8)

    st.session_state.lemons -= jugs_made * 5
    st.session_state.sugar -= jugs_made * 0.5
    st.session_state.cups -= cups_sold
    revenue = cups_sold * sale_price

    st.session_state.cash += revenue

    summary = {
        "day": st.session_state.day,
        "price": sale_price,
        "demand": demand,
        "cups_sold": cups_sold,
        "revenue": revenue,
        "left_lemons_gone_bad": 0,
        "rent_paid": st.session_state.rent * st.session_state.locations,
        "wages_paid": st.session_state.wages,
        "robbed_amount": 0,
        "sugar_melted": 0.0,
        "cash_start": cash_start,
    }

    # Lemon rot
    if st.session_state.lemons > 0:
        rot_factor = max(
            0,
            0.5 - 0.4 * (st.session_state.coolers / st.session_state.locations),
        )
        left_lemons = int(round(st.session_state.lemons * rot_factor))
        summary["left_lemons_gone_bad"] = left_lemons
        st.session_state.lemons -= left_lemons

    # Rent hike
    rent_hike = random.randint(min(st.session_state.day, 50), 70)
    if rent_hike == 50:
        st.session_state.rent += 5
        summary["rent_hiked"] = True
        summary["rent_hike_amount"] = 5
    else:
        summary["rent_hiked"] = False
        summary["rent_hike_amount"] = 0

    rent_paid = st.session_state.rent * st.session_state.locations
    summary["rent_paid"] = rent_paid
    st.session_state.cash -= rent_paid

    # Wages
    if st.session_state.wages > 0:
        st.session_state.cash -= st.session_state.wages

    # Robbed
    if random.randint(1, 25) == 12:
        amount_robbed = int((1 - random.uniform(0, 0.89)) * st.session_state.cash)
        summary["robbed_amount"] = amount_robbed
        st.session_state.cash -= amount_robbed

    # Bank interest
    if st.session_state.account > 0:
        st.session_state.account *= 1 + st.session_state.savingsInterest

    # Rain
    if random.randint(1, 15) == 12:
        sugar_lost = round(
            st.session_state.sugar
            * (0.5 - 0.5 * (st.session_state.canopies / st.session_state.locations)),
            2,
        )
        summary["sugar_melted"] = sugar_lost
        st.session_state.sugar -= sugar_lost

    # Loan
    st.session_state.loanAmount *= 1 + st.session_state.loansInterest
    if st.session_state.loanDays > 0:
        st.session_state.loanDays -= 1

    if st.session_state.loanDays == 0 and st.session_state.loan == 1:
        st.session_state.loan = 0
        st.session_state.account -= st.session_state.loanAmount
        st.session_state.loanAmount = 0

    # Campaign days
    for key in (
        "searchEngineCampaignDays",
        "socialMediaCampaignDays",
        "radioCampaignDays",
        "billboardCampaignDays",
    ):
        if st.session_state[key] > 0:
            st.session_state[key] -= 1

    summary["net_cash_change"] = st.session_state.cash - summary["cash_start"]
    summary["cash_after"] = st.session_state.cash

    st.session_state.summary = summary
    st.session_state.sales_history.append(summary.copy())
    st.session_state.sales_history = st.session_state.sales_history[-30:]

    st.session_state.maxcash = max(st.session_state.maxcash, st.session_state.cash)

    if st.session_state.cash <= 0:
        st.session_state.game_over = True
    else:
        st.session_state.day += 1
        update_prices()

    st.session_state.current_screen = "day_summary"
    st.rerun()


# ============================================================
# INTRO SCREEN
# ============================================================
if not st.session_state.game_started and not st.session_state.game_over:
    render_hero(
        "Build your lemonade empire.",
        "Start with a single stand. Watch prices move, make the calls, and grow from street vendor to empire.",
    )

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown(
            """
            <div class="intro-rules">
                <div class="section-kicker">THE GAME</div>
                <h3 style="margin:2px 0 8px;">Every day is a business decision.</h3>
                <div style="color:#5F6E60;line-height:1.65;">
                    Buy ingredients at changing market prices. Set your own selling price. Invest in marketing and infrastructure. Survive long enough to build an empire.
                    <br><br>
                    <strong>Important:</strong> tomorrow's demand is not shown in advance. You learn from what actually happened yesterday.
                </div>
                <hr style="border:none;border-top:1px solid #E7E2CA;margin:16px 0;">
                🍋 5 lemons + 🍬 0.5 kg sugar = <strong>1 jug</strong><br>
                🥤 1 jug = <strong>8 cups</strong><br>
                💵 High score = <strong>maximum cash accumulated</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">START YOUR EMPIRE</div>', unsafe_allow_html=True)
        name_input = st.text_input("Your name", max_chars=7, placeholder="PLAYER").strip().upper()
        if st.button("🍋 Start Empire", type="primary", use_container_width=True):
            if name_input:
                init_game_state(name_input)
                st.rerun()
            st.warning("Please enter a name to start the game.")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# MAIN GAME
# ============================================================
elif st.session_state.game_started and (not st.session_state.game_over or st.session_state.current_screen == "day_summary"):
    st.session_state.marketingEffect = current_marketing_effect()

    render_hero(
        f"Welcome back, {st.session_state.player_name}.",
        f"Day {st.session_state.day} · {empire_level_name(empire_level())}",
    )
    render_hud()

    with st.expander("📖 Recipe & Rules", expanded=False):
        show_recipe()

    # ========================================================
    # MAIN MENU / TOWN
    # ========================================================
    if st.session_state.current_screen == "main_menu":
        render_last_day()

        st.markdown('<div class="section-kicker">YOUR TOWN</div>', unsafe_allow_html=True)
        st.markdown("### Run the empire")

        town = st.columns(4)
        buildings = [
            ("🏪", "Market", "Stock up on ingredients at today's prices.", "market"),
            ("🏦", "Lemon Bank", "Protect cash, earn interest, or borrow.", "bank"),
            ("🏬", "Department Store", "Upgrade the stand and add locations.", "dept_store"),
            ("📢", "Marketing", "Buy campaigns that change customer demand.", "marketing"),
        ]

        for col, (icon, title, copy, screen) in zip(town, buildings):
            with col:
                st.markdown(
                    f"""
                    <div class="town-card">
                        <div class="town-icon">{icon}</div>
                        <div class="town-title">{title}</div>
                        <div class="town-copy">{copy}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Enter {title}", key=f"town_{screen}", use_container_width=True):
                    go(screen)

        st.markdown("### 🍋 Your Lemonade Stand")
        left, right = st.columns([1.15, 1])
        with left:
            render_stand_scene()
        with right:
            render_empire_progress()
            active = []
            for label, key in [
                ("Search", "searchEngineCampaignDays"),
                ("Social", "socialMediaCampaignDays"),
                ("Radio", "radioCampaignDays"),
                ("Billboard", "billboardCampaignDays"),
            ]:
                if st.session_state[key] > 0:
                    active.append(f"{label}: {st.session_state[key]}d")
            if active:
                st.markdown('<div class="card"><div class="section-kicker">ACTIVE CAMPAIGNS</div>' + "".join(f'<span class="pill">📢 {x}</span>' for x in active) + '</div>', unsafe_allow_html=True)

        render_price_history()

        st.markdown("### ☀️ Prepare for Today")
        left, right = st.columns([1.1, .9])
        with left:
            st.markdown(
                """
                <div class="price-panel">
                    <div class="section-kicker">SET YOUR PRICE</div>
                    <div class="price-label">Selling price per cup</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            sale_price = st.number_input(
                "Sale price per cup ($)",
                min_value=0.0,
                value=float(st.session_state.sale_price),
                step=0.05,
                format="%.2f",
                label_visibility="collapsed",
                key="sale_price_input",
            )
            st.session_state.sale_price = sale_price
            st.caption(f"💾 Saved for your next visit: {format_money(st.session_state.sale_price)}")

            if st.button("🚀 Open Shop", type="primary", use_container_width=True):
                simulate_day(sale_price)

        with right:
            st.markdown(
                f"""
                <div class="card">
                    <div class="section-kicker">WHAT YOU CAN SEE</div>
                    <h3 style="margin:3px 0 8px;">Yesterday, not tomorrow.</h3>
                    <div style="color:#5F6E60;font-size:.9rem;line-height:1.6;">
                        You can review prior selling prices, demand and actual sales. The demand for the day you are about to play stays hidden until you open the shop.
                    </div>
                    <div style="margin-top:12px;">
                        <span class="pill">🔒 Future demand hidden</span>
                        <span class="pill">📊 History visible</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # DAY SUMMARY
    # ========================================================
    elif st.session_state.current_screen == "day_summary":
        summary = st.session_state.summary
        if summary is None:
            go("main_menu")

        render_hero(
            f"Day {summary['day']} is complete.",
            "Now you know what the market actually did.",
        )

        cols = st.columns(4)
        stats = [
            ("🏷️", "Price", format_money(summary["price"])),
            ("👥", "Demand", f"{summary['demand']} cups"),
            ("🥤", "Sold", f"{summary['cups_sold']} cups"),
            ("💰", "Revenue", format_money(summary["revenue"])),
        ]
        for col, (icon, label, value) in zip(cols, stats):
            with col:
                st.markdown(
                    f'<div class="hud-card"><div class="hud-icon">{icon}</div><div class="hud-label">{label}</div><div class="hud-value">{value}</div></div>',
                    unsafe_allow_html=True,
                )

        left, right = st.columns([1.25, .95])
        with left:
            st.markdown("### 🌇 End-of-Day Report")
            net = summary["net_cash_change"]
            net_class = "good" if net >= 0 else "bad"
            st.markdown(
                f'<div class="event {net_class}"><strong>Net cash change:</strong> {"+" if net >= 0 else "−"}{format_money(abs(net))}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="event"><strong>🧾 Rent paid:</strong> −{format_money(summary["rent_paid"])}</div>',
                unsafe_allow_html=True,
            )
            if summary["wages_paid"] > 0:
                st.markdown(
                    f'<div class="event"><strong>👷 Wages paid:</strong> −{format_money(summary["wages_paid"])}</div>',
                    unsafe_allow_html=True,
                )
            if summary["left_lemons_gone_bad"] > 0:
                st.markdown(
                    f'<div class="event warning"><strong>🍋 Spoiled lemons:</strong> {summary["left_lemons_gone_bad"]} lost</div>',
                    unsafe_allow_html=True,
                )
            if summary["robbed_amount"] > 0:
                st.markdown(
                    f'<div class="event bad"><strong>🚨 Robbery:</strong> −{format_money(summary["robbed_amount"])}</div>',
                    unsafe_allow_html=True,
                )
            if summary["sugar_melted"] > 0:
                st.markdown(
                    f'<div class="event warning"><strong>🌧️ Rain:</strong> {summary["sugar_melted"]:.2f} kg sugar lost</div>',
                    unsafe_allow_html=True,
                )
            if summary.get("rent_hiked"):
                st.markdown(
                    f'<div class="event warning"><strong>🏠 Rent increased:</strong> +{format_money(summary["rent_hike_amount"])} per location</div>',
                    unsafe_allow_html=True,
                )

        with right:
            st.markdown("### 📈 What happened?")
            utilization = 0 if summary["demand"] == 0 else int(100 * summary["cups_sold"] / summary["demand"])
            st.metric("Demand captured", f"{utilization}%")
            st.caption("This tells you how much of the day's actual demand you fulfilled. It is not a forecast for tomorrow.")
            st.metric("Cash after day", format_money(st.session_state.cash))

        render_price_history()

        if st.session_state.game_over:
            st.warning("Your cash hit zero. The empire cannot continue.")
            if st.button("💀 See Game Over", type="primary", use_container_width=True):
                st.rerun()
        else:
            if st.button(f"🌅 Begin Day {st.session_state.day}", type="primary", use_container_width=True):
                go("main_menu")

    # ========================================================
    # MARKET
    # ========================================================
    elif st.session_state.current_screen == "market":
        render_hero("The Market", "Buy ingredients now. Prices move from day to day.")
        show_recipe()

        cols = st.columns(3)
        prices = [
            ("🍋", "Lemons", st.session_state.lemPrice, "unit"),
            ("🍬", "Sugar", st.session_state.sugPrice, "kg"),
            ("🥤", "Cups", st.session_state.cupPrice, "unit"),
        ]
        for col, (icon, name, price, unit) in zip(cols, prices):
            with col:
                st.markdown(
                    f'<div class="card"><div class="hud-icon">{icon}</div><div class="section-kicker">TODAY</div><h3 style="margin:2px 0;">{name}</h3><div class="price-number" style="font-size:2.2rem;">{format_money(price)}</div><div class="price-copy">per {unit}</div></div>',
                    unsafe_allow_html=True,
                )

        item_specs = [
            (
                "🍋 Lemons",
                [
                    ("1", 1, 0),
                    ("5 · 4% off", 5, .04),
                    ("20 · 7% off", 20, .07),
                ],
                buy_lemons,
            ),
            (
                "🍬 Sugar",
                [
                    ("1 kg", 1, 0),
                    ("5 kg · 2% off", 5, .02),
                    ("20 kg · 9% off", 20, .09),
                ],
                buy_sugar,
            ),
            (
                "🥤 Cups",
                [
                    ("1", 1, 0),
                    ("5 · 3% off", 5, .03),
                    ("20 · 8% off", 20, .08),
                ],
                buy_cups,
            ),
        ]
        prices_for_items = [st.session_state.lemPrice, st.session_state.sugPrice, st.session_state.cupPrice]
        for (title, options, purchase_fn), base_price in zip(item_specs, prices_for_items):
            st.markdown(f"### {title}")
            cols = st.columns(3)
            for col, (label, qty, discount) in zip(cols, options):
                total = round(qty * base_price * (1 - discount), 2)
                with col:
                    if st.button(f"Buy {label} · {format_money(total)}", key=f"buy_{title}_{label}", use_container_width=True):
                        purchase_fn(qty, discount)

        render_market_chart()
        if st.button("↩️ Back to Town", use_container_width=True):
            go("main_menu")

    # ========================================================
    # BANK
    # ========================================================
    elif st.session_state.current_screen == "bank":
        render_hero("Lemon Bank", "Keep cash safe, earn interest, and use credit strategically.")

        cols = st.columns(3)
        with cols[0]:
            st.markdown('<div class="card"><div class="section-kicker">SAVINGS</div><h3>Deposit</h3></div>', unsafe_allow_html=True)
            dep_amt = st.number_input("Deposit amount", min_value=0.0, max_value=float(st.session_state.cash), value=0.0, step=1.0, format="%.2f")
            if st.button("Deposit Cash", use_container_width=True):
                st.session_state.account += round(dep_amt, 2)
                st.session_state.cash -= round(dep_amt, 2)
                st.session_state.maxAccount = max(st.session_state.maxAccount, st.session_state.account)
                st.rerun()

        with cols[1]:
            st.markdown('<div class="card"><div class="section-kicker">SAVINGS</div><h3>Withdraw</h3></div>', unsafe_allow_html=True)
            draw_amt = st.number_input("Withdrawal amount", min_value=0.0, max_value=float(st.session_state.account), value=0.0, step=1.0, format="%.2f", key="draw")
            if st.button("Withdraw Cash", use_container_width=True):
                st.session_state.account -= round(draw_amt, 2)
                st.session_state.cash += round(draw_amt, 2)
                st.rerun()

        with cols[2]:
            st.markdown(f'<div class="card"><div class="section-kicker">CREDIT</div><h3>10-Day Loan</h3><div class="price-copy">Maximum credit is based on past balances.</div></div>', unsafe_allow_html=True)
            st.write(f"Savings interest: **{st.session_state.savingsInterest*100:.1f}% / day**")
            st.write(f"Loan interest: **{st.session_state.loansInterest*100:.1f}% / day**")
            request = st.number_input("Loan amount", min_value=0.0, value=0.0, step=10.0, format="%.2f", key="loan_request")
            if st.button("Request 10-Day Loan", use_container_width=True):
                if st.session_state.loan == 1:
                    st.error("Outstanding loan exists!")
                elif request > (st.session_state.maxAccount * 0.75 * 1.1):
                    st.error("Request denied: not enough credit history.")
                elif request <= 0:
                    st.error("Enter a positive amount.")
                else:
                    st.session_state.loanAmount = request
                    st.session_state.loan = 1
                    st.session_state.loanDays = 10
                    st.session_state.account += request
                    st.success("Request approved. Funds transferred.")
                    st.rerun()

        if st.session_state.loan == 1:
            st.markdown(
                f'<div class="event warning"><strong>Outstanding loan:</strong> {format_money(st.session_state.loanAmount)} · {st.session_state.loanDays} days remaining</div>',
                unsafe_allow_html=True,
            )
        if st.button("↩️ Back to Town", use_container_width=True):
            go("main_menu")

    # ========================================================
    # DEPARTMENT STORE
    # ========================================================
    elif st.session_state.current_screen == "dept_store":
        render_hero("Department Store", "Build a stronger stand and expand your territory.")
        cols = st.columns(3)
        upgrades = [
            ("🧊", "Lemon Cooler", "Reduces spoilage.", st.session_state.coolerPrice, "cooler"),
            ("⛱️", "Stand Canopy", "Reduces losses when it rains.", st.session_state.canopyPrice, "canopy"),
            ("🏪", "Additional Stand", "Adds another location and increases wages.", st.session_state.standPrice, "stand"),
        ]
        for col, (icon, name, copy, price, kind) in zip(cols, upgrades):
            with col:
                owned = {
                    "cooler": st.session_state.coolers,
                    "canopy": st.session_state.canopies,
                    "stand": max(0, st.session_state.locations - 1),
                }[kind]
                st.markdown(
                    f"""
                    <div class="upgrade-card">
                        <div class="upgrade-icon">{icon}</div>
                        <div class="upgrade-name">{name}</div>
                        <div class="upgrade-copy">{copy}</div>
                        <div class="pill">Owned: {owned}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if kind == "cooler":
                    if st.button(f"Buy Cooler · {format_money(price)}", key="upgrade_cooler", use_container_width=True):
                        if st.session_state.coolers < st.session_state.locations and st.session_state.cash >= price:
                            st.session_state.cash -= price
                            st.session_state.coolers += 1
                            st.toast("🧊 Cooler purchased!")
                            st.rerun()
                        st.error("Unavailable or insufficient funds.")
                elif kind == "canopy":
                    if st.button(f"Buy Canopy · {format_money(price)}", key="upgrade_canopy", use_container_width=True):
                        if st.session_state.canopies < st.session_state.locations and st.session_state.cash >= price:
                            st.session_state.cash -= price
                            st.session_state.canopies += 1
                            st.toast("⛱️ Canopy purchased!")
                            st.rerun()
                        st.error("Unavailable or insufficient funds.")
                else:
                    if st.button(f"Buy Stand · {format_money(price)}", key="upgrade_stand", use_container_width=True):
                        if st.session_state.cash >= price:
                            st.session_state.cash -= price
                            st.session_state.locations += 1
                            st.session_state.wages += 5
                            st.toast("🏪 New stand opened!")
                            st.rerun()
                        st.error("Insufficient funds.")

        st.markdown("### 🏙️ Empire Progress")
        render_stand_scene()
        render_empire_progress()

        if st.button("↩️ Back to Town", use_container_width=True):
            go("main_menu")

    # ========================================================
    # MARKETING
    # ========================================================
    elif st.session_state.current_screen == "marketing":
        render_hero("Marketing Agency", "Buy attention. Turn attention into customers.")
        effect = current_marketing_effect()
        st.markdown(
            f'<div class="card"><div class="section-kicker">CURRENT IMPACT</div><h3 style="margin:2px 0;">Marketing effectiveness: {effect}%</h3><div style="color:#5F6E60;">Combined campaigns change the demand calculation behind the scenes.</div></div>',
            unsafe_allow_html=True,
        )

        campaigns = [
            ("🔎", "Search", "searchEnginePrice", "searchEngineCampaignDays", 7),
            ("📱", "Social Media", "socialMediaPrice", "socialMediaCampaignDays", 7),
            ("📻", "Radio", "radioPrice", "radioCampaignDays", 7),
            ("🪧", "Billboard", "billboardPrice", "billboardCampaignDays", 7),
        ]
        cols = st.columns(4)
        for col, (icon, name, price_key, days_key, days) in zip(cols, campaigns):
            with col:
                price = st.session_state[price_key]
                remaining = st.session_state[days_key]
                st.markdown(
                    f"""
                    <div class="upgrade-card">
                        <div class="upgrade-icon">{icon}</div>
                        <div class="upgrade-name">{name}</div>
                        <div class="upgrade-copy">{remaining} days active</div>
                        <div class="pill">{format_money(price)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Buy {name}", key=f"campaign_{days_key}", use_container_width=True):
                    if st.session_state.cash >= price:
                        st.session_state.cash -= price
                        st.session_state[days_key] += days
                        st.toast(f"📢 {name} campaign active!")
                        st.rerun()
                    else:
                        st.error("Not enough cash!")

        if st.button("↩️ Back to Town", use_container_width=True):
            go("main_menu")

# ============================================================
# GAME OVER
# ============================================================
elif st.session_state.game_over:
    st.markdown(
        f"""
        <div class="game-over">
            <div style="font-size:4rem;">🍋💀</div>
            <div class="section-kicker">THE EMPIRE ENDS HERE</div>
            <h1 style="margin:4px 0;">Game Over</h1>
            <div style="font-size:1rem;color:#687568;">{st.session_state.player_name}'s empire lasted {st.session_state.day} day(s).</div>
            <div style="margin-top:16px;">Maximum cash reached: <strong>{format_money(st.session_state.maxcash)}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🍋 Build It Again", type="primary", use_container_width=True):
        st.session_state.game_started = False
        st.session_state.game_over = False
        st.session_state.current_screen = "main_menu"
        st.rerun()
