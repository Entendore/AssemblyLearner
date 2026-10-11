#!/usr/bin/env python3
"""
Assembly Learning Lab v5.0 - Comprehensive Multi-Architecture Edition
A PySide6 interactive educational tool for learning assembly language.
Covers x86, ARM, RISC-V, MIPS with detailed use cases and concepts.
"""

import sys, re, json, os, math, webbrowser, html as html_mod
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from collections import deque
from datetime import datetime

from PySide6.QtCore import (Qt, QObject, Signal, Slot, QRegularExpression, QTimer, QSize,
    QPoint, QRect, QPropertyAnimation, QEasingCurve, QThread, QRunnable, QThreadPool, QSettings, QUrl)
from PySide6.QtGui import (QColor, QFont, QFontDatabase, QSyntaxHighlighter, QTextCharFormat,
    QPainter, QPen, QBrush, QLinearGradient, QKeySequence, QAction, QTextCursor, QTextFormat,
    QIcon, QPalette, QPixmap, QShortcut, QDesktopServices, QTextDocument)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QTabWidget,
    QPlainTextEdit, QTextEdit, QDialog, QPushButton, QLabel, QLineEdit, QScrollArea, QFrame,
    QGroupBox, QToolBar, QStatusBar, QMenuBar, QMenu, QFileDialog, QMessageBox, QProgressBar,
    QComboBox, QSpinBox, QTreeWidget, QTreeWidgetItem, QSizePolicy, QCheckBox, QSlider,
    QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsView, QGraphicsScene, QInputDialog,
    QFormLayout, QDialogButtonBox, QTextBrowser, QDockWidget, QCompleter, QToolButton,
    QListWidget, QListWidgetItem, QToolTip)

# ============================================================
# LOAD INSTRUCTION DATA
# ============================================================

_SCRIPT_DIR = Path(__file__).parent
_DATA_PATH = _SCRIPT_DIR / "instruction_data.json"

def _load_instruction_data():
    if _DATA_PATH.exists():
        with open(_DATA_PATH, "r") as f:
            return json.load(f)
    return {"x86": {}, "arm": {}, "riscv": {}, "mips": {}, "concepts": []}

_RAW_DATA = _load_instruction_data()

# ============================================================
# THEME SYSTEM
# ============================================================

class Theme:
    _current = "dark"
    DARK = {"bg_primary":"#0d1117","bg_secondary":"#161b22","bg_tertiary":"#21262d","bg_elevated":"#30363d",
        "fg_primary":"#c9d1d9","fg_secondary":"#8b949e","fg_muted":"#6e7681","accent_blue":"#58a6ff",
        "accent_green":"#3fb950","accent_red":"#f85149","accent_yellow":"#d29922","accent_purple":"#a371f7",
        "accent_cyan":"#39c5cf","accent_orange":"#e3b341","border":"#30363d","border_hover":"#8b949e",
        "success":"#3fb950","error":"#f85149","warning":"#d29922"}
    LIGHT = {"bg_primary":"#ffffff","bg_secondary":"#f6f8fa","bg_tertiary":"#eaeef2","bg_elevated":"#d0d7de",
        "fg_primary":"#24292f","fg_secondary":"#57606a","fg_muted":"#8c959f","accent_blue":"#0969da",
        "accent_green":"#1a7f37","accent_red":"#cf222e","accent_yellow":"#9a6700","accent_purple":"#8250df",
        "accent_cyan":"#1b7c83","accent_orange":"#bf8700","border":"#d0d7de","border_hover":"#8c959f",
        "success":"#1a7f37","error":"#cf222e","warning":"#9a6700"}
    PURPLE = {"bg_primary":"#1e1e2e","bg_secondary":"#282840","bg_tertiary":"#33335a","bg_elevated":"#3d3d6b",
        "fg_primary":"#cdd6f4","fg_secondary":"#a6adc8","fg_muted":"#6c7086","accent_blue":"#89b4fa",
        "accent_green":"#a6e3a1","accent_red":"#f38ba8","accent_yellow":"#f9e2af","accent_purple":"#cba6f7",
        "accent_cyan":"#94e2d5","accent_orange":"#fab387","border":"#45475a","border_hover":"#9399b2",
        "success":"#a6e3a1","error":"#f38ba8","warning":"#f9e2af"}

    @classmethod
    def available_themes(cls): return ["dark", "light", "purple"]
    @classmethod
    def set_mode(cls, mode: str):
        if mode.lower() in ("dark","light","purple"): cls._current = mode.lower()
    @classmethod
    def get(cls, key: str) -> str:
        t = {"dark":cls.DARK,"light":cls.LIGHT,"purple":cls.PURPLE}.get(cls._current, cls.DARK)
        return t.get(key, cls.DARK.get(key, "#000000"))

    @classmethod
    def stylesheet(cls):
        g = cls.get; t = g('bg_primary')
        s = """
QMainWindow{background:%s}
QWidget{background:%s;color:%s;font-family:"JetBrains Mono","Fira Code","Consolas",monospace;font-size:10pt}
QPlainTextEdit,QTextEdit{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:8px;selection-background-color:%s40}
QPlainTextEdit:focus,QTextEdit:focus{border:1px solid %s}
QPushButton{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:8px 16px;font-weight:bold}
QPushButton:hover{background:%s;border-color:%s}
QPushButton:pressed{background:%s30}
QPushButton:disabled{background:%s;color:%s}
QLineEdit{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:6px 10px}
QLineEdit:focus{border:1px solid %s}
QTabWidget::pane{border:1px solid %s;border-radius:6px;background:%s}
QTabBar::tab{background:%s;color:%s;border:1px solid %s;border-bottom:none;border-top-left-radius:6px;border-top-right-radius:6px;padding:8px 16px;margin-right:2px}
QTabBar::tab:selected{background:%s20;color:%s;border-color:%s}
QTabBar::tab:hover:!selected{background:%s;color:%s}
QGroupBox{border:1px solid %s;border-radius:8px;margin-top:12px;padding-top:12px;font-weight:bold;color:%s}
QGroupBox::title{subcontrol-origin:margin;left:12px;padding:0 8px}
QScrollBar:vertical{background:%s;width:12px;border-radius:6px}
QScrollBar::handle:vertical{background:%s;border-radius:6px;min-height:30px}
QScrollBar::handle:vertical:hover{background:%s}
QTreeWidget{background:%s;border:1px solid %s;border-radius:6px}
QTreeWidget::item{padding:4px}
QTreeWidget::item:selected{background:%s30}
QComboBox{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:6px 10px}
QComboBox QAbstractItemView{background:%s;color:%s;selection-background-color:%s30;border:1px solid %s}
QMenuBar{background:%s;color:%s;border-bottom:1px solid %s}
QMenuBar::item:selected{background:%s}
QMenu{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:4px}
QMenu::item:selected{background:%s30}
QMenu::separator{height:1px;background:%s;margin:4px 8px}
QToolBar{background:%s;border:none;spacing:2px;padding:4px}
QStatusBar{background:%s;color:%s;border-top:1px solid %s}
QProgressBar{background:%s;border:1px solid %s;border-radius:4px;text-align:center;color:%s}
QProgressBar::chunk{background:%s;border-radius:4px}
QSplitter::handle{background:%s}
QSplitter::handle:horizontal{width:3px}
QSpinBox{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:4px}
QTableWidget{background:%s;border:1px solid %s;border-radius:6px;gridline-color:%s}
QTableWidget::item{padding:4px;border-bottom:1px solid %s}
QTableWidget::item:selected{background:%s30}
QHeaderView::section{background:%s;color:%s;padding:6px;border:none;border-bottom:1px solid %s;font-weight:bold}
QCheckBox{color:%s}
QCheckBox::indicator{width:16px;height:16px;border-radius:3px;border:1px solid %s;background:%s}
QCheckBox::indicator:checked{background:%s;border-color:%s}
QSlider::groove:horizontal{height:6px;background:%s;border-radius:3px}
QSlider::handle:horizontal{width:16px;height:16px;margin:-5px 0;background:%s;border-radius:8px}
QDockWidget{color:%s}
QDockWidget::title{background:%s;padding:6px;border:1px solid %s;border-radius:4px}
QListWidget{background:%s;border:1px solid %s;border-radius:6px}
QListWidget::item{padding:6px}
QListWidget::item:selected{background:%s30}
QListWidget::item:hover{background:%s}
QToolTip{background:%s;color:%s;border:1px solid %s;border-radius:4px;padding:6px;font-family:"JetBrains Mono",monospace;font-size:9pt}
QDialog{background:%s}
QToolButton{background:transparent;border:1px solid transparent;border-radius:6px;padding:6px 10px;color:%s;font-size:9pt}
QToolButton:hover{background:%s;border-color:%s}
QToolButton:pressed{background:%s30}
QToolButton:checked{background:%s25;border-color:%s;color:%s}
QTextBrowser{background:%s;color:%s;border:1px solid %s;border-radius:6px;padding:8px}
QScrollArea{border:none}
""" % (
    g('bg_primary'), g('bg_primary'), g('fg_primary'),
    g('bg_secondary'), g('fg_primary'), g('border'), g('accent_blue'), g('accent_blue'),
    g('bg_tertiary'), g('fg_primary'), g('border'),
    g('bg_elevated'), g('border_hover'), g('accent_blue'),
    g('bg_tertiary'), g('fg_muted'),
    g('bg_secondary'), g('fg_primary'), g('border'), g('accent_blue'),
    g('border'), g('bg_secondary'),
    g('bg_tertiary'), g('fg_secondary'), g('border'),
    g('accent_blue'), g('accent_blue'), g('accent_blue'),
    g('bg_elevated'), g('fg_primary'),
    g('border'), g('fg_secondary'),
    g('bg_secondary'), g('bg_elevated'), g('fg_muted'),
    g('bg_secondary'), g('border'),
    g('bg_secondary'), g('fg_primary'), g('border'),
    g('bg_secondary'), g('fg_primary'), g('accent_blue'), g('border'),
    g('bg_primary'), g('fg_primary'), g('border'),
    g('bg_tertiary'),
    g('bg_secondary'), g('fg_primary'), g('border'),
    g('bg_secondary'), g('fg_secondary'), g('border'),
    g('bg_tertiary'), g('border'), g('fg_primary'),
    g('border'),
    g('bg_secondary'), g('border'), g('border'),
    g('border'),
    g('accent_blue'),
    g('bg_tertiary'), g('fg_secondary'), g('border'),
    g('fg_primary'),
    g('border'), g('bg_secondary'),
    g('accent_blue'), g('accent_blue'),
    g('bg_tertiary'),
    g('accent_blue'),
    g('fg_primary'),
    g('bg_tertiary'), g('border'),
    g('bg_secondary'), g('border'),
    g('accent_blue'),
    g('bg_elevated'),
    g('bg_elevated'), g('fg_primary'), g('border'),
    g('bg_primary'),
    g('fg_primary'),
    g('bg_tertiary'), g('border'),
    g('accent_blue'),
    g('accent_blue'),
    g('accent_blue'),
    g('bg_secondary'), g('fg_primary'), g('border'), g('accent_blue'),
)
        return s

# ============================================================
# DATA MODELS
# ============================================================

class RegisterSize(Enum):
    BYTE=8; WORD=16; DWORD=32; QWORD=64

@dataclass
class Register:
    name: str; size: RegisterSize; value: int = 0; is_flag: bool = False
    history: deque = field(default_factory=lambda: deque(maxlen=100))
    def set_value(self, val: int): self.value = val & ((1 << self.size.value) - 1)
    def get_hex(self): return f"0x{self.value:0{self.size.value//4}x}"
    def get_binary(self): return f"0b{self.value:0{self.size.value}b}"

@dataclass
class MemoryCell:
    address: int; value: int = 0; label: Optional[str] = None
    def get_hex(self): return f"0x{self.value:02x}"

@dataclass
class Instruction:
    opcode: str; operands: List[str]; description: str; category: str
    difficulty: int; example: str; cycles: int = 1; affects_flags: str = ""
    use_cases: List[str] = field(default_factory=list)
    notes: str = ""
    architecture: str = "x86"

@dataclass
class Lesson:
    title: str; description: str; instructions: List[str]; objective: str; hint: str
    code_template: str = ""; expected_eax: Optional[int] = None
    expected_flags: Optional[Dict[str,int]] = None; challenge_time: Optional[int] = None
    challenge_stars: int = 3; concept: str = ""

@dataclass
class ExecutionRecord:
    line_number: int; instruction: str; result: str
    registers_before: Dict[str,int]; registers_after: Dict[str,int]
    flags_after: Dict[str,int]; timestamp: str; cycles: int = 1

@dataclass
class Breakpoint:
    line_number: int; enabled: bool = True; condition: Optional[str] = None

@dataclass
class CodeSnippet:
    name: str; description: str; code: str; category: str

# ============================================================
# BUILD INSTRUCTION DATABASE FROM JSON
# ============================================================

def build_instruction_db():
    """Convert JSON data into Instruction dataclass objects."""
    db = {}
    x86_raw = _RAW_DATA.get("x86", {})
    for opcode, d in x86_raw.items():
        db[opcode] = Instruction(
            opcode=d.get("opcode", opcode),
            operands=d.get("operands", []),
            description=d.get("description", ""),
            category=d.get("category", ""),
            difficulty=d.get("difficulty", 1),
            example=d.get("example", ""),
            cycles=d.get("cycles", 1),
            affects_flags=d.get("affects_flags", ""),
            use_cases=d.get("use_cases", []),
            notes=d.get("notes", ""),
            architecture="x86"
        )
    return db

JUMP_ALIASES = {"JZ":"JE","JNZ":"JNE","JNAE":"JB","JNB":"JAE","JNA":"JBE","JNBE":"JA"}

INSTRUCTION_DB = build_instruction_db()

# ============================================================
# LESSON CURRICULUM (40 lessons)
# ============================================================

LESSONS = [
    Lesson("Lesson 1: Moving Data","Learn MOV to transfer data between registers and immediates.",
        ["MOV"],"Set EAX to 42.","Use: MOV eax, 42","; Set EAX to 42\n",42,None,30,3,
        "MOV is the most fundamental instruction. It copies a value from source to destination. It never modifies flags. It is the single most-used instruction in x86 code (~25% of all instructions)."),
    Lesson("Lesson 2: Basic Arithmetic","Use ADD and SUB to perform calculations.",
        ["MOV","ADD","SUB"],"Calculate 15 + 27 in EAX.","MOV eax, 15 then ADD eax, 27","; 15 + 27\n",42,None,45,3,
        "ADD adds two values, SUB subtracts. Both modify flags based on the result. ADD/SUB are the workhorses of arithmetic in assembly."),
    Lesson("Lesson 3: Bitwise Operations","Master AND, OR, XOR for bit manipulation.",
        ["MOV","AND","OR","XOR"],"Set EAX=0xFF, clear lower nibble to get 0xF0.","AND eax, 0xF0","; Clear lower nibble\nMOV eax, 0xFF\n",0xF0,None,60,3,
        "AND clears bits (masking), OR sets bits, XOR toggles bits. Essential for low-level programming, device drivers, and protocol implementations."),
    Lesson("Lesson 4: Shifting Bits","Use SHL/SHR to multiply/divide by powers of 2.",
        ["MOV","SHL","SHR"],"Multiply 8 by 4 using SHL (result=32).","SHL eax, 2 = multiply by 4","; 8 * 4 via shift\nMOV eax, 8\n",32,None,45,3,
        "SHL shifts left (multiply by 2^n), SHR shifts right (unsigned divide by 2^n). Much faster than MUL/DIV! Compilers use shifts to replace multiplications by constants."),
    Lesson("Lesson 5: Stack Operations","Learn PUSH and POP for stack manipulation.",
        ["MOV","PUSH","POP"],"Push 100, pop to EBX.","PUSH 100 then POP ebx","; Stack demo\n",None,None,60,3,
        "The stack is LIFO. PUSH decrements ESP by 4 and stores. POP loads and increments ESP. The stack is used for function calls, local variables, and expression evaluation."),
    Lesson("Lesson 6: Comparison","Use CMP to compare values and set flags.",
        ["MOV","CMP"],"Compare EAX=50 with 50. ZF should be 1.","CMP eax, 50","; Compare 50==50\nMOV eax, 50\n",None,{"ZF":1},60,3,
        "CMP subtracts without storing. ZF=1 means equal. CF=1 means borrow (below). SF indicates sign of result. CMP is the foundation of all conditional branching."),
    Lesson("Lesson 7: Increment/Decrement","INC and DEC: efficient +/- 1.",
        ["MOV","INC","DEC"],"Set EAX=0, INC to 1, DEC back to 0.","INC eax and DEC eax","; INC/DEC\nMOV eax, 0\n",0,None,45,3,
        "INC/DEC are compact and preserve CF. They update ZF, SF, OF, PF like ADD/SUB. On modern CPUs, ADD reg,1 is sometimes preferred due to better macro-fusion with Jcc."),
    Lesson("Lesson 8: Complex Calculation","Chain multiple instructions for real-world math.",
        ["MOV","ADD","SUB","SHL","AND"],"Calculate ((10+6)*2) & 0x1F. Result=0.","ADD, SHL 1, AND","; Complex calc\n",0,None,90,3,
        "Real calculations chain instructions. SHL is used as a fast multiply, AND for masking. Compilers chain these operations to implement complex expressions efficiently."),
    Lesson("Lesson 9: Negation","Use NEG for two's complement.",
        ["MOV","NEG"],"Negate 5. Result = -5 (0xFFFFFFFB).","NEG eax = 0 - eax","; Negate 5\nMOV eax, 5\n",0xFFFFFFFB,None,45,3,
        "NEG computes 0 - operand. If operand is 0, CF=0; otherwise CF=1. NEG of 0x80000000 overflows. It is used for computing absolute values and implementing subtraction via addition."),
    Lesson("Lesson 10: XOR Swap","Swap without temporary using XOR.",
        ["MOV","XOR"],"Swap EAX=7 and EBX=3. EAX should be 3.","XOR eax,ebx; XOR ebx,eax; XOR eax,ebx","; XOR swap\nMOV eax, 7\nMOV ebx, 3\n",3,None,90,3,
        "XOR swap: a^=b, b^=a, a^=b. Historically saved a register, but modern XCHG is faster. Still a classic interview question and demonstrates XOR properties."),
    Lesson("Lesson 11: Rotate Operations","Use ROL and ROR for bit rotation.",
        ["MOV","ROL","ROR"],"Rotate 0x12345678 left by 8 bits.","ROL eax, 8","; Rotate left 8\nMOV eax, 0x12345678\n",0x34567812,None,60,3,
        "Rotations preserve all bits - bits falling off one end appear on the other. Used in cryptography (RC5, RC6), hashing algorithms, and bit manipulation tricks."),
    Lesson("Lesson 12: Arithmetic Shift","SAR for signed division by powers of 2.",
        ["MOV","SAR"],"SAR -16 (0xFFFFFFF0) by 2. Result=-4.","SAR preserves sign bit","; SAR divide\nMOV eax, 0xFFFFFFF0\n",0xFFFFFFFC,None,75,3,
        "SAR fills vacated bits with the sign bit (arithmetic shift). SHR fills with zeros (logical shift). Using the wrong one is a common source of bugs with negative numbers."),
    Lesson("Lesson 13: Carry Flag Ops","CLC, STC, ADC for multi-word arithmetic.",
        ["CLC","STC","CMC","ADC"],"STC, then ADD 5+3+CF=9.","STC then ADC","; ADC demo\nMOV eax, 5\n",9,None,90,3,
        "ADC is essential for 64-bit math on 32-bit CPUs: ADD low dword, ADC high dword. The carry from the lower addition propagates to the upper addition automatically via CF."),
    Lesson("Lesson 14: Conditional Jumps","Implement branching logic with CMP + Jcc.",
        ["MOV","CMP","JG","JL","JMP"],"If EAX=10 > EBX=5, set EAX=1, else 0.","CMP then JG","; Conditional\nMOV eax, 10\nMOV ebx, 5\n",1,None,120,3,
        "JG/JL are for signed, JA/JB for unsigned. Using the wrong one is a common bug! CMP sets flags, and Jcc reads those flags to decide whether to branch."),
    Lesson("Lesson 15: Signed Multiply","IMUL for signed multiplication.",
        ["MOV","IMUL","NEG"],"Calculate (-5)*7 = -35.","NEG then IMUL","; IMUL\nMOV eax, 5\n",0xFFFFFFDD,None,120,3,
        "IMUL preserves sign. Two-operand form stores truncated result. Overflow indicated by OF. IMUL has one, two, and three operand forms - the two/three operand forms are most commonly used by compilers."),
    Lesson("Lesson 16: Division","DIV for unsigned division with remainder.",
        ["MOV","DIV"],"Divide 100 by 7. EAX=quotient(14).","Clear EDX first!","; DIV 100/7\nMOV eax, 100\nMOV edx, 0\n",14,None,90,3,
        "DIV divides EDX:EAX by operand. EAX=quotient, EDX=remainder. Always clear EDX first (XOR edx,edx)! Division by zero causes an exception. DIV is one of the slowest integer instructions."),
    Lesson("Lesson 17: TEST Instruction","TEST to check individual bits.",
        ["MOV","TEST"],"Set EAX=0x0F, TEST with 1. ZF should be 0.","TEST eax, 1","; TEST bit 0\nMOV eax, 0x0F\n",None,{"ZF":0},75,3,
        "TEST = AND without storing. Standard way to check bits. TEST eax,eax checks for zero. TEST eax,1 checks if the number is odd. TEST is preferred over CMP reg,0 because it has a shorter encoding."),
    Lesson("Lesson 18: Loop Pattern","Implement a countdown loop.",
        ["MOV","DEC","CMP","JNE","JMP"],"Count from 5 to 0. EAX=0.","Loop: DEC, CMP 0, JNE back","; Countdown\nMOV eax, 5\n",0,None,120,3,
        "Loops use labels + conditional jumps. Pattern: init, test, body, adjust, jump back. This is the fundamental loop pattern that compilers generate for all counting loops."),
    Lesson("Lesson 19: Function Calls","CALL and RET for subroutines.",
        ["MOV","CALL","RET","PUSH","POP"],"CALL a subroutine that doubles EAX. Start 21, end 42.","CALL label, RET to return","; Function call\nMOV eax, 21\n",42,None,150,3,
        "CALL pushes return address and jumps. RET pops and jumps back. Basis of all function calls. The call stack enables recursion by saving return addresses at each nesting level."),
    Lesson("Lesson 20: Final Challenge","Combine loops, arithmetic, conditionals.",
        ["MOV","ADD","CMP","JLE","JMP","INC"],"Sum 1 to 10. EAX should be 55.","Loop with counter in ECX","; Sum 1..10\nMOV eax, 0\n",55,None,180,3,
        "This combines everything: loop initialization, accumulation, conditional exit. Congratulations! You have mastered the fundamentals of x86 assembly programming."),
    Lesson("Lesson 21: Population Count","Count the number of set bits (1-bits) in a register.",
        ["MOV","SHR","AND","ADD","JNE","JMP"],"Count bits in 0xFF (255). EAX should be 8.",
        "Loop: SHR, AND 1, ADD to count, JNE if still bits remain.",
        "; Popcount of 0xFF (should be 8)\nMOV eax, 0xFF\n",
        8, None, 120, 4,
        "Population count (popcount) counts the number of 1-bits. It's used in cryptography, error detection, and hash functions. Modern CPUs have a POPCNT instruction for this."),
    Lesson("Lesson 22: Bit Reversal","Reverse all 32 bits of a register.",
        ["MOV","SHL","SHR","OR","AND","DEC","CMP","JNE","JMP"],"Reverse 0x80000001 to get 0x10000080.",
        "Loop 32 times: shift src right, shift dst left, OR the bit, AND mask.",
        "; Reverse bits of 0x80000001\nMOV eax, 0x80000001\n",
        0x10000080, None, 180, 5,
        "Bit reversal is essential in FFT algorithms, CRC calculations, and some cryptographic operations."),
    Lesson("Lesson 23: Maximum of Two Numbers","Find the larger of two signed numbers.",
        ["MOV","CMP","JG","JMP"],"Given EAX=25, EBX=42, set EAX to the larger value (42).",
        "CMP eax, ebx then JG to skip the swap.",
        "; Find max of 25 and 42\nMOV eax, 25\nMOV ebx, 42\n",
        42, None, 90, 3,
        "Finding the maximum is a fundamental building block used in sorting, searching, and many algorithms."),
    Lesson("Lesson 24: Minimum of Three Numbers","Find the smallest of three values.",
        ["MOV","CMP","JLE","JMP"],"Find min of EAX=30, EBX=15, ECX=22. EAX should be 15.",
        "Compare EAX vs EBX, keep smaller, then compare with ECX.",
        "; Min of 30, 15, 22\nMOV eax, 30\nMOV ebx, 15\nMOV ecx, 22\n",
        15, None, 120, 4,
        "Finding the minimum of N values is done by iterating pairwise. This pattern extends to any N and is the basis of selection sort."),
    Lesson("Lesson 25: Factorial (Recursive)","Compute factorial using recursive CALL.",
        ["MOV","CMP","JLE","PUSH","CALL","RET","POP","IMUL"],"Compute 5! = 120. EAX should be 120.",
        "Factorial function: if n<=1 return 1, else CALL self with n-1, IMUL result.",
        "; Factorial of 5\nMOV eax, 5\nCALL factorial\nJMP end\n",
        120, None, 240, 5,
        "Factorial is the classic recursion example. Each CALL pushes a return address. The base case stops recursion. As returns unwind, each level multiplies."),
    Lesson("Lesson 26: Fibonacci Sequence","Compute F(10) = 55 iteratively.",
        ["MOV","ADD","DEC","CMP","JG","JMP"],"Compute the 10th Fibonacci number. EAX should be 55.",
        "Iterative: track prev and curr, add them each step, count down.",
        "; Fibonacci(10) = 55\n; F(1)=1, F(2)=1\nMOV eax, 0\n",
        55, None, 180, 4,
        "The Fibonacci sequence appears everywhere in nature and CS. The iterative approach is O(n) time and O(1) space."),
    Lesson("Lesson 27: Power Function","Compute 2^10 = 1024.",
        ["MOV","IMUL","DEC","CMP","JG","JMP"],"Compute 2^10 = 1024. EAX should be 1024.",
        "Loop: multiply accumulator by base, decrement exponent.",
        "; 2^10 = 1024\nMOV eax, 1\n",
        1024, None, 150, 4,
        "Power function is fundamental in mathematics and cryptography. Real implementations use binary exponentiation for O(log n) performance."),
    Lesson("Lesson 28: GCD (Euclidean Algorithm)","Find GCD of 48 and 18. Result=6.",
        ["MOV","CMP","JE","JL","SUB","JMP"],"Find GCD of 48 and 18. EAX should be 6.",
        "Loop: if a==b, done. If a>b, a-=b. Else b-=a.",
        "; GCD(48, 18) = 6\nMOV eax, 48\nMOV ebx, 18\n",
        6, None, 180, 4,
        "The Euclidean algorithm is one of the oldest algorithms (300 BCE). GCD is used for reducing fractions and cryptographic key generation."),
    Lesson("Lesson 29: Modulo Without DIV","Compute 100 mod 7 = 2.",
        ["MOV","CMP","JL","SUB","JMP"],"Compute 100 mod 7. EAX should be 2.",
        "Loop: if eax < divisor, done. Else subtract divisor and repeat.",
        "; 100 mod 7 = 2\nMOV eax, 100\n",
        2, None, 150, 4,
        "Modulo can be computed without DIV by repeated subtraction. For powers of 2, AND with (n-1) is much faster."),
    Lesson("Lesson 30: Array Sum","Sum first 5 even numbers = 30.",
        ["MOV","ADD","SHL","INC","CMP","JLE","JMP"],"Sum 2+4+6+8+10=30. EAX should be 30.",
        "Loop 5 times: compute value as (i+1)*2 using SHL or ADD, accumulate.",
        "; Sum of first 5 even numbers\nMOV eax, 0\n",
        30, None, 180, 4,
        "Array processing pattern: iterate with index, compute value, accumulate. Universal in array processing."),
    Lesson("Lesson 31: Bubble Sort Swap","Sort two values: 35 and 12.",
        ["MOV","CMP","JG","XCHG","DEC","JNE","JMP"],"After sorting EAX=12 (smaller).",
        "Compare EAX and EBX, if EAX > EBX, swap with XCHG.",
        "; Sort two values\nMOV eax, 35\nMOV ebx, 12\n",
        12, None, 120, 4,
        "Bubble sort repeatedly compares adjacent elements and swaps if wrong order. Time complexity: O(N^2)."),
    Lesson("Lesson 32: Linear Search","Search for value 7 in sequence 3,5,7,9.",
        ["MOV","CMP","JE","INC","DEC","JNE","JMP"],"Find 7. EAX should be 7 when found.",
        "Loop: compare current with target, if match jump to found.",
        "; Linear search for 7\nMOV eax, 3\n",
        7, None, 150, 3,
        "Linear search checks each element until target is found. O(n) on unsorted data."),
    Lesson("Lesson 33: Function Arguments","Pass args in registers, return sum.",
        ["MOV","PUSH","CALL","RET","POP","ADD"],"Pass EAX=10 and EBX=20. Return EAX=30.",
        "Pass args in EAX and EBX, CALL function, function adds, RET.",
        "; Function: add(EAX, EBX) -> EAX\nMOV eax, 10\nMOV ebx, 20\n",
        30, None, 180, 4,
        "Calling conventions define how functions receive arguments. In x86-64, first 6 args go in RDI,RSI,RDX,RCX,R8,R9."),
    Lesson("Lesson 34: Stack Frame","Save/restore registers around CALL.",
        ["MOV","PUSH","POP","CALL","RET","ADD"],"EAX should still be 99 after call.",
        "PUSH eax and ebx before CALL, POP in reverse after RET.",
        "; Stack frame demo\nMOV eax, 99\nMOV ebx, 77\n",
        99, None, 180, 4,
        "Stack frames save callee-saved registers (EBX, ESI, EDI, EBP). The prologue saves, epilogue restores."),
    Lesson("Lesson 35: Shift-and-Add Multiply","Multiply 9*13=117 using shifts.",
        ["MOV","SHL","SUB","ADD"],"Multiply EAX=9 by 13. Result=117.",
        "13 = 8+4+1 = (x<<3) + (x<<2) + x.",
        "; 9 * 13 = 117 via shift-add\nMOV eax, 9\n",
        117, None, 180, 5,
        "Compilers replace multiplications by constants with shifts and adds. Much faster than MUL (1-3 cycles vs 10+ cycles)."),
    Lesson("Lesson 36: State Machine","3-state FSM: state 1 adds 20.",
        ["MOV","CMP","JE","JMP","INC","ADD"],"State 1: EAX should be 20.",
        "CMP state with 0,1,2 and JMP to the right handler.",
        "; State machine: process state 1\nMOV eax, 0\n",
        20, None, 240, 5,
        "FSMs are used in parsers, network protocols, game AI, and hardware design. Each state has transitions based on input."),
    Lesson("Lesson 37: Absolute Value","Compute |EAX| for EAX=-15.",
        ["MOV","SAR","XOR","SUB"],"Compute |(-15)| = 15. EAX should be 15.",
        "SAR to get mask, XOR to flip, SUB to add 1.",
        "; Absolute value\nMOV eax, 0xFFFFFFF1\n",
        15, None, 120, 4,
        "Absolute value trick: cdq; xor eax,edx; sub eax,edx. This is branchless and commonly generated by compilers."),
    Lesson("Lesson 38: Multiplication by 7","Multiply EAX=11 by 7 = 77 using shifts.",
        ["MOV","SHL","SUB"],"Multiply 11*7=77.",
        "7 = 8-1 = (x<<3) - x.",
        "; 11 * 7 = 77\nMOV eax, 11\n",
        77, None, 120, 4,
        "x*7 = (x<<3) - x. Only 2 instructions vs 10+ for IMUL. Compilers always optimize constant multiplies."),
    Lesson("Lesson 39: Division by Shift","Divide 100 by 8 using SHR.",
        ["MOV","SHR"],"Divide 100/8=12 using SHR.",
        "SHR eax, 3 for unsigned /8.",
        "; 100 / 8 = 12\nMOV eax, 100\n",
        12, None, 90, 3,
        "Division by powers of 2 is a simple shift. For other constants, compilers use magic number multiplication + shift."),
    Lesson("Lesson 40: Grand Challenge","Sum of squares from 1 to 5 = 55.",
        ["MOV","ADD","IMUL","CMP","JLE","JMP","INC","DEC"],"Sum i^2 for i=1..5. EAX should be 55.",
        "Loop: multiply counter by itself, add to sum, increment, check.",
        "; Sum of squares: 1+4+9+16+25 = 55\nMOV eax, 0\n",
        55, None, 240, 5,
        "This combines loops, multiplication (via IMUL), accumulation, and conditional exit. You are now ready for real-world assembly programming!"),
]

# ============================================================
# CODE SNIPPETS
# ============================================================

CODE_SNIPPETS = [
    CodeSnippet("Hello World","Basic MOV","MOV eax, 42\n","Basics"),
    CodeSnippet("Add Two Numbers","ADD instruction","MOV eax, 10\nADD eax, 20\n; eax = 30\n","Arithmetic"),
    CodeSnippet("Multiply by Shift","SHL to multiply by 8","MOV eax, 5\nSHL eax, 3\n; eax = 40\n","Arithmetic"),
    CodeSnippet("Clear Register","Fastest zero: XOR","XOR eax, eax\n; eax = 0\n","Optimization"),
    CodeSnippet("Check if Zero","TEST for zero","TEST eax, eax\nJE is_zero\nJMP cont\nis_zero:\n; eax is 0\ncont:\n","Comparison"),
    CodeSnippet("If-Else","Conditional branching","CMP eax, ebx\nJG greater\nMOV eax, 0\nJMP done\ngreater:\nMOV eax, 1\ndone:\n","Control Flow"),
    CodeSnippet("Countdown Loop","Loop from N to 0","MOV ecx, 10\nloop_start:\nDEC ecx\nCMP ecx, 0\nJNE loop_start\n","Loops"),
    CodeSnippet("Sum 1 to N","Accumulate in loop","MOV eax, 0\nMOV ecx, 1\nsum_loop:\nADD eax, ecx\nINC ecx\nCMP ecx, 11\nJL sum_loop\n","Loops"),
    CodeSnippet("XOR Swap","Swap without temp","MOV eax, 7\nMOV ebx, 3\nXOR eax, ebx\nXOR ebx, eax\nXOR eax, ebx\n","Bitwise"),
    CodeSnippet("Bit Mask","Extract lower 4 bits","MOV eax, 0x3F\nAND eax, 0x0F\n; eax = 0x0F\n","Bitwise"),
    CodeSnippet("Stack Save/Restore","PUSH/POP pattern","PUSH eax\nPUSH ebx\n; ... work ...\nPOP ebx\nPOP eax\n","Stack"),
    CodeSnippet("Function Call","CALL/RET pattern","MOV eax, 5\nCALL double_it\nJMP end\ndouble_it:\nADD eax, eax\nRET\nend:\n","Functions"),
    CodeSnippet("Absolute Value","Compute |eax|","MOV ebx, eax\nSAR ebx, 31\nXOR eax, ebx\nSUB eax, ebx\n","Arithmetic"),
    CodeSnippet("Multiply by 7","Shift+add multiply","; eax * 7 = (eax<<3) - eax\nMOV ebx, eax\nSHL ebx, 3\nSUB ebx, eax\nMOV eax, ebx\n","Optimization"),
    CodeSnippet("Even/Odd","Test lowest bit","TEST eax, 1\nJE is_even\nJMP done\nis_even:\n; even\ndone:\n","Comparison"),
    CodeSnippet("Population Count","Count set bits in EAX","; Popcount: count 1-bits\nMOV ecx, 0\nMOV edx, eax\npop_loop:\nTEST edx, edx\nJE pop_done\nMOV ebx, edx\nAND ebx, 1\nADD ecx, ebx\nSHR edx, 1\nJMP pop_loop\npop_done:\nMOV eax, ecx\n","Algorithms"),
    CodeSnippet("Factorial (Recursive)","5! using recursive CALL","MOV eax, 5\nCALL factorial\nJMP end\nfactorial:\nPUSH eax\nCMP eax, 1\nJLE fact_base\nDEC eax\nCALL factorial\nPOP ebx\nIMUL eax, ebx\nRET\nfact_base:\nPOP eax\nMOV eax, 1\nRET\nend:\n","Functions"),
    CodeSnippet("Fibonacci (Iterative)","Compute F(10) = 55","; F(n) iterative\nMOV eax, 0\nMOV ebx, 1\nMOV ecx, 10\nfib_loop:\nMOV edx, eax\nADD edx, ebx\nMOV eax, ebx\nMOV ebx, edx\nDEC ecx\nCMP ecx, 1\nJG fib_loop\nMOV eax, ebx\n","Algorithms"),
    CodeSnippet("GCD (Euclidean)","GCD of two numbers","; GCD(a, b) by subtraction\nMOV eax, 48\nMOV ebx, 18\ngcd_loop:\nCMP eax, ebx\nJE gcd_done\nJL gcd_swap\nSUB eax, ebx\nJMP gcd_loop\ngcd_swap:\nXCHG eax, ebx\nJMP gcd_loop\ngcd_done:\n; eax = GCD = 6\n","Algorithms"),
    CodeSnippet("Power Function","base^exp by repeated mul","; Power: 2^10\nMOV eax, 1\nMOV ebx, 2\nMOV ecx, 10\npow_loop:\nIMUL eax, ebx\nDEC ecx\nCMP ecx, 0\nJG pow_loop\n; eax = 1024\n","Algorithms"),
    CodeSnippet("Max of Two","CMP + conditional jump","; max(a, b)\nMOV eax, 25\nMOV ebx, 42\nCMP eax, ebx\nJG skip_swap\nXCHG eax, ebx\nskip_swap:\n; eax = 42 (max)\n","Algorithms"),
    CodeSnippet("Modulo (no DIV)","100 mod 7 by subtraction","; a mod b\nMOV eax, 100\nMOV ebx, 7\nmod_loop:\nCMP eax, ebx\nJL mod_done\nSUB eax, ebx\nJMP mod_loop\nmod_done:\n; eax = 2\n","Arithmetic"),
    CodeSnippet("State Machine","3-state dispatcher","MOV esi, 1\nMOV eax, 0\nCMP esi, 0\nJE state_0\nCMP esi, 1\nJE state_1\nJMP state_2\nstate_0:\nADD eax, 10\nJMP sm_done\nstate_1:\nADD eax, 20\nJMP sm_done\nstate_2:\nADD eax, 30\nJMP sm_done\nsm_done:\n","Control Flow"),
    CodeSnippet("Bit Reversal","Reverse all 32 bits","MOV ebx, 0\nMOV ecx, 32\nrev_loop:\nSHR eax, 1\nADC ebx, ebx\nDEC ecx\nCMP ecx, 0\nJG rev_loop\nMOV eax, ebx\n","Bitwise"),
    CodeSnippet("Division by Shift","Divide by 8 via SHR","; Unsigned divide by 8\nMOV eax, 100\nSHR eax, 3\n; eax = 12\n","Optimization"),
    CodeSnippet("Sum of Squares","Sum i^2 for i=1..5","MOV eax, 0\nMOV ecx, 1\nsq_loop:\nMOV edx, ecx\nIMUL edx, ecx\nADD eax, edx\nINC ecx\nCMP ecx, 6\nJL sq_loop\n; eax = 55\n","Algorithms"),
]

# ============================================================
# SESSION STATISTICS
# ============================================================

class SessionStats:
    def __init__(self):
        self.start_time = datetime.now()
        self.total_instructions = 0; self.total_errors = 0
        self.lessons_completed = 0; self.challenges_won = 0; self.total_stars = 0
        self.files_saved = 0; self.files_loaded = 0
        self.instructions_used: Dict[str,int] = {}
        self.lesson_history: List[Dict] = []
    def record_execution(self, opcode: str, success: bool):
        self.total_instructions += 1
        if not success: self.total_errors += 1
        self.instructions_used[opcode.upper()] = self.instructions_used.get(opcode.upper(), 0) + 1
    def record_lesson(self, idx: int, stars: int = 0, time_taken: float = 0):
        self.lessons_completed += 1
        self.lesson_history.append({"lesson":idx,"stars":stars,"time":time_taken,"ts":datetime.now().isoformat()})
    def record_challenge(self, stars: int):
        self.challenges_won += 1; self.total_stars += stars
    def to_dict(self) -> Dict:
        e = (datetime.now() - self.start_time).total_seconds()
        return {"duration":f"{int(e//60)}m {int(e%60)}s","instructions":self.total_instructions,
            "errors":self.total_errors,"accuracy":f"{(1-self.total_errors/max(1,self.total_instructions))*100:.1f}%",
            "lessons":self.lessons_completed,"challenges":self.challenges_won,"stars":self.total_stars,
            "unique_ops":len(self.instructions_used),
            "most_used":max(self.instructions_used.items(),key=lambda x:x[1])[0] if self.instructions_used else "N/A"}

# ============================================================
# VIRTUAL CPU
# ============================================================

class VirtualCPU:
    def __init__(self):
        self.registers: Dict[str,Register] = {
            "eax":Register("eax",RegisterSize.DWORD),"ebx":Register("ebx",RegisterSize.DWORD),
            "ecx":Register("ecx",RegisterSize.DWORD),"edx":Register("edx",RegisterSize.DWORD),
            "esi":Register("esi",RegisterSize.DWORD),"edi":Register("edi",RegisterSize.DWORD),
            "esp":Register("esp",RegisterSize.DWORD,0x7FFF0000),
            "ebp":Register("ebp",RegisterSize.DWORD,0x7FFF0000),
            "eip":Register("eip",RegisterSize.DWORD),
        }
        self.flags: Dict[str,Register] = {
            "ZF":Register("ZF",RegisterSize.BYTE,0,True),"SF":Register("SF",RegisterSize.BYTE,0,True),
            "CF":Register("CF",RegisterSize.BYTE,0,True),"OF":Register("OF",RegisterSize.BYTE,0,True),
            "PF":Register("PF",RegisterSize.BYTE,0,True),"DF":Register("DF",RegisterSize.BYTE,0,True),
        }
        self.memory: Dict[int,MemoryCell] = {}
        self.stack: List[int] = []; self.labels: Dict[str,int] = {}
        self.program: List[str] = []; self.current_line: int = 0
        self.execution_history: List[ExecutionRecord] = []; self.total_cycles: int = 0
        self.call_stack: List[int] = []; self.breakpoints: Dict[int,Breakpoint] = {}
        self.max_steps: int = 10000; self.running: bool = False

    def reset(self):
        for n,r in self.registers.items():
            r.value = 0x7FFF0000 if n in ("esp","ebp") else 0; r.history.clear()
        for f in self.flags.values(): f.value = 0
        self.memory.clear(); self.stack.clear(); self.labels.clear(); self.program.clear()
        self.current_line = 0; self.execution_history.clear(); self.total_cycles = 0
        self.call_stack.clear(); self.running = False

    def load_program(self, code: str):
        self.reset(); self.program = code.split("\n"); self.labels = {}
        for i, line in enumerate(self.program):
            s = line.strip()
            if not s or s.startswith(";"): continue
            if ";" in s: s = s[:s.index(";")].strip()
            if ":" in s:
                lp = s.split(":")[0].strip()
                if lp and lp.replace("_","").isalnum(): self.labels[lp.lower()] = i

    def get_state_snapshot(self) -> Dict:
        return {"registers":{k:v.value for k,v in self.registers.items()},
            "flags":{k:v.value for k,v in self.flags.items()},"stack":list(self.stack),
            "esp":self.registers["esp"].value,"cycles":self.total_cycles,"line":self.current_line}

    def restore_state(self, snap: Dict):
        for n,v in snap.get("registers",{}).items():
            if n in self.registers: self.registers[n].value = v
        for n,v in snap.get("flags",{}).items():
            if n in self.flags: self.flags[n].value = v
        self.stack = list(snap.get("stack",[])); self.total_cycles = snap.get("cycles",0)
        self.current_line = snap.get("line",0)

    def parse_value(self, op: str) -> Tuple[int,bool]:
        op = op.strip().lower()
        if op in self.registers: return self.registers[op].value, True
        if op.startswith("0x"): return int(op,16), False
        if op.startswith("0b"): return int(op,2), False
        try: return int(op), False
        except ValueError: pass
        if op in self.labels: return self.labels[op], False
        raise ValueError(f"Unknown operand: {op}")

    def set_operand(self, op: str, val: int):
        op = op.strip().lower()
        if op in self.registers: self.registers[op].set_value(val)
        else: raise ValueError(f"Cannot write to '{op}'")

    def update_flags_arith(self, result: int, size=32, carry=False, overflow=False):
        mask = (1<<size)-1; sm = 1<<(size-1)
        self.flags["ZF"].value = 1 if (result&mask)==0 else 0
        self.flags["SF"].value = 1 if (result&sm)!=0 else 0
        self.flags["CF"].value = 1 if carry else 0
        self.flags["OF"].value = 1 if overflow else 0
        parity = sum(1 for i in range(8) if ((result&mask)>>i)&1)
        self.flags["PF"].value = 1 if parity%2==0 else 0

    def update_flags_logical(self, result: int, size=32):
        self.flags["CF"].value = 0; self.flags["OF"].value = 0
        mask = (1<<size)-1; self.flags["ZF"].value = 1 if (result&mask)==0 else 0
        self.flags["SF"].value = 1 if (result&mask)&(1<<(size-1)) else 0
        parity = sum(1 for i in range(8) if ((result&mask)>>i)&1)
        self.flags["PF"].value = 1 if parity%2==0 else 0

    def _get_jump_target(self, target: str) -> int:
        t = target.strip().lower()
        if t in self.labels: return self.labels[t]
        try: return int(t)-1
        except: pass
        raise ValueError(f"Unknown target: '{target}'")

    def _signed32(self, v): return v-0x100000000 if v&0x80000000 else v

    def execute_line(self, line: str) -> Tuple[str, int, Optional[int]]:
        line = line.strip()
        if not line or line.startswith(";"): return ("Skipped",0,None)
        if ";" in line: line = line[:line.index(";")].strip()
        if not line: return ("Skipped",0,None)
        if ":" in line and not any(line.upper().startswith(op) for op in INSTRUCTION_DB):
            return ("Label",0,None)
        parts = re.split(r"[\s,]+", line); parts = [p for p in parts if p]
        if not parts: return ("Empty",0,None)
        opcode = JUMP_ALIASES.get(parts[0].upper(), parts[0].upper())
        operands = parts[1:]
        return self._exec(opcode, operands)

    def _exec(self, op: str, ops: List[str]) -> Tuple[str,int,Optional[int]]:
        cyc = INSTRUCTION_DB[op].cycles if op in INSTRUCTION_DB else 1
        if op=="NOP": return ("NOP",cyc,None)
        elif op=="MOV":
            sv,_=self.parse_value(ops[1]); self.set_operand(ops[0],sv)
            return (f"MOV: {ops[0]} = {sv}",cyc,None)
        elif op=="MOVSX":
            sv,_=self.parse_value(ops[1])
            if sv&0x80: sv|=0xFFFFFF00
            self.set_operand(ops[0],sv); return (f"MOVSX: {ops[0]} = {sv&0xFFFFFFFF}",cyc,None)
        elif op=="MOVZX":
            sv,_=self.parse_value(ops[1]); self.set_operand(ops[0],sv&0xFF)
            return (f"MOVZX: {ops[0]} = {sv&0xFF}",cyc,None)
        elif op=="XCHG":
            v1,_=self.parse_value(ops[0]); v2,_=self.parse_value(ops[1])
            self.set_operand(ops[0],v2); self.set_operand(ops[1],v1)
            return (f"XCHG: swapped",cyc,None)
        elif op=="ADD":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1]); r=dv+sv
            c=r>0xFFFFFFFF; o=((dv>>31)==(sv>>31))and((r>>31)!=(dv>>31))
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,c,o)
            return (f"ADD: {ops[0]} = {dv} + {sv} = {r&0xFFFFFFFF}",cyc,None)
        elif op=="SUB":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1]); r=dv-sv
            c=dv<sv; o=((dv>>31)!=(sv>>31))and(((r>>31)&1)!=(dv>>31))
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,c,o)
            return (f"SUB: {ops[0]} = {dv} - {sv} = {r&0xFFFFFFFF}",cyc,None)
        elif op=="MUL":
            sv,_=self.parse_value(ops[0]); eax=self.registers["eax"].value; r=eax*sv
            hi=(r>>32)&0xFFFFFFFF; self.registers["edx"].set_value(hi); self.registers["eax"].set_value(r&0xFFFFFFFF)
            self.update_flags_arith(r,32,hi!=0,hi!=0)
            return (f"MUL: EDX:EAX = {eax}*{sv} (EAX=0x{r&0xFFFFFFFF:08x})",cyc,None)
        elif op=="DIV":
            sv,_=self.parse_value(ops[0])
            if sv==0: raise RuntimeError("Division by zero!")
            divd=(self.registers["edx"].value<<32)|self.registers["eax"].value
            q=divd//sv; rem=divd%sv
            self.registers["eax"].set_value(q); self.registers["edx"].set_value(rem)
            return (f"DIV: EAX={q}, EDX={rem}",cyc,None)
        elif op=="IMUL":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1])
            r=self._signed32(dv)*self._signed32(sv)
            self.set_operand(ops[0],r); o=r<-0x80000000 or r>0x7FFFFFFF
            self.update_flags_arith(r,32,o,o)
            return (f"IMUL: {ops[0]} = {self._signed32(dv)}*{self._signed32(sv)} = {self._signed32(r&0xFFFFFFFF)}",cyc,None)
        elif op=="IDIV":
            sv,_=self.parse_value(ops[0])
            if sv==0: raise RuntimeError("Division by zero!")
            divd=(self._signed32(self.registers["edx"].value)<<32)|self.registers["eax"].value
            ssv=self._signed32(sv); q=int(divd/ssv) if (divd<0)!=(ssv<0) and divd%ssv!=0 else divd//ssv
            rem=divd-q*ssv; self.registers["eax"].set_value(q); self.registers["edx"].set_value(rem)
            return (f"IDIV: EAX={q}, EDX={rem}",cyc,None)
        elif op=="INC":
            v,_=self.parse_value(ops[0]); r=v+1; ocf=self.flags["CF"].value
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,False,False)
            self.flags["CF"].value=ocf; return (f"INC: {ops[0]} = {r&0xFFFFFFFF}",cyc,None)
        elif op=="DEC":
            v,_=self.parse_value(ops[0]); r=v-1; ocf=self.flags["CF"].value
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,False,False)
            self.flags["CF"].value=ocf; return (f"DEC: {ops[0]} = {r&0xFFFFFFFF}",cyc,None)
        elif op=="NEG":
            v,_=self.parse_value(ops[0]); r=(-v)&0xFFFFFFFF
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,v!=0,v==0x80000000)
            return (f"NEG: {ops[0]} = {r}",cyc,None)
        elif op=="ADC":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1]); cf=self.flags["CF"].value
            r=dv+sv+cf; c=r>0xFFFFFFFF
            o=((dv>>31)==(sv>>31))and((r>>31)!=(dv>>31))
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,c,o)
            return (f"ADC: {ops[0]} = {dv}+{sv}+{cf} = {r&0xFFFFFFFF}",cyc,None)
        elif op=="SBB":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1]); cf=self.flags["CF"].value
            r=dv-sv-cf; c=dv<(sv+cf)
            o=((dv>>31)!=(sv>>31))and(((r>>31)&1)!=(dv>>31))
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,c,o)
            return (f"SBB: {ops[0]} = {dv}-{sv}-{cf} = {r&0xFFFFFFFF}",cyc,None)
        elif op=="AND":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1]); r=dv&sv
            self.set_operand(ops[0],r); self.update_flags_logical(r)
            return (f"AND: {ops[0]} = {dv} & {sv} = {r}",cyc,None)
        elif op=="OR":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1]); r=dv|sv
            self.set_operand(ops[0],r); self.update_flags_logical(r)
            return (f"OR: {ops[0]} = {dv} | {sv} = {r}",cyc,None)
        elif op=="XOR":
            dv,_=self.parse_value(ops[0]); sv,_=self.parse_value(ops[1]); r=dv^sv
            self.set_operand(ops[0],r); self.update_flags_logical(r)
            return (f"XOR: {ops[0]} = {dv} ^ {sv} = {r}",cyc,None)
        elif op=="NOT":
            v,_=self.parse_value(ops[0]); r=(~v)&0xFFFFFFFF; self.set_operand(ops[0],r)
            return (f"NOT: {ops[0]} = {r}",cyc,None)
        elif op=="SHL":
            dv,_=self.parse_value(ops[0]); cn,_=self.parse_value(ops[1]); cn&=0x1F
            if cn==0: return ("SHL: count=0",cyc,None)
            c=((dv<<(cn-1))&0x80000000)!=0; r=(dv<<cn)&0xFFFFFFFF
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,c,False)
            return (f"SHL: {ops[0]} = {dv} << {cn} = {r}",cyc,None)
        elif op=="SHR":
            dv,_=self.parse_value(ops[0]); cn,_=self.parse_value(ops[1]); cn&=0x1F
            if cn==0: return ("SHR: count=0",cyc,None)
            c=((dv>>(cn-1))&1)!=0; r=dv>>cn
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,c,False)
            return (f"SHR: {ops[0]} = {dv} >> {cn} = {r}",cyc,None)
        elif op=="SAR":
            dv,_=self.parse_value(ops[0]); cn,_=self.parse_value(ops[1]); cn&=0x1F
            if cn==0: return ("SAR: count=0",cyc,None)
            sb=dv&0x80000000; r=dv>>cn
            if sb: r|=(0xFFFFFFFF<<(32-cn))&0xFFFFFFFF
            c=((dv>>(cn-1))&1)!=0
            self.set_operand(ops[0],r); self.update_flags_arith(r,32,c,False)
            return (f"SAR: {ops[0]} = {dv} SAR {cn} = {r&0xFFFFFFFF}",cyc,None)
        elif op=="ROL":
            dv,_=self.parse_value(ops[0]); cn,_=self.parse_value(ops[1]); cn=(cn&0x1F)%32
            if cn==0: return ("ROL: count=0",cyc,None)
            r=((dv<<cn)|(dv>>(32-cn)))&0xFFFFFFFF
            self.set_operand(ops[0],r); self.flags["CF"].value=1 if r&1 else 0
            return (f"ROL: {ops[0]} = {r}",cyc,None)
        elif op=="ROR":
            dv,_=self.parse_value(ops[0]); cn,_=self.parse_value(ops[1]); cn=(cn&0x1F)%32
            if cn==0: return ("ROR: count=0",cyc,None)
            r=((dv>>cn)|(dv<<(32-cn)))&0xFFFFFFFF
            self.set_operand(ops[0],r); self.flags["CF"].value=1 if r&0x80000000 else 0
            return (f"ROR: {ops[0]} = {r}",cyc,None)
        elif op=="CMP":
            o1,_=self.parse_value(ops[0]); o2,_=self.parse_value(ops[1]); r=o1-o2
            c=o1<o2; o=((o1>>31)!=(o2>>31))and(((r>>31)&1)!=(o1>>31))
            self.update_flags_arith(r,32,c,o)
            return (f"CMP: {o1}-{o2} (ZF={self.flags['ZF'].value} SF={self.flags['SF'].value} CF={self.flags['CF'].value})",cyc,None)
        elif op=="TEST":
            o1,_=self.parse_value(ops[0]); o2,_=self.parse_value(ops[1]); r=o1&o2
            self.update_flags_logical(r)
            return (f"TEST: {o1} & {o2} = {r} (ZF={self.flags['ZF'].value})",cyc,None)
        elif op=="JMP":
            t=self._get_jump_target(ops[0]); return (f"JMP -> line {t+1}",cyc,t)
        elif op in ("JE","JNE","JG","JL","JA","JB","JGE","JLE","JAE","JBE","JS","JNS"):
            t=self._get_jump_target(ops[0]); ZF=self.flags["ZF"].value; SF=self.flags["SF"].value
            CF=self.flags["CF"].value; OF=self.flags["OF"].value; j=False
            if op=="JE":j=ZF==1
            elif op=="JNE":j=ZF==0
            elif op=="JG":j=ZF==0 and SF==OF
            elif op=="JL":j=SF!=OF
            elif op=="JA":j=CF==0 and ZF==0
            elif op=="JB":j=CF==1
            elif op=="JGE":j=SF==OF
            elif op=="JLE":j=ZF==1 or SF!=OF
            elif op=="JAE":j=CF==0
            elif op=="JBE":j=CF==1 or ZF==1
            elif op=="JS":j=SF==1
            elif op=="JNS":j=SF==0
            s="taken" if j else "not taken"
            return (f"{op}: {s}" + (f" -> line {t+1}" if j else ""),cyc,t if j else None)
        elif op=="PUSH":
            v,_=self.parse_value(ops[0]); self.stack.append(v&0xFFFFFFFF)
            self.registers["esp"].value=(self.registers["esp"].value-4)&0xFFFFFFFF
            return (f"PUSH: {v} (ESP={self.registers['esp'].get_hex()})",cyc,None)
        elif op=="POP":
            if not self.stack: raise RuntimeError("Stack underflow!")
            v=self.stack.pop(); self.registers["esp"].value=(self.registers["esp"].value+4)&0xFFFFFFFF
            self.set_operand(ops[0],v)
            return (f"POP: {v} -> {ops[0]}",cyc,None)
        elif op=="PUSHF":
            fv=self.flags["CF"].value|(self.flags["PF"].value<<2)|(self.flags["ZF"].value<<6)|(self.flags["SF"].value<<7)|(self.flags["DF"].value<<10)|(self.flags["OF"].value<<11)
            self.stack.append(fv&0xFFFF); self.registers["esp"].value=(self.registers["esp"].value-4)&0xFFFFFFFF
            return (f"PUSHF: 0x{fv&0xFFFF:04x}",cyc,None)
        elif op=="POPF":
            if not self.stack: raise RuntimeError("Stack underflow!")
            fv=self.stack.pop(); self.registers["esp"].value=(self.registers["esp"].value+4)&0xFFFFFFFF
            self.flags["CF"].value=(fv>>0)&1; self.flags["PF"].value=(fv>>2)&1
            self.flags["ZF"].value=(fv>>6)&1; self.flags["SF"].value=(fv>>7)&1
            self.flags["DF"].value=(fv>>10)&1; self.flags["OF"].value=(fv>>11)&1
            return ("POPF: flags restored",cyc,None)
        elif op=="CALL":
            self.call_stack.append(self.current_line+1); t=self._get_jump_target(ops[0])
            return (f"CALL '{ops[0]}' -> line {t+1}",cyc,t)
        elif op=="RET":
            if self.call_stack: ra=self.call_stack.pop(); return (f"RET -> line {ra+1}",cyc,ra)
            return ("RET: empty call stack",cyc,None)
        elif op=="LEA":
            src=ops[1]
            if "[" in src and "]" in src:
                expr=src[src.index("[")+1:src.index("]")]; total=0
                for p in re.split(r"([+-])",expr):
                    p=p.strip()
                    if not p or p in "+-": continue
                    if p.lower() in self.registers: total+=self.registers[p.lower()].value
                    else:
                        try: total+=int(p,16) if p.startswith("0x") else int(p)
                        except: pass
                self.set_operand(ops[0],total); return (f"LEA: {ops[0]} = {total}",cyc,None)
            else:
                v,_=self.parse_value(src); self.set_operand(ops[0],v); return (f"LEA: {ops[0]} = {v}",cyc,None)
        elif op=="CLC": self.flags["CF"].value=0; return ("CLC: CF=0",cyc,None)
        elif op=="STC": self.flags["CF"].value=1; return ("STC: CF=1",cyc,None)
        elif op=="CMC": self.flags["CF"].value=1-self.flags["CF"].value; return (f"CMC: CF={self.flags['CF'].value}",cyc,None)
        elif op=="CLD": self.flags["DF"].value=0; return ("CLD: DF=0",cyc,None)
        elif op=="STD": self.flags["DF"].value=1; return ("STD: DF=1",cyc,None)
        else: raise ValueError(f"Unknown opcode: {op}")

# ============================================================
# PSEUDOCODE TRANSLATOR
# ============================================================

class PseudocodeTranslator:
    @staticmethod
    def translate(code: str) -> str:
        lines = code.strip().split("\n"); out = []
        for line in lines:
            s = line.strip()
            if not s: continue
            if s.startswith(";"): out.append(f"  // {s[1:].strip()}"); continue
            if ";" in s: s = s[:s.index(";")].strip()
            if not s: continue
            if ":" in s:
                lbl = s.split(":")[0].strip(); rest = s.split(":",1)[1].strip()
                out.append(f"\n# {lbl}:")
                if rest: s = rest
                else: continue
            parts = re.split(r"[\s,]+", s); parts = [p for p in parts if p]
            if not parts: continue
            op = JUMP_ALIASES.get(parts[0].upper(), parts[0].upper()); ops = parts[1:]
            out.append(PseudocodeTranslator._line(op, ops))
        return "\n".join(out)

    @staticmethod
    def _line(op, ops):
        m = {"MOV":f"{ops[0]} = {ops[1]}","ADD":f"{ops[0]} += {ops[1]}","SUB":f"{ops[0]} -= {ops[1]}",
            "MUL":f"EDX:EAX = EAX * {ops[0]}","DIV":f"EAX = EDX:EAX // {ops[0]}, EDX = rem",
            "IMUL":f"{ops[0]} *= {ops[1]} (signed)","INC":f"{ops[0]} += 1","DEC":f"{ops[0]} -= 1",
            "NEG":f"{ops[0]} = -{ops[0]}","AND":f"{ops[0]} &= {ops[1]}","OR":f"{ops[0]} |= {ops[1]}",
            "XOR":f"{ops[0]} ^= {ops[1]}","NOT":f"{ops[0]} = ~{ops[0]}","SHL":f"{ops[0]} <<= {ops[1]}",
            "SHR":f"{ops[0]} >>= {ops[1]} (unsigned)","SAR":f"{ops[0]} >>= {ops[1]} (signed)",
            "CMP":f"# compare: {ops[0]} vs {ops[1]}","TEST":f"# test: {ops[0]} & {ops[1]}",
            "JMP":f"goto {ops[0]}","JE":f"if ZF==1: goto {ops[0]}","JNE":f"if ZF==0: goto {ops[0]}",
            "JG":f"if signed_greater: goto {ops[0]}","JL":f"if signed_less: goto {ops[0]}",
            "JA":f"if unsigned_above: goto {ops[0]}","JB":f"if unsigned_below: goto {ops[0]}",
            "PUSH":f"stack.push({ops[0]})","POP":f"{ops[0]} = stack.pop()",
            "CALL":f"call {ops[0]}()","RET":"return","NOP":"pass","LEA":f"{ops[0]} = &{ops[1]}"}
        if op in m: return m[op]
        if op in ("JGE","JLE","JAE","JBE","JS","JNS"): return f"if {op}: goto {ops[0]}"
        return f"# {op} {', '.join(ops)}"# SYNTAX HIGHLIGHTER
class AssemblyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent); self._setup()
    def _setup(self):
        self.fmt = {}
        def f(color, bold=False, italic=False):
            fm = QTextCharFormat(); fm.setForeground(QColor(Theme.get(color)))
            if bold: fm.setFontWeight(QFont.Weight.Bold)
            if italic: fm.setFontItalic(True)
            return fm
        self.fmt["opcode"] = f("accent_blue", True)
        self.fmt["register"] = f("accent_cyan")
        self.fmt["number"] = f("accent_green")
        self.fmt["comment"] = f("fg_muted", italic=True)
        self.fmt["label"] = f("accent_purple", True)
        self.fmt["directive"] = f("accent_yellow")
        self.rules = []
        ops = "|".join(list(INSTRUCTION_DB.keys()) + list(JUMP_ALIASES.keys()))
        self.rules.append((QRegularExpression(r"\b("+ops+r")\b", QRegularExpression.PatternOption.CaseInsensitiveOption), "opcode"))
        regs = "eax|ebx|ecx|edx|esi|edi|esp|ebp|eip|ax|bx|cx|dx|si|di|sp|bp|al|ah|bl|bh|cl|ch|dl|dh"
        self.rules.append((QRegularExpression(r"\b("+regs+r")\b", QRegularExpression.PatternOption.CaseInsensitiveOption), "register"))
        self.rules.append((QRegularExpression(r"\b0x[0-9a-fA-F]+\b"), "number"))
        self.rules.append((QRegularExpression(r"\b0b[01]+\b"), "number"))
        self.rules.append((QRegularExpression(r"\b\d+\b"), "number"))
        self.rules.append((QRegularExpression(r"^\s*[a-zA-Z_]\w*\s*(?=:)"), "label"))
        self.rules.append((QRegularExpression(r"\.(section|text|data|bss|global|extern|equ|db|dw|dd|dq)\b"), "directive"))

    def rehighlight(self):
        self._setup(); super().rehighlight()

    def highlightBlock(self, text):
        ci = text.find(";")
        if ci >= 0:
            self.setFormat(ci, len(text)-ci, self.fmt["comment"])
            text = text[:ci]
        for pat, name in self.rules:
            it = pat.globalMatch(text)
            while it.hasNext():
                m = it.next()
                if ci < 0 or m.capturedStart() < ci:
                    self.setFormat(m.capturedStart(), m.capturedLength(), self.fmt[name])

# CODE EDITOR WITH LINE NUMBERS, BREAKPOINTS, AUTOCOMPLETE
class LineNumberArea(QWidget):
    def __init__(self, editor): super().__init__(editor); self.editor = editor
    def sizeHint(self): return QSize(self.editor._ln_area_width(), 0)
    def paintEvent(self, e): self.editor._paint_line_numbers(e)

class CodeEditor(QPlainTextEdit):
    breakpoint_toggled = Signal(int, bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("JetBrains Mono", 11))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))
        self.ln_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_ln_width)
        self.updateRequest.connect(self._update_ln_area)
        self.cursorPositionChanged.connect(self._highlight_line)
        self.update_ln_width(0)
        self.highlighter = AssemblyHighlighter(self.document())
        self._highlight_line()
        self.breakpoints: Set[int] = set(); self.current_pc_line: int = -1
        self._setup_completer()

    def _setup_completer(self):
        words = list(INSTRUCTION_DB.keys()) + list(JUMP_ALIASES.keys()) + \
                ["eax","ebx","ecx","edx","esi","edi","esp","ebp","eip",
                 "ax","bx","cx","dx","al","ah","bl","bh","cl","ch","dl","dh"]
        self._completer = QCompleter(words, self)
        self._completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._completer.setWidget(self)
        self._completer.activated.connect(self._insert_completion)
        self._completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self._completer.popup().setFont(QFont("JetBrains Mono", 11))

    def _insert_completion(self, text):
        tc = self.textCursor(); tc.insertText(text.split("|")[0].strip()); self.setTextCursor(tc)

    def _ln_area_width(self):
        return 12 + self.fontMetrics().horizontalAdvance("9") * len(str(max(1,self.blockCount()))) + 24

    def update_ln_width(self, _):
        self.setViewportMargins(self._ln_area_width(), 0, 0, 0)

    def _update_ln_area(self, rect, dy):
        if dy: self.ln_area.scroll(0, dy)
        else: self.ln_area.update(0, rect.y(), self.ln_area.width(), rect.height())
        if rect.contains(self.viewport().rect()): self.update_ln_width(0)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.ln_area.setGeometry(QRect(cr.left(), cr.top(), self._ln_area_width(), cr.height()))

    def _highlight_line(self):
        sel = []; es = QTextEdit.ExtraSelection()
        c = QColor(Theme.get("accent_blue")); c.setAlpha(20)
        es.format.setBackground(c); es.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        es.cursor = self.textCursor(); es.cursor.clearSelection(); sel.append(es)
        self.setExtraSelections(sel)

    def _paint_line_numbers(self, event):
        p = QPainter(self.ln_area); p.fillRect(event.rect(), QColor(Theme.get("bg_secondary")))
        block = self.firstVisibleBlock(); bn = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bot = top + round(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bot >= event.rect().top():
                num = bn + 1
                if num in self.breakpoints:
                    p.setBrush(QBrush(QColor(Theme.get("accent_red")))); p.setPen(Qt.PenStyle.NoPen)
                    p.drawEllipse(4, top+4, 12, 12)
                if num == self.current_pc_line:
                    p.setBrush(QBrush(QColor(Theme.get("accent_yellow")))); p.setPen(Qt.PenStyle.NoPen)
                    p.drawPolygon([QPoint(20,top+4), QPoint(20,top+16), QPoint(28,top+10)])
                p.setPen(QColor(Theme.get("fg_muted")))
                p.drawText(30, top, self.ln_area.width()-35, self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, str(num))
            block = block.next(); top = bot; bot = top + round(self.blockBoundingRect(block).height()); bn += 1

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and e.pos().x() < self._ln_area_width():
            block = self.firstVisibleBlock(); bn = block.blockNumber()
            top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
            while block.isValid():
                if top <= e.pos().y() < top + round(self.blockBoundingRect(block).height()):
                    ln = bn + 1
                    if ln in self.breakpoints: self.breakpoints.remove(ln); self.breakpoint_toggled.emit(ln, False)
                    else: self.breakpoints.add(ln); self.breakpoint_toggled.emit(ln, True)
                    self.ln_area.update(); return
                block = block.next(); top += round(self.blockBoundingRect(block).height()); bn += 1
        super().mousePressEvent(e)

    def set_pc_line(self, line: int):
        self.current_pc_line = line; self.ln_area.update()

    def keyPressEvent(self, e):
        if self._completer.popup().isVisible():
            if e.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Tab, Qt.Key.Key_Escape):
                if e.key() == Qt.Key.Key_Escape: self._completer.popup().hide(); return
                self._completer.popup().hide()
                if e.key() == Qt.Key.Key_Tab: super().keyPressEvent(e)
                return
        if e.key() == Qt.Key.Key_Tab:
            self.textCursor().insertText("    "); return
        if e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            c = self.textCursor(); b = c.block().text(); ind = len(b)-len(b.lstrip())
            if b.strip().endswith(":"): ind += 4
            c.insertText("\n" + " "*ind); return
        super().keyPressEvent(e)
        if e.text().isalpha() or e.text() == "_":
            tc = self.textCursor(); tc.select(QTextCursor.SelectionType.WordUnderCursor)
            word = tc.selectedText()
            if len(word) >= 1:
                self._completer.setCompletionPrefix(word)
                popup = self._completer.popup()
                popup.setCurrentIndex(self._completer.completionModel().index(0, 0))
                cr = self.cursorRect()
                cr.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())
                self._completer.complete(cr)
            else: self._completer.popup().hide()
        else: self._completer.popup().hide()

    def get_labels(self) -> List[str]:
        labels = []
        for line in self.toPlainText().split("\n"):
            s = line.strip()
            if ";" in s: s = s[:s.index(";")].strip()
            if ":" in s:
                lbl = s.split(":")[0].strip()
                if lbl.replace("_","").isalnum(): labels.append(lbl)
        return labels

# ============================================================
# CUSTOM WIDGETS
# ============================================================

class RegisterWidget(QWidget):
    def __init__(self, name: str, cpu: VirtualCPU, parent=None):
        super().__init__(parent); self.name = name.lower(); self.cpu = cpu
        lo = QHBoxLayout(self); lo.setContentsMargins(8,3,8,3); lo.setSpacing(10)
        self.nl = QLabel(name.upper()); self.nl.setFont(QFont("JetBrains Mono",10,QFont.Weight.Bold))
        self.nl.setStyleSheet(f"color:{Theme.get('accent_cyan')}"); self.nl.setFixedWidth(42); lo.addWidget(self.nl)
        self.hl = QLabel("0x00000000"); self.hl.setFont(QFont("JetBrains Mono",10))
        self.hl.setStyleSheet(f"color:{Theme.get('accent_green')}"); self.hl.setFixedWidth(100); lo.addWidget(self.hl)
        self.dl = QLabel("0"); self.dl.setFont(QFont("JetBrains Mono",9))
        self.dl.setStyleSheet(f"color:{Theme.get('fg_secondary')}"); self.dl.setFixedWidth(100); lo.addWidget(self.dl)
        self.bl = QLabel(""); self.bl.setFont(QFont("JetBrains Mono",8))
        self.bl.setStyleSheet(f"color:{Theme.get('fg_muted')}"); lo.addWidget(self.bl)
        lo.addStretch(); self._old = ""
        self.setStyleSheet(f"RegisterWidget{{background:{Theme.get('bg_secondary')};border:1px solid {Theme.get('border')};border-radius:5px}}")

    def update_value(self):
        reg = self.cpu.registers[self.name]; nh = reg.get_hex()
        self.hl.setText(nh); self.dl.setText(str(reg.value))
        bs = format(reg.value & 0xFFFFFFFF, "032b")
        self.bl.setText(f"{bs[:8]}...{bs[-8:]}")
        if nh != self._old:
            self.hl.setStyleSheet(f"color:{Theme.get('accent_yellow')}")
            QTimer.singleShot(350, lambda: self.hl.setStyleSheet(f"color:{Theme.get('accent_green')}"))
        self._old = nh

    def refresh_style(self):
        self.nl.setStyleSheet(f"color:{Theme.get('accent_cyan')}")
        self.hl.setStyleSheet(f"color:{Theme.get('accent_green')}")
        self.dl.setStyleSheet(f"color:{Theme.get('fg_secondary')}")
        self.bl.setStyleSheet(f"color:{Theme.get('fg_muted')}")
        self.setStyleSheet(f"RegisterWidget{{background:{Theme.get('bg_secondary')};border:1px solid {Theme.get('border')};border-radius:5px}}")

class FlagWidget(QWidget):
    FLAG_DESC = {"ZF":"Zero Flag","SF":"Sign Flag","CF":"Carry Flag","OF":"Overflow Flag","PF":"Parity Flag","DF":"Direction Flag"}
    def __init__(self, name: str, cpu: VirtualCPU, parent=None):
        super().__init__(parent); self.name = name; self.cpu = cpu
        lo = QHBoxLayout(self); lo.setContentsMargins(10,4,10,4); lo.setSpacing(12)
        self.nl = QLabel(name); self.nl.setFont(QFont("JetBrains Mono",11,QFont.Weight.Bold))
        self.nl.setFixedWidth(32); lo.addWidget(self.nl)
        self.desc = QLabel(self.FLAG_DESC.get(name,"")); self.desc.setFont(QFont("JetBrains Mono",8))
        self.desc.setStyleSheet(f"color:{Theme.get('fg_secondary')}"); self.desc.setFixedWidth(140); lo.addWidget(self.desc)
        self.led = QLabel("0"); self.led.setFont(QFont("JetBrains Mono",14,QFont.Weight.Bold))
        self.led.setFixedWidth(28); lo.addWidget(self.led)
        lo.addStretch()
        self.setStyleSheet(f"FlagWidget{{background:{Theme.get('bg_secondary')};border:1px solid {Theme.get('border')};border-radius:5px}}")

    def update_value(self):
        v = self.cpu.flags[self.name].value; self.led.setText(str(v))
        c = Theme.get("success") if v else Theme.get("fg_muted")
        self.led.setStyleSheet(f"color:{c}")
        self.nl.setStyleSheet(f"color:{c}")
        self.desc.setStyleSheet(f"color:{Theme.get('fg_secondary')}")
        self.setStyleSheet(f"FlagWidget{{background:{Theme.get('bg_secondary')};border:1px solid {Theme.get('border')};border-radius:5px}}")

class BinaryVisualizer(QWidget):
    def __init__(self, cpu: VirtualCPU, parent=None):
        super().__init__(parent); self.cpu = cpu; self.setMinimumHeight(200); self.setMaximumHeight(280)
    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(Theme.get("bg_secondary")))
        p.setPen(QColor(Theme.get("accent_blue"))); p.setFont(QFont("JetBrains Mono",11,QFont.Weight.Bold))
        p.drawText(15,25,"EAX Binary")
        eax = self.cpu.registers["eax"].value
        bw = min(26,(self.width()-50)//32); sx = (self.width()-32*bw)//2; sy = 48
        for i in range(32):
            bit = (eax>>(31-i))&1; x = sx+i*bw
            if bit: g = QLinearGradient(x,sy,x,sy+32); g.setColorAt(0,QColor(Theme.get("accent_green"))); g.setColorAt(1,QColor(Theme.get("accent_green")).darker(130)); p.setBrush(QBrush(g))
            else: g = QLinearGradient(x,sy,x,sy+32); g.setColorAt(0,QColor(Theme.get("bg_tertiary"))); g.setColorAt(1,QColor(Theme.get("bg_elevated"))); p.setBrush(QBrush(g))
            p.setPen(Qt.PenStyle.NoPen); p.drawRoundedRect(x,sy,bw-2,32,3,3)
            p.setPen(QColor("#ffffff" if bit else Theme.get("fg_muted"))); p.setFont(QFont("JetBrains Mono",9,QFont.Weight.Bold))
            p.drawText(QRect(x,sy,bw-2,32), Qt.AlignmentFlag.AlignCenter, str(bit))
            if i%4==0:
                p.setPen(QColor(Theme.get("fg_muted"))); p.setFont(QFont("JetBrains Mono",7))
                p.drawText(x,sy+46,str(31-i))
        p.setPen(QColor(Theme.get("border")))
        for i in range(1,8): x=sx+i*4*bw; p.drawLine(x-1,sy-4,x-1,sy+36)
        yo = sy + 65; p.setFont(QFont("JetBrains Mono",10))
        p.setPen(QColor(Theme.get("accent_green"))); p.drawText(15,yo,f"Hex: {self.cpu.registers['eax'].get_hex()}")
        p.setPen(QColor(Theme.get("fg_primary"))); p.drawText(15,yo+22,f"Dec: {eax} ({eax-0x100000000 if eax&0x80000000 else eax} signed)")
        p.setPen(QColor(Theme.get("accent_purple")))
        asc = "".join(chr((eax>>(i*8))&0xFF) if 32<=((eax>>(i*8))&0xFF)<=126 else "." for i in reversed(range(4)))
        p.drawText(15,yo+44,f"ASCII: {asc}")

class StackVisualizer(QWidget):
    def __init__(self, cpu: VirtualCPU, parent=None):
        super().__init__(parent); self.cpu = cpu; self.setMinimumHeight(120)
    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(Theme.get("bg_secondary")))
        p.setPen(QColor(Theme.get("accent_blue"))); p.setFont(QFont("JetBrains Mono",10,QFont.Weight.Bold))
        p.drawText(15,22,"Stack")
        if not self.cpu.stack:
            p.setPen(QColor(Theme.get("fg_muted"))); p.setFont(QFont("JetBrains Mono",9))
            p.drawText(15,50,"Empty"); p.drawText(15,70,f"ESP = {self.cpu.registers['esp'].get_hex()}"); return
        cw = self.width()-30; sy = 42; ch = 28
        for i,val in enumerate(reversed(self.cpu.stack[-8:])):
            y = sy + i*(ch+3)
            if i==0: g=QLinearGradient(15,y,15,y+ch); g.setColorAt(0,QColor(Theme.get("accent_blue")).lighter(140)); g.setColorAt(1,QColor(Theme.get("accent_blue")).darker(120)); p.setBrush(QBrush(g))
            else: p.setBrush(QBrush(QColor(Theme.get("bg_tertiary"))))
            p.setPen(QColor(Theme.get("border"))); p.drawRoundedRect(15,y,cw,ch,4,4)
            addr = self.cpu.registers["esp"].value + i*4
            p.setPen(QColor(Theme.get("fg_muted"))); p.setFont(QFont("JetBrains Mono",8))
            p.drawText(25,y+18,f"{addr:08x}")
            p.setPen(QColor(Theme.get("accent_green"))); p.setFont(QFont("JetBrains Mono",9,QFont.Weight.Bold))
            p.drawText(110,y+18,f"{val:08x}")
            p.setPen(QColor(Theme.get("fg_secondary"))); p.setFont(QFont("JetBrains Mono",8))
            p.drawText(210,y+18,f"({val})")
            if i==0:
                p.setPen(QColor(Theme.get("accent_yellow"))); p.setFont(QFont("JetBrains Mono",8,QFont.Weight.Bold))
                p.drawText(cw-60,y+18,"<- TOP")

class ConsoleWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent); self.setReadOnly(True); self.setFont(QFont("JetBrains Mono",9)); self.setMaximumBlockCount(500)
    def log(self, msg: str, level="info"):
        colors = {"info":Theme.get("fg_primary"),"success":Theme.get("success"),"error":Theme.get("error"),
                  "warning":Theme.get("warning"),"header":Theme.get("accent_blue"),"muted":Theme.get("fg_muted")}
        c = self.textCursor(); c.movePosition(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat(); fmt.setForeground(QColor(colors.get(level,colors["info"])))
        if level=="header": fmt.setFontWeight(QFont.Weight.Bold)
        c.insertText(msg+"\n", fmt); self.setTextCursor(c); self.ensureCursorVisible()
    def clear_log(self): self.clear()

class HistoryTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["#","Line","Instruction","Result","Cyc"])
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False); self.setMaximumHeight(180)
        self.setColumnWidth(0,35); self.setColumnWidth(1,40); self.setColumnWidth(3,250); self.setColumnWidth(4,40)
    def add_record(self, r: ExecutionRecord):
        row = self.rowCount(); self.insertRow(row)
        self.setItem(row,0,QTableWidgetItem(str(row+1)))
        self.setItem(row,1,QTableWidgetItem(str(r.line_number+1)))
        self.setItem(row,2,QTableWidgetItem(r.instruction.split()[0] if r.instruction else ""))
        self.setItem(row,3,QTableWidgetItem(r.result))
        self.setItem(row,4,QTableWidgetItem(str(r.cycles)))
        self.scrollToBottom()
    def clear_history(self): self.setRowCount(0)

class RegisterHistoryGraph(QWidget):
    def __init__(self, cpu: VirtualCPU, parent=None):
        super().__init__(parent); self.cpu = cpu; self.setMinimumHeight(160); self.setMaximumHeight(220)
        self.history: Dict[str, List[Tuple[int,int]]] = {}
        self.step = 0
    def clear(self): self.history.clear(); self.step = 0; self.update()
    def record(self):
        self.step += 1
        for name, reg in self.cpu.registers.items():
            if name not in self.history: self.history[name] = []
            self.history[name].append((self.step, reg.value))
        self.update()
    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(Theme.get("bg_secondary")))
        p.setPen(QColor(Theme.get("fg_muted"))); p.setFont(QFont("JetBrains Mono",9))
        p.drawText(10,18,"Register History")
        if not self.history or self.step < 2: return
        colors = {"eax":Theme.get("accent_green"),"ebx":Theme.get("accent_blue"),
                  "ecx":Theme.get("accent_yellow"),"edx":Theme.get("accent_red")}
        margin_l, margin_r, margin_t, margin_b = 50, 15, 30, 25
        w = self.width()-margin_l-margin_r; h = self.height()-margin_t-margin_b
        all_vals = []
        for rn in colors:
            if rn in self.history: all_vals.extend(v for _,v in self.history[rn])
        if not all_vals: return
        vmin, vmax = min(all_vals), max(all_vals)
        if vmin == vmax: vmax = vmin + 1
        p.setPen(QColor(Theme.get("border"))); p.drawLine(margin_l, margin_t, margin_l, margin_t+h)
        p.drawLine(margin_l, margin_t+h, margin_l+w, margin_t+h)
        p.setPen(QColor(Theme.get("fg_muted"))); p.setFont(QFont("JetBrains Mono",7))
        p.drawText(2, margin_t+6, f"{vmax}")
        p.drawText(2, margin_t+h, f"{vmin}")
        max_steps = self.step
        for rn, color in colors.items():
            if rn not in self.history: continue
            data = self.history[rn]
            pen = QPen(QColor(color), 2); p.setPen(pen)
            points = []
            for step, val in data:
                x = margin_l + (step-1)/max(1,max_steps-1)*w
                y = margin_t + (1 - (val-vmin)/(vmax-vmin))*h
                points.append(QPoint(int(x), int(y)))
            if len(points) >= 2:
                for i in range(len(points)-1):
                    p.drawLine(points[i], points[i+1])
        lx = margin_l + 5
        for rn, color in colors.items():
            if rn not in self.history: continue
            p.setPen(Qt.PenStyle.NoPen); p.setBrush(QColor(color))
            p.drawRect(lx, 6, 10, 10)
            p.setPen(QColor(Theme.get("fg_secondary"))); p.setFont(QFont("JetBrains Mono",8))
            p.drawText(lx+14, 15, rn.upper()); lx += 60

class WatchPanel(QWidget):
    def __init__(self, cpu: VirtualCPU, parent=None):
        super().__init__(parent); self.cpu = cpu
        lo = QVBoxLayout(self); lo.setContentsMargins(4,4,4,4); lo.setSpacing(4)
        row = QHBoxLayout()
        self.inp = QLineEdit(); self.inp.setPlaceholderText("e.g. eax + ebx * 2"); row.addWidget(self.inp)
        b = QPushButton("Add"); b.setFixedWidth(60); b.clicked.connect(self._add); row.addWidget(b)
        lo.addLayout(row)
        self.table = QTableWidget(); self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Expr","Value","Hex"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        lo.addWidget(self.table); self.watches: List[str] = []

    def _add(self):
        e = self.inp.text().strip()
        if e and e not in self.watches: self.watches.append(e); self.refresh(); self.inp.clear()

    def refresh(self):
        self.table.setRowCount(len(self.watches))
        for i, expr in enumerate(self.watches):
            v = self._eval(expr)
            self.table.setItem(i,0,QTableWidgetItem(expr))
            self.table.setItem(i,1,QTableWidgetItem(str(v)))
            self.table.setItem(i,2,QTableWidgetItem(f"0x{v&0xFFFFFFFF:08x}"))

    def _eval(self, expr: str) -> int:
        try:
            e = expr.lower()
            for rn, reg in self.cpu.registers.items(): e = re.sub(r"\b"+rn+r"\b", str(reg.value), e)
            return int(eval(e)) & 0xFFFFFFFF
        except: return 0

class DiffViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); lo = QVBoxLayout(self); lo.setContentsMargins(4,4,4,4)
        self.text = QTextEdit(); self.text.setReadOnly(True); self.text.setFont(QFont("JetBrains Mono",10))
        lo.addWidget(self.text)
    def show_diff(self, expected: Dict, actual: Dict):
        h = f"<h3 style='color:{Theme.get('accent_blue')}'>State Comparison</h3>"
        h += "<table style='width:100%;font-family:monospace'>"
        h += f"<tr style='color:{Theme.get('fg_secondary')}'><th>Reg</th><th>Expected</th><th>Actual</th><th></th></tr>"
        for k in expected:
            ev = expected[k]; av = actual.get(k,"N/A"); ok = ev == av
            c = Theme.get("success") if ok else Theme.get("error"); s = "OK" if ok else "FAIL"
            h += f"<tr><td style='color:{Theme.get('accent_cyan')}'>{k}</td><td>{ev}</td><td>{av}</td><td style='color:{c};font-weight:bold'>{s}</td></tr>"
        h += "</table>"; self.text.setHtml(h)

# ============================================================
# MULTI-ARCHITECTURE INSTRUCTION REFERENCE (NEW)
# ============================================================

class ArchRefWidget(QWidget):
    """Widget showing instruction reference for ARM, RISC-V, MIPS."""
    def __init__(self, arch: str, parent=None):
        super().__init__(parent); self.arch = arch; self._data = _RAW_DATA.get(arch, {})
        lo = QVBoxLayout(self); lo.setContentsMargins(4,4,4,4); lo.setSpacing(4)
        # Search + category filter
        row = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText(f"Search {arch.upper()} instructions...")
        self.search.textChanged.connect(self._filter); row.addWidget(self.search)
        self.cat_combo = QComboBox(); self.cat_combo.addItem("All Categories")
        cats = sorted(set(i.get("category","") for i in self._data.values()))
        for c in cats: self.cat_combo.addItem(c)
        self.cat_combo.currentTextChanged.connect(self._filter); row.addWidget(self.cat_combo)
        lo.addLayout(row)
        # Table
        self.table = QTableWidget(); self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Instruction", "Syntax", "Category"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self._show_detail)
        lo.addWidget(self.table)
        # Detail panel
        self.detail = QTextEdit(); self.detail.setReadOnly(True)
        self.detail.setMaximumHeight(250)
        lo.addWidget(self.detail)
        self._populate()

    def _populate(self):
        self.table.setRowCount(0)
        for opcode, d in sorted(self._data.items()):
            row = self.table.rowCount(); self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(opcode))
            self.table.setItem(row, 1, QTableWidgetItem(d.get("syntax", "")))
            self.table.setItem(row, 2, QTableWidgetItem(d.get("category", "")))
            self.table.item(row, 0).setForeground(QColor(Theme.get("accent_blue")))
            self.table.item(row, 0).setFont(QFont("JetBrains Mono", 10, QFont.Weight.Bold))

    def _filter(self):
        q = self.search.text().upper(); cat = self.cat_combo.currentText()
        for i in range(self.table.rowCount()):
            op_item = self.table.item(i, 0); syn_item = self.table.item(i, 1); cat_item = self.table.item(i, 2)
            op_text = op_item.text().upper() if op_item else ""
            syn_text = syn_item.text().upper() if syn_item else ""
            cat_text = cat_item.text() if cat_item else ""
            match_search = not q or q in op_text or q in syn_text
            match_cat = cat == "All Categories" or cat == cat_text
            self.table.setRowHidden(i, not (match_search and match_cat))

    def _show_detail(self, row, col):
        op_item = self.table.item(row, 0)
        if not op_item: return
        opcode = op_item.text()
        d = self._data.get(opcode, {})
        desc = d.get("description", "No description available.")
        syntax = d.get("syntax", "")
        example = d.get("example", "")
        use_cases = d.get("use_cases", [])
        notes = d.get("notes", "")
        # Check x86 for use cases too
        x86_data = _RAW_DATA.get("x86", {}).get(opcode, {})
        if not use_cases and "use_cases" in x86_data:
            use_cases = x86_data["use_cases"]
        html = f"<h3 style='color:{Theme.get('accent_blue')}'>{opcode} <span style='color:{Theme.get('fg_muted')};font-weight:normal;font-size:9pt'>[{self.arch.upper()}]</span></h3>"
        if syntax:
            html += f"<p style='color:{Theme.get('accent_green')}'>Syntax: <code>{html_mod.escape(syntax)}</code></p>"
        html += f"<p style='color:{Theme.get('fg_primary')}'>{html_mod.escape(desc)}</p>"
        if example:
            html += f"<p style='color:{Theme.get('accent_orange')}'>Example: <code>{html_mod.escape(example)}</code></p>"
        if use_cases:
            html += f"<h4 style='color:{Theme.get('accent_purple')}'>Use Cases:</h4><ul style='color:{Theme.get('fg_secondary')}'>"
            for uc in use_cases:
                html += f"<li>{html_mod.escape(uc)}</li>"
            html += "</ul>"
        if notes:
            html += f"<p style='color:{Theme.get('accent_yellow')}'>Note: {html_mod.escape(notes)}</p>"
        self.detail.setHtml(html)

# ============================================================
# CONCEPTS LEARNING PANEL (NEW)
# ============================================================

class ConceptsPanel(QWidget):
    """Panel for learning assembly language concepts."""
    def __init__(self, parent=None):
        super().__init__(parent); self.concepts = _RAW_DATA.get("concepts", [])
        lo = QVBoxLayout(self); lo.setContentsMargins(4,4,4,4); lo.setSpacing(4)
        # Category filter
        row = QHBoxLayout()
        self.cat_combo = QComboBox(); self.cat_combo.addItem("All Topics")
        cats = sorted(set(c.get("category","") for c in self.concepts))
        for c in cats: self.cat_combo.addItem(c)
        self.cat_combo.currentTextChanged.connect(self._filter); row.addWidget(self.cat_combo)
        lo.addLayout(row)
        # List
        self.list = QListWidget(); self.list.currentRowChanged.connect(self._on_select)
        lo.addWidget(self.list)
        # Content
        self.content = QTextEdit(); self.content.setReadOnly(True)
        self.content.setOpenExternalLinks(True)
        lo.addWidget(self.content)
        self._populate()

    def _populate(self):
        self.list.clear()
        for c in self.concepts:
            item = QListWidgetItem(f"[{c.get('category','')}] {c.get('title','')}")
            item.setData(Qt.ItemDataRole.UserRole, c)
            self.list.addItem(item)

    def _filter(self, cat):
        for i in range(self.list.count()):
            item = self.list.item(i); c = item.data(Qt.ItemDataRole.UserRole)
            item.setHidden(cat != "All Topics" and c.get("category","") != cat)

    def _on_select(self, row):
        if row < 0: return
        c = self.list.item(row).data(Qt.ItemDataRole.UserRole)
        if c:
            self.content.setHtml(c.get("content", ""))

# ============================================================
# ENHANCED INSTRUCTION REFERENCE (with use cases)
# ============================================================

class InstructionReferenceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); lo = QVBoxLayout(self); lo.setContentsMargins(4,4,4,4); lo.setSpacing(4)
        row = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("Search x86 instructions...")
        self.search.textChanged.connect(self._filter); row.addWidget(self.search)
        self.cat = QComboBox(); self.cat.addItem("All")
        for c in sorted(set(i.category for i in INSTRUCTION_DB.values())): self.cat.addItem(c)
        self.cat.currentTextChanged.connect(self._filter); row.addWidget(self.cat)
        lo.addLayout(row)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Op","Category","Diff","Cyc"])
        self.tree.setColumnWidth(0,70); self.tree.setColumnWidth(1,90); self.tree.setColumnWidth(2,50); self.tree.setColumnWidth(3,35)
        self.tree.itemClicked.connect(self._detail)
        lo.addWidget(self.tree)
        self.detail = QTextEdit(); self.detail.setReadOnly(True)
        lo.addWidget(self.detail); self._populate()

    def _populate(self):
        self.tree.clear()
        for op, inst in sorted(INSTRUCTION_DB.items()):
            item = QTreeWidgetItem([inst.opcode, inst.category,
                "*" * inst.difficulty + "." * (5 - inst.difficulty), str(inst.cycles)])
            item.setData(0, Qt.ItemDataRole.UserRole, inst)
            item.setForeground(0, QColor(Theme.get("accent_blue")))
            item.setFont(0, QFont("JetBrains Mono", 10, QFont.Weight.Bold))
            self.tree.addTopLevelItem(item)

    def _filter(self):
        q = self.search.text().upper(); c = self.cat.currentText()
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i); inst = item.data(0, Qt.ItemDataRole.UserRole)
            ms = not q or q in inst.opcode or q in inst.description.upper() or q in inst.category.upper()
            mc = c == "All" or inst.category == c
            item.setHidden(not (ms and mc))

    def _detail(self, item, _):
        inst = item.data(0, Qt.ItemDataRole.UserRole)
        if not inst: return
        html = f"<h3 style='color:{Theme.get('accent_blue')}'>{inst.opcode} <span style='color:{Theme.get('fg_muted')};font-size:9pt'>{', '.join(inst.operands)}</span></h3>"
        html += f"<p style='color:{Theme.get('fg_primary')}'>{html_mod.escape(inst.description)}</p>"
        html += f"<p style='color:{Theme.get('accent_orange')}'><b>Example:</b> <code>{html_mod.escape(inst.example)}</code></p>"
        html += f"<p style='color:{Theme.get('fg_muted')};font-size:9pt'>{inst.category} | {'*'*inst.difficulty}{'.'*(5-inst.difficulty)} | ~{inst.cycles} cyc | Flags: {inst.affects_flags}</p>"
        # Use Cases
        if inst.use_cases:
            html += f"<h4 style='color:{Theme.get('accent_purple')}'>Use Cases:</h4><ul style='color:{Theme.get('fg_secondary')}'>"
            for uc in inst.use_cases:
                html += f"<li>{html_mod.escape(uc)}</li>"
            html += "</ul>"
        # Notes
        if inst.notes:
            html += f"<p style='color:{Theme.get('accent_yellow')}'>Note: {html_mod.escape(inst.notes)}</p>"
        # Related instructions
        if hasattr(inst, 'see_also') and inst.see_also:
            related = ", ".join(inst.see_also)
            html += f"<p style='color:{Theme.get('fg_muted')}'>See also: {html_mod.escape(related)}</p>"
        self.detail.setHtml(html)

# ============================================================
# CODE SNIPPETS PANEL
# ============================================================

class SnippetsPanel(QWidget):
    snippet_selected = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent); lo = QVBoxLayout(self); lo.setContentsMargins(4,4,4,4)
        row = QHBoxLayout()
        self.filter = QComboBox(); self.filter.addItem("All")
        for c in sorted(set(s.category for s in CODE_SNIPPETS)): self.filter.addItem(c)
        self.filter.currentTextChanged.connect(self._do_filter); row.addWidget(self.filter)
        lo.addLayout(row)
        self.list = QListWidget(); self.list.currentRowChanged.connect(self._on_select)
        lo.addWidget(self.list); self._populate()

    def _populate(self):
        self.list.clear()
        for s in CODE_SNIPPETS:
            item = QListWidgetItem(f"{s.name}  [{s.category}]")
            item.setData(Qt.ItemDataRole.UserRole, s)
            item.setToolTip(s.description)
            self.list.addItem(item)

    def _do_filter(self, cat):
        for i in range(self.list.count()):
            item = self.list.item(i); s = item.data(Qt.ItemDataRole.UserRole)
            item.setHidden(cat != "All" and s.category != cat)

    def _on_select(self, row):
        if row < 0: return
        s = self.list.item(row).data(Qt.ItemDataRole.UserRole)
        self.snippet_selected.emit(s.code)

# ============================================================
# LESSON PANEL
# ============================================================

class LessonPanel(QWidget):
    lesson_changed = Signal(int); challenge_requested = Signal()
    def __init__(self, parent=None):
        super().__init__(parent); lo = QVBoxLayout(self); lo.setContentsMargins(12,12,12,12); lo.setSpacing(8)
        self.title = QLabel("Lesson"); self.title.setFont(QFont("JetBrains Mono",13,QFont.Weight.Bold))
        self.title.setStyleSheet(f"color:{Theme.get('accent_blue')}"); lo.addWidget(self.title)
        self.desc = QLabel(""); self.desc.setWordWrap(True); self.desc.setFont(QFont("JetBrains Mono",9))
        self.desc.setStyleSheet(f"color:{Theme.get('fg_secondary')}"); lo.addWidget(self.desc)
        self.concept_box = QTextEdit(); self.concept_box.setReadOnly(True); self.concept_box.setMaximumHeight(80)
        self.concept_box.setFont(QFont("JetBrains Mono",9))
        lo.addWidget(self.concept_box)
        of = QFrame()
        ol = QVBoxLayout(of); ol.setContentsMargins(10,10,10,10)
        oh = QLabel("Objective"); oh.setFont(QFont("JetBrains Mono",10,QFont.Weight.Bold))
        oh.setStyleSheet(f"color:{Theme.get('accent_blue')}"); ol.addWidget(oh)
        self.obj = QLabel(""); self.obj.setWordWrap(True); self.obj.setFont(QFont("JetBrains Mono",9)); ol.addWidget(self.obj)
        lo.addWidget(of)
        self.allowed = QLabel(""); self.allowed.setFont(QFont("JetBrains Mono",9))
        self.allowed.setStyleSheet(f"color:{Theme.get('accent_green')}"); lo.addWidget(self.allowed)
        self.hint_label = QLabel(""); self.hint_label.setWordWrap(True); self.hint_label.setFont(QFont("JetBrains Mono",9))
        self.hint_label.setStyleSheet(f"color:{Theme.get('accent_yellow')}"); lo.addWidget(self.hint_label)
        self.progress = QProgressBar(); self.progress.setMaximum(len(LESSONS)); self.progress.setFormat("Lesson %v/%m")
        lo.addWidget(self.progress)
        nr = QHBoxLayout()
        self.prev = QPushButton("< Prev"); self.prev.clicked.connect(lambda: self.lesson_changed.emit(self.idx-1)); nr.addWidget(self.prev)
        self.next = QPushButton("Next >"); self.next.clicked.connect(lambda: self.lesson_changed.emit(self.idx+1)); nr.addWidget(self.next)
        lo.addLayout(nr)
        self.chal_btn = QPushButton("Challenge Mode")
        self.chal_btn.setStyleSheet(f"QPushButton{{background:{Theme.get('accent_yellow')}25;color:{Theme.get('accent_yellow')};border:1px solid {Theme.get('accent_yellow')}}}QPushButton:hover{{background:{Theme.get('accent_yellow')}45}}")
        self.chal_btn.clicked.connect(self.challenge_requested.emit); lo.addWidget(self.chal_btn)
        self.load_btn = QPushButton("Load Template"); lo.addWidget(self.load_btn)
        self.idx = 0

    def set_lesson(self, i):
        if 0 <= i < len(LESSONS):
            self.idx = i; l = LESSONS[i]
            self.title.setText(l.title); self.desc.setText(l.description)
            self.obj.setText(l.objective)
            self.concept_box.setHtml(f"<p style='color:{Theme.get('fg_primary')};margin:2px'>{l.concept}</p>" if l.concept else "")
            self.allowed.setText(f"Allowed: {', '.join(l.instructions)}")
            self.hint_label.setText(f"Hint: {l.hint}" if l.hint else "")
            self.progress.setValue(i+1); self.prev.setEnabled(i>0); self.next.setEnabled(i<len(LESSONS)-1)
            self.chal_btn.setEnabled(l.challenge_time is not None)
            self.load_btn.setEnabled(bool(l.code_template))

# ============================================================
# MEMORY VIEWER
# ============================================================

class MemoryViewer(QWidget):
    def __init__(self, cpu: VirtualCPU, parent=None):
        super().__init__(parent); self.cpu = cpu
        lo = QVBoxLayout(self); lo.setContentsMargins(4,4,4,4)
        row = QHBoxLayout(); row.addWidget(QLabel("Addr:"))
        self.addr = QLineEdit("0x7FFF0000"); self.addr.setFixedWidth(110); row.addWidget(self.addr)
        self.sz = QSpinBox(); self.sz.setRange(16,256); self.sz.setValue(64); self.sz.setSingleStep(16); row.addWidget(self.sz)
        b = QPushButton("Go"); b.clicked.connect(self.refresh); row.addWidget(b); row.addStretch(); lo.addLayout(row)
        self.disp = QPlainTextEdit(); self.disp.setReadOnly(True); self.disp.setFont(QFont("JetBrains Mono",9))
        lo.addWidget(self.disp)

    def refresh(self):
        try: a = int(self.addr.text(),16)
        except: a = 0x7FFF0000
        sz = self.sz.value(); lines = []
        for r in range(0, sz, 16):
            la = a+r; hb = []; ac = []
            for c in range(16):
                if r+c < sz:
                    v = self.cpu.memory[la+c].value if la+c in self.cpu.memory else 0
                    hb.append(f"{v:02x}"); ac.append(chr(v) if 32<=v<=126 else ".")
                else: hb.append("  "); ac.append(" ")
            lines.append(f"{la:08x}  {' '.join(hb)}  |{''.join(ac)}|")
        self.disp.setPlainText("\n".join(lines))

# ============================================================
# CHALLENGE DIALOG
# ============================================================

class ChallengeDialog(QDialog):
    completed = Signal(int, int)
    def __init__(self, lesson: Lesson, parent=None):
        super().__init__(parent); self.lesson = lesson
        self.time_limit = lesson.challenge_time or 60; self.remaining = self.time_limit
        self.setWindowTitle(f"Challenge: {lesson.title}"); self.setMinimumSize(380,220)
        lo = QVBoxLayout(self)
        info = QLabel(f"Complete within {self.time_limit}s!")
        info.setFont(QFont("JetBrains Mono",12,QFont.Weight.Bold))
        info.setStyleSheet(f"color:{Theme.get('accent_yellow')}"); lo.addWidget(info)
        self.obj = QLabel(lesson.objective); self.obj.setWordWrap(True); lo.addWidget(self.obj)
        self.timer_lbl = QLabel(f"Time: {self.remaining}s"); self.timer_lbl.setFont(QFont("JetBrains Mono",28,QFont.Weight.Bold))
        self.timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); lo.addWidget(self.timer_lbl)
        self.bar = QProgressBar(); self.bar.setMaximum(self.time_limit); self.bar.setValue(self.time_limit); lo.addWidget(self.bar)
        br = QHBoxLayout()
        self.start = QPushButton("Start"); self.start.clicked.connect(self._go); br.addWidget(self.start)
        c = QPushButton("Cancel"); c.clicked.connect(self.reject); br.addWidget(c); lo.addLayout(br)
        self.timer = QTimer(self); self.timer.timeout.connect(self._tick); self.running = False
    def _go(self): self.running = True; self.start.setEnabled(False); self.timer.start(1000)
    def _tick(self):
        self.remaining -= 1; self.timer_lbl.setText(f"Time: {self.remaining}s"); self.bar.setValue(self.remaining)
        if self.remaining <= 10: self.timer_lbl.setStyleSheet(f"color:{Theme.get('error')}")
        if self.remaining <= 0: self.timer.stop(); self.reject()
    def finish(self, ok):
        if not self.running: return
        self.timer.stop()
        if ok:
            t = self.time_limit - self.remaining; r = t/self.time_limit
            s = 3 if r < 0.3 else 2 if r < 0.6 else 1
            self.completed.emit(s, t); self.accept()
        else: self.reject()
    def closeEvent(self, e): self.timer.stop(); super().closeEvent(e)

# ============================================================
# SESSION STATS DIALOG
# ============================================================

class StatsDialog(QDialog):
    def __init__(self, stats: SessionStats, parent=None):
        super().__init__(parent); self.setWindowTitle("Session Statistics"); self.setMinimumSize(400,350)
        lo = QVBoxLayout(self)
        d = stats.to_dict()
        t = QTableWidget(); t.setColumnCount(2); t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.verticalHeader().setVisible(False); t.horizontalHeader().setVisible(False)
        items = [("Session Duration",d["duration"]),("Instructions Executed",str(d["instructions"])),
            ("Errors",str(d["errors"])),("Accuracy",d["accuracy"]),("Lessons Completed",str(d["lessons"])),
            ("Challenges Won",str(d["challenges"])),("Stars Earned",str(d["stars"])),
            ("Unique Instructions",str(d["unique_ops"])),("Most Used",d["most_used"])]
        t.setRowCount(len(items))
        for i,(k,v) in enumerate(items):
            ki = QTableWidgetItem(k); ki.setFont(QFont("JetBrains Mono",10,QFont.Weight.Bold))
            ki.setForeground(QColor(Theme.get("accent_cyan"))); t.setItem(i,0,ki)
            vi = QTableWidgetItem(v); t.setItem(i,1,vi)
        t.horizontalHeader().setStretchLastSection(True); t.setColumnWidth(0,200); lo.addWidget(t)
        if stats.instructions_used:
            lo.addWidget(QLabel("Instruction Frequency:"))
            freq = sorted(stats.instructions_used.items(), key=lambda x:-x[1])
            bar_text = " | ".join(f"{op}:{cnt}" for op,cnt in freq[:10])
            lo.addWidget(QLabel(bar_text))
        c = QPushButton("Close"); c.clicked.connect(self.accept); lo.addWidget(c)

# ============================================================
# EXPORT MANAGER
# ============================================================

class ExportManager:
    @staticmethod
    def to_html(cpu: VirtualCPU, code: str, history: List[ExecutionRecord], stats: SessionStats):
        reg_rows = "".join(f"<tr><td><b>{n.upper()}</b></td><td>{r.get_hex()}</td><td>{r.value}</td></tr>"
            for n,r in cpu.registers.items())
        flag_rows = "".join(f"<tr><td><b>{n}</b></td><td>{r.value}</td></tr>" for n,r in cpu.flags.items())
        hist_rows = "".join(f"<tr><td>{i+1}</td><td>{r.line_number+1}</td><td>{html_mod.escape(r.instruction)}</td><td>{html_mod.escape(r.result)}</td></tr>"
            for i,r in enumerate(history))
        sd = stats.to_dict()
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Assembly Lab Report</title>
<style>body{{font-family:'JetBrains Mono',monospace;background:#0d1117;color:#c9d1d9;padding:20px}}
table{{border-collapse:collapse;width:100%;margin:10px 0}}th,td{{border:1px solid #30363d;padding:6px 12px;text-align:left}}
th{{background:#161b22;color:#58a6ff}}tr:nth-child(even){{background:#161b22}}
h1{{color:#58a6ff}}h2{{color:#39c5cf}}h3{{color:#a371f7}}.meta{{color:#8b949e}}</style></head>
<body><h1>Assembly Learning Lab v5.0 - Report</h1>
<p class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Duration: {sd['duration']} | Instructions: {sd['instructions']} | Accuracy: {sd['accuracy']}</p>
<h2>Source Code</h2><pre style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">{html_mod.escape(code)}</pre>
<h2>Registers</h2><table><tr><th>Register</th><th>Hex</th><th>Decimal</th></tr>{reg_rows}</table>
<h2>Flags</h2><table><tr><th>Flag</th><th>Value</th></tr>{flag_rows}</table>
<h2>Execution History ({len(history)} steps, {cpu.total_cycles} cycles)</h2>
<table><tr><th>#</th><th>Line</th><th>Instruction</th><th>Result</th></tr>{hist_rows}</table>
<h2>Pseudocode</h2><pre style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">{html_mod.escape(PseudocodeTranslator.translate(code))}</pre>
</body></html>"""# ============================================================
# MAIN WINDOW
# ============================================================

class AssemblyLab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assembly Learning Lab v5.0 - Multi-Architecture Edition")
        self.setMinimumSize(1280, 820)
        self.resize(1440, 900)

        self.cpu = VirtualCPU()
        self.stats = SessionStats()
        self.state_stack: List[Dict] = []
        self.current_file: Optional[str] = None
        self.recent_files: List[str] = []
        self.settings = QSettings("AssemblyLab", "v5")
        self.challenge_dialog: Optional[ChallengeDialog] = None
        self.run_timer = QTimer(self)
        self.run_timer.timeout.connect(self._run_step)
        self._run_speed = 200

        self._build_ui()
        self._build_menus()
        self._build_toolbar()
        self._build_statusbar()
        self._connect_signals()
        self._apply_theme()

        theme = self.settings.value("theme", "dark")
        Theme.set_mode(theme)
        self._apply_theme()

        self.console.log("Welcome to Assembly Learning Lab v5.0 - Multi-Architecture Edition!", "header")
        self.console.log("F5=Run All | F10=Step | F6=Reset | Ctrl+S=Save | Ctrl+O=Open", "muted")
        self.console.log(f"Loaded {len(LESSONS)} lessons, {len(INSTRUCTION_DB)} x86 instructions.", "info")
        arm_count = len(_RAW_DATA.get("arm", {}))
        riscv_count = len(_RAW_DATA.get("riscv", {}))
        mips_count = len(_RAW_DATA.get("mips", {}))
        self.console.log(f"Multi-arch references: {arm_count} ARM, {riscv_count} RISC-V, {mips_count} MIPS", "info")
        self.console.log(f"Assembly concepts: {len(_RAW_DATA.get('concepts', []))} topics", "info")

    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        main_layout = QHBoxLayout(central); main_layout.setContentsMargins(4,4,4,4)

        # LEFT: Editor + Console
        left_splitter = QSplitter(Qt.Orientation.Vertical)
        self.editor = CodeEditor()
        self.editor.setPlainText("; Assembly Learning Lab v5.0\n; Start coding here!\n\nMOV eax, 42\n")
        left_splitter.addWidget(self.editor)

        console_group = QGroupBox("Console Output")
        cl = QVBoxLayout(console_group); cl.setContentsMargins(4,12,4,4)
        self.console = ConsoleWidget(); cl.addWidget(self.console)
        left_splitter.addWidget(console_group)
        left_splitter.setSizes([500, 200])

        # RIGHT: Registers/Flags/Stack + History + Graph
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        reg_group = QGroupBox("Registers")
        rl = QVBoxLayout(reg_group); rl.setContentsMargins(4,14,4,4); rl.setSpacing(2)
        self.reg_widgets = {}
        for name in ["eax","ebx","ecx","edx","esi","edi","esp","ebp"]:
            w = RegisterWidget(name, self.cpu); self.reg_widgets[name] = w; rl.addWidget(w)
        right_splitter.addWidget(reg_group)

        flag_group = QGroupBox("Flags")
        fl = QVBoxLayout(flag_group); fl.setContentsMargins(4,14,4,4); fl.setSpacing(2)
        self.flag_widgets = {}
        for name in ["ZF","SF","CF","OF","PF","DF"]:
            w = FlagWidget(name, self.cpu); self.flag_widgets[name] = w; fl.addWidget(w)
        right_splitter.addWidget(flag_group)

        vis_tabs = QTabWidget()
        self.binary_viz = BinaryVisualizer(self.cpu); vis_tabs.addTab(self.binary_viz, "Binary")
        self.stack_viz = StackVisualizer(self.cpu); vis_tabs.addTab(self.stack_viz, "Stack")
        right_splitter.addWidget(vis_tabs)

        hist_group = QGroupBox("Execution History")
        hl = QVBoxLayout(hist_group); hl.setContentsMargins(4,14,4,4)
        self.history_table = HistoryTable(); hl.addWidget(self.history_table)
        right_splitter.addWidget(hist_group)

        self.reg_graph = RegisterHistoryGraph(self.cpu)
        right_splitter.addWidget(self.reg_graph)
        right_splitter.setSizes([300, 150, 200, 180, 160])

        h_splitter = QSplitter(Qt.Orientation.Horizontal)
        h_splitter.addWidget(left_splitter)
        h_splitter.addWidget(right_splitter)
        h_splitter.setSizes([600, 540])
        main_layout.addWidget(h_splitter)

        # ---- DOCK PANELS ----
        # Lessons
        self.lesson_panel = LessonPanel()
        self.lesson_dock = QDockWidget("Lessons", self)
        self.lesson_dock.setWidget(self.lesson_panel)
        self.lesson_dock.setMinimumWidth(280)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.lesson_dock)

        # x86 Instruction Reference (with use cases)
        self.ref_widget = InstructionReferenceWidget()
        self.ref_dock = QDockWidget("x86 Instruction Reference", self)
        self.ref_dock.setWidget(self.ref_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.ref_dock)

        # Multi-Arch Reference Tabs (NEW)
        arch_tabs = QTabWidget()
        self.arm_ref = ArchRefWidget("arm"); arch_tabs.addTab(self.arm_ref, "ARM/AArch64")
        self.riscv_ref = ArchRefWidget("riscv"); arch_tabs.addTab(self.riscv_ref, "RISC-V")
        self.mips_ref = ArchRefWidget("mips"); arch_tabs.addTab(self.mips_ref, "MIPS")
        self.arch_dock = QDockWidget("Multi-Architecture Reference", self)
        self.arch_dock.setWidget(arch_tabs)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.arch_dock)

        # Concepts Panel (NEW)
        self.concepts_panel = ConceptsPanel()
        self.concepts_dock = QDockWidget("Assembly Concepts", self)
        self.concepts_dock.setWidget(self.concepts_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.concepts_dock)

        # Code Snippets
        self.snippets_panel = SnippetsPanel()
        self.snip_dock = QDockWidget("Code Snippets", self)
        self.snip_dock.setWidget(self.snippets_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.snip_dock)

        # Watch panel
        self.watch_panel = WatchPanel(self.cpu)
        self.watch_dock = QDockWidget("Watch Expressions", self)
        self.watch_dock.setWidget(self.watch_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.watch_dock)

        # Tabify some docks
        self.tabifyDockWidget(self.ref_dock, self.watch_dock)

        # Pseudocode (bottom dock)
        self.pseudo_edit = QTextEdit(); self.pseudo_edit.setReadOnly(True); self.pseudo_edit.setFont(QFont("JetBrains Mono",10))
        self.pseudo_dock = QDockWidget("Pseudocode", self); self.pseudo_dock.setWidget(self.pseudo_edit)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.pseudo_dock)

        # Memory viewer dock
        self.mem_viewer = MemoryViewer(self.cpu)
        self.mem_dock = QDockWidget("Memory", self); self.mem_dock.setWidget(self.mem_viewer)
        self.tabifyDockWidget(self.pseudo_dock, self.mem_dock)

        # Diff viewer dock
        self.diff_viewer = DiffViewer()
        self.diff_dock = QDockWidget("Diff Viewer", self); self.diff_dock.setWidget(self.diff_viewer)
        self.tabifyDockWidget(self.mem_dock, self.diff_dock)

        # Hide some docks by default for cleaner startup
        self.watch_dock.hide(); self.diff_dock.hide(); self.mem_dock.hide(); self.snip_dock.hide()
        self.concepts_dock.hide()

        # Set initial lesson
        self.lesson_panel.set_lesson(0)

    # ---- MENUS ----
    def _build_menus(self):
        mb = self.menuBar()
        fm = mb.addMenu("&File")
        self._action(fm, "New", "Ctrl+N", self._new_file)
        self._action(fm, "Open...", "Ctrl+O", self._open_file)
        self._action(fm, "Save", "Ctrl+S", self._save_file)
        self._action(fm, "Save As...", "Ctrl+Shift+S", self._save_file_as)
        fm.addSeparator()
        self.recent_menu = fm.addMenu("Recent Files")
        fm.addSeparator()
        self._action(fm, "Export HTML Report...", "Ctrl+E", self._export_html)
        fm.addSeparator()
        self._action(fm, "Exit", "Ctrl+Q", self.close)

        em = mb.addMenu("&Edit")
        self._action(em, "Undo (CPU State)", "Ctrl+Z", self._undo_state)
        self._action(em, "Clear Console", "Ctrl+L", self.console.clear_log)
        self._action(em, "Clear History", "", lambda: self.history_table.clear_history())
        self._action(em, "Copy Pseudocode", "", self._copy_pseudo)
        em.addSeparator()
        self._action(em, "Increase Font", "Ctrl++", lambda: self._change_font(1))
        self._action(em, "Decrease Font", "Ctrl+-", lambda: self._change_font(-1))

        vm = mb.addMenu("&View")
        vm.addAction(self.lesson_dock.toggleViewAction())
        vm.addAction(self.ref_dock.toggleViewAction())
        vm.addAction(self.arch_dock.toggleViewAction())
        vm.addAction(self.concepts_dock.toggleViewAction())
        vm.addAction(self.snip_dock.toggleViewAction())
        vm.addAction(self.watch_dock.toggleViewAction())
        vm.addAction(self.pseudo_dock.toggleViewAction())
        vm.addAction(self.mem_dock.toggleViewAction())
        vm.addAction(self.diff_dock.toggleViewAction())
        vm.addSeparator()
        theme_menu = vm.addMenu("Theme")
        for t in Theme.available_themes():
            a = theme_menu.addAction(t.capitalize())
            a.triggered.connect(lambda checked, th=t: self._set_theme(th))

        rm = mb.addMenu("&Run")
        self._action(rm, "Step (F10)", "F10", self._step)
        self._action(rm, "Run All (F5)", "F5", self._run_all)
        self._action(rm, "Run to Cursor", "F4", self._run_to_cursor)
        self._action(rm, "Stop", "Shift+F5", self._stop_run)
        self._action(rm, "Reset CPU (F6)", "F6", self._reset)
        rm.addSeparator()
        self._action(rm, "Toggle Breakpoint", "F9", lambda: self._toggle_bp(self.editor.textCursor().blockNumber()+1))
        self._action(rm, "Clear All Breakpoints", "", self._clear_breakpoints)

        hm = mb.addMenu("&Help")
        self._action(hm, "Keyboard Shortcuts", "F1", self._show_shortcuts)
        self._action(hm, "About", "", self._show_about)

    def _action(self, menu, text, shortcut, callback):
        a = QAction(text, self)
        if shortcut: a.setShortcut(QKeySequence(shortcut))
        a.triggered.connect(callback); menu.addAction(a); return a

    # ---- TOOLBAR ----
    def _build_toolbar(self):
        tb = self.addToolBar("Main"); tb.setMovable(False); tb.setIconSize(QSize(20,20))
        self.act_reset = QToolButton(); self.act_reset.setText("Reset"); self.act_reset.setToolTip("Reset CPU (F6)")
        self.act_reset.clicked.connect(self._reset); tb.addWidget(self.act_reset)
        tb.addSeparator()
        self.act_step = QToolButton(); self.act_step.setText("Step"); self.act_step.setToolTip("Step (F10)")
        self.act_step.clicked.connect(self._step); tb.addWidget(self.act_step)
        self.act_run = QToolButton(); self.act_run.setText("Run All"); self.act_run.setToolTip("Run All (F5)")
        self.act_run.clicked.connect(self._run_all); tb.addWidget(self.act_run)
        self.act_stop = QToolButton(); self.act_stop.setText("Stop"); self.act_stop.setToolTip("Stop (Shift+F5)")
        self.act_stop.clicked.connect(self._stop_run); self.act_stop.setEnabled(False); tb.addWidget(self.act_stop)
        tb.addSeparator()
        self.act_run_to = QToolButton(); self.act_run_to.setText("Run to Cursor"); self.act_run_to.setToolTip("Run to Cursor (F4)")
        self.act_run_to.clicked.connect(self._run_to_cursor); tb.addWidget(self.act_run_to)
        tb.addSeparator()
        tb.addWidget(QLabel(" Speed:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal); self.speed_slider.setRange(20,1000)
        self.speed_slider.setValue(200); self.speed_slider.setFixedWidth(100)
        self.speed_slider.setToolTip("Auto-run delay (ms)"); self.speed_slider.valueChanged.connect(self._set_speed)
        tb.addWidget(self.speed_slider)
        self.speed_label = QLabel("200ms"); self.speed_label.setFixedWidth(50); tb.addWidget(self.speed_label)
        tb.addSeparator()
        for t in Theme.available_themes():
            b = QToolButton(); b.setText(t.capitalize()); b.setCheckable(True); b.setChecked(t == Theme._current)
            b.setToolTip(f"Switch to {t} theme")
            b.clicked.connect(lambda checked, th=t: self._set_theme(th))
            tb.addWidget(b)

    # ---- STATUS BAR ----
    def _build_statusbar(self):
        sb = self.statusBar()
        self.sb_pos = QLabel("Line 1"); sb.addWidget(self.sb_pos)
        self.sb_cycles = QLabel("Cycles: 0"); sb.addPermanentWidget(self.sb_cycles)
        self.sb_steps = QLabel("Steps: 0"); sb.addPermanentWidget(self.sb_steps)
        self.sb_stars = QLabel("Stars: 0"); sb.addPermanentWidget(self.sb_stars)
        self.sb_theme = QLabel("Dark"); sb.addPermanentWidget(self.sb_theme)

    # ---- SIGNAL CONNECTIONS ----
    def _connect_signals(self):
        self.editor.cursorPositionChanged.connect(self._update_cursor_pos)
        self.editor.textChanged.connect(self._update_pseudocode)
        self.lesson_panel.lesson_changed.connect(self._on_lesson_changed)
        self.lesson_panel.challenge_requested.connect(self._start_challenge)
        self.lesson_panel.load_btn.clicked.connect(self._load_template)
        self.snippets_panel.snippet_selected.connect(self._insert_snippet)
        self.editor.breakpoint_toggled.connect(self._on_bp_toggled)

    # ---- CORE EXECUTION LOGIC ----
    def _step(self):
        if not self.cpu.program:
            self._load_code_to_cpu()
        if self.cpu.current_line >= len(self.cpu.program):
            self.console.log("Program finished.", "success"); self._stop_run(); return
        self.state_stack.append(self.cpu.get_state_snapshot())
        if len(self.state_stack) > 200: self.state_stack.pop(0)

        line = self.cpu.program[self.cpu.current_line]
        reg_before = {k: v.value for k, v in self.cpu.registers.items()}

        try:
            msg, cyc, jump = self.cpu.execute_line(line)
            self.cpu.total_cycles += cyc
            self.stats.record_execution(line.strip().split()[0].upper() if line.strip() and not line.strip().startswith(";") else "", True)
            flags_after = {k: v.value for k, v in self.cpu.flags.items()}
            reg_after = {k: v.value for k, v in self.cpu.registers.items()}
            if msg not in ("Skipped", "Label", "Empty"):
                rec = ExecutionRecord(self.cpu.current_line, line.strip(), msg, reg_before, reg_after, flags_after, datetime.now().isoformat(), cyc)
                self.cpu.execution_history.append(rec)
                self.history_table.add_record(rec)
                self.console.log(f"[{self.cpu.current_line+1}] {msg}", "info")
                self.reg_graph.record()
            if jump is not None:
                self.cpu.current_line = jump
            else:
                self.cpu.current_line += 1
        except (ValueError, RuntimeError) as ex:
            self.console.log(f"[{self.cpu.current_line+1}] ERROR: {ex}", "error")
            self.stats.record_execution(line.strip().split()[0].upper() if line.strip() else "", False)
            self.cpu.current_line += 1

        next_line = self.cpu.current_line + 1
        if next_line in self.cpu.breakpoints and next_line <= len(self.cpu.program):
            self.console.log(f"Breakpoint hit at line {next_line}", "warning")
            if self.cpu.running: self._stop_run()

        if self.cpu.current_line >= len(self.cpu.program):
            self.console.log("Program finished.", "success")
            if self.cpu.running: self._stop_run()

        self._update_display()
        if self.cpu.current_line >= len(self.cpu.program):
            self._check_lesson()

    def _run_all(self):
        if not self.cpu.program: self._load_code_to_cpu()
        if self.cpu.current_line >= len(self.cpu.program):
            self._reset(); self._load_code_to_cpu()
        self.cpu.running = True
        self.act_run.setEnabled(False); self.act_stop.setEnabled(True)
        self.run_timer.start(self._run_speed)
        self.console.log("Running...", "header")

    def _run_step(self):
        if not self.cpu.running: return
        if self.cpu.current_line >= len(self.cpu.program):
            self._stop_run(); return
        self._step()

    def _run_to_cursor(self):
        cursor_line = self.editor.textCursor().blockNumber() + 1
        if not self.cpu.program: self._load_code_to_cpu()
        self.cpu.running = True; self.act_run.setEnabled(False); self.act_stop.setEnabled(True)
        self.run_timer.start(self._run_speed)
        self.cpu.breakpoints[cursor_line] = Breakpoint(cursor_line)
        self.console.log(f"Running to line {cursor_line}...", "header")

    def _stop_run(self):
        self.run_timer.stop(); self.cpu.running = False
        self.act_run.setEnabled(True); self.act_stop.setEnabled(False)
        self.console.log("Stopped.", "muted")

    def _reset(self):
        self._stop_run(); self.cpu.reset(); self.state_stack.clear()
        self.history_table.clear_history(); self.reg_graph.clear()
        self.editor.set_pc_line(-1)
        self._update_display()
        self.console.log("CPU reset.", "warning")

    def _load_code_to_cpu(self):
        code = self.editor.toPlainText()
        self.cpu.load_program(code)
        self.console.log(f"Program loaded: {len(self.cpu.program)} lines, {len(self.cpu.labels)} labels found.", "info")
        labels = self.editor.get_labels()
        if labels:
            words = list(INSTRUCTION_DB.keys()) + list(JUMP_ALIASES.keys()) + \
                    ["eax","ebx","ecx","edx","esi","edi","esp","ebp","eip"] + labels
            self.editor._completer = QCompleter(words, self.editor)
            self.editor._completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.editor._completer.setWidget(self.editor)
            self.editor._completer.activated.connect(self.editor._insert_completion)

    def _undo_state(self):
        if not self.state_stack:
            self.console.log("Nothing to undo.", "warning"); return
        snap = self.state_stack.pop()
        self.cpu.restore_state(snap)
        self.console.log("Undone to previous state.", "info")
        self._update_display()

    # ---- DISPLAY UPDATE ----
    def _update_display(self):
        for name, w in self.reg_widgets.items(): w.update_value()
        for name, w in self.flag_widgets.items(): w.update_value()
        self.binary_viz.update(); self.stack_viz.update()
        self.editor.set_pc_line(self.cpu.current_line + 1)
        self.watch_panel.refresh()
        self.sb_cycles.setText(f"Cycles: {self.cpu.total_cycles}")
        self.sb_steps.setText(f"Steps: {len(self.cpu.execution_history)}")
        self.sb_stars.setText(f"Stars: {self.stats.total_stars}")

    def _update_cursor_pos(self):
        c = self.editor.textCursor()
        self.sb_pos.setText(f"Line {c.blockNumber()+1}, Col {c.columnNumber()+1}")

    def _update_pseudocode(self):
        code = self.editor.toPlainText()
        pseudo = PseudocodeTranslator.translate(code)
        self.pseudo_edit.setPlainText(pseudo)

    # ---- LESSON SYSTEM ----
    def _on_lesson_changed(self, idx):
        self.lesson_panel.set_lesson(idx)
        self._reset()

    def _load_template(self):
        l = LESSONS[self.lesson_panel.idx]
        if l.code_template:
            self.editor.setPlainText(l.code_template)
            self.console.log(f"Loaded template for {l.title}", "info")

    def _check_lesson(self):
        l = LESSONS[self.lesson_panel.idx]
        passed = True
        if l.expected_eax is not None:
            if self.cpu.registers["eax"].value != (l.expected_eax & 0xFFFFFFFF):
                passed = False; self.console.log(f"Expected EAX={l.expected_eax:#x}, got {self.cpu.registers['eax'].value:#x}", "error")
            else:
                self.console.log(f"EAX check passed! ({l.expected_eax:#x})", "success")
        if l.expected_flags:
            for fn, fv in l.expected_flags.items():
                actual = self.cpu.flags[fn].value
                if actual != fv:
                    passed = False; self.console.log(f"Expected {fn}={fv}, got {actual}", "error")
                else:
                    self.console.log(f"{fn} check passed! ({fv})", "success")
        if passed:
            self.console.log(f"Lesson objective COMPLETED!", "success")
            self.stats.record_lesson(self.lesson_panel.idx)
            expected = {}
            if l.expected_eax is not None: expected["EAX"] = f"{l.expected_eax & 0xFFFFFFFF:#010x}"
            if l.expected_flags:
                for fn, fv in l.expected_flags.items(): expected[fn] = str(fv)
            actual = {}
            if l.expected_eax is not None: actual["EAX"] = f"{self.cpu.registers['eax'].value:#010x}"
            if l.expected_flags:
                for fn in l.expected_flags: actual[fn] = str(self.cpu.flags[fn].value)
            if expected: self.diff_viewer.show_diff(expected, actual); self.diff_dock.show()

    def _start_challenge(self):
        l = LESSONS[self.lesson_panel.idx]
        if not l.challenge_time: return
        self._reset()
        if l.code_template: self.editor.setPlainText(l.code_template)
        self.challenge_dialog = ChallengeDialog(l, self)
        self.challenge_dialog.completed.connect(self._challenge_done)
        self.challenge_dialog.show()

    def _challenge_done(self, stars, time_taken):
        self.stats.record_challenge(stars)
        self.console.log(f"Challenge completed! {'*'*stars}{'.'*(3-stars)} in {time_taken}s", "success")
        self.sb_stars.setText(f"Stars: {self.stats.total_stars}")
        self._load_code_to_cpu()
        self.cpu.running = True
        while self.cpu.current_line < len(self.cpu.program) and self.cpu.running:
            line = self.cpu.program[self.cpu.current_line]
            try:
                msg, cyc, jump = self.cpu.execute_line(line)
                self.cpu.total_cycles += cyc
                if jump is not None: self.cpu.current_line = jump
                else: self.cpu.current_line += 1
            except: self.cpu.current_line += 1
        self.cpu.running = False
        self._update_display()
        self._check_lesson()
        self.stats.record_lesson(self.lesson_panel.idx, stars, time_taken)

    # ---- BREAKPOINTS ----
    def _toggle_bp(self, line):
        if line in self.editor.breakpoints:
            self.editor.breakpoints.remove(line)
            self.console.log(f"Breakpoint removed at line {line}", "muted")
        else:
            self.editor.breakpoints.add(line)
            self.console.log(f"Breakpoint set at line {line}", "info")
        self.editor.ln_area.update()

    def _on_bp_toggled(self, line, added):
        self.console.log(f"Breakpoint {'set' if added else 'removed'} at line {line}", "muted")

    def _clear_breakpoints(self):
        self.editor.breakpoints.clear(); self.cpu.breakpoints.clear()
        self.editor.ln_area.update()
        self.console.log("All breakpoints cleared.", "info")

    # ---- FILE I/O ----
    def _new_file(self):
        if self.editor.toPlainText().strip() and self.current_file is None:
            r = QMessageBox.question(self, "New", "Discard current code?")
            if r != QMessageBox.StandardButton.Yes: return
        self.editor.clear(); self.current_file = None
        self.setWindowTitle("Assembly Learning Lab v5.0")
        self.console.log("New file.", "info")

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Assembly", "", "Assembly Files (*.asm *.s *.txt);;All Files (*)")
        if path:
            try:
                with open(path, "r") as f: self.editor.setPlainText(f.read())
                self.current_file = path; self.stats.files_loaded += 1
                self._add_recent(path)
                self.setWindowTitle(f"Assembly Lab - {os.path.basename(path)}")
                self.console.log(f"Opened: {path}", "success")
            except Exception as e: self.console.log(f"Error opening: {e}", "error")

    def _save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as f: f.write(self.editor.toPlainText())
                self.stats.files_saved += 1
                self.console.log(f"Saved: {self.current_file}", "success")
            except Exception as e: self.console.log(f"Error saving: {e}", "error")
        else: self._save_file_as()

    def _save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Assembly", "code.asm", "Assembly Files (*.asm *.s);;All Files (*)")
        if path:
            try:
                with open(path, "w") as f: f.write(self.editor.toPlainText())
                self.current_file = path; self.stats.files_saved += 1; self._add_recent(path)
                self.setWindowTitle(f"Assembly Lab - {os.path.basename(path)}")
                self.console.log(f"Saved: {path}", "success")
            except Exception as e: self.console.log(f"Error: {e}", "error")

    def _add_recent(self, path):
        if path in self.recent_files: self.recent_files.remove(path)
        self.recent_files.insert(0, path)
        self.recent_files = self.recent_files[:5]
        self._update_recent_menu()

    def _update_recent_menu(self):
        self.recent_menu.clear()
        if not self.recent_files:
            a = self.recent_menu.addAction("(none)"); a.setEnabled(False); return
        for p in self.recent_files:
            a = self.recent_menu.addAction(os.path.basename(p))
            a.setToolTip(p); a.triggered.connect(lambda checked, path=p: self._open_recent(path))

    def _open_recent(self, path):
        try:
            with open(path, "r") as f: self.editor.setPlainText(f.read())
            self.current_file = path; self.stats.files_loaded += 1
            self.setWindowTitle(f"Assembly Lab - {os.path.basename(path)}")
            self.console.log(f"Opened: {path}", "success")
        except Exception as e: self.console.log(f"Error: {e}", "error")

    # ---- EXPORT ----
    def _export_html(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export HTML Report", "report.html", "HTML (*.html)")
        if path:
            html = ExportManager.to_html(self.cpu, self.editor.toPlainText(), self.cpu.execution_history, self.stats)
            with open(path, "w") as f: f.write(html)
            self.console.log(f"Exported to {path}", "success")
            webbrowser.open(f"file://{path}")

    # ---- THEME ----
    def _set_theme(self, theme):
        Theme.set_mode(theme); self._apply_theme()
        self.settings.setValue("theme", theme)
        self.sb_theme.setText(theme.capitalize())
        self.console.log(f"Theme: {theme}", "muted")
        self.editor.highlighter.rehighlight()

    def _apply_theme(self):
        self.setStyleSheet(Theme.stylesheet())
        for w in self.reg_widgets.values(): w.refresh_style()
        for w in self.flag_widgets.values(): w.update_value()
        self.sb_theme.setText(Theme._current.capitalize())

    # ---- SNIPPETS ----
    def _insert_snippet(self, code):
        self.editor.setPlainText(code)
        self.console.log("Snippet loaded.", "info")

    # ---- HELPERS ----
    def _change_font(self, delta):
        f = self.editor.font(); sz = max(8, f.pointSize() + delta)
        self.editor.setFont(QFont(f.family(), sz))
        self.console.log(f"Font size: {sz}pt", "muted")

    def _copy_pseudo(self):
        cb = QApplication.clipboard(); cb.setText(self.pseudo_edit.toPlainText())
        self.console.log("Pseudocode copied to clipboard.", "info")

    def _set_speed(self, val):
        self._run_speed = val; self.speed_label.setText(f"{val}ms")
        if self.run_timer.isActive(): self.run_timer.setInterval(val)

    def _show_shortcuts(self):
        QMessageBox.information(self, "Keyboard Shortcuts",
            "<h3>Keyboard Shortcuts</h3>"
            "<table style='font-family:monospace;font-size:11pt'>"
            "<tr><td><b>F5</b></td><td>Run All (auto-step)</td></tr>"
            "<tr><td><b>F10</b></td><td>Step (single instruction)</td></tr>"
            "<tr><td><b>F6</b></td><td>Reset CPU</td></tr>"
            "<tr><td><b>F9</b></td><td>Toggle breakpoint</td></tr>"
            "<tr><td><b>F4</b></td><td>Run to cursor</td></tr>"
            "<tr><td><b>Shift+F5</b></td><td>Stop running</td></tr>"
            "<tr><td><b>Ctrl+N</b></td><td>New file</td></tr>"
            "<tr><td><b>Ctrl+O</b></td><td>Open file</td></tr>"
            "<tr><td><b>Ctrl+S</b></td><td>Save file</td></tr>"
            "<tr><td><b>Ctrl+Z</b></td><td>Undo CPU state</td></tr>"
            "<tr><td><b>Ctrl+E</b></td><td>Export HTML report</td></tr>"
            "<tr><td><b>Ctrl+L</b></td><td>Clear console</td></tr>"
            "<tr><td><b>Tab</b></td><td>Insert 4 spaces / accept autocomplete</td></tr>"
            "<tr><td><b>Click gutter</b></td><td>Toggle breakpoint</td></tr>"
            "</table>")

    def _show_about(self):
        arm_count = len(_RAW_DATA.get("arm", {}))
        riscv_count = len(_RAW_DATA.get("riscv", {}))
        mips_count = len(_RAW_DATA.get("mips", {}))
        QMessageBox.about(self, "About",
            "<h2>Assembly Learning Lab v5.0</h2>"
            "<p>A comprehensive multi-architecture assembly learning environment.</p>"
            f"<p>x86: {len(INSTRUCTION_DB)} | ARM: {arm_count} | RISC-V: {riscv_count} | MIPS: {mips_count}</p>"
            f"<p>Lessons: {len(LESSONS)} | Snippets: {len(CODE_SNIPPETS)} | Concepts: {len(_RAW_DATA.get('concepts', []))}</p>"
            "<p>Built with PySide6.</p>")

    def closeEvent(self, event):
        self._stop_run()
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        super().closeEvent(event)


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Assembly Learning Lab")
    app.setOrganizationName("AssemblyLab")

    # Try to load JetBrains Mono, fallback to monospace
    fonts = QFontDatabase.families()
    if "JetBrains Mono" not in fonts:
        for alt in ["Fira Code", "Cascadia Code", "Consolas", "DejaVu Sans Mono", "Courier New"]:
            if alt in fonts:
                break

    window = AssemblyLab()

    # Restore geometry
    if window.settings.value("geometry"):
        window.restoreGeometry(window.settings.value("geometry"))
    if window.settings.value("windowState"):
        window.restoreState(window.settings.value("windowState"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()