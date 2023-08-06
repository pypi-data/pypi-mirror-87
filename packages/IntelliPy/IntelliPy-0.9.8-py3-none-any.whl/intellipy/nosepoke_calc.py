import pandas as pd
import numpy as np
def learning_rate_non_sucrose(df, path, phase, group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod=""):
    # create out path
    out_path = path + "/" + phase + "_nosepoke_learning_Data" + nameMod + ".xlsx"

    df["hourIntervall"] = df["StartTimecode"] // 3600

    # create df_licked with only those entries that were incorrect or correct and followed by a lick --> lickduration > 0
    df_temp = df[(df["SideCondition"] == "Incorrect") | (df["LickDuration"] > 0)]
    df_licked = df_temp.copy()

    df["CorrectNoLick"] = np.where((df["SideCondition"] == "Correct") & (df["LickDuration"] == 0), 1, 0)
    df["CorrectAndLick"] = np.where((df["SideCondition"] == "Correct") & (df["LickDuration"] > 0), 1, 0)

    df["NosepokePerAnimal"] = df.groupby("Animal")["VisitID"].expanding().count().reset_index(0)["VisitID"]
    df_licked["NosepokePerAnimal"] = df_licked.groupby("Animal")["VisitID"].expanding().count().reset_index(0)[
        "VisitID"]

    # code 1/0 for Correct, Sucrose and NotIncorrect
    df["Correct"] = np.where(df["SideCondition"] == "Correct", 1, 0)
    df_licked["Correct"] = np.where(df_licked["SideCondition"] == "Correct", 1, 0)

    # now sum it up
    df["cumCorrectNoLick"] = df.groupby("Animal")["CorrectNoLick"].expanding().sum().reset_index(0)["CorrectNoLick"]
    df["cumCorrectAndLick"] = df.groupby("Animal")["CorrectAndLick"].expanding().sum().reset_index(0)["CorrectAndLick"]
    df["cumCorrectNosepokes"] = df.groupby("Animal")["Correct"].expanding().sum().reset_index(0)["Correct"]
    df["cumNosepokes"] = df.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)["NosepokePerAnimal"]
    df_licked["cumCorrectNosepokes"] = df_licked.groupby("Animal")["Correct"].expanding().sum().reset_index(0)["Correct"]
    df_licked["cumNosepokes"] = df_licked.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)["NosepokePerAnimal"]

    df["cumCorrectNosepokesRate"] = df["cumCorrectNosepokes"] / df["cumNosepokes"]
    df["cumCorrectNoLickRate"] = df["cumCorrectNoLick"] / df["cumNosepokes"]
    df["cumCorrectAndLickRate"] = df["cumCorrectAndLick"] / df["cumNosepokes"]
    df_licked["cumCorrectNosepokesRate"] = df_licked["cumCorrectNosepokes"] / df_licked["cumNosepokes"]

    # fill with previous value
    df_filled = df.copy()
    df_filled.fillna(method="ffill", inplace=True)
    df_hour = df_filled.drop_duplicates(subset=["Animal", "hourIntervall"], keep="last")

    df_licked_filled = df_licked.copy()
    df_licked_filled.fillna(method="ffill", inplace=True)
    df_licked_hour = df_licked_filled.drop_duplicates(subset=["Animal", "hourIntervall"], keep="last")

    df_pivotHourCorrect = df_hour.pivot(index="hourIntervall", columns="Animal", values="cumCorrectNosepokesRate")
    df_pivotHourCorrect.fillna(method="ffill", inplace=True)

    df_licked_pivotHourCorrect = df_licked_hour.pivot(index="hourIntervall", columns="Animal",
                                                      values="cumCorrectNosepokesRate")
    df_licked_pivotHourCorrect.fillna(method="ffill", inplace=True)

    df_pivotNosepokeCorrect = df.pivot(index="NosepokePerAnimal", columns="Animal", values="cumCorrectNosepokesRate")
    df_pivotNosepokeCorrect.fillna(method="ffill", inplace=True)

    df_licked_pivotNosepokeCorrect = df_licked.pivot(index="NosepokePerAnimal", columns="Animal",
                                                     values="cumCorrectNosepokesRate")
    df_licked_pivotNosepokeCorrect.fillna(method="ffill", inplace=True)

    df_pivotNPCorrectNoLick = df.pivot(index="NosepokePerAnimal", columns="Animal", values="cumCorrectNoLickRate")
    df_pivotNPCorrectNoLick.fillna(method="ffill", inplace=True)

    df_pivotHourCorrectNoLick = df_hour.pivot(index="hourIntervall", columns="Animal", values="cumCorrectNoLickRate")
    df_pivotHourCorrectNoLick.fillna(method="ffill", inplace=True)

    df_pivotNPCorrectAndLick = df.pivot(index="NosepokePerAnimal", columns="Animal", values="cumCorrectAndLickRate")
    df_pivotNPCorrectAndLick.fillna(method="ffill", inplace=True)

    df_pivotHourCorrectAndLick = df_hour.pivot(index="hourIntervall", columns="Animal", values="cumCorrectAndLickRate")
    df_pivotHourCorrectAndLick.fillna(method="ffill", inplace=True)

    df_licked_pivotNosepokeCorrect_transposed = df_licked_pivotNosepokeCorrect.transpose()
    df_licked_pivotHourCorrect_transposed = df_licked_pivotHourCorrect.transpose()
    df_pivotNosepokeCorrect_transposed = df_pivotNosepokeCorrect.transpose()
    df_pivotHourCorrect_transposed = df_pivotHourCorrect.transpose()
    df_pivotNPCorrectNoLick_transposed = df_pivotNPCorrectNoLick.transpose()
    df_pivotHourCorrectNoLick_transposed = df_pivotHourCorrectNoLick.transpose()
    df_pivotNPCorrectAndLick_transposed = df_pivotNPCorrectAndLick.transpose()
    df_pivotHourCorrectAndLick_transposed = df_pivotHourCorrectAndLick.transpose()

    all_dfs = [df_licked_pivotNosepokeCorrect_transposed, df_licked_pivotHourCorrect_transposed,
               df_pivotNosepokeCorrect_transposed, df_pivotHourCorrect_transposed, df_pivotNPCorrectNoLick_transposed,
               df_pivotHourCorrectNoLick_transposed, df_pivotNPCorrectAndLick_transposed, df_pivotHourCorrectAndLick_transposed]

    for curr_df in all_dfs:
        for name, animals in group_dict.items():
            rowname = "Mean" + name
            curr_df.loc[rowname] = curr_df.loc[animals].mean()

    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    df_pivotNosepokeCorrect_transposed.to_excel(writer, sheet_name="CorrectNosepokeRate", startrow=0, startcol=0)
    df_pivotHourCorrect_transposed.to_excel(writer, sheet_name="CorrectNosepokeRateHour", startrow=0, startcol=0)
    if no_lick_ex:
        df_licked_pivotNosepokeCorrect_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickEx", startrow=0,
                                                       startcol=0)
        df_licked_pivotHourCorrect_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickEx_hour", startrow=0,
                                                   startcol=0)
    if no_lick_rem:
        df_pivotNPCorrectAndLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickIncorr", startrow=0,
                                                       startcol=0)
        df_pivotHourCorrectAndLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickIncorrHour", startrow=0,
                                                       startcol=0)
    if no_lick_only:
        df_pivotNPCorrectNoLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickOnly", startrow=0,
                                                      startcol=0)
        df_pivotHourCorrectNoLick_transposed.to_excel(writer, sheet_name="CorrNPRate_NoLickOnlyHour", startrow=0,
                                                      startcol=0)

    sheets = ["CorrectNosepokeRate", "CorrectNosepokeRateHour"]
    if no_lick_ex:
        sheets.extend(["CorrNPRate_NoLickEx", "CorrNPRate_NoLickEx_hour"])
    if no_lick_rem:
        sheets.extend(["CorrNPRate_NoLickIncorr", "CorrNPRate_NoLickIncorrHour"])
    if no_lick_only:
        sheets.extend(["CorrNPRate_NoLickOnly", "CorrNPRate_NoLickOnlyHour"])


    tables = [df_pivotNosepokeCorrect_transposed, df_pivotHourCorrect_transposed]
    if no_lick_ex:
        tables.extend([df_licked_pivotNosepokeCorrect_transposed, df_licked_pivotHourCorrect_transposed])
    if no_lick_rem:
        tables.extend([df_pivotNPCorrectAndLick_transposed, df_pivotHourCorrectAndLick_transposed])
    if no_lick_only:
        tables.extend([df_pivotNPCorrectNoLick_transposed, df_pivotHourCorrectNoLick_transposed])


    for i in range(len(sheets)):
        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        workbook = writer.book
        worksheet = writer.sheets[sheets[i]]

        # Create a chart object
        chart = workbook.add_chart({'type': 'line'})

        # Configure the series of the chart from the dataframe data
        for j in range(len(tables[i].index) - 6):
            row = j + 1
            chart.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, 1, 0, len(tables[i].index) - 6],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })

        worksheet.insert_chart('A35', chart)
        chart2 = workbook.add_chart({'type': 'line'})

        for j in range(len(tables[i].index) - 6, len(tables[i].index)):
            row = j + 1
            chart2.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, len(tables[i].index) - 6, 0, len(tables[i].index)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })
        worksheet.insert_chart('M35', chart2)
    writer.save()
    print(out_path + " written")


def learning_rate_sucrose(df, path, group_dict, no_lick_ex, no_lick_rem, no_lick_only, water_y_suc_n, water_y_suc_y, water_n_suc_y, sucrose_label):

    if water_y_suc_n:
        df_yn = df.copy()
        df_yn["SideCondition"] = df_yn["SideCondition"].replace([sucrose_label], "Incorrect")
        learning_rate_non_sucrose(df_yn, path, "SucrosePreference", group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod="_OnlyWaterCorrect")
    if water_y_suc_y:
        df_yy = df.copy()
        df_yy["SideCondition"] = df_yy["SideCondition"].replace([sucrose_label], "Correct")
        learning_rate_non_sucrose(df_yy, path, "SucrosePreference", group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod="_WaterSucroseCorrect")
    if water_n_suc_y:
        df_ny = df.copy()
        df_ny["SideCondition"] = df_ny["SideCondition"].replace(["Correct"], "Incorrect")
        df_ny["SideCondition"] = df_ny["SideCondition"].replace([sucrose_label], "Correct")
        learning_rate_non_sucrose(df_ny, path, "SucrosePreference", group_dict, no_lick_ex, no_lick_rem, no_lick_only, nameMod="_OnlySucroseCorrect")

    # create out path
    out_path = path + "/Sucrose_Preference_nosepoke_learning_Data.xlsx"

    df["hourIntervall"] = df["StartTimecode"] // 3600
    df["NosepokePerAnimal"] = df.groupby("Animal")["VisitID"].expanding().count().reset_index(0)["VisitID"]

    # now sum it up
    df["cumulativeLickDuration"] = df.groupby("Animal")["LickDuration"].expanding().sum().reset_index(0)["LickDuration"]
    df["cumNosepokes"] = df.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)[
        "NosepokePerAnimal"]

    df["cumulativeLickDurationSucrose"] = \
    df[df["SideCondition"] == sucrose_label].groupby("Animal")["LickDuration"].expanding().sum().reset_index(0)[
        "LickDuration"]

    # set all first ratios per Animal to 0
    df.loc[df.groupby('Animal', as_index=False).head(1).index, 'sucrosePerTotalLickduration'] = 0
    df.loc[df.groupby('Animal', as_index=False).head(1).index, 'cumulativeLickDurationSucrose'] = 0
    df["cumulativeLickDurationSucrose"].fillna(method="ffill", inplace=True)

    df["sucrosePerTotalLickduration"] = df["cumulativeLickDurationSucrose"] / df["cumulativeLickDuration"]

    df_l = df[df["LickDuration"] > 0].copy()
    df_l["LickDurIndex"] = df_l.groupby("Animal")["NosepokePerAnimal"].expanding().count().reset_index(0)[
        "NosepokePerAnimal"]
    df_pivot = df_l.pivot(index="LickDurIndex", columns="Animal", values="sucrosePerTotalLickduration")

    # fill with previous value
    df_pivot.fillna(method="ffill", inplace=True)
    df_filled = df.copy()
    df_filled.fillna(method="ffill", inplace=True)
    df_hour = df_filled.drop_duplicates(subset=["Animal", "hourIntervall"], keep="last")
    df_pivotHour = df_hour.pivot(index="hourIntervall", columns="Animal", values="sucrosePerTotalLickduration")
    df_pivotHour.fillna(method="ffill", inplace=True)


    # LickDuration
    df_pivot_transposed = df_pivot.transpose()
    df_pivotHour_transposed = df_pivotHour.transpose()

    all_dfs = [df_pivot_transposed, df_pivotHour_transposed]

    for curr_df in all_dfs:
        for name, animals in group_dict.items():
            rowname = "Mean" + name
            curr_df.loc[rowname] = curr_df.loc[animals].mean()


    out_path = path + "/Sucrose_Preference_sucroseRate.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')

    df_pivot_transposed.to_excel(writer, sheet_name="SucroseLickDurationRatioPerNP")
    df_pivotHour_transposed.to_excel(writer, sheet_name="SucroseLickDurationRatioPerHour")

    sheets = ["SucroseLickDurationRatioPerNP", "SucroseLickDurationRatioPerHour"]
    tables = [df_pivot_transposed, df_pivotHour_transposed]

    for i in range(len(sheets)):
        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        workbook = writer.book
        worksheet = writer.sheets[sheets[i]]

        # Create a chart object
        chart = workbook.add_chart({'type': 'line'})

        # 1 Configure the series of the chart from the dataframe data
        for j in range(len(tables[i].index) - 6):
            row = j + 1
            chart.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, 1, 0, len(tables[i].index) - 6],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })

        worksheet.insert_chart('A35', chart)
        chart2 = workbook.add_chart({'type': 'line'})

        for j in range(len(tables[i].index) - 6, len(tables[i].index)):
            row = j + 1
            chart2.add_series({
                'name': [sheets[i], row, 0],
                'categories': [sheets[i], 0, len(tables[i].index) - 6, 0, len(tables[i].index)],
                'values': [sheets[i], row, 1, row, len(tables[i].columns) + 1],
            })
        worksheet.insert_chart('M35', chart2)

    writer.save()
    print(out_path + " written")



