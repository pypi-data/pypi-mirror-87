# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_item_pool.ui'
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


class Ui_PresetItemPool(object):
    def setupUi(self, PresetItemPool):
        if not PresetItemPool.objectName():
            PresetItemPool.setObjectName(u"PresetItemPool")
        PresetItemPool.resize(566, 450)
        PresetItemPool.setMaximumSize(QSize(16777215, 16777215))
        self.centralWidget = QWidget(PresetItemPool)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea(self.centralWidget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setLineWidth(0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 566, 450))
        self.gridLayout = QGridLayout(self.scroll_area_contents)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.item_alternative_box = QGroupBox(self.scroll_area_contents)
        self.item_alternative_box.setObjectName(u"item_alternative_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_alternative_box.sizePolicy().hasHeightForWidth())
        self.item_alternative_box.setSizePolicy(sizePolicy)
        self.item_alternative_layout = QVBoxLayout(self.item_alternative_box)
        self.item_alternative_layout.setSpacing(6)
        self.item_alternative_layout.setContentsMargins(11, 11, 11, 11)
        self.item_alternative_layout.setObjectName(u"item_alternative_layout")

        self.gridLayout.addWidget(self.item_alternative_box, 0, 0, 1, 2)

        self.item_pool_box = QGroupBox(self.scroll_area_contents)
        self.item_pool_box.setObjectName(u"item_pool_box")
        self.item_pool_box.setToolTipDuration(-1)
        self.item_pool_box.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.item_pool_box.setFlat(False)
        self.gridLayout_3 = QGridLayout(self.item_pool_box)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.ammo_box = QGroupBox(self.item_pool_box)
        self.ammo_box.setObjectName(u"ammo_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ammo_box.sizePolicy().hasHeightForWidth())
        self.ammo_box.setSizePolicy(sizePolicy1)
        self.ammo_box.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.ammo_layout = QVBoxLayout(self.ammo_box)
        self.ammo_layout.setSpacing(6)
        self.ammo_layout.setContentsMargins(11, 11, 11, 11)
        self.ammo_layout.setObjectName(u"ammo_layout")
        self.ammo_layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.gridLayout_3.addWidget(self.ammo_box, 1, 1, 1, 1)

        self.major_items_box = QGroupBox(self.item_pool_box)
        self.major_items_box.setObjectName(u"major_items_box")
        sizePolicy1.setHeightForWidth(self.major_items_box.sizePolicy().hasHeightForWidth())
        self.major_items_box.setSizePolicy(sizePolicy1)
        self.major_items_box.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.major_items_layout = QGridLayout(self.major_items_box)
        self.major_items_layout.setSpacing(6)
        self.major_items_layout.setContentsMargins(11, 11, 11, 11)
        self.major_items_layout.setObjectName(u"major_items_layout")
        self.major_items_layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.gridLayout_3.addWidget(self.major_items_box, 1, 0, 1, 1)

        self.item_pool_count_label = QLabel(self.item_pool_box)
        self.item_pool_count_label.setObjectName(u"item_pool_count_label")
        self.item_pool_count_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.item_pool_count_label, 0, 0, 1, 2)


        self.gridLayout.addWidget(self.item_pool_box, 3, 0, 1, 2)

        self.random_starting_box = QGroupBox(self.scroll_area_contents)
        self.random_starting_box.setObjectName(u"random_starting_box")
        self.gridLayout_2 = QGridLayout(self.random_starting_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.maximum_starting_label = QLabel(self.random_starting_box)
        self.maximum_starting_label.setObjectName(u"maximum_starting_label")

        self.gridLayout_2.addWidget(self.maximum_starting_label, 2, 0, 1, 1)

        self.minimum_starting_label = QLabel(self.random_starting_box)
        self.minimum_starting_label.setObjectName(u"minimum_starting_label")
        self.minimum_starting_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.minimum_starting_label, 1, 0, 1, 1)

        self.minimum_starting_spinbox = QSpinBox(self.random_starting_box)
        self.minimum_starting_spinbox.setObjectName(u"minimum_starting_spinbox")
        self.minimum_starting_spinbox.setMaximum(30)

        self.gridLayout_2.addWidget(self.minimum_starting_spinbox, 1, 1, 1, 1)

        self.random_starting_label = QLabel(self.random_starting_box)
        self.random_starting_label.setObjectName(u"random_starting_label")
        self.random_starting_label.setWordWrap(True)

        self.gridLayout_2.addWidget(self.random_starting_label, 0, 0, 1, 2)

        self.maximum_starting_spinbox = QSpinBox(self.random_starting_box)
        self.maximum_starting_spinbox.setObjectName(u"maximum_starting_spinbox")
        self.maximum_starting_spinbox.setMaximum(30)

        self.gridLayout_2.addWidget(self.maximum_starting_spinbox, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.random_starting_box, 2, 0, 1, 2)

        self.scroll_area.setWidget(self.scroll_area_contents)

        self.verticalLayout.addWidget(self.scroll_area)

        PresetItemPool.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetItemPool)

        QMetaObject.connectSlotsByName(PresetItemPool)
    # setupUi

    def retranslateUi(self, PresetItemPool):
        PresetItemPool.setWindowTitle(QCoreApplication.translate("PresetItemPool", u"Item Pool", None))
        self.item_alternative_box.setTitle(QCoreApplication.translate("PresetItemPool", u"Item Alternatives", None))
        self.item_pool_box.setTitle(QCoreApplication.translate("PresetItemPool", u"Item Pool", None))
        self.ammo_box.setTitle(QCoreApplication.translate("PresetItemPool", u"Ammo", None))
        self.major_items_box.setTitle(QCoreApplication.translate("PresetItemPool", u"Major Items", None))
#if QT_CONFIG(tooltip)
        self.item_pool_count_label.setToolTip(QCoreApplication.translate("PresetItemPool", u"If there are fewer than 119 items, the rest of the item locations will contain Energy Transfer Modules.", None))
#endif // QT_CONFIG(tooltip)
        self.item_pool_count_label.setText(QCoreApplication.translate("PresetItemPool", u"Items in pool: #/119", None))
        self.random_starting_box.setTitle(QCoreApplication.translate("PresetItemPool", u"Random Starting Items", None))
        self.maximum_starting_label.setText(QCoreApplication.translate("PresetItemPool", u"Start with at most this many items:", None))
        self.minimum_starting_label.setText(QCoreApplication.translate("PresetItemPool", u"Start with at least this many items:", None))
        self.random_starting_label.setText(QCoreApplication.translate("PresetItemPool", u"<html><head/><body><p>Randovania will add additional starting items if necessary to make the seed possible.<br/>The first value controls how many items are always added.<br/>The second value controls how many items the seed can have before it fails to generate.</p></body></html>", None))
    # retranslateUi

