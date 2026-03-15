import pygame
import sys
import random

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Deep Space Rescue Service - Live Map")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
GRAY = (120, 120, 120)
YELLOW = (255, 255, 0)
RED = (220, 40, 40)
GREEN = (40, 220, 140)
BLUE = (80, 180, 255)
PURPLE = (210, 100, 230)
ORANGE = (255, 170, 40)
NAVY = (12, 24, 68)
CYAN = (90, 220, 255)

# Fonts
title_font = pygame.font.SysFont("Courier", 42, bold=True)
label_font = pygame.font.SysFont("Courier", 22, bold=True)
small_font = pygame.font.SysFont("Courier", 18)
tiny_font = pygame.font.SysFont("Courier", 16)

# Stars
stars = []
for _ in range(100):
    stars.append([
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT),
        random.uniform(0.2, 0.8)
    ])


def update_and_draw_stars(surface):
    for star in stars:
        star[1] += star[2]
        if star[1] > SCREEN_HEIGHT:
            star[0] = random.randint(0, SCREEN_WIDTH)
            star[1] = 0
        pygame.draw.circle(surface, WHITE, (int(star[0]), int(star[1])), 1)


def draw_intro_ship(surface, x, y):
    pygame.draw.rect(surface, WHITE, (x, y, 32, 38))
    pygame.draw.rect(surface, BLUE, (x + 8, y, 16, 10))

    # red cross
    pygame.draw.rect(surface, RED, (x + 12, y + 14, 8, 14))
    pygame.draw.rect(surface, RED, (x + 9, y + 18, 14, 6))

    # wings
    pygame.draw.polygon(surface, WHITE, [(x - 14, y + 28), (x, y + 34), (x, y + 20)])
    pygame.draw.polygon(surface, WHITE, [(x + 46, y + 28), (x + 32, y + 34), (x + 32, y + 20)])

    # lights
    if pygame.time.get_ticks() % 600 < 300:
        pygame.draw.rect(surface, RED, (x + 4, y - 4, 6, 4))
        pygame.draw.rect(surface, BLUE, (x + 20, y - 4, 6, 4))
    else:
        pygame.draw.rect(surface, BLUE, (x + 4, y - 4, 6, 4))
        pygame.draw.rect(surface, RED, (x + 20, y - 4, 6, 4))

    # engines
    pygame.draw.rect(surface, ORANGE, (x + 6, y + 38, 6, 8))
    pygame.draw.rect(surface, ORANGE, (x + 20, y + 38, 6, 8))


def draw_intro_screen():
    ship_y = SCREEN_HEIGHT - 140
    ship_x = SCREEN_WIDTH // 2 - 16

    message = label_font.render("Deep Space Rescue Service", True, RED)
    sub_message = small_font.render("Press ESC to enter the DSRS Live Map", True, CYAN)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.fill(BLACK)
        update_and_draw_stars(screen)

        msg_rect = message.get_rect(center=(SCREEN_WIDTH // 2, 90))
        sub_rect = sub_message.get_rect(center=(SCREEN_WIDTH // 2, 130))
        screen.blit(message, msg_rect)
        screen.blit(sub_message, sub_rect)

        if ship_y > 140:
            ship_y -= 1.5

        draw_intro_ship(screen, ship_x, int(ship_y))

        pygame.display.flip()
        clock.tick(FPS)


def draw_node(surface, x, y, color, radius=18):
    pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(surface, WHITE, (x, y), radius // 3)


def draw_incident_marker(surface, x, y):
    blink_on = (pygame.time.get_ticks() // 350) % 2 == 0
    if blink_on:
        pygame.draw.circle(surface, RED, (x, y), 12)
        pygame.draw.circle(surface, YELLOW, (x, y), 5)


def draw_vessel_preview_panel(surface, selected_vessel):
    panel_rect = pygame.Rect(980, 500, 260, 220)
    pygame.draw.rect(surface, NAVY, panel_rect)
    pygame.draw.rect(surface, WHITE, panel_rect, 2)

    panel_x = panel_rect.x
    panel_y = panel_rect.y

    header = label_font.render("SELECTED VESSEL", True, WHITE)
    surface.blit(header, (panel_x + 12, panel_y + 18))

    if not selected_vessel:
        none_text = small_font.render("No vessel selected", True, GRAY)
        surface.blit(none_text, (panel_x + 12, panel_y + 55))
        return

    ship_x = panel_x + 12
    ship_y = panel_y + 105
    draw_intro_ship(surface, ship_x, ship_y)

    lines = [
        f"Name: {selected_vessel.name}",
        f"Status: {selected_vessel.status}",
        f"Critical: {selected_vessel.critical_capacity}",
        f"Priority: {selected_vessel.priority_capacity}",
        f"Stable: {selected_vessel.stable_capacity}",
        f"Range: {selected_vessel.max_range_full_ly} LY",
    ]

    y = panel_y + 50
    for line in lines:
        txt = tiny_font.render(line, True, WHITE)
        surface.blit(txt, (panel_x + 90, y))
        y += 20


def draw_legend(surface):
    legend_rect = pygame.Rect(0, SCREEN_HEIGHT - 70, SCREEN_WIDTH, 70)
    pygame.draw.rect(surface, NAVY, legend_rect)

    items = [
        ("Hub", YELLOW),
        ("Port", GREEN),
        ("Incident", RED),
        ("Vessel", WHITE),
    ]

    x = 30
    for label, color in items:
        pygame.draw.circle(surface, color, (x, SCREEN_HEIGHT - 35), 10)
        txt = small_font.render(label, True, WHITE)
        surface.blit(txt, (x + 20, SCREEN_HEIGHT - 46))
        x += 180

def draw_map_vessel(surface, x, y):
    x = int(x)
    y = int(y)

    pygame.draw.rect(surface, WHITE, (x, y, 20, 24))
    pygame.draw.rect(surface, BLUE, (x + 5, y, 10, 6))

    # red cross
    pygame.draw.rect(surface, RED, (x + 8, y + 8, 4, 10))
    pygame.draw.rect(surface, RED, (x + 6, y + 11, 8, 4))

    # wings
    pygame.draw.polygon(surface, WHITE, [(x - 8, y + 16), (x, y + 20), (x, y + 10)])
    pygame.draw.polygon(surface, WHITE, [(x + 28, y + 16), (x + 20, y + 20), (x + 20, y + 10)])


def build_port_positions(hub):
    # you can fine tune these later
    positions = {
        "Eastman Station": (180, 170),
        "The PITT": (700, 160),
        "Sacred Heart Station": (200, 530),
        "St. Eligius": (680, 500),
    }

    fallback_positions = [
        (250, 180),
        (750, 180),
        (240, 520),
        (720, 520),
        (450, 250),
        (450, 560),
    ]

    port_positions = {}
    for idx, port in enumerate(hub.ports):
        port_positions[port.name] = positions.get(
            port.name,
            fallback_positions[idx % len(fallback_positions)]
        )

    return port_positions


def build_destination_positions():
    return {
        "Titan Outpost": (735, 565),
        "Europa Research Colony": (760, 120),
        "Vallis Marineris Station": (840, 620),
        "Kreet": (120, 110),
    }

def point_in_circle(px, py, cx, cy, radius):
    dx = px - cx
    dy = py - cy
    return dx * dx + dy * dy <= radius * radius


def draw_map(hub, selected_vessel=None):
    port_positions = build_port_positions(hub)
    destination_positions = build_destination_positions()
    hub_pos = (520, 520)
    selected_destination = None
    running = True
    selected_port = None
    selected_incident = None
    map_message = ""
    mission_result_message = ""
    # STATE
    animation_active = False
    animation_vessel_x = hub_pos[0]
    animation_vessel_y = hub_pos[1]
    animation_target_x = hub_pos[0]
    animation_target_y = hub_pos[1]
    animation_speed = 4
    animation_phase = None  # None, "outbound", "returning"
    animation_pause_until = None
    selected_dropoff_port = None
    awaiting_port_assignment = False

    next_auto_incident_time = pygame.time.get_ticks() + 10000
    while running:
        current_time = pygame.time.get_ticks()
        # retrieves and processes all user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC pressed")
                    running = False

                elif event.key == pygame.K_a:
                    print("A pressed")
                    if selected_incident and not selected_incident.accepted:
                        accepted = hub.accept_incoming_incident()
                        if accepted:
                            selected_incident = accepted
                            map_message = f"Accepted incident {accepted.incident_id}"

                elif event.key == pygame.K_v:
                    print("V pressed")

                    if selected_incident and selected_incident.accepted:
                        ready_vessels = [v for v in hub.fleet if v.status == "READY"]

                        if ready_vessels:
                            selected_vessel = random.choice(ready_vessels)
                            selected_incident.assigned_vessel = selected_vessel
                            map_message = f"Selected vessel: {selected_vessel.name}"
                            print(
                                "Selected vessel after V:",
                                selected_vessel.name,
                                selected_vessel.status
                            )
                        else:
                            map_message = "No READY vessels available"

                elif event.key == pygame.K_l:
                    print("L pressed")

                    if selected_incident:
                        candidate_vessels = [v for v in hub.fleet if v.status == "READY"]

                        if selected_vessel and selected_vessel in candidate_vessels:
                            candidate_vessels.remove(selected_vessel)
                            candidate_vessels.insert(0, selected_vessel)

                        launch_result = None
                        launched_vessel = None

                        for vessel in candidate_vessels:
                            print("Trying vessel:", vessel.name, vessel.status)
                            launch_result = vessel.launch_rescue(selected_incident)

                            if launch_result["success"]:
                                launched_vessel = vessel
                                selected_vessel = vessel
                                selected_incident.assigned_vessel = vessel
                                break
                            else:
                                print("Launch failed with:", vessel.name, launch_result["message"])

                        if launch_result is None:
                            map_message = "No vessels available for launch"
                            continue

                        print(launch_result)
                        mission_result_message = launch_result["message"]

                        if launch_result["success"] and launched_vessel:
                            mission_result_message = launch_result["flight_log"]["flight_message"]

                            destination_name = selected_incident.destination.name
                            if destination_name in destination_positions:
                                animation_vessel_x = hub_pos[0]
                                animation_vessel_y = hub_pos[1]
                                animation_target_x, animation_target_y = destination_positions[destination_name]
                                animation_active = True
                                animation_phase = "outbound"
                                animation_pause_until = None

                            map_message = f"Launching {launched_vessel.name}"
                        else:
                            map_message = "Launch failed: no reachable/capable READY vessel"
                
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # clear simple click selections, but keep mission state alive
                selected_port = None
                selected_destination = None
                # extracts mouse position from event/corresponds with x/y axis
                mx, my = event.pos

                for port in hub.ports:
                    # if no value found in position use 200 as default
                    x, y = port_positions.get(port.name, (200, 200))
                    # radius of 18 used to calc hit detection
                    if point_in_circle(mx, my, x, y, 18):
                        selected_port = port
                        print(f"Clicked port: {selected_port.name}")

                        if awaiting_port_assignment and selected_incident and selected_vessel:
                            selected_dropoff_port = port
                            map_message = f"Assigned evacuees to {port.name}"
                            print(f"Assigned dropoff port: {selected_dropoff_port.name}")

                            px, py = port_positions[port.name]
                            animation_target_x = px
                            animation_target_y = py
                            animation_active = True
                            animation_phase = "to_port"
                            awaiting_port_assignment = False
                        break

                if not selected_port:
                    for name, (x, y) in destination_positions.items():
                        
                        if point_in_circle(mx, my, x, y, 10):
                            selected_destination = name
                            print(f"Clicked destination: {selected_destination}")
                            break

                if (
                    selected_destination
                    and hub.current_incoming_incident
                ):
                    print(
                        "Current incoming incident destination:",
                        hub.current_incoming_incident.destination.name
                    )
                    print("Selected destination:", selected_destination)

                    if hub.current_incoming_incident.destination.name == selected_destination:
                        selected_incident = hub.current_incoming_incident
                        print(f"Selected incident: {selected_incident.incident_id}")
                        map_message = f"Incident selected: {selected_incident.incident_id}"

        if hub.hub_state == "IDLE" and current_time >= next_auto_incident_time:
            incident = hub.activate_random_incoming_incident()
            if incident:
                print("Map-generated incident:", incident.summary())
                map_message = f"Incoming incident: {incident.incident_id}"
            next_auto_incident_time = current_time + 15000  # next chance in 15 sec

        screen.fill(BLACK)
        update_and_draw_stars(screen)

        title = title_font.render("DSRS LIVE MAP", True, WHITE)
        screen.blit(title, (180, 30))

        action_help = tiny_font.render(
            "Click incident → A accept → V vessel → L launch → Click port for evac",
            True,
            WHITE
        )
        pygame.draw.rect(screen, NAVY, (10, 105, 520, 25))
        screen.blit(action_help, (20, 115))

        # Hub
        draw_node(screen, hub_pos[0], hub_pos[1], YELLOW, radius=20)
        hub_label = label_font.render("MAIN HUB", True, WHITE)
        screen.blit(hub_label, (hub_pos[0] - 45, hub_pos[1] + 35))

        # Ports
        for port in hub.ports:
            x, y = port_positions.get(port.name, (200, 200))
            draw_node(screen, x, y, GREEN, radius=18)

            label = label_font.render(port.name, True, WHITE)
            screen.blit(label, (x - 60, y + 28))

            capacity_text = tiny_font.render(
                f"C:{port.available_capacity()['critical']} "
                f"P:{port.available_capacity()['priority']} "
                f"S:{port.available_capacity()['stable']}",
                True,
                WHITE
            )
            screen.blit(capacity_text, (x - 55, y + 52))

        # Destinations
        for name, (x, y) in destination_positions.items():
            pygame.draw.circle(screen, PURPLE, (x, y), 10)
            label = small_font.render(name, True, WHITE)
            screen.blit(label, (x + 15, y - 8))

        # Auto-generated incident visualization
    
        # INCIDENT BANNER VISUAL
        if hub.current_incoming_incident:
            incident_name = hub.current_incoming_incident.destination.name
            if incident_name in destination_positions:
                ix, iy = destination_positions[incident_name]
                draw_incident_marker(screen, ix, iy)

            banner = small_font.render(
                f"INCOMING INCIDENT AT: {incident_name} | {hub.current_incoming_incident.incident_type}",
                True,
                RED
            )
            screen.blit(banner, (20, 140))


        if animation_active:
            dx = animation_target_x - animation_vessel_x
            dy = animation_target_y - animation_vessel_y
            distance = (dx * dx + dy * dy) ** 0.5

            if distance <= animation_speed:
                animation_vessel_x = animation_target_x
                animation_vessel_y = animation_target_y

                if animation_phase == "outbound":
                    map_message = "Rescue vessel arrived. Click a port for evacuee dropoff."
                    animation_active = False
                    animation_phase = "awaiting_port"
                    awaiting_port_assignment = True

                elif animation_phase == "to_port":
                    map_message = f"Evacuees delivered to {selected_dropoff_port.name}"

                    if selected_incident and selected_dropoff_port:
                        assigned = {
                            "critical": min(
                                selected_incident.casualties.critical,
                                selected_dropoff_port.available_capacity()["critical"]
                            ),
                            "priority": min(
                                selected_incident.casualties.priority,
                                selected_dropoff_port.available_capacity()["priority"]
                            ),
                            "stable": min(
                                selected_incident.casualties.stable,
                                selected_dropoff_port.available_capacity()["stable"]
                            ),
                        }

                        selected_dropoff_port.current_load["critical"] += assigned["critical"]
                        selected_dropoff_port.current_load["priority"] += assigned["priority"]
                        selected_dropoff_port.current_load["stable"] += assigned["stable"]

                    if hub.current_incoming_incident:
                        hub.clear_incoming_incident()

                    animation_phase = "returning"
                    animation_target_x = hub_pos[0]
                    animation_target_y = hub_pos[1]

                elif animation_phase == "returning":
                    map_message = "Rescue vessel returned to hub"
                    animation_active = False
                    animation_phase = None

                    if selected_vessel:
                        selected_vessel.mark_ready()

                    selected_incident = None
                    selected_dropoff_port = None
                    selected_destination = None
                    selected_port = None
                    awaiting_port_assignment = False
            else:
                animation_vessel_x += (dx / distance) * animation_speed
                animation_vessel_y += (dy / distance) * animation_speed

            draw_map_vessel(screen, animation_vessel_x, animation_vessel_y)

        # PORT SELECTION DISPLAY
        if selected_port:
            available = selected_port.available_capacity()

            line1 = small_font.render(
                f"PORT: {selected_port.name}",
                True,
                CYAN
            )
            line2 = tiny_font.render(
                f"Available C:{available['critical']} P:{available['priority']} S:{available['stable']}",
                True,
                WHITE
            )

            screen.blit(line1, (20, 150))
            screen.blit(line2, (20, 175))


        # DESTINATION DISPLAY
        if selected_destination:
            line1 = small_font.render(
                f"DESTINATION: {selected_destination}",
                True,
                PURPLE
            )
            screen.blit(line1, (20, 205))

        # SELECTED INCIDENT DISPLAY
        if selected_incident:
            line1 = small_font.render(
                f"INCIDENT: {selected_incident.incident_id} {selected_incident.incident_type}",
                True,
                RED
            )
            line2 = tiny_font.render(
                f"Severity: {selected_incident.severity} | Total casualties: {selected_incident.total_casualties()}",
                True,
                WHITE
            )
            screen.blit(line1, (20, 235))
            screen.blit(line2, (20, 260))

        if awaiting_port_assignment:
            port_prompt = small_font.render(
                "SELECT DROP-OFF PORT FOR EVACUEES",
                True,
                CYAN
            )
            port_prompt_2 = tiny_font.render(
                "Click one of the green port nodes to continue evacuation.",
                True,
                WHITE
            )
            screen.blit(port_prompt, (20, 320))
            screen.blit(port_prompt_2, (20, 345))

        if map_message:
            msg = small_font.render(map_message, True, CYAN)
            screen.blit(msg, (900, 90))

        if mission_result_message:
            result = tiny_font.render(mission_result_message, True, WHITE)
            screen.blit(result, (900, 120))

        draw_vessel_preview_panel(screen, selected_vessel)
        draw_legend(screen)

        pygame.display.flip()
        clock.tick(FPS)