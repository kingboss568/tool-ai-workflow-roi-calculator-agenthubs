# -*- coding: utf-8 -*-
"""26 functional calculators. Each renders a working page driven by app.js."""
from shell import (icon, ad_unit, app_page, page_head_block, site_config_script,
                   prefix_for, breadcrumb)

LIMITS = [
    "Outputs are planning estimates, not accounting, tax, or audited financial figures.",
    "Results depend entirely on the inputs you provide — confirm rates, prices, and adoption with your own data.",
    "All math runs in your browser. Nothing is uploaded; saved scenarios live in this device's local storage.",
]

# helper constructors -------------------------------------------------------
def F(id, label, default, hint="", money=False, step="any", wide=False, type="number", options=None):
    d = {"id": id, "label": label, "default": default, "type": type, "step": step, "min": 0}
    if hint: d["hint"] = hint
    if money: d["money"] = True
    if wide: d["wide"] = True
    if options: d["options"] = options
    return d

def O(label, expr, fmt="money", hero=False, chart=False, unit=None):
    o = {"label": label, "expr": expr, "format": fmt}
    if hero: o["hero"] = True
    if chart: o["chart"] = True
    if unit: o["unit"] = unit
    return o

# Each calc: slug,title,tagline,category,icon,fields,outputs,rules,advice,formula(plain+html),about,custom_faq
CALCS = []
def add(**kw): CALCS.append(kw)

add(slug="ai-workflow-roi", title="AI Workflow ROI Calculator", icon="calc",
    tagline="Turn hours saved, run volume, and tool cost into monthly net value, ROI, and annual return.",
    category="ROI & Payback",
    fields=[F("hoursSaved","Hours saved per run",1.4,"Time an automation removes each time it runs",step="0.1"),
            F("runs","Runs per month",120,"How many times the workflow runs"),
            F("hourlyRate","Loaded hourly value",55,"Fully-loaded cost of the person's time",money=True),
            F("toolCost","Monthly tool cost",180,"Subscription + usage for the AI tool",money=True)],
    outputs=[O("Net monthly value","hoursSaved*runs*hourlyRate - toolCost",hero=True,chart=True),
             O("Gross monthly value","hoursSaved*runs*hourlyRate",chart=True),
             O("Monthly tool cost","toolCost",chart=True),
             O("Return on investment","toolCost ? ((hoursSaved*runs*hourlyRate - toolCost)/toolCost)*100 : 0","percent"),
             O("Annual net value","(hoursSaved*runs*hourlyRate - toolCost)*12"),
             O("Hours reclaimed / mo","hoursSaved*runs","hours")],
    rules=[("hoursSaved*runs*hourlyRate < toolCost","The tool currently costs more than the time it saves — raise run volume, hours saved, or lower the plan tier."),
           ("((hoursSaved*runs*hourlyRate - toolCost)/(toolCost||1))*100 >= 300","Strong ROI above 300%. Document the assumptions so finance can validate the case.")],
    advice="Positive net value: the time reclaimed outweighs the tool cost at these volumes.",
    formula_plain="Net value = (hours saved × runs × hourly value) − tool cost.",
    formula="<b>Net value</b> = (hours saved × runs × loaded hourly value) − monthly tool cost",
    about="<p>The ROI of an AI workflow is the value of the time it gives back minus what the tool costs to run. This calculator multiplies the hours each run saves by how often it runs and by the loaded hourly value of the people involved, then subtracts the monthly subscription and usage fees.</p><p>Use the loaded hourly value — salary plus benefits, overhead, and tooling — rather than the raw wage, because that is the real cost of the time you are reclaiming. The annual figure simply extends the monthly net across twelve months and is the number most business cases lead with.</p>")

add(slug="llm-token-cost", title="LLM Token Cost Calculator", icon="coins",
    tagline="Estimate monthly spend from input/output tokens, request volume, and per-million pricing.",
    category="Token & API Cost",
    fields=[F("inputTokens","Input tokens / request",1200,"Prompt + context size"),
            F("outputTokens","Output tokens / request",800,"Generated completion size"),
            F("requests","Requests / month",5000),
            F("inputPrice","Input price (per 1M)",3,"USD per 1M input tokens",money=True),
            F("outputPrice","Output price (per 1M)",15,"USD per 1M output tokens",money=True)],
    outputs=[O("Total monthly cost","requests*((inputTokens/1000000)*inputPrice + (outputTokens/1000000)*outputPrice)",hero=True,chart=True),
             O("Input cost","requests*(inputTokens/1000000)*inputPrice",chart=True),
             O("Output cost","requests*(outputTokens/1000000)*outputPrice",chart=True),
             O("Cost per request","(inputTokens/1000000)*inputPrice + (outputTokens/1000000)*outputPrice","number",unit="USD"),
             O("Total tokens / mo","requests*(inputTokens+outputTokens)","integer"),
             O("Annual cost","requests*((inputTokens/1000000)*inputPrice + (outputTokens/1000000)*outputPrice)*12")],
    rules=[("(outputTokens/1000000)*outputPrice > (inputTokens/1000000)*inputPrice*2","Output tokens dominate your bill — tightening response length is the fastest lever."),],
    advice="Token spend scales linearly with volume. Trimming prompt size and capping output length both reduce cost.",
    formula_plain="Cost = requests × (input tokens ÷ 1M × input price + output tokens ÷ 1M × output price).",
    formula="<b>Cost</b> = requests × ( input÷1,000,000 × in-price + output÷1,000,000 × out-price )",
    about="<p>Large-language-model APIs bill per token, usually quoted per one million tokens and split into a cheaper input rate and a more expensive output rate. To forecast spend you need four things: typical prompt size, typical response size, monthly request volume, and the two prices.</p><p>Because output tokens are frequently 3–5× the price of input tokens, response length is often the single biggest driver of cost. This calculator separates the two so you can see exactly where the money goes before you commit to a model.</p>")

add(slug="api-cost-comparison", title="LLM API Cost Comparison", icon="scale",
    tagline="Compare two model providers on identical traffic and see the monthly and annual difference.",
    category="Token & API Cost",
    fields=[F("monthlyRequests","Requests / month",20000),
            F("avgInput","Avg input tokens",1500),
            F("avgOutput","Avg output tokens",700),
            F("priceAin","Provider A input (/1M)",2.5,money=True),
            F("priceAout","Provider A output (/1M)",10,money=True),
            F("priceBin","Provider B input (/1M)",3,money=True),
            F("priceBout","Provider B output (/1M)",15,money=True)],
    outputs=[O("Provider A monthly cost","monthlyRequests*((avgInput/1000000)*priceAin+(avgOutput/1000000)*priceAout)",hero=True,chart=True),
             O("Provider B monthly cost","monthlyRequests*((avgInput/1000000)*priceBin+(avgOutput/1000000)*priceBout)",chart=True),
             O("Monthly difference","abs(monthlyRequests*((avgInput/1000000)*priceBin+(avgOutput/1000000)*priceBout) - monthlyRequests*((avgInput/1000000)*priceAin+(avgOutput/1000000)*priceAout))"),
             O("Annual difference","abs(monthlyRequests*((avgInput/1000000)*priceBin+(avgOutput/1000000)*priceBout) - monthlyRequests*((avgInput/1000000)*priceAin+(avgOutput/1000000)*priceAout))*12")],
    rules=[("monthlyRequests*((avgInput/1000000)*priceAin+(avgOutput/1000000)*priceAout) < monthlyRequests*((avgInput/1000000)*priceBin+(avgOutput/1000000)*priceBout)","Provider A is cheaper at this traffic mix. Re-check if your input/output ratio changes."),
           ("monthlyRequests*((avgInput/1000000)*priceAin+(avgOutput/1000000)*priceAout) > monthlyRequests*((avgInput/1000000)*priceBin+(avgOutput/1000000)*priceBout)","Provider B is cheaper at this traffic mix. Confirm quality is comparable before switching.")],
    advice="Costs are close — small changes in prompt size or output length can flip which provider is cheaper.",
    formula_plain="Cost = requests × (input÷1M × in-price + output÷1M × out-price), compared for each provider.",
    formula="<b>Δ</b> = | costB − costA |, where each cost = requests × (in÷1M × in-price + out÷1M × out-price)",
    about="<p>Switching model providers can cut your bill significantly, but list prices alone are misleading because input and output rates differ. The honest comparison runs your real traffic — the same request volume and token mix — through both pricing tables.</p><p>This tool does exactly that and surfaces the monthly and annualised gap. Always pair the cost delta with a quality check: the cheaper model only wins if it meets your accuracy and latency bar.</p>")

add(slug="automation-savings", title="Automation Time-Savings Calculator", icon="clock",
    tagline="Convert repetitive task volume and automation coverage into reclaimed hours and dollar value.",
    category="ROI & Payback",
    fields=[F("tasksPerWeek","Tasks / week",40),
            F("minutesPerTask","Minutes per task",12),
            F("automationRate","Automation coverage %",70,"Share of the task the AI handles"),
            F("hourlyRate","Loaded hourly value",45,money=True)],
    outputs=[O("Weekly hours saved","tasksPerWeek*minutesPerTask/60*(automationRate/100)",hero=True,fmt="hours"),
             O("Weekly value","tasksPerWeek*minutesPerTask/60*(automationRate/100)*hourlyRate",chart=True),
             O("Annual value","tasksPerWeek*minutesPerTask/60*(automationRate/100)*hourlyRate*52",chart=True),
             O("Annual hours saved","tasksPerWeek*minutesPerTask/60*(automationRate/100)*52","hours")],
    advice="Reclaimed hours are most valuable when redirected to higher-leverage work, not just removed.",
    formula_plain="Hours saved = tasks/week × minutes/task ÷ 60 × automation coverage.",
    formula="<b>Weekly hours</b> = tasks × minutes ÷ 60 × (coverage% ÷ 100)",
    about="<p>Automation rarely removes 100% of a task — there is review, exception handling, and setup. Coverage percentage captures the realistic share the AI takes over, which keeps the estimate honest.</p><p>Multiplying reclaimed hours by a loaded hourly value translates time into money your finance team understands. The annual view is what justifies the subscription.</p>")

add(slug="break-even", title="AI Break-Even Calculator", icon="trend",
    tagline="Find how many months it takes for ongoing benefit to cover your upfront AI investment.",
    category="ROI & Payback",
    fields=[F("fixedCost","Upfront / setup cost",5000,"One-time build, integration, training",money=True),
            F("monthlyBenefit","Monthly benefit",1800,"Value created each month",money=True),
            F("monthlySubscription","Monthly running cost",400,money=True)],
    outputs=[O("Break-even point","(monthlyBenefit-monthlySubscription) > 0 ? fixedCost/(monthlyBenefit-monthlySubscription) : 0",hero=True,fmt="months"),
             O("Net monthly benefit","monthlyBenefit-monthlySubscription",chart=True),
             O("Monthly running cost","monthlySubscription",chart=True),
             O("Year-1 net","(monthlyBenefit-monthlySubscription)*12 - fixedCost"),
             O("Upfront cost","fixedCost")],
    rules=[("monthlyBenefit-monthlySubscription <= 0","Running cost exceeds monthly benefit — the project never breaks even at these numbers."),],
    advice="A break-even under 12 months is typically an easy approval; under 6 months is exceptional.",
    formula_plain="Break-even months = upfront cost ÷ (monthly benefit − monthly running cost).",
    formula="<b>Months</b> = upfront ÷ (monthly benefit − monthly running cost)",
    about="<p>Break-even analysis answers the first question every approver asks: when does this pay for itself? It divides the one-time investment by the net monthly benefit — the recurring value minus the recurring cost.</p><p>If the net monthly benefit is zero or negative, there is no break-even and the project loses money indefinitely; the tool flags that case so you catch it early.</p>")

add(slug="payback-period", title="AI Payback Period Calculator", icon="clock",
    tagline="Calculate payback months and first-year ROI for any AI investment.",
    category="ROI & Payback",
    fields=[F("investment","Total investment",12000,money=True),
            F("monthlyReturn","Monthly return",2500,money=True),
            F("monthlyCost","Monthly running cost",600,money=True)],
    outputs=[O("Payback period","(monthlyReturn-monthlyCost) > 0 ? investment/(monthlyReturn-monthlyCost) : 0",hero=True,fmt="months"),
             O("Net monthly return","monthlyReturn-monthlyCost",chart=True),
             O("Annual net return","(monthlyReturn-monthlyCost)*12",chart=True),
             O("First-year ROI","investment ? (((monthlyReturn-monthlyCost)*12 - investment)/investment)*100 : 0","percent")],
    advice="Payback period pairs well with break-even — use both when presenting to finance.",
    formula_plain="Payback months = investment ÷ (monthly return − monthly running cost).",
    formula="<b>Payback</b> = investment ÷ (monthly return − monthly running cost)",
    about="<p>Payback period is the time for cumulative net returns to repay the initial investment. It is the simplest capital-budgeting metric and the one non-financial stakeholders grasp instantly.</p><p>First-year ROI complements it by showing the percentage return after twelve months, so a fast payback with thin ongoing margins doesn't look better than it is.</p>")

add(slug="chatbot-deflection", title="Chatbot Deflection Savings", icon="bot",
    tagline="Model support cost avoided when an AI assistant deflects a share of incoming tickets.",
    category="ROI & Payback",
    fields=[F("monthlyTickets","Tickets / month",8000),
            F("deflectionRate","Deflection rate %",35,"Share resolved without an agent"),
            F("costPerTicket","Cost per human ticket",6,money=True),
            F("botCost","Monthly bot cost",900,money=True)],
    outputs=[O("Net monthly savings","monthlyTickets*(deflectionRate/100)*costPerTicket - botCost",hero=True,chart=True),
             O("Gross savings","monthlyTickets*(deflectionRate/100)*costPerTicket",chart=True),
             O("Monthly bot cost","botCost",chart=True),
             O("Tickets deflected","monthlyTickets*(deflectionRate/100)","integer"),
             O("Annual net savings","(monthlyTickets*(deflectionRate/100)*costPerTicket - botCost)*12")],
    rules=[("monthlyTickets*(deflectionRate/100)*costPerTicket < botCost","Deflection volume doesn't yet cover the bot's cost — raise deflection rate or ticket volume."),],
    advice="Deflection rates above 30% are achievable for FAQ-heavy queues with good content.",
    formula_plain="Savings = tickets × deflection% × cost per ticket − bot cost.",
    formula="<b>Net savings</b> = tickets × (deflection% ÷ 100) × cost/ticket − bot cost",
    about="<p>Conversational AI saves money by resolving routine questions before they reach a human agent. The value is the number of deflected tickets multiplied by what each human-handled ticket costs, minus the platform fee.</p><p>Be realistic about deflection rate: it depends heavily on knowledge-base quality and query mix. Measure it from a pilot rather than guessing.</p>")

add(slug="content-generation-roi", title="Content Generation ROI", icon="doc",
    tagline="Compare manual vs AI-assisted content production cost and time per month.",
    category="ROI & Payback",
    fields=[F("piecesPerMonth","Pieces / month",60),
            F("hoursPerPieceManual","Hours/piece — manual",3,step="0.1"),
            F("hoursPerPieceAI","Hours/piece — AI-assisted",0.8,step="0.1"),
            F("hourlyRate","Loaded hourly value",40,money=True),
            F("toolCost","Monthly tool cost",120,money=True)],
    outputs=[O("Net monthly value","piecesPerMonth*(hoursPerPieceManual-hoursPerPieceAI)*hourlyRate - toolCost",hero=True,chart=True),
             O("Gross time value","piecesPerMonth*(hoursPerPieceManual-hoursPerPieceAI)*hourlyRate",chart=True),
             O("Monthly tool cost","toolCost",chart=True),
             O("Hours saved / mo","piecesPerMonth*(hoursPerPieceManual-hoursPerPieceAI)","hours"),
             O("Cost per piece (AI)","hoursPerPieceAI*hourlyRate + toolCost/(piecesPerMonth||1)","number",unit="USD")],
    advice="AI-assisted drafting still needs human editing — keep the AI hours estimate realistic.",
    formula_plain="Net value = pieces × (manual hours − AI hours) × hourly value − tool cost.",
    formula="<b>Net value</b> = pieces × (manualHrs − aiHrs) × hourly value − tool cost",
    about="<p>AI shifts content work from drafting to editing, lowering hours per piece rather than eliminating them. The saving is the per-piece time delta multiplied by volume and hourly value.</p><p>The cost-per-piece output is useful for pricing or budgeting: it blends the AI editing time with the amortised tool fee.</p>")

add(slug="support-automation-roi", title="Support Automation ROI", icon="users",
    tagline="Estimate savings when AI handles a share of your support volume across the team.",
    category="ROI & Payback",
    fields=[F("agents","Support agents",12),
            F("ticketsPerAgentDay","Tickets / agent / day",45),
            F("workingDays","Working days / month",22),
            F("aiHandleRate","AI handle rate %",30),
            F("costPerTicketHuman","Human cost / ticket",5,money=True),
            F("aiCostPerTicket","AI cost / ticket",0.4,money=True)],
    outputs=[O("Monthly savings","agents*ticketsPerAgentDay*workingDays*(aiHandleRate/100)*(costPerTicketHuman-aiCostPerTicket)",hero=True,chart=True),
             O("Human cost avoided","agents*ticketsPerAgentDay*workingDays*(aiHandleRate/100)*costPerTicketHuman",chart=True),
             O("AI handling cost","agents*ticketsPerAgentDay*workingDays*(aiHandleRate/100)*aiCostPerTicket",chart=True),
             O("AI-handled tickets","agents*ticketsPerAgentDay*workingDays*(aiHandleRate/100)","integer"),
             O("Annual savings","agents*ticketsPerAgentDay*workingDays*(aiHandleRate/100)*(costPerTicketHuman-aiCostPerTicket)*12")],
    advice="Pair automation savings with a quality-of-service check so deflection doesn't hurt CSAT.",
    formula_plain="Savings = total tickets × AI handle% × (human cost − AI cost) per ticket.",
    formula="<b>Savings</b> = agents × tickets/day × days × handle% × (humanCost − aiCost)",
    about="<p>Scaling the per-ticket economics across a whole team shows the real operating impact of support automation. The model multiplies total monthly ticket volume by the AI handle rate, then by the cost gap between human and AI handling.</p><p>Keep the AI cost-per-ticket inclusive of platform fees and token costs so the comparison is fair.</p>")

add(slug="meeting-cost", title="Meeting Cost Calculator", icon="users",
    tagline="Price the real cost of recurring meetings so you know what AI summaries are worth replacing.",
    category="Workforce & Planning",
    fields=[F("attendees","Attendees",6),
            F("durationHours","Duration (hours)",1,step="0.25"),
            F("meetingsPerWeek","Meetings / week",5),
            F("avgHourlyRate","Avg loaded hourly rate",50,money=True)],
    outputs=[O("Cost per meeting","attendees*durationHours*avgHourlyRate",hero=True,chart=True),
             O("Weekly cost","attendees*durationHours*avgHourlyRate*meetingsPerWeek",chart=True),
             O("Annual cost","attendees*durationHours*avgHourlyRate*meetingsPerWeek*52",chart=True),
             O("Person-hours / week","attendees*durationHours*meetingsPerWeek","hours")],
    advice="If AI notes let you cut attendees or duration by 20%, apply that and recompute the saving.",
    formula_plain="Meeting cost = attendees × duration × hourly rate.",
    formula="<b>Cost</b> = attendees × duration (hrs) × loaded hourly rate",
    about="<p>Meetings are an invisible payroll line. Multiplying attendee count by duration and a loaded hourly rate exposes the true recurring cost, which is often surprising for standing weekly meetings.</p><p>Use this number as the baseline when evaluating AI note-takers or async alternatives — the saving is whatever attendee-hours you remove.</p>")

add(slug="developer-productivity", title="Developer Productivity ROI", icon="rocket",
    tagline="Value an AI coding assistant from team size, salary, and measured productivity uplift.",
    category="ROI & Payback",
    fields=[F("developers","Developers",10),
            F("avgSalary","Avg loaded salary / yr",110000,money=True),
            F("uplift","Productivity uplift %",15),
            F("seatCost","Seat cost / dev / mo",20,money=True)],
    outputs=[O("Annual net value","developers*avgSalary*(uplift/100) - developers*seatCost*12",hero=True,chart=True),
             O("Productivity value","developers*avgSalary*(uplift/100)",chart=True),
             O("Annual license cost","developers*seatCost*12",chart=True),
             O("Return on investment","(developers*seatCost*12) ? ((developers*avgSalary*(uplift/100) - developers*seatCost*12)/(developers*seatCost*12))*100 : 0","percent"),
             O("Value / dev / mo","avgSalary*(uplift/100)/12")],
    advice="Productivity uplift should come from measurement (cycle time, throughput), not vendor claims.",
    formula_plain="Net value = developers × salary × uplift% − license cost.",
    formula="<b>Net value</b> = devs × salary × uplift% − (devs × seat × 12)",
    about="<p>AI coding assistants are cheap per seat but their value depends on a credible productivity uplift. Even a conservative single-digit percentage on loaded developer salaries dwarfs the license cost.</p><p>Measure uplift from your own delivery metrics before plugging in a number — vendor benchmarks rarely match real teams.</p>")

add(slug="headcount-equivalent", title="Headcount Equivalent Calculator", icon="users",
    tagline="Translate automated hours into full-time-equivalent capacity and its dollar value.",
    category="Workforce & Planning",
    fields=[F("hoursAutomatedMonthly","Hours automated / month",640),
            F("hoursPerFTEmonth","Productive hours / FTE / mo",160),
            F("loadedCostPerFTE","Loaded cost / FTE / mo",6500,money=True)],
    outputs=[O("FTE equivalent","hoursAutomatedMonthly/(hoursPerFTEmonth||1)",hero=True,fmt="number",unit="FTE"),
             O("Monthly value","(hoursAutomatedMonthly/(hoursPerFTEmonth||1))*loadedCostPerFTE",chart=True),
             O("Annual value","(hoursAutomatedMonthly/(hoursPerFTEmonth||1))*loadedCostPerFTE*12",chart=True),
             O("Hours automated / yr","hoursAutomatedMonthly*12","hours")],
    advice="FTE-equivalent is a capacity metric, not a layoff plan — frame it as freed-up capacity.",
    formula_plain="FTE equivalent = hours automated ÷ productive hours per FTE.",
    formula="<b>FTE</b> = hours automated ÷ productive hours per FTE",
    about="<p>Leaders think in headcount, so converting automated hours into full-time-equivalents makes AI capacity tangible. Divide monthly automated hours by the productive hours a single employee delivers (after meetings and admin).</p><p>Multiplying by loaded FTE cost gives the capacity value — useful for redeploying people to higher-value work.</p>")

add(slug="subscription-vs-usage", title="Subscription vs Usage Pricing", icon="scale",
    tagline="Decide between a flat plan and pay-as-you-go at your real call volume.",
    category="Token & API Cost",
    fields=[F("monthlyCalls","API calls / month",50000),
            F("usagePrice","Pay-as-you-go price / call",0.02,money=True),
            F("flatPlan","Flat plan price",799,money=True),
            F("flatIncludedCalls","Calls included in plan",40000),
            F("overagePrice","Overage price / call",0.015,money=True)],
    outputs=[O("Pay-as-you-go cost","monthlyCalls*usagePrice",hero=True,chart=True),
             O("Flat plan cost","flatPlan + max(0, monthlyCalls-flatIncludedCalls)*overagePrice",chart=True),
             O("Monthly difference","abs(monthlyCalls*usagePrice - (flatPlan + max(0, monthlyCalls-flatIncludedCalls)*overagePrice))"),
             O("Annual difference","abs(monthlyCalls*usagePrice - (flatPlan + max(0, monthlyCalls-flatIncludedCalls)*overagePrice))*12")],
    rules=[("monthlyCalls*usagePrice < (flatPlan + max(0, monthlyCalls-flatIncludedCalls)*overagePrice)","Pay-as-you-go is cheaper at this volume — revisit if usage grows past the plan allowance."),
           ("monthlyCalls*usagePrice > (flatPlan + max(0, monthlyCalls-flatIncludedCalls)*overagePrice)","The flat plan wins at this volume — lock it in and monitor overage."),],
    advice="The crossover point moves with volume — recompute whenever traffic changes materially.",
    formula_plain="Compare calls × usage price against flat plan + overage on calls above the allowance.",
    formula="<b>Flat</b> = plan + max(0, calls − included) × overage &nbsp;vs&nbsp; <b>Usage</b> = calls × price",
    about="<p>Vendors price the same capability two ways, and the cheaper option flips with volume. Below the plan allowance the flat tier wastes money; well above it, overage charges can exceed pure pay-as-you-go.</p><p>This calculator finds which side of the crossover you are on today and how much it matters annually.</p>")

add(slug="prompt-cost", title="Prompt Cost Estimator", icon="coins",
    tagline="Scale a single prompt's token cost to daily, monthly, and annual spend.",
    category="Token & API Cost",
    fields=[F("dailyRuns","Runs / day",2000),
            F("inputTokens","Input tokens / run",900),
            F("outputTokens","Output tokens / run",450),
            F("priceIn","Input price (/1M)",2,money=True),
            F("priceOut","Output price (/1M)",8,money=True)],
    outputs=[O("Monthly cost","dailyRuns*((inputTokens/1000000)*priceIn+(outputTokens/1000000)*priceOut)*30",hero=True,chart=True),
             O("Daily cost","dailyRuns*((inputTokens/1000000)*priceIn+(outputTokens/1000000)*priceOut)",chart=True),
             O("Annual cost","dailyRuns*((inputTokens/1000000)*priceIn+(outputTokens/1000000)*priceOut)*365",chart=True),
             O("Cost per run","(inputTokens/1000000)*priceIn+(outputTokens/1000000)*priceOut","number",unit="USD"),
             O("Tokens / day","dailyRuns*(inputTokens+outputTokens)","integer")],
    advice="Caching repeated context and trimming system prompts both cut input-token cost at scale.",
    formula_plain="Monthly cost = runs/day × per-run token cost × 30.",
    formula="<b>Monthly</b> = runs/day × (in÷1M × inPrice + out÷1M × outPrice) × 30",
    about="<p>A prompt that costs a fraction of a cent looks free until you multiply by production volume. This tool scales the per-run token cost to daily, monthly, and annual figures so the true budget impact is visible before launch.</p><p>The biggest levers are output length and any repeated context you can cache or shorten.</p>")

add(slug="rag-pipeline-cost", title="RAG Pipeline Cost Estimator", icon="layers",
    tagline="Estimate embedding plus generation cost for a retrieval-augmented pipeline.",
    category="Token & API Cost",
    fields=[F("queriesMonthly","Queries / month",120000),
            F("embedTokens","Embedding tokens / query",500),
            F("genInput","Generation input tokens",2500),
            F("genOutput","Generation output tokens",400),
            F("embedPrice","Embedding price (/1M)",0.1,money=True),
            F("genInPrice","Gen input price (/1M)",3,money=True),
            F("genOutPrice","Gen output price (/1M)",15,money=True)],
    outputs=[O("Total monthly cost","queriesMonthly*((embedTokens/1000000)*embedPrice + (genInput/1000000)*genInPrice + (genOutput/1000000)*genOutPrice)",hero=True,chart=True),
             O("Embedding cost","queriesMonthly*(embedTokens/1000000)*embedPrice",chart=True),
             O("Generation cost","queriesMonthly*((genInput/1000000)*genInPrice + (genOutput/1000000)*genOutPrice)",chart=True),
             O("Cost per query","(embedTokens/1000000)*embedPrice + (genInput/1000000)*genInPrice + (genOutput/1000000)*genOutPrice","number",unit="USD"),
             O("Annual cost","queriesMonthly*((embedTokens/1000000)*embedPrice + (genInput/1000000)*genInPrice + (genOutput/1000000)*genOutPrice)*12")],
    advice="Large retrieved context inflates generation input — tune chunk size and top-k to control it.",
    formula_plain="Cost = queries × (embed + generation input + generation output token costs).",
    formula="<b>Per query</b> = embed + genIn + genOut token cost; × queries = monthly",
    about="<p>Retrieval-augmented generation has two cost centres: embedding the query (cheap) and generating an answer with retrieved context (expensive, because the context inflates input tokens). Modelling them separately shows where to optimise.</p><p>Reducing the number or size of retrieved chunks usually cuts generation input cost faster than anything else.</p>")

add(slug="fine-tuning-vs-prompting", title="Fine-Tuning vs Prompting Cost", icon="scale",
    tagline="Compare long-prompt inference against a fine-tuned model with shorter prompts.",
    category="Token & API Cost",
    fields=[F("monthlyRequests","Requests / month",100000),
            F("promptTokensBase","Prompt tokens — prompting",1800),
            F("promptTokensTuned","Prompt tokens — fine-tuned",600),
            F("pricePerM","Token price (/1M)",3,money=True),
            F("trainingCost","One-time training cost",2500,money=True),
            F("tunedHosting","Tuned hosting / month",400,money=True)],
    outputs=[O("Monthly saving","monthlyRequests*(promptTokensBase/1000000)*pricePerM - (monthlyRequests*(promptTokensTuned/1000000)*pricePerM + tunedHosting)",hero=True,chart=True),
             O("Prompting cost","monthlyRequests*(promptTokensBase/1000000)*pricePerM",chart=True),
             O("Fine-tuned cost","monthlyRequests*(promptTokensTuned/1000000)*pricePerM + tunedHosting",chart=True),
             O("Training payback","(monthlyRequests*(promptTokensBase/1000000)*pricePerM - (monthlyRequests*(promptTokensTuned/1000000)*pricePerM + tunedHosting)) > 0 ? trainingCost/(monthlyRequests*(promptTokensBase/1000000)*pricePerM - (monthlyRequests*(promptTokensTuned/1000000)*pricePerM + tunedHosting)) : 0","months"),
             O("Annual saving","(monthlyRequests*(promptTokensBase/1000000)*pricePerM - (monthlyRequests*(promptTokensTuned/1000000)*pricePerM + tunedHosting))*12")],
    rules=[("monthlyRequests*(promptTokensBase/1000000)*pricePerM <= (monthlyRequests*(promptTokensTuned/1000000)*pricePerM + tunedHosting)","Fine-tuning doesn't pay off at this volume — stick with prompting until traffic grows."),],
    advice="Fine-tuning pays off when high request volume amortises the training and hosting cost.",
    formula_plain="Saving = prompting token cost − (fine-tuned token cost + hosting); payback = training ÷ saving.",
    formula="<b>Saving</b> = promptingCost − (tunedCost + hosting); <b>payback</b> = training ÷ saving",
    about="<p>Fine-tuning trades a fixed training cost and ongoing hosting for shorter prompts at inference. At high volume the per-request token saving is large; at low volume the fixed costs dominate.</p><p>The payback output tells you how many months of saving repay the training spend — the deciding number.</p>")

add(slug="email-automation-roi", title="Email Automation ROI", icon="mail",
    tagline="Value the time AI drafting and triage saves across your inbox volume.",
    category="ROI & Payback",
    fields=[F("emailsPerWeek","Emails / week",300),
            F("minutesPerEmail","Minutes / email",4),
            F("automationRate","Time saved %",60),
            F("hourlyRate","Loaded hourly value",38,money=True),
            F("toolCost","Monthly tool cost",60,money=True)],
    outputs=[O("Net monthly value","emailsPerWeek*4.33*minutesPerEmail/60*(automationRate/100)*hourlyRate - toolCost",hero=True,chart=True),
             O("Gross time value","emailsPerWeek*4.33*minutesPerEmail/60*(automationRate/100)*hourlyRate",chart=True),
             O("Monthly tool cost","toolCost",chart=True),
             O("Hours saved / mo","emailsPerWeek*4.33*minutesPerEmail/60*(automationRate/100)","hours"),
             O("Annual net value","(emailsPerWeek*4.33*minutesPerEmail/60*(automationRate/100)*hourlyRate - toolCost)*12")],
    advice="Drafting assistance still needs a human send decision — keep the time-saved share realistic.",
    formula_plain="Net value = emails × minutes ÷ 60 × time-saved% × hourly value − tool cost.",
    formula="<b>Net value</b> = emails/wk × 4.33 × min ÷ 60 × saved% × rate − tool cost",
    about="<p>AI assistance compresses the time spent reading, triaging, and drafting email rather than removing the inbox. The time-saved percentage captures that compression realistically.</p><p>Across a month of inbox volume even modest per-email savings add up to meaningful reclaimed hours.</p>")

add(slug="data-labeling-cost", title="Data Labeling Cost Calculator", icon="grid",
    tagline="Compare fully manual labeling against AI pre-labeling with human review.",
    category="Workforce & Planning",
    fields=[F("items","Items / month",50000),
            F("secondsPerItem","Seconds / item — manual",20),
            F("reviewSeconds","Seconds / item — AI review",6),
            F("labelerHourly","Labeler hourly cost",15,money=True)],
    outputs=[O("Monthly saving","items*secondsPerItem/3600*labelerHourly - items*reviewSeconds/3600*labelerHourly",hero=True,chart=True),
             O("Manual cost","items*secondsPerItem/3600*labelerHourly",chart=True),
             O("AI-assisted cost","items*reviewSeconds/3600*labelerHourly",chart=True),
             O("Hours saved / mo","items*(secondsPerItem-reviewSeconds)/3600","hours"),
             O("Annual saving","(items*secondsPerItem/3600*labelerHourly - items*reviewSeconds/3600*labelerHourly)*12")],
    advice="AI pre-labeling shifts work from labeling to reviewing — include QA on a sample to hold quality.",
    formula_plain="Saving = items × (manual seconds − review seconds) ÷ 3600 × labeler hourly cost.",
    formula="<b>Saving</b> = items × (manualSec − reviewSec) ÷ 3600 × hourly cost",
    about="<p>AI pre-labeling doesn't remove humans — it turns labelers into reviewers, cutting seconds per item dramatically. The saving is the time delta across your monthly item volume.</p><p>Always keep a QA sample of fully reviewed items so model drift doesn't quietly degrade label quality.</p>")

add(slug="translation-savings", title="Translation Automation Savings", icon="translate",
    tagline="Compare human translation against AI plus post-editing across your word volume.",
    category="Workforce & Planning",
    fields=[F("wordsPerMonth","Words / month",200000),
            F("humanRate","Human rate / word",0.12,money=True),
            F("aiRate","AI rate / word",0.002,money=True),
            F("postEditRate","Post-edit rate / word",0.03,money=True),
            F("postEditShare","Post-edited %",70)],
    outputs=[O("Monthly saving","wordsPerMonth*humanRate - (wordsPerMonth*aiRate + wordsPerMonth*(postEditShare/100)*postEditRate)",hero=True,chart=True),
             O("Human-only cost","wordsPerMonth*humanRate",chart=True),
             O("AI + post-edit cost","wordsPerMonth*aiRate + wordsPerMonth*(postEditShare/100)*postEditRate",chart=True),
             O("Cost / 1k words (AI)","(wordsPerMonth*aiRate + wordsPerMonth*(postEditShare/100)*postEditRate)/(wordsPerMonth/1000||1)","number",unit="USD"),
             O("Annual saving","(wordsPerMonth*humanRate - (wordsPerMonth*aiRate + wordsPerMonth*(postEditShare/100)*postEditRate))*12")],
    advice="High-stakes content needs full post-editing — raise the post-edited share for legal or medical text.",
    formula_plain="Saving = human cost − (AI cost + post-editing on the edited share).",
    formula="<b>Saving</b> = words × humanRate − (words × aiRate + words × share% × postEditRate)",
    about="<p>Machine translation plus human post-editing is the standard production workflow, and it is far cheaper than pure human translation. The honest model adds post-editing cost only on the share of content that actually needs it.</p><p>For regulated or brand-critical content, push the post-edited share toward 100% and re-check the saving.</p>")

add(slug="sales-outreach-roi", title="Sales Outreach Automation ROI", icon="rocket",
    tagline="Value the rep hours AI personalization and drafting return across your team.",
    category="ROI & Payback",
    fields=[F("reps","Sales reps",8),
            F("emailsPerRepDay","Emails / rep / day",40),
            F("minutesSaved","Minutes saved / email",2.5,step="0.1"),
            F("workingDays","Working days / month",22),
            F("hourlyRate","Loaded hourly value",42,money=True),
            F("toolCost","Monthly tool cost",480,money=True)],
    outputs=[O("Net monthly value","reps*emailsPerRepDay*workingDays*minutesSaved/60*hourlyRate - toolCost",hero=True,chart=True),
             O("Gross time value","reps*emailsPerRepDay*workingDays*minutesSaved/60*hourlyRate",chart=True),
             O("Monthly tool cost","toolCost",chart=True),
             O("Hours saved / mo","reps*emailsPerRepDay*workingDays*minutesSaved/60","hours"),
             O("Annual net value","(reps*emailsPerRepDay*workingDays*minutesSaved/60*hourlyRate - toolCost)*12")],
    advice="The bigger upside is often more selling time, not just cost saved — track pipeline impact too.",
    formula_plain="Net value = reps × emails/day × days × minutes saved ÷ 60 × hourly value − tool cost.",
    formula="<b>Net value</b> = reps × emails × days × min ÷ 60 × rate − tool cost",
    about="<p>Outreach tooling personalizes and drafts at scale, returning minutes per message to each rep. Across a team and a month those minutes become real selling capacity.</p><p>This model captures the hard time saving; the strategic upside is the additional pipeline that reclaimed time can generate.</p>")

add(slug="cost-per-conversation", title="Cost per Conversation Calculator", icon="bot",
    tagline="Break down the true per-conversation cost of an AI assistant including platform fees.",
    category="Token & API Cost",
    fields=[F("conversationsMonthly","Conversations / month",30000),
            F("turnsPerConvo","Turns / conversation",6),
            F("tokensPerTurn","Tokens / turn",700),
            F("pricePerM","Token price (/1M)",4,money=True),
            F("platformMonthly","Platform cost / month",500,money=True)],
    outputs=[O("Cost per conversation","(conversationsMonthly*turnsPerConvo*tokensPerTurn/1000000*pricePerM + platformMonthly)/(conversationsMonthly||1)",hero=True,fmt="number",unit="USD"),
             O("Total monthly cost","conversationsMonthly*turnsPerConvo*tokensPerTurn/1000000*pricePerM + platformMonthly",chart=True),
             O("Token cost","conversationsMonthly*turnsPerConvo*tokensPerTurn/1000000*pricePerM",chart=True),
             O("Platform cost","platformMonthly",chart=True),
             O("Annual cost","(conversationsMonthly*turnsPerConvo*tokensPerTurn/1000000*pricePerM + platformMonthly)*12")],
    advice="Compare cost per conversation against your human cost per contact to size the opportunity.",
    formula_plain="Cost/convo = (token cost + platform fee) ÷ conversations.",
    formula="<b>Cost / convo</b> = (convos × turns × tokens ÷ 1M × price + platform) ÷ convos",
    about="<p>A single conversation spans multiple turns, each consuming tokens, plus a fixed platform fee spread across volume. Dividing the all-in monthly cost by conversation count gives a unit economic you can benchmark.</p><p>Compared against human cost per contact, this number tells you whether — and where — automation pays.</p>")

add(slug="three-year-tco", title="3-Year AI Total Cost of Ownership", icon="map",
    tagline="Project setup, subscription, usage, and staffing into a 3-year cost with growth.",
    category="Workforce & Planning",
    fields=[F("setupCost","Setup / build cost",15000,money=True),
            F("subscription","Subscription / month",1200,money=True),
            F("usage","Usage / month",800,money=True),
            F("staffMonthly","Staffing / month",2000,money=True),
            F("annualGrowth","Annual cost growth %",10)],
    outputs=[O("3-year TCO","setupCost + (subscription+usage+staffMonthly)*12*(1 + (1+annualGrowth/100) + pow(1+annualGrowth/100,2))",hero=True,chart=True),
             O("Year-1 cost","setupCost + (subscription+usage+staffMonthly)*12",chart=True),
             O("Year-3 cost","(subscription+usage+staffMonthly)*12*pow(1+annualGrowth/100,2)",chart=True),
             O("Avg monthly cost","(setupCost + (subscription+usage+staffMonthly)*12*(1 + (1+annualGrowth/100) + pow(1+annualGrowth/100,2)))/36","number",unit="USD"),
             O("Setup cost","setupCost")],
    advice="TCO should include the people who run and maintain the system, not just vendor invoices.",
    formula_plain="TCO = setup + recurring × 12 × (1 + (1+g) + (1+g)²), where g is annual growth.",
    formula="<b>TCO</b> = setup + monthly×12 × (1 + (1+g) + (1+g)²)",
    about="<p>Headline subscription prices hide the real cost of owning an AI system: integration, usage that grows with adoption, and the people who maintain it. A three-year view with a growth factor is the fair basis for vendor comparison.</p><p>Pair this TCO with a benefit projection to get a true multi-year ROI.</p>")

add(slug="ai-vs-human-cost", title="AI vs Human Cost per Task", icon="scale",
    tagline="Compare per-task cost of human work against an AI process at your volume.",
    category="ROI & Payback",
    fields=[F("tasksMonthly","Tasks / month",20000),
            F("humanCostPerTask","Human cost / task",2.5,money=True),
            F("aiCostPerTask","AI cost / task",0.15,money=True),
            F("aiSetupMonthly","AI fixed cost / month",1500,money=True)],
    outputs=[O("Monthly saving","tasksMonthly*humanCostPerTask - (tasksMonthly*aiCostPerTask + aiSetupMonthly)",hero=True,chart=True),
             O("Human cost","tasksMonthly*humanCostPerTask",chart=True),
             O("AI total cost","tasksMonthly*aiCostPerTask + aiSetupMonthly",chart=True),
             O("Cost reduction","(tasksMonthly*humanCostPerTask) ? ((tasksMonthly*humanCostPerTask - (tasksMonthly*aiCostPerTask + aiSetupMonthly))/(tasksMonthly*humanCostPerTask))*100 : 0","percent"),
             O("Annual saving","(tasksMonthly*humanCostPerTask - (tasksMonthly*aiCostPerTask + aiSetupMonthly))*12")],
    rules=[("tasksMonthly*humanCostPerTask < (tasksMonthly*aiCostPerTask + aiSetupMonthly)","At this volume the fixed AI cost outweighs the per-task saving — automate only above the break-even volume."),],
    advice="Include the AI fixed cost (platform, maintenance) so low-volume cases aren't overstated.",
    formula_plain="Saving = tasks × human cost − (tasks × AI cost + AI fixed cost).",
    formula="<b>Saving</b> = tasks × humanCost − (tasks × aiCost + fixed)",
    about="<p>The cleanest automation case compares unit cost: what a task costs a human versus what it costs the AI, including the fixed platform cost spread across volume. High volume makes the fixed cost negligible; low volume can erase the saving.</p><p>The cost-reduction percentage is the headline most executives remember.</p>")

# ---------------------------------------------------------------- rendering
RELATED = {}  # built later: slug -> list of (title, slug, tagline, icon)

def calc_config(c):
    title = c["title"]
    hero = next((o for o in c["outputs"] if o.get("hero")), c["outputs"][0])
    examples = [
        ("Run a quick estimate", f"Enter your numbers and the {title} instantly shows {hero['label'].lower()} with a live breakdown you can copy, save, or download."),
        ("Compare scenarios side by side", f"Change one input at a time to watch {hero['label'].lower()} move, then save each version as a named scenario in your workspace."),
        ("Drop it into your business case", "Export clean figures as JSON or copy a formatted summary straight into a deck, spreadsheet, or proposal."),
    ]
    faq = [
        (f"How is {hero['label'].lower()} calculated?", c["formula_plain"] + " Everything updates live as you type."),
        ("Is my data sent anywhere?", "No. Every calculation runs entirely in your browser. Nothing is uploaded, and any saved scenarios stay in this device's local storage."),
        ("Can I trust this for a real business case?", "Treat the output as a rigorous first pass. The math is exact; the accuracy depends on your inputs, so validate rates, prices, and adoption assumptions with your own data before presenting."),
    ]
    if c.get("custom_faq"):
        faq = c["custom_faq"] + faq[1:]
    rules = [{"if": r[0], "text": r[1]} if r[0] else {"text": r[1]} for r in c.get("rules", [])]
    return {
        "title": title, "kind": "calculator",
        "fields": c["fields"],
        "engine": {"outputs": c["outputs"], "rules": rules, "defaultAdvice": c["advice"]},
        "examples": [{"title": t, "body": b} for t, b in examples],
        "faq": [{"q": q, "a": a} for q, a in faq],
        "limits": LIMITS,
    }

def calc_body(c, pfx, related):
    title = c["title"]
    n_in = len(c["fields"])
    head = page_head_block(pfx, c["category"], title, c["tagline"], c["icon"],
                           trail=[("Home", ""), ("Calculators", "calculators/"), (title, None)])
    tool = f'''<section class="calc">
  <div class="panel">
    <div class="panel-head"><h2>Your inputs</h2><span class="chip">{n_in} inputs</span></div>
    <div class="panel-body"><div class="fields" id="toolFields"></div></div>
  </div>
  <div class="panel result-panel">
    <div class="panel-head"><h2>Result</h2>
      <div class="toolbar">
        <button class="btn btn-ghost btn-sm" id="copyExport" type="button">Copy</button>
        <button class="btn btn-ghost btn-sm" type="button" data-save-current>Save scenario</button>
        <button class="btn btn-primary btn-sm" type="button" data-download-current>JSON</button>
      </div>
    </div>
    <div class="panel-body"><div id="toolResult"></div></div>
  </div>
</section>'''
    method = f'''<section class="panel"><div class="panel-body prose">
  <h2>How the {title} works</h2>
  <div class="formula">{c["formula"]}</div>
  {c["about"]}
  <div class="callout"><strong>Tip:</strong> {c["advice"]}</div>
</div></section>'''
    examples = '<section><div class="section-head left"><h2>Ways to use it</h2><p>Built for repeat decisions, not one-off pages.</p></div><div class="grid grid-3" id="examples"></div></section>'
    limits = '<section class="panel"><div class="panel-body prose"><h2>Limits &amp; good practice</h2><ul class="advice-list" id="limits" style="list-style:none"></ul></div></section>'
    faq = '<section><div class="section-head left"><h2>Frequently asked</h2><p>Short, specific answers.</p></div><div id="faq"></div></section>'
    rel_cards = "".join(
        f'<a class="card hoverable" href="{pfx}calculators/{s}/"><div class="icon-tile tile-{tile}">{icon(ic)}</div><h3>{t}</h3><p>{tg}</p><span class="card-link">Open {icon("arrow")}</span></a>'
        for t, s, tg, ic, tile in related)
    rel = f'<section><div class="section-head left"><h2>Related calculators</h2><p>Keep modelling the same decision.</p></div><div class="grid grid-3">{rel_cards}</div></section>'
    return head + ad_unit() + tool + method + examples + ad_unit() + faq + limits + rel

def render_calc(c, related):
    pfx = prefix_for("calculators/" + c["slug"])
    body = calc_body(c, pfx, related)
    scripts = (site_config_script(calc_config(c))
               + f'<script src="{pfx}app.js"></script><script src="{pfx}saas.js"></script>')
    desc = c["tagline"][:155]
    html = app_page(c["title"] + " | " + "AgentHubs", desc, "calculators/" + c["slug"],
                    "calculators", "", body, scripts)
    return html
