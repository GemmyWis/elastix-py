#! /usr/bin/env python
#
# Example script that shows how to preform the registration

from __future__ import print_function, absolute_import
import elastix
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os
import SimpleITK as sitk

# IMPORTANT: these paths may differ on your system, depending on where
# Elastix has been installed. Please set accordingly.
ELASTIX_PATH = os.path.join(r'/home/koen/repos/elastix/bin/elastix')
TRANSFORMIX_PATH = os.path.join(r'/home/koen/repos/elastix/bin/transformix')

# Make a results directory if non exists
if not os.path.exists('results'):
    os.mkdir('results')

# Define the paths to the two images you want to register
fixed_image_path = os.path.join('example_data', 'patient1.jpg')
moving_image_path = os.path.join('example_data', 'patient2.jpg')

# Define a new elastix object 'el' with the CORRECT PATH to elastix
# If you use Windows paths (i.e. with backslashes, be sure to prepend your string with
# the letter r).
el = elastix.ElastixInterface(elastix_path=ELASTIX_PATH)

# Execute the registration. Make sure the paths below are correct, and
# that the results folder exists from where you are running this script
el.register(
    fixed_image=fixed_image_path,
    moving_image=moving_image_path,
    parameters=[os.path.join('example_data', 'parameters_bspline_multires_MR.txt')],
    output_dir='results')

# Find the results
transform_path = os.path.join('results', 'TransformParameters.0.txt')
result_path = os.path.join('results', 'result.0.tiff')


# Open the logfile into the dictionary log
for i in range(5):
    log_path = os.path.join('results', 'IterationInfo.0.R{}.txt'.format(i))
    log = elastix.logfile(log_path)
    # Plot the 'metric' against the iteration number 'itnr'
    plt.plot(log['itnr'], log['metric'])
plt.legend(['Resolution {}'.format(i) for i in range(5)])


# Show the resulting image side by side with the fixed and moving image
fig, ax = plt.subplots(1, 4, figsize=(20, 5))
fixed_image = imageio.imread(fixed_image_path)[:, :, 0]
moving_image = imageio.imread(moving_image_path)[:, :, 0]
transformed_moving_image = imageio.imread(result_path)
ax[0].imshow(fixed_image, cmap='gray')
ax[0].set_title('Fixed image')
ax[1].imshow(moving_image, cmap='gray')
ax[1].set_title('Moving image')
ax[2].imshow(transformed_moving_image, cmap='gray')
ax[2].set_title('Transformed\nmoving image')

# Make a new transformix object tr with the CORRECT PATH to transformix
tr = elastix.TransformixInterface(parameters=transform_path,
                                  transformix_path=TRANSFORMIX_PATH)

# Transform a new image with the transformation parameters
transformed_image_path = tr.transform_image(fixed_image_path, output_dir=r'results')

# Get the Jacobian matrix
jacobian_matrix_path = tr.jacobian_matrix(output_dir=r'results')

# Get the Jacobian determinant
jacobian_determinant_path = tr.jacobian_determinant(output_dir=r'results').replace('dcm', 'tiff')

# Get the full deformation field
deformation_field_path = tr.deformation_field(output_dir=r'results')


ax[3].imshow(imageio.imread(jacobian_determinant_path))
ax[3].set_title('Jacobian\ndeterminant')
[x.set_axis_off() for x in ax]
plt.show()