import logging

from qtpy import QtWidgets, QtCore, QtGui

log = logging.getLogger(__name__)


class DoubleSlider(QtWidgets.QSlider):
    """A Slider that increments based on the `interval`

    Adapted from here: https://stackoverflow.com/a/61439114/6237583

    NOTE: This slider emits the index, not the underlying value which is likely
    what we want to emit
    """

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._min = 0
        self._max = 99
        self.interval = 1

        # Subclasses use this to connect to their _handle_changed, which
        # re-emits the underlying self.value() as appropriate type
        self.valueChanged.connect(self._handle_changed)
        self.sliderPressed.connect(self._handle_slider_pressed)

        self.style = QtWidgets.QApplication.style()
        self.opt = QtWidgets.QStyleOptionSlider()

    def _show_tooltip(self, val, x_offset, y_offset):
        """Displays the tooltip over the slider handle

        Kudos: https://stackoverflow.com/a/31658984/6237583
        """
        self.initStyleOption(self.opt)
        handle = self.style.subControlRect(
            self.style.CC_Slider, self.opt, self.style.SC_SliderHandle
        )

        pos_local = handle.topLeft() + QtCore.QPoint(x_offset, y_offset)
        pos_global = self.mapToGlobal(pos_local)
        QtWidgets.QToolTip.showText(pos_global, str(val))

    @QtCore.Slot()
    def _handle_slider_pressed(self):
        """Show tooltip when slider is pressed"""
        self._show_tooltip(str(self.value()), 3, -45)

    def setValue(self, value):
        index = round((value - self._min) / self.interval)
        return super().setValue(index)

    def value(self):
        return self.index * self.interval + self._min

    @property
    def index(self):
        return super().value()

    def setIndex(self, index):
        return super().setValue(index)

    def setMinimum(self, value):
        self._min = value
        self._range_adjusted()

    def minimum(self):
        return self._min

    def maximum(self):
        return self._max

    def setMaximum(self, value):
        self._max = value
        self._range_adjusted()

    def setInterval(self, value):
        # To avoid division by zero
        if not value:
            raise ValueError("Interval of zero specified")
        self.interval = value
        self._range_adjusted()

    def _range_adjusted(self):
        number_of_steps = int((self._max - self._min) / self.interval)
        super().setMaximum(number_of_steps)

    def wheelEvent(self, event):
        """Ignore wheel event so it gets passed to parent scroll area

        If not ignored, constantly changing sliders instead of scrolling
        """
        event.ignore()

    def get_interval_fmt_str(self):
        parts = str(self.interval).split(".")
        if len(parts) > 1:
            n_chars = len(parts[1])
        else:
            n_chars = 0

        return f"0.{n_chars}f"


class IntQSlider(DoubleSlider):
    """A QSlider that will emit integers"""

    value_changed = QtCore.Signal(int)

    @QtCore.Slot(int)
    def _handle_changed(self, val):
        """Re-Emit the underlying value and not the index"""
        real_val = int(self.value())
        self.setToolTip(str(real_val))
        self._show_tooltip(real_val, 3, -40)
        self.value_changed.emit(real_val)


class FloatQSlider(DoubleSlider):
    """A QSlider that will emit Floats"""

    value_changed = QtCore.Signal(float)

    @QtCore.Slot(int)
    def _handle_changed(self, val):
        """Re-Emit the underlying value and not the index"""
        real_val = float(self.value())
        fmt = self.get_interval_fmt_str()
        self.setToolTip(f"{real_val:{fmt}}")
        self._show_tooltip(f"{real_val:{fmt}}", 3, -40)
        self.value_changed.emit(float(self.value()))


class EditableQLabel(QtWidgets.QStackedWidget):
    """A QLabel that be edited by doubleClicking; emits valueChanged"""

    valueChanged = QtCore.Signal(str)

    def __init__(self, txt, alignment, validator=None, width=80, parent=None):
        super().__init__(parent=parent)
        self.setFixedWidth(width)
        self.setFixedHeight(20)
        self.edit = QtWidgets.QLineEdit()
        self.edit.setAlignment(alignment)
        if validator:
            self.edit.setValidator(validator)
        self.label = QtWidgets.QLabel(str(txt), alignment=alignment)
        self.label.installEventFilter(self)
        self.edit.installEventFilter(self)
        self.addWidget(self.label)
        self.addWidget(self.edit)

    def set_validator(self, validator):
        self.edit.setValidator(validator)

    def setText(self, text):
        self.label.setText(text)

    def set_width(self, width):
        self.setFixedWidth(width)

    def eventFilter(self, obj: QtWidgets.QWidget, event: QtCore.QEvent):
        """Handle events for QLabel or QLineEdit"""
        if obj == self.label:
            self._handle_label(event)
        elif obj == self.edit:
            self._handle_edit(event)

        return super().eventFilter(obj, event)

    def _handle_label(self, event: QtCore.QEvent):
        """Display QLineEdit if label is double clicked"""
        if event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
            self.edit.setText(self.label.text())
            self.setCurrentWidget(self.edit)
            self.edit.selectAll()
            self.edit.setFocus()

    def _handle_edit(self, event: QtCore.QEvent):
        """Handle closing edit box and redisplayin label"""
        if event.type() == QtCore.QEvent.Type.KeyPress:
            key = event.key()
            if key in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
                if not self.edit.hasAcceptableInput():
                    self.setCurrentWidget(self.label)
                    return
                self.label.setText(self.edit.text())
                self.setCurrentWidget(self.label)
                self.valueChanged.emit(self.label.text())
            if key == QtCore.Qt.Key.Key_Escape:
                self.setCurrentWidget(self.label)
        elif event.type() == QtCore.QEvent.FocusOut:
            self.setCurrentWidget(self.label)


class SliderContainer(QtWidgets.QWidget):
    """Adds min/max values under slider at either end

    Double clicking the endpoints turns them into a LineEdit and allows you to
    change the min/max.
    """

    def __init__(self, slider, editable_range, parent=None, show_editable_value=True):
        super().__init__(parent=parent)
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Slider
        self.slider = slider
        self.slider.setParent(self)
        _min, _max = slider.minimum(), slider.maximum()

        # Slider Text
        slider_validator = self._get_validator(self.slider, _min, _max)
        self.slider_text = EditableQLabel(
            str(self.slider.value()),
            width=45,
            validator=slider_validator,
            alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        main_layout.addWidget(self.slider_text)
        if not show_editable_value:
            self.slider_text.setVisible(False)


        # Min/Max Labels
        self.min_label, self.max_label = self._get_minmax_labels(
            self.slider, _min, _max, editable_range
        )

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(self.min_label)
        hbox.addWidget(self.max_label)
        hbox.setAlignment(self.min_label, QtCore.Qt.AlignLeft)
        hbox.setAlignment(self.max_label, QtCore.Qt.AlignRight)

        # Contains slider and min/max labeel container
        slider_vbox = QtWidgets.QVBoxLayout()
        slider_vbox.setContentsMargins(5, 0, 0, 0)
        slider_vbox.addWidget(self.slider)
        slider_vbox.addLayout(hbox)

        main_layout.addLayout(slider_vbox)

        # Change handlers for slider and its text box
        self.slider.valueChanged.connect(self._handle_slider_changed)
        self.slider_text.valueChanged.connect(self._handle_slider_text_input)

    @QtCore.Slot(str)
    def _handle_slider_text_input(self, val):
        """Set slider to specified value"""
        self.slider.setValue(float(val))

    @QtCore.Slot(float)
    @QtCore.Slot(int)
    def _handle_slider_changed(self, _):
        """Update slider text"""
        val = self.slider.value()
        if isinstance(val, float):
            fmt = self.slider.get_interval_fmt_str()
            real_val = f"{val:{fmt}}"
        else:
            real_val = str(val)
        self.slider_text.setText(real_val)

    def _get_minmax_labels(self, slider, bot, top, editable_range):
        """Return either standard QLabel or EditableQLabel w/ connected slots"""
        if not editable_range:
            return QtWidgets.QLabel(str(bot)), QtWidgets.QLabel(str(top))

        min_validator = self._get_validator(slider, -1000000000, top)
        max_validator = self._get_validator(slider, bot, 1000000000)

        min_label = EditableQLabel(
            bot, validator=min_validator, alignment=QtCore.Qt.AlignLeft
        )
        max_label = EditableQLabel(
            top, validator=max_validator, alignment=QtCore.Qt.AlignRight
        )

        min_label.valueChanged.connect(self._handle_min_changed)
        max_label.valueChanged.connect(self._handle_max_changed)

        return min_label, max_label

    def _update_slider_text_validator(self):
        """Sets the slider_text validator to current slider min/max"""
        _min = self.slider.minimum()
        _max = self.slider.maximum()
        validator = self._get_validator(self.slider, _min, _max)
        self.slider_text.set_validator(validator)

    @QtCore.Slot(str)
    def _handle_min_changed(self, value):
        """Update slider min value and limits of max_label validator"""
        if isinstance(self.slider, IntQSlider):
            value = int(value)
        elif isinstance(self.slider, FloatQSlider):
            value = float(value)
        validator = self._get_validator(self.slider, value, 1000000000)
        self.max_label.set_validator(validator)
        self.slider.setMinimum(value)
        self._update_slider_text_validator()

    @QtCore.Slot(str)
    def _handle_max_changed(self, value):
        """Update slider max value and limits of min_label validator"""
        if isinstance(self.slider, IntQSlider):
            value = int(value)
        elif isinstance(self.slider, FloatQSlider):
            value = float(value)
        validator = self._get_validator(self.slider, -1000000000, value)
        self.min_label.set_validator(validator)
        self.slider.setMaximum(value)
        self._update_slider_text_validator()

    def _get_validator(self, slider, bot, top):
        """Return proper validator based on slider type"""
        if isinstance(slider, IntQSlider):
            return QtGui.QIntValidator(bot, top)
        elif isinstance(slider, FloatQSlider):
            return QtGui.QDoubleValidator(bot, top, 20)


class SliderPair(SliderContainer):
    topChanged = QtCore.Signal((int,), (float,))
    botChanged = QtCore.Signal((int,), (float,))

    def __init__(self, top_slider, bot_slider, editable_range, parent=None):
        super().__init__(
            slider=top_slider, editable_range=editable_range, parent=parent,
            show_editable_value=False
        )
        self.layout().children()[0].insertWidget(1, bot_slider)
        top_slider.value_changed.connect(self._emit_top_changed)
        bot_slider.value_changed.connect(self._emit_bot_changed)

    @QtCore.Slot(int)
    @QtCore.Slot(float)
    def _emit_top_changed(self, value):
        self.topChanged.emit(value)

    @QtCore.Slot(int)
    @QtCore.Slot(float)
    def _emit_bot_changed(self, value):
        self.botChanged.emit(value)
