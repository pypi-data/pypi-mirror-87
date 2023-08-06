class AbzuColors:
    _abzu_colors = {'hot_magenta': '#FF1EC8',
                    'majorelle_blue': '#4646E6',
                    'spiro_disco_ball': '#0AB4FA',
                    'robin_egg_blue': '#00C8C8',
                    'guppie_green': '#00F082',
                    'golden_yellow': '#FFE10A',
                    'safety_orange': '#FF640A',
                    'dark_jungle_green': '#1E1E1E',
                    'black': '#1E1E1E',
                    'snow': '#FAFAFA',
                    'white': '#FAFAFA'}

    @staticmethod
    def get(color):
        return AbzuColors._abzu_colors.get(color, color)


class FeynTheme:
    primary = ('guppie_green', 'spiro_disco_ball')
    accent = ('hot_magenta', 'safety_orange')
    light = ('snow', 'dark_jungle_green')
    dark = ('dark_jungle_green', 'snow')
    neutral = ('robin_egg_blue')
    secondary = ('golden_yellow', 'majorelle_blue')

    font_sizes = {'small': 10,
                  'medium': 12,
                  'large': 14}

    def __init__(self, dark_mode=False):
        self.dark_mode = dark_mode

    def color(self, color):
        color = getattr(self, color, color)

        if type(color) == tuple:
            # dark mode support if you follow this pattern as second tuple string
            if self.dark_mode and len(color) == 2:
                color = color[1]
            else:
                color = color[0]

        # Just so we can support abzu color names
        return AbzuColors.get(color)

    def get_gradient(self):
        return [('low', self.color('accent')),
                ('mid', self.color('light')),
                ('high', self.color('primary'))]

    def font_size(self, size):
        # Just trust the user knows to feed the right thing in if not key
        return self.font_sizes.get(size, size)


class MonoTheme(FeynTheme):
    # Linear space of 12 colors between 0xFA and 0x1E (Don't use the darkest ones to improve contrast)
    # R = np.linspace(0xFA,0x1E, 12)
    # print(list(map(lambda r: f"#{int(r):2X}{int(r):2X}{int(r):2X}", R)))
    _grayscale = ['#FAFAFA', '#E6E6E6', '#D2D2D2', '#BEBEBE', '#AAAAAA', '#969696',
                  '#828282', '#6E6E6E', '#5A5A5A', '#464646', '#323232', '#1E1E1E']
    primary = (_grayscale[5], _grayscale[-6])
    accent = (_grayscale[1], _grayscale[-2])
    light = (_grayscale[0],  _grayscale[-1])
    dark = (_grayscale[-1], _grayscale[0])
    neutral = (_grayscale[4], _grayscale[-5])
    secondary = (_grayscale[6], _grayscale[-7])

    def get_gradient(self):
        # Override gradient
        return [('low', self.color('light')),
                ('mid', self.color('accent')),
                ('high', self.color('primary'))]


class Theme:
    _themes = {
        'default': FeynTheme(),
        'dark': FeynTheme(dark_mode=True),
        'mono': MonoTheme(),
        'mono_dark': MonoTheme(dark_mode=True)
    }
    _theme = 'default'

    @staticmethod
    def _get_current():
        """ Get the currently active theme

        Returns:
            FeynTheme -- A FeynTheme instance
        """
        return Theme._themes.get(Theme._theme, 'default')

    @staticmethod
    def color(color):
        """ Helper to get a color from the current theme

        Arguments:
            color {str} -- A color from the theme, either among:
            ['primary', 'secondary', 'accent', 'light', 'dark', 'neutral']
            a color among AbzuColors,
            Colors defined in the theme,
            Hex code (will pass through if not defined)

        Returns:
            [str] -- a string with a color hex code, i.e. '#FF1EC8'
        """
        return Theme._get_current().color(color)

    @staticmethod
    def gradient():
        """ Helper to get a three-step gradient from the current theme

        Returns:
            [Array(tuple(str, str))] -- An array of tuples [('low', <color>), ('mid', <color>), ('high', <color>)]
        """
        return Theme._get_current().get_gradient()

    @staticmethod
    def font_size(size):
        """ Helper to get a font size in pixels from a t-shirt size definition such as:
            ['small', 'medium', 'large']


        Arguments:
            size {str} -- A size in t-shirt sizing

        Returns:
            int -- font size in pixels corresponding to the provided t-shirt size
        """
        return Theme._get_current().font_size(size)

    @staticmethod
    def set_theme(theme='default'):
        """ Sets the theme for visual output in Feyn.

        Arguments:
            theme {str} -- Choose amongst: ['default', 'dark', 'mono', 'mono_dark']
        """
        # TODO: Should the matplotlib stylings also somehow be affected by theme selection?
        if theme not in Theme._themes:
            raise ValueError(f'Must select among available themes: {list(Theme._themes.keys())}')
        Theme._theme = theme
