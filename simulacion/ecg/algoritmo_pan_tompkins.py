import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

def graficar(i, x, y, titulo, inf, sup, n,xlabel, ylabel, title):
    fig1 = plt.figure(title)
    fig1.subplots_adjust(hspace=0.75, wspace=0.75)
    ax = fig1.add_subplot(3, 2, i)
    ax.plot(x, y)
    plt.axis([-1, n, inf, sup])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.grid()


def aplicar_filtro_pasabanda(amplitudes, fs):
    b,a= signal.butter(3, [5*2/fs, 2*2/fs], btype='bandpass')
    n = signal.firwin(19, [5 * 2 / fs, 15 * 2 / fs], pass_zero=False)
    return signal.lfilter(n, 1, amplitudes)

def aplicar_filtro_derivativo(input):
    h_d = [-1 / 8, -2 / 8, 0, 2 / 8, 1 / 8]
    return signal.convolve(input, h_d)

def aplicar_alisado(input):
    salida = [0 for i in range(len(input))]

    for i in range(len(input)):
        salida[i] = input[i] ** 2
    return salida

def aplicar_filtro_media_movil(input):

    N = 25
    salida = [0] * len(input)

    for n in range(N - 1, len(input)):
        for i in range(N - 1):
            salida[n] = salida[n] + input[n - i]
        salida[n] = salida[n] / N
    return salida

def graficar_resultados(muestra, amplitudes, resultado_filtro, resultado_filtro_derivativo, resultado_alisado, resultado_media_movil, title):
    n = len(muestra)
    muestra2 = []
    for i in range(len(muestra)):
        muestra2.append(muestra[i])

    for i in range(len(resultado_filtro_derivativo) - n):
        muestra2.append(n + i)

    inicio = 0
    fin = 0
    avanzar = 1
    m = []
    umbral = np.mean(resultado_media_movil[0:len(resultado_media_movil)])

    while (avanzar):
        for i in range(fin, len(resultado_media_movil)):
            if (i == len(resultado_media_movil) - 200):
                avanzar = 0
            if (resultado_media_movil[i] >= umbral):
                inicio = i
                break
        for i in range(inicio, len(resultado_media_movil)):
            if (resultado_media_movil[i] <= umbral):
                fin = i
                break
        if (inicio < fin and len(resultado_media_movil[inicio:fin]) > 0):
            #Armo un vector con las posiciones de cada pico R detectado
            m.append(inicio + np.argmax(resultado_media_movil[inicio:fin]))

    muestra_1 = []
    muestra_2 = []
    muestra_3 = []

    for i in m:
        muestra_1.append(i - 28)
        muestra_2.append(i - 24)
        muestra_3.append(i - 47)

    # número de muestras
    cantidad_muestras = 1500

    graficar_ecg(amplitudes, cantidad_muestras, muestra, title)

    graficar_filtro_pasa_banda(cantidad_muestras, muestra, resultado_filtro, title)

    graficar_filtro_derivativo(cantidad_muestras, muestra2, resultado_filtro_derivativo, title)

    graficar_alisado(cantidad_muestras, muestra2, resultado_alisado, title)

    graficar_media_movil(cantidad_muestras, muestra2, resultado_media_movil, title)

    plt.plot([0, cantidad_muestras], [umbral, umbral], 'g')
    plt.plot([inicio, inicio], [min(resultado_media_movil) - 0.001, (max(resultado_media_movil) + 0.001)], 'g')
    plt.plot([fin, fin], [min(resultado_media_movil) - 0.001, (max(resultado_media_movil) + 0.001)], 'g')

    return muestra_2


def graficar_media_movil(cantidad_muestras, muestra2, resultado_media_movil, title):
    graficar(5, muestra2, resultado_media_movil, "Media móvil", min(resultado_media_movil) - 0.001,
             (max(resultado_media_movil) + 0.001), cantidad_muestras, "numero muestras [n]", "amplitud [mV]", title)


def graficar_alisado(cantidad_muestras, muestra2, resultado_alisado, title):
    graficar(4, muestra2, resultado_alisado, "Alisado", min(resultado_alisado) - 0.01, (max(resultado_alisado) + 0.01),
             cantidad_muestras, "numero muestras [n]", "amplitud [mV]", title)


def graficar_filtro_derivativo(cantidad_muestras, muestra2, resultado_filtro_derivativo, title):
    graficar(3, muestra2, resultado_filtro_derivativo, "Filtro Derivativo", min(resultado_filtro_derivativo) - 0.01,
             (max(resultado_filtro_derivativo) + 0.01), cantidad_muestras, "numero muestras [n]", "amplitud [mV]",
             title)


def graficar_filtro_pasa_banda(cantidad_muestras, muestra, resultado_filtro, title):
    graficar(2, muestra, resultado_filtro, "Filtro Pasabanda", min(resultado_filtro) - 0.01,
             (max(resultado_filtro) + 0.01), cantidad_muestras, "numero muestras [n]", "amplitud [mV]", title)


def graficar_ecg(amplitudes, cantidad_muestras, muestra, title):
    graficar(1, muestra, amplitudes, "ECG", min(amplitudes) - 0.01, (max(amplitudes) + 0.01), cantidad_muestras,
             "numero muestras [n]", "amplitud [mV]", title)


def procesar_señal(muestra, amplitudes, fs, title) :
    resultado_filtro = aplicar_filtro_pasabanda(amplitudes, fs);
    resultado_filtro_derivativo = aplicar_filtro_derivativo(resultado_filtro);
    resultado_alisado = aplicar_alisado(resultado_filtro_derivativo);
    resultado_media_movil = aplicar_filtro_media_movil(resultado_alisado);
    return graficar_resultados(muestra, amplitudes, resultado_filtro, resultado_filtro_derivativo, resultado_alisado, resultado_media_movil, title);