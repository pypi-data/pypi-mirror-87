import pyautogui

center = pyautogui.locateCenterOnScreen('chrome.png')
print(center)
pyautogui.click(center)


