
"""

Stylesheet taken from https://github.com/martinrotter/qt-material-stylesheet
Please leave a star to the creator for their amazing work!

"""


material_blue = """

        QWidget:window {					/* Borders around the code editor and debug window */
        border: 0px solid transparent;
        background-color: #070707;  /* Change this */
    }

    QToolTip {
        background-color: #80CBC4;
        color: black;
        padding: 5px;
        border-radius: 0;
        opacity: 200;
    }

    /* ==================== Dialog ==================== */
    QLabel {
        background: transparent;
        color: #CFD8DC;				/* Not sure about this one */
    }

    QDialog, QListView {
        background-color: #070707;
        color: #FFFFFF;
        outline: 0;
        border: 2px solid transparent;
    }

    QListView::item:hover {
        color: #AFBDC4;
        background: transparent;
    }


    QListView::item:selected {
        color: #ffffff;
        background: transparent;
    }

    /* === QTabBar === */
    QTabBar {
        background: transparent;
    }

    QTabWidget::pane {
        background: transparent;	/* Only at the very bottom of the tabs */
    }

    QTabBar::tab {
        background: transparent;
        border: 0px solid transparent;
        border-bottom: 2px solid transparent;
        color: #FFFFFF;
        padding-left: 10px;
        padding-right: 10px;
        padding-top: 3px;
        padding-bottom: 3px;
    }

    QTabBar::tab:hover {
        background-color: transparent;
        border: 0px solid transparent;
        border-bottom: 2px solid #80CBC4;
        color: #AFBDC4;
    }

    QTabBar::tab:selected {
        background-color: transparent;
        border: 0px solid transparent;
        border-top: none;
        border-bottom: 2px solid #80CBC4;
        color: #FFFFFF;
    }

    QStackedWidget {
        background: #070707;	/* This covers a bunch of things, I was thinking about making it transparent, */
                                /* but I would have to find all the other elements... but QTabWidget::pane may be it */
    }


    /* === QGroupBox === */
    QGroupBox {
        border: 1px solid transparent;
        margin-top: 1em;
    }

    QGroupBox::title {
        color: #80CBC4;
        subcontrol-origin: margin;
        left: 6px;
        padding: 0 3px 0 3px;
    }

    QComboBox {
        color: #FFFFFF;
        background-color: transparent;
        selection-background-color: transparent;
        outline: 0;
    }

    QComboBox QAbstractItemView
    {    
        selection-background-color: transparent;
        outline: 0;
    }

    /* === QCheckBox === */
    QCheckBox, QRadioButton {
        color: #AFBDC4;
    }

    QCheckBox::indicator::unchecked  {
        background-color: #070707;
        border: 1px solid #536D79;
    }

    QRadioButton::indicator::unchecked {
        background-color: #070707;
        border: 1px solid #536D79;
        border-radius: 4px;
    }

    QCheckBox::indicator::checked, QTreeView::indicator::checked {
        background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #070707);
        border: 1px solid #536D79;
    }

    QRadioButton::indicator::checked {
        background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #070707);
        border: 1px solid #536D79;
        border-radius: 4px;
    }

    QCheckBox::indicator:disabled, QRadioButton::indicator:disabled, QTreeView::indicator:disabled {
        background-color: #444444;			/* Not sure what this looks like */
    }

    QCheckBox::indicator::checked:disabled, QRadioButton::indicator::checked:disabled, QTreeView::indicator::checked:disabled {  
        background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #BBBBBB, stop:1 #444444); /* Not sure what this looks like */
    }

    QTreeView {
        background-color: transparent;
        color: #FFFFFF;
        outline: 0;
        border: 0;
    }

    QTreeView::item:hover {
        background-color: transparent;
        color: #AFBDC4;
    }

    QTreeView::item:selected {
        background-color: transparent;
        color: #FFFFFF;
    }

    QTreeView QHeaderView:section {
        background-color: #070707;
        color: #CFD8DC;
        border: 0;
    }

    QTreeView::indicator:checked {
        background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #80CBC4, stop:1 #070707);
        border: 1px solid #536D79;
        selection-background-color: transparent;
    }

    QTreeView::indicator:unchecked {			/* This and the one above style the checkbox in the Options -> Keyboard */
        background-color: #070707;				/* This is still a hover over in blue I can't get rid of */
        border: 1px solid #536D79;
        selection-background-color: transparent;
    }

    /*QTreeView QScrollBar {
        background-color: #070707
    }*/

    QTreeView::branch {
        /* Skip - applies to everything */
    }

    QTreeView::branch:has-siblings:adjoins-item {
        /* Skip - files */
    }

    QTreeView::branch:has-siblings:!adjoins-item {
        /* Skip - applies to almost all on the left side */
    }

    QTreeView::branch:closed:has-children:has-siblings {
        background: url('./images/rightarrowgray.png') center center no-repeat;
    }

    QTreeView::branch:has-children:!has-siblings:closed {
        background: url('./images/rightarrowgray.png') center center no-repeat;
    }

    QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        /* Skip - files */
    }

    QTreeView::branch:open:has-children:has-siblings {
        background: url('./images/downarrowgray.png') center center no-repeat;
    }

    QTreeView::branch:open:has-children:!has-siblings {
        background: url('./images/downarrowgray.png') center center no-repeat;
    }

    /* === QScrollBar:horizontal === */
    QScrollBar:horizontal {
        background: #070707;				/* Background where slider is not */
        height: 10px;
        margin: 0;
    }

    QScrollBar:vertical {
        background: #070707;				/* Background where slider is not */
        width: 10px;
        margin: 0;
    }

    QScrollBar::handle:horizontal {
        background: #37474F;					/* Slider color */
        min-width: 16px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical {
        background: #37474F;					/* Slider color */
        min-height: 16px;
        border-radius: 5px;
    }

    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;												/* Removes the dotted background */
    }

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {	/* Hides the slider arrows */
          border: none;
          background: none;
    }

    QPushButton {
        background-color: #2c2c2c;
        color: #FFFFFF;
        border: 1px solid transparent;
        padding-left: 5px;
        padding-right: 5px;
        padding-bottom: 2px;
        padding-top: 2px;
        font-family: Iosevka;
        font-size: 11;
    }

    QPushButton:hover {
        color: #AFBDC4;
    }

    QPushButton:pressed {
        color: #FFFFFF;
    }

    QLineEdit {
        background: transparent;
        border: 1px solid transparent;
        color: #FFFFFF;
    }

    QSpinBox {
        background: transparent;
        border: 1px solid transparent;
        color: #FFFFFF;
    }

    /*****************************************************************************
    Main Screen
    *****************************************************************************/
    QTreeView {
        background-color: #070707;
    }

    QMenu {
        background-color: #070707;		/* File Menu Background color */
        color: #FFFFFF;
    }

    QMenu::item:selected {
        color: #AFBDC4;
    }

    QMenu::item:pressed {
        color: #FFFFFF;
    }

    QMenu::separator {
        height: 1px;
        background: transparent;			/* Could change this to #FFFFFF and reduce the margin top and bottom to 1px */
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    /* === QMenuBar === */
    QMenuBar {
        background-color: #070707;
        color: #FFFFFF;
    }

    QMenuBar::item {
        background: transparent;
    }

    QMenuBar::item:disabled {
        color: gray;
    }

    QMenuBar::item:selected {
        color: #AFBDC4;
    }

    QMenuBar::item:pressed {
        color: #FFFFFF;
    }

    QToolBar {
        background: #070707;
        border: 1px solid transparent;
    }

    QToolBar:handle {
        background: transparent;
        border-left: 2px dotted #80CBC4;	/* Fix the 4 handle dots so it doesn't look crappy */
        color: transparent;
    }

    QToolBar::separator {
        border: 0;
    }

    /* === QToolButton === */
    QToolButton:hover, QToolButton:pressed {
        background-color: transparent;
    }

    QToolButton::menu-button {
        background: url('./images/downarrowgray.png') center center no-repeat;
        background-color: #070707;												/* This needs to be set to ensure the other brown arrows don't show */
    }

    QToolButton::menu-button:hover, QToolButton::menu-button:pressed {
        background-color: #070707;
    }

    QStatusBar {
        background-color: #070707;
    }

    QLabel {
        color: #FFFFFF;		/* Text at the bottom right corner of the screen */
    }

    QToolButton {	/* I don't like how the items depress */
        color: #FFFFFF;
    }

    QToolButton:hover, QToolButton:pressed, QToolButton:checked {
        background-color: #070707;
    }

    QToolButton:hover {
        color: #AFBDC4;

    }

    QToolButton:checked, QToolButton:pressed {
        color: #FFFFFF;
    }


    QToolButton {
        border: 1px solid transparent;
        margin: 1px;
    }

    QToolButton:hover {
        background-color: transparent;				/* I don't like how the down arrows in the top menu bar move down when clicked */
        border: 1px solid transparent;
    }

    QToolButton[popupMode="1"] { /* only for MenuButtonPopup */
        padding-right: 20px; /* make way for the popup button */
    }

    QToolButton::menu-button {
        border-left: 1px solid transparent;
        background: transparent;
        width: 16px;
    }

    QToolButton::menu-button:hover {
        border-left: 1px solid transparent;
        background: transparent;
        width: 16px;
    }

    QStatusBar::item {
        color: #FFFFFF;
        background-color: #070707;
    }

    QAbstractScrollArea  {	/* Borders around the code editor and debug window */
        border: 0;
    }

    /*****************************************************************************
    Play around with these settings
    *****************************************************************************/

    /* Force the dialog's buttons to follow the Windows guidelines. */
    QDialogButtonBox {
        button-layout: 0;
    }

    QTabWidget::tab-bar {
        left: 0px; /* Test this out on OS X, it will affect the tabs in the Options Dialog, on OS X they are centered */
    }

"""
