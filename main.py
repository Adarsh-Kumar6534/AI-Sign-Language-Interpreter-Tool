import sys
import os
import networkx as nx
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect,
    QTabWidget, QLineEdit, QToolTip, QComboBox, QDialog, QGridLayout, QSpinBox
)
from PyQt6.QtGui import QFont, QColor, QBrush, QLinearGradient
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QSize
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import random
import requests
import json
from sklearn.cluster import KMeans
from datetime import datetime

class DeadlockDetectionAI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Powered Deadlock Detection System")
        self.setGeometry(100, 100, 1000, 650)
        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B3E5FC, stop:1 #4FC3F7);
            QToolTip { color: #0A1A44; background-color: #FFFFFF; border: 1px solid #0A1A44; padding: 5px; font-size: 16px; font-weight: bold; }
        """)
        self.num_processes = 5  # Default number of processes, adjustable up to 9
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        self.deadlock_graph_tab1 = nx.DiGraph()
        self.deadlock_graph_tab3 = nx.DiGraph()
        self.history = []
        try:
            if os.path.exists("deadlock_history.json"):
                with open("deadlock_history.json", "r") as f:
                    self.history = json.load(f)
        except json.JSONDecodeError:
            self.history = []
        self.current_graph_type = "3D Bar Plot"
        self.recovery_method = "Preemption"
        self.ai_suggested_method = None
        self.bankers_configured = False
        self.max_demand = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
        self.allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
        self.available = [3, 3, 3]
        print("Project Highlight: This tool utilizes a dynamic process table and AI-powered ML clustering to detect deadlock patterns. For patent-related inquiries or code use, please contact the owner at adarshsingh6534@gmail.com.")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.label = QLabel("AI-Powered Deadlock Detection System")
        self.label.setFont(QFont("Helvetica", 24, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #0A1A44; background: transparent; padding: 5px; border: 2px solid #0A1A44; border-radius: 5px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.label.setGraphicsEffect(shadow)
        self.label.setFixedHeight(50)
        main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #0A1A44; background: transparent; }
            QTabBar::tab { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #26A69A, stop:1 #FF6F61);
                           color: #0A1A44; padding: 5px; font-weight: bold; margin-right: 5px; }
            QTabBar::tab:selected { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF6F61, stop:1 #26A69A); }
        """)
        self.tabs.currentChanged.connect(self.animate_tab_transition)
        main_layout.addWidget(self.tabs)

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.setup_tab4()

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def animate_tab_transition(self, index):
        widget = self.tabs.widget(index)
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()

    def button_style(self, color):
        return f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {color}, stop:1 {self.darken_color(color)});
            color: #0A1A44; font-size: 16px; border-radius: 8px; padding: 8px; border: 2px solid {self.darken_color(color)};
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {self.lighten_color(color)}, stop:1 {color});
        }}
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {self.darken_color(color)}, stop:1 {color});
        }}
    """

    def darken_color(self, color):
        return f"{color[:-2]}80"

    def lighten_color(self, color):
        return f"{color[:-2]}FF"

    def configure_system_size(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configure System Size")
        dialog.setMinimumSize(300, 200)
        layout = QVBoxLayout()

        label = QLabel("Select Number of Processes (1-9):")
        label.setStyleSheet("color: #0A1A44; font-weight: bold;")
        layout.addWidget(label)

        combo = QComboBox()
        combo.addItems([str(i) for i in range(1, 10)])
        combo.setCurrentText(str(self.num_processes))
        combo.currentTextChanged.connect(lambda x: setattr(self, 'num_processes', int(x)))
        combo.setStyleSheet("""
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #26A69A, stop:1 #4682B4);
                color: #FFFFFF; font-size: 16px; border: 2px solid #0A1A44; padding: 5px; border-radius: 8px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { color: #0A1A44; background-color: #F5F5F5; selection-background-color: #26A69A; }
            QComboBox::hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4682B4, stop:1 #26A69A); }
        """)
        layout.addWidget(combo)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: #4CAF50; color: black; font-weight: bold; padding: 5px;")
        ok_button.clicked.connect(lambda: self.apply_system_size(dialog))
        layout.addWidget(ok_button)

        dialog.setLayout(layout)
        dialog.setStyleSheet("background-color: #E0F7FA; color: black;")
        dialog.exec()

    def apply_system_size(self, dialog):
        self.num_processes = int(self.num_processes)  # Use the updated value from combo
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        self.max_demand = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]] + [[0, 0, 0]] * (self.num_processes - 5)
        self.allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]] + [[0, 0, 0]] * (self.num_processes - 5)
        self.update_all_tabs()
        dialog.close()

    def update_all_tabs(self):
        self.table_tab1.setRowCount(self.num_processes)
        self.table_tab1.setColumnCount(self.num_processes)
        self.table_tab1.setHorizontalHeaderLabels(self.processes)
        self.table_tab1.setVerticalHeaderLabels(self.processes)
        self.update_table_tab1()

        self.table_tab3.setRowCount(self.num_processes)
        self.table_tab3.setColumnCount(self.num_processes)
        self.table_tab3.setHorizontalHeaderLabels(self.processes)
        self.table_tab3.setVerticalHeaderLabels(self.processes)
        self.update_table_tab3()

        self.update_chart_tab1()
        self.update_chart_tab2()
        self.update_chart_tab3()

    def setup_tab1(self):
        tab1 = QWidget()
        two_part_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.table_tab1 = QTableWidget(self.num_processes, self.num_processes)
        self.table_tab1.setHorizontalHeaderLabels(self.processes)
        self.table_tab1.setVerticalHeaderLabels(self.processes)
        self.table_tab1.setStyleSheet("QTableWidget { background-color: #FFFFFF; color: #0A1A44; font-size: 16px; border: 1px solid #0A1A44; } QHeaderView::section { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #26A69A, stop:1 #FF6F61); color: #0A1A44; font-weight: bold; }")
        self.table_tab1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_tab1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_tab1.setToolTip("Enter '1' to indicate a process dependency (e.g., P1 waits for P2)")
        left_layout.addWidget(self.table_tab1)

        button_layout = QHBoxLayout()
        self.detect_button = QPushButton("Detect Deadlock")
        self.detect_button.setStyleSheet(self.button_style("#26A69A"))
        self.detect_button.clicked.connect(self.detect_deadlock_tab1)
        self.detect_button.setToolTip("Analyze the table for deadlocks")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.detect_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.detect_button)

        self.fix_button = QPushButton("Fix Deadlock")
        self.fix_button.setStyleSheet(self.button_style("#FF6F61"))
        self.fix_button.clicked.connect(self.fix_deadlock_tab1)
        self.fix_button.setToolTip("Resolve detected deadlocks")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.fix_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.fix_button)

        self.bankers_button = QPushButton("Banker's")
        self.bankers_button.setStyleSheet(self.button_style("#4682B4"))
        self.bankers_button.clicked.connect(self.show_bankers_config)
        self.bankers_button.setToolTip("Configure Banker's Algorithm and analyze")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.bankers_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.bankers_button)

        self.export_graph_button = QPushButton("Export Graph")
        self.export_graph_button.setStyleSheet(self.button_style("#3CB371"))
        self.export_graph_button.clicked.connect(self.export_graph)
        self.export_graph_button.setToolTip("Save the bar chart as PNG")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.export_graph_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.export_graph_button)

        self.export_values_button = QPushButton("Export Values")
        self.export_values_button.setStyleSheet(self.button_style("#4682B4"))
        self.export_values_button.clicked.connect(self.export_values)
        self.export_values_button.setToolTip("Save the dependency table as CSV")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.export_values_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.export_values_button)

        self.process_size_button = QPushButton("Process Size")
        self.process_size_button.setStyleSheet(self.button_style("#26A69A"))
        self.process_size_button.clicked.connect(self.configure_system_size)
        self.process_size_button.setToolTip("Adjust the number of processes (1-9)")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.process_size_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.process_size_button)

        left_layout.addLayout(button_layout)
        two_part_layout.addLayout(left_layout, stretch=1)

        right_layout = QVBoxLayout()
        self.figure_tab1 = Figure(figsize=(4, 3))
        self.figure_tab1.patch.set_alpha(0)
        self.canvas_tab1 = FigureCanvas(self.figure_tab1)
        self.canvas_tab1.setStyleSheet("border: 1px solid #0A1A44; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B3E5FC, stop:1 #4FC3F7);")
        self.canvas_tab1.mpl_connect('button_press_event', self.on_bar_click)
        right_layout.addWidget(self.canvas_tab1, stretch=1)
        self.update_chart_tab1()

        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)
        self.message_log.setStyleSheet("QTextEdit { background-color: #F5E6E8; color: #0A1A44; font-family: 'Lilita', 'Helvetica', sans-serif; font-size: 16px; font-weight: bold; border: none; }")
        message_shadow = QGraphicsDropShadowEffect()
        message_shadow.setBlurRadius(15)
        message_shadow.setXOffset(0)
        message_shadow.setYOffset(0)
        message_shadow.setColor(QColor(255, 255, 255, 200))
        self.message_log.setGraphicsEffect(message_shadow)
        self.add_message("System initialized...")
        right_layout.addWidget(self.message_log, stretch=1)

        two_part_layout.addLayout(right_layout, stretch=1)
        tab1.setLayout(two_part_layout)
        self.tabs.addTab(tab1, "Deadlock Detection")

    def setup_tab2(self):
        tab2 = QWidget()
        layout = QVBoxLayout()
        self.figure_tab2 = Figure(figsize=(5, 4))
        self.figure_tab2.patch.set_alpha(0)
        self.canvas_tab2 = FigureCanvas(self.figure_tab2)
        self.canvas_tab2.setStyleSheet("border: 1px solid #0A1A44; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B3E5FC, stop:1 #4FC3F7);")
        self.canvas_tab2.setToolTip("Visualize dependency from Tab 1 table")
        layout.addWidget(self.canvas_tab2)

        button_layout = QHBoxLayout()
        self.choose_graph_button = QPushButton("Choose Graph")
        self.choose_graph_button.setStyleSheet(self.button_style("#26A69A"))
        self.choose_graph_button.clicked.connect(self.show_graph_selection)
        self.choose_graph_button.setToolTip("Select a graph type to visualize Tab 1 dependencies")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.choose_graph_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.choose_graph_button)

        self.rotate_h_button = QPushButton("Rotate Horizontally")
        self.rotate_h_button.setStyleSheet(self.button_style("#26A69A"))
        self.rotate_h_button.clicked.connect(lambda: self.rotate_view(1, 0))
        self.rotate_h_button.setToolTip("Rotate the graph horizontally")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.rotate_h_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.rotate_h_button)

        self.rotate_v_button = QPushButton("Rotate Vertically")
        self.rotate_v_button.setStyleSheet(self.button_style("#FF6F61"))
        self.rotate_v_button.clicked.connect(lambda: self.rotate_view(0, 1))
        self.rotate_v_button.setToolTip("Rotate the graph vertically")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.rotate_v_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.rotate_v_button)

        layout.addLayout(button_layout)
        self.update_chart_tab2()
        tab2.setLayout(layout)
        self.tabs.addTab(tab2, "Dependency Visualization")

    def setup_tab3(self):
        tab3 = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 60)

        left_layout = QVBoxLayout()
        self.table_tab3 = QTableWidget(self.num_processes, self.num_processes)
        self.table_tab3.setHorizontalHeaderLabels(self.processes)
        self.table_tab3.setVerticalHeaderLabels(self.processes)
        self.table_tab3.setStyleSheet("QTableWidget { background-color: #FFFFFF; color: #0A1A44; font-size: 16px; border: 1px solid #0A1A44; } QHeaderView::section { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #26A69A, stop:1 #FF6F61); color: #0A1A44; font-weight: bold; }")
        self.table_tab3.setToolTip("Watch dependencies change in real-time")
        left_layout.addWidget(self.table_tab3)

        button_layout1 = QHBoxLayout()
        self.start_sim_button = QPushButton("Start Simulation")
        self.start_sim_button.setStyleSheet(self.button_style("#26A69A"))
        self.start_sim_button.clicked.connect(self.start_simulation)
        self.start_sim_button.setToolTip("Begin simulation with selected or AI-recommended deadlock fix")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.start_sim_button.setGraphicsEffect(fix_shadow)
        button_layout1.addWidget(self.start_sim_button)

        self.stop_sim_button = QPushButton("Stop Simulation")
        self.stop_sim_button.setStyleSheet(self.button_style("#FF6F61"))
        self.stop_sim_button.clicked.connect(self.stop_simulation)
        self.stop_sim_button.setToolTip("Pause the simulation")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.stop_sim_button.setGraphicsEffect(fix_shadow)
        button_layout1.addWidget(self.stop_sim_button)
        left_layout.addLayout(button_layout1)

        button_layout2 = QHBoxLayout()
        self.clear_output_button = QPushButton("Clear Output")
        self.clear_output_button.setStyleSheet(self.button_style("#3CB371"))
        self.clear_output_button.clicked.connect(self.clear_sim_output)
        self.clear_output_button.setToolTip("Clear the simulation output")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.clear_output_button.setGraphicsEffect(fix_shadow)
        button_layout2.addWidget(self.clear_output_button)

        self.recovery_combo = QComboBox()
        self.recovery_combo.addItems(["Preemption", "Random Kill", "Resource Timeout"])
        self.recovery_combo.setCurrentText(self.recovery_method)
        self.recovery_combo.currentTextChanged.connect(lambda x: setattr(self, 'recovery_method', x))
        self.recovery_combo.setToolTip("Select deadlock recovery method")
        self.recovery_combo.setStyleSheet("""
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #26A69A, stop:1 #4682B4);
                color: #FFFFFF; font-size: 16px; border: 2px solid #0A1A44; padding: 5px; border-radius: 8px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                color: #0A1A44; background-color: #F5F5F5; selection-background-color: #26A69A; selection-color: #FFFFFF;
            }
            QComboBox::hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4682B4, stop:1 #26A69A); }
        """)
        button_layout2.addWidget(self.recovery_combo)

        self.ai_suggest_button = QPushButton("AI Suggestion")
        self.ai_suggest_button.setStyleSheet(self.button_style("#4682B4"))
        self.ai_suggest_button.clicked.connect(self.fetch_ai_recommendation)
        self.ai_suggest_button.setToolTip("Get AI-recommended deadlock resolution method")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.ai_suggest_button.setGraphicsEffect(fix_shadow)
        button_layout2.addWidget(self.ai_suggest_button)

        left_layout.addLayout(button_layout2)
        left_layout.addStretch()
        main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        self.sim_output = QTextEdit()
        self.sim_output.setReadOnly(True)
        self.sim_output.setStyleSheet("QTextEdit { background-color: #F5E6E8; color: #0A1A44; font-family: 'Lilita', 'Helvetica', sans-serif; font-size: 16px; font-weight: bold; border: 1px solid #0A1A44; padding: 5px; }")
        self.sim_output.setFixedHeight(150)
        sim_shadow = QGraphicsDropShadowEffect()
        sim_shadow.setBlurRadius(15)
        sim_shadow.setXOffset(0)
        sim_shadow.setYOffset(0)
        sim_shadow.setColor(QColor(255, 255, 255, 200))
        self.sim_output.setGraphicsEffect(sim_shadow)
        right_layout.addWidget(self.sim_output)

        self.figure_tab3 = Figure(figsize=(6, 5))
        self.figure_tab3.patch.set_alpha(0)
        self.canvas_tab3 = FigureCanvas(self.figure_tab3)
        self.canvas_tab3.setStyleSheet("border: 1px solid #0A1A44; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B3E5FC, stop:1 #4FC3F7);")
        right_layout.addWidget(self.canvas_tab3, stretch=1)
        self.update_chart_tab3()
        right_layout.addStretch()
        main_layout.addLayout(right_layout)

        tab3.setLayout(main_layout)
        self.tabs.addTab(tab3, "Simulation Mode")

    def setup_tab4(self):
        tab4 = QWidget()
        layout = QVBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter scenario (e.g., 'P1 waits for P2, P2 waits for P3')")
        self.text_input.setStyleSheet("QLineEdit { background-color: #FFFFFF; color: #0A1A44; font-size: 16px; border: 1px solid #0A1A44; padding: 5px; }")
        self.text_input.setToolTip("Type a scenario for AI analysis")
        layout.addWidget(self.text_input)

        self.predict_button = QPushButton("Predict Deadlock")
        self.predict_button.setStyleSheet(self.button_style("#26A69A"))
        self.predict_button.clicked.connect(self.predict_deadlock)
        self.predict_button.setToolTip("Get AI predictions using Gemini")
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.predict_button.setGraphicsEffect(fix_shadow)
        layout.addWidget(self.predict_button)

        self.ai_log = QTextEdit()
        self.ai_log.setReadOnly(True)
        self.ai_log.setStyleSheet("QTextEdit { background-color: #F5E6E8; color: #0A1A44; font-family: 'Lilita', 'Helvetica', sans-serif; font-size: 16px; font-weight: bold; border: none; }")
        ai_shadow = QGraphicsDropShadowEffect()
        ai_shadow.setBlurRadius(15)
        ai_shadow.setXOffset(0)
        ai_shadow.setYOffset(0)
        ai_shadow.setColor(QColor(255, 255, 255, 200))
        self.ai_log.setGraphicsEffect(ai_shadow)
        layout.addWidget(self.ai_log)
        tab4.setLayout(layout)
        self.tabs.addTab(tab4, "AI Prediction")

    def update_chart_tab1(self):
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        self.series1 = [sum(1 for u, v in self.deadlock_graph_tab1.edges if u == p) for p in self.processes]
        self.series2 = [sum(1 for u, v in self.deadlock_graph_tab1.edges if v == p) for p in self.processes]
        self.series3 = [1] * self.num_processes
        self.waiting_on_details = {p: [] for p in self.processes}
        self.waited_by_details = {p: [] for p in self.processes}
        for u, v in self.deadlock_graph_tab1.edges:
            if u in self.processes:
                self.waiting_on_details[u].append(v)
            if v in self.processes:
                self.waited_by_details[v].append(u)

        self.figure_tab1.clear()
        ax = self.figure_tab1.add_subplot(111)
        ax.set_facecolor('#F5F5F5')
        x = np.arange(len(self.processes))
        width = 0.2
        ax.bar(x - width - 0.02, [s * 0.9 for s in self.series1], width, color='gray', alpha=0.3, zorder=1, label="_nolegend_")
        ax.bar(x - 0.02, [s * 0.9 for s in self.series2], width, color='gray', alpha=0.3, zorder=1, label="_nolegend_")
        ax.bar(x + width - 0.02, [s * 0.9 for s in self.series3], width, color='gray', alpha=0.3, zorder=1, label="_nolegend_")
        bars1 = ax.bar(x - width, self.series1, width, label="Waiting On", color='#4682B4', edgecolor='black', hatch='//', zorder=2)
        bars2 = ax.bar(x, self.series2, width, label="Waited By", color='#FF6347', edgecolor='black', hatch='//', zorder=2)
        bars3 = ax.bar(x + width, self.series3, width, label="Resources Held", color='#3CB371', edgecolor='black', hatch='//', zorder=2)
        ax.set_xticks(x)
        ax.set_xticklabels(self.processes)
        ax.set_ylabel("Number of Dependencies")
        ax.set_title("Process Dependency Analysis")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        self.canvas_tab1.draw()

    def update_chart_tab2(self):
        self.figure_tab2.clear()
        self.ax = self.figure_tab2.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#F5F5F5')
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        self.series1 = [sum(1 for u, v in self.deadlock_graph_tab1.edges if u == p) for p in self.processes]
        self.series2 = [sum(1 for u, v in self.deadlock_graph_tab1.edges if v == p) for p in self.processes]
        self.series3 = [1] * self.num_processes

        if self.current_graph_type == "3D Bar Plot":
            x = np.arange(len(self.processes))
            y = np.zeros(len(self.processes))
            z1, z2, z3 = self.series1, self.series2, self.series3
            dx = dy = 0.5
            self.ax.bar3d(x - 0.2, y, np.zeros(len(z1)), dx, dy, z1, color='#4682B4', label='Waiting On', edgecolor='black', shade=True)
            self.ax.bar3d(x, y, np.zeros(len(z2)), dx, dy, z2, color='#FF6347', label='Waited By', edgecolor='black', shade=True)
            self.ax.bar3d(x + 0.2, y, np.zeros(len(z3)), dx, dy, z3, color='#3CB371', label='Resources Held', edgecolor='black', shade=True)
            for u, v in self.deadlock_graph_tab1.edges:
                u_idx = self.processes.index(u)
                v_idx = self.processes.index(v)
                self.ax.plot([u_idx, v_idx], [0, 0], [z1[u_idx], z2[v_idx]], c='black', alpha=0.5)
            self.ax.set_xlabel("Processes")
            self.ax.set_ylabel("Depth (Fixed)")
            self.ax.set_zlabel("Number of Dependencies")
            self._add_legend()

        elif self.current_graph_type == "3D Scatter Plot":
            pos = nx.spring_layout(self.deadlock_graph_tab1, dim=3)
            nodes = list(self.deadlock_graph_tab1.nodes)
            x, y, z = [], [], []
            for node in nodes:
                x_i, y_i, z_i = pos[node]
                x.append(x_i)
                y.append(y_i)
                z.append(z_i)
            scatter = self.ax.scatter(x, y, z, c=['red', 'green', 'blue', 'yellow', 'gray', 'purple', 'orange', 'pink', 'brown'][:len(nodes)], s=100)
            for u, v in self.deadlock_graph_tab1.edges:
                x = [pos[u][0], pos[v][0]]
                y = [pos[u][1], pos[v][1]]
                z = [pos[u][2], pos[v][2]]
                self.ax.plot(x, y, z, c='black', alpha=0.5)
            self.ax.set_xlabel("X Coordinate")
            self.ax.set_ylabel("Y Coordinate")
            self.ax.set_zlabel("Z Coordinate")
            self._add_legend()

        elif self.current_graph_type == "3D Surface Plot":
            x = np.arange(len(self.processes))
            y = np.zeros(len(self.processes))
            X, Y = np.meshgrid(x, y)
            Z = np.array([self.series1])
            self.ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='black')
            for u, v in self.deadlock_graph_tab1.edges:
                u_idx = self.processes.index(u)
                v_idx = self.processes.index(v)
                self.ax.plot([u_idx, v_idx], [0, 0], [self.series1[u_idx], self.series1[v_idx]], c='black', alpha=0.5)
            self.ax.set_xlabel("Processes")
            self.ax.set_ylabel("Depth (Fixed)")
            self.ax.set_zlabel("Dependency Count")
            self._add_legend()

        elif self.current_graph_type == "3D Circular Layout":
            theta = np.linspace(0, 2*np.pi, len(self.processes), endpoint=False)
            x = np.cos(theta)
            y = np.sin(theta)
            z = np.zeros(len(self.processes))
            self.ax.scatter(x, y, z, c=['red', 'green', 'blue', 'yellow', 'gray', 'purple', 'orange', 'pink', 'brown'][:len(self.processes)], s=100)
            for u, v in self.deadlock_graph_tab1.edges:
                u_idx = self.processes.index(u)
                v_idx = self.processes.index(v)
                self.ax.plot([x[u_idx], x[v_idx]], [y[u_idx], y[v_idx]], [0, 0], c='black', alpha=0.5)
            self.ax.set_xlabel("X Coordinate")
            self.ax.set_ylabel("Y Coordinate")
            self.ax.set_zlabel("Z Coordinate (Fixed)")
            self._add_legend()

        else:
            self.current_graph_type = "3D Bar Plot"
            self.update_chart_tab2()

        self.ax.set_title(f"{self.current_graph_type} of Tab 1 Dependencies")
        self.canvas_tab2.draw()

    def _add_legend(self):
        legend_ax = self.figure_tab2.add_axes([0.85, 0.05, 0.15, 0.9])
        legend_ax.axis('off')
        handles = [
            plt.Line2D([0], [0], color='#4682B4', lw=10, label='Waiting On'),
            plt.Line2D([0], [0], color='#FF6347', lw=10, label='Waited By'),
            plt.Line2D([0], [0], color='#3CB371', lw=10, label='Resources Held'),
            plt.Line2D([0, 1], [0, 0], color='black', lw=2, label='Dependency Direction')
        ]
        legend_ax.legend(handles=handles, loc='center', frameon=True)

    def show_graph_selection(self):
        graph_types = ["3D Bar Plot", "3D Scatter Plot", "3D Surface Plot", "3D Circular Layout"]
        combo = QComboBox()
        combo.addItems(graph_types)
        combo.setCurrentText(self.current_graph_type)
        combo.currentTextChanged.connect(lambda x: self.set_graph_type(x))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Graph Type to Visualize Tab 1 Dependencies:"))
        for name in graph_types:
            layout.addWidget(QLabel(name))
        layout.addWidget(combo)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: (self.set_graph_type(combo.currentText()), dialog.close()))
        layout.addWidget(ok_button)

        dialog = QDialog(self)
        dialog.setLayout(layout)
        dialog.setWindowTitle("Choose Graph")
        dialog.exec()

    def set_graph_type(self, graph_type):
        self.current_graph_type = graph_type
        self.update_chart_tab2()

    def update_chart_tab3(self):
        self.figure_tab3.clear()
        ax = self.figure_tab3.add_subplot(111, projection='3d')
        ax.set_facecolor('#F5F5F5')
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        
        for p in self.processes:
            if p not in self.deadlock_graph_tab3.nodes:
                self.deadlock_graph_tab3.add_node(p)
        
        if self.deadlock_graph_tab3.edges:
            pos = nx.circular_layout(self.deadlock_graph_tab3)
        else:
            theta = np.linspace(0, 2 * np.pi, len(self.processes), endpoint=False)
            pos = {p: [np.cos(t), np.sin(t)] for p, t in zip(self.processes, theta)}
        
        z = [sum(1 for u, v in self.deadlock_graph_tab3.edges if u == p or v == p) for p in self.processes]
        max_z = max(z) if z and max(z) > 0 else 1
        node_sizes = [1000 * (z_i / max_z) + 500 for z_i in z]
        
        scatter = ax.scatter([pos[p][0] for p in self.processes], [pos[p][1] for p in self.processes], z,
                            c=['red', 'green', 'blue', 'yellow', 'gray', 'purple', 'orange', 'pink', 'brown'][:self.num_processes], s=node_sizes, alpha=0.7)
        for u, v in self.deadlock_graph_tab3.edges:
            u_idx = self.processes.index(u)
            v_idx = self.processes.index(v)
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], [z[u_idx], z[v_idx]],
                    c='black', linewidth=2, alpha=0.8)
        
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_zlabel("Dependency Weight")
        ax.set_title("Dynamic Dependency Network")
        self.canvas_tab3.draw()

    def start_simulation(self):
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.simulate_step)
        self.deadlock_graph_tab3 = self.get_table_data_tab3()
        deadlock_type = self.identify_deadlock_type(self.deadlock_graph_tab3)
        if "No Deadlock" in deadlock_type:
            self.add_sim_message("<span style='color: #FF4500;'><b>No Deadlock Detected.</b></span>")
        else:
            cycle = list(nx.find_cycle(self.deadlock_graph_tab3, orientation='original')) if "Circular Wait" in deadlock_type else []
            cycle_str = " -> ".join([f"{u} to {v}" for u, v, _ in cycle]) if cycle else "N/A"
            processes_involved = [p[0] for p in cycle] if cycle else list(self.deadlock_graph_tab3.nodes)
            self.add_sim_message(f"<span style='color: #FF4500;'><b>Deadlock Detected! Type: {deadlock_type}</b></span>")
            self.add_sim_message(f"<b>Processes Involved: {', '.join(processes_involved)}</b>")
            self.add_sim_message(f"<b>Cycle: {cycle_str}</b>")
            method_to_use = self.ai_suggested_method if self.ai_suggested_method else self.recovery_method
            self.add_sim_message(f"<span style='color: #006400;'><b>Starting simulation with {method_to_use} method...</b></span>")
            self.simulation_timer.start(1000)

    def fetch_ai_recommendation(self):
        self.deadlock_graph_tab3 = self.get_table_data_tab3()
        deadlock_type = self.identify_deadlock_type(self.deadlock_graph_tab3)
        if "No Deadlock" in deadlock_type:
            self.add_sim_message("<span style='color: #FF4500;'><b>No Deadlock Detected. No AI suggestion needed.</b></span>")
            return
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "insert_your_api")
        GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
        prompt = f"Given a deadlock of type '{deadlock_type}', recommend the best resolution method (Preemption, Random Kill, or Resource Timeout) in a concise point-wise format."
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            recommendation = result["candidates"][0]["content"]["parts"][0]["text"]
            lines = [line.strip() for line in recommendation.split('\n') if line.strip()]
            method = next((m for m in ["Resource Timeout", "Preemption", "Random Kill"] 
                          if any(m.lower() in line.lower() for line in lines)), "Preemption")
            explanation = [line.replace('*', '').replace('-', '').strip() 
                          for line in lines if not any(m.lower() in line.lower() for m in ["preemption", "random kill", "resource timeout"])]
            self.ai_suggested_method = method
            self.add_sim_message(f"<span style='color: #006400;'><b>AI Recommended Method: {method}</b></span>")
            self.add_sim_message("<b>Reasons:</b><br>" + "<br>".join(f"- {exp}" for exp in explanation[:3]))
            self.add_sim_message("<span style='color: #FF4500;'><b>Click 'Start Simulation' to use this method.</b></span>")
        except requests.exceptions.RequestException as e:
            self.add_sim_message(f"<span style='color: #FF4500;'><b>API Error: {str(e)}. Falling back to selected method.</b></span>")

    def stop_simulation(self):
        if hasattr(self, 'simulation_timer'):
            self.simulation_timer.stop()

    def clear_sim_output(self):
        self.sim_output.clear()

    def simulate_step(self):
        if "No Deadlock" not in self.identify_deadlock_type(self.deadlock_graph_tab3):
            try:
                cycle = list(nx.find_cycle(self.deadlock_graph_tab3, orientation='original'))
                method_to_use = self.ai_suggested_method if self.ai_suggested_method else self.recovery_method
                if method_to_use == "Preemption" and cycle:
                    process_to_remove = cycle[0][0]
                    self.deadlock_graph_tab3.remove_node(process_to_remove)
                    self.add_sim_message(f"<span style='color: #006400;'><b>Deadlock Resolved! Preempted process {process_to_remove} using {method_to_use}.</b></span>")
                elif method_to_use == "Random Kill" and self.deadlock_graph_tab3.nodes:
                    process_to_remove = random.choice(list(self.deadlock_graph_tab3.nodes))
                    self.deadlock_graph_tab3.remove_node(process_to_remove)
                    self.add_sim_message(f"<span style='color: #006400;'><b>Deadlock Resolved! Randomly killed process {process_to_remove} using {method_to_use}.</b></span>")
                elif method_to_use == "Resource Timeout" and cycle:
                    edge_to_remove = random.choice(cycle)[:2]
                    if (edge_to_remove[0], edge_to_remove[1]) in self.deadlock_graph_tab3.edges:
                        self.deadlock_graph_tab3.remove_edge(*edge_to_remove)
                        self.add_sim_message(f"<span style='color: #006400;'><b>Deadlock Resolved! Timed out dependency {edge_to_remove[0]} -> {edge_to_remove[1]} using {method_to_use}.</b></span>")
                else:
                    self.add_sim_message("<span style='color: #FF4500;'><b>No valid cycle or node to resolve deadlock.</b></span>")
            except nx.NetworkXNoCycle:
                self.add_sim_message("<span style='color: #006400;'><b>Deadlock Resolved! No cycle remaining.</b></span>")
            except Exception as e:
                self.add_sim_message(f"<span style='color: #FF4500;'><b>Error resolving deadlock: {e}</b></span>")
        else:
            self.add_sim_message("<span style='color: #FF4500;'><b>No Deadlock Remaining.</b></span>")
            self.stop_simulation()
        self.update_table_tab3()
        self.update_chart_tab3()

    def update_table_tab3(self):
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        for i in range(self.num_processes):
            for j in range(self.num_processes):
                item = QTableWidgetItem("1" if (self.processes[i], self.processes[j]) in self.deadlock_graph_tab3.edges else "0")
                self.table_tab3.setItem(i, j, item)

    def predict_deadlock(self):
        scenario = self.text_input.text()
        current_state = {f"{u}->{v}": 1 for u, v in self.deadlock_graph_tab1.edges}
        if current_state:
            self.history.append({"state": current_state, "label": 1 if self.identify_deadlock_type(self.deadlock_graph_tab1) != "No Deadlock" else 0, "timestamp": str(datetime.now())})
            try:
                with open("deadlock_history.json", "w") as f:
                    json.dump(self.history, f, indent=2)
            except Exception as e:
                self.ai_log.append(f"<b>Error saving history:</b> {str(e)}")

        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "insert_your_api")
        GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
        prompt = f"Analyze this scenario: '{scenario}' and historical data: {self.history}. Predict if a deadlock is likely and suggest prevention strategies. If the scenario is a question, provide a clear explanation."
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            prediction = result["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.HTTPError as http_err:
            self.ai_log.append(f"<b>HTTP Error:</b> {str(http_err)} - Please check your API key and endpoint.")
        except requests.exceptions.RequestException as req_err:
            self.ai_log.append(f"<b>Request Error:</b> {str(req_err)} - Check your internet connection or API service.")
        except (KeyError, IndexError) as parse_err:
            self.ai_log.append(f"<b>Parsing Error:</b> {str(parse_err)} - Invalid response format from API.")
        except Exception as e:
            self.ai_log.append(f"<b>Unexpected Error:</b> {str(e)} - Contact support if persistent.")
        else:
            formatted_prediction = "<b><u>AI Prediction Result</u></b><br>"
            formatted_prediction += f"<br><b style='color: #0A1A44;'>Scenario:</b> {scenario}<br>"
            lines = prediction.split('\n')
            current_section = ""
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if "likelihood of deadlock" in line.lower():
                    current_section = "prediction"
                    formatted_prediction += f"<br><b style='color: #FF6F61;'>Prediction:</b><br>"
                elif "prevention strategies" in line.lower():
                    current_section = "prevention"
                    formatted_prediction += f"<br><b style='color: #006400;'>Prevention Strategies:</b><br>"
                elif "improving prediction" in line.lower():
                    current_section = "improving"
                    formatted_prediction += f"<br><b style='color: #4682B4;'>Improving Prediction:</b><br>"
                elif "conclusion" in line.lower():
                    current_section = "conclusion"
                    formatted_prediction += f"<br><b style='color: #4682B4;'>Conclusion:</b><br>"
                elif "analysis" in line.lower():
                    current_section = "analysis"
                    formatted_prediction += f"<br><b style='color: #26A69A;'>Analysis:</b><br>"
                elif "explanation" in line.lower() or "what is" in scenario.lower():
                    current_section = "explanation"
                    formatted_prediction += f"<br><b style='color: #26A69A;'>Explanation:</b><br>"
                else:
                    clean_line = line.replace('- -', '-').replace('*-', '-').replace('*', '').strip()
                    if clean_line.startswith('-'):
                        formatted_prediction += f"- {clean_line[1:].strip()}<br>"
                    else:
                        formatted_prediction += f"{clean_line}<br>"

            self.ai_log.append(formatted_prediction)

        if scenario:
            self.processes = [f"P{i+1}" for i in range(self.num_processes)]
            parts = scenario.split(", ")
            for part in parts:
                if "waits for" in part:
                    try:
                        p1, p2 = part.split(" waits for ")
                        p1, p2 = p1.strip(), p2.strip()
                        if p1 in self.processes and p2 in self.processes:
                            self.deadlock_graph_tab1.add_edge(p1, p2)
                    except ValueError:
                        self.ai_log.append(f"<b>Warning:</b> Invalid format in '{part}', expected 'P1 waits for P2'")
            self.update_chart_tab1()
            self.update_table_tab3()
            self.update_chart_tab2()

    def export_graph(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"deadlock_graph_{timestamp}.png"
        self.figure_tab1.savefig(filename)
        self.add_message(f"Graph exported as '{filename}'")

    def export_values(self):
        import csv
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dependency_values_{timestamp}.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([""] + self.processes)
            for i, row in enumerate(range(self.num_processes)):
                data = [f"P{i+1}"] + [self.table_tab1.item(row, col).text() if self.table_tab1.item(row, col) else "0" for col in range(self.num_processes)]
                writer.writerow(data)
        self.add_message(f"Values exported as '{filename}'")

    def add_message(self, msg):
        if "System initialized" in msg:
            formatted_msg = f'<b><u>{msg}</u></b>'
        elif "No Deadlock Detected" in msg or "Deadlock Detected" in msg or "No Deadlock Remaining" in msg or "ML Analysis" in msg:
            formatted_msg = f'<span style="color: #FF4500;"><b>{msg}</b></span>'
        elif "Deadlock Resolved" in msg:
            formatted_msg = f'<span style="color: #006400;"><b>{msg}</b></span>'
        elif "Process" in msg and ("Waited By" in msg or "Waiting On" in msg):
            formatted_msg = f'<span style="color: #0A1A44;">{msg}</span>'
        else:
            formatted_msg = msg
        self.message_log.append(f'<span style="font-family: \'Lilita\', \'Helvetica\', sans-serif; font-size: 16px; font-weight: bold;">{formatted_msg}</span>')
        self.message_log.ensureCursorVisible()

    def add_sim_message(self, msg):
        if "System initialized" in msg:
            formatted_msg = f'<b><u>{msg}</u></b>'
        elif "No Deadlock Detected" in msg or "Deadlock Detected" in msg or "No Deadlock Remaining" in msg or "Okay, now let's fix this deadlock" in msg:
            formatted_msg = f'<span style="color: #FF4500;"><b>{msg}</b></span>'
        elif "Deadlock Resolved" in msg:
            formatted_msg = f'<span style="color: #006400;"><b>{msg}</b></span>'
        elif "Process" in msg and ("Waited By" in msg or "Waiting On" in msg):
            formatted_msg = f'<span style="color: #0A1A44;">{msg}</span>'
        else:
            formatted_msg = msg
        self.sim_output.append(f'<span style="font-family: \'Lilita\', \'Helvetica\', sans-serif; font-size: 16px; font-weight: bold;">{formatted_msg}</span>')
        self.sim_output.ensureCursorVisible()

    def get_table_data_tab1(self):
        graph = nx.DiGraph()
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        for i in range(self.num_processes):
            for j in range(self.num_processes):
                item = self.table_tab1.item(i, j)
                if item and item.text() == "1":
                    graph.add_edge(self.processes[i], self.processes[j])
        return graph

    def get_table_data_tab3(self):
        graph = nx.DiGraph()
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        for i in range(self.num_processes):
            for j in range(self.num_processes):
                item = self.table_tab3.item(i, j)
                if item and item.text() == "1":
                    graph.add_edge(self.processes[i], self.processes[j])
        return graph

    def analyze_ml_deadlock(self):
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        self.series1 = [sum(1 for u, v in self.deadlock_graph_tab1.edges if u == p) for p in self.processes]  # Waiting On
        self.series2 = [sum(1 for u, v in self.deadlock_graph_tab1.edges if v == p) for p in self.processes]  # Waited By
        self.series3 = [1] * self.num_processes  # Resources Held
        try:
            cycle = list(nx.find_cycle(self.deadlock_graph_tab1, orientation='original'))
            cycle_nodes = set([n for edge in cycle for n in edge[:2]])
            cycle_feature = [1 if p in cycle_nodes else 0 for p in self.processes]
        except nx.NetworkXNoCycle:
            cycle_feature = [0] * self.num_processes

        X = np.array([[w, wb, r, c] for w, wb, r, c in zip(self.series1, self.series2, self.series3, cycle_feature)])

        kmeans = KMeans(n_clusters=2, random_state=42)
        clusters = kmeans.fit_predict(X)

        risky_processes = [self.processes[i] for i in range(len(clusters)) if cycle_feature[i] == 1]

        if risky_processes:
            message = f"ML Analysis: Potential deadlock risk detected in processes {', '.join(risky_processes)} due to cycle involvement."
        else:
            message = "ML Analysis: No significant deadlock risk detected based on clustering."

        self.add_message(message)

    def identify_deadlock_type(self, graph):
        if not graph or not graph.edges:
            return "No Deadlock"
        
        edges = list(graph.edges)
        edges_set = set(edges)
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]

        # Check for Mutual Exclusion (self-loops)
        has_self_loop = any(u == v for u, v in edges)
        if has_self_loop:
            return "Mutual Exclusion Deadlock (Self-loop detected)"

        # Check for Circular Wait (cycles in the graph)
        try:
            cycle = nx.find_cycle(graph, orientation="original")
            if cycle:
                return "Circular Wait Deadlock"
        except nx.NetworkXNoCycle:
            pass

        # Check for No Preemption (bidirectional dependencies)
        has_bidirectional = any((v, u) in edges_set for u, v in edges if u != v)
        if has_bidirectional:
            return "No Preemption Deadlock"

        return "No Deadlock"

    def detect_deadlock_tab1(self):
        self.deadlock_graph_tab1 = self.get_table_data_tab1()
        if len(self.deadlock_graph_tab1.nodes) == 0:
            self.add_message("No valid process dependencies found.")
            self.update_table_tab1()
            return

        deadlock_type = self.identify_deadlock_type(self.deadlock_graph_tab1)
        self.analyze_ml_deadlock()
        matrix = [[self.table_tab1.item(i, j).text() if self.table_tab1.item(i, j) else "0" for j in range(self.num_processes)] for i in range(self.num_processes)]
        if "No Deadlock" in deadlock_type:
            self.history.append({"matrix": matrix, "label": 0, "timestamp": str(datetime.now())})
            self.add_message("No Deadlock Detected.")
        else:
            cycle = list(nx.find_cycle(self.deadlock_graph_tab1, orientation='original')) if "Circular Wait" in deadlock_type else []
            cycle_str = " -> ".join([f"{u} to {v}" for u, v, _ in cycle]) if cycle else "N/A"
            processes_involved = [p[0] for p in cycle] if cycle else [n for n in self.deadlock_graph_tab1.nodes if any(n in edge for edge in self.deadlock_graph_tab1.edges)]
            explanation = f"Deadlock Detected! Type: {deadlock_type}<br>Processes Involved: {', '.join(processes_involved)}<br>Cycle: {cycle_str}"
            self.add_message(explanation)
            self.highlight_deadlock_tab1(processes_involved)
            self.history.append({"matrix": matrix, "label": 1, "cycle": cycle_str, "timestamp": str(datetime.now())})

        try:
            with open("deadlock_history.json", "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            self.add_message(f"Error saving history: {str(e)}")

        self.update_table_tab1()
        self.update_chart_tab1()
        self.update_chart_tab2()

    def show_bankers_config(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configure Banker's Algorithm")
        dialog.setMinimumSize(400, 600)  # Increased size for better visibility
        layout = QGridLayout()

        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        resources = ["R1", "R2", "R3"]
        available = [QSpinBox() for _ in range(3)]
        max_demand = [[QSpinBox() for _ in range(3)] for _ in range(self.num_processes)]
        allocation = [[QSpinBox() for _ in range(3)] for _ in range(self.num_processes)]

        layout.addWidget(QLabel("Available Resources:"), 0, 0, 1, 3)
        for i, (spin, res) in enumerate(zip(available, resources), 1):
            label = QLabel(f"{res}:")
            label.setStyleSheet("color: black; font-weight: bold;")
            layout.addWidget(label, i, 0)
            spin.setRange(0, 10)
            spin.setValue(3 if i == 1 else 3 if i == 2 else 3)
            spin.setStyleSheet("color: black; background-color: white;")
            layout.addWidget(spin, i, 1)

        layout.addWidget(QLabel("Max Demand:"), 4, 0)
        for i in range(self.num_processes):
            label = QLabel(self.processes[i])
            label.setStyleSheet("color: black; font-weight: bold;")
            layout.addWidget(label, i + 5, 0)
            for j in range(3):
                max_demand[i][j].setRange(0, 10)
                max_demand[i][j].setValue(self.max_demand[i][j])
                max_demand[i][j].setStyleSheet("color: black; background-color: white;")
                layout.addWidget(max_demand[i][j], i + 5, j + 1)

        layout.addWidget(QLabel("Allocation:"), 5 + self.num_processes, 0)
        for i in range(self.num_processes):
            label = QLabel(self.processes[i])
            label.setStyleSheet("color: black; font-weight: bold;")
            layout.addWidget(label, i + 6 + self.num_processes, 0)
            for j in range(3):
                allocation[i][j].setRange(0, 10)
                allocation[i][j].setValue(self.allocation[i][j])
                allocation[i][j].setStyleSheet("color: black; background-color: white;")
                layout.addWidget(allocation[i][j], i + 6 + self.num_processes, j + 1)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: #4CAF50; color: black; font-weight: bold; padding: 5px;")
        ok_button.clicked.connect(lambda: self.configure_bankers_and_detect(available, max_demand, allocation, dialog))
        layout.addWidget(ok_button, 6 + 2 * self.num_processes, 1)

        dialog.setLayout(layout)
        dialog.setStyleSheet("background-color: #E0F7FA; color: black;")
        dialog.exec()

    def configure_bankers_and_detect(self, available, max_demand, allocation, dialog):
        self.available = [spin.value() for spin in available]
        self.max_demand = [[spin.value() for spin in row] for row in max_demand]
        self.allocation = [[spin.value() for spin in row] for row in allocation]
        self.bankers_configured = True
        dialog.close()
        self.detect_deadlock_bankers()

    def detect_deadlock_bankers(self):
        if not self.bankers_configured:
            self.add_message("Please configure Banker's Algorithm parameters first.")
            return

        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        work = self.available.copy()
        need = [[max(0, m - a) for m, a in zip(max_d, alloc)] for max_d, alloc in zip(self.max_demand, self.allocation)]
        finish = [False] * self.num_processes
        safe_sequence = []

        while False in finish:
            found = False
            for p in range(self.num_processes):
                if not finish[p] and all(n <= w for n, w in zip(need[p], work)):
                    for j in range(len(work)):
                        work[j] += self.allocation[p][j]
                    safe_sequence.append(f"P{self.processes[p][1:]}")
                    finish[p] = True
                    found = True
            if not found:
                self.add_message("Deadlock Detected! Unsafe state identified by Banker's Algorithm.")
                return

        self.add_message(f"No Deadlock Detected! Safe sequence: {' -> '.join(safe_sequence)}")

    def highlight_deadlock_tab1(self, deadlocked_processes):
        gradient = QLinearGradient(0, 0, 100, 100)
        gradient.setColorAt(0, QColor("#8B0000"))
        gradient.setColorAt(1, QColor("#FF4500"))
        brush = QBrush(gradient)
        for process in deadlocked_processes:
            idx = int(process[1:]) - 1
            for col in range(self.num_processes):
                item = QTableWidgetItem(self.table_tab1.item(idx, col).text() if self.table_tab1.item(idx, col) else "0")
                item.setBackground(brush)
                self.table_tab1.setItem(idx, col, item)

    def fix_deadlock_tab1(self):
        if not self.deadlock_graph_tab1 or not self.deadlock_graph_tab1.edges:
            self.add_message("No deadlock detected to fix.")
            self.update_table_tab1()
            return

        deadlock_type = self.identify_deadlock_type(self.deadlock_graph_tab1)
        if "No Deadlock" in deadlock_type:
            self.add_message("No deadlock to fix.")
            self.update_table_tab1()
            return

        try:
            cycle = list(nx.find_cycle(self.deadlock_graph_tab1, orientation='original')) if "Circular Wait" in deadlock_type else []
            if cycle:
                process_to_remove = cycle[0][0]
                self.deadlock_graph_tab1.remove_node(process_to_remove)
                self.add_message(f"Deadlock Resolved! Process {process_to_remove} preempted to break Circular Wait.")
            elif "Mutual Exclusion" in deadlock_type:
                self_loop = next((u, v) for u, v in self.deadlock_graph_tab1.edges if u == v)
                self.deadlock_graph_tab1.remove_edge(*self_loop)
                self.add_message(f"Deadlock Resolved! Removed self-loop {self_loop[0]} to fix Mutual Exclusion.")
            elif "No Preemption" in deadlock_type:
                bidirectional_edge = next(((u, v) for u, v in self.deadlock_graph_tab1.edges if (v, u) in self.deadlock_graph_tab1.edges), None)
                if bidirectional_edge:
                    self.deadlock_graph_tab1.remove_edge(*bidirectional_edge)
                    self.add_message(f"Deadlock Resolved! Removed bidirectional edge {bidirectional_edge[0]} -> {bidirectional_edge[1]} to fix No Preemption.")
                else:
                    self.add_message("Error: Could not identify bidirectional edge to fix No Preemption.")
                    return

            self.update_table_tab1()
            self.update_chart_tab1()
            self.highlight_fix_tab1()
            self.update_chart_tab2()
        except nx.NetworkXNoCycle:
            self.add_message("No cycle detected to fix. Please verify the deadlock condition.")
            self.update_table_tab1()
        except Exception as e:
            self.add_message(f"Error resolving deadlock: {str(e)}")
            self.update_table_tab1()

    def highlight_fix_tab1(self):
        gradient = QLinearGradient(0, 0, 100, 100)
        gradient.setColorAt(0, QColor("#006400"))
        gradient.setColorAt(1, QColor("#90EE90"))
        brush = QBrush(gradient)
        for row in range(self.table_tab1.rowCount()):
            for col in range(self.table_tab1.columnCount()):
                item = QTableWidgetItem(self.table_tab1.item(row, col).text() if self.table_tab1.item(row, col) else "0")
                item.setBackground(brush)
                self.table_tab1.setItem(row, col, item)
        QTimer.singleShot(15000, self.reset_table_tab1)

    def update_table_tab1(self):
        self.processes = [f"P{i+1}" for i in range(self.num_processes)]
        for i in range(self.num_processes):
            for j in range(self.num_processes):
                item = QTableWidgetItem("1" if (self.processes[i], self.processes[j]) in self.deadlock_graph_tab1.edges else "0")
                self.table_tab1.setItem(i, j, item)

    def reset_table_tab1(self):
        for row in range(self.table_tab1.rowCount()):
            for col in range(self.table_tab1.columnCount()):
                item = self.table_tab1.item(row, col)
                if item:
                    item.setBackground(QColor("#FFFFFF"))

    def on_bar_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if x is None or y is None:
                return
            process_idx = int(round(x))
            if 0 <= process_idx < len(self.processes):
                process = self.processes[process_idx]
                waited_by_count = len(self.waited_by_details[process])
                waiting_on_count = len(self.waiting_on_details[process])
                details = [
                    f"Process {process} - Waited By Details:",
                    f"  Count: {waited_by_count} process{'es' if waited_by_count != 1 else ''}",
                    f"  Definition: This indicates the number of processes that are waiting for {process} to release resources.",
                    f"  Processes: {', '.join(self.waited_by_details[process]) if self.waited_by_details[process] else 'None'}",
                    f"Process {process} - Waiting On Details:",
                    f"  Count: {waiting_on_count} process{'es' if waiting_on_count != 1 else ''}",
                    f"  Definition: This indicates the number of processes that {process} is waiting for to release resources.",
                    f"  Processes: {', '.join(self.waiting_on_details[process]) if self.waiting_on_details[process] else 'None'}"
                ]
                for detail in details:
                    self.add_message(detail)

    def rotate_view(self, horizontal, vertical):
        if hasattr(self, 'ax'):
            current_elev = self.ax.elev
            current_azim = self.ax.azim
            # Horizontal rotation adjusts azimuth (around vertical axis)
            if horizontal:
                self.ax.view_init(elev=current_elev, azim=current_azim + 15)
            # Vertical rotation adjusts elevation (up/down tilt)
            if vertical:
                self.ax.view_init(elev=current_elev + 15, azim=current_azim)
            self.canvas_tab2.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeadlockDetectionAI()
    window.show()
    sys.exit(app.exec())
