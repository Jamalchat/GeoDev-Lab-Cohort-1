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
