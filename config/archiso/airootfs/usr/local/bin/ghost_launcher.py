#!/usr/bin/env python3
"""
GhostyHub Micro Launcher
Scales from ASCII (8MB GPU) to Neon (High-End).
RAM Usage Target: < 120MB
"""

import os
import sys
import time
import subprocess
import curses
import shutil

# Detect Hardware / Mode
def detect_mode():
    # Check for simple RAM check
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'MemTotal' in line:
                    mem_kb = int(line.split()[1])
                    if mem_kb < 1048576: # < 1GB
                        return "ASCII"
    except:
        pass

    # Check GPU (mock check, if no DISPLAY, fallback to ASCII)
    if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        return "ASCII"

    return "NEON"

MODE = detect_mode()

class AsciiLauncher:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.items = ["Steam", "RetroArch", "Shutdown"]
        self.selected = 0

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        # Logo
        logo = [
            " G H O S T Y H U B ",
            " ───────────────── ",
            "  Boot. Dominate.  "
        ]

        start_y = h // 2 - 5
        for i, line in enumerate(logo):
            self.stdscr.addstr(start_y + i, (w - len(line)) // 2, line, curses.A_BOLD)

        # Menu
        menu_y = start_y + 5
        for idx, item in enumerate(self.items):
            x = (w - len(item)) // 2
            if idx == self.selected:
                self.stdscr.addstr(menu_y + idx, x - 2, f"> {item} <", curses.A_REVERSE)
            else:
                self.stdscr.addstr(menu_y + idx, x, item)

        self.stdscr.refresh()

    def run(self):
        while True:
            self.draw()
            key = self.stdscr.getch()

            if key == curses.KEY_UP and self.selected > 0:
                self.selected -= 1
            elif key == curses.KEY_DOWN and self.selected < len(self.items) - 1:
                self.selected += 1
            elif key == 10: # Enter
                self.launch(self.items[self.selected])

    def launch(self, item):
        self.stdscr.addstr(0, 0, f"Launching {item}...", curses.A_BOLD)
        self.stdscr.refresh()
        time.sleep(1)
        if item == "Shutdown":
            subprocess.run(["poweroff"])
        elif item == "Steam":
            # In ASCII mode, we might not be able to launch GUI steam easily without X
            # But let's assume we start xinit
            curses.endwin()
            subprocess.run(["startx", "/usr/bin/steam"])
        elif item == "RetroArch":
            curses.endwin()
            subprocess.run(["retroarch"])

def run_ascii():
    curses.wrapper(lambda stdscr: AsciiLauncher(stdscr).run())

def run_neon():
    # Lazy import to save RAM if in ASCII mode
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 40)
    small_font = pygame.font.SysFont("monospace", 24)

    items = ["Steam", "RetroArch", "Shutdown"]
    selected = 0

    running = True
    while running:
        screen.fill((10, 10, 10)) # Void Black

        # Glow Logo (Simulated)
        text = font.render("GHOSTYHUB", True, (0, 240, 255)) # Neon Cyan
        rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//3))
        screen.blit(text, rect)

        # Menu
        for idx, item in enumerate(items):
            color = (139, 92, 246) if idx == selected else (160, 160, 160) # Purple vs Gray
            if idx == selected:
                label = font.render(f"> {item} <", True, color)
            else:
                label = small_font.render(item, True, color)

            label_rect = label.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + idx * 50))
            screen.blit(label, label_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(items)
                elif event.key == pygame.K_RETURN:
                    if items[selected] == "Shutdown":
                        subprocess.run(["poweroff"])
                    elif items[selected] == "Steam":
                        subprocess.run(["steam"])
                    elif items[selected] == "RetroArch":
                        subprocess.run(["retroarch"])

        clock.tick(30) # 30 FPS Limit as requested

if __name__ == "__main__":
    if MODE == "ASCII":
        run_ascii()
    else:
        try:
            run_neon()
        except ImportError:
            # Fallback if pygame fails
            run_ascii()
