import pprint


class Widget:
    __count = 0  # _Widget__count

    def __init__(self):
        super().__init__()
        self.__count = Widget.__count
        Widget.__count += 1

    @property
    def widget_id(self):
        return self.__count

    @staticmethod
    def total_widgets_created():
        return Widget.__count


class Button(Widget):
    def __init__(self):
        super().__init__()
        self.__count = 0  # _Button_count

    def click(self):
        self.__count += 1

    def total_clicks(self):
        return self.__count


def main():
    print(Widget.total_widgets_created(), "widgets")

    b = Button()

    print(Widget.total_widgets_created(), "widgets")

    print(b.total_clicks(), "clicks")
    b.click()
    b.click()

    print(b.total_clicks(), "clicks")
    print(Widget.total_widgets_created(), "widgets")

    pprint.pprint(b.__dict__)


if __name__ == '__main__':
    main()
