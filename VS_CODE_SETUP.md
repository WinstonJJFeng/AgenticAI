# VS Code/Cursor Setup Guide for Python ML Development

## ✅ Setup Complete!

Your VS Code/Cursor environment is now configured for Python machine learning development.

## 📦 Installed Configuration Files

1. **`.vscode/launch.json`** - Debugging configurations
2. **`.vscode/settings.json`** - Python and Jupyter settings
3. **`.vscode/extensions.json`** - Recommended extensions
4. **`requirements.txt`** - Python dependencies

## 🔧 Required VS Code Extensions

Open the Command Palette (Cmd+Shift+P) and run:
- `Extensions: Show Recommended Extensions`

Or install manually:
1. **Python** (ms-python.python) - Core Python support
2. **Pylance** (ms-python.vscode-pylance) - Fast Python language server
3. **Jupyter** (ms-toolsai.jupyter) - Jupyter notebook support
4. **Python Debugger** (ms-python.debugpy) - Debugging support
5. **Black Formatter** (ms-python.black-formatter) - Code formatting
6. **Flake8** (ms-python.flake8) - Linting

## 🐛 How to Debug Python Code

### Debugging Python Scripts (.py files)

1. **Open a Python file** (e.g., `Rilla/debug_example.py`)
2. **Set breakpoints** by clicking to the left of line numbers (red dot appears)
3. **Press F5** or click the "Run and Debug" button
4. **Select "Python: Current File"** from the dropdown
5. Use debugging controls:
   - **F10** - Step Over (execute current line)
   - **F11** - Step Into (enter function calls)
   - **Shift+F11** - Step Out (exit current function)
   - **F5** - Continue execution
   - **Shift+F5** - Stop debugging

### Debugging Jupyter Notebooks (.ipynb files)

#### Method 1: Debug Cell by Cell
1. Open your `.ipynb` file
2. Add breakpoints in code cells (click left of line numbers)
3. Run cells normally - breakpoints will be hit
4. Use Debug Console to inspect variables

#### Method 2: Convert to Python Script
1. Use `# %%` to create cells in `.py` files
2. Debug as regular Python file
3. Example:
```python
# %%
import pandas as pd
# Set breakpoint here

# %%
data = pd.read_csv('file.csv')
# Debug this cell separately
```

### Debug Console Features

When paused at a breakpoint:
- **Inspect variables** - Hover over variable names
- **Evaluate expressions** - Type in Debug Console
- **Watch expressions** - Add variables to Watch panel
- **Call Stack** - See function call hierarchy

## 📝 Working with Jupyter Notebooks

1. **Open .ipynb files** directly in VS Code
2. **Run cells** using:
   - `Shift+Enter` - Run cell and move to next
   - `Ctrl+Enter` - Run cell
   - Code completion works in cells
3. **Variable explorer** - View all variables in notebook
4. **Interactive window** - Run code interactively

## 🎯 Quick Start Guide

### 1. Test Debugging Setup

1. Open `Rilla/debug_example.py`
2. Set a breakpoint on line 18 (`print("Loading manager_data...")`)
3. Press F5
4. Select "Python: Current File"
5. Execution will pause at breakpoint
6. Hover over variables or use Debug Console

### 2. Work with Your Notebooks

1. Open `Rilla/Rilla_reading_local_files_working.ipynb`
2. Run cells to load your data
3. Variables are available across cells
4. Use IntelliSense for code completion

### 3. Create New Scripts

1. Create new `.py` file in `Rilla/` folder
2. Write your code
3. Use F5 to debug
4. Use Ctrl+` to open integrated terminal

## 💡 Tips & Tricks

### Code Formatting
- **Auto-format on save** is enabled
- Uses Black formatter (100 char line length)
- Or format manually: `Shift+Alt+F` (Windows/Linux) or `Shift+Option+F` (Mac)

### Code Quality
- **Flake8 linting** is enabled
- See errors/warnings in Problems panel
- Auto-fix suggestions available

### Terminal Integration
- Press `` Ctrl+` `` to toggle terminal
- Uses zsh on macOS
- Python environment is activated automatically

### Keyboard Shortcuts
- `F5` - Start debugging
- `Shift+F5` - Stop debugging
- `Ctrl+Shift+P` - Command Palette
- `Ctrl+P` - Quick file open
- `Ctrl+` ` - Toggle terminal

## 🔍 Troubleshooting

### Python Interpreter Not Found
1. Press `Cmd+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `python3` or your virtual environment

### Debugging Not Working
1. Check that Python extension is installed
2. Verify breakpoints are set (red dots)
3. Check Debug Console for error messages

### Jupyter Notebook Issues
1. Ensure Jupyter extension is installed
2. Restart VS Code
3. Check that ipykernel is installed: `pip3 install ipykernel`

## 📚 Next Steps

1. **Install recommended extensions** (see above)
2. **Test debugging** with `debug_example.py`
3. **Continue working** with your notebooks
4. **Create new scripts** in `Rilla/` folder as needed

Happy coding! 🚀



