import re
import tkinter as tk

import numpy as np


def chng_sub6_et_psat_pgain(
    Selected_spc,
    rat,
    band,
    ET_Psat_var,
    ETSAPT_Psat_Ave,
    ETSAPT_Psat_Max,
    ETSAPT_Psat_Min,
    ET_Pgain_var,
    ETSAPT_Pgain_Ave,
    ETSAPT_Pgain_Max,
    ETSAPT_Pgain_Min,
    text_area,
):
    ET_Psat = int(ET_Psat_var.get())  # 1dB = 100
    ET_Pgain = int(ET_Pgain_var.get())  # 1dB = 100
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_ET_S-APT_Psat"):
            New_String = Old_String = line
            New_String = sub6_et_psat_pgain(line, band, ET_Psat, ETSAPT_Psat_Ave, ETSAPT_Psat_Min, ETSAPT_Psat_Max, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX_ET_S-APT_Pgain"):
            New_String = Old_String = line
            New_String = sub6_et_psat_pgain(
                line, band, ET_Pgain, ETSAPT_Pgain_Ave, ETSAPT_Pgain_Min, ETSAPT_Pgain_Max, text_area
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_ET_S-APT_Psat"):
            New_String = Old_String = line
            New_String = sub6_et_psat_pgain(line, band, ET_Psat, ETSAPT_Psat_Ave, ETSAPT_Psat_Min, ETSAPT_Psat_Max, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_ET_S-APT_Pgain"):
            New_String = Old_String = line
            New_String = sub6_et_psat_pgain(
                line, band, ET_Pgain, ETSAPT_Pgain_Ave, ETSAPT_Pgain_Min, ETSAPT_Pgain_Max, text_area
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_DC_I	="):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_et_psat_pgain(line, band, Spec, df1, df2, df3, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    text_area.insert(
        tk.END,
        f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
    )
    text_area.see(tk.END)

    if df1.get(band) is not None:
        if df1[band].get(Path) is not None:
            New_String[2] = round(df1[band, Path])
        else:
            New_String[2] = 0
    else:
        New_String[2] = 0

    New_String[3] = New_String[2] - Spec
    New_String[4] = New_String[2] + Spec

    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_et_freq(Selected_spc, rat, band, ET_Freq_var, ETSAPT_Freq_Ave, ETSAPT_Freq_Max, ETSAPT_Freq_Min, text_area):
    ET_Freq = int(ET_Freq_var.get())  # 1dB = 100
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_ET_S-APT_Freq_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_et_freq(line, band, ET_Freq, ETSAPT_Freq_Ave, ETSAPT_Freq_Max, ETSAPT_Freq_Min, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_ET_S-APT_Freq_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_et_freq(line, band, ET_Freq, ETSAPT_Freq_Ave, ETSAPT_Freq_Max, ETSAPT_Freq_Min, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_DC_I	="):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_et_freq(line, band, ET_Freq, ETSAPT_Freq_Ave, ETSAPT_Freq_Max, ETSAPT_Freq_Min, text_area):
    New_String = re.split("=|\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    Read_index = int(Word[6])
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"

    text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t")
    text_area.see(tk.END)

    if ETSAPT_Freq_Ave.get(band) is not None:
        if ETSAPT_Freq_Ave[band].get(Path) is not None:
            Index_count = ETSAPT_Freq_Ave.loc[(band, Path)].count()
            if Read_index < Index_count:
                New_String[1] = round(ETSAPT_Freq_Ave[band, Path][Read_index])
                New_String[2] = round(ETSAPT_Freq_Min[band, Path][Read_index]) - ET_Freq
                New_String[3] = round(ETSAPT_Freq_Max[band, Path][Read_index]) + ET_Freq
            else:
                New_String[1] = 0
                New_String[2] = New_String[1] - ET_Freq
                New_String[3] = New_String[1] + ET_Freq
        else:
            New_String[1] = 0
            New_String[2] = New_String[1] - ET_Freq
            New_String[3] = New_String[1] + ET_Freq
    else:
        New_String[1] = 0
        New_String[2] = New_String[1] - ET_Freq
        New_String[3] = New_String[1] + ET_Freq

    text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
    text_area.see(tk.END)
    Word = "_".join(Word) + "\t" + "="
    New_String[0] = Word
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_et_power(Selected_spc, rat, band, ET_Power_var, ETSAPT_Power_Ave, ETSAPT_Power_Max, ETSAPT_Power_Min, text_area):
    ET_Power = int(ET_Power_var.get())  # 1dB = 100
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_ET_S-APT_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_et_power(line, band, ET_Power, ETSAPT_Power_Ave, ETSAPT_Power_Max, ETSAPT_Power_Min, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_ET_S-APT_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_et_power(line, band, ET_Power, ETSAPT_Power_Ave, ETSAPT_Power_Max, ETSAPT_Power_Min, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_DC_I	="):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_et_power(line, band, ET_Power, ETSAPT_Power_Ave, ETSAPT_Power_Max, ETSAPT_Power_Min, text_area):
    New_String = re.split("=|\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    Read_index = int(Word[5])
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"

    text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t")
    text_area.see(tk.END)

    if ETSAPT_Power_Ave.get(band) is not None:
        if ETSAPT_Power_Ave[band].get(Path) is not None:
            Index_count = ETSAPT_Power_Ave.loc[(band, Path)].count()
            if Read_index < Index_count:
                New_String[1] = round(ETSAPT_Power_Ave[band, Path][Read_index])
                New_String[2] = round(ETSAPT_Power_Min[band, Path][Read_index]) - ET_Power
                New_String[3] = round(ETSAPT_Power_Max[band, Path][Read_index]) + ET_Power
            else:
                New_String[1] = 0
                New_String[2] = New_String[1] - ET_Power
                New_String[3] = New_String[1] + ET_Power
        else:
            New_String[1] = 0
            New_String[2] = New_String[1] - ET_Power
            New_String[3] = New_String[1] + ET_Power
    else:
        New_String[1] = 0
        New_String[2] = New_String[1] - ET_Power
        New_String[3] = New_String[1] + ET_Power

    text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
    text_area.see(tk.END)
    Word = "_".join(Word) + "\t" + "="
    New_String[0] = Word
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_3g_et_psat_pgain(
    Selected_spc,
    rat,
    band,
    ET_Psat_var,
    ETSAPT_3G_Psat_Ave,
    ETSAPT_3G_Psat_Max,
    ETSAPT_3G_Psat_Min,
    ET_Pgain_var,
    ETSAPT_3G_Power_Ave,
    ETSAPT_3G_Power_Max,
    ETSAPT_3G_Power_Min,
    text_area,
):
    ET_Psat = float(ET_Psat_var.get())  # 1dB = 100
    ET_Pgain = float(ET_Pgain_var.get())
    target_word = f"[{rat}_BAND{band}_Calibration_Spec]"
    band = f"B{band}"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_ET_S-APT_Psat"):
            New_String = Old_String = line
            New_String = et_3g(line, band, ET_Psat, ETSAPT_3G_Psat_Ave, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX_ET_S-APT_Power"):
            New_String = Old_String = line
            New_String = et_3g(line, band, ET_Psat, ETSAPT_3G_Power_Ave, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_DC_I"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def et_3g(line, band, spec, df, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
    text_area.see(tk.END)

    if df.empty:
        New_String[2] = 0
        New_String[3] = round(New_String[2] - spec)
        New_String[4] = round(New_String[2] + spec)
    else:
        a = np.array([df[band, "R99"], df[band, "HSUPA"]])
        New_String[2] = round(a.mean())
        New_String[3] = round(New_String[2] - spec)
        New_String[4] = round(New_String[2] + spec)
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String