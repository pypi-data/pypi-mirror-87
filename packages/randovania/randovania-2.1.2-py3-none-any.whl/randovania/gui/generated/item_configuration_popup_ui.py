# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item_configuration_popup.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_ItemConfigurationPopup(object):
    def setupUi(self, ItemConfigurationPopup):
        if not ItemConfigurationPopup.objectName():
            ItemConfigurationPopup.setObjectName(u"ItemConfigurationPopup")
        ItemConfigurationPopup.resize(326, 197)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ItemConfigurationPopup.sizePolicy().hasHeightForWidth())
        ItemConfigurationPopup.setSizePolicy(sizePolicy)
        ItemConfigurationPopup.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(ItemConfigurationPopup)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.warning_label = QLabel(ItemConfigurationPopup)
        self.warning_label.setObjectName(u"warning_label")
        self.warning_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.warning_label)

        self.included_box = QGroupBox(ItemConfigurationPopup)
        self.included_box.setObjectName(u"included_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.included_box.sizePolicy().hasHeightForWidth())
        self.included_box.setSizePolicy(sizePolicy1)
        self.included_box.setCheckable(True)
        self.gridLayout = QGridLayout(self.included_box)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.shuffled_spinbox = QSpinBox(self.included_box)
        self.shuffled_spinbox.setObjectName(u"shuffled_spinbox")
        self.shuffled_spinbox.setMinimum(1)
        self.shuffled_spinbox.setMaximum(99)

        self.gridLayout.addWidget(self.shuffled_spinbox, 2, 1, 1, 1)

        self.shuffled_radio = QRadioButton(self.included_box)
        self.shuffled_radio.setObjectName(u"shuffled_radio")

        self.gridLayout.addWidget(self.shuffled_radio, 2, 0, 1, 1)

        self.starting_radio = QRadioButton(self.included_box)
        self.starting_radio.setObjectName(u"starting_radio")

        self.gridLayout.addWidget(self.starting_radio, 1, 0, 1, 1)

        self.vanilla_radio = QRadioButton(self.included_box)
        self.vanilla_radio.setObjectName(u"vanilla_radio")

        self.gridLayout.addWidget(self.vanilla_radio, 0, 0, 1, 1)

        self.provided_ammo_label = QLabel(self.included_box)
        self.provided_ammo_label.setObjectName(u"provided_ammo_label")
        self.provided_ammo_label.setWordWrap(True)

        self.gridLayout.addWidget(self.provided_ammo_label, 3, 0, 1, 1)

        self.provided_ammo_spinbox = QSpinBox(self.included_box)
        self.provided_ammo_spinbox.setObjectName(u"provided_ammo_spinbox")

        self.gridLayout.addWidget(self.provided_ammo_spinbox, 3, 1, 1, 1)


        self.verticalLayout.addWidget(self.included_box)

        self.button_box = QDialogButtonBox(ItemConfigurationPopup)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(ItemConfigurationPopup)

        QMetaObject.connectSlotsByName(ItemConfigurationPopup)
    # setupUi

    def retranslateUi(self, ItemConfigurationPopup):
        ItemConfigurationPopup.setWindowTitle(QCoreApplication.translate("ItemConfigurationPopup", u"Item Configuration", None))
        self.warning_label.setText(QCoreApplication.translate("ItemConfigurationPopup", u"Hidden warning!", None))
        self.included_box.setTitle(QCoreApplication.translate("ItemConfigurationPopup", u"Included", None))
        self.shuffled_radio.setText(QCoreApplication.translate("ItemConfigurationPopup", u"Shuffled", None))
        self.starting_radio.setText(QCoreApplication.translate("ItemConfigurationPopup", u"Starting Item", None))
        self.vanilla_radio.setText(QCoreApplication.translate("ItemConfigurationPopup", u"Vanilla", None))
#if QT_CONFIG(tooltip)
        self.provided_ammo_label.setToolTip(QCoreApplication.translate("ItemConfigurationPopup", u"<html><head/><body><p>When this item is collected, it also gives this amount of the given ammos.</p><p>This is included in the calculation of how much each pickup of this ammo gives.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.provided_ammo_label.setText(QCoreApplication.translate("ItemConfigurationPopup", u"<html><head/><body><p>Provided Ammo<br/>(XXXX and YYYY)</p></body></html>", None))
    # retranslateUi

