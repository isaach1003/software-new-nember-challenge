#python 3.13, pandas 2.3.3, numpy 2.3.4
import pandas as pd
import numpy as np
import glob
import json

def ffmt(flt: float, decimals: int=3) -> str: #formats float for json and rounding
    return f"{float(flt):.{decimals}f}"
    

def driver_analysis(df_driver: pd.DataFrame) -> dict:
    df_driver = df_driver.sort_values('lap_number')  #for sectors

    fastest_row = df_driver.loc[df_driver['time'].idxmin()]
    fastest_lap = fastest_row['lap_number']
    fastest_time = fastest_row['time']


    sectors_columns = sorted(df_driver.filter(like="sector").columns)  #trying to maintain scalability if needed
    sectors = {col: ffmt(fastest_row[col]) for col in sectors_columns}


    if df_driver.shape[0] > 1:  #checks to make sure there are multiple times, otherwise slope is 0 (to avoid errors with polyfit)
        y = df_driver['time'].values
        x = df_driver['lap_number'].values
        slope, _ = np.polyfit(x, y, 1)
    else:
        slope = 0

    trend = "Improving" if slope < -0.05 else "Degrading" if slope > 0.05 else "Stable"

    if trend == "Stable":
        trend_des = "Lap times remain consistent"
    else:
        trend_des = f"Lap times {'decreasing' if trend == 'Improving' else 'increasing'} by {abs(slope):.2f}s per lap on average"


    average_pace = df_driver['time'].mean()
    consistency = df_driver['time'].std(ddof=0)
    consistency_rating = 'Excellent' if consistency < 0.5 else 'Good' if consistency < 1.5 else 'Needs Improvement'

    return {
        "fastest_lap": {
            "lap_number": int(fastest_lap),  #converting for json formatting
            "time": ffmt(fastest_time),
            "sector_times": sectors,
        },
        "average_pace": ffmt(average_pace),
        "consistency_rating": {
            "standard_deviation": ffmt(consistency),
            "rating": consistency_rating
        },
        "trend": {
            "type": trend,
            "slope": ffmt(slope),
            "description": trend_des,
        },
    }

def lap_time_analysis(df: pd.DataFrame) -> dict:
    drivers = {}

    for driver in df['driver'].unique():
        driver_df = df[df['driver'] == driver].copy()
        drivers[driver] = driver_analysis(driver_df)

    # ------ summary ------

    #sectors
    sectors_summary = {}
    for col in df.filter(like="sector").columns: #also for scalibitiy
        fastest_sector_rows = df[df[col] == df[col].min()] #keep only fastest rows (ties)
        sectors_summary[f"fastest_{col}"] = {
            "driver(s)": fastest_sector_rows['driver'].unique().tolist(),
            "lap_number(s)": fastest_sector_rows['lap_number'].unique().tolist(),
            "time": ffmt(fastest_sector_rows['time'].iloc[0]) #aka .min()
        }

    #overall fastest
    fastest_rows = df[df['time'] == df['time'].min()]
    overall_fastest = {
        "overall_fastest_lap": {
            "driver(s)": fastest_rows['driver'].unique().tolist(),
            "lap_number(s)": fastest_rows['lap_number'].unique().tolist(),
            "time": ffmt(fastest_rows['time'].iloc[0])
        }
    }

    summary = {
        "total_laps_analyzed": int(df.shape[0]),
        "drivers_count": len(drivers),
        **sectors_summary,
        **overall_fastest
    }


    return {"drivers": drivers, "summary": summary}

#start of test files
test_cases_files = glob.glob('test_cases/in/*.csv')
for i, f in enumerate(test_cases_files, start=1):
    file_info = lap_time_analysis(pd.read_csv(f))
    with open(f"out/out_{i}.json", "w") as out_f:
        json.dump(file_info, out_f, indent=4)
#end of test files

'''        
df = pd.readcsv(in/data.csv)
analysis = lap_time_analysis(df)
with open(f"out/out.json", "w") as out_f:
    json.dump(analysis, out_f, indent=4)
'''

