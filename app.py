import streamlit as s

# Let's write the Streamlit application code directly to a file named `app.py`
with open('app.py', 'w') as f:
    f.write('''import streamlit as st
import random
import pandas as pd
from datetime import date
import os

# Page Configuration
st.set_page_config(page_title="Lemonade Empire", page_icon="🍋", layout="centered")

# Initialize Session State variables if they don't exist
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "main_menu"

# Game State Variables
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
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.current_screen = "main_menu"
    update_prices()

def update_prices():
    # daily change in sugar, lemon, and cup prices
    lemChange = random.uniform(-0.08, 0.11)
    sugChange = random.uniform(-0.07, 0.10)
    cupChange = random.uniform(-0.03, 0.04)
    
    st.session_state.lemPrice = max(0.05, round(st.session_state.yestLemPrice + lemChange, 2))
    st.session_state.sugPrice = max(0.05, round(st.session_state.yestSugPrice + sugChange, 2))
    st.session_state.cupPrice = max(0.05, round(st.session_state.yestCupPrice + cupChange, 2))
    
    st.session_state.yestLemPrice = st.session_state.lemPrice
    st.session_state.yestSugPrice = st.session_state.sugPrice
    st.session_state.yestCupPrice = st.session_state.cupPrice
    
    # Department store items prices
    st.session_state.coolerPrice = 35 + random.randint(-10, 10)
    st.session_state.canopyPrice = 50 + random.randint(-15, 15)
    st.session_state.standPrice = 115 + random.randint(-30, 30)
    
    # Marketing prices
    st.session_state.radioPrice = 235 + random.randint(-15, 75)
    st.session_state.searchEnginePrice = 30 + random.randint(-5, 15)
    st.session_state.socialMediaPrice = 55 + random.randint(-10, 25)
    st.session_state.billboardPrice = 650 + random.randint(-25, 85)

# Title and Intro Screen
if not st.session_state.game_started and not st.session_state.game_over:
    st.title("🍋 Lemonade Empire")
    st.write("Welcome to Lemonade Empire! Build your business empire from scratch.")
    
    name_input = st.text_input("Please enter your name:", max_chars=7).strip().upper()
    
    st.subheader("Guidelines")
    st.markdown("""
    1. Don't run out of cash.
    2. 5 Lemons + 0.5kg Sugar = 1 Jug of Lemonade.
    3. 1 Jug = 8 Cups of Lemonade.
    4. High scores are based on maximum money accumulated.
    """)
    
    if st.button("Start Empire"):
        if name_input:
            init_game_state(name_input)
            st.rerun()
        else:
            st.warning("Please enter a name to start the game!")

# Main Game Dashboard and Screens
elif st.session_state.game_started and not st.session_state.game_over:
    # Update marketing effect
    m_eff = 0
    if st.session_state.searchEngineCampaignDays > 0:
        m_eff = 10
        if st.session_state.socialMediaCampaignDays > 0:
            m_eff = 30
            if st.session_state.radioCampaignDays > 0:
                m_eff = 60
            if st.session_state.billboardCampaignDays > 0:
                m_eff = 100
        elif st.session_state.radioCampaignDays > 0:
            m_eff = 40
            if st.session_state.billboardCampaignDays > 0:
                m_eff = 80
        elif st.session_state.billboardCampaignDays > 0:
            m_eff = 50
    elif st.session_state.socialMediaCampaignDays > 0:
        m_eff = 15
        if st.session_state.radioCampaignDays > 0:
            m_eff = 45
            if st.session_state.billboardCampaignDays > 0:
                m_eff = 85
        elif st.session_state.billboardCampaignDays > 0:
            m_eff = 60
    elif st.session_state.radioCampaignDays > 0:
        m_eff = 25
        if st.session_state.billboardCampaignDays > 0:
            m_eff = 65
    elif st.session_state.billboardCampaignDays > 0:
        m_eff = 35
    
    st.session_state.marketingEffect = m_eff

    # Global Sidebar / Status bar
    st.sidebar.title(f"📊 {st.session_state.player_name}'s Status")
    st.sidebar.markdown(f"**Day:** {st.session_state.day}")
    st.sidebar.markdown(f"**Cash:** ${st.session_state.cash:,.2f}")
    st.sidebar.markdown(f"**Bank Account:** ${st.session_state.account:,.2f}")
    st.sidebar.markdown(f"**Debt:** ${st.session_state.loanAmount:,.2f}")
    st.sidebar.markdown(f"**Locations Owned:** {st.session_state.locations}")
    
    st.sidebar.subheader("Inventory")
    st.sidebar.markdown(f"🍋 **Lemons:** {st.session_state.lemons}")
    st.sidebar.markdown(f"🍬 **Sugar:** {st.session_state.sugar:,.1f} kg")
    st.sidebar.markdown(f"🥛 **Cups:** {st.session_state.cups}")
    st.sidebar.markdown(f"❄️ **Coolers:** {st.session_state.coolers}")
    st.sidebar.markdown(f"⛺ **Canopies:** {st.session_state.canopies}")

    # Main Menu Navigation
    st.title(f"🍋 Day {st.session_state.day}")
    
    # Screen routing
    if st.session_state.current_screen == "main_menu":
        st.subheader("Main Menu")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏬 Visit Market", use_container_width=True):
                st.session_state.current_screen = "market"
                st.rerun()
            if st.button("🏦 Visit Bank", use_container_width=True):
                st.session_state.current_screen = "bank"
                st.rerun()
        with col2:
            if st.button("🏢 Department Store", use_container_width=True):
                st.session_state.current_screen = "dept_store"
                st.rerun()
            if st.button("📢 Marketing Agency", use_container_width=True):
                st.session_state.current_screen = "marketing"
                st.rerun()

        st.write("---")
        st.subheader("🌅 Prepare for Sales Day")
        sale_price = st.number_input("Set Sale Price per Cup ($):", min_value=0.0, value=0.5, step=0.05)
        if st.button("🚀 Open Shop & Simulate Day", type="primary", use_container_width=True):
            # Simulation calculations
            if (5.85 - sale_price) < 0:
                salesDemand = 0
            else:
                salesDemand = int(1.45 * (5.85 - sale_price) ** 2)
            
            demand = int(salesDemand * random.uniform(.72, 1.45) * st.session_state.locations * random.uniform(.85, 1.2) * (1 + st.session_state.marketingEffect / 50))
            maxJugs = min(int(st.session_state.lemons // 5), int(st.session_state.sugar // 0.5))
            cups_sold = min(min(maxJugs * 8, demand), st.session_state.cups)
            
            jugsMade = int((cups_sold + 7) // 8)
            st.session_state.lemons -= jugsMade * 5
            st.session_state.sugar -= jugsMade * 0.5
            st.session_state.cups -= cups_sold
            st.session_state.cash += cups_sold * sale_price
            
            # Record results in session state for a summary screen
            st.session_state.summary = {
                "demand": demand,
                "cups_sold": cups_sold,
                "revenue": cups_sold * sale_price,
                "left_lemons_gone_bad": 0,
                "rent_paid": st.session_state.rent * st.session_state.locations,
                "wages_paid": st.session_state.wages,
                "robbed_amount": 0,
                "sugar_melted": 0.0
            }
            
            # Lemons Rotting
            if st.session_state.lemons > 0:
                rot_factor = 0.5 - 0.4 * (st.session_state.coolers / st.session_state.locations)
                left_lemons = int(round(st.session_state.lemons * rot_factor))
                st.session_state.summary["left_lemons_gone_bad"] = left_lemons
                st.session_state.lemons -= left_lemons
                
            # Rent Hike Chance
            rentHike = random.randint(min(st.session_state.day, 50), 70)
            if rentHike == 50:
                st.session_state.rent += 5
            st.session_state.cash -= st.session_state.rent * st.session_state.locations
            
            # Wages Payment
            if st.session_state.wages > 0:
                st.session_state.cash -= st.session_state.wages
                
            # Robbed Chance
            if random.randint(1, 25) == 12:
                amount_robbed = int((1 - random.uniform(0, 0.89)) * st.session_state.cash)
                st.session_state.summary["robbed_amount"] = amount_robbed
                st.session_state.cash -= amount_robbed
                
            # Bank Interest Accumulation
            if st.session_state.account > 0:
                st.session_state.account *= (1 + st.session_state.savingsInterest)
                
            # Rained Chance
            if random.randint(1, 15) == 12:
                sugar_lost = round(st.session_state.sugar * (0.5 - 0.5 * (st.session_state.canopies / st.session_state.locations)), 2)
                st.session_state.summary["sugar_melted"] = sugar_lost
                st.session_state.sugar -= sugar_lost
                
            # Loan Adjustments
            st.session_state.loanAmount *= (1 + st.session_state.loansInterest)
            if st.session_state.loanDays > 0:
                st.session_state.loanDays -= 1
            if st.session_state.loanDays == 0 and st.session_state.loan == 1:
                st.session_state.loan = 0
                st.session_state.account -= st.session_state.loanAmount
                st.session_state.loanAmount = 0
                
            # Campaign reduction
            if st.session_state.searchEngineCampaignDays > 0: st.session_state.searchEngineCampaignDays -= 1
            if st.session_state.socialMediaCampaignDays > 0: st.session_state.socialMediaCampaignDays -= 1
            if st.session_state.radioCampaignDays > 0: st.session_state.radioCampaignDays -= 1
            if st.session_state.billboardCampaignDays > 0: st.session_state.billboardCampaignDays -= 1
            
            # Game over check
            if st.session_state.cash <= 0:
                st.session_state.game_over = True
            else:
                st.session_state.day += 1
                update_prices()
            
            st.session_state.current_screen = "day_summary"
            st.rerun()

    elif st.session_state.current_screen == "day_summary":
        st.subheader("🌅 Daily Summary")
        sum_data = st.session_state.summary
        st.write(f"**Demand Today:** {sum_data['demand']} cups")
        st.write(f"**Cups Sold:** {sum_data['cups_sold']}")
        st.success(f"**Revenue:** +${sum_data['revenue']:,.2f}")
        st.error(f"**Rent paid:** -${sum_data['rent_paid']:,.2f}")
        if sum_data['wages_paid'] > 0:
            st.error(f"**Wages paid:** -${sum_data['wages_paid']:,.2f}")
        if sum_data['left_lemons_gone_bad'] > 0:
            st.warning(f"🍋 **Lemons Rot (gone bad):** {sum_data['left_lemons_gone_bad']} units")
        if sum_data['robbed_amount'] > 0:
            st.error(f"🚨 **Robbed!** Lost -${sum_data['robbed_amount']:,.2f}")
        if sum_data['sugar_melted'] > 0:
            st.warning(f"🌧️ **Rained!** {sum_data['sugar_melted']} kg sugar melted")
            
        if st.button("Proceed to Next Day", type="primary", use_container_width=True):
            st.session_state.current_screen = "main_menu"
            st.rerun()

    elif st.session_state.current_screen == "market":
        st.subheader("🏬 Market Shop")
        st.write(f"Lemons: ${st.session_state.lemPrice:.2f} | Sugar: ${st.session_state.sugPrice:.2f}/kg | Cups: ${st.session_state.cupPrice:.2f}")
        
        tab1, tab2, tab3 = st.tabs(["🍋 Lemons", "🍬 Sugar", "🥛 Cups"])
        
        with tab1:
            qty = st.selectbox("Buy Quantity:", ["1 unit", "5 units (4% Off)", "20 units (7% Off)"])
            amt = st.number_input("Number of packs to buy:", min_value=0, value=0, step=1)
            cost = 0.0
            total_items = 0
            if "1 unit" in qty:
                cost = amt * st.session_state.lemPrice
                total_items = amt
            elif "5 units" in qty:
                cost = amt * round(5 * st.session_state.lemPrice * 0.96, 2)
                total_items = amt * 5
            else:
                cost = amt * round(20 * st.session_state.lemPrice * 0.93, 2)
                total_items = amt * 20
            st.write(f"Total Cost: **${cost:.2f}**")
            if st.button("Confirm Lemon Purchase", use_container_width=True):
                if cost <= st.session_state.cash:
                    st.session_state.cash -= cost
                    st.session_state.lemons += total_items
                    st.success(f"Purchased {total_items} lemons!")
                    st.rerun()
                else:
                    st.error("Not enough cash!")
                    
        with tab2:
            qty_s = st.selectbox("Buy Quantity Sugar:", ["1kg", "5kg (2% Off)", "20kg (9% Off)"])
            amt_s = st.number_input("Number of sugar packs to buy:", min_value=0, value=0, step=1, key="sug_pack")
            cost_s = 0.0
            total_sug = 0.0
            if "1kg" in qty_s:
                cost_s = amt_s * st.session_state.sugPrice
                total_sug = amt_s * 1.0
            elif "5kg" in qty_s:
                cost_s = amt_s * round(5 * st.session_state.sugPrice * 0.98, 2)
                total_sug = amt_s * 5.0
            else:
                cost_s = amt_s * round(20 * st.session_state.sugPrice * 0.91, 2)
                total_sug = amt_s * 20.0
            st.write(f"Total Cost: **${cost_s:.2f}**")
            if st.button("Confirm Sugar Purchase", use_container_width=True):
                if cost_s <= st.session_state.cash:
                    st.session_state.cash -= cost_s
                    st.session_state.sugar += total_sug
                    st.success(f"Purchased {total_sug}kg sugar!")
                    st.rerun()
                else:
                    st.error("Not enough cash!")
                    
        with tab3:
            qty_c = st.selectbox("Buy Quantity Cups:", ["1 cup", "5 cups (3% Off)", "20 cups (8% Off)"])
            amt_c = st.number_input("Number of cup packs to buy:", min_value=0, value=0, step=1, key="cup_pack")
            cost_c = 0.0
            total_cups = 0
            if "1 cup" in qty_c:
                cost_c = amt_c * st.session_state.cupPrice
                total_cups = amt_c
            elif "5 cups" in qty_c:
                cost_c = amt_c * round(5 * st.session_state.cupPrice * 0.97, 2)
                total_cups = amt_c * 5
            else:
                cost_c = amt_c * round(20 * st.session_state.cupPrice * 0.92, 2)
                total_cups = amt_c * 20
            st.write(f"Total Cost: **${cost_c:.2f}**")
            if st.button("Confirm Cups Purchase", use_container_width=True):
                if cost_c <= st.session_state.cash:
                    st.session_state.cash -= cost_c
                    st.session_state.cups += total_cups
                    st.success(f"Purchased {total_cups} cups!")
                    st.rerun()
                else:
                    st.error("Not enough cash!")
                    
        if st.button("↩️ Back to Menu", use_container_width=True):
            st.session_state.current_screen = "main_menu"
            st.rerun()

    elif st.session_state.current_screen == "bank":
        st.subheader("🏦 Lemon Bank")
        st.write(f"Savings Interest: **{st.session_state.savingsInterest*100}%**")
        st.write(f"Loan Interest: **{st.session_state.loansInterest*100}%**")
        
        dep_col, draw_col, loan_col = st.columns(3)
        
        with dep_col:
            st.markdown("**Deposit**")
            dep_amt = st.number_input("Amount:", min_value=0.0, max_value=float(st.session_state.cash), value=0.0, step=1.0)
            if st.button("Deposit Cash", use_container_width=True):
                st.session_state.account += round(dep_amt, 2)
                st.session_state.cash -= round(dep_amt, 2)
                st.rerun()
                
        with draw_col:
            st.markdown("**Withdraw**")
            draw_amt = st.number_input("Amount:", min_value=0.0, max_value=float(st.session_state.account), value=0.0, step=1.0, key="draw")
            if st.button("Withdraw Cash", use_container_width=True):
                st.session_state.account -= round(draw_amt, 2)
                st.session_state.cash += round(draw_amt, 2)
                st.rerun()
                
        with loan_col:
            st.markdown("**Get Loan**")
            st.write("Maximum credit is based on past balances.")
            request = st.number_input("Loan Amount Requested:", min_value=0.0, value=0.0, step=10.0)
            if st.button("Request 10 Day Loan", use_container_width=True):
                if st.session_state.loan == 1:
                    st.error("Outstanding loan exists!")
                elif request > (st.session_state.maxAccount * 0.75 * 1.1):
                    st.error("Request Denied! Not enough credit.")
                elif request <= 0:
                    st.error("Request positive amount.")
                else:
                    st.session_state.loanAmount = request
                    st.session_state.loan = 1
                    st.session_state.loanDays = 10
                    st.session_state.account += request
                    st.success("Request Approved! Funds transferred.")
                    st.rerun()
                    
        if st.button("↩️ Back to Menu", use_container_width=True):
            st.session_state.current_screen = "main_menu"
            st.rerun()

    elif st.session_state.current_screen == "dept_store":
        st.subheader("🏬 Department Store")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Lemon Cooler**")
            st.write(f"Price: ${st.session_state.coolerPrice:.2f}")
            if st.button("Buy Cooler", use_container_width=True):
                if st.session_state.coolers < st.session_state.locations and st.session_state.cash >= st.session_state.coolerPrice:
                    st.session_state.cash -= st.session_state.coolerPrice
                    st.session_state.coolers += 1
                    st.success("Cooler purchased!")
                    st.rerun()
                else:
                    st.error("Unavailable or insufficient funds.")
        with col2:
            st.write(f"**Lemon Stand Canopy**")
            st.write(f"Price: ${st.session_state.canopyPrice:.2f}")
            if st.button("Buy Canopy", use_container_width=True):
                if st.session_state.canopies < st.session_state.locations and st.session_state.cash >= st.session_state.canopyPrice:
                    st.session_state.cash -= st.session_state.canopyPrice
                    st.session_state.canopies += 1
                    st.success("Canopy purchased!")
                    st.rerun()
                else:
                    st.error("Unavailable or insufficient funds.")
        with col3:
            st.write(f"**Additional Lemon Stand**")
            st.write(f"Price: ${st.session_state.standPrice:.2f}")
            if st.button("Buy Additional Stand", use_container_width=True):
                if st.session_state.cash >= st.session_state.standPrice:
                    st.session_state.cash -= st.session_state.standPrice
                    st.session_state.locations += 1
                    st.session_state.wages += 5
                    st.success("Additional stand purchased!")
                    st.rerun()
                else:
                    st.error("Insufficient funds.")
                    
        if st.button("↩️ Back to Menu", use_container_width=True):
            st.session_state.current_screen = "main_menu"
            st.rerun()

    elif st.session_state.current_screen == "marketing":
        st.subheader("📢 Marketing Agency")
        st.write(f"Overall Effectiveness: **{st.session_state.marketingEffect}%**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Internet Search (SEO): ${st.session_state.searchEnginePrice:.2f}")
            if st.button("Buy SEO", use_container_width=True):
                if st.session_state.cash >= st.session_state.searchEnginePrice:
                    st.session_state.cash -= st.session_state.searchEnginePrice
                    st.session_state.searchEngineCampaignDays += 7
                    st.success("SEO Active!")
                    st.rerun()
            st.write(f"Radio Ad: ${st.session_state.radioPrice:.2f}")
            if st.button("Buy Radio Campaign", use_container_width=True):
                if st.session_state.cash >= st.session_state.radioPrice:
                    st.session_state.cash -= st.session_state.radioPrice
                    st.session_state.radioCampaignDays += 7
                    st.success("Radio Active!")
                    st.rerun()
        with col2:
            st.write(f"Social Media Ad: ${st.session_state.socialMediaPrice:.2f}")
            if st.button("Buy Social Media Ads", use_container_width=True):
                if st.session_state.cash >= st.session_state.socialMediaPrice:
                    st.session_state.cash -= st.session_state.socialMediaPrice
                    st.session_state.socialMediaCampaignDays += 7
                    st.success("Social Media active!")
                    st.rerun()
            st.write(f"Billboard Ad: ${st.session_state.billboardPrice:.2f}")
            if st.button("Buy Billboard Ad", use_container_width=True):
                if st.session_state.cash >= st.session_state.billboardPrice:
                    st.session_state.cash -= st.session_state.billboardPrice
                    st.session_state.billboardCampaignDays += 7
                    st.success("Billboard active!")
                    st.rerun()
                    
        if st.button("↩️ Back to Menu", use_container_width=True):
            st.session_state.current_screen = "main_menu"
            st.rerun()

# Game Over Screen
elif st.session_state.game_over:
    st.title("💀 GAME OVER")
    st.error(f"Your empire came crumbling down after {st.session_state.day} day(s).")
    
    if st.button("Play Again", type="primary", use_container_width=True):
        st.session_state.game_started = False
        st.session_state.game_over = False
        st.rerun()
''')
