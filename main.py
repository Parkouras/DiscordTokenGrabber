from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from tkinter import *
from threading import Thread
import pyperclip as clipboard
import chromedriver_autoinstaller


global usernametext
global passwordtext
global tokentext
global win

def mainwindow():

    global usernametext
    global passwordtext
    global tokentext
    global win
    

    win = Tk()
    win.title("Discord Token Grabber")
    win.geometry("440x200")
    Label(win, text="Email:", width=25).grid(row=0, column=0, padx=10, pady=10, sticky=S)
    Label(win, text="Password:", width=25).grid(row=1, column=0, padx=10, pady=10)
    usernametext = StringVar()
    passwordtext = StringVar()
    tokentext = StringVar()
    tokentext.set(" ")
    username = Entry(win, textvariable=usernametext)
    username.grid(row=0, column=1)
    password = Entry(win, textvariable=passwordtext, show="*")
    password.grid(row=1, column=1)
    Label(win, text="Status: ").grid(row=2, column=0, padx=10, pady=10)
    Button(win, text="Get Token", command=auth_user).grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    win.mainloop()
    

def auth_user():
    global usernametext
    global passwordtext
    global win

    chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    login = driver.get('https://discord.com/login')
    username_field = driver.find_element(By.NAME, "email")
    usernametext = usernametext.get()
    username_field.send_keys(usernametext)
    password_field = driver.find_element(By.NAME, "password")
    passwordtext = passwordtext.get()
    password_field.send_keys(passwordtext)
    loginbutton = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]")
    loginbutton.click()
    try:
        element = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div[1]/section/div[2]/div[1]/div[1]")))
        for request in driver.requests:
            if request.headers['authorization']:
                token = request.headers['authorization']
                clipboard.copy(token)
                tokentext = StringVar()
                tokentext.set(token)
                tokenfinal = tokentext.get()
                print(tokenfinal)
                Label(win, text="Copied to clipboard!").grid(row=2, column=1)
                win.update()
                break
    except:
        Label(win, text="Error").grid(row=2, column=1)



chromedriver_autoinstaller.install()
mainwindow()
