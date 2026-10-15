# Analyzing U.S. and Canadian Train Derailments

### bevo_big_data

# Goal of Analysis
The goal of this project is to analyze train derailments reported by the FRA from 2014-2022. Specifically we want to identify annual fluctuations in train derailments and their associated causes across different railroad companies for the years spanning from 2014 to 2022.

## Data Sources and Data Collection
This project uses two datasets provided by the Federal Railroad Administration (FRA), an agency of the U.S. Department of Transportation (USDOT). The datasets provide complementary information: one records reportable railroad accidents and incidents, while the other contains operational data that can be used to measure railroad activity. Combining these sources allows the analysis of accident trends in relation to operational exposure.

### 1. FRA Rail Equipment Accident/Incident Data (Form 54)
Official dataset name: Rail Equipment Accident/Incident Data (Form 54)
Original source: https://data.transportation.gov/Railroads/Rail-Equipment-Accident-Incident-Data-Form-54-/85tf-25kj/data_preview
Data dictionary: https://data.transportation.gov/Railroads/Rail-Equipment-Accident-Incident-Data-Form-54-/85tf-25kj/about_data
The Rail Equipment Accident/Incident Data (Form 54) is a publicly available dataset maintained by the Federal Railroad Administration (FRA). It contains records of reportable railroad equipment accidents and incidents in the United States, including derailments, collisions, fires, explosions, and other events involving railroad on-track equipment, whether standing or moving.
Under federal reporting requirements, railroads must report qualifying accidents and incidents to the FRA using Form FRA 6180.54 — Rail Equipment Accident/Incident. These reports include information about the event, such as its date, location, equipment involved, accident characteristics, and reported cause. Reporting requirements include events resulting in damages exceeding the applicable reporting threshold for the year in which the event occurred.
The dataset is available in a human-readable format and can be accessed through the USDOT data portal. Users can explore the records online and obtain the data for further analysis through downloadable formats such as CSV and available data-access interfaces.
In this project, the dataset serves as the primary source of accident information. It is used to identify derailments, examine their reported causes, and analyze how accident patterns vary across FRA regions and over time.
The accompanying data dictionary documents the dataset's fields and their definitions, supporting the interpretation and selection of relevant variables for the analysis.

### 2. FRA Operational Data 1.02
Official report name: Operational Data 1.02
Original source: https://data.transportation.gov/stories/s/Operational-Data-1-02-/b39d-rg8e/
Data query interface: ttps://explore.dot.gov/vizql/v_202532603161545/javascripts/hybrid-window/min/index.html?id=1k4jguhsn%24y5so-y7-oe-ay-a4vigd&moduleId=view_data
Operational Data 1.02 is a report provided by the FRA containing railroad operational statistics reported to the agency. These data describe the volume of railroad activity and include measures such as train miles, employee hours worked, yard switching miles, passengers transported, passenger miles, and the number of individual reports submitted.
Unlike the accident dataset, which documents specific events, Operational Data 1.02 provides measures of railroad activity that help describe the operational context in which accidents occur. Train miles are particularly relevant to this project because they can be used as an exposure measure when calculating derailment rates.
The report's default display covers one year of data, and the published data are presented at the U.S. national level, rather than at the state, county, or city level. Therefore, the geographic and temporal resolution of the operational data must be considered when combining them with the accident records.
In this project, Operational Data 1.02 is used as the source of operational exposure data. The goal is to calculate derailment rates per million train miles and compare accident patterns over time and, where the available data support it, across FRA regions.
The operational dataset complements the Form 54 records by providing a denominator for rate calculations, allowing the analysis to consider not only the number of derailments but also the amount of railroad activity.

### Data Integration and Limitations
The two datasets serve different purposes and must be processed separately before they can be combined. Accident records are event-based, whereas operational statistics summarize railroad activity over a defined reporting period. Before calculating rates, the project must ensure that the accident counts and train-mile totals refer to compatible time periods and populations of railroad operations.
To connect both dataset is needed to use “Railroad Name” column
A key limitation is that Operational Data 1.02 is published at the national level according to its documentation. Therefore, regional derailment rates require operational exposure data broken down by the corresponding FRA regions. If suitable regional train-mile data are unavailable, national-level rates can still be calculated, but they cannot be interpreted as regional rates. The project will document this limitation and adjust the analysis to match the geographic resolution supported by the data.
The data dictionaries and source documentation will be used to interpret variables, identify missing information, and document the assumptions applied during data cleaning and analysis.


### Limitations

From Will: Percent changes assume a non-zero early-period rate, and NJT's small counts make the percentages volatile compared to the other railroads.
NJTR has a small count and is a passenger vs the other majors are freight
percent change assumes a non-zero early rate
"per million miles" includes yard switching.

### Methodology
From Will: Rate = derailments / (Total Train Miles(TTM)/1,000,000) TTM includes Yard Switching Miles.
Groups: tope 7 railroads by parent company plus other (BNSF, UP, NS, CSX, CPKC, CN, NJTR)
Rate over time = one rate per railroad per year, summed of the four cause rates.
causes by railroad: years combined, derailments summed over years/ miles summed over years. Each railroad-year's miles counted once.
change chart - '14 - '16 vs -'20 - '22 rates, percent change = (late-early)/early * 100
cause groups: Signal merged with miscellaneous due to low numbers - would not be significantly shown if kept separate.

### Findings
