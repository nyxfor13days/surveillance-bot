from pynput import keyboard
from gpiozero import Robot


class Controller:
    def __init__(self):
        self.robot = Robot(left=(4, 14), right=(17, 18))

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.robot.forward()
                print('forward')
            elif key.char == 's':
                self.robot.backward()
                print('backward')
            elif key.char == 'a':
                self.robot.left()
                print('left')
            elif key.char == 'd':
                self.robot.right()
                print('right')
            elif key.char == 'q':
                self.robot.stop()
                print('stop')

        except AttributeError:
            if key == 'w':
                self.robot.forward()
                print('forward')
            elif key == 's':
                self.robot.backward()
                print('backward')
            elif key == 'a':
                self.robot.left()
                print('left')
            elif key == 'd':
                self.robot.right()
                print('right')
            elif key == 'q':
                self.robot.stop()
                print('stop')

    def on_release(self, key):
        self.robot.stop()
        print('stop')

        if key == keyboard.Key.esc:
            return False

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def stop(self):
        self.robot.stop()
        self.robot.cleanup()


if __name__ == '__main__':
    controller = Controller()
    controller.run()
