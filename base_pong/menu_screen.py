from base_pong.UtilityClasses import Button, GameObject, UtilityFunctions
from base_pong.menu import MenuBar, MenuItem
from base_pong.players import Player
from base_pong.ball import Ball
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from game_mechanics import GameRunner
game_menu = MenuBar(screen_height * .1)
game_menu.y_coordinate = screen_height - game_menu.height
paddle = Player()
paddle1 = Player()
paddle2 = Player()
paddle2.x_coordinate = screen_length - paddle2.length
ball = Ball()
ball.reset()

class StartButton(Button):
    game_is_started = False
    x_coordinate = 0
    y_coordinate = 0
    length = screen_length / 4
    height = screen_height / 4

    def render(self):
        UtilityFunctions.draw_font("START (SPACE)", pygame.font.Font('freesansbold.ttf', 50), 
                                   x_coordinate=self.x_coordinate, y_coordinate=self.y_coordinate, foreground=self.gray,
                                   background=self.green)
    
menus = [MenuItem("Paddle Dimensions", [Player().height, Player().length], ["height", "length"], 5),
         MenuItem("Paddle Power", [Player().power], ["power"], 1),
         MenuItem("Ball Dimensions", [Ball().height, Ball().length], ["height", "length"], 5),
         MenuItem("Ball Speed", [Ball().base_forwards_velocity], ["base_velocity"], VelocityCalculator.give_velocity(screen_length, 5))]
start_button = StartButton()

def add_menus():
    for menu in menus:
        game_menu.add(menu)

def change_properties():
    for menu in menus:
        object_modifying = paddle if menu.label.__contains__("Paddle") else ball
        object_modifying.__dict__[menu.properties_modifying[0]] = menu.values[0]
        if menu.properties_modifying.__len__() == 2:
            object_modifying.__dict__[menu.properties_modifying[1]] = menu.values[1]

    modified_properties = ["length", "height", "power"]
    paddle2.change_properties(modified_properties, paddle)
    paddle1.change_properties(modified_properties, paddle)
    paddle2.x_coordinate = screen_length - paddle2.length

def change_class_attributes():
    modified_properties = ["length", "height", "power"]
    GameRunner.player1.change_properties(modified_properties, paddle)
    GameRunner.player2.change_properties(modified_properties, paddle)
    GameRunner.ball = ball
def show_menu_screen():
    controlls = pygame.key.get_pressed()
    change_properties()
    ball.draw()
    paddle1.draw()
    paddle2.draw()
    game_menu.render()
    start_button.render()
    if start_button.got_clicked() or controlls[pygame.K_SPACE]:
        start_button.game_is_started = True
        change_class_attributes()
        

add_menus()

