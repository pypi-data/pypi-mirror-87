# Installation
Download from PiPY

pip install ltool

# Input
The ltools module requires an SCC database file as input.
The paths an options to log in the SCC database file and the output folders must be specified in the configuration file

Run the script as:

ltool -m <measurement_ID> -c <full_path_to_settings_file>

# Output
A netCDF file is produced per measurement ID. It contains the layer boundaries and some metrics of the layer (e.g. peak, width etc.)

More specifically the geometrical properties include:

-- "base": the layer base altitude (km)

-- "center_of_mass": the layer center of mass altitude (km)

-- "top": the layer top altitude (km)

-- "peak": the altitude where the profile is max inside the layer (km)

-- "thickness": top - base altitude (km)

-- "base_sig": the optical product value at the base (Mm^-1 sr^-1)

-- "top_sig": the optical product value at the top (Mm^-1 sr^-1)

-- "peak_sig": the optical product value at the peak (Mm^-1 sr^-1)

-- "weight": the ratio of the layer integrated backscatter to the total
integrated backscatter
