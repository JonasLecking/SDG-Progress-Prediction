import pandas as pd
import numpy as np
import fbprophet as prophet
import os

raw_data = pd.read_excel("Raw Trend Data.xlsx")
codebook = pd.read_excel("Codebook.xlsx")

distinct_countries = raw_data["Country"].unique()
distinct_years = raw_data["Year"].unique()
distinct_targets = raw_data.columns[4:-1]
covered_targets = codebook["Indicator"].unique()

targets = []

for target in distinct_targets:
    if target in covered_targets:
        targets.append(target)

##### GLOBAL ANALYSIS #######

df = pd.DataFrame(columns=distinct_years, index=targets)

for year in distinct_years:
    
    selection = raw_data.loc[raw_data["Year"] == year]
    selection.set_index("Country", inplace=True)
    total_pop = sum(selection["Population"].to_list())
        
    for target in targets:

        weighted_value = 0
        total_pop_target = 0

        for country in selection.index.unique():
            population = selection.at[country, "Population"]
            value = selection.at[country, target]

            if not np.isnan(value):
                total_pop_target = total_pop_target + population
        
        for country in selection.index.unique():
            population = selection.at[country, "Population"]
            value = selection.at[country, target]

            if not np.isnan(value):
                weighted_value = weighted_value + value * (population/total_pop_target)

        #print(target + " | " + str(year) + " | " + str(weighted_value))

        if float(weighted_value) == float(0):
            df.at[target, year] = np.nan
        else:
            df.at[target, year] = weighted_value


df2 = pd.DataFrame(columns=["2023", "2023 Upper Bound (95%)", "2023 Lower Bound (95%)", "Description",
                            "Optimum (= 100 Points)", "Minimum (= 0 Points)", "Green Threshold (On Track)", "Red Threshold (Far Off)"],index=targets)
codebook.set_index("Indicator", inplace=True)

for (index, row) in df.iterrows():
    predict_df = pd.DataFrame(list(row))
    predict_df["y"] = predict_df[0]
    predict_df["ds"] = predict_df.index
    predict_df.drop([0], inplace=True)
    predict_df["ds"] = pd.to_datetime(predict_df["ds"], format="%d")

    try:
        m = prophet.Prophet()                  
        m.fit(predict_df)
        future_df = m.make_future_dataframe(periods = 3)
        forecast = m.predict(future_df)
        final_value = forecast["yhat"].to_list()[-1]
        final_lower = forecast["yhat_lower"].to_list()[-1]
        final_upper = forecast["yhat_upper"].to_list()[-1]
        print(index, final_value)
        df2.at[index, "2023"] = final_value
        df2.at[index, "2023 Lower Bound (95%)"] = final_lower
        df2.at[index, "2023 Upper Bound (95%)"] = final_upper
        df2.at[index, "Description"] = codebook.at[index, "Label"]
        df2.at[index, "Optimum (= 100 Points)"] = codebook.at[index, "Optimum (= 100)"]
        df2.at[index, "Minimum (= 0 Points)"] = codebook.at[index, "Lower Bound (=0)"]
        df2.at[index, "Green Threshold (On Track)"] = codebook.at[index, "Green threshold"]
        df2.at[index, "Red Threshold (Far Off)"] = codebook.at[index, "Red threshold"]
                            
    except Exception as e:
        print(e)
        df2.at[index, "2023"] = np.nan
        df2.at[index, "2023_lower"] = np.nan
        df2.at[index, "2023_upper"] = np.nan

output_df = pd.concat([df2, df], axis=1)
output_df.to_excel("prediction_results.xlsx")

        
#### BY COUNTRY ANALYSIS THAT CAN BE RECONCILED TO ENHANCED GLOBAL PREDICTION ####
#### (Requires too much computing power; estimated runtime: 22h 50min, requires creation of > 16,000 ML models) ####
#### Note: Could be performed as batch job on Wharton Research Data Services Cloud ####

##df = pd.DataFrame(columns=targets, index=distinct_countries)
##
##for country in distinct_countries:
##
##    print(country)
##    selection = raw_data.loc[raw_data["Country"] == country]
##    selection.sort_values("Year")
##                  
##    for target in targets:
##
##        try:
##            data = selection[target]
##            predict_df = pd.DataFrame(data)
##            predict_df.reset_index(inplace=True)
##            predict_df.drop(columns=["index"], inplace=True)
##            predict_df.rename({target:"y"}, axis="columns", inplace=True)
##            predict_df["ds"] = predict_df.index + 1
##            predict_df["ds"] = pd.to_datetime(predict_df["ds"], format="%d")
##
##            try:
##                m = prophet.Prophet()
##                m.yearly_seasonality = False
##                m.daily_seasonality = False
##
##                if m.n_changepoints > len(predict_df):
##                    m.n_changepoints = len(predict_df) - 1
##                            
##                m.fit(predict_df)
##                future_df = m.make_future_dataframe(periods = 3)
##                forecast = m.predict(future_df)
##                final_value = forecast["yhat"].to_list()[-1]
##                df.at[country, target] = final_value
##                print(country + " | " + target + " | " + str(final_value))
##                            
##            except:
##                df.at[country, target] = np.nan
##                print(country + " | " + target + " | " + "Too many NaN.")
##        except:
##            df.at[country, target] = np.nan
##            print(country + " | " + target + " | " + "Error.")


#df.to_excel("results.xlsx")
        

    

    
        
        
        
            


    

