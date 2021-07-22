#!/usr/bin/python

#Library
import csv
import os, sys, time
import requests

from datetime import datetime
from requests.exceptions import ConnectionError

print (sys.argv)

import subprocess

# Clear the screen
subprocess.call('clear', shell=True)

print('Bienvenido al detector de header Server | X-Powered-By')
print(' ')

def main():

    print('Escoja una opcion disponible\n')
    print('[1] Una URL')
    print('[2] Multiple URL desde un archivo')

    print('[3] Salir.')
    print('\n')

    option = int(input('Opcion a seleccionar:'))
    now = datetime.now() # current date and time

    if (option == 2):
        urlFile = input('Ingrese IP Address(s) / URL(s):')

        try:
            #for url in textfile:
            pathOutput = input("Ingrese el nombre del archivo de salida: ")
            filename, ext = os.path.splitext(pathOutput)
            if not ext:
                ext = '.csv'
            pathOutput = filename + ext

            response = requests.request("GET", urlFile, verify=True)
            headServer = response.headers.get('Server')
            headPoweredBy = response.headers.get('X-Powered-By')
            headAspVer = response.headers.get('X-AspNet-Version')

            if headServer:
                print('Server:', headServer, '\n')
            if headPoweredBy:
                print('X-Powered-By:', headPoweredBy, '\n')
            if headAspVer:
                print('X-AspNet-Version:', headAspVer, '\n')
                
            headerCols = ("Nombre del Sitio","Server","X-Powered-By","X-AspNet-Version","Evidencia")
            with open(pathOutput, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(headerCols)
                spamwriter.writerow([urlFile, headServer, headPoweredBy, headAspVer])
        except ConnectionError:
            print ('Se omite la URL {url} no se obtuvo respuesta')

        print('\n[**] Proceso finalizado \n')
        print(f'[**] Resultado almacenado en {pathOutput} \n')
        main()

    if (option == 1):
        url = input('Ingrese IP Address / URL:')

        try:
            #for url in textfile:
            pathOutput = input("Ingrese el nombre del archivo de salida: ")
            filename, ext = os.path.splitext(pathOutput)
            if not ext:
                ext = '.csv'
            pathOutput = filename + ext

            response = requests.request("GET", url, verify=True)
            headServer = response.headers.get('Server')
            headPoweredBy = response.headers.get('X-Powered-By')
            headAspVer = response.headers.get('X-AspNet-Version')

            if headServer:
                print('Server:', headServer, '\n')
            if headPoweredBy:
                print('X-Powered-By:', headPoweredBy, '\n')
            if headAspVer:
                print('X-AspNet-Version:', headAspVer, '\n')
                
            headerCols = ("Nombre del Sitio","Server","X-Powered-By","X-AspNet-Version","Evidencia")
            with open(pathOutput, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(headerCols)
                spamwriter.writerow([url, headServer, headPoweredBy, headAspVer])
        except ConnectionError:
            print ('Ha fallado obtener respuesta de la URL {url}')

        print('\n[**] Proceso finalizado. \n')
        print(f'[**] Resultado almacenado en {pathOutput} \n')
        main()

    else:
        print("\nOpcion no valida... Intente de nuevo otra vez >>\n")
        #main()


if __name__ == "__main__":

    try:
       main()

    except KeyboardInterrupt: 
        print("\n Ha terminado inesperadamente :(")
        print("\n[**] Finalizando el escaneo.. Gracias por usar la herramienta \n")
        time.sleep(2)
        sys.exit(0)