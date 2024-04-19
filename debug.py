import board
import neopixel
import time

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1
start_time = 0

class Debug:
    
    def status(status, id_color):
        pixel.fill(id_color)
        time.sleep(0.25)
        pixel.fill((0, 255, 0) if status else (255, 0, 0))
        time.sleep(0.25)
        pixel.fill((0, 0, 0))
    
    def timer_start():
        global start_time
        start_time = time.monotonic_ns()
    
    def timer_stop(task :str):
        global start_time
        ms_duration = round((time.monotonic_ns() - start_time) / 1e6, 1)
        print(f"{task} duration: {ms_duration} ms")