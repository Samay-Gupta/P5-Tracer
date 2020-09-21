"""
To Create a template p5.js file to trace an image
"""

import json
import pygame

TEMPLATE_FILE = 'files/template.js'
REFERENCE_FILE = 'files/image.png'
OUTPUT_JS_FILE = 'files/lab1.js'
CANVAS_SIZE = [400, 400]
SEGMENTS = ['Head', 'Body', 'Leg', 'Eye', 'Mouth', 'Nose', 'Ear', 'misc1', 'misc2', 'misc3'] 
SHOW_TRACER = True
TRACER_COLOR = (0, 255, 0)
TRACER_WIDTH = 2
GENERATE_JSON = True
OUTPUT_JSON_FILE = 'files/coordinates.json'
CLOSED_FIGURE = True
NEXT_KEY = ord('k')
FPS = 30

pygame.font.init()
screen = pygame.display.set_mode((CANVAS_SIZE[0], CANVAS_SIZE[1]+200))
clock = pygame.time.Clock()
pygame.display.set_caption('p5.js Tracer')
font = pygame.font.SysFont('Comic Sans MS', 32)
if isinstance(SEGMENTS, int):
    SEGMENTS = list(range(1, SEGMENTS+1))
if GENERATE_JSON:
    coordinates_dict = {}
reference_image = pygame.image.load(REFERENCE_FILE)
DRAW_CODE = '\n'
for segment_id in SEGMENTS:
    RUNNING = True
    coordinates = []
    draw_lines = ['\t// Code for segment {}'.format(segment_id), '\tbeginShape();']
    image_caption = font.render(segment_id, False, (0, 0, 0))
    while RUNNING:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == 5:
                if event.button == 1:
                    x_pos, y_pos = pygame.mouse.get_pos()
                    coordinates.append([x_pos, y_pos])
                    draw_lines.append('\tvertex({}, {});'.format(x_pos, y_pos))
            if event.type == 2:
                if event.key == NEXT_KEY:
                    RUNNING = False
        screen.blit(reference_image, (0, 0))
        if SHOW_TRACER:
            if len(coordinates) > 1:
                pygame.draw.lines(screen, TRACER_COLOR, CLOSED_FIGURE, coordinates, TRACER_WIDTH)
        screen.blit(image_caption, image_caption.get_rect(
            center=(CANVAS_SIZE[0]//2, CANVAS_SIZE[1]+100)))
        pygame.draw.rect(screen, (0, 0, 0), (0, CANVAS_SIZE[1], CANVAS_SIZE[0], 200), 2)
        pygame.display.flip()
        clock.tick(FPS)
    if GENERATE_JSON:
        coordinates_dict[segment_id] = coordinates
    draw_lines.append('\tendShape(' + ('CLOSE' if CLOSED_FIGURE else '') + ');')
    DRAW_CODE += '\n'.join(draw_lines) + '\n\n'
if GENERATE_JSON:
    json.dump(coordinates_dict, open(OUTPUT_JSON_FILE, 'w'))
with open(TEMPLATE_FILE) as file_obj:
    template = file_obj.read()
template = template.replace('/*X_WIDTH*/', str(CANVAS_SIZE[0]))
template = template.replace('/*Y_WIDTH*/', str(CANVAS_SIZE[1]))
template = template.replace('/* TODO */', DRAW_CODE)
with open(OUTPUT_JS_FILE, 'w') as file_obj:
    file_obj.write(template)
