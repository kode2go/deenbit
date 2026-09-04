# --------------------------------
# DEENBIT STARTER APP
# --------------------------------
#
# Logo   = Smiley + Giggle
# A      = Thikr Counter
# B      = Temperature
# A + B  = Qibla Compass
# Clap   = Night Light
#
# --------------------------------


# --------------------------------
# VARIABLES
# --------------------------------

thikr_count = 0

# Approximate Qibla direction
QIBLA_DIRECTION = 23

# +/- 5 degrees tolerance
QIBLA_TOLERANCE = 5

night_light_on = False


# --------------------------------
# SMALL NUMBER DISPLAY
# Displays 0 - 99 on the 5x5 LEDs
# --------------------------------

def draw_digit(digit, x_offset):
    patterns = [
        ["11", "11", "10", "11", "11"],  # 0 - small break
        ["01", "11", "01", "01", "11"],  # 1
        ["11", "01", "11", "10", "11"],  # 2
        ["11", "01", "11", "01", "11"],  # 3
        ["10", "11", "01", "01", "01"],  # 4
        ["11", "10", "11", "01", "11"],  # 5
        ["11", "10", "11", "11", "11"],  # 6
        ["11", "01", "01", "01", "01"],  # 7
        ["11", "11", "11", "11", "11"],  # 8
        ["11", "11", "11", "01", "11"]   # 9
    ]

    pattern = patterns[digit]

    for y in range(5):
        for x in range(2):
            if pattern[y][x] == "1":
                led.plot(x + x_offset, y)


def show_small_number(number):
    basic.clear_screen()

    if number < 10:
        draw_digit(number, 2)

    else:
        tens = number // 10
        ones = number % 10

        draw_digit(tens, 0)
        draw_digit(ones, 3)


# --------------------------------
# SMART NUMBER DISPLAY
# Small display from 0 - 99
# Scroll normally from 100+
# --------------------------------

def show_deenbit_number(number):
    if number <= 99:
        show_small_number(number)
    else:
        basic.show_number(number)


# --------------------------------
# GIGGLE SOUND
# --------------------------------

def play_giggle():
    music.play(
        music.builtin_playable_sound_effect(
            soundExpression.giggle
        ),
        music.PlaybackMode.UNTIL_DONE
    )


# --------------------------------
# LOGO
# Smiley + giggle
# --------------------------------

def on_logo_pressed():
    play_giggle()
    basic.show_icon(IconNames.HAPPY)

input.on_logo_event(
    TouchButtonEvent.PRESSED,
    on_logo_pressed
)


# --------------------------------
# BUTTON A
# THIKR COUNTER
# --------------------------------

def on_button_pressed_a():
    global thikr_count

    thikr_count += 1

    show_deenbit_number(thikr_count)

input.on_button_pressed(
    Button.A,
    on_button_pressed_a
)


# --------------------------------
# BUTTON B
# TEMPERATURE
# --------------------------------

def on_button_pressed_b():
    temp = input.temperature()

    # Small numbers up to 99
    show_deenbit_number(temp)

    basic.pause(1000)

    basic.show_string("C")

input.on_button_pressed(
    Button.B,
    on_button_pressed_b
)


# --------------------------------
# A + B
# QIBLA COMPASS
# --------------------------------

def on_button_pressed_ab():

    # Qibla compass runs for about 10 seconds
    for i in range(50):

        heading = input.compass_heading()

        # Calculate shortest distance
        # between heading and Qibla direction

        difference = abs(
            heading - QIBLA_DIRECTION
        )

        if difference > 180:
            difference = 360 - difference


        # --------------------------------
        # FACING QIBLA
        # Within +/- 5 degrees
        # --------------------------------

        if difference <= QIBLA_TOLERANCE:

            # Show North/up arrow
            basic.show_arrow(
                ArrowNames.NORTH
            )

            music.play_tone(
                988,
                music.beat(
                    BeatFraction.SIXTEENTH
                )
            )

            basic.pause(300)


        # --------------------------------
        # NOT YET FACING QIBLA
        # Show current compass degrees
        # --------------------------------

        else:

            show_deenbit_number(
                heading
            )

            basic.pause(300)

    basic.clear_screen()


input.on_button_pressed(
    Button.AB,
    on_button_pressed_ab
)


# --------------------------------
# CLAP
# NIGHT LIGHT
# --------------------------------

def on_loud_sound():
    global night_light_on

    night_light_on = not night_light_on

    if night_light_on:

        basic.show_leds("""
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
        """)

    else:

        basic.clear_screen()


input.on_sound(
    DetectedSound.LOUD,
    on_loud_sound
)


# --------------------------------
# STARTUP
# --------------------------------

play_giggle()

basic.show_icon(
    IconNames.HAPPY
)
