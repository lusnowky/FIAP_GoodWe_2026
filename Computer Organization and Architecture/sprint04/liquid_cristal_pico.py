import machine  # type: ignore[reportMissingImports]
import time

class GpioLcd:
    def __init__(self, rs_pin, enable_pin, d4_pin, d5_pin, d6_pin, d7_pin, num_lines=2, num_columns=16):
        self.rs = rs_pin
        self.en = enable_pin
        self.d4 = d4_pin
        self.d5 = d5_pin
        self.d6 = d6_pin
        self.d7 = d7_pin
        self.num_lines = num_lines
        self.num_columns = num_columns
        
        self.rs.init(machine.Pin.OUT)
        self.en.init(machine.Pin.OUT)
        self.d4.init(machine.Pin.OUT)
        self.d5.init(machine.Pin.OUT)
        self.d6.init(machine.Pin.OUT)
        self.d7.init(machine.Pin.OUT)
        
        self.rs.value(0)
        self.en.value(0)
        
        time.sleep_ms(20)
        self._write_nibble(0x30)
        time.sleep_ms(5)
        self._write_nibble(0x30)
        time.sleep_ms(1)
        self._write_nibble(0x30)
        self._write_nibble(0x20)
        
        self.cmd(0x28)
        self.cmd(0x0C)
        self.cmd(0x06)
        self.clear()

    def _pulse_enable(self):
        self.en.value(0)
        time.sleep_us(1)
        self.en.value(1)
        time.sleep_us(1)
        self.en.value(0)
        time.sleep_us(100)

    def _write_nibble(self, nibble):
        self.d4.value((nibble >> 4) & 0x01)
        self.d5.value((nibble >> 5) & 0x01)
        self.d6.value((nibble >> 6) & 0x01)
        self.d7.value((nibble >> 7) & 0x01)
        self._pulse_enable()

    def _write_byte(self, value):
        self._write_nibble(value)
        self._write_nibble(value << 4)

    def cmd(self, value):
        self.rs.value(0)
        self._write_byte(value)

    def putchar(self, char):
        self.rs.value(1)
        self._write_byte(ord(char))

    def putstr(self, string):
        for char in string:
            self.putchar(char)

    def clear(self):
        self.cmd(0x01)
        time.sleep_ms(2)

    def move_to(self, col, row):
        offsets = [0x00, 0x40]
        self.cmd(0x80 | (offsets[row] + col))

# Vincula o nome LiquidCrystalPico para satisfazer o import da Linha 3
LiquidCrystalPico = GpioLcd

# Injeta o GpioLcd no escopo global para satisfazer a Linha 29 do seu main.py
import builtins
builtins.GpioLcd = GpioLcd
