# SolarWise — Solar Savings & Awareness Tool

A Python 3.12+ and Streamlit educational app for a university Project Management assignment supporting **SDG 7: Affordable and Clean Energy**. Designed for students, young adults and households, including visitors arriving from an Instagram bio link or QR code.

## What it includes

- A responsive green, yellow and neutral interface with four pages: Home, Solar Calculator, Clean Energy Education, and About / Methodology.
- A user-controlled hypothetical bill reduction, RM results, simple payback, and interactive Plotly bill-comparison and 20-year cumulative-gross-savings charts. A table and text alternatives accompany the charts.
- Introductions to rooftop solar, solar home systems, mini-grids, wind, micro-hydro, responsible electricity use, and solar myths.
- A five-question quiz with immediate explanations, a final score and retry. Inputs and quiz answers survive page changes within the session.
- Transparent formulas, limitations, linked general educational references and clearly labeled project-evidence placeholders.
- No accounts, database, API keys, paid services, external images, custom tracking scripts or added tracking parameters. Streamlit usage statistics are disabled in project configuration.

## Windows / VS Code setup using uv

1. Install Python **3.12 or newer**, VS Code and its Python extension. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed. Python 3.12 is the recommended deployment version for this project.
2. Open this project folder in VS Code. Open **Terminal → New Terminal** using PowerShell.
3. Run:

```powershell
uv sync
uv run streamlit run app.py
```

Open the **Local URL printed by Streamlit** (normally `http://localhost:8501`). If that port is occupied, use the URL it actually prints, or choose a different port:

```powershell
uv run streamlit run app.py --server.port 8502
```

No virtual-environment activation is required with `uv run`. In VS Code, use **Python: Select Interpreter** and choose `.venv\Scripts\python.exe` for editor support. Stop the server with **Ctrl+C** in its terminal. Do not double-click `app.py` or run it with ordinary `python app.py`; Streamlit needs its runner.

`uv sync` installs runtime and development dependencies using `uv.lock`. `uv sync --locked` checks that the lock agrees with `pyproject.toml`. To require an already installed interpreter without downloads, use `uv sync --python 3.12 --no-python-downloads`.

### Without uv

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The pip route does not install pytest; add it with `.\.venv\Scripts\python.exe -m pip install "pytest>=8.4,<10"` if you want to run tests. Paths in these commands avoid PowerShell activation-policy changes.

## Testing and verification

```powershell
uv run pytest -q
```

`tests/test_calculator.py` checks normal and fractional inputs, zero savings, zero cost, 100% reduction, gross cumulative savings, negative and out-of-range inputs, NaN/infinity, non-numeric values and numeric extremes.

`tests/test_app.py` uses Streamlit's official `AppTest` to exercise navigation, default metrics, zero-value scenarios, retained inputs, quiz feedback, changing answers, final scores and resetting the quiz. AppTest checks application behavior; it does not replace browser checks of visual appearance.

For a server smoke check, run the app and visit the printed URL. The `/_stcore/health` path on the same server should return `ok`. A health response alone does not execute every page; the AppTest workflows provide that additional check.

Before sharing, also manually check at a narrow phone width: navigation wraps, controls can be operated, chart labels are readable, all quiz answers work, and the disabled Instagram button explains what is missing.

### Verification performed on 23 October 2026

- Python 3.12.10, Streamlit 1.66.1 and Plotly 6.9.0 installed in the project's `.venv` with uv.
- `pytest -q`: **46 passed**, including calculator unit tests and Streamlit AppTest workflows.
- Locked dependency synchronization and Python compilation completed successfully.
- Streamlit started at `http://127.0.0.1:8501`; `/` returned HTTP 200 and `/_stcore/health` returned HTTP 200 with `ok`. The verification server was stopped after the checks; use the run command above to restart it.
- Browser automation was unavailable in the build session. Visual appearance at desktop and phone widths still needs a browser review. No public deployment was performed.

## Calculator methodology

Let `B` be the monthly bill in RM, `C` the upfront installation cost in RM and `r` the user-assumed reduction percentage:

```text
monthly_savings       = B * r / 100
new_monthly_bill      = B - monthly_savings
annual_savings        = monthly_savings * 12
simple_payback_years  = C / annual_savings, if annual_savings > 0
cumulative_savings(t) = annual_savings * t
```

If annual savings are zero, payback is **N/A**, including when cost is zero. With positive savings and zero cost, arithmetic payback is **0 years**, not a claim that a free installation is available. A payback beyond 20 years remains visible in the results but falls outside the chart. Extremely small values may round to RM0.00 or produce no representable finite payback; these do not produce an infinite metric.

The example `B=200`, `C=12000`, `r=50` gives RM100 monthly savings, RM100 remaining monthly bill, RM1,200 annual savings and 10-year simple payback. **The defaults are illustrative inputs, not verified installation prices or savings estimates.**

Input guardrails: finite numeric values only; monthly bill RM0–100,000; installation cost RM0–10,000,000; assumed reduction 0–100%. These limits are interface safeguards, not market evidence. Calculations use unrounded floats; displayed currency uses two decimal places. The graph starts at year 0 and ends at year 20. Gross savings do not subtract the installation cost; the dashed cost line is a comparison reference. The horizon is not a system-lifetime claim.

### Material limitations

This is a **scenario-based educational calculation**, not a solar-output prediction, tariff calculator, system-sizing tool, quotation, guaranteed saving or full financial feasibility analysis. It does not apply official Malaysian tariff rates or incentives.

Actual results depend on Malaysian tariff structures, energy consumption, location, system size, solar generation, self-consumption, installation costs, maintenance, degradation and applicable rules or incentives. The model holds savings constant and excludes financing, discounting, inflation, changing tariffs, maintenance, equipment replacement, degradation, export credits and taxes. It does not estimate emissions avoided.

General educational references are listed with plain URLs on the About page and maintained in `content.py`. Overseas sources explain technologies; they do not verify Malaysian rules, installation suitability or campaign outcomes. Source links were reviewed on 23 October 2026; the team should review them again before public launch. No expert review is claimed.

## Deploy to Streamlit Community Cloud

The source is prepared for deployment; **no public deployment or external-account change is performed by this project setup**. Publishing is a team action requiring approval and the team's accounts.

1. Run the tests and review the content and evidence checklist below.
2. Create a GitHub repository and upload/commit the project files, including `app.py`, `calculator.py`, `charts.py`, `content.py`, `assets/`, `.streamlit/config.toml`, `pyproject.toml`, `uv.lock` and `requirements.txt`. Do not upload `.venv`, `.uv-cache`, logs or secrets; `.gitignore` covers these.
3. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/), connect your GitHub account and choose **Create app**. Select the repository and branch; set the entrypoint to `app.py` (or its repository-relative path if nested).
4. In advanced settings choose **Python 3.12**. No secrets or API keys are required. Confirm the app's audience before deploying.
5. Deploy and inspect the build logs. This repository supplies a uv lockfile and a pinned pip requirements export; Cloud currently gives `uv.lock` precedence in the same directory, so the full repository uses uv. Keep both in sync. Cloud recommends a single deployment dependency specification: for a pip-only deployment copy, include `requirements.txt` and omit `uv.lock` and `pyproject.toml` from that copy.
6. Open the actual URL returned by Cloud and repeat calculator, navigation, quiz and phone-width checks. Only then put that real URL in the Instagram bio or encode it into a QR code. Test the QR code on a phone and preserve dated evidence for the assignment.

Cloud documentation: [Deploy an app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [App dependencies and file precedence](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies). Hosting interfaces and supported Python versions can change; consult those instructions when deploying.

After changing dependencies:

```powershell
uv lock
uv sync
uv export --no-dev --no-hashes --no-emit-project --format requirements.txt --output-file requirements.txt
uv run pytest -q
```

`requirements.txt` contains the locked runtime dependencies; pytest remains in the uv development group.

## Required team input and human verification

- **Expert interview findings:** obtain permission where appropriate, then add the verified interviewee details, role, date, questions, findings and limitations in `app.py`'s About page. Nothing is invented on the team's behalf.
- **Changes after expert feedback:** replace that separate placeholder with specific implemented changes and dated evidence. Planned changes are not results.
- **Instagram URL:** set `INSTAGRAM_URL` in `content.py` to the real, verified `https://www.instagram.com/<campaign>/` address, without query/tracking parameters. Until then the campaign button stays disabled. Setting a link does not prove campaign integration, reach or impact.
- **Actual published app URL and Instagram evidence:** after approved deployment, document the real bio/post links, QR-code checks, screenshots and dates. No engagement numbers are fabricated.
- **Local accuracy:** verify current Malaysian connection/export rules, tariff arrangements, incentives, installer quotations and suitability with appropriate current authorities and qualified professionals before making real purchasing decisions. These are not inputs automatically fetched by the tool.
- **Final public review:** review content, reference links, accessibility, mobile layout, hosting privacy and all claims before sharing.

## Project structure

```text
SolarWise/
  app.py                       # Four pages, navigation, inputs and quiz UI
  calculator.py                # Validated pure calculations
  charts.py                    # Plotly chart builders
  content.py                   # Education, quiz, sources, campaign URL
  assets/
    style.css                  # Responsive styles, local system fonts
    solar-neighborhood.svg     # Original local illustration
  tests/
    test_calculator.py
    test_app.py
  .streamlit/
    config.toml                # Theme and disabled usage statistics
  .python-version
  .gitignore
  pyproject.toml
  uv.lock
  requirements.txt
  README.md
```

No build step or database is needed. Edit educational text and quiz questions in `content.py`, page layout in `app.py`, calculation rules in `calculator.py`, charts in `charts.py`, and visual styles in `assets/style.css`.

## Privacy

The app keeps inputs and quiz choices only in the current Streamlit session and does not write them to a database or file. A deployed Streamlit server necessarily processes those inputs; a hosting provider can retain operational logs. The project adds no external analytics or tracking scripts. Reference links lead to third-party sites, whose policies are separate.
