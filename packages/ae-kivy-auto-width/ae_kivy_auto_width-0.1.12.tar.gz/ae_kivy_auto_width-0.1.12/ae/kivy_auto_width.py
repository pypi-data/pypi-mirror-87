"""
automatic width for kivy widgets
================================

This ae portion is providing mix-in-classes for to automatically size and resize kivy widgets.


automatic font size iteration with animation
--------------------------------------------

Mix-in the :class:`AutoFontSizeBehavior` for to grow or shrink the font size automatically to fully fill the
width/height of a widget with its texture.

More details see in the documentation of the :class:`AutoFontSizeBehavior` class.


automatic ticker animation
--------------------------

For to automatic slide the texture of a widget if it is too big to be completely/fully displayed, like in a news
ticker, simply mix-in the :class:`SimpleAutoTickerBehavior`.

More details see in the documentation of the :class:`SimpleAutoTickerBehavior` class.


automatic container width with opening animation
------------------------------------------------

The class :class:`ContainerChildrenAutoWidthBehavior` determines the optimal width of a container widget
so that the text of any its label and button children widgets is fully visible/displayed.

The optimal container width is determined by increasing width of the container in iterations,
which are implemented through a kivy :class:`~kivy.animation.Animation`. As soon as the texts of all children
are fully displayed (or the maximum width is reached) the animation stops.

More details see in the documentation of the :class:`ContainerChildrenAutoWidthBehavior` class.


"""
from typing import Callable, Optional

from kivy.animation import Animation                                                        # type: ignore
from kivy.core.window import Window                                                         # type: ignore
from kivy.factory import Factory                                                            # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import NumericProperty                                                 # type: ignore # noqa: E0611
from kivy.uix.label import Label                                                            # type: ignore
from kivy.uix.widget import Widget                                                          # type: ignore

try:        # optional requirement
    from ae.gui_app import MAX_FONT_SIZE, MIN_FONT_SIZE                                     # type: ignore
except ImportError:                                                                         # pragma: no cover
    MIN_FONT_SIZE = 15
    MAX_FONT_SIZE = 69


__version__ = '0.1.12'


class AutoFontSizeBehavior:
    """ mix-in for to interpolate the optimal font size so that the texture is filling the full width of the widget.

    The desired spacing (left plus right) between the texture and the widget borders can be set via the
    :attr:`auto_font_text_spacing` property.

    For to disable the animation set the length of the :data:`auto_font_anim_duration` to zero or very short value.

    The minimum and maximum of the texture font size can be restricted by setting the attributes
    :attr:`auto_font_min_size` and :attr:`auto_font_max_size`.
    """
    # abstracts
    bind: Callable
    font_size: float
    texture_size: tuple
    texture_update: Callable
    width: float
    height: float

    # public attributes
    auto_font_anim_duration: float = NumericProperty(0.9)
    """ duration of the font size grow/shrink animation in seconds.

    :attr:`auto_font_anim_duration` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.9 seconds.
    """

    auto_font_max_size: float = NumericProperty(MAX_FONT_SIZE)
    """ maximum font size.

    :attr:`auto_font_max_size` is a :class:`~kivy.properties.NumericProperty` and
    defaults to :data:`~ae.gui_app.MAX_FONT_SIZE`.
    """

    auto_font_min_size: float = NumericProperty(MIN_FONT_SIZE)
    """ minimum font size.

    :attr:`auto_font_min_size` is a :class:`~kivy.properties.NumericProperty` and
    defaults to :data:`~ae.gui_app.MIN_FONT_SIZE`.
    """

    auto_font_text_spacing: float = NumericProperty('18sp')
    """ horizontal padding between widget and texture width in pixels.

    :attr:`auto_font_text_spacing` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 18sp.
    """

    # internal attributes
    _font_size_anim: Optional[Animation] = None
    _font_anim_mode: int = 0
    _last_font_size: float = 0.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text=self._start_font_anim)
        self.bind(width=self._start_font_anim)
        self.bind(height=self._start_font_anim)

    def _font_size_adjustable(self):
        """ check if font size need/has to be adjustable. """
        if self.texture_size[0] + self.auto_font_text_spacing < self.width \
                and self.texture_size[1] + self.auto_font_text_spacing / 1.8 < self.height \
                and self.font_size < min(self.auto_font_max_size, self.height):
            return 1
        if (self.texture_size[0] + self.auto_font_text_spacing > self.width
            or self.texture_size[1] + self.auto_font_text_spacing / 1.8 > self.height) \
                and self.font_size > self.auto_font_min_size:
            return -1
        return 0

    def _start_font_anim(self, *_args):
        """ delayed anim check """
        if getattr(self, '_ticker_text_updating', False):
            return                  # ignore when SimpleAutoTickerBehaviour is shortening text

        self._stop_font_anim()      # stop just running animation (obsoleted by this new text/size change)
        self.texture_update()
        if not self.texture_size[0]:
            return

        self._font_anim_mode = self._font_size_adjustable()
        if not self._font_anim_mode:
            return                  # font size not adjustable

        reach_size = min(self.auto_font_max_size, self.height) if self._font_anim_mode == 1 else self.auto_font_min_size
        self._font_size_anim = Animation(font_size=reach_size, t='out_quad', d=self.auto_font_anim_duration)
        self._font_size_anim.bind(on_progress=self._font_size_progress)
        self._font_size_anim.start(self)

    def _stop_font_anim(self):
        if self._font_size_anim:
            self._font_size_anim.stop(self)
            self._font_size_anim = None
        self._font_anim_mode = 0

    def _font_size_progress(self, _anim: Animation, _self: Widget, _progress: float):
        """ animation on_progress event handler. """
        if self._font_anim_mode and self._font_anim_mode != self._font_size_adjustable():
            self._stop_font_anim()
            if self._last_font_size and not self.auto_font_min_size <= self.font_size <= self.auto_font_max_size:
                self.font_size = self._last_font_size   # correct to last value of out of allowed min/max range
        self._last_font_size = min(max(self.auto_font_min_size, self.font_size), self.auto_font_max_size)


Factory.register('AutoFontSizeBehavior', cls=AutoFontSizeBehavior)


class ContainerChildrenAutoWidthBehavior:
    """ detect minimum width for the complete display of the textures of all children at opening with animation.

    This mix-in class can be added to any type of container or layout widget for to provide a consistent API
    with :meth:`.open` and :meth:`.close` methods, a :meth:`.on_complete_opened` event and a :attr:`.container`
    attribute.

    A `container` attribute will be automatically created for container classes without it.

    The animation starts when the :meth:`~ContainerChildrenAutoWidthBehavior.open` method get called.
    This call will be forwarded via `super()` to the container if it has an `open` method.

    At animation start the width of this container will be set to value of the :attr:`auto_width_start`
    attribute. Then the container width increases via the running animation until, either:

    * the container width is greater than the value of the :attr:`auto_width_minimum` attribute
      and the textures of all children are fully visible or

    * the container width reaches the app window width minus the window padding specified in the
      :attr:`auto_width_window_padding` attribute.

    The window width gets bound to the container width for to ensure proper displaying if
    the window width changes.

    :Events:
        `on_complete_opened`:
            Fired when the container width animation is finished or stopped because all children are fully visible.

    """
    container: Widget           #: widget to add the dynamic children to (provided by the widget to be mixed into)
    dismiss: Callable           #: optional method provided by the widget to be mixed into
    dispatch: Callable          #: event dispatch method, provided by the widget to be mixed into
    opacity: float              #: opacity of the widget to be mixed into
    parent: Widget              #: parent of this widget/container.
    width: float                #: width of the widget to be mixed into (mostly a parent of self.container)

    auto_width_anim_duration: float = NumericProperty(0.9)
    """ duration of the width animation in seconds.

    :attr:`auto_width_anim_duration` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.9 seconds.
    """

    auto_width_window_padding: float = NumericProperty('96sp')
    """ horizontal padding between the window and the container in pixels.

    :attr:`auto_width_window_padding` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 96sp.
    """

    auto_width_minimum: float = NumericProperty('369sp')
    """ minimum container width in pixels (before the width animation will be stopped).

    :attr:`auto_width_minimum` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 369sp.
    """

    auto_width_child_padding: float = NumericProperty('87sp')
    """ horizontal padding between child widget and child texture in pixels.

    :attr:`auto_width_child_padding` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 87sp.
    """

    auto_width_start: float = NumericProperty('3sp')
    """ container width in pixels at the start of the width animation.

    :attr:`auto_width_start` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 3sp.
    """

    # internal attributes
    _width_anim: Animation = None
    _complete_width: float = 0.0

    def __init__(self, **kwargs):
        # noinspection PyUnresolvedReferences
        self.register_event_type('on_complete_opened')  # pylint: disable=maybe-no-member
        super().__init__(**kwargs)

    def close(self, *_args, **_kwargs):
        """ close/dismiss container/layout (ae.gui_app popup handling compatibility for all GUI frameworks).

        :param _args:           unused argument (for to have compatible signature for DropDown/Popup/ModalView widgets).
        :param _kwargs:         unused argument (for to have compatible signature for DropDown/Popup/ModalView widgets).
        """
        try:
            # noinspection PyUnresolvedReferences
            super().close(*_args, **_kwargs)
        except AttributeError:
            try:
                self.dismiss(*_args, **_kwargs)
            except AttributeError:
                if self.parent and self in self.parent.children:
                    self.parent.remove_widget(self)

    def on_complete_opened(self):
        """ dispatch event when opening and width got determined. """

    def open(self, *_args, **kwargs):
        """ start optional open animation after calling open method if exists in inheriting container/layout widget.

        :param _args:           unused argument (for to have compatible signature for Popup/ModalView and DropDown
                                widgets passing the parent widget).
        :param kwargs:          extra arguments that are removed before to be passed to the inheriting open method:

                                * 'open_width_animation': `False` will disable the `width` animation (default=True).
        """
        anim_width = kwargs.pop('open_width_animation', True)

        if not hasattr(super(), 'container'):
            self.container = getattr(self, '_container', self)  # Popup has _container attribute, BoxLayout=self

        if callable(getattr(super(), 'open', None)):
            # noinspection PyUnresolvedReferences
            super().open(*_args, **kwargs)      # pylint: disable=maybe-no-member

        if anim_width:
            container_max_width = Window.width - self.auto_width_window_padding
            self._width_anim = Animation(opacity=1.0, width=container_max_width,
                                         t='in_out_sine', d=self.auto_width_anim_duration)
            self._width_anim.bind(on_progress=self._open_width_progress)
            self._width_anim.bind(on_complete=self._on_complete_opened)
            self.width = self.auto_width_start
            self._width_anim.start(self)
        else:
            self._win_width_bind()

    def reset_width_detection(self):
        """ call to reset the last detected minimum container width (e.g. if the children text got changed). """
        self._complete_width = 0.0

    # internal methods

    def _detect_complete_width(self) -> float:
        """ check clients textures until widest child texture got detected.

        :return:                0.0 until complete width got detected, then the last detected minimum container width.
        """
        if not self._complete_width:
            if all(chi.texture_size[0] + self.auto_width_child_padding < self.width
                   for chi in self.container.children if isinstance(chi, Label)):
                self._complete_width = self.width
        return self._complete_width

    def _on_complete_opened(self, *_args):
        """ open animation completion callback/event. """
        self.opacity = 1.0
        self._win_width_bind()
        self.dispatch('on_complete_opened')

    def _on_win_width(self, *_args):
        """ Window.width event handler. """
        self.width = min(max(self.auto_width_minimum, Window.width),
                         self._detect_complete_width() or Window.width - self.auto_width_window_padding)

    def _open_width_progress(self, _anim: Animation, _self: Widget, _progress: float):
        """ animation on_progress event handler. """
        if self.width > self.auto_width_minimum:
            if self._detect_complete_width():
                self._width_anim.stop(self)

    def _win_width_bind(self):
        """ bind :class:`~kivy.core.window.Window` width property to container width. """
        Window.bind(width=self._on_win_width)


Factory.register('ContainerChildrenAutoWidthBehavior', cls=ContainerChildrenAutoWidthBehavior)


class SimpleAutoTickerBehavior:
    """ mix-in class for to slide texture if too long to be displayed completely.

    If the `text` or `size` of the widget where this class get mixed in changes then this instance is first
    determining the number of characters that can be displayed completely in this widget. This is done with
    an kivy animation. The duration of this animation can be set via the property
    :attr:`auto_ticker_length_anim_duration`.

    For to adjust the padding space between the widget border and their texture width, the property
    :attr:`auto_ticker_text_spacing` can be changed accordingly.

    After determining the maximum number of characters that can be displayed and storing this value into
    the private attribute :attr:`_ticker_text_length` a second animation gets started for to slide/scroll
    the text. The duration of the second animation can be set via the property
    :attr:`auto_ticker_offset_anim_duration`.

    .. note::
        While the ticker animations are running the `text` property of the widget is only containing the
        visible part of the full initial text string. Use the private attribute :attr:`_ori_text` for
        to determine the full text string.

    """
    # abstracts
    bind: Callable
    text: str
    texture_size: tuple
    texture_update: Callable
    width: float

    # public attributes
    auto_ticker_length_anim_duration: float = NumericProperty(0.9)
    """ duration in seconds of the iteration animation for to determine the maximum text length.

    :attr:`auto_ticker_length_anim_duration` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.9 seconds.
    """

    auto_ticker_offset_anim_duration: float = NumericProperty(9.6)
    """ duration of the font size grow/shrink animation in seconds.

    :attr:`auto_ticker_length_anim_duration` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 9.6 seconds.
    """

    auto_ticker_text_spacing: float = NumericProperty('18sp')
    """ horizontal padding between widget and texture width in pixels.

    :attr:`auto_ticker_text_spacing` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 18sp.
    """

    # internal attributes
    _length_anim: Optional[Animation] = None
    _offset_anim: Optional[Animation] = None
    _ori_text: str = ""
    _ticker_text_offset: int = 0                #: current animated offset in the ticker text
    _ticker_text_length: int = 1                #: number of characters that are completely visible in widget
    _ticker_texture_width: float = 0.0          #: texture width of the complete text
    _ticker_text_updating: bool = False         #: flag to block restart of ticker on internal update of `text` property

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(height=self._start_length_anim)
        self.bind(text=self._text_changed)
        self.bind(width=self._start_length_anim)

    def _text_changed(self, *_args):
        """ called on change of label text. """
        # assert _args[1] == self.text
        if not self._ticker_text_updating:
            self._ori_text = self.text
            self._start_length_anim()

    def _start_length_anim(self, *_args):
        self.text = self._ori_text
        self._stop_offset_anim()
        self._stop_length_anim()

        self._ticker_texture_width = self.width - self.auto_ticker_text_spacing

        self._length_anim = Animation(_ticker_text_length=9, d=self.auto_ticker_length_anim_duration, t='out_quad')
        self._length_anim.bind(on_progress=self._ticker_length_progress)
        self._length_anim.start(self)

    def _start_offset_anim(self, *_args):
        self._offset_anim = Animation(_ticker_text_offset=0, d=self.auto_ticker_offset_anim_duration)
        self._offset_anim.bind(on_progress=self._ticker_offset_progress)
        self._offset_anim.start(self)

    def _stop_length_anim(self):
        if self._length_anim:
            self._length_anim.stop(self)
            self._length_anim = None
        self._ticker_text_length = len(self._ori_text)
        self._ticker_texture_width = 0.0

    def _stop_offset_anim(self):
        if self._offset_anim:
            self._offset_anim.stop(self)
            self._offset_anim = None
        self._ticker_text_offset = 0

    def _ticker_length_progress(self, _anim: Animation, _self: Widget, _progress: float):
        self.texture_update()
        if self.texture_size[0] < self._ticker_texture_width:
            self._ticker_text_length = len(self.text)
            self._ticker_text_offset = round(self._ticker_max_offset() / 2)
            if self._length_anim:
                self._length_anim.stop(self)
                self._length_anim = None
            self._start_offset_anim()
        else:
            self._ticker_text_update(self.text[1:-1])

    def _ticker_max_offset(self):
        return round(len(self._ori_text) - self._ticker_text_length)

    def _ticker_offset_progress(self, _anim: Animation, _self: Widget, progress: float):
        beg = int(self._ticker_text_offset)
        end = beg + int(self._ticker_text_length)
        self._ticker_text_update(self._ori_text[beg:end])
        if progress >= 1.0 and self._offset_anim:      # added `and self._offset_anim` for mypy
            self._offset_anim.stop(self)
            self._offset_anim = Animation(_ticker_text_offset=0 if beg else self._ticker_max_offset() + 1,
                                          d=self.auto_ticker_offset_anim_duration)
            self._offset_anim.bind(on_progress=self._ticker_offset_progress)
            self._offset_anim.start(self)

    def _ticker_text_update(self, text: str):
        self._ticker_text_updating = True
        self.text = text
        self._ticker_text_updating = False


Factory.register('SimpleAutoTickerBehavior', cls=SimpleAutoTickerBehavior)
