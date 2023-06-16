import re
import tkinter as tk


def chng_3g_rx_gain_default(flag, Selected_spc, rat, band, HSPA_RX_Gain_default, text_area):
    if flag == "daseul":
        target_word = f"[{rat}_BAND{band}_CAL_PARAM]"
        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()
    elif flag == "mtm":
        target_word = f"[{rat}_CALIBRATION_PARAM_BAND{band}]"
        with open(Selected_spc, "r", encoding="latin_1") as file:
            data_lines = file.readlines()
        file.close()

    text_area.insert(tk.END, f"\n{target_word}\n")
    text_area.insert(tk.END, "-" * 100)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)

    new_text_content = ""
    Not_Duplicated = True
    Check = False
    enable_4RX = False

    for index, line in enumerate(data_lines):
        New_String = Old_String = line

        if line.startswith(target_word):
            new_text_content += line
            Check = True
        elif Check & Not_Duplicated & line.startswith("4RX_Cal_Mode="):
            Diversity = re.split("=| |//", line)
            if Diversity[1] == "3":
                enable_4RX = True
            Not_Duplicated = False
            new_text_content += line
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & line.startswith(f"RX_Gain_DRX_Default_LNAOn="):
            New_String = Rxgain_3g_cal(line, band, "Main", "DRX", "LNAON", 5, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"RX_Gain_DRX_Default_LNAOn2="):
            New_String = Rxgain_3g_cal(line, band, "Main", "DRX", "LNAON2", 5, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"RX_Gain_DRX_Default_BypassLNA="):
            New_String = Rxgain_3g_cal(line, band, "Main", "DRX", "LNABYP", 5, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & enable_4RX & line.startswith(f"RX_Gain_4RX(PRX)Default="):
            New_String = Rxgain_3g_cal(line, band, "4RX", "PRX", "LNAON", 3, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & enable_4RX & line.startswith(f"RX_Gain_4RX(DRX)Default="):
            New_String = Rxgain_3g_cal(line, band, "4RX", "DRX", "LNAON", 3, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
            enable_4RX = False
        elif Check & (line.startswith("ET_MODE")):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    # text_area.insert(tk.END, f"Tech= {rat}  \t| Band= {band:<7}\t| Ant= {Antenna}\t| Path= {Path}\n")
    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def Rxgain_3g_cal(line, band, ant, path, lna, Position, HSPA_RX_Gain_default, text_area):
    band = f"WB{band}"
    New_String = re.split(r"[_=,\n]", line)  # 띄어쓰기로 분리
    New_String = [v for v in New_String if v]

    if HSPA_RX_Gain_default[band][ant][path].get([lna]) is not None:
        text_area.insert(tk.END, f"{ant:<4} {path} {lna:<6}|   ")
        text_area.insert(tk.END, f"{New_String[Position]:>5}\n")

        New_String[Position] = round(HSPA_RX_Gain_default[band][ant][path][lna]) * 256

        text_area.insert(tk.END, f"               | \u2192 ")
        text_area.insert(tk.END, f"{New_String[Position]:>5}\n\n")
        text_area.see(tk.END)

    New_String1 = "_".join(map(str, New_String[:Position]))
    New_String = New_String1 + "=" + str(New_String[Position]) + "\n"

    return New_String


def chng_3g_rx_freq_default(
    flag, Selected_spc, rat, band, HSPA_RX_Freq_default, Bluetick, blue_3grx_freq, blue_3gdrx_offset, text_area
):
    if flag == "daseul":
        target_word = f"[{rat}_BAND{band}_CAL_PARAM]"
        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()
    elif flag == "mtm":
        target_word = f"[{rat}_CALIBRATION_PARAM_BAND{band}]"
        with open(Selected_spc, "r", encoding="latin_1") as file:
            data_lines = file.readlines()
        file.close()

    new_text_content = ""
    Check = False
    Enable_4RX = False

    for index, line in enumerate(data_lines):
        New_String = Old_String = line

        if line.startswith(target_word):
            new_text_content += line
            Check = True
        elif Check & line.startswith("4RX_Cal_Mode="):
            Diversity = re.split("=| |//", line)
            if Diversity[1] == "3":
                Enable_4RX = True
            new_text_content += line
        elif Check & line.startswith("RX_Comp_Ch="):
            result = re.split(r"[ |\t|//]", line)  # 띄어쓰기로 // 분리
            Freq_List = re.split("[=,\n]", result[0])[1:]
            Freq_List = [v for v in Freq_List if v]
            new_text_content += line
        elif Check & line.startswith(f"RX_Comp_DRX_Default="):
            New_String = Rxfreq_3g_cal(
                Freq_List,
                line,
                band,
                "Main",
                "DRX",
                4,
                HSPA_RX_Freq_default,
                Bluetick,
                blue_3grx_freq,
                blue_3gdrx_offset,
                text_area,
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"RX_Comp_4RX(PRX)Default="):
            New_String = Rxfreq_3g_cal(
                Freq_List,
                line,
                band,
                "4RX",
                "PRX",
                3,
                HSPA_RX_Freq_default,
                Bluetick,
                blue_3grx_freq,
                blue_3gdrx_offset,
                text_area,
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"RX_Comp_4RX(DRX)Default="):
            New_String = Rxfreq_3g_cal(
                Freq_List,
                line,
                band,
                "4RX",
                "DRX",
                3,
                HSPA_RX_Freq_default,
                Bluetick,
                blue_3grx_freq,
                blue_3gdrx_offset,
                text_area,
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"ET_MODE"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def Rxfreq_3g_cal(
    Freq_List, line, band, ant, path, Position, HSPA_RX_Freq_default, Bluetick, blue_3grx_freq, blue_3gdrx_offset, text_area
):
    band = f"WB{band}"
    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    text_area.insert(tk.END, f"{ant:<4} {path} FREQ  |   ")
    text_area.see(tk.END)

    for i in range(len(New_String[Position:])):
        if i == range(len(New_String[Position:]))[-1]:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5}\n")
            text_area.see(tk.END)
        else:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5}, ")
            text_area.see(tk.END)
    text_area.insert(tk.END, f"               | \u2192 ")

    del New_String[Position:]
    # Freq_List 길이만큼 0 으로 채워넣기 하고 값을 변경
    for i in range(len(Freq_List)):
        New_String.append(0)
        if Bluetick & (band == "WB5"):
            if int(Freq_List[i]) == blue_3grx_freq:
                New_String[Position + i] = int(
                    (round(HSPA_RX_Freq_default[band][ant][path][Freq_List[i]], 1) - blue_3gdrx_offset) * 256
                )
            else:
                New_String[Position + i] = int(round(HSPA_RX_Freq_default[band][ant][path][Freq_List[i]], 1) * 256)
        else:
            New_String[Position + i] = int(round(HSPA_RX_Freq_default[band][ant][path][Freq_List[i]], 1) * 256)

    for i in range(len(Freq_List)):
        if i == range(len(Freq_List))[-1]:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5}\n\n")
            text_area.see(tk.END)
        else:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5}, ")
            text_area.see(tk.END)
    text_area.see(tk.END)

    New_String1 = "_".join(map(str, New_String[:Position]))
    New_String2 = ",".join(map(str, New_String[Position:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def chng_3g_rfic_gain(Selected_spc, rat, band, RFIC_Spec_var, RFIC_gain, text_area):
    RFIC_gain_Spec = int(RFIC_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("TX_RFIC_GAIN_Index_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            gainindex = int(re.sub(r"[^0-9]", "", New_String[0]))
            text_area.insert(tk.END, f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t")
            text_area.see(tk.END)
            if gainindex == 0:
                New_String[3] = int(New_String[2]) - 0.1
                New_String[4] = int(New_String[2]) + 0.1
            elif gainindex <= 8:
                New_String[2] = round(RFIC_gain["WCDMA"][band]["Tx"][f"Index{gainindex} "])
                New_String[3] = New_String[2] - RFIC_gain_Spec
                New_String[4] = New_String[2] + RFIC_gain_Spec
            elif gainindex <= 12:
                value = round(RFIC_gain["WCDMA"][band]["Tx"][f"Index{gainindex} "])
                New_String[2] = value
                New_String[3] = New_String[2] - RFIC_gain_Spec - 5
                New_String[4] = New_String[2] + RFIC_gain_Spec + 5
            elif gainindex >= 13:
                if RFIC_gain["WCDMA"][band]["Tx"].get(f"Index{gainindex} ") is not None:
                    value = round(RFIC_gain["WCDMA"][band]["Tx"][f"Index{gainindex} "])
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
        elif line.startswith("TX_FBRX_GAIN_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_rx_gain(Selected_spc, rat, band, RX_Gain_3G_Spec_var, RXGain_3G, RxComp_3G, text_area):
    RX_Gain_Spec = int(RX_Gain_3G_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("AGC_Rx1_LNAON_0"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[2] = round(RXGain_3G[band])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("AGC_Rx1_Ch_LNAON_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            Read_index = int(Word[4])
            Index_count = RxComp_3G.loc[(band)].count()
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            if Read_index < Index_count:
                New_String[2] = round(RxComp_3G[band][Read_index])
                New_String[3] = New_String[2] - RX_Gain_Spec
                New_String[4] = New_String[2] + RX_Gain_Spec
            else:
                New_String[2] = 0
                New_String[3] = New_String[2] - RX_Gain_Spec
                New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            Word = "_".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_PA_LOW_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_fbrx_gain_meas(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Meas_3G, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("TX_FBRX_GAIN_Index_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            Read_index = int(Word[4])
            Index_count = FBRX_Gain_Meas_3G.loc[("WCDMA", band)].count()
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            if Read_index < Index_count:
                New_String[2] = round(FBRX_Gain_Meas_3G["WCDMA", band][Read_index])
                New_String[3] = New_String[2] - FBRX_Spec
                New_String[4] = New_String[2] + FBRX_Spec
            else:
                New_String[2] = 0
                New_String[3] = New_String[2] - FBRX_Spec
                New_String[4] = New_String[2] + FBRX_Spec
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            Word = "_".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("AGC_Rx1_LNAON_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_fbrx_gain_code(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Code_3G, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get()) * 100  # 1dB = 100
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
        elif Check & line.startswith("TX_Modulation_FBRX_Result"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[2] = round(FBRX_Gain_Code_3G["WCDMA", band][0])
            New_String[3] = New_String[2] - FBRX_Spec
            New_String[4] = New_String[2] + FBRX_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("AGC_Rx1_LNAON_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_fbrx_freq_meas(
    Selected_spc,
    rat,
    band,
    FBRX_3G_Spec_var,
    FBRX_Freq_Meas_3G,
    FBRX_Freq_Meas_3G_Max,
    FBRX_Freq_Meas_3G_Min,
    text_area,
):
    FBRX_Spec = int(FBRX_3G_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("TX_FBRX_FREQ	="):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            New_String[2] = round(FBRX_Freq_Meas_3G["WCDMA", band])
            New_String[3] = New_String[2] - FBRX_Spec
            New_String[4] = New_String[2] + FBRX_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX_FBRX_FREQ_RIPPLE	="):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}| {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            New_String[2] = round(FBRX_Freq_Meas_3G_Max["WCDMA", band]) - round(FBRX_Freq_Meas_3G_Min["WCDMA", band])
            New_String[3] = 0
            New_String[4] = New_String[2] + 3
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("AGC_Rx1_LNAON_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_apt(Selected_spc, rat, band, APT_Spec_var, APT_Meas_3G_Ave):
    APT_Spec = float(APT_Spec_var.get())  # 1dB = 100
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
        elif Check & line.startswith("TX_APT_PA_"):
            New_String = Old_String = line
            New_String = apt_3g(line, band, APT_Spec, APT_Meas_3G_Ave)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TxP_Channel_Comp_PA_MID_"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def apt_3g(line, band, APT_Spec, APT_Meas_NR_Ave):
    New_String = re.split("=|\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    Pa_stage = Word[3]
    Read_index = int(Word[5])
    Index_count = APT_Meas_NR_Ave.loc[(band, Pa_stage)].count()
    if Read_index < Index_count:
        New_String[1] = round(APT_Meas_NR_Ave[band, Pa_stage][Read_index])
        New_String[2] = round(APT_Meas_NR_Ave[band, Pa_stage][Read_index]) - APT_Spec
        New_String[3] = round(APT_Meas_NR_Ave[band, Pa_stage][Read_index]) + APT_Spec
    else:
        New_String[1] = -10
        New_String[2] = New_String[1] - 0.1
        New_String[3] = New_String[1] + 0.1
    Word = "_".join(Word) + "\t" + "="
    New_String[0] = Word
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String