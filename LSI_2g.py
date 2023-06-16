import re
import tkinter as tk
import numpy as np


def GSM_Params(band, data_lines):
    target_word = f"[{band}_Calibration_Parameter]"
    Param = False
    MPM = LPM = ULPM = True
    for index, line in enumerate(data_lines):
        if target_word in line:
            Param = True
        elif Param & line.startswith("Tx_PAMAPTGainMode_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            Gainmode = New_String[1:]
            if Gainmode[1] == "0":
                MPM = False
            if Gainmode[2] == "0":
                LPM = False
            if Gainmode[3] == "0":
                ULPM = False
        elif Param & line.startswith("Tx_APT_HPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            HPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_MPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            MPM_Index = New_String[1:3]
        elif Param & line.startswith("Tx_APT_LPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            LPM_Index = New_String[1:3]
        elif Param & line.startswith("Tx_APT_ULPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            ULPM_Index = New_String[1:3]
        elif Param & line.startswith("Tx_PAMAPTGainMode_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            Gainmode = New_String[1:]
            if Gainmode[1] == "0":
                EPSK_MPM = False
            if Gainmode[2] == "0":
                EPSK_LPM = False
            if Gainmode[3] == "0":
                EPSK_ULPM = False
        elif Param & line.startswith("Tx_APT_HPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_HPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_MPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_MPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_LPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_LPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_ULPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_ULPM_Index = New_String[1:5]
        elif line.startswith("EPSK_FineTxCal="):
            Param = False

    return (
        HPM_Index,
        MPM_Index,
        LPM_Index,
        ULPM_Index,
        EPSK_HPM_Index,
        EPSK_MPM_Index,
        EPSK_LPM_Index,
        EPSK_ULPM_Index,
        MPM,
        LPM,
        ULPM,
        EPSK_MPM,
        EPSK_LPM,
        EPSK_ULPM,
    )


def rx_gain(PRX_Gain_2G, RX_Gain_2G_Spec, band, spec_only, String, text_area):
    text_area.insert(tk.END, f"{String[0]:<30}| {String[3]:>5}\t{String[4]:>5}\t\t\u2192\t")
    text_area.see(tk.END)

    if spec_only == "Spec_Only":
        RX_agcoffset = [float(String[3]), float(String[4])]
        RX_agc_mean = np.mean(RX_agcoffset)
        String[2] = round(int(RX_agc_mean))
        String[3] = round(int(RX_agc_mean) - RX_Gain_2G_Spec)
        String[4] = round(int(RX_agc_mean) + RX_Gain_2G_Spec)
    else:
        String[2] = round(PRX_Gain_2G[band])
        String[3] = round(int(String[2]) - RX_Gain_2G_Spec)
        String[4] = round(int(String[2]) + RX_Gain_2G_Spec)

    text_area.insert(tk.END, f"{String[3]:>5}\t{String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = "\t".join(map(str, String)) + "\n"

    return New_String


def chng_2g_rx_gain(Selected_spc, band, RX_Gain_2G_Spec_var, PRX_Gain_2G, Ripple_2G, text_area):
    RX_Gain_2G_Spec = int(RX_Gain_2G_Spec_var.get())  # 1dB = 100
    target_word = f"[{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("Rx_AGCOffset_0"):
            String = Old_String = line
            String = re.split("\t|\n", line)
            String = [v for v in String if v]
            New_String = rx_gain(PRX_Gain_2G, RX_Gain_2G_Spec, band, "daseul", String, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("Rx_Ripple"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            New_String[3] = round(Ripple_2G[band]) + 2
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("GMSK_Ref_Power0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def Chng_2G_rx_gain_spec_only(Selected_spc, rat, band, RX_Gain_2G_Spec_var, text_area):

    RX_Gain_2G_Spec = float(RX_Gain_2G_Spec_var.get())
    target_word = f"[{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False
    PRX_Gain_2G = []  # Spec only에서는 빈 리스트만 전달에서 오류 방지
    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(target_word):
            new_text_content += line
            Check = True
            text_area.insert(tk.END, f"\n{target_word}\n")
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & line.startswith("Rx_AGCOffset_0"):
            String = Old_String = line
            String = re.split("\t|\n", line)
            String = [v for v in String if v]
            New_String = rx_gain(PRX_Gain_2G, RX_Gain_2G_Spec, band, "Spec_Only", String, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("Rx_AGCOffset_1"):
            String = Old_String = line
            String = re.split("\t|\n", line)
            String = [v for v in String if v]
            New_String = rx_gain(PRX_Gain_2G, RX_Gain_2G_Spec, band, "Spec_Only", String, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("Rx_AGCOffset_2"):
            String = Old_String = line
            String = re.split("\t|\n", line)
            String = [v for v in String if v]
            New_String = rx_gain(PRX_Gain_2G, RX_Gain_2G_Spec, band, "Spec_Only", String, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("Rx_AGCOffset_3"):
            String = Old_String = line
            String = re.split("\t|\n", line)
            String = [v for v in String if v]
            New_String = rx_gain(PRX_Gain_2G, RX_Gain_2G_Spec, band, "Spec_Only", String, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("GMSK_Ref_Power"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_2g_tx(
    Selected_spc,
    band,
    GMSK_Spec_var,
    GMSK_Mean,
    GTxL_Spec_var,
    GMSK_TXL_Mean,
    GCode_Spec_var,
    GMSK_Code_Mean,
    EPSK_Spec_var,
    EPSK_Mean,
    ETxL_Spec_var,
    EPSK_TXL_Mean,
    ECode_Spec_var,
    EPSK_Code_Mean,
    text_area,
):
    GMSK_Spec = int(GMSK_Spec_var.get())
    EPSK_Spec = int(EPSK_Spec_var.get())
    GTxL_Spec = int(GTxL_Spec_var.get())
    ETxL_Spec = int(ETxL_Spec_var.get())
    GCode_Spec = int(GCode_Spec_var.get())
    ECode_Spec = int(ECode_Spec_var.get())
    target_word = f"[{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False
    Param = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    (
        HPM_Index,
        MPM_Index,
        LPM_Index,
        ULPM_Index,
        EPSK_HPM_Index,
        EPSK_MPM_Index,
        EPSK_LPM_Index,
        EPSK_ULPM_Index,
        MPM,
        LPM,
        ULPM,
        EPSK_MPM,
        EPSK_LPM,
        EPSK_ULPM,
    ) = GSM_Params(band, data_lines)

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("GMSK_Ref_Power"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("Power", New_String[0])
            Word = [v for v in Word if v]
            Index_N = int(Word[1])
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            if Index_N in [0, 1, 2, 3]:
                gain = "HPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][HPM_Index[Index_N]])
            elif Index_N in [4]:
                gain = "HPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            elif MPM & (Index_N in [5, 6]):
                gain = "MPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][MPM_Index[Index_N - 5]])
            elif MPM & (Index_N in [7]):
                gain = "MPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            elif LPM & (Index_N in [8, 9]):
                gain = "LPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][LPM_Index[Index_N - 8]])
            elif LPM & (Index_N in [10]):
                gain = "LPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            elif ULPM & (Index_N in [11, 12]):
                gain = "ULPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][ULPM_Index[Index_N - 11]])
            elif ULPM & (Index_N in [13]):
                gain = "ULPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            else:
                New_String[2] = 0
            New_String[3] = New_String[2] - GMSK_Spec
            New_String[4] = New_String[2] + GMSK_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            Word = "Power".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("GMSK_TxL"):  # Code
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            New_String[2] = round(GMSK_Code_Mean[band, Word[1]])
            New_String[3] = New_String[2] - GCode_Spec
            New_String[4] = New_String[2] + GCode_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("GMSK_Power_TxL"):  # TX Powerl level
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            New_String[2] = str(round(GMSK_TXL_Mean[band, Word[2]]) - GTxL_Spec)
            New_String[3] = str(round(GMSK_TXL_Mean[band, Word[2]]) + GTxL_Spec)
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("EPSK_Ref_Power"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("Power", New_String[0])
            Word = [v for v in Word if v]
            Index_N = int(Word[1])
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            if Index_N in [0, 1, 2, 3]:
                gain = "HPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_HPM_Index[Index_N]])
            elif (EPSK_MPM == True or EPSK_LPM == True or EPSK_ULPM == True) & (Index_N in [4]):
                gain = "HPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            elif EPSK_MPM & (Index_N in [5, 6]):
                gain = "MPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_MPM_Index[Index_N - 5]])
            elif EPSK_MPM & (Index_N in [7]):
                gain = "MPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            elif EPSK_LPM & (Index_N in [8, 9]):
                gain = "LPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_LPM_Index[Index_N - 8]])
            elif EPSK_LPM & (Index_N in [10]):
                gain = "LPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            elif EPSK_ULPM & (Index_N in [11, 12]):
                gain = "ULPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_ULPM_Index[Index_N - 11]])
            elif EPSK_ULPM & (Index_N in [13]):
                gain = "ULPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            else:
                New_String[2] = 0
            New_String[3] = New_String[2] - EPSK_Spec
            New_String[4] = New_String[2] + EPSK_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            Word = "Power".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("EPSK_TxL"):  # Code
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            New_String[2] = round(GMSK_Code_Mean[band, Word[1]])
            New_String[3] = New_String[2] - ECode_Spec
            New_String[4] = New_String[2] + ECode_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("EPSK_Power_TxL"):  # TX Power level
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            New_String[2] = str(round(EPSK_TXL_Mean[band, Word[2]]) - ETxL_Spec)
            New_String[3] = str(round(EPSK_TXL_Mean[band, Word[2]]) + ETxL_Spec)
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            New_String = "\t".join(New_String) + "\n"
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


def tx_power(Spec_var, band, option, line, text_area):
    String = line.strip().split("\t")
    if option == "Power_TxL":
        text_area.insert(tk.END, f"{String[0]:<30}| {String[2]:>5}\t{String[3]:>5}\t\t\u2192\t")
        TxLevel = int(re.split("TxL|=|\t|\n", line)[1])
        if band == "G085" or band == "G09":
            TxP = (19 - TxLevel) * 2 + 5
        else:
            TxP = (15 - TxLevel) * 2
        String[2] = round(int(TxP) - Spec_var)
        String[3] = round(int(TxP) + Spec_var)
        text_area.insert(tk.END, f"{String[2]:>5}\t{String[3]:>5}\n")
    else:
        text_area.insert(tk.END, f"{String[0]:<30}| {String[3]:>5}\t{String[4]:>5}\t\t\u2192\t")
        text_area.see(tk.END)
        Tx_value = [float(String[3]), float(String[4])]
        Tx_mean = np.mean(Tx_value)
        String[2] = round(int(Tx_mean))
        String[3] = round(int(Tx_mean) - Spec_var)
        String[4] = round(int(Tx_mean) + Spec_var)
        text_area.insert(tk.END, f"{String[3]:>5}\t{String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = "\t".join(map(str, String)) + "\n"

    return New_String


def Chng_2g_tx_spec_only(
    Selected_spc, band, GMSK_Spec_var, GTxL_Spec_var, GCode_Spec_var, EPSK_Spec_var, ETxL_Spec_var, ECode_Spec_var, text_area
):
    # 2G TX FBRX Spec
    GMSK_2G_Spec = float(GMSK_Spec_var.get())
    GTxL_2G_Spec = float(GTxL_Spec_var.get())
    GCode_2G_Spec = float(GCode_Spec_var.get())
    EPSK_2G_Spec = float(EPSK_Spec_var.get())
    ETxL_2G_Spec = float(ETxL_Spec_var.get())
    ECode_2G_Spec = float(ECode_Spec_var.get())
    target_word = f"[{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()

    for index, line in enumerate(data_lines):
        if line.startswith(target_word):
            new_text_content += line
            Check = True
            text_area.insert(tk.END, f"\n{target_word}\n")
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & line.startswith("GMSK_Ref_Power"):
            New_String = tx_power(GMSK_2G_Spec, band, "Ref", line, text_area)
            Change_Str = line.replace(line, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("GMSK_TxL"):
            New_String = tx_power(GCode_2G_Spec, band, "TxL", line, text_area)
            Change_Str = line.replace(line, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("GMSK_Power_TxL"):
            New_String = tx_power(GTxL_2G_Spec, band, "Power_TxL", line, text_area)
            Change_Str = line.replace(line, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("EPSK_Ref_Power"):
            New_String = tx_power(EPSK_2G_Spec, band, "Ref", line, text_area)
            Change_Str = line.replace(line, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("EPSK_TxL"):
            New_String = tx_power(ECode_2G_Spec, band, "TxL", line, text_area)
            Change_Str = line.replace(line, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("EPSK_Power_TxL"):
            New_String = tx_power(ETxL_2G_Spec, band, "Power_TxL", line, text_area)
            Change_Str = line.replace(line, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith("Channel_Comp_GMSK"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()