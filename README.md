# Prediction of progress towards UN SDGs

As part of the module "Global Environment of Business" at Warwick Business School (led by Dr Frederick Dahlmann), this repository contains a tool to predict the progress towards achieving the UN SDGs.
Specifically, it uses additive prediction models to forecast the progress towards each SDG indicator in 192 countries until any given year after 2020 and before 2030. This data is reconciled to a global forecast by weighting each country/target combination's prediction with the country's population as a percentage of the global population.
The underlying data comes from the Sustainable Development Report 2020, created by the Bertelsmann Stiftung in conjunction with the Sustainable Development Solutions Network.


The dataset used can be found here: https://github.com/sdsna/SDR2020. Given that the format of the data doesn't vary too much from year to year, it can be replaced by any year's SDR. Note: from the SDR report's Excel dataset file, save sheats "Codebook" and "Raw Data" as separate .xlsx files for the analysis to work.
