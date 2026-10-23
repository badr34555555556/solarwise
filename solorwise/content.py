"""Editable educational copy, references, quiz data and campaign placeholders."""

# Set only after the team supplies and verifies the actual campaign URL.
INSTAGRAM_URL: str | None = None
SOURCE_REVIEW_DATE = "23 October 2026"

SOURCES = {
    "sdg": (
        "United Nations — Sustainable Development Goal 7",
        "https://www.un.org/sustainabledevelopment/energy/",
    ),
    "pv": (
        "U.S. Department of Energy — Solar Photovoltaic Technology Basics",
        "https://www.energy.gov/cmei/systems/solar-photovoltaic-technology-basics",
    ),
    "design": (
        "U.S. Department of Energy — Solar Photovoltaic System Design Basics",
        "https://www.energy.gov/cmei/systems/solar-photovoltaic-system-design-basics",
    ),
    "grid": (
        "U.S. Department of Energy — Distributed Energy Resources and Microgrids Basics",
        "https://www.energy.gov/cmei/systems/solar-integration-distributed-energy-resources-and-microgrids-basics",
    ),
    "community": (
        "World Bank — Lighting Up Rural Communities in Bangladesh",
        "https://www.worldbank.org/en/results/2021/03/13/lighting-up-rural-communities-in-bangladesh-the-second-rural-electrification-and-renewable-energy-development-project",
    ),
    "minigrid": (
        "World Bank — Mini Grids for Half a Billion People: Executive Summary",
        "https://ppp.worldbank.org/sites/default/files/2021-09/Mini-Grids-for-Half-a-Billion-People-Market-Outlook-and-Handbook-for-Decision-Makers-Executive-Summary%20%28English%29.pdf",
    ),
    "wind": (
        "U.S. Department of Energy — Small Wind Guidebook",
        "https://www.energy.gov/cmei/systems/windexchange/small-wind-guidebook",
    ),
    "hydro": (
        "Government of Ontario — Micro-hydro Systems",
        "https://www.ontario.ca/page/micro-hydro-systems",
    ),
    "habits": (
        "Singapore National Environment Agency — Energy Saving Tips by Appliance",
        "https://www.nea.gov.sg/our-services/climate-change-energy-efficiency/energy-efficiency/household-sector/energy-saving-tips",
    ),
}

LIMITATIONS = (
    "Actual results depend on Malaysian electricity tariff structures, electricity "
    "consumption, location, system size, solar generation, self-consumption, installation "
    "cost, maintenance, equipment degradation, and applicable rules or incentives. "
    "SolarWise does not model these factors or verify any current tariff or incentive. "
    "The scenario holds the bill and reduction constant for 20 years. It excludes "
    "financing, discounting, inflation, tariff changes, maintenance, replacements and "
    "degradation. Simple payback is not a full financial feasibility analysis."
)

SOLAR_STEPS = [
    ("01", "Catch sunlight", "Photovoltaic (PV) panels turn sunlight into direct-current electricity."),
    ("02", "Convert the power", "An inverter changes direct current into alternating current for household appliances."),
    ("03", "Use it at home", "Electricity used while panels generate can reduce electricity bought from the grid."),
    ("04", "Plan for later", "Storage can shift energy to later hours. Grid exports depend on local rules and the system design."),
]

BENEFITS = [
    "Generate electricity at the point of use from a renewable resource.",
    "Potentially reduce grid purchases when generation matches household demand.",
    "Make energy use a more visible part of household decisions.",
]

SOLAR_LIMITS = [
    "Generation varies with sunlight, shade, orientation and weather; panels do not generate at night.",
    "Roof condition, usable space and upfront cost can limit suitability.",
    "Ordinary grid-connected solar typically shuts down in a power cut; backup needs appropriate equipment and controls.",
    "Installation quality, maintenance and eventual equipment replacement matter.",
]

COST_FACTORS = {
    "Your home and roof": "Usable area, shading, orientation, roof condition and installation access affect system design and work required.",
    "Equipment and scope": "Panel capacity, inverter choice, mounting, wiring, battery storage and warranties affect a quotation.",
    "When you use power": "Using electricity during generation hours changes how much solar electricity can be consumed directly.",
    "Local arrangements": "The applicable tariff, connection rules and any export or incentive scheme must be checked with current Malaysian authorities and a qualified installer.",
}

COMMUNITY_SOLUTIONS = [
    (
        "01", "Solar home systems", "A household-scale starting point",
        "A standalone solar panel, controller and often a battery can supply selected household loads such as lighting and phone charging. Capacity limits what can run at once.",
        "Plan for battery care, repair access, replacement costs and the household's actual needs.",
    ),
    (
        "02", "Community mini-grids", "Shared generation, local connections",
        "A mini-grid distributes locally generated electricity to several users. It may combine solar, storage and other sources to serve homes, schools or small businesses.",
        "Community participation, fair payment arrangements, trained operators and long-term maintenance are essential planning questions.",
    ),
    (
        "03", "Micro-hydro", "Power from a suitable water resource",
        "Moving water drives a turbine. Available output depends on water flow and the vertical drop, called head; seasonal changes affect suitability.",
        "Assess water rights, ecological effects, civil works and maintenance. A nearby stream alone does not establish feasibility.",
    ),
]

ENERGY_HABITS = [
    ("Cool thoughtfully", "Use fans where comfortable, avoid unnecessary overcooling, close doors when cooling a room, and maintain filters."),
    ("Light only what you need", "Switch off unused lights, use daylight when practical and choose efficient lighting when replacing bulbs."),
    ("Cut avoidable standby use", "Switch off suitable unused devices at the socket. Keep essential medical, safety and food-storage equipment powered."),
    ("Use appliances well", "Run appropriate full laundry loads, air-dry where possible and avoid overcooling the refrigerator."),
    ("Notice your own patterns", "Review bills and appliance energy labels. Choose one habit to try, then compare your use over time."),
]

MYTHS = [
    ("Solar panels work only on hot days.", "Panels use sunlight rather than heat. Cloud and shade can reduce output; temperature also affects performance.", "pv"),
    ("Every home gets the same savings.", "Savings depend on the system, consumption pattern and billing arrangements. A percentage chosen in this tool is only an assumption.", "design"),
    ("Rooftop solar always keeps a house powered during a blackout.", "Typical grid-connected systems disconnect during a grid outage. Backup operation needs a suitable design and controls.", "grid"),
    ("Clean energy means only rooftop solar.", "Options include solar home systems, shared mini-grids, wind and suitable micro-hydro. The right choice depends on local conditions.", "community"),
]

QUIZ = [
    {
        "question": "What is the main aim of SDG 7?",
        "options": ["Free electricity for every appliance", "Affordable, reliable, sustainable and modern energy for all", "Replacing every energy source with rooftop solar"],
        "correct": 1,
        "explanation": "SDG 7 connects energy access, renewable energy and energy efficiency.",
        "source": "sdg",
    },
    {
        "question": "What do photovoltaic panels convert into electricity?",
        "options": ["Sunlight", "Heat stored in the roof", "Electricity already bought from the grid"],
        "correct": 0,
        "explanation": "PV cells convert sunlight into electricity; an inverter makes it usable by typical household appliances.",
        "source": "pv",
    },
    {
        "question": "Which option can share locally generated power across a remote community?",
        "options": ["A phone charger alone", "A community mini-grid", "A higher electricity bill"],
        "correct": 1,
        "explanation": "A mini-grid connects multiple local users to a shared electricity supply.",
        "source": "minigrid",
    },
    {
        "question": "Which habit can reduce unnecessary electricity use?",
        "options": ["Leave lights on in empty rooms", "Keep windows open while air conditioning", "Switch off unused lights and suitable idle devices"],
        "correct": 2,
        "explanation": "Avoiding unnecessary lighting and standby consumption is a practical efficiency step.",
        "source": "habits",
    },
    {
        "question": "What does choosing a 50% reduction in SolarWise mean?",
        "options": ["An installer has guaranteed the savings", "An official tariff has been applied", "You are exploring a hypothetical bill-reduction scenario"],
        "correct": 2,
        "explanation": "The calculator applies your assumption to your bill. It does not predict solar generation or verify a tariff.",
        "source": None,
    },
]
