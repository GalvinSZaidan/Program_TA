import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import math
import neurokit2 as nk
#install all libraries first

# Load data
dataset = pd.read_csv(r"C:\Users\galvi\Documents\Kuliah\Tugas Akhir\Data\Hasil Perekaman Alat 5 lead\3 Agustus 2024\aesan_duduk\Data_2_converted.csv", names=['I-mV', 'II-mV', 'V1-mV'], sep=',', skiprows=1, skipfooter=0, dtype=float)
t = (np.arange(0, len(dataset)))
#change the path to your dataset path for input

#start the program

# Preprocessing and plotting for each lead
for lead in ['I-mV', 'II-mV', 'V1-mV']:
    ecgmv = (dataset[lead]) 

    # Raw data plot
    plt.figure(figsize=(10, 6))
    plt.plot(t, ecgmv, color='blue')
    plt.title(f'Electrocardiogram Signal ({lead}) - Raw Data')
    plt.xlabel('Time [ms]')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)
    plt.tight_layout()
    
    # Baseline Correction
    detr_ecg = scipy.signal.detrend(ecgmv, axis=-1, type='linear', bp=0, overwrite_data=False)

    # Subplot for Baseline Correction, Butterworth, and FIR
    plt.figure(figsize=(10, 18))

    # Baseline Correction plot
    plt.subplot(3, 1, 1)
    plt.plot(t, detr_ecg, color='blue')
    plt.title(f'Signal ({lead}) - Baseline Correction')
    plt.xlabel('Time [ms]')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)


    # y-axis
    y = [e for e in detr_ecg]
    N = len(y)
    Fs = int(len(dataset) / 10) # Define Fs as the sampling frequency
    T = 1.0 / Fs
    
    b, a = scipy.signal.butter(4, 0.8, 'low')
    tempf_butter = scipy.signal.filtfilt(b, a, y)

    # Butterworth plot
    plt.subplot(3, 1, 2)
    plt.plot(t, tempf_butter, color='green')
    plt.title(f'Signal ({lead}) - Butterworth Filtered')
    plt.xlabel('Time [ms]')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)

    # FIR filter
    Fsf = int(len(dataset) / 10)
    cutoff_hz = 1
    min_Fsf = 2 * cutoff_hz
    if Fsf < min_Fsf:
        Fsf = min_Fsf

    nyq_rate = Fsf / 2
    width = 2.0 / nyq_rate
    attenuation_db = 60.0
    O, beta = scipy.signal.kaiserord(attenuation_db, width)
    if O % 2 == 0:
        O += 1
    else:
        O, beta = scipy.signal.kaiserord(attenuation_db, width)

    taps = scipy.signal.firwin(O, cutoff_hz/nyq_rate, window=('kaiser', beta), pass_zero=False)
    y_filt = scipy.signal.lfilter(taps, 1.0, tempf_butter)

    # FIR plot
    plt.subplot(3, 1, 3)
    plt.plot(t, y_filt, color='red')
    plt.title(f'Signal ({lead}) - FIR Filtered')
    plt.xlabel('Time [ms]')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)
    plt.tight_layout()

    # PQRST Peak Detection
    _, rpeaks = nk.ecg_peaks(y_filt, sampling_rate=Fs)
    signal_dwt, waves_dwt = nk.ecg_delineate(y_filt, rpeaks, sampling_rate=Fs, method="dwt")

    # Remove Nan and change to ndarray int
    peaksR = np.array([x for x in rpeaks['ECG_R_Peaks'] if math.isnan(x) is False]).astype(int)
    peaksP = np.array([x for x in waves_dwt['ECG_P_Peaks'] if math.isnan(x) is False]).astype(int)
    peaksQ = np.array([x for x in waves_dwt['ECG_Q_Peaks'] if math.isnan(x) is False]).astype(int)
    peaksS = np.array([x for x in waves_dwt['ECG_S_Peaks'] if math.isnan(x) is False]).astype(int)
    peaksT = np.array([x for x in waves_dwt['ECG_T_Peaks'] if math.isnan(x) is False]).astype(int)
    peaksPOnsets = np.array([x for x in waves_dwt['ECG_P_Onsets'] if math.isnan(x) is False]).astype(int)
    peaksPOffsets = np.array([x for x in waves_dwt['ECG_P_Offsets'] if math.isnan(x) is False]).astype(int)
    peaksROnsets = np.array([x for x in waves_dwt['ECG_R_Onsets'] if math.isnan(x) is False]).astype(int)
    peaksROffsets = np.array([x for x in waves_dwt['ECG_R_Offsets'] if math.isnan(x) is False]).astype(int)
    peaksTOnsets = np.array([x for x in waves_dwt['ECG_T_Onsets'] if math.isnan(x) is False]).astype(int)
    peaksTOffsets = np.array([x for x in waves_dwt['ECG_T_Offsets'] if math.isnan(x) is False]).astype(int)

    # Remove Nan and change to ndarray int
    rpeaks['ECG_R_Peaks'] = np.array([x for x in rpeaks['ECG_R_Peaks'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_P_Peaks'] = np.array([x for x in waves_dwt['ECG_P_Peaks'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_Q_Peaks'] = np.array([x for x in waves_dwt['ECG_Q_Peaks'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_S_Peaks'] = np.array([x for x in waves_dwt['ECG_S_Peaks'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_T_Peaks'] = np.array([x for x in waves_dwt['ECG_T_Peaks'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_P_Onsets'] = np.array([x for x in waves_dwt['ECG_P_Onsets'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_P_Offsets'] = np.array([x for x in waves_dwt['ECG_P_Offsets'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_R_Onsets'] = np.array([x for x in waves_dwt['ECG_R_Onsets'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_R_Offsets'] = np.array([x for x in waves_dwt['ECG_R_Offsets'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_T_Onsets'] = np.array([x for x in waves_dwt['ECG_T_Onsets'] if math.isnan(x) is False]).astype(int)
    waves_dwt['ECG_T_Offsets'] = np.array([x for x in waves_dwt['ECG_T_Offsets'] if math.isnan(x) is False]).astype(int)

    # Correcting first cycle
    if rpeaks['ECG_R_Peaks'][0] < waves_dwt['ECG_P_Onsets'][0]:
        rpeaks['ECG_R_Peaks'] = np.delete(rpeaks['ECG_R_Peaks'], 0)
    if waves_dwt['ECG_P_Peaks'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_P_Peaks'] = np.delete(peaksP, 0)
    if waves_dwt['ECG_Q_Peaks'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_Q_Peaks'] = np.delete(waves_dwt['ECG_Q_Peaks'], 0)
    if waves_dwt['ECG_S_Peaks'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_S_Peaks'] = np.delete(waves_dwt['ECG_S_Peaks'], 0)
    if waves_dwt['ECG_T_Peaks'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_T_Peaks'] = np.delete(waves_dwt['ECG_T_Peaks'], 0)
    if waves_dwt['ECG_P_Offsets'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_P_Offsets'] = np.delete(waves_dwt['ECG_P_Offsets'], 0)
    if waves_dwt['ECG_R_Offsets'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_R_Offsets'] = np.delete(waves_dwt['ECG_R_Offsets'], 0)
    if waves_dwt['ECG_T_Offsets'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_T_Offsets'] = np.delete(waves_dwt['ECG_T_Offsets'], 0)
    if waves_dwt['ECG_R_Onsets'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_R_Onsets'] = np.delete(waves_dwt['ECG_R_Onsets'], 0)
    if waves_dwt['ECG_T_Onsets'][0] < waves_dwt['ECG_P_Onsets'][0]:
        waves_dwt['ECG_T_Onsets'] = np.delete(waves_dwt['ECG_T_Onsets'], 0)
    if waves_dwt['ECG_R_Offsets'][0] < rpeaks['ECG_R_Peaks'][0]:
        waves_dwt['ECG_R_Offsets'] = np.delete(waves_dwt['ECG_R_Offsets'], 0)
    if waves_dwt['ECG_T_Offsets'][0] < rpeaks['ECG_R_Peaks'][0]:
        waves_dwt['ECG_T_Offsets'] = np.delete(waves_dwt['ECG_T_Offsets'], 0)
    if waves_dwt['ECG_T_Onsets'][0] < rpeaks['ECG_R_Peaks'][0]:
        waves_dwt['ECG_T_Onsets'] = np.delete(waves_dwt['ECG_T_Onsets'], 0)
    if waves_dwt['ECG_S_Peaks'][0] < rpeaks['ECG_R_Peaks'][0]:
        waves_dwt['ECG_S_Peaks'] = np.delete(waves_dwt['ECG_S_Peaks'], 0)
    if waves_dwt['ECG_T_Peaks'][0] < rpeaks['ECG_R_Peaks'][0]:
        waves_dwt['ECG_T_Peaks'] = np.delete(waves_dwt['ECG_T_Peaks'], 0)

    if y_filt[rpeaks['ECG_R_Peaks']][0] < y_filt[rpeaks['ECG_R_Peaks']][1]/2:
        rpeaks['ECG_R_Peaks'] = np.delete(rpeaks['ECG_R_Peaks'], 0)
        waves_dwt['ECG_P_Peaks'] = np.delete(waves_dwt['ECG_P_Peaks'], 0)
        waves_dwt['ECG_Q_Peaks'] = np.delete(waves_dwt['ECG_Q_Peaks'], 0)
        waves_dwt['ECG_S_Peaks'] = np.delete(waves_dwt['ECG_S_Peaks'], 0)
        waves_dwt['ECG_T_Peaks'] = np.delete(waves_dwt['ECG_T_Peaks'], 0)
        waves_dwt['ECG_R_Onsets'] = np.delete(waves_dwt['ECG_R_Onsets'], 0)
        waves_dwt['ECG_R_Offsets'] = np.delete(waves_dwt['ECG_R_Offsets'], 0)
        waves_dwt['ECG_P_Onsets'] = np.delete(waves_dwt['ECG_P_Onsets'], 0)
        waves_dwt['ECG_P_Offsets'] = np.delete(waves_dwt['ECG_P_Offsets'], 0)
        waves_dwt['ECG_T_Onsets'] = np.delete(waves_dwt['ECG_T_Onsets'], 0)
        waves_dwt['ECG_T_Offsets'] = np.delete(waves_dwt['ECG_T_Offsets'], 0)

    # Correcting last cycle
    if rpeaks['ECG_R_Peaks'][len( rpeaks['ECG_R_Peaks']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        rpeaks['ECG_R_Peaks'] = np.delete( rpeaks['ECG_R_Peaks'], (len( rpeaks['ECG_R_Peaks']) - 1))
    if waves_dwt['ECG_P_Peaks'][len( waves_dwt['ECG_P_Peaks']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_P_Peaks'] = np.delete( waves_dwt['ECG_P_Peaks'], (len( waves_dwt['ECG_P_Peaks']) - 1))
    if waves_dwt['ECG_Q_Peaks'][len(waves_dwt['ECG_Q_Peaks']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_Q_Peaks'] = np.delete(waves_dwt['ECG_Q_Peaks'], (len(waves_dwt['ECG_Q_Peaks']) - 1))
    if waves_dwt['ECG_S_Peaks'][len(waves_dwt['ECG_S_Peaks']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_S_Peaks'] = np.delete(peaksS, (len(waves_dwt['ECG_S_Peaks']) - 1))
    if waves_dwt['ECG_T_Peaks'][len(waves_dwt['ECG_T_Peaks']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_T_Peaks'] = np.delete(waves_dwt['ECG_T_Peaks'], (len(waves_dwt['ECG_T_Peaks']) - 1))
    if waves_dwt['ECG_P_Onsets'][len(waves_dwt['ECG_P_Onsets']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_P_Onsets'] = np.delete(waves_dwt['ECG_P_Onsets'], (len(waves_dwt['ECG_P_Onsets']) - 1))
    if waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_T_Offsets'] = np.delete(waves_dwt['ECG_T_Offsets'], (len(waves_dwt['ECG_T_Offsets']) - 1))
    if waves_dwt['ECG_T_Onsets'][len(waves_dwt['ECG_T_Onsets']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_T_Onsets'] = np.delete(waves_dwt['ECG_T_Onsets'], (len(waves_dwt['ECG_T_Onsets']) - 1))
    if waves_dwt['ECG_R_Onsets'][len(waves_dwt['ECG_R_Onsets']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_R_Onsets'] = np.delete(waves_dwt['ECG_R_Onsets'], (len(waves_dwt['ECG_R_Onsets']) - 1))
    if waves_dwt['ECG_R_Offsets'][len(waves_dwt['ECG_R_Offsets']) - 1] > waves_dwt['ECG_T_Offsets'][len(waves_dwt['ECG_T_Offsets']) - 1]:
        waves_dwt['ECG_R_Offsets'] = np.delete(waves_dwt['ECG_R_Offsets'], (len(waves_dwt['ECG_R_Offsets']) - 1))

    if waves_dwt['ECG_P_Peaks'][len(waves_dwt['ECG_P_Peaks']) - 1] > rpeaks['ECG_R_Peaks'][len(rpeaks['ECG_R_Peaks']) - 1]:
        waves_dwt['ECG_P_Peaks'] = np.delete(waves_dwt['ECG_P_Peaks'], (len(waves_dwt['ECG_P_Peaks']) - 1))
    if waves_dwt['ECG_Q_Peaks'][len(waves_dwt['ECG_Q_Peaks']) - 1] > rpeaks['ECG_R_Peaks'][len(rpeaks['ECG_R_Peaks']) - 1]:
        waves_dwt['ECG_Q_Peaks'] = np.delete(waves_dwt['ECG_Q_Peaks'], (len(waves_dwt['ECG_Q_Peaks']) - 1))
    if waves_dwt['ECG_P_Onsets'][len(waves_dwt['ECG_P_Onsets']) - 1] > rpeaks['ECG_R_Peaks'][len(rpeaks['ECG_R_Peaks']) - 1]:
        waves_dwt['ECG_P_Onsets'] = np.delete(waves_dwt['ECG_P_Onsets'], (len(waves_dwt['ECG_P_Onsets']) - 1))
    if waves_dwt['ECG_P_Offsets'][len(waves_dwt['ECG_P_Offsets']) - 1] > rpeaks['ECG_R_Peaks'][len(rpeaks['ECG_R_Peaks']) - 1]:
        waves_dwt['ECG_P_Offsets'] = np.delete(waves_dwt['ECG_P_Offsets'], (len(waves_dwt['ECG_P_Offsets']) - 1))
    if waves_dwt['ECG_R_Onsets'][len(waves_dwt['ECG_R_Onsets']) - 1] > rpeaks['ECG_R_Peaks'][len(rpeaks['ECG_R_Peaks']) - 1]:
        waves_dwt['ECG_R_Onsets'] = np.delete(waves_dwt['ECG_R_Onsets'], (len(waves_dwt['ECG_R_Onsets']) - 1))

    # Further processing for each lead
    if lead == 'II-mV':
        # Calculate RR, PR, QT, BPM for lead II_mV
        RR_list = []
        cnt = 0
        while (cnt < (len(rpeaks['ECG_R_Peaks']) - 1)):
            RR_interval = (rpeaks['ECG_R_Peaks'][cnt + 1] - rpeaks['ECG_R_Peaks'][cnt])
            RRms_dist = ((RR_interval / Fs) * 1000.0)  # Convert sample distances to ms distances
            RR_list.append(RRms_dist)
            cnt += 1
        dfRR = pd.DataFrame(RR_list)
        dfRR = dfRR.fillna(0)
        RR_stdev = np.std(RR_list, axis=None)  # Save Average to RRstdev
        sum = 0.0
        count = 0.0
        for index in range(len(RR_list)):

            if (np.isnan(RR_list[index]) == True):
                continue
            else:
                sum += RR_list[index]
                count += 1
            # print(sum / count)
            RR_avg = (sum / count)

        # PR interval
        PR_peak_list = []
        idex = ([x for x in range(0, len(waves_dwt['ECG_R_Onsets']) - 1)])
        for i in idex:
            if waves_dwt['ECG_R_Onsets'][i] < waves_dwt['ECG_P_Onsets'][i]:
                cnt = 0
                while (cnt < (len(waves_dwt['ECG_R_Onsets']) - 1)):
                    PR_peak_interval = (waves_dwt['ECG_Q_Peaks'][cnt] - waves_dwt['ECG_P_Onsets'][cnt])
                    ms_dist = ((PR_peak_interval / Fs) * 1000.0)  # Convert sample distances to ms distances
                    PR_peak_list.append(ms_dist)
                    cnt += 1
            else:
                cnt = 0
                while (cnt < (len(waves_dwt['ECG_R_Onsets']) - 1)):
                    PR_peak_interval = (waves_dwt['ECG_R_Onsets'][cnt] - waves_dwt['ECG_P_Onsets'][cnt])
                    ms_dist = ((PR_peak_interval / Fs) * 1000.0)  # Convert sample distances to ms distances
                    PR_peak_list.append(ms_dist)
                    cnt += 1
        dfPR = pd.DataFrame(PR_peak_list)
        dfPR = dfPR.fillna(0)
        PR_stdev = np.std(PR_peak_list, axis=None)  # Save Average to RRstdev
        sum = 0.0
        count = 0.0
        for index in range(len(PR_peak_list)):

            if (np.isnan(PR_peak_list[index]) == True):
                continue
            else:
                sum += PR_peak_list[index]
                count += 1
            # print(sum / count)
            PR_avg = (sum / count)

        # QS interval
        QS_peak_list = []
        try:
            idex = ([x for x in range(0, len(waves_dwt['ECG_S_Peaks']) - 1)])
            for i in idex:
                if waves_dwt['ECG_S_Peaks'][i] < waves_dwt['ECG_Q_Peaks'][i]:
                    QRS_complex = (waves_dwt['ECG_S_Peaks'][i + 1] - waves_dwt['ECG_Q_Peaks'][i])
                    ms_dist = ((QRS_complex / Fs) * 1000.0)  # Convert sample distances to ms distances
                    QS_peak_list.append(ms_dist)
                else:
                    QRS_complex = (waves_dwt['ECG_S_Peaks'][i] - waves_dwt['ECG_Q_Peaks'][i])
                    ms_dist = ((QRS_complex / Fs) * 1000.0)  # Convert sample distances to ms distances
                    QS_peak_list.append(ms_dist)
        except:
            print("QRS width Error")

        dfQS = pd.DataFrame(QS_peak_list)
        dfQS = dfQS.fillna(0)
        QS_stdev = np.std(QS_peak_list, axis=None)  # Save Average to RRstdev
        sum = 0.0
        count = 0.0
        for index in range(len(QS_peak_list)):

            if (np.isnan(QS_peak_list[index]) == True):
                continue
            else:
                sum += QS_peak_list[index]
                count += 1
            # print(sum / count)
            QS_avg = (sum / count)
        
        # QT interval
        QT_peak_list = []
        try:
            idex = ([x for x in range(0, len(waves_dwt['ECG_T_Offsets']) - 1)])
            for i in idex:
                if waves_dwt['ECG_T_Offsets'][i] < waves_dwt['ECG_R_Onsets'][i]:
                    QTdeff = (waves_dwt['ECG_T_Offsets'][i + 1] - waves_dwt['ECG_R_Onsets'][i])
                    ms_dist = ((QTdeff / Fs) * 1000.0)  # Convert sample distances to ms distances
                    QT_peak_list.append(ms_dist)
                else:
                    QTdeff = (waves_dwt['ECG_T_Offsets'][i] - waves_dwt['ECG_R_Onsets'][i])
                    ms_dist = ((QTdeff / Fs) * 1000.0)  # Convert sample distances to ms
                    QT_peak_list.append(ms_dist)

        except:
            print("QT Interval Error")

        dfQT = pd.DataFrame(QT_peak_list)
        dfQT = dfQT.fillna(0)
        QT_stdev = np.std(QT_peak_list, axis=None)  # Save Average to RRstdev
        sum = 0.0
        count = 0.0
        for index in range(len(QT_peak_list)):
            if (np.isnan(QT_peak_list[index]) == True):
                continue
            else:
                sum += QT_peak_list[index]
                count += 1
            # print(sum / count)
            QT_avg = (sum / count)
        QTc_avg = QT_avg / (math.sqrt(np.mean(RR_list)/ 1000))

        #BPM
        bpm = 60000 / np.mean(RR_list)  # 60000 ms (1 minute) / average R-R interval of signal

        print('\nII_mV - RR Interval (ms) - Mean:', RR_avg, ', Standard Deviation:', RR_stdev)
        print('II_mV - PR Interval (ms) - Mean:', PR_avg, ', Standard Deviation:', PR_stdev)
        print('II_mV - QS Interval (ms) - Mean:', QS_avg, ', Standard Deviation:', QS_stdev)
        print('II_mV - QT Interval (ms) - Mean:', QT_avg, ', Standard Deviation:', QT_stdev)
        print('II_mV - QTc Interval (ms) - Mean:', QTc_avg)
        print('II_mV - BPM:', bpm)
        plt.figure(figsize=(10, 6))
        plt.title(f'Electrocardiogram Signal ({lead}) - PQRST Peaks Detection')
        plt.plot(y_filt, color='orange', label="Filtered Data")
        plt.plot(waves_dwt['ECG_P_Peaks'], y_filt[waves_dwt['ECG_P_Peaks']], "x", color='blue', label="P Peak")
        plt.plot(waves_dwt['ECG_P_Onsets'], y_filt[waves_dwt['ECG_P_Onsets']], "o", color='blue', label="P Onset")
        plt.plot(waves_dwt['ECG_P_Offsets'], y_filt[waves_dwt['ECG_P_Offsets']], "o", color='blue', label="P Offset")
        plt.plot(waves_dwt['ECG_Q_Peaks'], y_filt[waves_dwt['ECG_Q_Peaks']], "x", color='green', label="Q Peak")
        plt.plot(rpeaks['ECG_R_Peaks'], y_filt[rpeaks['ECG_R_Peaks']], "x", color='black', label="R Peak")
        plt.plot(waves_dwt['ECG_R_Onsets'], y_filt[waves_dwt['ECG_R_Onsets']], "o", color='black', label="R Onset")
        plt.plot(waves_dwt['ECG_R_Offsets'], y_filt[waves_dwt['ECG_R_Offsets']], "o", color='black', label="R Offset")
        plt.plot(waves_dwt['ECG_S_Peaks'], y_filt[waves_dwt['ECG_S_Peaks']], "x", color='red', label="S Peak")
        plt.plot(waves_dwt['ECG_T_Peaks'], y_filt[waves_dwt['ECG_T_Peaks']], "x", color='purple', label="T Peak")
        plt.plot(waves_dwt['ECG_T_Onsets'], y_filt[waves_dwt['ECG_T_Onsets']], "o", color='purple', label="T Onset")
        plt.plot(waves_dwt['ECG_T_Offsets'], y_filt[waves_dwt['ECG_T_Offsets']], "o", color='purple', label="T Offset")
        plt.xlabel('Time [ms]')
        plt.ylabel('Amplitude [mV]')
        plt.legend(loc="lower left")
        for i, j in zip(waves_dwt['ECG_P_Peaks'], y_filt[waves_dwt['ECG_P_Peaks']]):
            plt.annotate('P', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_Q_Peaks'], y_filt[waves_dwt['ECG_Q_Peaks']]):
            plt.annotate('Q', xy=(i, j))
        for i, j in zip(rpeaks['ECG_R_Peaks'], y_filt[rpeaks['ECG_R_Peaks']]):
            plt.annotate('R', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_S_Peaks'], y_filt[waves_dwt['ECG_S_Peaks']]):
            plt.annotate('S', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_T_Peaks'], y_filt[waves_dwt['ECG_T_Peaks']]):
            plt.annotate('T', xy=(i, j))

    elif lead == 'I-mV':
        
        ST_peak_list = []
        try:
            for i in ([x for x in range(0, len(waves_dwt['ECG_T_Onsets']) - 1)]):
                if waves_dwt['ECG_T_Onsets'][i] < waves_dwt['ECG_R_Offsets'][i]:
                    cnt = 0
                    while (cnt < (len(waves_dwt['ECG_T_Onsets']) - 1)):
                        ST_peak_interval = (waves_dwt['ECG_T_Onsets'][cnt+1] - waves_dwt['ECG_R_Offsets'][cnt])
                        ms_dist = ((ST_peak_interval / Fs) * 1000.0)  # Convert sample distances to ms distances
                        ST_peak_list.append(ms_dist)
                        cnt += 1
                else:
                    cnt = 0
                    while (cnt < (len(waves_dwt['ECG_T_Onsets']) - 1)):
                        ST_peak_interval = (waves_dwt['ECG_T_Onsets'][cnt] - waves_dwt['ECG_R_Offsets'][cnt])
                        ms_dist = ((ST_peak_interval / Fs) * 1000.0)  # Convert sample distances to ms distances
                        ST_peak_list.append(ms_dist)
                        cnt += 1
        except:
            print("Error in calculating ST interval for I_mV")

        dfST = pd.DataFrame(ST_peak_list)
        dfST = dfST.fillna(0)
        ST_stdev = np.std(ST_peak_list, axis=None)  # Save Average to RRstdev
        sum = 0.0
        count = 0.0
        for index in range(len(ST_peak_list)):

            if (np.isnan(ST_peak_list[index]) == True):
                continue
            else:
                sum += ST_peak_list[index]
                count += 1
            # print(sum / count)
            ST_avg = (sum / count)

        print('\nI_mV - ST Interval (ms) - Mean:', ST_avg, ', Standard Deviation:', ST_stdev)
        plt.figure(figsize=(10, 6))
        plt.title(f'Electrocardiogram Signal ({lead}) - PQRST Peaks Detection')
        plt.plot(y_filt, color='orange', label="Filtered Data")
        plt.plot(rpeaks['ECG_R_Peaks'], y_filt[rpeaks['ECG_R_Peaks']], "x", color='black', label="R Peak")
        plt.plot(waves_dwt['ECG_P_Peaks'], y_filt[waves_dwt['ECG_P_Peaks']], "x", color='blue', label="P Peak")
        plt.plot(waves_dwt['ECG_Q_Peaks'], y_filt[waves_dwt['ECG_Q_Peaks']], "x", color='green', label="Q Peak")
        plt.plot(waves_dwt['ECG_S_Peaks'], y_filt[waves_dwt['ECG_S_Peaks']], "x", color='red', label="S Peak")
        plt.plot(waves_dwt['ECG_T_Peaks'], y_filt[waves_dwt['ECG_T_Peaks']], "x", color='purple', label="T Peak")
        plt.xlabel('Time [ms]')
        plt.ylabel('Amplitude [mV]')
        plt.legend(loc="lower left")
        for i, j in zip(waves_dwt['ECG_P_Peaks'], y_filt[waves_dwt['ECG_P_Peaks']]):
            plt.annotate('P', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_Q_Peaks'], y_filt[waves_dwt['ECG_Q_Peaks']]):
            plt.annotate('Q', xy=(i, j))
        for i, j in zip(rpeaks['ECG_R_Peaks'], y_filt[rpeaks['ECG_R_Peaks']]):
            plt.annotate('R', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_S_Peaks'], y_filt[waves_dwt['ECG_S_Peaks']]):
            plt.annotate('S', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_T_Peaks'], y_filt[waves_dwt['ECG_T_Peaks']]):
            plt.annotate('T', xy=(i, j))

    elif lead == 'V1-mV':
        # _, rpeaks_V1 = nk.ecg_peaks(y_filt, sampling_rate=Fs)
        # signal_dwt_V1, waves_dwt_V1 = nk.ecg_delineate(y_filt, rpeaks_V1, sampling_rate=Fs, method="dwt")

        if 'ECG_S_Peaks' in waves_dwt.keys() :

            R_mean_amp_V1 = np.mean([y_filt[int(i)] for i in rpeaks['ECG_R_Peaks']]) #if not np.isnan(i)])
            S_mean_amp_V1 = np.mean([y_filt[int(i)] for i in waves_dwt['ECG_S_Peaks']]) #if not np.isnan(i)])

            RS_ratio_V1 =(R_mean_amp_V1) / abs(S_mean_amp_V1)
            print('\nV1_mV - R/S Ratio:', RS_ratio_V1)
        else:
            print("\nTidak ada puncak R yang ditemukan pada sinyal V1_mV.")

        plt.figure(figsize=(10, 6))
        plt.title(f'Electrocardiogram Signal ({lead}) - PQRST Peaks Detection')
        plt.plot(y_filt, color='orange', label="Filtered Data")
        plt.plot(rpeaks['ECG_R_Peaks'], y_filt[rpeaks['ECG_R_Peaks']], "x", color='black', label="R Peak")
        plt.plot(waves_dwt['ECG_P_Peaks'], y_filt[waves_dwt['ECG_P_Peaks']], "x", color='blue', label="P Peak")
        plt.plot(waves_dwt['ECG_Q_Peaks'], y_filt[waves_dwt['ECG_Q_Peaks']], "x", color='green', label="Q Peak")
        plt.plot(waves_dwt['ECG_S_Peaks'], y_filt[waves_dwt['ECG_S_Peaks']], "x", color='red', label="S Peak")
        plt.plot(waves_dwt['ECG_T_Peaks'], y_filt[waves_dwt['ECG_T_Peaks']], "x", color='purple', label="T Peak")
        plt.xlabel('Time [ms]')
        plt.ylabel('Amplitude [mV]')
        plt.legend(loc="lower left")
        for i, j in zip(waves_dwt['ECG_P_Peaks'], y_filt[waves_dwt['ECG_P_Peaks']]):
            plt.annotate('p', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_Q_Peaks'], y_filt[waves_dwt['ECG_Q_Peaks']]):
            plt.annotate('Q', xy=(i, j))
        for i, j in zip(rpeaks['ECG_R_Peaks'], y_filt[rpeaks['ECG_R_Peaks']]):
            plt.annotate('R', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_S_Peaks'], y_filt[waves_dwt['ECG_S_Peaks']]):
            plt.annotate('S', xy=(i, j))
        for i, j in zip(waves_dwt['ECG_T_Peaks'], y_filt[waves_dwt['ECG_T_Peaks']]):
            plt.annotate('T', xy=(i, j))
  
packedData = {
            "rr": RR_avg,
            # "rr_stdev": RR_stdev,
            "pr": PR_avg,
            # "pr_stdev": PR_stdev,
            "qs": QS_avg,
            # "qs_stdev": QS_stdev,
            "qtc": QTc_avg,
            # "qt_stdev": QT_stdev,
            "st": ST_avg,
            # "st_stdev": ST_stdev,
            "r/s ratio" : RS_ratio_V1,
            "heartrate": bpm,
           }

# first input
# use this to save the first input data
# df = pd.DataFrame([packedData])
# df.to_excel(r"C:\\Users\galvi\Documents\Kuliah\Tugas Akhir\Data\Hasil Perekaman Alat 5 lead\3 Agustus 2024/aesan_duduk/HasilOlahDatax.xlsx", index=False)
# print(packedData)

#new data
# use this to save next new data
# df = pd.DataFrame([packedData])
# filepath = r'C:\Users\galvi\Documents\Kuliah\Tugas Akhir\Data\Hasil Perekaman Alat 5 lead\3 Agustus 2024\aesan_duduk/HasilOlahDatax.xlsx'
# with pd.ExcelWriter(
#         filepath,
#         engine='openpyxl',
#         mode='a',
#         if_sheet_exists='overlay') as writer:
#     reader = pd.read_excel(r'C:\Users\galvi\Documents\Kuliah\Tugas Akhir\Data\Hasil Perekaman Alat 5 lead\3 Agustus 2024\aesan_duduk\HasilOlahDatax.xlsx')
#     df.to_excel(
#         writer,
#         startrow=reader.shape[0] + 1,
#         index=False,
#         header=False)

plt.show()
