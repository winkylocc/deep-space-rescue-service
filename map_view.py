import math
import random
import sys
import pygame

from models import MainHub
from data.port_catalog import PORT_CATALOG
from data.vessel_catalog import VESSEL_CATALOG
from data.destination_catalog import DESTINATION_CATALOG

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 340
SCREEN_HEIGHT = 250
SCALING_FACTOR = 4

window_size = (SCREEN_WIDTH * SCALING_FACTOR, SCREEN_HEIGHT * SCALING_FACTOR)
screen = pygame.display.set_mode(window_size, pygame.SCALED)
pygame.display.set_caption("Deep Space Rescue Service - Live Map")
display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


clock = pygame.time.Clock()
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 170)
YELLOW = (255, 255, 0)
RED = (170, 0, 0)
GREEN = (0, 200, 120)
CYAN = (80, 220, 255)
MAGENTA = (220, 80, 220)
GRAY = (90, 90, 90)
DARK_BLUE = (15, 25, 60)
ORANGE = (255, 140, 0)

try:
    font = pygame.font.Font("font.ttf", 16)
    small_font = pygame.font.Font("font.ttf", 8)
except FileNotFoundError:
    font = pygame.font.SysFont("Courier", 16)
    small_font = pygame.font.SysFont("Courier", 8)

hub = MainHub(name="DSRS Main Hub")

for vessel in VESSEL_CATALOG.values():
    hub.register_vessel(vessel)

for port in PORT_CATALOG.values():
    hub.register_port(port)

HUB_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

PORT_POSITIONS = {
    "Eastman Station": (70, 60),
    "The PITT": (280, 55),
    "Sacred Heart Station": (80, 200),
    "St. Eligius": (270, 190),
}

DESTINATION_POSITIONS = {
    "Kreet": (40, 35),
    "Neebas": (120, 35),
    "Eridan II": (300, 90),
    "Muphrid IV": (300, 30),
    "Toliman II": (35, 120),
    "Jemison": (300, 215),
    "Codos": (35, 220),
}
resolved_port_positions = dict(PORT_POSITIONS)
resolved_destination_positions = dict(DESTINATION_POSITIONS)

def random_map_point():
    return (random.randint(25, SCREEN_WIDTH - 25), random.randint(25, SCREEN_HEIGHT - 35))

stars = []
for _ in range(60):
    stars.append([
        random.randint(0, SCREEN_WIDTH - 1),
        random.randint(0, SCREEN_HEIGHT - 1),
        random.uniform(0.1, 0.4)
    ])

ship_sprites = []
for vessel in hub.fleet:
    ship_sprites.append({
        "vessel": vessel,
        "pos": [HUB_POS[0], HUB_POS[1]],
        "target": HUB_POS,
        "speed": random.uniform(0.35, 0.8),
        "color": WHITE,
    })

status_message = "Press R to report an incident"
highlight_destination_names = set()
highlight_port_names = set()
active_destination_name = None


def scaled_mouse_pos():
    mx, my = pygame.mouse.get_pos()
    return mx // SCALING_FACTOR, my // SCALING_FACTOR


def was_clicked(mouse_pos, obj_pos, radius=8):
    mx, my = mouse_pos
    ox, oy = obj_pos
    return ((mx - ox) ** 2 + (my - oy) ** 2) <= radius ** 2


def update_starfield():
    for star in stars:
        star[1] += star[2]
        if star[1] > SCREEN_HEIGHT:
            star[0] = random.randint(0, SCREEN_WIDTH - 1)
            star[1] = 0
        display_surface.set_at((int(star[0]), int(star[1])), WHITE)


def draw_ship_icon(x, y, color=WHITE):
    pygame.draw.rect(display_surface, color, (x - 2, y - 2, 5, 5))
    pygame.draw.rect(display_surface, BLUE, (x - 1, y - 4, 3, 2))


def move_ship(ship):
    tx, ty = ship["target"]
    x, y = ship["pos"]

    dx = tx - x
    dy = ty - y
    dist = math.sqrt(dx * dx + dy * dy)

    if dist < 2:
        return

    ship["pos"][0] += ship["speed"] * dx / dist
    ship["pos"][1] += ship["speed"] * dy / dist


def quality_color(port):
    if port.quality_of_care == "HIGH":
        return GREEN
    if port.quality_of_care == "MEDIUM":
        return CYAN
    return ORANGE


def draw_hub():
    hx, hy = HUB_POS
    pygame.draw.circle(display_surface, YELLOW, (hx, hy), 8)
    pygame.draw.circle(display_surface, RED, (hx, hy), 3)
    label = small_font.render("MAIN HUB", True, WHITE)
    display_surface.blit(label, (hx - 18, hy + 12))


def draw_ports():
    for port in hub.ports:
        pos = get_port_position(port.name)
        color = quality_color(port)

        pygame.draw.line(display_surface, GRAY, HUB_POS, pos, 1)

        radius = 9 if port.name in highlight_port_names else 7
        border = WHITE if port.name in highlight_port_names else color

        pygame.draw.circle(display_surface, border, pos, radius)
        pygame.draw.circle(display_surface, color, pos, radius - 2)
        pygame.draw.circle(display_surface, WHITE, pos, 3)

        available = port.available_capacity()
        label = small_font.render(port.name, True, WHITE)
        cap = small_font.render(
            f"C:{available['critical']} P:{available['priority']} S:{available['stable']}",
            True,
            WHITE,
        )
        display_surface.blit(label, (pos[0] - 24, pos[1] + 10))
        display_surface.blit(cap, (pos[0] - 28, pos[1] + 18))


def draw_destinations():
    for name in DESTINATION_CATALOG.keys():
        pos = get_destination_position(name)

        if name == active_destination_name:
            color = RED
            radius = 7
        elif name in highlight_destination_names:
            color = YELLOW
            radius = 6
        else:
            color = MAGENTA
            radius = 4

        pygame.draw.circle(display_surface, color, pos, radius)
        label = small_font.render(name, True, WHITE)
        display_surface.blit(label, (pos[0] + 6, pos[1] - 4))


def draw_ships():
    for ship in ship_sprites:
        move_ship(ship)
        x = int(ship["pos"][0])
        y = int(ship["pos"][1])
        draw_ship_icon(x, y, ship["color"])


def draw_header():
    title = font.render("DSRS LIVE MAP", True, WHITE)
    display_surface.blit(title, (88, 8))
    subtitle = small_font.render(status_message, True, CYAN)
    display_surface.blit(subtitle, (10, 28))


def draw_legend():
    pygame.draw.rect(display_surface, DARK_BLUE, (5, SCREEN_HEIGHT - 28, SCREEN_WIDTH - 10, 23))
    items = [
        ("Hub", YELLOW),
        ("Port", GREEN),
        ("Incident", RED),
        ("Vessel", WHITE),
    ]

    x = 12
    for label, color in items:
        pygame.draw.circle(display_surface, color, (x, SCREEN_HEIGHT - 16), 4)
        text = small_font.render(label, True, WHITE)
        display_surface.blit(text, (x + 8, SCREEN_HEIGHT - 20))
        x += 65


def redraw():
    display_surface.fill(BLACK)
    update_starfield()
    draw_header()
    draw_destinations()
    draw_ports()
    draw_hub()
    draw_ships()
    draw_legend()
    screen.blit(pygame.transform.scale(display_surface, window_size), (0, 0))
    pygame.display.flip()


def send_ships_to_destination(destination_name):
    global active_destination_name
    active_destination_name = destination_name
    destination_pos = get_destination_position(destination_name)

    for i, ship in enumerate(ship_sprites):
        if i < 4:
            ship["target"] = destination_pos
        else:
            ship["target"] = HUB_POS


def prompt_incident_details_terminal():
    print("Enter a description of the incident")
    incident_description = input("> ").strip()

    print("Enter incident type")
    incident_type = input("> ").strip()

    while True:
        print("Enter severity (LOW/MEDIUM/HIGH)")
        severity = input("> ").strip().upper()
        if severity in ["LOW", "MEDIUM", "HIGH"]:
            break
        print("Invalid entry. Please enter LOW, MEDIUM, or HIGH.")

    while True:
        available = hub.get_total_available_capacity()
        print(f"\nNetwork capacity -> critical={available['critical']}, priority={available['priority']}, stable={available['stable']}")

        try:
            print("Number of critical casualties")
            critical = int(input("> ").strip())
            print("Number of priority casualties")
            priority = int(input("> ").strip())
            print("Number of stable casualties")
            stable = int(input("> ").strip())

            errors = []
            if critical < 0 or priority < 0 or stable < 0:
                errors.append("Casualty counts cannot be negative.")
            if critical > available["critical"]:
                errors.append(f"Critical exceeds available capacity ({available['critical']}).")
            if priority > available["priority"]:
                errors.append(f"Priority exceeds available capacity ({available['priority']}).")
            if stable > available["stable"]:
                errors.append(f"Stable exceeds available capacity ({available['stable']}).")

            if errors:
                print("\nUnable to record incident with those casualty counts:")
                for error in errors:
                    print(f"- {error}")
                continue

            return {
                "incident_description": incident_description,
                "incident_type": incident_type,
                "severity": severity,
                "critical": critical,
                "priority": priority,
                "stable": stable,
            }

        except ValueError:
            print("Invalid input. Please enter whole numbers.")


def select_destination_on_map():
    global highlight_destination_names, status_message

    highlight_destination_names = set(DESTINATION_CATALOG.keys())
    status_message = "Click a destination"
    print("\nClick a destination on the pygame map...")

    while True:
        redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                highlight_destination_names = set()
                status_message = "Destination selection cancelled"
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = scaled_mouse_pos()

                for name in DESTINATION_CATALOG.keys():
                    pos = get_destination_position(name)
                    if was_clicked(mouse, pos, 8):
                        highlight_destination_names = set()
                        status_message = f"Selected destination: {name}"
                        return DESTINATION_CATALOG[name]

        clock.tick(FPS)


def select_port_on_map(remaining, available_ports):
    global highlight_port_names, status_message

    highlight_port_names = {p.name for p in available_ports}
    status_message = (
        f"Click port | C:{remaining['critical']} "
        f"P:{remaining['priority']} S:{remaining['stable']}"
    )

    print(
        f"\nClick a port for placement -> "
        f"Critical: {remaining['critical']}, "
        f"Priority: {remaining['priority']}, "
        f"Stable: {remaining['stable']}"
    )

    while True:
        redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                highlight_port_names = set()
                status_message = "Port selection cancelled"
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = scaled_mouse_pos()

                for port in available_ports:
                    pos = PORT_POSITIONS.get(port.name, random_map_point())
                    if was_clicked(mouse, pos, 10):
                        highlight_port_names = set()
                        status_message = f"Selected port: {port.name}"
                        return port

        clock.tick(FPS)


def run_incident_workflow():
    global status_message

    details = prompt_incident_details_terminal()
    destination = select_destination_on_map()
    if destination is None:
        return

    incident = hub.create_incident(
        destination=destination,
        incident_type=details["incident_type"],
        severity=details["severity"],
        critical=details["critical"],
        priority=details["priority"],
        stable=details["stable"],
        incident_description=details["incident_description"],
    )

    print("\nIncident recorded:")
    print(incident.summary())

    send_ships_to_destination(destination.name)

    assignments = hub.assign_ports_for_casualties_with_selector(
        incident,
        select_port_on_map
    )

    print("\nUpdated port status:")
    for port, critical, priority, stable in assignments:
        available = port.available_capacity()
        print(
            f"{port.name} received "
            f"{critical} critical, {priority} priority, {stable} stable casualties."
        )
        print(
            f"{port.name} remaining capacity -> "
            f"critical={available['critical']}, "
            f"priority={available['priority']}, "
            f"stable={available['stable']}"
        )

    status_message = f"Incident complete at {destination.name}"

def get_port_position(port_name):
    if port_name not in resolved_port_positions:
        resolved_port_positions[port_name] = random_map_point()
    return resolved_port_positions[port_name]


def get_destination_position(destination_name):
    if destination_name not in resolved_destination_positions:
        resolved_destination_positions[destination_name] = random_map_point()
    return resolved_destination_positions[destination_name]

running = True
while running:
    redraw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                run_incident_workflow()

    clock.tick(FPS)

pygame.quit()
sys.exit()