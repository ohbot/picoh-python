from ohbot import ohbot
from threading import Thread
import pygame

ohbot.reset()
pygame.mixer.init()
s = pygame.mixer.Sound("demoOpera.wav")

def doPlay():
	s.play()

def doLips():
	ohbot.wait(0.05)
	ohbot.move(4,5)
	ohbot.move(5,5)
	ohbot.wait(0.5861804837892748)
	ohbot.move(4,5)
	ohbot.move(5,5)
	ohbot.wait(0.07375042173905144)
	ohbot.move(4,9)
	ohbot.move(5,9)
	ohbot.wait(0.4978153467385975)
	ohbot.move(4,5)
	ohbot.move(5,5)
	ohbot.wait(0.07835982309774225)
	ohbot.move(4,9)
	ohbot.move(5,9)
	ohbot.wait(0.5992221766297934)
	ohbot.move(4,5)
	ohbot.move(5,5)
	ohbot.wait(0.19820425842370093)
	ohbot.move(4,9)
	ohbot.move(5,9)
	ohbot.wait(2.456810924182153)
	ohbot.move(4,5)
	ohbot.move(5,5)
	ohbot.wait(0.6414933000935639)

def doNod():
	ohbot.wait(0.5861804837892748)
	ohbot.wait(0.07375042173905144)
	ohbot.wait(0.4978153467385975)
	ohbot.wait(0.07835982309774225)
	ohbot.wait(0.5992221766297934)
	ohbot.wait(0.19820425842370093)
	ohbot.move(0,4)
	ohbot.wait(2.456810924182153)
	ohbot.wait(0.6414933000935639)

def doEmo():
	ohbot.wait(1.2543763625714643)
	ohbot.move(2,2,9)
	ohbot.wait(1.2543763625714643)
	ohbot.move(2,5,9)
	ohbot.wait(1.4261171080663775)
	ohbot.move(2,6,1)
	ohbot.wait(1.4261171080663775)
	ohbot.move(2,5,1)
threads = [Thread(target=doPlay), Thread(target=doLips), Thread(target=doNod), Thread(target=doEmo)]

for t in threads:
	t.start()

for t in threads:
	t.join()
ohbot.reset()
ohbot.wait(1)
ohbot.close()
