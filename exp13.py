import meep as mp
import numpy as np
import matplotlib.pyplot as plt

# Define the simulation cell size
cell_size = mp.Vector3(24, 16, 0)

# Define the PML boundary conditions
pml_layers = [mp.PML(2.0)]

# Define the resolution
resolution = 10

# Create the Meep simulation object
sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=pml_layers,
                    resolution=resolution)

# Define the waveguide parameters
waveguide_width = 1.0
waveguide_length = 10.0

# Define the MZI parameters
splitter_length = 1.0
arm_length = 5.0
phase_shifter_length = 1.0

# Define the waveguide structures
waveguide1 = mp.Block(material=mp.Medium(index=10),
                      size=mp.Vector3(waveguide_length, waveguide_width, mp.inf),
                      center=mp.Vector3(-waveguide_length/2, 0, 0))

waveguide2 = mp.Block(material=mp.Medium(index=10),
                      size=mp.Vector3(waveguide_length, waveguide_width, mp.inf),
                      center=mp.Vector3(waveguide_length/2, 0, 0))

# Add the waveguide structures to the simulation cell
sim.geometry.append(waveguide1)
sim.geometry.append(waveguide2)

# Define the Y splitter structures
splitter1 = mp.Block(material=mp.Medium(index=15),
                     size=mp.Vector3(waveguide_width, splitter_length, mp.inf),
                     center=mp.Vector3(-waveguide_length/2, waveguide_width/2 + splitter_length/2, 0))

splitter2 = mp.Block(material=mp.Medium(index=15),
                     size=mp.Vector3(waveguide_width, splitter_length, mp.inf),
                     center=mp.Vector3(waveguide_length/2, waveguide_width/2 + splitter_length/2, 0))

# Add the Y splitter structures to the simulation cell
sim.geometry.append(splitter1)
sim.geometry.append(splitter2)

# Define the arm structures
arm1 = mp.Block(material=mp.Medium(index=15),
                size=mp.Vector3(arm_length, waveguide_width, mp.inf),
                center=mp.Vector3(-waveguide_length/2 + splitter_length/2 + arm_length/2, waveguide_width/2 + splitter_length, 0))

arm2 = mp.Block(material=mp.Medium(index=15),
                size=mp.Vector3(arm_length, waveguide_width, mp.inf),
                center=mp.Vector3(waveguide_length/2 - splitter_length/2 - arm_length/2, waveguide_width/2 + splitter_length, 0))

# Add the arm structures to the simulation cell
sim.geometry.append(arm1)
sim.geometry.append(arm2)

# Define the phase shifter structure
phase_shifter = mp.Block(material=mp.Medium(index=15),
                         size=mp.Vector3(phase_shifter_length, waveguide_width, mp.inf),
                         center=mp.Vector3(0, waveguide_width/2 + splitter_length + phase_shifter_length/2, 0))

# Add the phase shifter structure to the simulation cell
sim.geometry.append(phase_shifter)

# Add a continuous wave (CW) source to the simulation
cw_source = mp.Source(mp.ContinuousSource(wavelength=5 * (11**0.5), width=20), component=mp.Ez, center=mp.Vector3(-9.99, 0, 0),size=mp.Vector3(0,1))

# Set up the boundary conditionsze
sim.boundary_conditions = [
    mp.PML(2.0),
    mp.PML(2.0),
    mp.PML(2.0),
]



# Add the sources to the simulation
sim.sources = [cw_source]

# Run the simulation
sim.run(until=200)

sim.run(
    mp.at_beginning(mp.output_epsilon),
    mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
    until=200,
)

# Plot the structure
eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)

plt.figure(figsize=(10, 6), dpi=100)
plt.imshow(np.flipud(np.transpose(eps_data)),
           cmap='binary',
           interpolation='spline36',
           extent=(-cell_size.x/2, cell_size.x/2, -cell_size.y/2, cell_size.y/2))

plt.xlabel('x')
plt.ylabel('y')
plt.title('Mach-Zehnder Interferometer Structure')
plt.colorbar(label='Dielectric Constant')

plt.show()

# Plot the Ez field
plt.figure(figsize=(10, 6), dpi=100)
sim.plot2D(fields=mp.Ez)
plt.show()
