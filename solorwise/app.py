"""SolarWise: a beginner-friendly, educational Streamlit application."""

from html import escape
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st

from calculator import (
    HORIZON_YEARS, MAX_INSTALLATION_COST, MAX_MONTHLY_BILL,
    calculate_solar_savings,
)
from charts import cumulative_savings_chart, monthly_bill_chart
from content import (
    BENEFITS, COMMUNITY_SOLUTIONS, COST_FACTORS, ENERGY_HABITS, INSTAGRAM_URL,
    LIMITATIONS, MYTHS, QUIZ, SOLAR_LIMITS, SOLAR_STEPS, SOURCE_REVIEW_DATE, SOURCES,
)

ROOT = Path(__file__).parent
PAGES = ["Home", "Solar Calculator", "Clean Energy Education", "About / Methodology"]

st.set_page_config(
    page_title="SolarWise · Solar Savings & Awareness Tool",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def navigate(page: str) -> None:
    """A button callback can safely change navigation before the next rerun."""
    st.session_state["page"] = page


def money(value: float) -> str:
    return f"RM {value:,.2f}"


def source_note(*keys: str) -> None:
    links = [f"[{SOURCES[key][0]}]({SOURCES[key][1]})" for key in keys]
    st.caption("Sources: " + " · ".join(links))


def page_heading(kicker: str, title: str, description: str) -> None:
    st.html(f'<p class="eyebrow">{escape(kicker)}</p>')
    st.title(title)
    st.html(f'<p class="section-intro">{escape(description)}</p>')


def sdg_banner(title: str, text: str) -> None:
    st.html(
        '<section class="sdg-banner"><div class="sdg-number" aria-label="Goal 7">7</div>'
        f'<div><h3>{escape(title)}</h3><p>{escape(text)}</p></div></section>'
    )


def campaign_section() -> None:
    st.subheader("From your feed to a brighter future")
    st.write(
        "This tool supports our SDG 7 Instagram awareness campaign: explore a rooftop "
        "solar scenario, learn about energy access beyond cities, and choose an "
        "electricity-saving habit to share."
    )
    # Only a verified Instagram address should be enabled. There is no Instagram API.
    parsed = urlparse(INSTAGRAM_URL or "")
    valid_url = (
        parsed.scheme == "https"
        and parsed.hostname in {"instagram.com", "www.instagram.com"}
        and parsed.username is None
        and parsed.password is None
        and bool(parsed.path.strip("/"))
        and not parsed.query
        and not parsed.fragment
    )
    if valid_url:
        st.link_button("Visit Our Instagram Campaign", INSTAGRAM_URL)
        st.caption("Team-supplied campaign link. Campaign outcomes still require evidence.")
    else:
        st.button("Visit Our Instagram Campaign", disabled=True, key="instagram_placeholder")
        st.caption("Placeholder · The team's real Instagram campaign URL has not been supplied.")
    st.info(
        "Share one idea: “Explore a solar scenario. Learn about clean energy access. "
        "Try one electricity-saving habit today.” After deployment, add the real app "
        "URL to your Instagram bio or a QR code."
    )


def home_page() -> None:
    illustration = (ROOT / "assets" / "solar-neighborhood.svg").read_text(encoding="utf-8")
    st.html(
        '<section class="hero"><div><span class="pill">☀ &nbsp; Small choices. Brighter futures.</span>'
        '<h1>A little sunshine.<br><em>A smarter energy future.</em></h1>'
        '<p>Get curious about rooftop solar, explore what savings could look like, '
        'and discover how clean energy can reach more communities.</p></div>'
        f'<div>{illustration}</div></section>'
    )
    left, right = st.columns(2)
    with left:
        st.button("Explore your solar savings →", type="primary", width="stretch",
                  on_click=navigate, args=("Solar Calculator",))
    with right:
        st.button("Discover clean energy →", width="stretch",
                  on_click=navigate, args=("Clean Energy Education",))
    st.caption("Built for learning · Malaysian Ringgit scenarios · No account needed")

    st.subheader("Better energy starts with understanding.")
    st.html(
        '<div class="feature-grid">'
        '<article class="feature"><div class="number">01</div><h3>Picture the possibilities</h3>'
        '<p>Change a bill-reduction assumption and see the effect on savings and simple payback.</p></article>'
        '<article class="feature"><div class="number">02</div><h3>Look beyond your rooftop</h3>'
        '<p>Explore solar home systems, community mini-grids and other options for remote communities.</p></article>'
        '<article class="feature"><div class="number">03</div><h3>Make everyday energy count</h3>'
        '<p>Build practical electricity-saving habits and check your understanding with a five-question quiz.</p></article></div>'
    )
    sdg_banner(
        "Affordable and clean energy, for everyone.",
        "SDG 7 brings together access to reliable energy, renewable energy and energy efficiency. "
        "SolarWise connects those ideas to decisions at home and in the community.",
    )
    source_note("sdg")
    st.html(
        '<aside class="callout"><strong>A scenario, with the assumptions in view.</strong> '
        'Our calculator explores a percentage you choose. It does not predict solar output, '
        'apply an official tariff or guarantee savings.</aside>'
    )
    campaign_section()


def remember_scenario(name: str) -> None:
    st.session_state["scenario_inputs"][name] = st.session_state[f"_input_{name}"]


def reset_scenario() -> None:
    defaults = {"bill": 200.0, "cost": 12000.0, "reduction": 50}
    st.session_state["scenario_inputs"] = defaults.copy()
    for name, value in defaults.items():
        st.session_state[f"_input_{name}"] = value


def calculator_page() -> None:
    page_heading(
        "Explore a possibility", "What could solar savings look like?",
        "Adjust three inputs to explore an educational scenario. Every result follows "
        "your hypothetical bill-reduction assumption; no solar output is predicted.",
    )
    st.session_state.setdefault("scenario_inputs", {"bill": 200.0, "cost": 12000.0, "reduction": 50})
    for name, value in st.session_state["scenario_inputs"].items():
        st.session_state.setdefault(f"_input_{name}", value)

    inputs, results = st.columns([1, 1.9], gap="large")
    with inputs:
        with st.container(border=True):
            st.subheader("Your scenario")
            bill = st.number_input(
                "Monthly electricity bill (RM)", min_value=0.0, max_value=MAX_MONTHLY_BILL,
                step=10.0, format="%.2f", key="_input_bill",
                on_change=remember_scenario, args=("bill",),
                help="Your current bill, entered by you. This app does not look up a tariff.",
            )
            cost = st.number_input(
                "Estimated installation cost (RM)", min_value=0.0, max_value=MAX_INSTALLATION_COST,
                step=500.0, format="%.2f", key="_input_cost",
                on_change=remember_scenario, args=("cost",),
                help="Your own scenario input. The default is not a verified market quotation.",
            )
            reduction = st.slider(
                "Hypothetical bill reduction (%)", min_value=0, max_value=100, step=1,
                key="_input_reduction", on_change=remember_scenario, args=("reduction",),
                help="User-controlled assumption, not an engineering estimate or guaranteed reduction.",
            )
            st.caption("You control this assumption. 50% is an example, not a verified solar saving.")
            st.button("Reset to example", on_click=reset_scenario, width="stretch")
            st.caption(
                "Educational input limits: bill RM0–100,000/month; installation RM0–10,000,000. "
                "These guardrails are not market-price estimates."
            )
    try:
        scenario = calculate_solar_savings(bill, cost, reduction)
    except ValueError as error:
        st.error(str(error))
        return

    with results:
        st.subheader("Your scenario at a glance")
        row = st.columns(3)
        row[0].metric("Current monthly bill", money(scenario.monthly_bill), border=True)
        row[1].metric("Monthly bill after solar", money(scenario.new_monthly_bill), border=True)
        row[2].metric("Monthly savings", money(scenario.monthly_savings), border=True)
        row = st.columns(3)
        row[0].metric("Annual savings", money(scenario.annual_savings), border=True)
        row[1].metric("Upfront cost", money(scenario.installation_cost), border=True)
        payback = scenario.simple_payback_years
        payback_label = "N/A" if payback is None else (f"{payback:,.2f} years" if payback >= 0.01 or payback == 0 else "< 0.01 years")
        row[2].metric("Simple payback", payback_label, border=True)
        st.info(
            f"Assumptions: {money(bill)}/month starting bill · {money(cost)} upfront · "
            f"{reduction}% user-assumed bill reduction · constant savings for {HORIZON_YEARS} years. "
            "These are hypothetical inputs, not verified prices or performance."
        )
        if scenario.annual_savings == 0:
            st.warning("No savings in this scenario. Simple payback is not applicable, including when cost is zero.")
        elif payback is None:
            st.warning("The savings are too small to express a finite payback. Try a larger scenario input.")
        elif cost == 0:
            st.info("A zero-cost input gives an arithmetic payback of 0 years. It does not imply a free installation is available.")
        elif payback > HORIZON_YEARS:
            st.warning("Simple payback falls beyond the 20-year chart. The chart does not imply a system lifetime or warranty.")

    st.divider()
    st.subheader("A smaller bill, under your assumption")
    st.plotly_chart(monthly_bill_chart(scenario), width="stretch", config={"displaylogo": False, "scrollZoom": False})
    st.caption(f"Text alternative: current bill {money(bill)}/month; assumed bill after solar {money(scenario.new_monthly_bill)}/month.")
    st.subheader("Watch the scenario add up")
    st.write("Compare cumulative gross savings with the one-time upfront cost over 20 years.")
    st.plotly_chart(cumulative_savings_chart(scenario), width="stretch", config={"displaylogo": False, "scrollZoom": False})
    st.caption(
        f"At year 20: {money(scenario.annual_savings * HORIZON_YEARS)} cumulative gross savings, "
        f"versus {money(cost)} upfront cost. Gross savings start at zero and do not deduct the installation cost. "
        "The intersection, when present, is simple payback."
    )
    with st.expander("View the chart values as a table"):
        st.dataframe(
            {"Year": list(range(HORIZON_YEARS + 1)),
             "Cumulative gross savings (RM)": scenario.cumulative_savings(),
             "Upfront installation cost (RM)": [cost] * (HORIZON_YEARS + 1)},
            hide_index=True, width="stretch",
        )
    st.warning("Educational scenario only. " + LIMITATIONS)
    sdg_banner(
        "Explore savings. Think about access. Use energy wisely.",
        "A household scenario is one part of SDG 7. Affordable energy for remote communities "
        "and efficient electricity use matter alongside rooftop solar.",
    )
    st.button("Learn how clean energy works →", on_click=navigate, args=("Clean Energy Education",))


def remember_answer(index: int) -> None:
    st.session_state["quiz_answers"][index] = st.session_state[f"_quiz_{index}"]


def reset_quiz() -> None:
    st.session_state["quiz_answers"] = {}
    for index in range(len(QUIZ)):
        st.session_state.pop(f"_quiz_{index}", None)


def quiz_section() -> None:
    st.subheader("Five questions. A little more energy know-how.")
    st.write("Choose an answer for immediate feedback. You can change your choices as you learn.")
    answers = st.session_state.setdefault("quiz_answers", {})
    completed = len(answers)
    st.progress(completed / len(QUIZ), text=f"{completed} of {len(QUIZ)} answered")
    for index, question in enumerate(QUIZ):
        key = f"_quiz_{index}"
        st.session_state.setdefault(key, answers.get(index))
        with st.container(border=True):
            selection = st.radio(
                f"{index + 1}. {question['question']}", question["options"], index=None,
                key=key, on_change=remember_answer, args=(index,),
            )
            if selection is not None:
                correct_answer = question["options"][question["correct"]]
                if selection == correct_answer:
                    st.success("Correct! " + question["explanation"])
                else:
                    st.info(f"The correct answer is: {correct_answer}. {question['explanation']}")
                if question["source"]:
                    source_note(question["source"])
    if completed == len(QUIZ):
        score = sum(answers[i] == q["options"][q["correct"]] for i, q in enumerate(QUIZ))
        st.success(f"Final score: {score} / {len(QUIZ)}. Keep exploring and share one thing you learned.")
    else:
        st.caption("Answer all five questions to see your final score.")
    st.button("Try the quiz again", on_click=reset_quiz)


def education_page() -> None:
    page_heading(
        "The clean energy learning hub", "Understand the energy behind everyday life.",
        "From your rooftop to a remote community: explore the options, their limits, "
        "and the choices you can make today.",
    )
    sdg_banner(
        "What is SDG 7?",
        "The United Nations goal is access to affordable, reliable, sustainable and modern energy for all. "
        "Energy enables activities such as studying, healthcare and livelihoods. Access, renewables "
        "and efficiency all belong in the conversation.",
    )
    source_note("sdg")
    tabs = st.tabs(["Solar at home", "Energy for everyone", "Everyday actions", "Myth or fact?", "Quick quiz"])
    with tabs[0]:
        st.subheader("From sunlight to your socket")
        steps = "".join(
            f'<article class="step"><span>{number}</span><h3>{escape(title)}</h3><p>{escape(text)}</p></article>'
            for number, title, text in SOLAR_STEPS
        )
        st.html(f'<div class="step-grid">{steps}</div>')
        source_note("pv", "design")
        left, right = st.columns(2, gap="large")
        with left:
            st.subheader("Why consider rooftop solar?")
            for benefit in BENEFITS:
                st.markdown(f"- {benefit}")
        with right:
            st.subheader("What should you plan around?")
            for limitation in SOLAR_LIMITS:
                st.markdown(f"- {limitation}")
        source_note("design", "grid")
        st.subheader("What influences costs and savings?")
        for title, description in COST_FACTORS.items():
            with st.expander(title):
                st.write(description)
        st.caption("Planning questions, not a price guide. Obtain a site assessment and an itemised quotation from a qualified installer.")
        st.button("Try your own bill-reduction scenario →", on_click=navigate, args=("Solar Calculator",))
    with tabs[1]:
        st.subheader("Clean energy beyond the city")
        st.write(
            "Where extending the main grid is difficult, local systems can offer another route "
            "to electricity access. Suitability depends on resources, demand, affordability and "
            "the ability to operate and maintain the system. Communities should help shape the solution."
        )
        for number, title, subtitle, description, planning in COMMUNITY_SOLUTIONS:
            with st.container(border=True):
                st.caption(f"{number} / {subtitle}")
                st.subheader(title)
                st.write(description)
                st.info(planning)
        source_note("community", "minigrid", "hydro")
        st.subheader("And what about wind?")
        st.write(
            "Wind turbines turn moving air into electricity. A suitable wind resource, space, "
            "siting and maintenance access are important. A windy impression at street level "
            "is not a substitute for a proper site assessment."
        )
        source_note("wind")
        st.caption("These are general technology introductions. Overseas examples and guidance do not establish Malaysian regulatory approval or local project feasibility.")
    with tabs[2]:
        st.subheader("Start with the electricity you already use")
        st.write("Renewable energy and responsible consumption work together. Choose one practical habit to try this week.")
        for title, description in ENERGY_HABITS:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(description)
        source_note("habits")
        st.info("Your small action: tell a friend which habit you will try and why. Changes in a bill alone do not prove savings from that habit; weather, occupancy and tariffs can also change.")
    with tabs[3]:
        st.subheader("Let's clear up a few common ideas")
        for myth, fact, source in MYTHS:
            with st.expander(f"Myth: {myth}", expanded=True):
                st.markdown(f"**Fact:** {fact}")
                source_note(source)
    with tabs[4]:
        quiz_section()


def about_page() -> None:
    page_heading(
        "About / Methodology", "Clear purpose. Transparent assumptions.",
        "SolarWise — Solar Savings & Awareness Tool is a university Project Management "
        "educational project supporting SDG 7: Affordable and Clean Energy.",
    )
    st.subheader("Who this is for")
    st.write("University students, young adults and households curious about solar, clean energy access and responsible electricity consumption.")
    st.subheader("Three campaign goals, one learning tool")
    st.markdown(
        "1. **Explore rooftop solar adoption:** understand how it works and examine hypothetical costs, savings and payback.\n"
        "2. **Raise awareness of remote-community solutions:** introduce solar home systems, mini-grids and micro-hydro.\n"
        "3. **Encourage responsible consumption:** share practical electricity-saving habits that can reduce unnecessary grid demand."
    )
    st.subheader("How the calculator works")
    st.write("Let B be the current monthly bill in RM, C the upfront installation cost in RM, and r your hypothetical reduction percentage from 0 to 100.")
    st.latex(r"\text{Monthly savings} = B \times \frac{r}{100}")
    st.latex(r"\text{New monthly bill} = B - \text{Monthly savings}")
    st.latex(r"\text{Annual savings} = 12 \times \text{Monthly savings}")
    st.latex(r"\text{Simple payback (years)} = \frac{C}{\text{Annual savings}}\quad\text{if annual savings} > 0")
    st.latex(r"\text{Cumulative gross savings at year }t = t \times \text{Annual savings}")
    st.write(
        "With a RM200 monthly bill, RM12,000 upfront cost and a user-assumed 50% reduction: "
        "monthly savings are RM100, the new bill is RM100, annual savings are RM1,200, "
        "and simple payback is 10 years. These defaults are illustrative, not market evidence."
    )
    st.write(
        "Zero savings gives no applicable payback. Zero installation cost with positive "
        "savings gives an arithmetic payback of 0 years. The cost line is a constant reference, "
        "and the savings line shows gross savings rather than net profit. Currency is rounded "
        "only for display; the calculations use unrounded values."
    )
    st.subheader("Assumptions and limitations")
    st.warning(LIMITATIONS)
    st.write(
        "This is not a system-sizing tool, a generation forecast, a tariff calculator, "
        "an installer quotation or a guarantee. It does not calculate exported-energy credits, "
        "emissions avoided or a full investment return. The 20-year display is a comparison "
        "window, not an equipment lifetime claim."
    )
    st.caption(
        "Validation: only finite numeric inputs are accepted; negative values are rejected. "
        "The bill is capped at RM100,000/month, cost at RM10,000,000, and reduction at 100%. "
        "These are educational interface limits. Extremely small amounts can round to RM0.00; "
        "an unrepresentable finite payback is shown as N/A."
    )
    st.subheader("Evidence still to be added by the project team")
    with st.container(border=True):
        st.markdown("**Expert interview findings — placeholder / not yet supplied**")
        st.write("Add the expert's verified role and name with permission, interview date, questions, findings and limitations. No interview or expert endorsement is claimed.")
    with st.container(border=True):
        st.markdown("**Changes after expert feedback — placeholder / not yet supplied**")
        st.write("Record each specific suggestion, the corresponding change, its date and evidence of verification. Do not describe planned changes as completed results.")
    with st.container(border=True):
        st.markdown("**Instagram campaign URL and evidence — placeholder / not yet supplied**")
        st.write("Add the actual campaign URL, published app URL and dated evidence of bio links or posts. Campaign reach, engagement and impact must be supported by real evidence.")
    campaign_section()
    st.subheader("References and source scope")
    st.write(
        f"General educational references reviewed on {SOURCE_REVIEW_DATE}. These sources "
        "support the technology and SDG introductions; they do not verify the calculator's "
        "example prices or reductions, Malaysian tariffs, incentives or project outcomes. "
        "Recheck relevant sources before the public launch."
    )
    for title, url in SOURCES.values():
        st.markdown(f"**{title}**  \n{url}")
    st.subheader("Privacy and sharing")
    st.write(
        "No login, database, external analytics scripts or tracking parameters are added by this project. "
        "Inputs and quiz answers are held in the current Streamlit session; this app does not "
        "save them to a database or file. A deployed Streamlit server processes the inputs, "
        "and the hosting provider may keep normal operational logs."
    )


def main() -> None:
    st.html(f"<style>{(ROOT / 'assets' / 'style.css').read_text(encoding='utf-8')}</style>")
    st.html(
        '<header class="brand"><div class="wordmark"><span class="brand-sun" aria-hidden="true">☼</span>'
        'SolarWise<span style="color:#72905f">.</span></div>'
        '<span class="brand-caption">A brighter future starts with us</span></header>'
    )
    page = st.radio("Main navigation", PAGES, horizontal=True, key="page", label_visibility="collapsed")
    st.divider()
    {"Home": home_page, "Solar Calculator": calculator_page,
     "Clean Energy Education": education_page, "About / Methodology": about_page}[page]()
    st.html(
        '<footer class="footer"><span><strong>SolarWise.</strong> &nbsp; Solar Savings &amp; Awareness Tool</span>'
        '<span>A university SDG 7 project · Educational scenarios, informed choices.</span></footer>'
    )


if __name__ == "__main__":
    main()
