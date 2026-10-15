# bevo_big_data

## Goal
Question: How do derailment rates in the US per million train miles change across railroads from 2014 to 2022 and what caused them?

## Data Sources and Data Collection
This project uses two datasets provided by the Federal Railroad Administration (FRA), an agency of the U.S. Department of Transportation (USDOT). The datasets provide complementary information: one records reportable railroad accidents and incidents, while the other contains operational data that can be used to measure railroad activity. Combining these sources allows the analysis of accident trends in relation to operational exposure.

### 1. FRA Rail Equipment Accident/Incident Data (Form 54)
- Official dataset name: Rail Equipment Accident/Incident Data (Form 54)
- Original source: https://data.transportation.gov/Railroads/Rail-Equipment-Accident-Incident-Data-Form-54-/85tf-25kj/data_preview
- Data dictionary: https://data.transportation.gov/Railroads/Rail-Equipment-Accident-Incident-Data-Form-54-/85tf-25kj/about_data
- The Rail Equipment Accident/Incident Data (Form 54) is a publicly available dataset maintained by the Federal Railroad Administration (FRA). It contains records of reportable railroad equipment accidents and incidents in the United States, including derailments, collisions, fires, explosions, and other events involving railroad on-track equipment, whether standing or moving.
- Under federal reporting requirements, railroads must report qualifying accidents and incidents to the FRA using Form FRA 6180.54 — Rail Equipment Accident/Incident. These reports include information about the event, such as its date, location, equipment involved, accident characteristics, and reported cause. Reporting requirements include events resulting in damages exceeding the applicable reporting threshold for the year in which the event occurred.
- The dataset is available in a human-readable format and can be accessed through the USDOT data portal. Users can explore the records online and obtain the data for further analysis through downloadable formats such as CSV and available data-access interfaces.
- In this project, the dataset serves as the primary source of accident information. It is used to identify derailments, examine their reported causes, and analyze how accident patterns vary across railroads and over time.
- The accompanying data dictionary documents the dataset's fields and their definitions, supporting the interpretation and selection of relevant variables for the analysis.

### 2. FRA Operational Data 1.02
- Official report name: Operational Data 1.02
- Original source: https://data.transportation.gov/stories/s/Operational-Data-1-02-/b39d-rg8e/
- Data query interface: https://explore.dot.gov/vizql/v_202532603161545/javascripts/hybrid-window/min/index.html?id=1k4jguhsn%24y5so-y7-oe-ay-a4vigd&moduleId=view_data
-Operational Data 1.02 is a report provided by the FRA containing railroad operational statistics reported to the agency. These data describe the volume of railroad activity and include measures such as train miles, employee hours worked, yard switching miles, passengers transported, passenger miles, and the number of individual reports submitted.
- Unlike the accident dataset, which documents specific events, Operational Data 1.02 provides measures of railroad activity that help describe the operational context in which accidents occur. Train miles are particularly relevant to this project because they can be used as an exposure measure when calculating derailment rates.
- The report's default display covers one year of data, and the published data are presented per railroad per month, filed under each railroad's headquarters location.Therefore, the company and temporal resolution of the operational data must be considered when combining them with the accident records.
- In this project, Operational Data 1.02 is used as the source of operational exposure data. The goal is to calculate derailment rates per million train miles and compare accident patterns over time and, where the available data support it, across railroads.
- The operational dataset complements the Form 54 records by providing a denominator for rate calculations, allowing the analysis to consider not only the number of derailments but also the amount of railroad activity.

### Data Integration
- The two datasets serve different purposes and must be processed separately before they can be combined. Accident records are event-based, whereas operational statistics summarize railroad activity over a defined reporting period. Before calculating rates, the project must ensure that the accident counts and train-mile totals refer to compatible time periods and populations of railroad operations.
- To connect both datasets, we joined the railroad group and year, after each table is aggregated.
- The data dictionaries and source documentation will be used to interpret variables, identify missing information, and document the assumptions applied during data cleaning and analysis.


### Findings
![Derailments per million train miles by railroad, 2014-2022](artifacts/derailments_over_time.png)
![Derailments per million train miles by railroad](artifacts/derailments_by_cause.png)
![Change in rate of derailments by railroad from early period to late period](artifacts/changes_between_periods.png)




### Methodology
From Will: Rate = derailments / (Total Train Miles(TTM)/1,000,000) TTM includes Yard Switching Miles.
Groups: tope 7 railroads by parent company plus other (BNSF, UP, NS, CSX, CPKC, CN, NJTR)
Rate over time = one rate per railroad per year, summed of the four cause rates.
causes by railroad: years combined, derailments summed over years/ miles summed over years. Each railroad-year's miles counted once.
change chart - '14 - '16 vs -'20 - '22 rates, percent change = (late-early)/early * 100
cause groups: Signal merged with miscellaneous due to low numbers - would not be significantly shown if kept separate.

### Limitations
- A key limitation is that Operational Data 1.02 is published per railroad according to the data. Therefore, regional derailment rates require operational exposure data broken down by the corresponding FRA regions. If suitable regional train-mile data are unavailable, per-railroad rates can still be calculated, but they cannot be interpreted as regional rates. The project will document this limitation and adjust the analysis to match the geographic resolution supported by the data.
- Miles by state, region, or line do not exist and so accident data cannot be used alongside operational data to find geographical differences.
- Amtrak, the national passenger railroad service, is not included in the data set
- Only accidents above a certain amount are reported to the FRA. If it's below the set threshold per year ($10,500-$11,300 depending on the year).
- Percent changes assume a non-zero early-period rate, and NJT's small counts make the percentages volatile compared to the other railroads.
- NJTR has a small absolute count and is a passenger railroad with different behavior than the other major railroads.
- The percent change in the period comparison graph assumes a non-zero early rate.
- "Per million miles" for all statistics includes yard switching miles.
