#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, clases, random
from clases import ancho, alto, paleta, fondo, c1, c2, c3
pygame.init()



def main():
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Arkanoid")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 15, 5)
    beep = pygame.mixer.Sound("sound/Beep1.wav")

    player = clases.player(ancho/2, alto-20, 80, 10)
    pelota = clases.boll()
    ladrillo = []

    for i in range(0, 5):
        for j in range(0, 10):
            w = 50
            h = 15
            x = 70+(w*j)
            y = 10+(h*i)
            c = random.randint(0, 2)+2
            ladrillo.append(clases.pixel(x, y, w-1, h-1, paleta[c]))


    quit = False

    while not quit:
        vidas = font.render("Vidas: {0}".format(player.vidas), 1, paleta[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit = True
            player.handle(event)
            pelota.empieza(event)

        pelota.muere(player)
        pelota.handle()

        player.limites()

        pelota.colicion(player)
        for i in ladrillo:
            if pelota.colicion(i):
                beep.play()
                ladrillo.remove(i)


        player.mueve()
        pelota.mueve()

        pelota.inicio(player)

        ventana.fill(paleta[fondo])
        ventana.blit(vidas, (ancho-55, 10))
        player.pinta(ventana)
        pelota.pinta(ventana)
        for i in ladrillo:
            i.pinta(ventana)

        pygame.display.update()
        clock.tick(30)
        if len(ladrillo) == 0 or player.vidas <= 0: quit = True

    pygame.quit()

main()
