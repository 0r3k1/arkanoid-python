import pygame

ancho = 640
alto = 480

paleta = [(64, 78, 77), (255,255,255), (91,192,235), (253,231,76), (195, 65, 63)]
fondo = 0
pelota = 1
c1 = 2
c2 = 3
c3 = 4

class pixel(object):
	def __init__(self, x=0, y=0, w=10, h=10, c=(255, 255, 255)):
		self.r = pygame.Rect(x, y, w, h)
		self.color = c
		self.movx = 0
		self.movy = 0
		self.speed = 8

	def pinta(self, ventana):
		pygame.draw.rect(ventana, self.color, self.r)

	def mueve(self):
		self.r.move_ip(self.movx, self.movy)

class player(pixel):
	def __init__(self, x=0, y=0, w=10, h=10, c=(255, 255, 255)):
		pixel.__init__(self, x, y, w, h, c)
		self.color = paleta[pelota]
		self.juega = False
		self.vidas = 3

	def handle(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT: self.movx = self.speed
			if event.key == pygame.K_LEFT: self.movx = -self.speed
			if event.key == pygame.K_SPACE: self.juega = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				self.movx = 0

	def limites(self):
		if self.r.left < 0:
			self.r.left = 0
			self.movx = 0
		if self.r.right > ancho:
			self.r.right = ancho
			self.movx = 0

class boll(pixel):
	def __init__(self, x=0, y=0, w=10, h=10, c=(255, 255, 255)):
		pixel.__init__(self, x, y, w, h, c)
		self.speed = 3
		self.movx = 0
		self.movy = 0
		self.color = paleta[pelota]
		self.juega = False

	def inicio(self, player):
		if not player.juega:
			self.r.x = player.r.x + (player.r.width/2) - (self.r.width/2)
			self.r.y = player.r.y - (self.r.height)
			self.juega = True

	def empieza(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and self.juega:
				self.movx = self.speed
				self.movy = -self.speed
				self.juega = False

	def handle(self):
		if self.r.left < 0:
			self.movx = self.speed
		elif self.r.right > ancho:
			self.movx = -self.speed
		if self.r.top < 0:
			self.movy = self.speed
		elif self.r.bottom > alto:
			self.movy = -self.speed

	def colicion(self, rect):
		m = self.speed
		ret = self.r.colliderect(rect.r)
		if self.r.right > rect.r.left and self.r.left < rect.r.right-m and self.r.bottom > rect.r.top+m and self.r.top < rect.r.bottom-m:
			self.movx = -self.speed
			self.speed += .3
		elif self.r.left < rect.r.right and self.r.right > rect.r.left+m and self.r.bottom > rect.r.top+m and self.r.top < rect.r.bottom-m:
			self.movx = self.speed
			self.speed += .3
		elif self.r.bottom > rect.r.top and self.r.top < rect.r.bottom-m and self.r.right > rect.r.left+m and self.r.left < rect.r.right-m:
			self.movy = -self.speed
			self.speed += .3
		elif self.r.top < rect.r.bottom and self.r.bottom > rect.r.top+m and self.r.right > rect.r.left+m and self.r.left < rect.r.right-m:
			self.movy = self.speed
			self.speed += .3

		if self.speed > 8: self.speed = 8
		return ret

	def muere(self, player):
		if self.r.bottom > alto:
			player.r.x = ancho/2
			player.juega = False
			player.vidas -= 1
			self.juega = True
