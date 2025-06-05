#import machine
from machine import Pin, RTC, Timer
import time

button1 = machine.Pin(16, machine.Pin.IN)
button2 = machine.Pin(20, machine.Pin.IN)
button3 = machine.Pin(21, machine.Pin.IN)
temp1	= machine.Pin(27, machine.Pin.IN)

c1 = machine.Pin(15, machine.Pin.OUT)
c2 = machine.Pin(17, machine.Pin.OUT)
c3 = machine.Pin(18, machine.Pin.OUT)
c4 = machine.Pin(19, machine.Pin.OUT)
led_pin  = machine.Pin(22, machine.Pin.OUT)

tim = Timer()  #hardware časovač pro blikání s LED "dvoutečkou" - po inicializaci nezatěžuje jádro.
def toggle_led(t):
    led_pin.value(not led_pin.value())
# Initialize the timer
tim.init(mode=Timer.PERIODIC, period=500, callback=toggle_led)

segment_pins = [
     machine.Pin(5, machine.Pin.OUT), #segment a
     machine.Pin(6, machine.Pin.OUT),  #b
     machine.Pin(14, machine.Pin.OUT), #c
     machine.Pin(12, machine.Pin.OUT), #d
     machine.Pin(7, machine.Pin.OUT), #e
     machine.Pin(0, machine.Pin.OUT), #f
     machine.Pin(4, machine.Pin.OUT), #n
     machine.Pin(11, machine.Pin.OUT), #j
     machine.Pin(2, machine.Pin.OUT), #g
     machine.Pin(9, machine.Pin.OUT), #l
     machine.Pin(1, machine.Pin.OUT), #p
     machine.Pin(3, machine.Pin.OUT), #h
     machine.Pin(8, machine.Pin.OUT), #m
     machine.Pin(10, machine.Pin.OUT), #k
     machine.Pin(13, machine.Pin.OUT), #dp
]


chars = {
     #     a  b  c  d  e  f  g1 g2 i  l  h  i  k  m  dp  #pouze pro zobrazení jednotlivých segmentů displeje - testování atd...
    "a":  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "b":  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "c":  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "d":  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "e":  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "f":  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "n":  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "j":  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    "g":  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    "l":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "p":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "h":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "m":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "k":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "dp": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    }

letters = {
    #     a  b  c  d  e  f  g1 g2 i  l  h  i  k  m  dp  #jednotlivé segmenty, na internetu můžeš najít jaké jsou jednotlivé segmenty - hledej "14 digit display segments" 
    " ": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # zde můžeš pridávat libovolně své znaky pro zobrazování
    "0": [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #ne všechny znaky jsou spávně nastavené, je potřeba doplnit
    "1": [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #bacha, funkce je case-sensitive -> pozor na mal8 a velká písmena
    "2": [1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], #"1" znamená, že daný segment svítí.
    "3": [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "4": [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "5": [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "6": [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "7": [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "8": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "9": [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "a": [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "b": [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "c": [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "d": [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "e": [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "f": [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "g": [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],	#ne všechny znaky jsou spávně nastavené, je potřeba doplnit
    "h": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "i": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "j": [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "k": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "l": [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "m": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "n": [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "o": [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "p": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "q": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "r": [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "s": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "t": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "u": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "v": [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "w": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "x": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "y": [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "z": [1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    ".": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    
    }


def seg_print(segment): #zobrazí pouze jeden segment (dobré pro testování atd, nikoli pro zobrazování dat) - možné vstupní parametry a,b,c,d,e,f,g,dp. použití např. seg_print(a). je potřeba zapnout digit pomocí zapsání "1" do nějakého z výstupu "c" , např. "c1.value(1)" pro spuštění 1. digitu displeje
    vals = chars[segment]
    for segment_number in range(0, 15):
        segment_pins[segment_number].value(vals[segment_number])


def seg_print_letter(x):#zobrazí znak ze setu "letters". jako argument bere čísla (int) i znaky (char, popř jeden znak string), je potřeba zapnout digit pomocí zapsání "1" do nějakého z výstupu "c" , např. "c1.value(1)" pro spuštění 1. digitu displeje
    x = str(x)  # Převod na string
    if x in letters:
        vals = letters[x]
        for segment_number in range(0, 15):
            segment_pins[segment_number].value(vals[segment_number])
    else:
        print(f"Neznámý znak: {x}")#pokud znak naní v setu "letters", vypíše do konzole.
        time.sleep_us(100000)

def show_number(number): #zobrazí na displeji číslo (int). zobrazí jen 4 poslední číslice, ostatní vyplní nulami. použití např. show_number(12)
    if isinstance(number, int):
        seg_print_letter((number%10000)//1000)  
        c1.value(1)
        time.sleep_us(100)
        c1.value(0)

        seg_print_letter((number%1000)//100)
        c2.value(1)
        time.sleep_us(100)
        c2.value(0)

        seg_print_letter((number%100)//10)
        c3.value(1)
        time.sleep_us(100)
        c3.value(0)

        seg_print_letter(number%10)
        c4.value(1)
        time.sleep_us(100)
        c4.value(0)
    else:
        print("špatný datový typ")
        time.sleep_us(100000)
    
def show_number1(number): #zobrazí na displeji číslo (int). zobrazí jen 4 poslední číslice, ostatní nezobrazí. použití např. show_number(12)
    if isinstance(number, int): #kontrola, zda je předaná hodnota opravdu typu int (celé číslo), jinak nezobrazí nic
        if (number//1000):
            seg_print_letter((number%10000)//1000)  
            c1.value(1)
            time.sleep_us(100)
            c1.value(0)

        if (number//100):
            seg_print_letter((number%1000)//100)
            c2.value(1)
            time.sleep_us(100)
            c2.value(0)

        if (number//10):
            seg_print_letter((number%100)//10)
            c3.value(1)
            time.sleep_us(100)
            c3.value(0)

        if (number):
            seg_print_letter(number%10)
            c4.value(1)
            time.sleep_us(100)
            c4.value(0)
    else:
        print("špatný datový typ")
        time.sleep_us(100000)

def set_time_epoch(sec):	#nastaví čas vnitřních RTC hodin na epoch time (čas v sekundách od roku 1970)
    # Convert epoch seconds to a tuple: (year, month, mday, hour, minute, second, weekday, yearday)
    dt = time.localtime(sec)
    # dt = (year, month, mday, hour, minute, second, weekday, yearday)

    # Set the RTC with the datetime tuple
    rtc = machine.RTC()
    rtc.datetime((dt[0], dt[1], dt[2], 0, dt[3], dt[4], dt[5], 0))
   
   
rtc.datetime((2020, 1, 21, 2, 10, 32, 36, 0)) #inicializace RTC hodin
while True: #nekonečná smyčka, zde piš program
    
    #příklady, co lze psát do této smyčky.
    
    #show_number1(89)	#napíše na displej číslo 89, zbytek digitů vypíše "0" - takže na dispeji bude "0089"
    #show_number1(1)	#napíše na displej číslo 1, zbytek digitů nebude svítit
    #show_string("zdar") #možná bude potřeba dodělat některé znaky v "letters"  
    #aby bylo vidět zobrazené data, je potřeba volat funkci hodně často (ve smyčce) - na displeji je vždy zobrazený jen jeden digit (multiplex). iluze toho, že jich svítí víc je zpusobena tím, že oči jsou "pomalé"
    
    #neboj se můj kód v téhle smyčce smazat a zkus naprogramovat něco svého...
    
    show_number1(time.localtime()[3]*100 +time.localtime()[4])
    
    i = 0
    while button1.value():
        i += 5	#pro postupne zrychlovani upravy casu
        if i > 20000:
            i = 20000
        time.sleep_us(500)
        set_time_epoch(time.time()+i//200)	# // je celociselne deleni
        show_number1(time.localtime()[3]*100 +time.localtime()[4])

    while (button2.value() or button3.value()):
        i += 1
        if i >> 5:
            i=0
            if button2.value():
                set_time_epoch(time.time()+1)
            if button3.value():
                set_time_epoch(time.time()-2)    
        x = 0        
        while (button2.value() and button3.value()):	#prekvapeni :)
            x += 1
            string = "jedovcela    "
            y = x >> 8
            show_string(string[:y])
            
        show_number1(time.localtime()[4]*100 +time.localtime()[5])    

