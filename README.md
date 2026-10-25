# Week 3
## 🛠️ Step-by-Step Data Preparation Procedure (QGIS)

### Step 1: Coordinate Reference System (CRS) Verification &amp; Reprojection

1. Open QGIS and load the raw **Delta State LGAs** polygon boundary layer and any secondary layers (e.g., national settlement extents or road networks).
2. Verify the native CRS under `Layer Properties &gt; Information`[3]. The raw layers were defined in **EPSG:4326 (WGS 84)**, which uses angular units (degrees) that are unsuitable for distance or area calculations[3].
3. **Reproject the layer**:
  * Open the **Processing Toolbox** (`Processing &gt; Toolbox`).
  * Navigate to `Vector general &gt; Reproject layer`.
  * Set **Target CRS** to **EPSG:32631 (WGS 84 / UTM Zone 31N)** (or **EPSG:32632**, depending on your specific LGA focus across Delta State).
  * *Note*: Do **not** use `Properties &gt; Source &gt; Assign CRS`, as assigning merely relabels the metadata without recalculating coordinate values.

### Step 2: Running the 5 Data Quality Checks

Before performing spatial operations, run the five standard quality checks on the dataset:

1. **CRS Verification**: Confirm that the target layer displays as a projected system (`UTM Zone 31N`, meters).
2. **Missing/Null Values**: Open the **Attribute Table** and check required fields for `NULL` or missing records.
3. **Duplicate Features**: Check for duplicated LGA entries or overlapping spatial features.
4. **Geometry Validity**: Check vector geometries for self-crossing polygons or invalid ring structures.
5. **Coverage Completeness**: Verify that all 25 LGAs of Delta State are completely covered and no spatial extents cut off prematurely.

### Step 3: Layer Alignment &amp; Clipping

1. Ensure both the overlay boundary (Delta State LGAs) and the input layer (e.g., national settlements or infrastructure) share the same Projected CRS (**EPSG:32631**) before clipping.
2. Open the **Clip tool** via `Processing &gt; Toolbox &gt; Vector overlay &gt; Clip`.
3. Set:
  * **Input layer**: The larger contextual dataset (e.g., national settlement extent).
  * **Overlay layer**: The reprojected Delta State LGAs boundary layer.
4. Run the tool to trim all external data outside Delta State.

### Step 4: Exporting Analysis-Ready GeoPackage

1. Save the clipped output directly to a **GeoPackage (** **.gpkg** **)** container rather than a Shapefile.
2. Name the output file clearly: `delta_state_analysis_ready.gpkg`.
3. Save the file in the `data/processed/` directory of your repository.

---

## 📝 Data Preparation Note &amp; Quality Report

### 1\. Selected CRS and Justification

* **Chosen CRS**: `EPSG:32631 (WGS 84 / UTM Zone 31N)`.
* **Justification**: Delta State lies in South-Western/Southern Nigeria (\~5°E to 6°45'E). Geographic systems (EPSG:4326) store coordinates in angular degrees, making area and distance measurements inaccurate[3]. UTM Zone 31N projects the surface into linear units (meters), making it suitable for accurate spatial analysis across Western and South-Western Nigeria.

### 2\. Operations Performed

* **Reprojected**: Delta State LGA boundary layer and national contextual layer from `EPSG:4326` to `EPSG:32631`.
* **Clipped**: National settlement extent dataset clipped strictly down to the Delta State LGA boundary, removing unnecessary features outside the study area to optimize performance.

### 3\. Results of the 5 Data Quality Checks

| Quality Check                 | Status        | Findings                                                                                                                                                |
| ----------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1\. CRS Correctness**       | **Passed**    | Layer correctly reprojected to EPSG:32631 with units in meters.                                                                               |
| **2\. Null / Missing Values** | **Inspected** | Core administrative attributes (LGA names, state codes) are complete; non-essential statistical fields containing `NULL` values were flagged. |
| **3\. Duplicate Features**    | **Passed**    | Confirmed 25 unique LGA polygon features matching Delta State's administrative divisions with no duplicate IDs.                                    |
| **4\. Geometry Validity**     | **Passed**    | Geometries checked; no invalid self-intersecting lines or topology errors found.                                                                   |
| **5\. Spatial Coverage**      | **Passed**    | Coverage extends across the entire boundary of Delta State without truncation.                                                                     |

### 4\. Problems Encountered &amp; Resolution

* **Issue**: Raw national context layer contained `NULL` attribute fields and spanned across the entire country, slowing down processing.
* **Action Taken**:
  * **Flagged**: Noted non-critical `NULL` fields in the documentation so downstream analyses avoid using those columns.
  * **Fixed**: Applied the `Clip` tool using the reprojected Delta State boundary overlay, removing all features outside the state and speeding up processing.

### 5\. Storage Location of Analysis-Ready Dataset

* **File Path**: `data/processed/delta_state_analysis_ready.gpkg`.
* **Format**: **GeoPackage (** **.gpkg** **)**, stored as a single self-contained file that retains coordinate reference metadata reliably without sidecar file issues.


# Month 2: Preparation of environment, and early Python


## Week 5
* I set up Python. VS Code and terminal. I created a hello.py script, and it runs.

---
# Week 6: 
## Project setup with uv and added pandas. check.py prints the pandas version.
---

This document provides a detailed step-by-step summary and breakdown of **Week 6** in the GeoDev Lab Cohort 1 program. Week 6 focuses on Python package management, virtual environments, project isolation, and environment reproducibility using Astral `uv`.

---

## Overview & Core Concepts

* **Instructor / Channel**: GeoDev Lab Africa
* **Core Topic**: Python Environments and Project Setup with `uv`
* **Core Philosophy**: A clean, isolated environment for every project ensures reproducibility and prevents version conflicts.

---

## Part 1: Theory of Packages & Virtual Environments

### 1. What is a Package?
* **Source Code vs. Package**: The code you write yourself is your **source code** (`src`). A **package** is third-party code written, tested, and shared by others that you install to extend Python's functionality and save development time.
* **Modules vs. Packages**: A single `.py` file is a **module**. A **package** is a collection of one or more modules bundled together with core functions, utilities, and I/O handlers.

### 2. Why Are Virtual Environments Needed?
* **An Isolated Workspace**: A virtual environment (`.venv`) is an isolated folder containing its own dedicated Python interpreter and set of installed packages.
* **Preventing Dependency Conflicts**: Different projects often require different versions of the same library (e.g., Project A needs `pandas 1.0`, while Project B needs `pandas 1.2`). Installing packages globally causes version clashes and breaks workflows.
* **Reproducibility**: Environment configuration files allow collaborators on any machine to rebuild an identical environment.
* **Cheap to Create & Dispose**: Virtual environments take seconds to create and can be deleted and rebuilt cleanly using lockfiles.

### 3. Comparison of Package Managers in Python
| Tool | Developer | Key Features & Trade-offs |
| :--- | :--- | :--- |
| **`pip`** | Python Default | Standard installer included with Python. Cannot manage or create virtual environments natively, is slower, and installs globally by default. |
| **`conda`** | Anaconda | Handles complex binary C/C++ compiled dependencies (e.g., GDAL, GEOS, C/C++ libraries used in AI/deep learning), but can be heavy and slow. |
| **`uv`** | Astral | Modern, extremely fast package manager written in **Rust**. Combines package installation, environment creation, lockfiles, and execution into a single, unified tool. |

---

## Part 2: Installing & Initializing Astral `uv`

### 1. Installation on Windows
* Open **Windows PowerShell** (preferably as Administrator).
* Copy and execute the official Astral installer command from the `uv` documentation.
* Verify installation in the terminal:
  ```bash
  uv --version
  ```

---

## Part 3: The Core `uv` Workflow & Commands

Every `uv`-managed project relies on four fundamental commands:

### 1. `uv init` — Initialising a Project
Running `uv init` inside a folder converts it into a `uv`-managed Python project.

**Key Created Files**:
* **`pyproject.toml`**: The central configuration file. Stores project metadata (name, version, description), required Python version (`>=3.12`), and direct third-party dependencies.
* **`uv.lock`**: The detailed lockfile. Pinpoint records exact package versions, dependency chains, source URLs, `.whl` wheel archives, and SHA cryptographic hashes to guarantee 100% exact environment reproducibility across all operating systems.
* **`main.py`**: Boilerplate starter Python script.
* **`README.md`**: Project documentation file.
* **`.gitignore`**: Specifies files/folders (such as `.venv`) that Git should ignore.
* **`.python-version`**: Specifies the pinned Python version for the project.

### 2. `uv add <package>` — Adding Dependencies
Downloads the package into the local `.venv` directory and automatically records it under `dependencies` in `pyproject.toml`.

```bash
uv add pandas
```
* **Transitive Dependencies**: Installing a top-level package automatically pulls in its required chain of sub-dependencies (e.g., `pandas` automatically installs `numpy`, `python-dateutil`, `six`, and `tzdata`).
* **Explicit vs. Implicit Dependencies**: Following the *Zen of Python* ("Explicit is better than implicit"), directly used packages should be added explicitly with `uv add` even if pulled in by another package (such as `geopandas`).
* **Security Warning (Typosquatting)**: Typos such as `uv add panda` instead of `pandas` can inadvertently install malicious third-party packages into your project.

### 3. `uv run <script.py>` — Executing Scripts
Executes a Python script inside the project's isolated `.venv` environment.

* **`python main.py`**: Uses the system/global Python interpreter. Fails with `ModuleNotFoundError` if packages were installed inside the project environment.
* **`uv run main.py`**: Uses the isolated `.venv` interpreter where project dependencies reside.

### 4. `uv remove <package>` — Removing Dependencies
Uninstalls a third-party package and cleans up its unused transitive dependencies from `.venv` and `pyproject.toml`.

```bash
uv remove pandas
```

### 5. `uv sync` — Rebuilding Environments
Reads `pyproject.toml` and `uv.lock` to instantly recreate or sync the virtual environment (`.venv`) if deleted or transferred to a collaborator's machine.

---

## Part 4: Hands-On Data Processing Examples

### 1. Tabular Data with Pandas
Reading structured CSV datasets using pandas:

```python
import pandas as pd

# Read CSV dataset into a DataFrame
df = pd.read_csv("states.csv")

# Print DataFrame details
print(f"Pandas Version: {pd.__version__}")
print(df.head())       # Display first 5 rows
print(df.describe())   # Statistical summary of numerical columns (e.g., area)
print(df.info())       # Column data types and non-null counts
```

### 2. Spatial Data with GeoPandas
Reading vector spatial datasets (GeoJSON) using GeoPandas:

```python
import geopandas as gpd

# Read vector dataset into a GeoDataFrame
gdf = gpd.read_file("Africa_countries.geojson")

# Inspect spatial metadata and geometry
print(f"Shape (rows, cols): {gdf.shape}")  # e.g., (54, 6)
print(gdf.head())                           # Includes attribute columns + 'geometry'
```

# Week 7 

## analyse.py reads wards.csv, converts each area and classifies each ward

This document provides a detailed step-by-step summary and breakdown of **Week 7** in the GeoDev Lab Cohort 1 program. Week 7 bridges foundational programming theory with real-world spatial data processing using Python and `uv`.

---

## Overview & The Golden Rule

* **Instructor**: Williams (GeoDev Lab Africa) [10]
* **Core Philosophy**: *"Type everything yourself—don't copy and paste a single line."* Hands and eyes learn by typing.
* **Execution Environment**: Scripts are run inside isolated project environments using the `uv` tool via terminal (`uv run script.py`).
* **Scratchpad vs. Script**: `learn.py` is used as an unsubmitted scratchpad for learning concepts, while `analyse.py` and `wards.csv` form the final submitted program.

---

## Part 1: The Six Core Programming Ideas

Every Python program ever written is built from six fundamental concepts:

### 1. Variables
* **Definition**: A variable is a named memory location in RAM—a labelled box holding a data value.
* **Assignment Operator (`=`)**: Assigns a value to a variable name (e.g., `state = "Oyo"`).
* **Naming Rules & Conventions**:
  * Use lowercase letters with underscores for multi-word names (`buffer_distance`, `ward_name`).
  * Cannot contain spaces or start with numbers.
  * Names are case-sensitive (`State` $\neq$ `state`).
* **Sequential Execution**: Python executes line by line from top to bottom. Updating a variable overwrites its previous contents.

```python
# Variable assignment and reassignment
state = "Oyo"
print(state)  # Outputs: Oyo

state = "Lagos"
print(state)  # Outputs: Lagos
```

---

### 2. Data Types
Data types dictate what operations Python can perform on a value.

| Data Type | Class | Description | Example |
| :--- | :--- | :--- | :--- |
| **String** | `str` | Text enclosed in matching quotes (`"` or `'`) | `"Bodija"`, `"12.4"` |
| **Integer** | `int` | Whole numbers without decimals or commas | `774`, `100` |
| **Float** | `float` | Numbers containing decimal points | `3080.5`, `12.4` |
| **Boolean** | `bool` | Logical truth values (must be capitalized) | `True`, `False` |

* **Type Checking**: Use `type(variable)` to inspect data types.
* **Type Conversion**: Data read from files arrives as strings. Use `float()` or `int()` to convert strings into numbers before doing math.
* **Concatenation vs. Addition**:
  * `"5" + "5"` $\rightarrow$ `"55"` (string concatenation).
  * `5 + 5` $\rightarrow$ `10` (numeric addition).

```python
# Type conversion example
area_text = "12.4"              # String read from file
area_num = float(area_text)     # Convert to float number
area_ha = area_num * 100        # Unit conversion (1240.0)
```

---

### 3. Lists
* **Definition**: Ordered collections of items enclosed in square brackets `[...]` and separated by commas.
* **Zero-Based Indexing**: Python counts positions starting at `0`.
  * First item: `items[0]`
  * Second item: `items[1]`
* **List Methods & Functions**:
  * `len(my_list)`: Returns the total number of items.
  * `my_list.append(item)`: Adds a new item to the end of the list.
* **IndexError**: Requesting an index that does not exist (e.g., `words[4]` on a 4-item list) raises an `IndexError: list index out of range`.

```python
wards = ["Agodi", "Bodija", "Sabo", "Mokola"]
print(len(wards))    # 4
print(wards[0])      # "Agodi"
wards.append("Ojoo") # Adds "Ojoo" to the list
```

---

### 4. Loops
* **Definition**: A structure that repeats a block of code for every item in a list or sequence.
* **Indentation Rules**: In Python, 4 spaces of indentation define code belonging inside the loop block. Outdented code runs after the loop completes.

```python
areas = [12.4, 8.1, 5.7, 9.3]
for area in areas:
    ha = area * 100
    print(f"{area} sq km is {ha} hectares")
print("Done processing all areas.") # Runs once after loop finishes
```

---

### 5. Conditional Statements & Logic
* **Definition**: Allows code to make decisions based on boolean checks (`if`, `elif`, `else`).
* **Comparison Operators**:
  * `==` : Checks equality (`state == "Oyo"`).
  * `!=` : Checks inequality (`state != "Lagos"`).
  * `>`, `<`, `>=`, `<=`: Numeric comparison checks.

```python
area = 12.4
if area > 9:
    size = "large"
else:
    size = "small"
print(f"Ward size: {size}")
```

---

### 6. Functions
* **Definition**: Reusable, named blocks of code defined using the `def` keyword that return outputs using `return`.
* **Parameters & Scope**:
  * Functions accept input arguments.
  * Variables created inside functions exist in local scope.

```python
def sqkm_to_hectares(area_sqkm):
    return area_sqkm * 100

print(sqkm_to_hectares(12.4)) # 1240.0
```

---

## Debugging: The 5 Common Python Error Types

When a script fails, **always read the last line of the terminal traceback first**, then check the line number listed directly above it.

1. **`NameError`**: Calling a variable or function name that has not been defined or contains a typo (e.g., `total` vs `total_area`).
2. **`TypeError`**: Operating on incompatible data types, such as attempting string concatenation on an integer without `str()`.
3. **`IndentationError`**: Missing the required 4-space indentation block after `for`, `if`, or `def` lines.
4. **`SyntaxError`**: Missing colons (`:`) at the end of loop/condition headers or mismatched quotation marks.
5. **`ValueError`**: Invalid type conversion, such as passing a decimal string `"12.4"` directly to `int()` instead of `float()`.

---

## Part 2: Hands-On Practical (Building `analyse.py`)

In Part 2, all six ideas are integrated into a working spatial analysis program that reads `wards.csv`, converts units, classifies wards, and prints results [1, 8].

### Step 1: Create the Data File (`wards.csv`)
Create a plain text CSV file with column headers and no extra spaces around commas:

```csv
ward,area_km2
Agodi,12.4
Bodija,8.1
Sabo,5.7
Mokola,9.3
```

---

### Step 2: Build the Processing Script (`analyse.py`)
Write the complete script combining file I/O, list slicing, string cleaning, type casting, arithmetic, and conditional logic:

```python
# Step 1: Open the CSV file safely using a context manager
with open("wards.csv") as f:
    lines = f.readlines()

# Step 2: Skip the header row using list slicing lines[1:] and loop over data rows
for line in lines[1:]:
    # Step 3: Strip newline characters and split row by commas
    parts = line.strip().split(",")
    ward = parts[0]
    
    # Step 4: Cast area text string to float
    area = float(parts[1])
    
    # Step 5: Apply conditional logic threshold (> 9 km2)
    if area > 9:
        size = "large"
    else:
        size = "small"
        
    # Step 6: Display result
    print(f"{ward} is {size}")
```

---

### Step 3: Terminal Execution & Output Verification

Run the completed script using `uv`:

```bash
uv run analyse.py
```

**Expected Terminal Output**:
```text
Agodi is large
Bodija is small
Sabo is small
Mokola is large
```

# Week 8

## inspect_data.py summarises states.csv into the smallest, largest, and number of states

This document provides a detailed step-by-step summary and breakdown of **Week 8** in the GeoDev Lab Cohort 1 program. Week 8 marks the transition from basic synthetic examples to inspecting and cleaning real-world spatial datasets gathered in Month 1 using Python, `csv.DictReader`, dictionaries, and `uv`.

---

## Overview & Core Philosophy

* **Instructor**: Williams Adajan (GeoDev Lab Africa)
* **Milestone**: "Where Month 1 and Month 2 meet"—pointing the six core Python programming concepts at real messy GIS data.
* **Golden Debugging Habit**: Always read the last line of the error traceback first, and use `print()` statements to inspect variables at runtime whenever logic produces unexpected values.
* **Scratchpad vs. Script**: `l.py` / `learn.py` serves as the practice scratchpad, while `inspect_data.py` and your dataset CSV form the final submitted program.

---

## Part 1: Core Theoretical Concepts

### 1. `print()` vs. `return` (The Single Most Common Beginner Mistake)
Functions can display information or pass data back to the calling program, but they behave fundamentally differently in memory:

* **`print()`**: Displays a value on the screen/terminal for visual inspection. It does **not** return a value to memory. Assigning the result of a printing function to a variable stores `None`.
* **`return`**: Sends a calculated result back to the caller, allowing it to be stored in a variable and used in downstream calculations.
* **The `NoneType` Error**: Attempting math on a variable assigned to a function that only printed results in a `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`.

```python
# Function with print (returns None)
def with_print(x):
    print(x * 100)

a = with_print(5)  # Prints 500, but 'a' holds None!

# Function with return (saves to memory)
def with_return(x):
    return x * 100

b = with_return(5) # 'b' holds 500
print(b + 1)       # Outputs: 501
```

---

### 2. Reading CSV Files: String Splitting vs. `csv.DictReader`
While `split(",")` works for basic, uniform CSVs, real data requires robust parsing tools:

* **Problem with `split(",")`**: If a cell contains a comma inside quotes (e.g., `"Ibadan, Oyo"`), `split(",")` splits that single cell into two separate elements, corrupting column alignments without throwing an explicit syntax error.
* **Solution (`csv.DictReader`)**: Reads each row as a Python dictionary. Values are accessed by their exact column header name (e.g., `row["area_km2"]`), ignoring column ordering shifts and respecting quoted text commas.

---

### 3. Handling Invisible Character Markers (`encoding="utf-8-sig"`)
External software like Microsoft Excel or QGIS frequently embeds an invisible Byte Order Mark (BOM) (`\ufeff`) at the beginning of exported CSV files.

* **Symptom**: Python raises a `KeyError: 'ward'` even though the `'ward'` header is visually visible in the CSV editor.
* **Fix**: Always open CSV files using `encoding="utf-8-sig"`. This instructs Python to detect and automatically strip invisible BOM markers:

```python
import csv

with open("Places.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["ward"])
```

---

### 4. Working with Dictionaries
Dictionaries store data using descriptive **key-value pairs** inside curly braces `{}`.

* **Lists vs. Dictionaries**: Lists hold multiple ordered items accessed by integer positions (`list[0]`). Dictionaries hold properties of an entity accessed by descriptive string labels (`dict["area"]`).
* **Accessing & Modifying**:
  * Read value: `ward["area"]`.
  * Add or update key: `ward["population"] = 45000`.
  * Iterating keys/values: `for key, value in ward.items():`.
* **`KeyError`**: Accessing a non-existent key raises a `KeyError`.

---

### 5. Working with JSON Data
JSON (JavaScript Object Notation) is a semi-structured hierarchical data format widely used for web APIs and spatial GeoJSON files.

* **Reading JSON**: Use `import json` and `json.load(f)`. Python automatically parses JSON objects into nested dictionaries and lists.
* **Numeric Integrity**: Unlike CSV files where all cell values arrive as strings (`str`), JSON preserves native numbers (`int`, `float`) without requiring manual type casting.

---

### 6. Logical Bugs & Debugging with `print()`
Logical bugs occur when code executes cleanly without errors, but produces mathematically incorrect results.

* **Common Pitfall**: Resetting accumulator variables (like `total = 0`) *inside* a `for` loop instead of *outside*, causing only the last loop iteration's value to survive.
* **Debugging Strategy**: Place temporary `print()` statements inside loops to monitor variable progression at each step.

---

### 7. Data Cleaning: Handling Messy & Missing Data
Real data contains whitespace padding, empty cells, `"NA"` strings, and thousands-separator commas.

* **Stripping Whitespace**: Use `.strip()` to clean leading and trailing spaces from text inputs.
* **Removing Commas**: Numbers like `"5,580,894"` fail during `float()` conversion. Use `.replace(",", "")` first.
* **Handling Empty Cells & `"NA"`**: Attempting `float("")` or `float("NA")` raises a `ValueError` [42]. Use `if not raw_val or raw_val == "NA": continue` to log and skip invalid cells gracefully.
* **Honest Data Reporting**: Track and report the count of skipped rows so stakeholders know how many rows were excluded.

---

## Part 2: Hands-On Practical (`inspect_data.py`)

In Part 2, a complete data inspection script is constructed to read a CSV dataset, clean numeric columns, skip missing entries, and calculate summary metrics using dictionaries.

### Step 1: Naming the Script (`inspect_data.py` vs `inspect.py`)
* **Crucial Rule**: Name the script **`inspect_data.py`**, **never `inspect.py`**.
* **Reason**: Python contains a built-in standard library module named `inspect`. Creating a local file named `inspect.py` causes module shadowing (a name collision), breaking Python's internal imports.

---

### Step 2: Complete Code Implementation (`inspect_data.py`)

Below is the complete, clean script structure for reading a dataset, cleaning numeric values, and returning summary dictionaries:

```python
import csv

def inspect_column(file_name, column_name):
    """
    Opens a CSV file, cleans numeric values for a specified column,
    skips empty/missing cells, and returns a summary dictionary.
    """
    values = []
    skipped_count = 0

    with open(file_name, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Extract raw string value and strip whitespace
            raw_val = row[column_name].strip()

            # Skip empty cells or 'NA' entries
            if not raw_val or raw_val == "NA":
                skipped_count += 1
                continue

            # Remove thousands-separator commas and convert to float
            clean_val = float(raw_val.replace(",", ""))
            values.append(clean_val)

    # Return summary dictionary
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": round(sum(values) / len(values), 2),
        "skipped": skipped_count
    }

# Execute function for two distinct numeric columns
col1_summary = inspect_column("states.csv", "area_km2")
col2_summary = inspect_column("states.csv", "lgas")

# Print summary dictionaries to terminal
print("Column 1 Summary:", col1_summary)
print("Column 2 Summary:", col2_summary)
```

---

### Step 3: Terminal Execution & Verification

Run the inspection script inside your project environment using `uv`:

```bash
uv run inspect_data.py
```

**Expected Terminal Output**:
```text
Column 1 Summary: {'count': 10, 'min': 5.7, 'max': 12.4, 'avg': 8.88, 'skipped': 0}
Column 2 Summary: {'count': 10, 'min': 150.0, 'max': 450.0, 'avg': 285.5, 'skipped': 0}
```

---
