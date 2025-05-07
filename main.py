import win32gui
import win32ui
import win32con
import pygame
import sys
from PIL import Image
from pathlib import Path
pygame.init()
pygame.font.init()
THISFILE = Path(__file__).resolve().parent
fontDir = THISFILE / "DMSans-ExtraLightItalic.ttf"
noneDir = THISFILE / "None.png"
font = pygame.font.Font(str(fontDir), 20)
noneImg = pygame.image.load(str(noneDir))
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("DLL Icon")
clock = pygame.time.Clock()
drawX = 0
xg = 0
bgcolor = 40 #og is 0 / 20
bgchange = 1
moved = True
searchIdx = ""
searchPulseRed = 0
searchResultPulseGreen = 0
IconsList = []
def load_icon_surface(dll_path, index, size=256):
    icons, _ = win32gui.ExtractIconEx(dll_path, index, 1)
    if not icons:
        return pygame.image.load(str(noneDir))
    hicon = icons[0]

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    memdc = hdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(hdc, size, size)
    memdc.SelectObject(bmp)

    win32gui.DrawIconEx(memdc.GetSafeHdc(), 0, 0, hicon, size, size, 0, None, win32con.DI_NORMAL)

    img = Image.frombuffer("RGB", (size, size), bmp.GetBitmapBits(True), "raw", "BGRX", 0, 1)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

for i in range(400):
    Icon = load_icon_surface(r"C:\Windows\System32\imageres.dll", index=i, size=256)
    Icon = pygame.transform.smoothscale(Icon, (32, 32))
    IconsList.append(Icon)

def DrawBox(id,offsetX,Row):
    screen.blit(IconsList[id], (drawX+offsetX, 48+(100*Row)))
    if searchResultPulseGreen > 0 and id == int(searchIdx):
        screen.blit(font.render(str(id), True, (255-searchResultPulseGreen, 255, 255-searchResultPulseGreen)), (drawX+offsetX, 80+(100*Row)))
    else:screen.blit(font.render(str(id), True, (255, 255, 255)), (drawX+offsetX, 80+(100*Row)))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_LCTRL:
#                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
#                    xg = 5
#                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
#                    xg = -5
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                xg = 3
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                xg = -3
            if event.unicode.isnumeric() and len(searchIdx) < 3:
                searchIdx += event.unicode
                searchResultPulseGreen = 0
            if event.key == pygame.K_BACKSPACE:
                searchIdx = searchIdx[:-1]
                searchResultPulseGreen = 0
            if event.key == pygame.K_RETURN:
                if len(searchIdx) > 0:
                    if int(searchIdx) >= 400:
                        searchPulseRed = 255
                    else:
                        drawX = (int(searchIdx)%100 * -32)# + 32
                        searchResultPulseGreen = 255
                else:searchPulseRed = 255
        if event.type == pygame.KEYUP:
            xg = 0
    
    drawX += xg
    if drawX >= 32:
        drawX = 32
    if drawX <= -2808:
        drawX = -2808

    bgcolor += bgchange*0.25
    if bgcolor > 100:
        bgcolor = 100
        bgchange = -1
    if bgcolor < 40:
        bgcolor = 40
        bgchange = 1
    screen.fill((bgcolor, bgcolor, bgcolor))
    for h in range(4):
        for i in range(100):
            DrawBox(i+(100*h), drawX+(64*i), h)

    #pygame.draw.rect(screen, (25, 25, 25), (0, 0, 150, 75), 0)
    #pygame.draw.rect(screen, (0, 0, 0), (0, 0, 140, 65), 0)
    screen.blit(font.render("Search: "+str(searchIdx), True, (100+(searchPulseRed-100), 255-searchPulseRed, 100-(searchPulseRed/2.55))), (5, 5))
    searchPulseRed *= 0.94
    searchResultPulseGreen *= 0.985
    screen.blit(font.render("Imageres.dll Icon Gallery", True, (255, 255, 255)), ((font.size("Imageres.dll Icon Gallery")[0]/2)+200, 0))
    pygame.display.flip()
    #moved = False

    clock.tick(60)
