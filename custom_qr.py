# Importando as libs
import argparse
import time
import cv2
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar

def qr_id():
    #Variable para salirse
    salir = False
    # Construye el analizador de argumentos y analiza los argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="resultado.csv",)
    args = vars(ap.parse_args())

    # Inicia la transmisión (inicia la cámara web) y permite que el sensor de la cámara se encienda
    print("[INFO] Iniciando la transmisión y el archivo .CSV")
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    # abra el archivo CSV de salida para guardar e inicializar el conjunto de
    # códigos de barras (código qr) encontrados hasta ahora
    csv = open(args["output"], "w")
    found = set()

    # loop del stream
    while True:
        #tomar el marco de la secuencia de video vinculada y cambiar su tamaño a
        #contiene un ancho máximo de 400 píxeles
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # encuentre los códigos de barras (código qr) en el tablero y 
        # decodifique cada uno de los códigos de barras
        barcodes = pyzbar.decode(frame)

        # recorrer los códigos de barras detectados
        for barcode in barcodes:
            # extraer la ubicación del cuadro delimitador del código de barras y dibujar
            # el cuadro delimitador que rodea el código de barras en la imagen (en este caso es verde)
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
            # los datos del código de barras son un objeto de byte, así que si queremos dibujarlo
            # en nuestra imagen de salida, primero debemos convertirla en una cadena
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # dibuja los datos del código de barras y el tipo de código de barras en la imagen
            text = "{}".format(barcodeData)
            print(text)
        

            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # No imprimí el texto que contiene los datos, etc., si desea mostrar
            # solo cambia el '' para texto, se vería así \ /
            # text = "{} ({})".format(barcodeData, barcodeType)
            # cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # si el texto del código de barras no está en nuestro archivo CSV, escribirá
            # la fecha y hora + código de barras en el disco y actualizar los datos

            # No quería la fecha y la hora, si lo desea, solo use este código a continuación \ /
            # csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))

            if barcodeData not in found:
                # aquí es opcional, lo puse solo para hacerle saber que el resultado se guardó
                # pygame es responsable de hacer una obra de sonido
                # pygame.mixer.init()
                # pygame.mixer.music.load('sucess.wav')
                # pygame.mixer.music.play()
                # fin del sonido

                csv.write("{}\n".format(barcodeData))
                csv.flush()

                found.clear()
                found.add(barcodeData)
                salir = True
        # Título del Frame
        cv2.imshow("Registro de tiempo", frame)
        key = cv2.waitKey(1) & 0xFF

        # Si se presionó la tecla 'q', se romperá el bucle y cerrará la ventana
        if key == ord("q") or salir == True:
            break

    # cierra el archivo CSV
    print("[INFO] Finalizando la secuencia y cerrando el archivo CSV ...")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()
    return text
