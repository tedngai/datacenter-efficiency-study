# Power, water and bills: what the data shows

A brief for environmental and community groups. It uses the datasets in this
repository and names each source. Current as of November 2026.

---

## The thesis

**Most AI data center capacity is not built yet. So the main community question
is about decisions that are still open, not about damage that is already done.**

The evidence shows two real ways that these campuses can put costs on a
community:

1. **Electricity.** New data center load raises shared grid costs in regional
   power markets. The clearest measurement is in PJM, the grid that serves 13
   states from Illinois to Virginia.
2. **Water.** Campuses that cool by evaporation can take a large share of a
   small town's water. Campuses with dry or closed-loop cooling take very
   little.

Each impact depends on a choice that a utility commission, a city or a county
can still set:

- **Who pays** for new generation and transmission.
- **How the campus cools**, and where its water comes from.
- **What the operator must disclose**, site by site, every year.

The data does not support "every data center raises your bill". It also does
not support "data centers lower your bill". It does support this: the cost risk
is real at the regional level, and rate design can assign it. The water risk is
local and depends on the design, and most operators do not publish it.

---

## 1. Most of the load is a plan

We track 442 campuses with 123 GW of stated power capacity. That figure is
nameplate capacity, not the power the sites use today.

| Status | World GW | Share | US GW | Share |
|---|---:|---:|---:|---:|
| Operational | 20.4 | 17% | 10.5 | 15% |
| Partially operational | 16.5 | 13% | 12.5 | 18% |
| Under construction | 41.0 | 33% | 23.5 | 35% |
| Planned | 45.5 | 37% | 21.7 | 32% |
| **Total** | **123.4** | | **68.1** | |

GW = gross facility power where published, else IT load. A partially
operational site carries its full target, not its live load.

What this means for a community:

- **70% of tracked capacity is planned or under construction.** In the US the
  share is 66%. For most sites, the tariff, the water contract and the permit
  are still under negotiation or open to challenge.
- **Texas holds half of the tracked US capacity (33.2 GW), and 83% of it is
  planned or under construction.** One proposal, Fermi America in Amarillo, is
  11 GW with no named tenant.
- **A planned gigawatt is a request for power, not a load.** Some of these
  projects will not be built. Utilities and grid operators must still plan for
  the requests, and that planning has a cost.
- **Nameplate is more than average draw.** Meta reports 18.06 TWh of data center
  electricity for 2024. That is an average of 2.06 GW. We track about 3.97 GW of
  Meta IT capacity, and some of it is not built yet. So the average draw was
  about half of the capacity on paper.

For scale: the US planned and under-construction capacity alone is 45.2 GW. At
full load for one year, that is about 396 TWh. Lawrence Berkeley National
Laboratory (LBNL) estimates that all US data centers used 176 TWh in 2023 (4.4%
of US electricity). LBNL projects 325–580 TWh by 2028. Full load is an upper
bound. Real use will be lower, because some projects will stop and no campus
runs at 100%.

---

## 2. Electricity: the cost goes through the regional market

**Finding.** In PJM, the cost of data center load reaches every customer
through the capacity market. The size of the effect is large.

- PJM's Independent Market Monitor estimates that data center load added
  **$9.33 billion** to the 2025/26 capacity auction. The auction total was
  $14.69 billion. Without data center load, the monitor estimates $5.35 billion.
  The model includes 7.9 GW of existing and forecast data center load
  ([IMM, Part G, 3 Jun 2025](https://www.monitoringanalytics.com/reports/reports/2025/IMM_Analysis_of_the_20252026_RPM_Base_Residual_Auction_Part_G_20250603_Revised.pdf)).
- The monitor's conclusion: "data center load growth is the primary reason" for
  the high capacity prices.
- Capacity costs go into retail bills through each state's supply rates. New
  Jersey's 17–20% supply-rate step in June 2025 followed that auction.

**Caveat.** The monitor's figure is a model result: the auction with and
without data center load. It is not an accounting of bills. It covers all data
centers in PJM, not only the AI campuses in this dataset.

**What the state data shows.** Residential prices rose in every state where we
track a site. The US average rose 33.2% from 2021 to the 2026 year to date
(EIA). The rise follows the market structure more than local AI capacity:

- The six states in our table that sit mostly in PJM (PA, NJ, OH, IL, VA, WV)
  rose by **44% on average**. The other 26 tracked states rose by **26%**.
- Across the 32 states, the price rise has **only a weak relation** to the
  operating AI capacity that we track in each state. The rank correlation is
  0.15, which is too weak to mean much for 32 states.
- Iowa has 1.2 GW of tracked operating capacity. It had the smallest rise in
  the table (+14.3%). New York has 0.75 GW, and its price rose by 50.2%.

**Caveat.** These are state averages, without controls for gas prices, storm
costs or other causes. Our inventory covers large AI campuses only, not every
data center. Virginia has the largest data center market in the world, but we
track only 2.2 GW there. So the state comparison cannot prove that data centers
raise bills. It also cannot prove that they do not.

**The decision that matters: rate design.** From 2025 to 2026, most large
utilities filed a data center rate class. Examples from our utility table:

- Dominion Virginia GS-5: a class for loads of 25 MW or more, from 2027. It sets
  an 85% minimum take on transmission and distribution, and 60% on generation.
- AEP Ohio: data centers pay for at least 85% of contracted capacity, for up to
  12 years.
- Wisconsin: the PSC made data centers pay 100% of new generation costs.
- PGE Oregon: a new class with +29.7% for data centers and −1.3% for homes.

Consumer advocates in Virginia, Ohio, Illinois, Wisconsin, Minnesota, Oregon and
Pennsylvania argue that these terms are not strong enough. The full list is in
`data/us_utility_impacts.csv`.

**Utility claims that data centers lower bills.** Some utilities make this
claim, for example MidAmerican Iowa, MDU North Dakota and Entergy. Treat it as a
claim. In Mississippi and Arkansas, the contracts that support it are trade
secrets under state law.

---

## 3. Water: local, set by design, mostly not disclosed

**Finding.** Data center water use is small at national scale, but it can be a
large share of a local supply. The cooling design sets the size, and the design
is a choice.

Measured or reported shares of local supply:

| Place | Share | Basis |
|---|---|---|
| The Dalles, Oregon | ~40% of city water | City records, released after a lawsuit |
| Loudoun County, Virginia | ~9% of average-day drinking water | Loudoun Water |
| Columbus area, Ohio | ~3% of city supply (~1.2B gal/yr) | Columbus utilities |
| Ridgeland, Mississippi | 82% of peak capacity, if the reported 3.7 MGD peak is correct | Reported, not verified |

Volumes at single sites can be large. Google's Council Bluffs, Iowa campus
consumed 1,346 million gallons in 2025. That is about the use of 12,000 US
households, at the EPA figure of about 300 gallons per family per day. Meta's
whole global fleet consumed about 786 million gallons in 2024, which is less
than that one site.

**Design sets the water.** At the same IT load, the reported water intensity
differs by a factor of 500:

| Operator | Water per kWh of IT energy | Water for 1 MW for one year | Cooling |
|---|---:|---:|---|
| Google | 1.02 L (consumption, derived) | 2.36M gal | Evaporative at large campuses |
| Microsoft | 0.27 L | 0.63M gal | Mixed |
| Meta | 0.19 L (withdrawal) | 0.44M gal | Mixed |
| AWS | 0.12 L | 0.28M gal | Mixed |
| Crusoe | ~0.002 L (design) | ~0.005M gal | Closed loop |

Evaporative cooling uses less electricity and more water. Dry cooling uses more
electricity and less water. So a water-stressed place and a grid-stressed place
can rationally ask for different designs.

**Liquid-cooled chips do not mean a waterless campus.** The rack can use liquid,
and the plant can still reject that heat through cooling towers. Google's
liquid-cooled TPU campuses do this. Ask about the plant, not the chip.

**Caveat.** Only Google publishes water by site. For all other operators, our
site water figures are the fleet average applied to the site. No site in our
dataset has a metered site figure for water per unit of IT energy. For 32 of 61
US campuses that are planned or under construction, the cooling water
dependency is unknown.

---

## 4. Disclosure is the bottleneck

- Of 13 operators, **4 publish assured annual figures** for energy and water:
  Google, Meta, Microsoft and AWS. xAI, CoreWeave, Applied Digital, Lambda and
  Galaxy publish no usable figures.
- **Secrecy, more than volume, starts most water disputes in our data.**
  Examples: The Dalles (records lawsuit), Eagle Mountain, Utah (the city
  contract keeps use confidential), Chesterfield, Virginia, and Racine,
  Wisconsin.
- **Disclosure laws work.** Nebraska LB1010 and Utah HB76 require reporting.
  Mississippi SB 2001 goes the other way: it makes the contracts trade secrets.

---

## 5. What this dataset cannot tell you yet

We state these gaps so that no reader takes the data for more than it is.

- **Air emissions.** We do not track on-site gas generation, for example the xAI
  turbines in Memphis or the gas plants planned for Meta Hyperion. For many
  neighbours, this is the main health issue.
- **Water at the power plant.** Thermal power plants use water too. Our water
  figures cover the campus only.
- **Total data center load per utility.** We track large AI campuses, not every
  data center. The utility's own load forecast is the better source.
- **Actual energy use per site.** We have capacity, not metered energy (MWh).
- **Hourly carbon.** "100% renewable" claims are annual and global matches. They
  do not mean that the power at a given campus is renewable at every hour.

---

## 6. Questions to ask about a proposed campus

These questions follow from the findings. Each one asks for a number that the
operator or the utility has.

1. **Load.** How many MW does the contract request, and on what schedule?
2. **Who pays.** Does the tariff have a minimum take, an exit fee and a
   collateral requirement? Who pays for the new transmission?
3. **On-site generation.** What fuel, how many MW, and under which air permit?
4. **Cooling.** Is the plant evaporative, dry or hybrid? What is the design
   water use per MW, on the peak day and over a year?
5. **Water source.** Drinking water, reclaimed water or groundwater? What
   happens to the campus supply in a drought?
6. **Reporting.** Will the operator publish each year, for this site, the
   energy use (MWh), the water withdrawn and the water consumed?

---

## Sources and data

- Site capacity and status: `data/published/data_centers.csv`. Method and
  caveats: `README.md`.
- Utility prices, rate cases, water and named groups:
  `data/us_utility_impacts.csv`, `docs/us_water_energy.md`. Checks:
  `docs/us_impacts_verification.md`.
- Operator energy and water efficiency: `data/operator_efficiency.csv`,
  `docs/operator_efficiency.md`.
- Cooling design by site: `data/gpu_cooling.csv`, `docs/gpu_cooling.md`.
- PJM Independent Market Monitor, *Analysis of the 2025/2026 RPM Base Residual
  Auction, Part G* (3 Jun 2025, revised).
- LBNL, *2024 United States Data Center Energy Usage Report* (Dec 2024):
  https://eta-publications.lbl.gov/publications/2024-lbnl-data-center-energy-usage-report
- EIA, *Electric Power Annual* Table 2.10 and *Electric Power Monthly* Table
  5.6.B (state residential prices).
- US EPA WaterSense, household water use (~300 gal per family per day).

The state comparison in section 2 uses `pipeline/verification/eia_table.txt` and
the operating capacity per state from the site dataset. The script is
`pipeline/verification/price_vs_capacity.py`.
