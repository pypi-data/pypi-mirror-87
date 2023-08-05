#!/usr/bin/env python

### setup.py

from setuptools import setup, find_packages
import sys, os

setup(name='RegionProposalGenerator',
      version='1.0.5',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/distRPG/RegionProposalGenerator-1.0.5.html',
      download_url='https://engineering.purdue.edu/kak/distRPG/RegionProposalGenerator-1.0.5.tar.gz',
      description='An educational module for generating region proposals for object detection',
      long_description='''

Consult the module API page at

      https://engineering.purdue.edu/kak/distRPG/RegionProposalGenerator-1.0.5.html

for all information related to this module, including information related
to the latest changes to the code.  The page at the URL shown above lists
all of the module functionality you can invoke in your own code.

::

        from RegionProposalGenerator import *

        rpg = RegionProposalGenerator(
                       ###  The first 6 options affect only the graph-based part of the algo
                       sigma = 1.0,
                       max_iterations = 40,
                       kay = 0.05,
                       image_normalization_required = True,
                       image_size_reduction_factor = 4,
                       min_size_for_graph_based_blobs = 4,
                       ###  The next 4 options affect only the Selective Search part of the algo
                       color_homogeneity_thresh = [20,20,20],
                       gray_var_thresh = 16000,           
                       texture_homogeneity_thresh = 120,
                       max_num_blobs_expected = 8,
              )
        
        image_name = "images/mondrian.jpg"
        segmented_graph,color_map = rpg.graph_based_segmentation(image_name)
        rpg.visualize_segmentation_in_pseudocolor(segmented_graph[0], color_map, "graph_based" )
        merged_blobs, color_map = rpg.selective_search_for_region_proposals( segmented_graph, image_name )
        rpg.visualize_segmentation_with_mean_gray(merged_blobs, "ss_based_segmentation_in_bw" )

          ''',

      license='Python Software Foundation License',
      keywords='object detection, image segmentation, computer vision',
      platforms='All platforms',
      classifiers=['Topic :: Scientific/Engineering :: Image Recognition', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.8'],
      packages=['RegionProposalGenerator']
)
