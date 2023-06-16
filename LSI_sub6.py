import re
import tkinter as tk
import numpy as np


def chng_sub6_rfic_gain(Selected_spc, rat, band, RFIC_Spec_var, RFIC_gain, text_area):
    RFIC_gain_Spec = int(RFIC_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("TX_RFIC_Index_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Extract_String = [v for v in New_String[0].split("TX_") if v]
            gainindex = int(re.sub(r"[^0-9]", "", Extract_String[0]))
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            if Word[0] == "TX":
                Path = "Tx"
            elif Word[0] == "TX2":
                Path = "Tx2"
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            text_area.see(tk.END)

            if gainindex == 0:
                New_String[2] = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                New_String[3] = int(New_String[2]) - 0.1
                New_String[4] = int(New_String[2]) + 0.1
            elif gainindex <= 8:
                New_String[2] = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                New_String[3] = New_String[2] - RFIC_gain_Spec
                New_String[4] = New_String[2] + RFIC_gain_Spec
            elif gainindex <= 12:
                value = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                New_String[2] = value
                New_String[3] = New_String[2] - RFIC_gain_Spec - 5
                New_String[4] = New_String[2] + RFIC_gain_Spec + 5
            elif gainindex >= 13:
                if RFIC_gain["NR"][band][Path].get(f"Index{gainindex} ") is not None:
                    value = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                    New_String[2] = value
                    New_String[3] = New_String[2] - RFIC_gain_Spec - 5
                    New_String[4] = New_String[2] + RFIC_gain_Spec + 5
                else:
                    New_String[2] = value - 5
                    New_String[3] = New_String[2] - RFIC_gain_Spec - 5
                    New_String[4] = New_String[2] + RFIC_gain_Spec + 5

            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string

        elif Check & line.startswith("TX2_RFIC_Index_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Extract_String = [v for v in New_String[0].split("TX2_") if v]
            gainindex = int(re.sub(r"[^0-9]", "", Extract_String[0]))
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            if Word[0] == "TX":
                Path = "Tx"
            elif Word[0] == "TX2":
                Path = "Tx2"
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            text_area.see(tk.END)

            if gainindex == 0:
                New_String[2] = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                New_String[3] = int(New_String[2]) - 0.1
                New_String[4] = int(New_String[2]) + 0.1
            elif gainindex <= 8:
                New_String[2] = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                New_String[3] = New_String[2] - RFIC_gain_Spec
                New_String[4] = New_String[2] + RFIC_gain_Spec
            elif gainindex <= 12:
                value = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                New_String[2] = value
                New_String[3] = New_String[2] - RFIC_gain_Spec - 5
                New_String[4] = New_String[2] + RFIC_gain_Spec + 5
            elif gainindex >= 13:
                if RFIC_gain["NR"][band][Path].get(f"Index{gainindex} ") is not None:
                    value = round(RFIC_gain["NR"][band][Path][f"Index{gainindex} "])
                    New_String[2] = value
                    New_String[3] = New_String[2] - RFIC_gain_Spec - 5
                    New_String[4] = New_String[2] + RFIC_gain_Spec + 5
                else:
                    New_String[2] = value - 5
                    New_String[3] = New_String[2] - RFIC_gain_Spec - 5
                    New_String[4] = New_String[2] + RFIC_gain_Spec + 5

            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string

        elif line.startswith("RX_Gain_main"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_sub6_rx_gain(Selected_spc, rat, band, read_stage, RX_Gain_Spec_var, RXGain_sub6, RXRSRP_sub6, RXComp_sub6, text_area):
    RX_Gain_Spec = int(RX_Gain_Spec_var.get())
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
        elif Check & line.startswith("RX_Gain_main_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            gainstage = int(re.sub(r"[^0-9]", "", New_String[0]))
            if gainstage > read_stage:
                new_text_content += line
            else:
                text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
                New_String[2] = round(RXGain_sub6[band, f"STAGE{gainstage}(-50.00dBm) "])
                New_String[3] = New_String[2] - RX_Gain_Spec
                New_String[4] = New_String[2] + RX_Gain_Spec
                text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
                text_area.see(tk.END)
                New_String = [str(v) for v in New_String]
                New_String = "\t".join(New_String) + "\n"
                new_string = line.replace(Old_String, New_String)
                new_text_content += new_string
        elif Check & line.startswith("RX_RsrpOffset_main_0"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            gainstage = int(re.sub(r"[^0-9]", "", New_String[0]))
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            New_String[2] = round(RXRSRP_sub6[band])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("RX_FreqOffset_prx_0"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            gainstage = int(re.sub(r"[^0-9]", "", New_String[0]))
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            New_String[2] = round(RXComp_sub6[band])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.insert(tk.END, f"\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line == "// TX FBRX\n":
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_sub6_fbrx_gain_meas(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Meas_sub6, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get())
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
        elif Check & line.startswith("TX_FBRX_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_meas(line, band, FBRX_Spec, FBRX_Gain_Meas_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_FBRX_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_meas(line, band, FBRX_Spec, FBRX_Gain_Meas_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_gain_meas(line, band, FBRX_Spec, FBRX_Gain_Meas_sub6, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    gainstage = int(Word[4])
    text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
    New_String[2] = round(FBRX_Gain_Meas_sub6["NR", band, Path, f"Index{gainstage} "])
    New_String[3] = New_String[2] - FBRX_Spec
    New_String[4] = New_String[2] + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_fbrx_gain_code(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Code_sub6, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get()) * 100  # 1dB = 100
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
        elif Check & line.startswith("TX_FBRX_Code_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_code(line, band, FBRX_Spec, FBRX_Gain_Code_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_FBRX_Code_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_code(line, band, FBRX_Spec, FBRX_Gain_Code_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_gain_code(line, band, FBRX_Spec, FBRX_Gain_Code_sub6, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    gainstage = int(Word[4])
    text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
    New_String[2] = round(FBRX_Gain_Code_sub6["NR", band, Path, f"Index{gainstage} "])
    New_String[3] = New_String[2] - FBRX_Spec
    New_String[4] = New_String[2] + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_fbrx_freq_meas(
    Selected_spc,
    rat,
    band,
    FBRX_Spec_var,
    FBRX_Freq_Meas_sub6,
    FBRX_Freq_Meas_sub6_Max,
    FBRX_Freq_Meas_sub6_Min,
    text_area,
):
    FBRX_Spec = int(FBRX_Spec_var.get())
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Cable = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Cable = True
            new_text_content += line
        elif Cable & line.startswith("TX_FBRX_Channel_Pow"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_meas(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Meas_sub6,
                FBRX_Freq_Meas_sub6_Max,
                FBRX_Freq_Meas_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Cable & line.startswith("TX2_FBRX_Channel_Pow"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_meas(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Meas_sub6,
                FBRX_Freq_Meas_sub6_Max,
                FBRX_Freq_Meas_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Cable = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_freq_meas(line, band, FBRX_Spec, FBRX_Freq_Meas_sub6, FBRX_Freq_Meas_sub6_Max, FBRX_Freq_Meas_sub6_Min, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
    New_String[2] = round(FBRX_Freq_Meas_sub6["NR", band, Path])
    New_String[3] = round(FBRX_Freq_Meas_sub6_Min["NR", band, Path]) - FBRX_Spec
    New_String[4] = round(FBRX_Freq_Meas_sub6_Max["NR", band, Path]) + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_fbrx_freq_code(
    Selected_spc,
    rat,
    band,
    FBRX_Spec_var,
    FBRX_Freq_Code_sub6,
    FBRX_Freq_Code_sub6_Max,
    FBRX_Freq_Code_sub6_Min,
    text_area,
):
    FBRX_Spec = int(FBRX_Spec_var.get()) * 100  # 1dB = 100
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
        elif Check & line.startswith("TX_FBRX_Channel_Code"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_code(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Code_sub6,
                FBRX_Freq_Code_sub6_Max,
                FBRX_Freq_Code_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_FBRX_Channel_Code"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_code(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Code_sub6,
                FBRX_Freq_Code_sub6_Max,
                FBRX_Freq_Code_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_freq_code(line, band, FBRX_Spec, FBRX_Freq_Code_sub6, FBRX_Freq_Code_sub6_Max, FBRX_Freq_Code_sub6_Min, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
    New_String[2] = round(FBRX_Freq_Code_sub6["NR", band, Path])
    New_String[3] = round(FBRX_Freq_Code_sub6_Min["NR", band, Path]) - FBRX_Spec
    New_String[4] = round(FBRX_Freq_Code_sub6_Max["NR", band, Path]) + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_apt(Selected_spc, rat, band, APT_Spec_var, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min):
    APT_Spec = float(APT_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("TX_APT_"):
            New_String = Old_String = line
            New_String = sub6_apt(line, band, APT_Spec, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_APT_"):
            New_String = Old_String = line
            New_String = sub6_apt(line, band, APT_Spec, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_DC_I"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_apt(line, band, APT_Spec, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min):
    New_String = re.split("=|\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    Pa_stage = Word[2]
    values = [
        APT_Meas_sub6_Ave[band, Path, Pa_stage, f"Index{Word[5]} "],
        APT_Meas_sub6_Max[band, Path, Pa_stage, f"Index{Word[5]} "],
        APT_Meas_sub6_Min[band, Path, Pa_stage, f"Index{Word[5]} "],
    ]
    if all(v == -10.0 for v in values):
        New_String[1] = -10
        New_String[2] = -10.1
        New_String[3] = -9.9
    else:
        New_String[1] = round(APT_Meas_sub6_Ave[band, Path, Pa_stage, f"Index{Word[5]} "])
        New_String[2] = New_String[1] - APT_Spec
        New_String[3] = New_String[1] + APT_Spec
    Word = "_".join(Word) + "\t" + "="
    New_String[0] = Word
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_bwcal(Selected_spc, rat, band, BW_Cal_Spec_var, BW_Cal, text_area):
    BWCal_Spec = float(BW_Cal_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("TX_BW_Cal_Diff"):
            text_area.insert(tk.END, f"BW Power Calibration\n")
            text_area.see(tk.END)
            New_String = Old_String = line
            New_String = sub6_bwcal(line, band, BWCal_Spec, BW_Cal)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_BW_Cal_Diff"):
            New_String = Old_String = line
            New_String = sub6_bwcal(line, band, BWCal_Spec, BW_Cal)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("RX_Gain_main_"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_bwcal(line, band, BWCal_Spec, BW_Cal):
    New_String = re.split("=|\t|\n", line)
    New_String = [v for v in New_String if v]

    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]

    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"

    New_String[1] = round(BW_Cal[band, Path])
    New_String[2] = round(0 - BWCal_Spec)
    New_String[3] = round(0 + BWCal_Spec)

    Word = "_".join(Word) + "\t" + "="
    New_String[0] = Word
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def Read_sub6_default_cal_option(flag, Selected_spc, rat, band, dict_option, text_area):
    if flag == "daseul":
        target_word = f"[{rat}_n{band}_CAL_PARAM]"
        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()
    else:
        target_word = f"[{rat}_CAL_PARAM_BAND{band}]"
        with open(Selected_spc, "r", encoding="latin_1") as file:
            data_lines = file.readlines()
        file.close()
    Check = Check_4rx = Check_6rx = Check_8rx = Check_10rx = Check_12rx = Check_14rx = False
    Check_16rx = Check_Freq = Check_Freq_ca1 = Check_Freq_ca2 = Check_Freq_ca3 = Check_mixer = False

    Rxpath_bit = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()

    for index, line in enumerate(data_lines):
        if line.startswith(target_word):
            Check = True
            if flag == "daseul":
                Band_number = line.split("_")[1]
            else:
                Band_number = "n" + re.sub(r"[^0-9]", "", line.split("_")[3])

            dict_option = {
                Band_number: {
                    # CA3, CA2, CA1, 16RX_EN, 14RX_EN, 12RX_EN, 10RX_EN, 8RX_EN, 6RX_EN, 4RX_EN, Main
                    "GDeP": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "GDeD": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "FreP": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "FreD": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "MixP": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "MixD": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "Freq": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                }
            }
        # ? RX Gain cal default option
        elif Check & line.startswith("Rx_4RX_CAL_EN=1"):
            Check_4rx = True
        elif Check & line.startswith("Rx_6RX_CAL_EN=1"):
            Check_6rx = True
        elif Check & line.startswith("Rx_8RX_CAL_EN=1"):
            Check_8rx = True
        elif Check & line.startswith("Rx_10RX_CAL_EN=1"):
            Check_10rx = True
        elif Check & line.startswith("Rx_12RX_CAL_EN=1"):
            Check_12rx = True
        elif Check & line.startswith("Rx_14RX_CAL_EN=1"):
            Check_14rx = True
        elif Check & line.startswith("Rx_16RX_CAL_EN=1"):
            Check_16rx = True
        elif Check & line.startswith("Use_DRX_MAIN_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][10] = 1
        elif (Check & Check_4rx) & line.startswith("Use_PRX_4RX_DEFAULT=1"):
            dict_option[Band_number]["GDeP"][9] = 1
        elif (Check & Check_4rx) & line.startswith("Use_DRX_4RX_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][9] = 1
        elif (Check & Check_6rx) & line.startswith("Use_PRX_6RX_DEFAULT=1"):
            dict_option[Band_number]["GDeP"][8] = 1
        elif (Check & Check_6rx) & line.startswith("Use_DRX_6RX_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][8] = 1
        elif (Check & Check_8rx) & line.startswith("Use_PRX_8RX_DEFAULT=1"):
            dict_option[Band_number]["GDeP"][7] = 1
        elif (Check & Check_8rx) & line.startswith("Use_DRX_8RX_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][7] = 1
        elif (Check & Check_10rx) & line.startswith("Use_PRX_10RX_DEFAULT=1"):
            dict_option[Band_number]["GDeP"][6] = 1
        elif (Check & Check_10rx) & line.startswith("Use_DRX_10RX_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][6] = 1
        elif (Check & Check_12rx) & line.startswith("Use_PRX_12RX_DEFAULT=1"):
            dict_option[Band_number]["GDeP"][5] = 1
        elif (Check & Check_12rx) & line.startswith("Use_DRX_12RX_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][5] = 1
        elif (Check & Check_14rx) & line.startswith("Use_PRX_14RX_DEFAULT=1"):
            dict_option[Band_number]["GDeP"][4] = 1
        elif (Check & Check_14rx) & line.startswith("Use_DRX_14RX_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][4] = 1
        elif (Check & Check_16rx) & line.startswith("Use_PRX_16RX_DEFAULT=1"):
            dict_option[Band_number]["GDeP"][3] = 1
        elif (Check & Check_16rx) & line.startswith("Use_DRX_16RX_DEFAULT=1"):
            dict_option[Band_number]["GDeD"][3] = 1

        elif Check & line.startswith("RX_CAL_FREQ"):
            result = re.split("[\t|//]", line)  # Tab, // 분리
            Freq_List = re.split("[=,\n]", result[0])[1:]
            Freq_List = [v for v in Freq_List if v]
            dict_option[Band_number]["Freq"] = [v for v in Freq_List if v]

        # ? Freq. cal default option
        elif Check & line.startswith("RX_FREQ_CAL_EN=1"):
            Check_Freq = True
        elif (Check & Check_Freq) & line.startswith("RX_FREQv2_MAIN_EN"):
            bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            Rxpath_bit = [*f"{bit:0>8}"]
        elif (Check & Check_Freq) & ((Rxpath_bit[7] == "1") & line.startswith("RX_FREQv2_MAIN_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][10] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][10] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & ((Rxpath_bit[6] == "1") & line.startswith("RX_FREQv2_4RX_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][9] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][9] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & ((Rxpath_bit[5] == "1") & line.startswith("RX_FREQv2_6RX_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][8] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][8] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & ((Rxpath_bit[4] == "1") & line.startswith("RX_FREQv2_8RX_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][7] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][7] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & ((Rxpath_bit[3] == "1") & line.startswith("RX_FREQv2_10RX_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][6] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][6] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & ((Rxpath_bit[2] == "1") & line.startswith("RX_FREQv2_12RX_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][5] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][5] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & ((Rxpath_bit[1] == "1") & line.startswith("RX_FREQv2_14RX_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][4] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][4] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & ((Rxpath_bit[0] == "1") & line.startswith("RX_FREQv2_16RX_USE_DEFAULT")):
            f_bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][3] = int(freqbit[1])  # PRX
            dict_option[Band_number]["FreD"][3] = int(freqbit[0])  # DRX
        elif (Check & Check_Freq) & line.startswith("RX_FREQv2_CA1_EN=1"):
            Check_Freq_ca1 = True
        elif (Check & Check_Freq) & line.startswith("RX_FREQv2_CA2_EN=1"):
            Check_Freq_ca2 = True
        elif (Check & Check_Freq) & line.startswith("RX_FREQv2_CA3_EN=1"):
            Check_Freq_ca3 = True
        elif (Check & Check_Freq) & Check_Freq_ca1 & line.startswith("RX_FREQv2_CA1_USE_DEFAULT"):
            freqca = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][2] = int(freqca[1])  # PRX
            dict_option[Band_number]["FreD"][2] = int(freqca[0])  # DRX
        elif (Check & Check_Freq) & Check_Freq_ca2 & line.startswith("RX_FREQv2_CA2_USE_DEFAULT"):
            freqca = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][1] = int(freqca[1])  # PRX
            dict_option[Band_number]["FreD"][1] = int(freqca[0])  # DRX
        elif (Check & Check_Freq) & Check_Freq_ca3 & line.startswith("RX_FREQv2_CA3_USE_DEFAULT"):
            freqca = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            freqbit = [*f"{f_bit:0>2}"]
            dict_option[Band_number]["FreP"][0] = int(freqca[1])  # PRX
            dict_option[Band_number]["FreD"][0] = int(freqca[0])  # DRX

        # ? Mixer Cal default option
        elif Check & line.startswith("RX_Mixer_Cal_mode"):
            bit = bin(int(re.split("[=,//,\n]", line)[1]))[2:]
            Mixer_bit = [*f"{bit:0>8}"]
            Check_mixer = True
        elif (Check & Check_mixer) & line.startswith("Use_PRX_MAIN_Offset_DEFAULT=1"):
            if Mixer_bit[7] == "1":
                dict_option[Band_number]["MixP"][10] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_MAIN_Offset_DEFAULT=1"):
            if Mixer_bit[7] == "1":
                dict_option[Band_number]["MixD"][10] = 1
        elif (Check & Check_mixer) & line.startswith("Use_PRX_4RX_Offset_DEFAULT=1"):
            if Mixer_bit[6] == "1":
                dict_option[Band_number]["MixP"][9] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_4RX_Offset_DEFAULT=1"):
            if Mixer_bit[6] == "1":
                dict_option[Band_number]["MixD"][9] = 1
        elif (Check & Check_mixer) & line.startswith("Use_PRX_6RX_Offset_DEFAULT=1"):
            if Mixer_bit[5] == "1":
                dict_option[Band_number]["MixP"][8] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_6RX_Offset_DEFAULT=1"):
            if Mixer_bit[5] == "1":
                dict_option[Band_number]["MixD"][8] = 1
        elif (Check & Check_mixer) & line.startswith("Use_PRX_8RX_Offset_DEFAULT=1"):
            if Mixer_bit[4] == "1":
                dict_option[Band_number]["MixP"][7] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_8RX_Offset_DEFAULT=1"):
            if Mixer_bit[4] == "1":
                dict_option[Band_number]["MixD"][7] = 1
        elif (Check & Check_mixer) & line.startswith("Use_PRX_10RX_Offset_DEFAULT=1"):
            if Mixer_bit[3] == "1":
                dict_option[Band_number]["MixP"][6] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_10RX_Offset_DEFAULT=1"):
            if Mixer_bit[3] == "1":
                dict_option[Band_number]["MixD"][6] = 1
        elif (Check & Check_mixer) & line.startswith("Use_PRX_12RX_Offset_DEFAULT=1"):
            if Mixer_bit[2] == "1":
                dict_option[Band_number]["MixP"][5] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_12RX_Offset_DEFAULT=1"):
            if Mixer_bit[2] == "1":
                dict_option[Band_number]["MixD"][5] = 1
        elif (Check & Check_mixer) & line.startswith("Use_PRX_14RX_Offset_DEFAULT=1"):
            if Mixer_bit[1] == "1":
                dict_option[Band_number]["MixP"][4] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_14RX_Offset_DEFAULT=1"):
            if Mixer_bit[1] == "1":
                dict_option[Band_number]["MixD"][4] = 1
        elif (Check & Check_mixer) & line.startswith("Use_PRX_16RX_Offset_DEFAULT=1"):
            if Mixer_bit[0] == "1":
                dict_option[Band_number]["MixP"][3] = 1
        elif (Check & Check_mixer) & line.startswith("Use_DRX_16RX_Offset_DEFAULT=1"):
            if Mixer_bit[0] == "1":
                dict_option[Band_number]["MixD"][3] = 1
        elif Check & line.startswith("// TX Cal Parameters"):
            return dict_option


def chng_sub6_rx_gain_default(flag, Selected_spc, rat, band, dict_option, Sub6_RX_Gain_default, text_area):
    if flag == "daseul":
        target_word = f"[{rat}_n{band}_CAL_PARAM]"
        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()
    else:
        target_word = f"[{rat}_CAL_PARAM_BAND{band}]"
        with open(Selected_spc, "r", encoding="latin_1") as file:
            data_lines = file.readlines()
        file.close()

    band = f"n{band}"
    text_area.insert(tk.END, "\n")
    text_area.insert(tk.END, f"{target_word}\n")
    text_area.insert(tk.END, "-" * 100)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)

    new_text_content = ""
    Check = False

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(target_word):
            new_text_content += line
            Check = True
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & line.startswith(f"PRX_RxGAIN_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rxgain_cal(
                line, band, path[2], path[0], dict_option[band]["GDeP"], Sub6_RX_Gain_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_RxGAIN_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rxgain_cal(
                line, band, path[2], path[0], dict_option[band]["GDeD"], Sub6_RX_Gain_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & (line.startswith("// TX Cal Parameters")):
            new_text_content += line
            Check = False
        else:
            new_text_content += line
    text_area.see(tk.END)
    # text_area.insert(tk.END, f"Tech= {rat}  \t| Band= {band:<7}\t| Ant= {Antenna}\t| Path= {Path}\n")
    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rxgain_cal(line, band, ant, path, dict_option, Sub6_RX_Gain_default, text_area):
    check = False
    if (ant == "MAIN") & (path == "PRX" or path == "DRX"):
        check = dict_option[10]
    elif (ant == "4RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[9]
    elif (ant == "6RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[8]
    elif (ant == "8RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[7]
    elif (ant == "10RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[6]
    elif (ant == "12RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[5]
    elif (ant == "14RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[4]
    elif (ant == "16RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[3]
    elif (ant == "CA1") & (path == "PRX" or path == "DRX"):
        check = dict_option[2]
    elif (ant == "CA2") & (path == "PRX" or path == "DRX"):
        check = dict_option[1]
    elif (ant == "CA3") & (path == "PRX" or path == "DRX"):
        check = dict_option[0]

    if check:
        New_String = re.split("[_=,\n]", line)
        New_String = [v for v in New_String if v]
        if ant == "CA1" or ant == "CA2" or ant == "CA3":
            ca = ant
            ant = "MAIN"
            text_area.insert(tk.END, f"{ca:<4} {path} GAIN  |   ")
        else:
            ca = "NonCA"
            text_area.insert(tk.END, f"{ant:<4} {path} GAIN  |   ")

        for i in range(6):
            if i == 5:
                text_area.insert(tk.END, f"{New_String[5+i]:>5}\n")
            else:
                text_area.insert(tk.END, f"{New_String[5+i]:>5}, ")
        for i in range(6):
            New_String[5 + i] = round(Sub6_RX_Gain_default[band][ant][path][f"Stage{i}"] * 100)

        text_area.insert(tk.END, f"               | \u2192 ")
        for i in range(6):
            if i == 5:
                text_area.insert(tk.END, f"{New_String[5+i]:>5}\n\n")
            else:
                text_area.insert(tk.END, f"{New_String[5+i]:>5}, ")

        text_area.see(tk.END)
    else:
        New_String = re.split("[_=,\n]", line)
        New_String = [v for v in New_String if v]
        for i in range(6):
            New_String[5 + i] = 0

    New_String1 = "_".join(map(str, New_String[:5]))
    New_String2 = ",".join(map(str, New_String[5:]))
    New_String = New_String1 + "=" + New_String2 + "\n"
    return New_String

def chng_sub6_rsrp_offset_default(flag, Selected_spc, rat, band, dict_option, Sub6_RSRP_Offset_default, text_area):
    if flag == "daseul":
        target_word = f"[{rat}_n{band}_CAL_PARAM]"
        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()
    else:
        target_word = f"[{rat}_CAL_PARAM_BAND{band}]"
        with open(Selected_spc, "r", encoding="latin_1") as file:
            data_lines = file.readlines()
        file.close()
    band = f"n{band}"
    new_text_content = ""
    Check = False

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(target_word):
            new_text_content += line
            Check = True
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & line.startswith(f"PRX_RSRP_Offset_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rsrp_offset(
                index, line, rat, band, path[3], path[0], dict_option[band]["GDeP"], Sub6_RSRP_Offset_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_RSRP_Offset_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rsrp_offset(
                index, line, rat, band, path[3], path[0], dict_option[band]["GDeD"], Sub6_RSRP_Offset_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & (line.startswith("// TX Cal Parameters")):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rsrp_offset(index, line, rat, band, ant, path, dict_option, Sub6_RSRP_Offset_default, text_area):
    check = False
    if (ant == "MAIN") & (path == "PRX" or path == "DRX"):
        check = dict_option[10]
    elif (ant == "4RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[9]
    elif (ant == "6RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[8]
    elif (ant == "8RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[7]
    elif (ant == "10RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[6]
    elif (ant == "12RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[5]
    elif (ant == "14RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[4]
    elif (ant == "16RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[3]
    elif (ant == "CA1") & (path == "PRX" or path == "DRX"):
        check = dict_option[2]
    elif (ant == "CA2") & (path == "PRX" or path == "DRX"):
        check = dict_option[1]
    elif (ant == "CA3") & (path == "PRX" or path == "DRX"):
        check = dict_option[0]

    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    if check:
        if ant == "CA1" or ant == "CA2" or ant == "CA3":
            ca = ant
            ant = "MAIN"
            text_area.insert(tk.END, f"{ca:<4} {path} RSRP  |   ")
        else:
            ca = "NonCA"
            text_area.insert(tk.END, f"{ant:<4} {path} RSRP  |   ")

        text_area.insert(tk.END, f"{New_String[6]:>5}\n")
        New_String[6] = round(Sub6_RSRP_Offset_default[band][ant][path] * 100)
        text_area.insert(tk.END, f"               | \u2192 {New_String[6]:>5}\n\n")
        text_area.see(tk.END)
    else:
        New_String[6] = 0

    New_String1 = "_".join(map(str, New_String[:6]))
    New_String2 = ",".join(map(str, New_String[6:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def chng_sub6_rx_freq_default(
    flag,
    Selected_spc,
    rat,
    band,
    dict_option,
    Sub6_RX_Freq_default,
    Bluetick,
    blue_nrrx_freq,
    blue_nrdrx_offset,
    text_area,
):
    if flag == "daseul":
        target_word = f"[{rat}_n{band}_CAL_PARAM]"
        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()
    else:
        target_word = f"[{rat}_CAL_PARAM_BAND{band}]"
        with open(Selected_spc, "r", encoding="latin_1") as file:
            data_lines = file.readlines()
        file.close()

    band = f"n{band}"
    new_text_content = ""
    Check = False

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(target_word):
            new_text_content += line
            Check = True
        elif Check & line.startswith(f"PRX_RXFREQ_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rxfreq_cal(
                dict_option[band]["Freq"],
                index,
                line,
                rat,
                band,
                path[2],
                path[0],
                dict_option[band]["FreP"],
                Sub6_RX_Freq_default,
                Bluetick,
                blue_nrrx_freq,
                blue_nrdrx_offset,
                text_area,
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_RXFREQ_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rxfreq_cal(
                dict_option[band]["Freq"],
                index,
                line,
                rat,
                band,
                path[2],
                path[0],
                dict_option[band]["FreD"],
                Sub6_RX_Freq_default,
                Bluetick,
                blue_nrrx_freq,
                blue_nrdrx_offset,
                text_area,
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"// TX Cal Parameters"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rxfreq_cal(
    Freq_List,
    index,
    line,
    rat,
    band,
    ant,
    path,
    dict_option,
    Sub6_RX_Freq_default,
    Bluetick,
    blue_nrrx_freq,
    blue_nrdrx_offset,
    text_area,
):
    check = False
    if (ant == "MAIN") & (path == "PRX" or path == "DRX"):
        check = dict_option[10]
    elif (ant == "4RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[9]
    elif (ant == "6RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[8]
    elif (ant == "8RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[7]
    elif (ant == "10RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[6]
    elif (ant == "12RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[5]
    elif (ant == "14RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[4]
    elif (ant == "16RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[3]
    elif (ant == "CA1") & (path == "PRX" or path == "DRX"):
        check = dict_option[2]
    elif (ant == "CA2") & (path == "PRX" or path == "DRX"):
        check = dict_option[1]
    elif (ant == "CA3") & (path == "PRX" or path == "DRX"):
        check = dict_option[0]

    if check:
        New_String = re.split("[_=,\n]", line)
        New_String = [v for v in New_String if v]
        if ant == "CA1" or ant == "CA2" or ant == "CA3":
            ca = ant
            ant = "MAIN"
            text_area.insert(tk.END, f"{ca:<4} {path} FREQ  |   ")
        else:
            ca = "NonCA"
            text_area.insert(tk.END, f"{ant:<4} {path} FREQ  |   ")

        for i in range(len(New_String[4:])):
            if i == range(len(New_String[4:]))[-1]:
                text_area.insert(tk.END, f"{New_String[4+i]:>5}\n")
            else:
                text_area.insert(tk.END, f"{New_String[4+i]:>5}, ")
        text_area.insert(tk.END, f"               | \u2192 ")
        # New_String의 Freq list를 모두 지우고, Freq_List 길이만큼 0 으로 채워넣기 후 값을 변경
        del New_String[4:]

        for i in range(len(Freq_List)):
            New_String.append(0)
            try:
                value = Sub6_RX_Freq_default[band][ca][ant][path][Freq_List[i]]
                if Bluetick & (band == "n28") & (path == "DRX"):
                    if int(Freq_List[i]) == blue_nrrx_freq:
                        New_String[4 + i] = round(value * 100) + (blue_nrdrx_offset * 100)
                    elif int(Freq_List[i]) in [blue_nrrx_freq - 1000, blue_nrrx_freq + 1000]:
                        New_String[4 + i] = round(value * 100) + 100
                    else:
                        New_String[4 + i] = round(value * 100)
                else:
                    New_String[4 + i] = round(value * 100)
            except:
                pass

        for i in range(len(Freq_List)):
            if i == range(len(Freq_List))[-1]:
                text_area.insert(tk.END, f"{New_String[4+i]:>5}\n\n")
            else:
                text_area.insert(tk.END, f"{New_String[4+i]:>5}, ")
        text_area.see(tk.END)

    else:
        New_String = re.split("[_=,\n]", line)
        New_String = [v for v in New_String if v]
        del New_String[4:]

        for i in range(len(Freq_List)):
            New_String.append(0)

    New_String1 = "_".join(map(str, New_String[:4]))
    New_String2 = ",".join(map(str, New_String[4:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def chng_sub6_rx_mixer_default(flag, Selected_spc, rat, band, dict_option, Sub6_RX_Mixer_default, text_area):
    if flag == "daseul":
        target_word = f"[{rat}_n{band}_CAL_PARAM]"
        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()
    else:
        target_word = f"[{rat}_CAL_PARAM_BAND{band}]"
        with open(Selected_spc, "r", encoding="latin_1") as file:
            data_lines = file.readlines()
        file.close()
    band = f"n{band}"
    new_text_content = ""
    Check = False

    # band별 Mixer 갯수 구하기
    # Mixer = Sub6_RX_Mixer_default.reset_index().groupby("Band")['Mixer'].nunique().loc[band]
    Mixer_list = Sub6_RX_Mixer_default[band].index.get_level_values("Mixer").tolist()
    Mixer = list(dict.fromkeys(Mixer_list))  # list 중복 제거

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(target_word):
            new_text_content += line
            Check = True
        elif Check & line.startswith(f"PRX_MIXER_RSRP_Offset_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rx_mixer_cal(
                index, line, rat, band, Mixer, path[4], path[0], dict_option[band]["MixP"], Sub6_RX_Mixer_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_MIXER_RSRP_Offset_"):
            path = re.split("_|=|,|\n", line)
            New_String = sub6_rx_mixer_cal(
                index, line, rat, band, Mixer, path[4], path[0], dict_option[band]["MixD"], Sub6_RX_Mixer_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif line.startswith(f"// TX Cal Parameters"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rx_mixer_cal(index, line, rat, band, Mixer, ant, path, dict_option, Sub6_RX_Mixer_default, text_area):
    check = False
    if (ant == "MAIN") & (path == "PRX" or path == "DRX"):
        check = dict_option[10]
    elif (ant == "4RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[9]
    elif (ant == "6RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[8]
    elif (ant == "8RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[7]
    elif (ant == "10RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[6]
    elif (ant == "12RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[5]
    elif (ant == "14RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[4]
    elif (ant == "16RX") & (path == "PRX" or path == "DRX"):
        check = dict_option[3]
    elif (ant == "CA1") & (path == "PRX" or path == "DRX"):
        check = dict_option[2]
    elif (ant == "CA2") & (path == "PRX" or path == "DRX"):
        check = dict_option[1]
    elif (ant == "CA3") & (path == "PRX" or path == "DRX"):
        check = dict_option[0]

    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    if check:
        Mixer_no = []
        Old_Mixer_no = New_String[7::2]
        Old_Value = New_String[8::2]

        if ant == "CA1" or ant == "CA2" or ant == "CA3":
            ca = ant
            ant = "MAIN"
            text_area.insert(tk.END, f"{ca:<4} {path} MIXER |   ")
            if ant == "MAIN":
                for i in Mixer:
                    if len(i) == 2:
                        Mixer_no.append(i)
            elif ant == "4RX":
                for i in Mixer:
                    if len(i) == 3:
                        Mixer_no.append(i)
        else:
            ca = "NonCA"
            text_area.insert(tk.END, f"{ant:<4} {path} MIXER |   ")
            if ant == "MAIN":
                for i in Mixer:
                    if len(i) == 2:
                        Mixer_no.append(i)
            elif ant == "4RX":
                for i in Mixer:
                    if len(i) == 3:
                        Mixer_no.append(i)
        count = 0
        # spc 파일의 default cal mixer 갯수와 실제 캘된 mixer 갯수가 다를 수 있기 때문에 mixer 데이터를 삭제하고
        del New_String[7:]
        # Main ant의 mixer 넘버를 Mixer_no에 저장하고
        # Mixer_no의 길이만큼 0 으로 채워넣기 한다.
        for i in range(len(Mixer_no)):
            New_String.append(0)
            New_String.append(0)

        New_Mixer_no = New_String[7::2]
        New_Value = New_String[8::2]

        for i in Mixer_no:
            if count > (len(Old_Mixer_no) - 1):
                Old_Mixer_no.append(0)
                Old_Value.append(0)
            text_area.insert(tk.END, f"{Old_Mixer_no[count]:>3}  {Old_Value[count]:>4}\n")
            text_area.insert(tk.END, f"               | \u2192 ")
            New_Mixer_no[count] = str(i)
            New_Value[count] = str(round(Sub6_RX_Mixer_default[band, i, path] * 100))
            text_area.insert(tk.END, f"{New_Mixer_no[count]:>3}  {New_Value[count]:>4}\n")
            if i == Mixer_no[-1]:
                pass
            else:
                text_area.insert(tk.END, f"               |   ")
            count += 1
        text_area.insert(tk.END, f"\n")
        text_area.see(tk.END)
        New_String[7::2] = New_Mixer_no
        New_String[8::2] = New_Value

    else:
        del New_String[7:]
        New_String.append(0)

    New_String1 = "_".join(map(str, New_String[:7]))
    New_String2 = ",".join(map(str, New_String[7:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def Chng_fbrx_meas_spec_only(Selected_spc, rat, band, FBRX_Spec_var, text_area):
    FBRX_Spec = float(FBRX_Spec_var.get())
    new_text_content = ""
    Check = False
    if rat == "SUB6":
        target_word = f"[{rat}_n{band}_Calibration_Spec]"
        End_word = f"// APT"
    else:
        target_word = f"[{rat}_BAND{band}_Calibration_Spec]"
        End_word = f"// Rx Level"

    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(target_word):
            new_text_content += line
            Check = True
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check and line.startswith("TX_FBRX_FREQ"):
            New_String = fbrx_spec(line, "hspa", FBRX_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX_FBRX_Pow_Index_"):
            New_String = fbrx_spec(line, "nr", FBRX_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX_FBRX_Code_Index_"):
            New_String = fbrx_spec(line, "nr", FBRX_Spec * 100, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX_FBRX_Channel_Pow"):
            New_String = fbrxfreq_spec(line, "nr", FBRX_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX_FBRX_Channel_Code"):
            New_String = fbrxfreq_spec(line, "nr", FBRX_Spec * 100, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX2_FBRX_Pow_Index_"):
            New_String = fbrx_spec(line, "nr", FBRX_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX2_FBRX_Code_Index_"):
            New_String = fbrx_spec(line, "nr", FBRX_Spec * 100, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX2_FBRX_Channel_Pow"):
            New_String = fbrxfreq_spec(line, "nr", FBRX_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("TX2_FBRX_Channel_Code"):
            New_String = fbrxfreq_spec(line, "nr", FBRX_Spec * 100, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith(End_word):
            new_text_content += line
            Check = False

        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def fbrx_spec(line, rat, FBRX_Spec, text_area):
    String = re.split("[_=,\t\n]", line)
    String = [v for v in String if v]
    if rat == "hspa":
        if String[3] == "RIPPLE":
            text_area.insert(
                tk.END,
                f"{String[0]:<3}  {String[1]:<4}   {String[2]:>4}   {String[3]:>6}     | {String[5]:>5}\t{String[6]:>5}\t  \u2192  ",
            )
            FBRX_Value = [float(String[5]), float(String[6])]
            FBRX_mean = np.mean(FBRX_Value)
            String[4] = round(FBRX_mean)
            String[5] = round(FBRX_mean - FBRX_Spec)
            String[6] = round(FBRX_mean + FBRX_Spec)
            text_area.insert(tk.END, f"\t{String[5]:>5}\t{String[6]:>5}\n")
            text_area.see(tk.END)
            New_String1 = "_".join(map(str, String[:4]))
            New_String2 = "\t".join(map(str, String[4:]))
        else:
            text_area.insert(
                tk.END,
                f"{String[0]:<3}  {String[1]:<4}   {String[2]:>4}              | {String[4]:>5}\t{String[5]:>5}\t  \u2192  ",
            )
            FBRX_Value = [float(String[4]), float(String[5])]
            FBRX_mean = np.mean(FBRX_Value)
            String[3] = round(FBRX_mean)
            String[4] = round(FBRX_mean - FBRX_Spec)
            String[5] = round(FBRX_mean + FBRX_Spec)
            text_area.insert(tk.END, f"\t{String[4]:>5}\t{String[5]:>5}\n")
            text_area.see(tk.END)
            New_String1 = "_".join(map(str, String[:3]))
            New_String2 = "\t".join(map(str, String[3:]))
    elif rat == "nr":
        text_area.insert(
            tk.END,
            f" {String[0]:<3}{String[1]:^6}  {String[2]:<4}   {String[3]:<5}   {String[4]:<1}  | {String[6]:>5}\t{String[7]:>5}\t  \u2192  ",
        )
        FBRX_Value = [float(String[6]), float(String[7])]
        FBRX_mean = np.mean(FBRX_Value)
        String[5] = round(FBRX_mean)
        String[6] = round(FBRX_mean - FBRX_Spec)
        String[7] = round(FBRX_mean + FBRX_Spec)
        text_area.insert(tk.END, f"\t{String[6]:>5}\t{String[7]:>5}\n")
        text_area.see(tk.END)
        New_String1 = "_".join(map(str, String[:5]))
        New_String2 = "\t".join(map(str, String[5:]))

    New_String = New_String1 + "\t=\t" + New_String2 + "\n"

    return New_String


def fbrxfreq_spec(line, rat, FBRX_Spec, text_area):
    String = re.split("[_=,\t\n]", line)
    String = [v for v in String if v]
    if rat == "nr":
        text_area.insert(
            tk.END,
            f" {String[0]:<3}{String[1]:^6}  {String[2]:<6}{String[3]:<4}       | {String[5]:>5}\t{String[6]:>5}\t  \u2192  ",
        )
        FBRX_Value = [float(String[5]), float(String[6])]
        FBRX_mean = np.mean(FBRX_Value)
        String[4] = round(FBRX_mean)
        String[5] = round(FBRX_mean - FBRX_Spec)
        String[6] = round(FBRX_mean + FBRX_Spec)
        text_area.insert(tk.END, f"\t{String[5]:>5}\t{String[6]:>5}\n")
        text_area.see(tk.END)
        New_String1 = "_".join(map(str, String[:4]))
        New_String2 = "\t".join(map(str, String[4:]))
        New_String = New_String1 + "\t=\t" + New_String2 + "\n"

    return New_String


def Chng_rx_gain_spec_only(Selected_spc, rat, band, RX_Gain_Spec_var, text_area):
    RX_Gain_Spec = float(RX_Gain_Spec_var.get())
    new_text_content = ""
    Check = False

    if rat == "HSPA":
        Search_WD = f"[{rat}_BAND{band}_Calibration_Spec]"
        End_WD = f"TX_APT_PA_LOW_Index_0"
    elif rat == "SUB6":
        Search_WD = f"[{rat}_n{band}_Calibration_Spec]"
        End_WD = "// TX FBRX"

    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(Search_WD):
            new_text_content += line
            Check = True
            text_area.insert(tk.END, f"\n{Search_WD}\n")
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check and line.startswith("RX_Gain_main_"):
            New_String = change_rx_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("RX_Gain_4rx_"):
            New_String = change_rx_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("RX_RsrpOffset_main_"):
            New_String = change_rx_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("RX_RsrpOffset_4rx_"):
            New_String = change_rx_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("AGC_Rx1_LNAON_"):
            New_String = change_rx_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("AGC_Rx1_4RX_"):
            New_String = change_rx_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("AGC_Rx1_LNAON2_"):
            New_String = change_rx_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith("AGC_Rx1_Ch_"):
            New_String = change_rx_ch_spec(line, RX_Gain_Spec, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check and line.startswith(End_WD):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def change_rx_spec(line, RX_Gain_Spec, text_area):
    String = re.split("[_=,\t\n]", line)
    String = [v for v in String if v]
    if String[1] == "RsrpOffset":
        text_area.insert(
            tk.END, f"{String[0]:^4} RSRP   {String[2]:<6} {String[3]:<1}          | {String[5]:>5}\t{String[6]:>5}\t  \u2192  "
        )
    else:
        text_area.insert(
            tk.END,
            f"{String[0]:^4}{String[1]:^6}  {String[2]:<6} {String[3]:<1}          | {String[5]:>5}\t{String[6]:>5}\t  \u2192  ",
        )
    RX_Gain_Value = [float(String[5]), float(String[6])]
    RX_Gain_mean = np.mean(RX_Gain_Value)

    String[4] = round(RX_Gain_mean)
    String[5] = round(RX_Gain_mean - RX_Gain_Spec)
    String[6] = round(RX_Gain_mean + RX_Gain_Spec)

    text_area.insert(tk.END, f"\t{String[5]:>5}\t{String[6]:>5}\n")
    text_area.see(tk.END)
    New_String1 = "_".join(map(str, String[:4]))
    New_String2 = "\t".join(map(str, String[4:]))
    New_String = New_String1 + "\t=\t" + New_String2 + "\n"

    return New_String


def change_rx_ch_spec(line, RX_ch_Spec, text_area):
    String = re.split("[_=,\t\n]", line)
    String = [v for v in String if v]
    text_area.insert(
        tk.END,
        f"{String[0]:^4} {String[1]:<3} {String[2]:<2} {String[3]:<5}  {String[4]:<1}          | {String[6]:>5}\t{String[7]:>5}\t  \u2192  ",
    )
    RX_Gain_Value = [float(String[6]), float(String[7])]
    RX_Gain_mean = np.mean(RX_Gain_Value)

    String[5] = round(RX_Gain_mean)
    String[6] = round(RX_Gain_mean - RX_ch_Spec)
    String[7] = round(RX_Gain_mean + RX_ch_Spec)

    text_area.insert(tk.END, f"\t{String[6]:>5}\t{String[7]:>5}\n")
    text_area.see(tk.END)
    New_String1 = "_".join(map(str, String[:5]))
    New_String2 = "\t".join(map(str, String[5:]))
    New_String = New_String1 + "\t=\t" + New_String2 + "\n"

    return New_String