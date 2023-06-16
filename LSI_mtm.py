import pandas as pd
import re
import tkinter as tk
import Common_function as Lsi_func


def get_mtm_bandlist(list_file):
    Test_list = {}
    for count, file in enumerate(list_file, start=1):
        my_cols = [str(i) for i in range(20)]  # create some col names
        df_Data = pd.read_csv(file, sep="\t|,|=", names=my_cols, header=None, engine="python")
        df_Data = df_Data.iloc[:, :1]
        df_null = df_Data[df_Data["0"].isnull()].index
        df_Data.drop(df_null, inplace=True)
        Bandlist = df_Data.drop_duplicates()["0"].to_list()
        Test_list["HSPA"] = [int(re.sub(r"[^0-9]", "", x)) for x in Bandlist if x.startswith("WB")]
        Test_list["SUB6"] = [int(re.sub(r"[^0-9]", "", x)) for x in Bandlist if x.startswith("NR")]

        keys_to_delete = []
        for key, value in Test_list.items():
            if not value:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del Test_list[key]

    return Test_list


def HSPA_Rx_gain_average_mtm(df_Meas, Save_data_var, text_area):
    HSPA_RX_Gain = df_Meas[df_Meas["Item"].str.contains("_RX Gain ").to_list()]
    # grounpby 에서의 numeric_only 문제 -> astype(float)으로 변경 후 merge 하도록 수정
    HSPA_RX_Gain_Value = HSPA_RX_Gain.iloc[:, 2:].astype(float)
    HSPA_RX_Gain_Item = HSPA_RX_Gain["Item"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    HSPA_RX_Gain_Item.drop(columns=[1, 2, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    HSPA_RX_Gain_Item.columns = ["Band", "Antenna", "Path", "LNA"]
    HSPA_RX_Gain = pd.merge(HSPA_RX_Gain_Item, HSPA_RX_Gain_Value, left_index=True, right_index=True)

    HSPA_RX_Gain_Mean = round(HSPA_RX_Gain.groupby(["Band", "Antenna", "Path", "LNA"]).mean(), 2)
    HSPA_RX_Gain_Mean = pd.concat([HSPA_RX_Gain_Mean, round(HSPA_RX_Gain_Mean.mean(axis=1), 2).rename("Average")], axis=1)
    HSPA_RX_Gain_Mean = pd.concat([HSPA_RX_Gain_Mean, round(HSPA_RX_Gain_Mean.max(axis=1), 2).rename("Max")], axis=1)
    HSPA_RX_Gain_Mean = pd.concat([HSPA_RX_Gain_Mean, round(HSPA_RX_Gain_Mean.min(axis=1), 2).rename("Min")], axis=1)

    if Save_data_var.get():
        filename = "MTM_HSPA_RX_Gain.xlsx"
        with pd.ExcelWriter(filename) as writer:
            HSPA_RX_Gain_Mean.to_excel(writer, sheet_name="HSPA_RX_Gain_Mean")
        Lsi_func.WB_Format(filename, 2, 5, 0, text_area)

    return HSPA_RX_Gain_Mean["Average"]


def HSPA_Rx_freq_average_mtm(df_Meas, Save_data_var, text_area):
    HSPA_RX_Freq = df_Meas[df_Meas["Item"].str.contains(" RX FREQ ").to_list()]
    HSPA_RX_Freq_Value = HSPA_RX_Freq.iloc[:, 2:].astype(float)
    HSPA_RX_Freq_Item = HSPA_RX_Freq["Item"].str.split("_| |\\(|:|\\)", expand=True)
    # 의미없는 컬럼 삭제
    HSPA_RX_Freq_Item.drop(columns=[1, 2, 5, 6, 8], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    HSPA_RX_Freq_Item.columns = ["Band", "Antenna", "Path", "Freq"]
    HSPA_RX_Freq = pd.merge(HSPA_RX_Freq_Item, HSPA_RX_Freq_Value, left_index=True, right_index=True)

    HSPA_RX_Freq_Mean = round(HSPA_RX_Freq.groupby(["Band", "Antenna", "Path", "Freq"]).mean(), 2)
    HSPA_RX_Freq_Mean = pd.concat([HSPA_RX_Freq_Mean, round(HSPA_RX_Freq_Mean.mean(axis=1), 2).rename("Average")], axis=1)
    HSPA_RX_Freq_Mean = pd.concat([HSPA_RX_Freq_Mean, round(HSPA_RX_Freq_Mean.max(axis=1), 2).rename("Max")], axis=1)
    HSPA_RX_Freq_Mean = pd.concat([HSPA_RX_Freq_Mean, round(HSPA_RX_Freq_Mean.min(axis=1), 2).rename("Min")], axis=1)

    if Save_data_var.get():
        filename = "MTM_HSPA_RX_Freq.xlsx"
        with pd.ExcelWriter(filename) as writer:
            HSPA_RX_Freq_Mean.to_excel(writer, sheet_name="HSPA_RX_Freq_Mean")
        Lsi_func.WB_Format(filename, 2, 4, 0, text_area)

    return HSPA_RX_Freq_Mean["Average"]


def Rx_2G_gain_average_mtm(df_Meas, Save_data_var, text_area):
    GSM_RX_Gain = df_Meas[df_Meas["Item"].str.contains("_RX_AGC ").to_list()]
    GSM_RX_Gain_Value = GSM_RX_Gain.iloc[:, 2:].astype(float)
    GSM_RX_Gain_Item = GSM_RX_Gain["Item"].str.split("_| |\\[|\\]", expand=True)
    # 의미없는 컬럼 삭제
    GSM_RX_Gain_Item.drop(columns=[1, 2, 3, 4, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    GSM_RX_Gain_Item.columns = ["Band"]
    GSM_RX_Gain = pd.merge(GSM_RX_Gain_Item, GSM_RX_Gain_Value, left_index=True, right_index=True)
    GSM_RX_Gain.drop_duplicates(["Band"], keep="last", inplace=True, ignore_index=True)

    GSM_RX_Gain_Mean = round(GSM_RX_Gain.groupby(["Band"]).mean(), 2)
    GSM_RX_Gain_Mean = pd.concat([GSM_RX_Gain_Mean, round(GSM_RX_Gain_Mean.mean(axis=1), 2).rename("Average")], axis=1)
    GSM_RX_Gain_Mean = pd.concat([GSM_RX_Gain_Mean, round(GSM_RX_Gain_Mean.max(axis=1), 2).rename("Max")], axis=1)
    GSM_RX_Gain_Mean = pd.concat([GSM_RX_Gain_Mean, round(GSM_RX_Gain_Mean.min(axis=1), 2).rename("Min")], axis=1)

    if Save_data_var.get():
        filename = "MTM_GSM_RX_Gain.xlsx"
        with pd.ExcelWriter(filename) as writer:
            GSM_RX_Gain_Mean.to_excel(writer, sheet_name="GSM_RX_Gain_Mean")
        Lsi_func.WB_Format(filename, 2, 4, 0, text_area)

    return GSM_RX_Gain_Mean["Average"]


def Sub6_Rx_gain_average_mtm(df_Meas, Save_data_var, text_area):
    Sub6_RX_Gain = df_Meas[df_Meas["Item"].str.contains("_Gain_Stage").to_list()]
    Sub6_RX_Gain_Value = Sub6_RX_Gain.iloc[:, 2:].astype(float)
    Sub6_RX_Gain_Item = Sub6_RX_Gain["Item"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    Sub6_RX_Gain_Item.drop(columns=[3], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RX_Gain_Item.columns = ["Band", "Antenna", "Path", "Gain_Stage"]
    Sub6_RX_Gain = pd.merge(Sub6_RX_Gain_Item, Sub6_RX_Gain_Value, left_index=True, right_index=True)

    Sub6_RX_Gain_Mean = round(Sub6_RX_Gain.groupby(["Band", "Antenna", "Path", "Gain_Stage"]).mean(), 2)
    Sub6_RX_Gain_Mean = pd.concat([Sub6_RX_Gain_Mean, round(Sub6_RX_Gain_Mean.mean(axis=1), 2).rename("Average")], axis=1)
    Sub6_RX_Gain_Mean = pd.concat([Sub6_RX_Gain_Mean, round(Sub6_RX_Gain_Mean.max(axis=1), 2).rename("Max")], axis=1)
    Sub6_RX_Gain_Mean = pd.concat([Sub6_RX_Gain_Mean, round(Sub6_RX_Gain_Mean.min(axis=1), 2).rename("Min")], axis=1)

    Sub6_RSRP_Offset = df_Meas[df_Meas["Item"].str.contains("_RSRP_Offset").to_list()]
    Sub6_RSRP_Offset_Value = Sub6_RSRP_Offset.iloc[:, 2:].astype(float)
    Sub6_RSRP_Offset_Item = Sub6_RSRP_Offset["Item"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    Sub6_RSRP_Offset_Item.drop(columns=[3, 4], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RSRP_Offset_Item.columns = ["Band", "Antenna", "Path"]
    Sub6_RSRP_Offset = pd.merge(Sub6_RSRP_Offset_Item, Sub6_RSRP_Offset_Value, left_index=True, right_index=True)

    Sub6_RSRP_Offset_Mean = round(Sub6_RSRP_Offset.groupby(["Band", "Antenna", "Path"]).mean(), 2)
    Sub6_RSRP_Offset_Mean = pd.concat(
        [Sub6_RSRP_Offset_Mean, round(Sub6_RSRP_Offset_Mean.mean(axis=1), 2).rename("Average")], axis=1
    )
    Sub6_RSRP_Offset_Mean = pd.concat([Sub6_RSRP_Offset_Mean, round(Sub6_RSRP_Offset_Mean.max(axis=1), 2).rename("Max")], axis=1)
    Sub6_RSRP_Offset_Mean = pd.concat([Sub6_RSRP_Offset_Mean, round(Sub6_RSRP_Offset_Mean.min(axis=1), 2).rename("Min")], axis=1)

    if Save_data_var.get():
        filename = "MTM_Sub6_RX_Gain.xlsx"
        with pd.ExcelWriter(filename) as writer:
            Sub6_RX_Gain_Mean.to_excel(writer, sheet_name="Sub6_RX_Gain_Mean")
        Lsi_func.WB_Format(filename, 2, 4, 0, text_area)

        filename = "MTM_Sub6_RSRP_Offset.xlsx"
        with pd.ExcelWriter(filename) as writer:
            Sub6_RSRP_Offset_Mean.to_excel(writer, sheet_name="Sub6_RSRP_Offset_Mean")
        Lsi_func.WB_Format(filename, 2, 4, 0, text_area)

    return Sub6_RX_Gain_Mean["Average"], Sub6_RSRP_Offset_Mean["Average"]


def Sub6_Rx_freq_average_mtm(df_Meas, Save_data_var, text_area):
    Sub6_RX_Freq_CA = df_Meas[df_Meas["Item"].str.contains("_CA1")]
    df_Meas.drop(df_Meas[df_Meas["Item"].str.contains("_CA1")].index, inplace=True)

    if Sub6_RX_Freq_CA.empty:
        Sub6_RX_Freq_CA_Item = pd.DataFrame()
        Sub6_RX_Freq_CA_Value = pd.DataFrame()
    else:
        Sub6_RX_Freq_CA_Value = Sub6_RX_Freq_CA.iloc[:, 2:].astype(float)
        Sub6_RX_Freq_CA_Item = Sub6_RX_Freq_CA["Item"].str.split("\[([^]]+)\]", expand=True)
        CA_Item1 = Sub6_RX_Freq_CA_Item[0].str.split("_", expand=True)
        CA_Item2 = Sub6_RX_Freq_CA_Item[1].str.split(" ", expand=True)
        Sub6_RX_Freq_CA_Item = pd.merge(CA_Item1, CA_Item2, left_index=True, right_index=True)
        # 의미없는 컬럼 삭제
        Sub6_RX_Freq_CA_Item.drop(columns=[4, "1_y"], inplace=True)
        # groupby 실행을 위한 컬럼명 변경
        Sub6_RX_Freq_CA_Item.columns = ["Band", "CA", "Antenna", "Path", "Freq"]

    Sub6_RX_Freq = df_Meas[df_Meas["Item"].str.contains("RX_Offset ").to_list()]
    Sub6_RX_Freq_Value = Sub6_RX_Freq.iloc[:, 2:].astype(float)
    Sub6_RX_Freq_Item = Sub6_RX_Freq["Item"].str.split("\[([^]]+)\]", expand=True)
    Item1 = Sub6_RX_Freq_Item[0].str.split("_", expand=True)
    Item1.insert(1, "NonCA", "NonCA")
    Item1.columns = range(5)
    Item2 = Sub6_RX_Freq_Item[1].str.split(" ", expand=True)
    Sub6_RX_Freq_Item = pd.merge(Item1, Item2, left_index=True, right_index=True)
    # 의미없는 컬럼 삭제
    Sub6_RX_Freq_Item.drop(columns=[4, "1_y"], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RX_Freq_Item.columns = ["Band", "CA", "Antenna", "Path", "Freq"]

    New_Sub6_RX_Freq_Item = pd.concat([Sub6_RX_Freq_CA_Item, Sub6_RX_Freq_Item], axis=0)
    New_Sub6_RX_Freq_Value = pd.concat([Sub6_RX_Freq_CA_Value, Sub6_RX_Freq_Value], axis=0)
    Sub6_RX_Freq = pd.merge(New_Sub6_RX_Freq_Item, New_Sub6_RX_Freq_Value, left_index=True, right_index=True)

    Sub6_RX_Freq_Mean = round(Sub6_RX_Freq.groupby(["Band", "CA", "Antenna", "Path", "Freq"]).mean(), 2)
    Sub6_RX_Freq_Mean = pd.concat([Sub6_RX_Freq_Mean, round(Sub6_RX_Freq_Mean.mean(axis=1), 2).rename("Average")], axis=1)
    Sub6_RX_Freq_Mean = pd.concat([Sub6_RX_Freq_Mean, round(Sub6_RX_Freq_Mean.max(axis=1), 2).rename("Max")], axis=1)
    Sub6_RX_Freq_Mean = pd.concat([Sub6_RX_Freq_Mean, round(Sub6_RX_Freq_Mean.min(axis=1), 2).rename("Min")], axis=1)

    if Save_data_var.get():
        filename = "MTM_Sub6_RX_Freq.xlsx"
        with pd.ExcelWriter(filename) as writer:
            Sub6_RX_Freq_Mean.to_excel(writer, sheet_name="Sub6_RX_Freq_Mean")
        Lsi_func.WB_Format(filename, 2, 5, 0, text_area)

    return Sub6_RX_Freq_Mean["Average"]


def Sub6_Rx_mixer_average_mtm(df_Meas, Save_data_var, text_area):
    Sub6_RX_Mixer = df_Meas[df_Meas["Item"].str.contains("_Mixer").to_list()]
    Sub6_RX_Mixer_Value = Sub6_RX_Mixer.iloc[:, 2:].astype(float)
    Sub6_RX_Mixer_Item = Sub6_RX_Mixer["Item"].str.split("[_Mixer| ]", expand=True)
    # 의미없는 컬럼 삭제
    Sub6_RX_Mixer_Item.drop(columns=[1, 2, 3, 4, 5, 8], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RX_Mixer_Item.columns = ["Band", "Mixer", "Path"]
    Sub6_RX_Mixer = pd.merge(Sub6_RX_Mixer_Item, Sub6_RX_Mixer_Value, left_index=True, right_index=True)

    Sub6_RX_Mixer_Mean = round(Sub6_RX_Mixer.groupby(["Band", "Mixer", "Path"]).mean(), 2)
    Sub6_RX_Mixer_Mean = pd.concat([Sub6_RX_Mixer_Mean, round(Sub6_RX_Mixer_Mean.mean(axis=1), 2).rename("Average")], axis=1)
    Sub6_RX_Mixer_Mean = pd.concat([Sub6_RX_Mixer_Mean, round(Sub6_RX_Mixer_Mean.max(axis=1), 2).rename("Max")], axis=1)
    Sub6_RX_Mixer_Mean = pd.concat([Sub6_RX_Mixer_Mean, round(Sub6_RX_Mixer_Mean.min(axis=1), 2).rename("Min")], axis=1)

    if Save_data_var.get():
        filename = "MTM_Sub6_RX_Mixer.xlsx"
        with pd.ExcelWriter(filename) as writer:
            Sub6_RX_Mixer_Mean.to_excel(writer, sheet_name="Sub6_RX_Mixer_Mean")
        Lsi_func.WB_Format(filename, 2, 4, 0, text_area)

    return Sub6_RX_Mixer_Mean["Average"]