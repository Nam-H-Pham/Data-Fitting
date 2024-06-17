import pygame
import numpy

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fit data")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

dots = []

def fit_data(dots, degree=1):
    y = numpy.array([dot[1] for dot in dots])

    m = numpy.array([dot[0] for dot in dots])
    M = numpy.array([[m[i]**j for j in range(degree+1)] for i in range(len(m))])
    
    M_T = numpy.transpose(M)

    v = numpy.linalg.inv(M_T.dot(M)).dot(M_T).dot(y)

    return v

def correct_coords(x, y):
    return (x, height - y)

def draw_graph(v):
    if v is None:
        return
    degree = len(v) - 1
    x = numpy.linspace(0, width, 100)
    y = sum([v[i] * x**i for i in range(degree+1)])

    for i in range(len(x)):
        x[i], y[i] = correct_coords(x[i], y[i])

    for i in range(len(x)-1):
        pygame.draw.line(screen, black, (x[i], y[i]), (x[i+1], y[i+1]))
    
# Main loop
running = True
v = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # on mouse up 
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            dots.append(correct_coords(x, y))

            v = fit_data(dots, len(dots))
    
    screen.fill(white)
    
    for dot in dots:
        x, y = correct_coords(dot[0], dot[1])
        pygame.draw.circle(screen, black, (x, y), 5)


    draw_graph(v)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
