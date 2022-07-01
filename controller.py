from pynput import keyboard
from gpiozero import Robot


class Controller:
    def __init__(self):
        self.robot = Robot(left=(4, 14), right=(17, 18))

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.robot.forward()
            elif key.char == 's':
                self.robot.backward()
            elif key.char == 'a':
                self.robot.left()
            elif key.char == 'd':
                self.robot.right()
            elif key.char == 'q':
                self.robot.stop()

        except AttributeError:
            if key == 'w':
                self.robot.forward()
            elif key == 's':
                self.robot.backward()
            elif key == 'a':
                self.robot.left()
            elif key == 'd':
                self.robot.right()
            elif key == 'q':
                self.robot.stop()

    def on_release(self, key):
        self.robot.stop()

        if key == keyboard.Key.esc:
            return False

    def run(self):
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def stop(self):
        self.robot.stop()
        self.robot.cleanup()


if __name__ == '__main__':
    controller = Controller()
    controller.run()
