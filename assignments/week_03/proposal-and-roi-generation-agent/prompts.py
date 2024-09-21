from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)

SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=", ".join(["FINISH", "Researcher", "Coder"]), members=", ".join(["Researcher", "Coder"]))

INPUT_PROMPT = """The goal is to generate a sales proposal for a weight loss drug that BioLama, a biotech startup, will pitch to Bausch Health, a Canadian pharmaceutical company. Additionally, you will guide the agents in calculating future ROI trends for the next 5 years, including generating a graph that visualizes the yearly ROI.
Task Overview:
Research and Proposal Generation
You can search online on different websites and gather relevant information about Bausch Health, the pharmaceutical industry, and market trends.
Generate a comprehensive sales proposal, which should include the following sections:
Executive Summary: Highlight the key points of the weight loss drug pitch and its importance for Bausch Health.
Company Overview (Bausch Health): Provide a detailed background on Bausch Health, its history, and its role in the pharmaceutical industry.
Product Description: Describe the new weight loss drug, its composition, mechanism of action, clinical benefits, and unique selling points.
Market Analysis: Research and analyze the current weight loss market, including competitor products, demand trends, and target demographics.
Marketing Strategy: Propose a marketing strategy, outlining the product's positioning, target audience, and promotional channels.
Financial Projections: Estimate production costs (e.g., R&D, manufacturing, distribution) and project sales and revenue for the next 5 years.
Conclusion: Summarize the proposal and provide a compelling closing statement to convince Bausch Health to invest.
Once the proposal is generated, use the financial data (production costs, sales projections, revenue) for ROI calculation.
ROI Calculation and Graph Generation
Initial ROI Calculation:
The agent should calculate the ROI based on the financial data using the formula:
ROI = (Net Profit / Cost of Investment) * 100 where:
Net Profit: Total revenue minus total costs (including production, R&D, marketing).
Cost of Investment: Initial production and operational costs.
Yearly ROI Trends:
The agent will calculate the yearly ROI over 5 years and account for:
Market growth rate assumptions
Potential changes in production costs and economies of scale
Discounted cash flow (DCF) analysis for a more accurate future projection
Generate Graph:
The agent will create a graph showing the projected yearly ROI trend for the next 5 years, using Python plotting libraries (e.g., Matplotlib or Plotly). This graph should visualize how the ROI evolves year over year based on different assumptions (e.g., optimistic, moderate, and conservative scenarios).
Final Report
After the agent completes the ROI calculation and graph generation, review both the proposal and the ROI analysis. Consolidate the information into a final report that includes:
A summary of the sales proposal for the weight loss drug.
A visual representation of the 5-year ROI trends, showing the potential financial outcomes of the project.
Goal:
The final deliverable should be a comprehensive report that includes:
A well-researched, structured proposal to pitch the weight loss drug to Bausch Health.
A graph that clearly illustrates the projected ROI trends over the next 5 years, providing valuable insights for decision-makers at Bausch Health.
"""