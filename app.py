import streamlit as st
import random
import pandas as pd
from datetime import date
import os

# Page Configuration
st.set_page_config(
    page_title="Lemonade Empire",
    page_icon="🍋",
    layout="centered"
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "current_screen" not in st.session_state:
    st.session_state.current_screen = "main_menu"

# ============================================================
# GAME STATE
# ============================================================

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

    # NEW: Remember the player's last selling price
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

    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.current_screen = "main_menu"

    update_prices()


def update_prices():
    # Daily change in sugar, lemon, and cup prices
    lemChange = random.uniform(-0.08, 0.11)
    sugChange = random.uniform(-0.07, 0.10)
    cupChange = random.uniform(-0.03, 0.04)

    st.session_state.lemPrice = max(
        0.05,
        round(st.session_state.yestLemPrice + lemChange, 2)
    )

    st.session_state.sugPrice = max(
        0.05,
        round(st.session_state.yestSugPrice + sugChange, 2)
    )

    st.session_state.cupPrice = max(
        0.05,
        round(st.session_state.yestCupPrice + cupChange, 2)
    )

    st.session_state.yestLemPrice = st.session_state.lemPrice
    st.session_state.yestSugPrice = st.session_state.sugPrice
    st.session_state.yestCupPrice = st.session_state.cupPrice

    # Department store items
    st.session_state.coolerPrice = 35 + random.randint(-10, 10)
    st.session_state.canopyPrice = 50 + random.randint(-15, 15)
    st.session_state.standPrice = 115 + random.randint(-30, 30)

    # Marketing prices
    st.session_state.radioPrice = 235 + random.randint(-15, 75)
    st.session_state.searchEnginePrice = 30 + random.randint(-5, 15)
    st.session_state.socialMediaPrice = 55 + random.randint(-10, 25)
    st.session_state.billboardPrice = 650 + random.randint(-25, 85)


# ============================================================
# RECIPE
# ============================================================

def show_recipe():
    """
    Displays the lemonade recipe in a popover.
    Available from anywhere in the game.
    """
    with st.popover("📖 Recipe", use_container_width=True):
        st.subheader("🍋 Lemonade Recipe")

        st.markdown("""
        ### One Jug of Lemonade

        🍋 **5 Lemons**  
        🍬 **0.5 kg Sugar**  
        🥛 **Makes 8 Cups**

        ---

        **Quick Reference**

        | Ingredient | Per Jug |
        |---|---:|
        | 🍋 Lemons | 5 |
        | 🍬 Sugar | 0.5 kg |
        | 🥛 Cups | 8 |

        **Example:**  
        20 lemons + 2 kg sugar = **4 jugs = 32 cups**
        """)


# ============================================================
# INGREDIENT PURCHASE FUNCTIONS
# ============================================================

def buy_lemons(quantity, discount=0):
    base_cost = quantity * st.session_state.lemPrice
    cost = round(base_cost * (1 - discount), 2)

    if cost <= st.session_state.cash:
        st.session_state.cash -= cost
        st.session_state.lemons += quantity
        st.toast(f"🍋 Bought {quantity} lemons for ${cost:.2f}")
        st.rerun()
    else:
        st.error("Not enough cash!")


def buy_sugar(quantity, discount=0):
    base_cost = quantity * st.session_state.sugPrice
    cost = round(base_cost * (1 - discount), 2)

    if cost <= st.session_state.cash:
        st.session_state.cash -= cost
        st.session_state.sugar += quantity
        st.toast(f"🍬 Bought {quantity:g}kg sugar for ${cost:.2f}")
        st.rerun()
    else:
        st.error("Not enough cash!")


def buy_cups(quantity, discount=0):
    base_cost = quantity * st.session_state.cupPrice
    cost = round(base_cost * (1 - discount), 2)

    if cost <= st.session_state.cash:
        st.session_state.cash -= cost
        st.session_state.cups += quantity
        st.toast(f"🥛 Bought {quantity} cups for ${cost:.2f}")
        st.rerun()
    else:
        st.error("Not enough cash!")


# ============================================================
# INTRO SCREEN
# ============================================================

if not st.session_state.game_started and not st.session_state.game_over:

    st.title("🍋 Lemonade Empire")

    st.write(
        "Welcome to Lemonade Empire! "
        "Build your business empire from scratch."
    )

    name_input = st.text_input(
        "Please enter your name:",
        max_chars=7
    ).strip().upper()

    st.subheader("Guidelines")

    st.markdown("""
    1. Don't run out of cash.
    2. 5 Lemons + 0.5kg Sugar = 1 Jug of Lemonade.
    3. 1 Jug = 8 Cups of Lemonade.
    4. High scores are based on maximum money accumulated.
    """)

    if st.button(
        "Start Empire",
        type="primary",
        use_container_width=True
    ):
        if name_input:
            init_game_state(name_input)
            st.rerun()
        else:
            st.warning("Please enter a name to start the game!")


# ============================================================
# MAIN GAME
# ============================================================

elif st.session_state.game_started and not st.session_state.game_over:

    # ========================================================
    # MARKETING EFFECT
    # ========================================================

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

    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.title(
        f"📊 {st.session_state.player_name}'s Status"
    )

    st.sidebar.markdown(
        f"**Day:** {st.session_state.day}"
    )

    st.sidebar.markdown(
        f"**Cash:** ${st.session_state.cash:,.2f}"
    )

    st.sidebar.markdown(
        f"**Bank Account:** ${st.session_state.account:,.2f}"
    )

    st.sidebar.markdown(
        f"**Debt:** ${st.session_state.loanAmount:,.2f}"
    )

    st.sidebar.markdown(
        f"**Locations Owned:** {st.session_state.locations}"
    )

    st.sidebar.subheader("Inventory")

    st.sidebar.markdown(
        f"🍋 **Lemons:** {st.session_state.lemons}"
    )

    st.sidebar.markdown(
        f"🍬 **Sugar:** {st.session_state.sugar:,.1f} kg"
    )

    st.sidebar.markdown(
        f"🥛 **Cups:** {st.session_state.cups}"
    )

    st.sidebar.markdown(
        f"❄️ **Coolers:** {st.session_state.coolers}"
    )

    st.sidebar.markdown(
        f"⛺ **Canopies:** {st.session_state.canopies}"
    )

    # Recipe is ALWAYS available in the sidebar
    st.sidebar.divider()
    show_recipe()

    # ========================================================
    # MAIN TITLE
    # ========================================================

    st.title(f"🍋 Day {st.session_state.day}")

    # ========================================================
    # MAIN MENU
    # ========================================================

    if st.session_state.current_screen == "main_menu":

        st.subheader("Main Menu")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🏬 Visit Market",
                use_container_width=True
            ):
                st.session_state.current_screen = "market"
                st.rerun()

            if st.button(
                "🏦 Visit Bank",
                use_container_width=True
            ):
                st.session_state.current_screen = "bank"
                st.rerun()

        with col2:

            if st.button(
                "🏢 Department Store",
                use_container_width=True
            ):
                st.session_state.current_screen = "dept_store"
                st.rerun()

            if st.button(
                "📢 Marketing Agency",
                use_container_width=True
            ):
                st.session_state.current_screen = "marketing"
                st.rerun()

        st.write("---")

        # ====================================================
        # PREPARE FOR SALES
        # ====================================================

        st.subheader("🌅 Prepare for Sales Day")

        sale_price = st.number_input(
            "Set Sale Price per Cup ($):",
            min_value=0.0,
            value=float(st.session_state.sale_price),
            step=0.05,
            key="sale_price_input"
        )

        # Save the most recently entered price immediately
        st.session_state.sale_price = sale_price

        st.caption(
            f"💾 Last price saved: ${st.session_state.sale_price:.2f}"
        )

        if st.button(
            "🚀 Open Shop & Simulate Day",
            type="primary",
            use_container_width=True
        ):

            # Simulation calculations
            if (5.85 - sale_price) < 0:
                salesDemand = 0
            else:
                salesDemand = int(
                    1.45 * (5.85 - sale_price) ** 2
                )

            demand = int(
                salesDemand
                * random.uniform(.72, 1.45)
                * st.session_state.locations
                * random.uniform(.85, 1.2)
                * (1 + st.session_state.marketingEffect / 50)
            )

            maxJugs = min(
                int(st.session_state.lemons // 5),
                int(st.session_state.sugar // 0.5)
            )

            cups_sold = min(
                min(maxJugs * 8, demand),
                st.session_state.cups
            )

            jugsMade = int((cups_sold + 7) // 8)

            st.session_state.lemons -= jugsMade * 5
            st.session_state.sugar -= jugsMade * 0.5
            st.session_state.cups -= cups_sold

            revenue = cups_sold * sale_price

            st.session_state.cash += revenue

            # Record results
            st.session_state.summary = {
                "demand": demand,
                "cups_sold": cups_sold,
                "revenue": revenue,
                "left_lemons_gone_bad": 0,
                "rent_paid": (
                    st.session_state.rent
                    * st.session_state.locations
                ),
                "wages_paid": st.session_state.wages,
                "robbed_amount": 0,
                "sugar_melted": 0.0
            }

            # =================================================
            # LEMON ROT
            # =================================================

            if st.session_state.lemons > 0:

                rot_factor = (
                    0.5
                    - 0.4
                    * (
                        st.session_state.coolers
                        / st.session_state.locations
                    )
                )

                left_lemons = int(
                    round(
                        st.session_state.lemons
                        * rot_factor
                    )
                )

                st.session_state.summary[
                    "left_lemons_gone_bad"
                ] = left_lemons

                st.session_state.lemons -= left_lemons

            # =================================================
            # RENT HIKE
            # =================================================

            rentHike = random.randint(
                min(st.session_state.day, 50),
                70
            )

            if rentHike == 50:
                st.session_state.rent += 5

            st.session_state.cash -= (
                st.session_state.rent
                * st.session_state.locations
            )

            # =================================================
            # WAGES
            # =================================================

            if st.session_state.wages > 0:
                st.session_state.cash -= st.session_state.wages

            # =================================================
            # ROBBED
            # =================================================

            if random.randint(1, 25) == 12:

                amount_robbed = int(
                    (
                        1
                        - random.uniform(0, 0.89)
                    )
                    * st.session_state.cash
                )

                st.session_state.summary[
                    "robbed_amount"
                ] = amount_robbed

                st.session_state.cash -= amount_robbed

            # =================================================
            # BANK INTEREST
            # =================================================

            if st.session_state.account > 0:
                st.session_state.account *= (
                    1 + st.session_state.savingsInterest
                )

            # =================================================
            # RAIN
            # =================================================

            if random.randint(1, 15) == 12:

                sugar_lost = round(
                    st.session_state.sugar
                    * (
                        0.5
                        - 0.5
                        * (
                            st.session_state.canopies
                            / st.session_state.locations
                        )
                    ),
                    2
                )

                st.session_state.summary[
                    "sugar_melted"
                ] = sugar_lost

                st.session_state.sugar -= sugar_lost

            # =================================================
            # LOAN
            # =================================================

            st.session_state.loanAmount *= (
                1 + st.session_state.loansInterest
            )

            if st.session_state.loanDays > 0:
                st.session_state.loanDays -= 1

            if (
                st.session_state.loanDays == 0
                and st.session_state.loan == 1
            ):

                st.session_state.loan = 0

                st.session_state.account -= (
                    st.session_state.loanAmount
                )

                st.session_state.loanAmount = 0

            # =================================================
            # MARKETING CAMPAIGNS
            # =================================================

            if st.session_state.searchEngineCampaignDays > 0:
                st.session_state.searchEngineCampaignDays -= 1

            if st.session_state.socialMediaCampaignDays > 0:
                st.session_state.socialMediaCampaignDays -= 1

            if st.session_state.radioCampaignDays > 0:
                st.session_state.radioCampaignDays -= 1

            if st.session_state.billboardCampaignDays > 0:
                st.session_state.billboardCampaignDays -= 1

            # =================================================
            # GAME OVER
            # =================================================

            if st.session_state.cash <= 0:

                st.session_state.game_over = True

            else:

                st.session_state.day += 1
                update_prices()

            st.session_state.current_screen = "day_summary"

            st.rerun()

    # ========================================================
    # DAY SUMMARY
    # ========================================================

    elif st.session_state.current_screen == "day_summary":

        st.subheader("🌅 Daily Summary")

        sum_data = st.session_state.summary

        st.write(
            f"**Demand Today:** "
            f"{sum_data['demand']} cups"
        )

        st.write(
            f"**Cups Sold:** "
            f"{sum_data['cups_sold']}"
        )

        st.success(
            f"**Revenue:** "
            f"+${sum_data['revenue']:,.2f}"
        )

        st.error(
            f"**Rent paid:** "
            f"-${sum_data['rent_paid']:,.2f}"
        )

        if sum_data["wages_paid"] > 0:

            st.error(
                f"**Wages paid:** "
                f"-${sum_data['wages_paid']:,.2f}"
            )

        if sum_data["left_lemons_gone_bad"] > 0:

            st.warning(
                f"🍋 **Lemons Rot (gone bad):** "
                f"{sum_data['left_lemons_gone_bad']} units"
            )

        if sum_data["robbed_amount"] > 0:

            st.error(
                f"🚨 **Robbed!** "
                f"Lost -${sum_data['robbed_amount']:,.2f}"
            )

        if sum_data["sugar_melted"] > 0:

            st.warning(
                f"🌧️ **Rained!** "
                f"{sum_data['sugar_melted']} kg sugar melted"
            )

        if st.button(
            "Proceed to Next Day",
            type="primary",
            use_container_width=True
        ):

            st.session_state.current_screen = "main_menu"
            st.rerun()

    # ========================================================
    # MARKET
    # ========================================================

    elif st.session_state.current_screen == "market":

        st.subheader("🏬 Market Shop")

        st.write(
            f"🍋 Lemons: ${st.session_state.lemPrice:.2f} "
            f"| 🍬 Sugar: ${st.session_state.sugPrice:.2f}/kg "
            f"| 🥛 Cups: ${st.session_state.cupPrice:.2f}"
        )

        # ====================================================
        # LEMONS
        # ====================================================

        st.markdown("### 🍋 Lemons")

        lemon_col1, lemon_col2, lemon_col3 = st.columns(3)

        lemon_1_price = round(
            st.session_state.lemPrice,
            2
        )

        lemon_5_price = round(
            5 * st.session_state.lemPrice * 0.96,
            2
        )

        lemon_20_price = round(
            20 * st.session_state.lemPrice * 0.93,
            2
        )

        with lemon_col1:

            if st.button(
                f"Buy 1 🍋\n${lemon_1_price:.2f}",
                use_container_width=True
            ):
                buy_lemons(1)

        with lemon_col2:

            if st.button(
                f"Buy 5 🍋\n${lemon_5_price:.2f} · 4% off",
                use_container_width=True
            ):
                buy_lemons(5, 0.04)

        with lemon_col3:

            if st.button(
                f"Buy 20 🍋\n${lemon_20_price:.2f} · 7% off",
                use_container_width=True
            ):
                buy_lemons(20, 0.07)

        st.write("---")

        # ====================================================
        # SUGAR
        # ====================================================

        st.markdown("### 🍬 Sugar")

        sugar_col1, sugar_col2, sugar_col3 = st.columns(3)

        sugar_1_price = round(
            st.session_state.sugPrice,
            2
        )

        sugar_5_price = round(
            5 * st.session_state.sugPrice * 0.98,
            2
        )

        sugar_20_price = round(
            20 * st.session_state.sugPrice * 0.91,
            2
        )

        with sugar_col1:

            if st.button(
                f"Buy 1kg 🍬\n${sugar_1_price:.2f}",
                use_container_width=True
            ):
                buy_sugar(1)

        with sugar_col2:

            if st.button(
                f"Buy 5kg 🍬\n${sugar_5_price:.2f} · 2% off",
                use_container_width=True
            ):
                buy_sugar(5, 0.02)

        with sugar_col3:

            if st.button(
                f"Buy 20kg 🍬\n${sugar_20_price:.2f} · 9% off",
                use_container_width=True
            ):
                buy_sugar(20, 0.09)

        st.write("---")

        # ====================================================
        # CUPS
        # ====================================================

        st.markdown("### 🥛 Cups")

        cup_col1, cup_col2, cup_col3 = st.columns(3)

        cup_1_price = round(
            st.session_state.cupPrice,
            2
        )

        cup_5_price = round(
            5 * st.session_state.cupPrice * 0.97,
            2
        )

        cup_20_price = round(
            20 * st.session_state.cupPrice * 0.92,
            2
        )

        with cup_col1:

            if st.button(
                f"Buy 1 🥛\n${cup_1_price:.2f}",
                use_container_width=True
            ):
                buy_cups(1)

        with cup_col2:

            if st.button(
                f"Buy 5 🥛\n${cup_5_price:.2f} · 3% off",
                use_container_width=True
            ):
                buy_cups(5, 0.03)

        with cup_col3:

            if st.button(
                f"Buy 20 🥛\n${cup_20_price:.2f} · 8% off",
                use_container_width=True
            ):
                buy_cups(20, 0.08)

        st.write("---")

        if st.button(
            "↩️ Back to Menu",
            use_container_width=True
        ):
            st.session_state.current_screen = "main_menu"
            st.rerun()

    # ========================================================
    # BANK
    # ========================================================

    elif st.session_state.current_screen == "bank":

        st.subheader("🏦 Lemon Bank")

        st.write(
            f"Savings Interest: "
            f"**{st.session_state.savingsInterest*100}%**"
        )

        st.write(
            f"Loan Interest: "
            f"**{st.session_state.loansInterest*100}%**"
        )

        dep_col, draw_col, loan_col = st.columns(3)

        with dep_col:

            st.markdown("**Deposit**")

            dep_amt = st.number_input(
                "Amount:",
                min_value=0.0,
                max_value=float(st.session_state.cash),
                value=0.0,
                step=1.0
            )

            if st.button(
                "Deposit Cash",
                use_container_width=True
            ):

                st.session_state.account += round(
                    dep_amt,
                    2
                )

                st.session_state.cash -= round(
                    dep_amt,
                    2
                )

                st.rerun()

        with draw_col:

            st.markdown("**Withdraw**")

            draw_amt = st.number_input(
                "Amount:",
                min_value=0.0,
                max_value=float(st.session_state.account),
                value=0.0,
                step=1.0,
                key="draw"
            )

            if st.button(
                "Withdraw Cash",
                use_container_width=True
            ):

                st.session_state.account -= round(
                    draw_amt,
                    2
                )

                st.session_state.cash += round(
                    draw_amt,
                    2
                )

                st.rerun()

        with loan_col:

            st.markdown("**Get Loan**")

            st.write(
                "Maximum credit is based on past balances."
            )

            request = st.number_input(
                "Loan Amount Requested:",
                min_value=0.0,
                value=0.0,
                step=10.0
            )

            if st.button(
                "Request 10 Day Loan",
                use_container_width=True
            ):

                if st.session_state.loan == 1:

                    st.error(
                        "Outstanding loan exists!"
                    )

                elif request > (
                    st.session_state.maxAccount
                    * 0.75
                    * 1.1
                ):

                    st.error(
                        "Request Denied! Not enough credit."
                    )

                elif request <= 0:

                    st.error(
                        "Request positive amount."
                    )

                else:

                    st.session_state.loanAmount = request
                    st.session_state.loan = 1
                    st.session_state.loanDays = 10
                    st.session_state.account += request

                    st.success(
                        "Request Approved! Funds transferred."
                    )

                    st.rerun()

        if st.button(
            "↩️ Back to Menu",
            use_container_width=True
        ):
            st.session_state.current_screen = "main_menu"
            st.rerun()

    # ========================================================
    # DEPARTMENT STORE
    # ========================================================

    elif st.session_state.current_screen == "dept_store":

        st.subheader("🏬 Department Store")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write("**Lemon Cooler**")

            st.write(
                f"Price: "
                f"${st.session_state.coolerPrice:.2f}"
            )

            if st.button(
                "Buy Cooler",
                use_container_width=True
            ):

                if (
                    st.session_state.coolers
                    < st.session_state.locations
                    and st.session_state.cash
                    >= st.session_state.coolerPrice
                ):

                    st.session_state.cash -= (
                        st.session_state.coolerPrice
                    )

                    st.session_state.coolers += 1

                    st.success(
                        "Cooler purchased!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unavailable or insufficient funds."
                    )

        with col2:

            st.write("**Lemon Stand Canopy**")

            st.write(
                f"Price: "
                f"${st.session_state.canopyPrice:.2f}"
            )

            if st.button(
                "Buy Canopy",
                use_container_width=True
            ):

                if (
                    st.session_state.canopies
                    < st.session_state.locations
                    and st.session_state.cash
                    >= st.session_state.canopyPrice
                ):

                    st.session_state.cash -= (
                        st.session_state.canopyPrice
                    )

                    st.session_state.canopies += 1

                    st.success(
                        "Canopy purchased!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unavailable or insufficient funds."
                    )

        with col3:

            st.write("**Additional Lemon Stand**")

            st.write(
                f"Price: "
                f"${st.session_state.standPrice:.2f}"
            )

            if st.button(
                "Buy Additional Stand",
                use_container_width=True
            ):

                if (
                    st.session_state.cash
                    >= st.session_state.standPrice
                ):

                    st.session_state.cash -= (
                        st.session_state.standPrice
                    )

                    st.session_state.locations += 1
                    st.session_state.wages += 5

                    st.success(
                        "Additional stand purchased!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Insufficient funds."
                    )

        if st.button(
            "↩️ Back to Menu",
            use_container_width=True
        ):
            st.session_state.current_screen = "main_menu"
            st.rerun()

    # ========================================================
    # MARKETING
    # ========================================================

    elif st.session_state.current_screen == "marketing":

        st.subheader("📢 Marketing Agency")

        st.write(
            f"Overall Effectiveness: "
            f"**{st.session_state.marketingEffect}%**"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"Internet Search (SEO): "
                f"${st.session_state.searchEnginePrice:.2f}"
            )

            if st.button(
                "Buy SEO",
                use_container_width=True
            ):

                if (
                    st.session_state.cash
                    >= st.session_state.searchEnginePrice
                ):

                    st.session_state.cash -= (
                        st.session_state.searchEnginePrice
                    )

                    st.session_state.searchEngineCampaignDays += 7

                    st.success("SEO Active!")

                    st.rerun()

                else:
                    st.error("Not enough cash!")

            st.write(
                f"Radio Ad: "
                f"${st.session_state.radioPrice:.2f}"
            )

            if st.button(
                "Buy Radio Campaign",
                use_container_width=True
            ):

                if (
                    st.session_state.cash
                    >= st.session_state.radioPrice
                ):

                    st.session_state.cash -= (
                        st.session_state.radioPrice
                    )

                    st.session_state.radioCampaignDays += 7

                    st.success("Radio Active!")

                    st.rerun()

                else:
                    st.error("Not enough cash!")

        with col2:

            st.write(
                f"Social Media Ad: "
                f"${st.session_state.socialMediaPrice:.2f}"
            )

            if st.button(
                "Buy Social Media Ads",
                use_container_width=True
            ):

                if (
                    st.session_state.cash
                    >= st.session_state.socialMediaPrice
                ):

                    st.session_state.cash -= (
                        st.session_state.socialMediaPrice
                    )

                    st.session_state.socialMediaCampaignDays += 7

                    st.success(
                        "Social Media active!"
                    )

                    st.rerun()

                else:
                    st.error("Not enough cash!")

            st.write(
                f"Billboard Ad: "
                f"${st.session_state.billboardPrice:.2f}"
            )

            if st.button(
                "Buy Billboard Ad",
                use_container_width=True
            ):

                if (
                    st.session_state.cash
                    >= st.session_state.billboardPrice
                ):

                    st.session_state.cash -= (
                        st.session_state.billboardPrice
                    )

                    st.session_state.billboardCampaignDays += 7

                    st.success(
                        "Billboard active!"
                    )

                    st.rerun()

                else:
                    st.error("Not enough cash!")

        if st.button(
            "↩️ Back to Menu",
            use_container_width=True
        ):
            st.session_state.current_screen = "main_menu"
            st.rerun()


# ============================================================
# GAME OVER
# ============================================================

elif st.session_state.game_over:

    st.title("💀 GAME OVER")

    st.error(
        f"Your empire came crumbling down "
        f"after {st.session_state.day} day(s)."
    )

    if st.button(
        "Play Again",
        type="primary",
        use_container_width=True
    ):

        st.session_state.game_started = False
        st.session_state.game_over = False

        st.rerun()
