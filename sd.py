import board
import sdcardio
import storage

def mount():
    spi = board.SPI()
    cs = board.D25     # Use the pin you wired to the breakout CS

    sdcard = sdcardio.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")