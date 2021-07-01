import numpy as np
import matplotlib.pyplot as plt
import wfdb

from simulacion.ecg.algoritmo_pan_tompkins import procesar_señal, graficar


def importar_archivo(s):
    record = wfdb.rdrecord(s)
    #print(record.__dict__)
    #wfdb.plot_wfdb(record, title=record.file_name)
    num_muestra = []
    valor = []

    for i in range(0,record.sig_len):
        num_muestra.append(i)
        valor.append(float(record.p_signal[i][0]))
    return num_muestra, valor, record.fs

def frecuencia_cardiaca(input, fetal, title):
    if fetal:
        limite_superior = 160
        limite_inferior = 120
        print("ECG FETAL")

    else:
         limite_superior = 100
         limite_inferior = 60

    print("La frecuencia cardíaca se considera normal entre: " + str(limite_inferior) + " y " + str(limite_superior))
    frecuencia_cardiaca =[]
    for i in range(len(input)-1):
        if(input[i+1]!=input[i]):
            frecuencia_cardiaca.append(fs*60/(input[i+1]-input[i]))
    # Grafico de la frecuencia media. Marco en el gráfico la frecuencia mímina y máxima que se considera bradicardia o taquicardia
    x = [x for x in range(len(frecuencia_cardiaca))]
    graficar(6, x, frecuencia_cardiaca, "Frecuencia cardíaca latido por latido", 30, 200, len(frecuencia_cardiaca), "n° latido", "Frecuencia [lat/min]", title)

    plt.plot([0, len(frecuencia_cardiaca)], [limite_inferior, limite_inferior], 'r')
    plt.plot([0, len(frecuencia_cardiaca)], [limite_superior, limite_superior], 'r')
    freq_media = np.mean(frecuencia_cardiaca)

    plt.figtext(0.05, 0.04, "Frecuecia media: " + str(int(freq_media)), fontsize=12, va="bottom", ha="left")
    print("La frecuencia cardíaca se considera normal entre: " + str(limite_inferior) + " y " + str(limite_superior))
    plt.figtext(0.05, 0.02, "La frecuencia cardíaca se considera normal entre: " + str(limite_inferior) + " y " + str(limite_superior), fontsize=12, va="bottom", ha="left")
    if (freq_media < limite_inferior):
        print("Bradicardia")
        plt.figtext(0.05, 0, "Bradicardia", fontsize=12, va="bottom", ha="left")
    elif (freq_media > limite_superior):
      print("Taquicardia")
      plt.figtext(0.05, 0, "Taquicardia", fontsize=12, va="bottom", ha="left")
    else:
        print("Frecuencia regular")
        plt.figtext(0.05, 0, "Frecuencia regular", fontsize=12, va="bottom", ha="left")
    plt.show()
    print("Frecuecia media: " + str(int(freq_media)))



if __name__ == "__main__":

    archivos_ecg = [{"title":"ECG Normal","filename":"111", "fetal":0},
                    {"title":"ECG Arritmia Taquicardia","filename":"233","fetal":0},
                    {"title":"ECG Arritmia Bradicardia","filename":"231","fetal":0},
                    {"title":"ECG Fetal","filename":"a02","fetal":1}];
    for i in range(len(archivos_ecg)):
        muestra, amplitudes,fs=importar_archivo(archivos_ecg[i]["filename"])
        salida = procesar_señal(muestra, amplitudes, fs, archivos_ecg[i]["title"])
        frecuencia_cardiaca(salida, archivos_ecg[i]["fetal"], archivos_ecg[i]["title"])

