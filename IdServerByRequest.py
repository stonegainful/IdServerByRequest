#!/usr/bin/python
import requests
#Library
import csv
import os, sys, time
import re
import json

#Library
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw

from datetime import datetime
from pathlib import Path
from requests.exceptions import ConnectionError

PIXEL_ON = (255, 255, 255)  # PIL color to use for "on"
PIXEL_OFF = 0  # PIL color to use for "off"

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

    if (option == 2):
        urlFile = input('Ingrese el nombre y ubicacion del archivo de entrada:')
        f = open(urlFile, "r")
        urls = []
        for line in f:
            urls.append(line[0:len(line)-1])
        f.close()

        #for url in textfile:
        pathOutput = input("Ingrese el nombre del archivo de salida: ")
        filename, ext = os.path.splitext(pathOutput)
        if not ext:
            ext = '.csv'
        #Create a folder to save all generated files            
        pathOutput = filename + ext
        foldername = datetime.now().strftime("%Y%m%d")
        Path("./"+foldername).mkdir(parents=True, exist_ok=True)
        path_dest = os.path.join('./',foldername, pathOutput)

        headerCols = ("Nombre del Sitio","Server","X-Powered-By","X-AspNet-Version","Evidencia")
        with open(path_dest, 'w', newline='') as csvfile:
            textWriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            textWriter.writerow(headerCols)
            for url in urls:
                try:
                    response = requests.request("GET", url, verify=True)
                    headServer = response.headers.get('Server')
                    headPoweredBy = response.headers.get('X-Powered-By')
                    headAspVer = response.headers.get('X-AspNet-Version')

                    print('\nURL:', url)
                    if headServer:
                        version = re.findall('[0-9]+', headServer)
                        if len(version)>0:
                            print('Server:', headServer)
                    if headPoweredBy:
                        version = re.findall('[0-9]+', headPoweredBy)
                        if len(version)>0:
                            print('X-Powered-By:', headPoweredBy)
                    if headAspVer:
                        version = re.findall('[0-9]+', headAspVer)
                        if len(version)>0:
                            print('X-AspNet-Version:', headAspVer)

                    #Delete cookies for compact response
                    response.headers.pop('Set-Cookie', None)
                    now = datetime.now() # current date and time
                    tmp_filename = now.strftime("%Y%m%d_%H%M%S")+'.png'
                    image = text_image(response.headers, url)
                    tmp_path = os.path.join('./',foldername, tmp_filename)
                    image.save(tmp_path)

                    textWriter.writerow([url, headServer, headPoweredBy, headAspVer, tmp_filename])

                except ConnectionError:
                    print (f'Se omite la URL no se obtuvo respuesta')

        print('\n[**] Proceso finalizado \n')
        print(f'[**] Resultado almacenado en {path_dest} \n')
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
                version = re.findall('[0-9]+', headServer)
                if len(version)>0:
                    print('Server:', headServer)
            if headPoweredBy:
                version = re.findall('[0-9]+', headPoweredBy)
                if len(version)>0:
                    print('X-Powered-By:', headPoweredBy)
            if headAspVer:
                version = re.findall('[0-9]+', headAspVer)
                if len(version)>0:
                    print('X-AspNet-Version:', headAspVer)
                
            #Delete cookies for compact response
            response.headers.pop('Set-Cookie', None)
            now = datetime.now() # current date and time
            filename = now.strftime("%Y%m%d_%H%M%S")+'.png'
            image = text_image(response.headers, url)
            image.save(filename)

            headerCols = ("Nombre del Sitio","Server","X-Powered-By","X-AspNet-Version","Evidencia")
            with open(pathOutput, 'w', newline='') as csvfile:
                textWriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                textWriter.writerow(headerCols)
                textWriter.writerow([url, headServer, headPoweredBy, headAspVer, filename])

        except ConnectionError:
            print ('Ha fallado obtener respuesta de la URL {url}')

        print('\n[**] Proceso finalizado. \n')
        print(f'[**] Resultado almacenado en {pathOutput} \n')
        main()

    if (option == 3):
        print("\n[**] Finalizando el script... Gracias por usar la herramienta \n")

    else:
        print("\nOpcion no valida... Intente de nuevo otra vez >>\n")
        #main()


def text_image(plain_text, title='', font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    plain_text - the content of this file will be converted to an image
    title - the title placed on bottom of this image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'RGB'

    # choose a font (you can see more detail in my library on github)
    large_font = 20  # get better resolution with larger size
    font_path = font_path or 'courbd.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(plain_text, key=len)
    # max height is adjusted down because it's too large visually for spacing
    test_string = json.dumps(dict(plain_text))
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(plain_text)  # perfect or a little oversized
    width = int(round(max_width * 4))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # parse the file into lines
    text = json.dumps(dict(plain_text), indent=4, sort_keys=True)
    # margin of text line
    vertical_position = 5
    horizontal_position = 5

    draw.text((horizontal_position, vertical_position), text, fill=PIXEL_ON,font=font)

    text_w, text_h = draw.textsize(title, font)
    draw.text(((width - text_w) // 2, height - text_h), title, fill=PIXEL_ON,font=font)

    return image

if __name__ == "__main__":
    
    try:
       main()

    except KeyboardInterrupt: 
        print("\n Ha terminado inesperadamente :(")
        print("\n[**] Finalizando el escaneo.. Gracias por usar la herramienta \n")
        time.sleep(2)
        sys.exit(0)