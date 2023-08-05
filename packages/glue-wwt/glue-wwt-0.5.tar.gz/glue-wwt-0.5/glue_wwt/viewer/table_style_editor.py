from __future__ import absolute_import, division, print_function

import os

from qtpy import QtWidgets

from echo.qt import autoconnect_callbacks_to_qt
from glue.utils.qt import load_ui, fix_tab_widget_fontsize


class WWTTableStyleEditor(QtWidgets.QWidget):

    def __init__(self, layer_artist):

        super(WWTTableStyleEditor, self).__init__()

        self.ui = load_ui('table_style_editor.ui', self,
                          directory=os.path.dirname(__file__))

        fix_tab_widget_fontsize(self.ui.tab_widget)

        self.state = layer_artist.state

        self.layer_artist = layer_artist
        self.layer = layer_artist.layer

        connect_kwargs = {'value_alpha': dict(value_range=(0., 1.)),
                          'value_size_scaling': dict(value_range=(0.1, 10), log=True)}
        self._connect = autoconnect_callbacks_to_qt(self.state, self.ui, connect_kwargs)

        # Set initial values
        self._update_size_mode()
        self._update_color_mode()

        self.state.add_callback('color_mode', self._update_color_mode)
        self.state.add_callback('size_mode', self._update_size_mode)

        self.ui.button_center.clicked.connect(layer_artist.center)

        self._viewer_state = layer_artist._viewer_state
        self._viewer_state.add_callback('mode', self._on_mode_changed)

    def _on_mode_changed(self, *args):
        self.ui.button_center.setVisible(self._viewer_state.mode == 'Sky')

    def _update_size_mode(self, *args):

        if self.state.size_mode == "Fixed":
            self.ui.size_row_2.hide()
            self.ui.combosel_size_att.hide()
            self.ui.valuetext_size.show()
        else:
            self.ui.valuetext_size.hide()
            self.ui.combosel_size_att.show()
            self.ui.size_row_2.show()

    def _update_color_mode(self, *args):

        if self.state.color_mode == "Fixed":
            self.ui.color_row_2.hide()
            self.ui.color_row_3.hide()
            self.ui.combosel_cmap_att.hide()
            self.ui.spacer_color_label.show()
            self.ui.color_color.show()
        else:
            self.ui.color_color.hide()
            self.ui.combosel_cmap_att.show()
            self.ui.spacer_color_label.hide()
            self.ui.color_row_2.show()
            self.ui.color_row_3.show()
