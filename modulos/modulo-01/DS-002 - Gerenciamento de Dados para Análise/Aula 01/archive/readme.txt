Dataset Name: Dengue Cases in Brazil, 2012-2021

File format: Comma Seperated Values (CSV)

Dataset Files and Decriptions:
	- Brazil_Dengue_Model_Data_w_pop.csv
		- Dengue Data for Brazil as a whole country, 2012 - 2021
	- State_Dengue_Model_Data_w_pop.csv
		- Dengue Data for Individual States / Federative Units in Brazil, 2012 - 2021

Dataset Sources: 
	- Records of Dengue Cases in Brazil: Brazilian Government’s Sistema de Informação de Agravos de Notificação (SINAN)
		-URL Link: https://data.mendeley.com/datasets/2d3kr8zynf/4
	- Brazil State Codes / Federative Unit Codes: Brazilian Government’s Instituto Brasileiro de Geografia e Estatística (IBGE)
		-URL Link: https://github.com/datasets-br/state-codes
	- Evironmental Data in Brazil (Temperature and Percipitation): World Bank Climate Knowledge
		-URL Link: https://climateknowledgeportal.worldbank.org/country/brazil/climate-data-historical
	- Brazil Population Data: Brazilian Government’s Instituto Brasileiro de Geografia e Estatística (IBGE)
		-URL Link: https://www.ibge.gov.br/en/statistics/social/population/18448-estimates-of-resident-population-for-municipalities-and-federation-units.html?edicao=28688&t=conceitos-e-metodos

Dataset Managers: 
	- Jimmy Zhang | jz876@drexel.edu
	- Jonathan Watkins | jfw68@drexel.edu
	- Jascha Brettschneider | jmb598@drexel.edu

Column Headers:
	Year - a Year Between 2012 and 2021
	State - Brazil or a Brazillian State / Federative Unit
	Mean_Tmp - Mean Temperature in Degrees Celsius
	Min_Tmp - Min Temperature in Degrees Celsius
	Max_Tmp - Max Temperature in Degrees Celsius
	Percipitation - Annual Percipitation Given in Millimeters
	Change_Tmp - Max_Tmp minus Min_Temp in Degrees Celsius
	State_ID - Abbreviation for State / Federative Unit
	Cases - Number of Recorded Dengue Cases
	Region - Directional Location Relative to Brazil's Center. Possible Values: North (N), Northeast (NE), Center-West (CO), Southeast (SE), South (S)
	State_Area(km2) - Area of State / Federative Unit Given in Squared Kilometers
	Population - Estimation of Total Population
