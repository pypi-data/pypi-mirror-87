__version__   = '1.0.5'
__author__    = "Avinash Kak (kak@purdue.edu)"
__date__      = '2020-November-30'   
__url__       = 'https://engineering.purdue.edu/kak/distRPG/RegionProposalGenerator-1.0.5.html'
__copyright__ = "(C) 2020 Avinash Kak. Python Software Foundation."

__doc__ = '''

RegionProposalGenerator.py

Version: ''' + __version__ + '''
   
Author: Avinash Kak (kak@purdue.edu)

Date: ''' + __date__ + '''


@title
CHANGE LOG:

  Version 1.0.5:

     In keeping with the tutorial nature of this module, this version
     includes methods that come in handy for batch-based processing of
     images. These methods carry names like "displaying_and_histogramming_
     images_in_batchX()" where X is 1, 2, and 3.  The rest of the module, 
     especially the part that deals with constructing region proposals 
     remains unchanged.

  Version 1.0.4:

    This is the first public release version of the module.


@title
INTRODUCTION:

    This module was created with two objectives in mind: (1) To provide a
    platform for experimenting with the logic used for constructing region
    proposals for object detection; and (2) to provide an educational tool
    for becoming familiar with the basic PyTorch functionality for image
    processing.  In order to fulfill these objectives, the module provides
    a self-documenting implementation of the algorithms that should be
    relatively easy to change, rather than a highly optimized
    implementation that would be good mostly for production work.  For
    high-speed production work, it would be best to use the implementations
    provided by the original authors of the algorithms that are
    incorporated in this module.

    At this point, the reader might ask: What is a region proposal?  To
    respond, let's say you want to detect an object in an image, but you
    know neither the exact location of the object nor the scale at which
    the object has manifested itself --- assuming the object is present at
    all in the image.  Under these conditions, in the old days, at each
    scale of detection, you would run a sliding window through the image,
    moving it from one pixel to the next, and, at each position of the
    window, test whether the pixels inside the window speak to the presence
    of the object.  The main problem with this approach to object detection
    is its high computational overhead, especially when the occurrence of
    the object inside a window is a rare occurrence.  Detecting objects in
    a 500x500 image at, say, 4 different scales would involve testing for
    the presence of the object in a million different windows.  Assuming
    that at most one of these windows contains the object fully, all of the
    computations in all the other windows would be wasted.

    To get around this computational overhead, more recently research in
    object detection has taken to first creating region proposals in an
    image, these being pixel blobs that look different from the general
    background in the image, and then applying the object detection
    algorithm to just those regions.  This is the approach that was used in
    the first deep-learning based object-detection framework called R-CNN
    by Girshick, Donahue, Darrell, and Malik. Although this approach was
    subsequently abandoned in later variants of the algorithm (by using a
    CNN to also form the region proposals), finding region proposals with
    non-CNN based methods is of continued importance in several problem
    domains that do not lend themselves to deep-learning based methods.
    That is, becoming familiar with the older non-learning based methods
    for constructing region proposals still has considerable value.
    Consider, for example, the problem of detecting objects in satellite
    images where you simply do not have access to the amount of training
    data you would need for a CNN based approach to work.

    That brings me to the presentation of this module. From an algorithmic
    standpoint, RegionProposalGenerator (RPG) implements elements of the
    Selective Search (SS) algorithm for object detection as proposed by
    Uijlings, van de Sande, Gevers, and Smeulders.  The Selective Search
    algorithm sits on top of the graph-based image segmentation algorithm
    of Felzenszwalb and Huttenlocher (FH) whose implementation is also
    included in the RPG module.

    It is important to note that the RegionProposalGenerator module is not
    intended for production work. The code is not at all optimized since
    the goal is merely to provide a rather easy-to-understand
    self-documenting implementation for experimenting with the logic of
    Selective Search.  For highly efficient and optimized implementations
    of both the Selective Search algorithm and the graph-based image
    segmentation algorithm (FH), the reader should use the original
    implementations as provided by the authors of those algorithms.

    The RPG module first processes an image with the FH graph-based
    algorithm for image segmentation to divide an image into pixel blobs.
    The module subsequently invokes elements of the SS algorithm to
    selectively merge the blobs on the basis of three properties:
    homogeneity of the color, grayscale variance, and texture homogeneity.

    The FH algorithm is based on creating a graph-based representation of
    an image in which, at the beginning, each pixel is a single vertex and
    the edge between two vertices that stand for two adjacent pixels
    represents the difference between some pixel property (such as the
    color difference) at the two pixels.  Subsequently, for the vertex
    merging logic, each vertex u, that after the first iteration stands for
    a grouping of pixels, is characterized by a property called Int(u),
    which is the largest value of the inter-pixel color difference between
    the adjacent pixels.  In order to account for the fact that, at the
    beginning, each vertex consists of only one pixel [which would not
    allow for the calculation of Int(u)], the unary property of the pixels
    at a vertex is extended from Int(u) to MInt(u) with the addition of a
    vertex-size dependent number equal to k/|C| where "k" is a
    user-specified parameter and |C| the cardinality of the set of pixels
    represented by the vertex u in the graph.

    As mentioned above, initially the edges in the graph representation of
    an image are set to the color difference between the two 8-adjacent
    pixels that correspond to two different vertices.  Subsequently, as the
    vertices are merged, an edge, E(u,v), between two vertices u and v is
    set to the smallest value of the inter-pixel color difference for two
    adjacent pixels that belong to the two vertices. At each iteration of
    the algorithm, two vertices u and v are merged provided E(u,v) is less
    than the smaller of the MInt(u) or MInt(v) attributes at the two
    vertices.  My experience is that for most images the algorithm
    terminates of its own accord after a small number of iterations while
    the vertex merging condition can be satisfied.

    Since the algorithm is driven by the color differences between
    8-adjacent pixels, the FH algorithm is likely to create too fine a
    segmentation of an image.  The segments produced by FH can be made
    larger by using the logic of SS that allows blobs of pixels to merge
    into larger blobs provided doing so makes sense based on the inter-blob
    values for mean color levels, color variances, texture values, etc.

    With regard to the other objective of this module, the two scripts
    in the Examples subdirectory of the distribution with names that
    begin with 'torchvision' speak for themselves.


@title
INSTALLATION:

    The RegionProposalGenerator class was packaged using setuptools.  For
    installation, execute the following command in the source directory
    (this is the directory that contains the setup.py file after you have
    downloaded and uncompressed the package):
 
            sudo python setup.py install

    and/or, for the case of Python3, 

            sudo python3 setup.py install

    On Linux distributions, this will install the module file at a location
    that looks like

             /usr/local/lib/python2.7/dist-packages/

    and, for the case of Python3, at a location that looks like

             /usr/local/lib/python3.6/dist-packages/

    If you do not have root access, you have the option of working directly
    off the directory in which you downloaded the software by simply
    placing the following statements at the top of your scripts that use
    the RegionProposalGenerator class:

            import sys
            sys.path.append( "pathname_to_RegionProposalGenerator_directory" )

    To uninstall the module, simply delete the source directory, locate
    where the RegionProposalGenerator module was installed with "locate
    RegionProposalGenerator" and delete those files.  As mentioned above,
    the full pathname to the installed version is likely to look like
    /usr/local/lib/python2.7/dist-packages/RegionProposalGenerator*

    If you want to carry out a non-standard install of the
    RegionProposalGenerator module, look up the on-line information on
    Disutils by pointing your browser to

              http://docs.python.org/dist/dist.html

@title
USAGE:

    To generate region proposals, you would need to construct an instance
    of the RegionProposalGenerator class and invoke the methods shown below
    on this instance:

        from RegionProposalGenerator import *

        rpg = RegionProposalGenerator(
                       ###  The first 6 options affect only the Graph-Based part of the algo
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


@title
CONSTRUCTOR PARAMETERS: 

    Of the 10 constructor parameters listed below, the first six are meant for
    the FH algorithm and the last four for the SS algorithm.

    sigma: Controls the size of the Gaussian kernel used for smoothing the
                    image before its gradient is calculated.  Assuming the
                    pixel sampling interval to be unity, a sigma of 1 gives
                    you a 7x7 smoothing operator with Gaussian weighting.
                    The default for this parameter is 1.

    max_iterations: Sets an upper limit on the number of iterations of the
                    graph-based FH algorithm for image segmentation.

    kay: This is the same as the "k" parameter in the FH algorithm.  As
                    mentioned in the Introduction above, the Int(u)
                    property of the pixels represented by each vertex in
                    the graph representation of the image is extended to
                    MInt(u) by the addition of a number k/|C| where |C| is
                    the cardinality of the set of pixels at that vertex.

    image_normalization_required: This applies Torchvision's image
                    normalization to the pixel values in the image.

    image_size_reduction_factor: As mentioned at the beginning of this
                    document, RegionProposalGenerator is really not meant
                    for production work.  The code is pure Python and, even
                    with that, not at all optimized.  The focus of the
                    module is primarily on easy understandability of what
                    the code is doing so that you can experiment with the
                    algorithm itself.  For the module to produce results
                    within a reasonable length of time, you can use this
                    constructor parameter to downsize the array of pixels
                    that the module must work with.  Set this parameter to
                    a value so that the initial graph constructed from the
                    image has no more than around 3500 vertices if you
                    don't want to wait too long for the results.

    min_size_for_graph_based_blobs: This declares a threshold on the
                   smallest size you'd like to see (in terms of the number
                   of pixels) in a segmented blob in the output of the
                   graph-based segmenter.  (I typically use values from 1
                   to 4 for this parameter.)

    color_homogeneity_thresh:  

                    This and the next three constructor options are meant
                    specifically for the SS algorithm that sits on top of
                    the FH algorithm for further merging of the pixel blobs
                    produced by FH.  This constructor option specifies the
                    maximum allowable difference between the mean color
                    values in two pixel blobs for them to be merged.

    gray_var_thresh:

                   This option declares the maximum allowable difference in 
                   the variances in the grayscale in two blobs if they are
                   to be merged. 

    texture_homogeneity_thresh:

                   The RegionProposalGenerator module characterizes the
                   texture of the pixels in each segmented blob by its LBP
                   (Local Binary Patterns) texture.  We want the LBP
                   texture values for two different blobs to be within the
                   value specified by this constructor option if those
                   blobs are to be merged.

    max_num_blobs_expected:

                   If you only want to extract a certain number of the
                   largest possible blobs, you can do that by giving a
                   value to this constructor option.

@title
PUBLIC METHODS:

    (1)  selective_search_for_region_proposals()

         This method implements elements of the Selective Search (SS)
         algorithm proposed by Uijlings, van de Sande, Gevers, and
         Smeulders for creating region proposals for object detection.
         As mentioned elsewhere here, this algorithm sits on top of
         the graph based image segmentation algorithm that was
         proposed by Felzenszwalb and Huttenlocher. 

    (2)  graph_based_segmentation()

         This is an implementation of the Felzenszwalb and Huttenlocher
         (FH) algorithm for graph-based segmentation of images.  At the
         moment, it is limited to working on grayscale images.

    (3)  display_tensor_as_image()

         This method converts the argument tensor into a photo image that
         you can display in your terminal screen. It can convert tensors of
         three different shapes into images: (3,H,W), (1,H,W), and (H,W),
         where H, for height, stands for the number of pixel in the
         vertical direction and W, for width, the same along the horizontal
         direction. When the first element of the shape is 3, that means
         that the tensor represents a color image in which each pixel in
         the (H,W) plane has three values for the three color channels.  On
         the other hand, when the first element is 1, that stands for a
         tensor that will be shown as a grayscale image.  And when the
         shape is just (H,W), that is automatically taken to be for a
         grayscale image.

    (4)  graying_resizing_binarizing()

         This is a demonstration of some of the more basic and commonly
         used image transformations from the torchvision.transformations
         module.  The large comment blocks are meant to serve as tutorial
         introduction to the syntax used for invoking these
         transformations.  The transformations shown can be used for
         converting a color image into a grayscale image, for resizing an
         image, for converting a PIL.Image into a tensor and a tensor back
         into an PIL.Image object, and so on.

    (5)  accessing_one_color_plane()

         This method shows how can access the n-th color plane of the
         argument color image.

    (6)  working_with_hsv_color_space()

         Illustrates converting an RGB color image into its HSV
         representation.

    (7)  histogramming_the_image()

         PyTorch based experiments with histogramming the grayscale
         and the color values in an image

    (8)  histogramming_and_thresholding():

         This method illustrates using the PyTorch functionality for
         histogramming and thresholding individual images.

    (9)  convolutions_with_pytorch()

         This method calls on torch.nn.functional.conv2d() for
         demonstrating a single image convolution with a specified
         kernel.

    (10) gaussian_smooth()

         This method smooths an image with a Gaussian of specified
         sigma.  You can do the same much faster by using the
         functionality programmed into torch.nn.functional.

    (11) visualize_segmentation_in_pseudocolor()

         After an image has been segmented, this method can be used to
         assign a random color to each blob in the segmented output
         for a better visualization of the segmentation.

    (12) visualize_segmentation_with_mean_gray()

         If the visualization produced by the previous method appears
         too chaotic, you can use this method to assign the mean color
         to each each blob in the output of an image segmentation
         algorithm.  The mean color is derived from the pixel values
         in the blob.

    (13) extract_image_region_interactively_by_dragging_mouse()

         You can use this method to apply the graph-based segmentation
         and the selective search algorithms to just a portion of your
         image.  This method extract the portion you want.  You click
         at the upper left corner of the rectangular portion of the
         image you are interested in and you then drag the mouse
         pointer to the lower right corner.  Make sure that you click
         on "save" and "exit" after you have delineated the area.

    (14) extract_image_region_interactively_through_mouse_clicks()

         This method allows a user to use a sequence of mouse clicks in
         order to specify a region of the input image that should be
         subject to further processing.  The mouse clicks taken together
         define a polygon. The method encloses the polygonal region by a
         minimum bounding rectangle, which then becomes the new input image
         for the rest of processing.

    (15) displaying_and_histogramming_images_in_batch1(image_dir, batch_size)

         This method is the first of three such methods in this module for
         illustrating the functionality of matplotlib for simultaneously
         displaying multiple images and the results obtained on them in
         gridded arrangements.  The code idea in this method is to call
         "plt.subplots(2,batch_size)" to create 'batch_size' number of
         subplot objects, called "axes", in the form of a '2xbatch_size'
         array. We use the first row of this grid to display each image in
         its own subplot object.  And we use the second row the grid to
         display the histogram of the corresponding image in the first row.

    (16) displaying_and_histogramming_images_in_batch2(image_dir, batch_size)

         I now show a second approach to display multiple images and their
         corresponding histograms in a gridded display.  In this method we
         call on "torchvision.utils.make_grid()" to construct a grid for
         us.  The grid is created by giving an argument like "nrow=4" to
         it.  The grip object returned by the call to make_grid() is a
         tensor unto itself. Such a tensor object is converted into a numpy
         array so that it can displayed by matplotlib's "imshow()"
         function.

    (17) displaying_and_histogramming_images_in_batch3(image_dir, batch_size)

         This method illustrates two things: (1) The syntax used for the
         'singular' version of the subplot function "plt.subplot()" ---
         although I'll be doing so by actually calling "fig.add_subplot()".
         And (2) How you can put together multiple multi-image plots by
         creating multiple Figure objects.  'Figure' is the top-level
         container of plots in matplotlib.  This method creates two
         separate Figure objects, one as a container for all the images in
         the batch and the other as a container for all the histograms for
         the images.  The two Figure containers are displayed in two
         separate windows on your computer screen.


@title 
THE Examples DIRECTORY:

    The Examples subdirectory in the distribution illustrates the sort
    of region proposal results you can obtain with this module.  The
    specific illustrations are in the following subdirectories of the
    Examples directory:

        Examples/color_blobs/

        Examples/mondrian/

        Examples/wallpic2/

    Each subdirectory contains at least the following two files:
    the function 

        selective_search.py
        and
        the image file specific for that subdirectory.

    All you have to do is to execute selective_search.py in that directory to
    see the results on the image in that directory.

    In addition to the above, the Examples directory also contains the following
    Python scripts:

        selective_search.py

            This is the same script that you will see in the three subdirectories
            (color_blobs, mondrian, and wallpic2) mentioned above.

        interactive_graph_based_segmentation.py

            This allows you to extract a portion of an image for applying
            graph-based segmentation logic and selective-search based
            region-proposal formation to.

            This interactive script can be used in two different modes: you
            can extract a portion of the image by dragging your mouse over
            the portion, or by clicking the mouse at the vertices of an
            imaginary polygon that defines the portion you would like to
            extract from the image.

        torchvision_some_basic_transformations.py    

            This is a demonstration of some of the more basic and commonly
            used image transformations from the torchvision.transformations
            module.  The transformations shown can be used for converting a
            color image into a grayscale image, for resizing an image, for
            converting a PIL.Image into a tensor and a tensor back into an
            PIL.Image object, and so on.

        torchvision_based_image_processing.py

            This script illustrates some single-image image processing
            operations you can carry out with the capabilities built
            into some of the PyTorch classes.  Examples shown include
            constructing a histogram for each color channel by
            invoking 'torch.hist()' on the channel; using
            torch.nn.functional.conv2d() for demonstrating a single
            image convolution with a specified kernel; and so on.

        multi_image_histogramming_and_display.py  

            To the extent that batch-based processing of images has become
            central to what goes on in most deep-learning algorithms, it is
            good to play with code that can be used for simultaneously
            displaying multiple images along with the results obtained from
            them.  This example script invokes three different versions
            of a method that uses a gridded display to show all the images
            in a batch and their corresponding histograms.


@title
CAVEATS:

    As mentioned earlier, this module is NOT meant for production work
    for constructing region proposals --- simply because it would be
    much too slow for full-sized images.  Yes, you can work with
    images of any size provided you set the constructor option
    image_size_reduction_factor appropriately.  However, note that
    setting this parameter to a large value causes a significant loss
    of resolution in the image, which reduces the quality of the
    output results.

    For full sized images, you will be better off using the
    implementations provided by the original authors of the
    algorithms.

    The goal of this module is solely to provide code that is a
    self-documented implementation of the algorithms involved.  This
    is to make it easy to experiment with the logic of the algorithms.
    

@title
BUGS:

    Please notify the author if you encounter any bugs.  When sending
    email, please place the string 'RegionProposalGenerator' in the
    subject line to get past the author's spam filter.


@title
ABOUT THE AUTHOR:

    The author, Avinash Kak, is a professor of Electrical and Computer
    Engineering at Purdue University.  For all issues related to this
    module, contact the author at kak@purdue.edu If you send email,
    please place the string "RegionProposalGenerator" in your subject
    line to get past the author's spam filter.

@title
COPYRIGHT:

    Python Software Foundation License

    Copyright 2020 Avinash Kak

@endofdocs
'''

import torch
import torch.nn as nn
import torchvision.transforms as tvt
import torchvision.utils as tutils
import numpy as np
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk
import sys,os,os.path,glob,signal
import re
import functools
import math
import random
import copy
if sys.version_info[0] == 3:
    import tkinter as Tkinter
    from tkinter.constants import *
else:
    import Tkinter    
    from Tkconstants import *

import matplotlib.pyplot as plt

import BitVector                  ##  needed for the LBP texture operator 


#___________________________________  Utility functions  ____________________________________


def _gaussian(sigma):
    '''
    A 1-D Gaussian smoothing operator is generated by assuming that the pixel
    sampling interval is a unit distance.  We truncate the operator a 3 times the
    value of sigma.  So when sigma is set to 1, you get a 7-element operator.  On the
    other hand, when sigma is set to 2, you get a 13-element operator, and so on.
    '''
    win_half_width = int(3 * sigma)
    xvals = range(-win_half_width, win_half_width+1)
    gauss = lambda x: math.exp(-((x**2)/(2*float(sigma**2))))
    operator = [gauss(x) for x in xvals]
    summed = functools.reduce( lambda x, y: x+y, operator )
    operator = [x/summed for x in operator]
    return operator

def _convolution_1D(input_array, operator):
    '''
    Since the Gaussian kernel is separable in its x and y dependencies, 2D convolution
    of an image with the kernel can be decomposed into a sequence of 1D convolutions
    first with the rows of the image and then another sequence of 1D convolutions
    with the columns of the output from the first.  This function carries out a 1D
    convolution.
    '''
    height,width = input_array.shape
    result_array = np.zeros((height, width), dtype="float")
    w = len(operator)                   # should be an odd number
    op_half_width = int((w-1)/2)
    for i in range(height):
        for j in range(width):
            accumulated = 0.0
            for k in range(-op_half_width,op_half_width+1):
                if (j+k) >= 0 and (j+k) < width:
                    accumulated += input_array[i,(j+k)] * operator[k + op_half_width]
            result_array[(i,j)] = accumulated
    return result_array

def _convolution_2D(input_array, operator):
    '''
    Since the Gaussian kernel is separable in its x and y dependencies, 2D convolution
    of an image with the kernel can be decomposed into a sequence of 1D convolutions
    first with the rows of the image and then another sequence of 1D convolutions
    with the columns of the output from the first.  This function orchestrates the
    invocation of 1D convolutions.
    '''
    result_conv_along_x = _convolution_1D(input_array, operator)
    result_conv_along_y = _convolution_1D(result_conv_along_x.transpose(), operator)
    final_result = result_conv_along_y.transpose()
    return final_result

def _line_intersection(line1, line2):                  ### needed for interactive extraction of
                                                       ### of an image portion by using mouse clicks
    '''                                                                                                  
    Each line is defined by a 4-tuple, with its first two elements defining the                          
    coordinates of the first endpoint and the two elements defining the coordinates                      
    of the second endpoint.  This function defines a predicate that tells us whether                     
    or not two given line segments intersect.                                                            
    '''
    line1_endpoint1_x = line1[0]
    line1_endpoint1_y = line1[1]
    line1_endpoint2_x = line1[2]
    line1_endpoint2_y = line1[3]
    line2_endpoint1_x = line2[0] + 0.5
    line2_endpoint1_y = line2[1] + 0.5
    line2_endpoint2_x = line2[2] + 0.5
    line2_endpoint2_y = line2[3] + 0.5
    if max([line1_endpoint1_x,line1_endpoint2_x]) <= min([line2_endpoint1_x,line2_endpoint2_x]):
        return 0
    elif max([line1_endpoint1_y,line1_endpoint2_y]) <= min([line2_endpoint1_y,line2_endpoint2_y]):
        return 0
    elif max([line2_endpoint1_x,line2_endpoint2_x]) <= min([line1_endpoint1_x,line1_endpoint2_x]):
        return 0
    elif max([line2_endpoint1_y,line2_endpoint2_y]) <= min([line1_endpoint1_y,line1_endpoint2_y]):
        return 0
    # Use homogeneous representation of lines:      
    hom_rep_line1 = _cross_product((line1_endpoint1_x,line1_endpoint1_y,1),(line1_endpoint2_x,line1_endpoint2_y,1))
    hom_rep_line2 = _cross_product((line2_endpoint1_x,line2_endpoint1_y,1),(line2_endpoint2_x,line2_endpoint2_y,1))
    hom_intersection = _cross_product(hom_rep_line1, hom_rep_line2)
    if hom_intersection[2] == 0:
        return 0
    intersection_x = hom_intersection[0] / (hom_intersection[2] * 1.0)
    intersection_y = hom_intersection[1] / (hom_intersection[2] * 1.0)
    if intersection_x >= line1_endpoint1_x and intersection_x <= line1_endpoint2_x and intersection_y >= line1_endpoint1_y and intersection_y <= line1_endpoint2_y:
        return 1
    return 0

def _cross_product(vector1, vector2):             ### needed by the above line intersection tester
    '''
    Returns the vector cross product of two triples
    '''
    (a1,b1,c1) = vector1
    (a2,b2,c2) = vector2
    p1 = b1*c2 - b2*c1
    p2 = a2*c1 - a1*c2
    p3 = a1*b2 - a2*b1
    return (p1,p2,p3)

def ctrl_c_handler( signum, frame ):             
    print("Killed by Ctrl C")                       
    os.kill( os.getpid(), signal.SIGKILL )       
signal.signal( signal.SIGINT, ctrl_c_handler )   


#______________________________  RegionProposalGenerator Class Definition  ________________________________

class RegionProposalGenerator(object):

    # Class variables: 
    region_mark_coords = {}
    drawEnable = startX = startY = 0
    canvas = None

    def __init__(self, *args, **kwargs ):
        if args:
            raise ValueError(  
                   '''RegionProposalGenerator constructor can only be called with keyword arguments for 
                      the following keywords: data_image, binary_or_gray_or_color, kay,
                      image_size_reduction_factor, max_iterations, sigma, image_normalization_required,
                      min_size_for_graph_based_blobs, max_num_blobs_expected,
                      color_homogeneity_thresh, gray_var_thresh, texture_homogeneity_thresh, and debug''')
        data_image = sigma = image_size_reduction_factor = kay = None
        min_size_for_graph_based_blobs = max_num_blobs_expected = None
        binary_or_gray_or_color =  max_iterations = image_normalization_required = None
        color_homogeneity_thresh = gray_var_thresh = texture_homogeneity_thresh = debug = None
        if 'data_image' in kwargs                    :   data_image = kwargs.pop('data_image')
        if 'sigma' in kwargs                         :   sigma = kwargs.pop('sigma')
        if 'kay' in kwargs                           :   kay = kwargs.pop('kay')
        if 'image_size_reduction_factor' in kwargs   :   image_size_reduction_factor = kwargs.pop('image_size_reduction_factor')
        if 'binary_or_gray_or_color' in kwargs       :   binary_or_gray_or_color = kwargs.pop('binary_or_gray_or_color')
        if 'image_normalization_required' in kwargs  :   image_normalization_required = kwargs.pop('image_normalization_required')
        if 'max_iterations' in kwargs                :   max_iterations=kwargs.pop('max_iterations')
        if 'color_homogeneity_thresh' in kwargs      :   color_homogeneity_thresh = kwargs.pop('color_homogeneity_thresh')
        if 'gray_var_thresh' in kwargs               :    gray_var_thresh = kwargs.pop('gray_var_thresh')
        if 'texture_homogeneity_thresh' in kwargs    :   texture_homogeneity_thresh = kwargs.pop('texture_homogeneity_thresh')
        if 'min_size_for_graph_based_blobs' in kwargs :  min_size_for_graph_based_blobs = kwargs.pop('min_size_for_graph_based_blobs')
        if 'max_num_blobs_expected' in kwargs        :  max_num_blobs_expected = kwargs.pop('max_num_blobs_expected')
        if 'debug' in kwargs                         :   debug = kwargs.pop('debug') 
        if len(kwargs) != 0: raise ValueError('''You have provided unrecognizable keyword args''')
        if data_image: 
            self.data_im_name = data_image
            self.data_im =  Image.open(data_image)
            self.original_im = Image.open(data_image)
        if binary_or_gray_or_color:
            self.binary_or_gray_or_color = binary_or_gray_or_color
        if sigma is not None: 
            self.sigma = sigma
        else:
            self.sigma = 0
        if kay is not None:   self.kay = kay
        if image_size_reduction_factor is not None:
            self.image_size_reduction_factor = image_size_reduction_factor
        else:
            self.image_size_reduction_factor = 1
        if image_normalization_required is not None:
            self.image_normalization_required = image_normalization_required
        else:
            self.image_normalization_required = False
        if max_iterations is not None:
            self.max_iterations = max_iterations
        else:
            self.max_iterations = 40
        if color_homogeneity_thresh is not None:
            self.color_homogeneity_thresh = color_homogeneity_thresh
        if gray_var_thresh is not None:
            self.gray_var_thresh = gray_var_thresh
        if texture_homogeneity_thresh is not None:
            self.texture_homogeneity_thresh = texture_homogeneity_thresh
        if min_size_for_graph_based_blobs is not None:
            self.min_size_for_graph_based_blobs = min_size_for_graph_based_blobs
        if max_num_blobs_expected is not None:
            self.max_num_blobs_expected = max_num_blobs_expected
        self.image_portion_delineation_coords = []
        if debug:                             
            self.debug = debug
        else:
            self.debug = 0
        self.iterations_used = 0


    def graying_resizing_binarizing(self, image_file, polarity=1, area_threshold=0, min_brightness_level=100):
        '''
        This is a demonstration of some of the more basic and commonly used image
        transformations from the torchvision.transformations module.  The large comments
        blocks are meant to serve as tutorial introduction to the syntax used for invoking
        these transformations.  The transformations shown can be used for converting a
        color image into a grayscale image, for resizing an image, for converting a
        PIL.Image into a tensor and a tensor back into an PIL.Image object, and so on.
        '''
        if os.path.isfile(image_file):
            im_pil = Image.open(image_file)
        else:
            sys.exit("the image file %s does not exist --- aborting" % image_file)
        self.displayImage6(im_pil, "input_image")

        ###  The next three lines of code that follow are three examples of calls to the
        ###  constructor of the torchvision.tranforms.Compose class whose contract, as its
        ###  name implies, is to compose a sequence of transformations to be applied to an
        ###  image.  The instance of Compose constructed in line (A) has only one
        ###  transformation in it, which would resize an image to a 64x64 array of pixels.
        ###  On the other hand, the instance constructed in line (B) includes two
        ###  transformations: the first transformation is for converting an image from
        ###  "RGB" to gray scale, and the second for resizing an image as before to an
        ###  array of 64x64 pixels.  The instance of Compose constructed in line (C)
        ###  incorporates a sequence of five transformations. It invoked on a color image,
        ###  it will convert the image into grayscale, then resize it to an array of 64x64
        ###  pixels, convert the array to a tensor, normalize the array so that its mean
        ###  and the standard deviation both equal 0.5, and, finally, convert the tensor
        ###  into a PIL image object.  
        ###
        ###  A most important thing to note here is that each of the instances returned in
        ###  lines (A), (B), and (C) is a callable object, meaning that the instance can
        ###  be called directly, with the image to which the transformation are to be
        ###  applied, as the argument to the instance.
        ###
        ###  Note that in the Compose instance constructed in line (C), we had to
        ###  interpose the "ToTensor" transformation between the Resize and the Normalize
        ###  transformations because the Resize transformation returns an Image object that
        ###  cannot be normalized directly.  That is, the Normalize transformation is
        ###  meant for the normalization of tensors --- it takes a tensor as its input and
        ###  returns a tensor at its output.  If you want the final result of the sequence
        ###  of transformations in line (C) to return an Image, then you would also like
        ###  to call the ToPILImage transformation as shown.
        ###  
        resize_xform = tvt.Compose( [ tvt.Resize((64,64)) ] )                               ## (A)

        gray_and_resize = tvt.Compose( [tvt.Grayscale(num_output_channels = 1),  
                                        tvt.Resize((64,64)) ] )                             ## (B)

        gray_resize_normalize = tvt.Compose( [tvt.Grayscale(num_output_channels = 1), 
                                              tvt.Resize((64,64)), 
                                              tvt.ToTensor(), 
                                              tvt.Normalize(mean=[0.5], std=[0.5]), 
                                              tvt.ToPILImage() ] )                          ## (C)

        ###  As explained in the previous comment block, the three statements shown above
        ###  are merely calls to the constructor of the Compose class for the creation of
        ###  instances.  As also mentioned previously, these instances are designed to be
        ###  callable; that is, they can be treated like function objects for actually
        ###  applying the transformations to a given image.  This is shown in the lines of
        ###  code that follow.
        ###
        ###  Applying the resize_xform of line (A) to an image:
        img = resize_xform( im_pil )
        self.displayImage6(img, "output_of_resize_xform")

        ###  Applying gray_and_resize of line (B) to an image:
        img = gray_and_resize( im_pil )
        self.displayImage6(img, "output_of_gray_and_resize")

        ###  Applying gray_resize_normalize of line (C) to an image:
        img = gray_resize_normalize( im_pil )
        self.displayImage6(img, "output_of_gray_resize_normalize")

        ###  Demonstrating the ToTensor transformation all by itself.  As in earlier
        ###  examples, first construct a callable instance of Compose and then invoke it
        ###  on the image which must of type PIL.Image.
        img_tensor = tvt.Compose([tvt.ToTensor()])
        img_data = img_tensor(img)
        print("\nshape of the img_data tensor: %s" % str(img_data.shape))               ##  (1,64,64)
        print("\n\n\nimg_tensor: %s" % str(img_data))
                           #
                           #  tensor([[[0.9333, 0.9569, 0.9647,  ..., 0.6745, 0.5882, 0.5569],
                           #           [0.8392, 0.8392, 0.7922,  ..., 0.6275, 0.6980, 0.7922],
                           #           [0.9255, 0.9176, 0.8157,  ..., 0.9725, 0.9725, 0.9882],
                           #           ...,
                           #           [0.4431, 0.4745, 0.5882,  ..., 0.6588, 0.7373, 0.6667],
                           #           [0.4431, 0.5098, 0.5725,  ..., 0.4667, 0.5255, 0.5412],
                           #           [0.5098, 0.5490, 0.5255,  ..., 0.4980, 0.6118, 0.5804]]])
                           #               

        ###  With the image in its 1x64x64 numeric tensor representation, we can apply a
        ###  comparison operator to the individual elements of the tensor to threshold the
        ###  the image data.  Since the pixel values in a grayscale image (we have
        ###  grayscale because of an earlier transformation to the originally color image)
        ###  are between 0 and 255 and since the normalization is going to convert these
        ###  numbers into floating point numbers between 0.0 and 1.0, the thresholding
        ###  operation applied below is going to set to FALSE all pixel values that are
        ###  below 128 and to TRUE all pixel values that are above 128.
        img_data = img_data > 0.5                                                           ## (D)
        print("\n\n\nimg_data: %s" % str(img_data))
                           #
                           #  tensor([[[ True,  True,  True,  ...,  True,  True,  True],
                           #           [ True,  True,  True,  ...,  True,  True,  True],
                           #           [ True,  True,  True,  ...,  True,  True,  True],
                           #           ...,
                           #           [False, False,  True,  ...,  True,  True,  True],
                           #           [False,  True,  True,  ..., False,  True,  True],
                           #           [ True,  True,  True,  ..., False,  True,  True]]])

        ###  In order to visualize the thresholding effect achieved above, we need to
        ###  convert the Boolean pixel values back into numbers, which we can do by
        ###  calling float() on the output image tensor as shown below:
        img_data = img_data.float()                                                         ## (E)
        ###  Now we need to construct a Compose instance with the ToPILImage
        ###  transformation at its heart.  This we can do by:
        to_image_xform = tvt.Compose([tvt.ToPILImage()])                                    ## (F)
        ###  Invoking the callable to_image_xform instance on the tensor returned by the
        ###  call in line (E) gives us the desired PIL.Image object that can be
        ###  visualized.
        img = to_image_xform(img_data)
        self.displayImage6(img, "after_thresholding")

    def display_tensor_as_image2(self, tensor, title=""):
        '''
        This method converts the argument tensor into a photo image that you can display
        in your terminal screen. It can convert tensors of three different shapes
        into images: (3,H,W), (1,H,W), and (H,W), where H, for height, stands for the
        number of pixels in the vertical direction and W, for width, for the same
        along the horizontal direction.  When the first element of the shape is 3,
        that means that the tensor represents a color image in which each pixel in
        the (H,W) plane has three values for the three color channels.  On the other
        hand, when the first element is 1, that stands for a tensor that will be
        shown as a grayscale image.  And when the shape is just (H,W), that is
        automatically taken to be for a grayscale image.
        '''
        tensor_range = (torch.min(tensor).item(), torch.max(tensor).item())
        if tensor_range == (-1.0,1.0):
            ##  The tensors must be between 0.0 and 1.0 for the display:
            print("\n\n\nimage un-normalization called")
            tensor = tensor/2.0 + 0.5     # unnormalize
        plt.figure(title)
        ###  The call to plt.imshow() shown below needs a numpy array. We must also
        ###  transpose the array so that the number of channels (the same thing as the
        ###  number of color planes) is in the last element.  For a tensor, it would be in
        ###  the first element.
        if tensor.shape[0] == 3 and len(tensor.shape) == 3:
#            plt.imshow( tensor.numpy().transpose(1,2,0) )
            plt.imshow( tensor.numpy().transpose(1,2,0) )
        ###  If the grayscale image was produced by calling torchvision.transform's
        ###  ".ToPILImage()", and the result converted to a tensor, the tensor shape will
        ###  again have three elements in it, however the first element that stands for
        ###  the number of channels will now be 1
        elif tensor.shape[0] == 1 and len(tensor.shape) == 3:
            tensor = tensor[0,:,:]
            plt.imshow( tensor.numpy(), cmap = 'gray' )
        ###  For any one color channel extracted from the tensor representation of a color
        ###  image, the shape of the tensor will be (W,H):
        elif len(tensor.shape) == 2:
            plt.imshow( tensor.numpy(), cmap = 'gray' )
        else:
            sys.exit("\n\n\nfrom 'display_tensor_as_image2()': tensor for image is ill formed -- aborting")
        plt.show()


    def display_tensor_as_image(self, tensor, title=""):
        '''
        This method converts the argument tensor into a photo image that you can display
        in your terminal screen. It can convert tensors of three different shapes
        into images: (3,H,W), (1,H,W), and (H,W), where H, for height, stands for the
        number of pixels in the vertical direction and W, for width, for the same
        along the horizontal direction.  When the first element of the shape is 3,
        that means that the tensor represents a color image in which each pixel in
        the (H,W) plane has three values for the three color channels.  On the other
        hand, when the first element is 1, that stands for a tensor that will be
        shown as a grayscale image.  And when the shape is just (H,W), that is
        automatically taken to be for a grayscale image.
        '''
        print("\n\n\ndisplay_tensor_as_image() called with a tensor of type: %s" % tensor.type())
                                                                                  ##  torch.FloatTensor
        ###  The 'plt' in the following statement stands for the plotting module 
        ###  matplotlib.pyplot.  See the module import declarations at the beginning of
        ###  this module.
        plt.figure(title)

        ###  The call to plt.imshow() shown below needs a numpy array. We must also
        ###  transpose the array so that the number of channels (the same thing as the
        ###  number of color planes) is in the last element.  For a tensor, it would be in
        ###  the first element.
        if tensor.shape[0] == 3 and len(tensor.shape) == 3:
            plt.imshow( tensor.numpy().transpose(1,2,0) )

        ###  If the grayscale image was produced by calling torchvision.transform's
        ###  ".ToPILImage()", and the result converted to a tensor, the tensor shape will
        ###  again have three elements in it, however the first element that stands for
        ###  the number of channels will now be 1
        elif tensor.shape[0] == 1 and len(tensor.shape) == 3:
            tensor = tensor[0,:,:]
            plt.imshow( tensor.numpy(), cmap = 'gray' )

        ###  For any one color channel extracted from the tensor representation of a color
        ###  image, the shape of the tensor will be (W,H):
        elif len(tensor.shape) == 2:
            plt.imshow( tensor.numpy(), cmap = 'gray' )
        else:
            sys.exit("\n\n\ntensor for image is ill formed -- aborting")
        plt.show()
            
    def accessing_one_color_plane(self, image_file, n):
        '''
        This method shows how can access the n-th color plane of the argument color image.
        '''
        if os.path.isfile(image_file):
            im_pil = Image.open(image_file)
        else:
            sys.exit("the image file %s does not exist --- aborting" % image_file)

        ###  In order to access the color planes individually, it is best to first convert
        ###  the image into a tensor of shape 3xWxH where 3 is for the three color planes,
        ###  W for the width of the image in pixels, and H for the height of the image in
        ###  pixels. To accomplish this PIL.Image to tensor conversion, we first need to
        ###  construct an instance of the ToTensor class by calling its constructor.
        ###  Since the resulting instance will be a callable object, we can treat it like
        ###  a function object and invoke it directly as shown below while supplying the
        ###  image to it as its argument.
        image_to_tensor_converter = tvt.ToTensor()
        image_as_tensor = image_to_tensor_converter(im_pil)

        ###  IT IS VERY IMPORTANT TO REALIZE that while the pixels in the original color
        ###  image are one-byte integers, with values between 0 and 255 for each of the
        ###  color channels, after the image is turned into a tensor, the three values at
        ###  each pixel are convereted into a floating point number between 0.0 and 1.0.
        print("\n\n\nimage as tensor: %s" % str(image_as_tensor))
                            #
                            #  tensor([[[0.4588, 0.4588, 0.4627,  ..., 0.2667, 0.2627, 0.2549],    r-plane
                            #           [0.4588, 0.4627, 0.4667,  ..., 0.2784, 0.2745, 0.2667],
                            #           [0.4588, 0.4667, 0.4745,  ..., 0.2784, 0.2745, 0.2667],
                            #           ...,
                            #           [0.2078, 0.2235, 0.2392,  ..., 0.2941, 0.2627, 0.2392],
                            #           [0.2118, 0.2314, 0.2431,  ..., 0.2902, 0.2706, 0.2549],
                            #           [0.2235, 0.2392, 0.2471,  ..., 0.2706, 0.2588, 0.2510]],
                            # 
                            #          [[0.4784, 0.4784, 0.4824,  ..., 0.2902, 0.2863, 0.2784],    g-plane
                            #           [0.4745, 0.4784, 0.4824,  ..., 0.3020, 0.2980, 0.2902],
                            #           [0.4824, 0.4902, 0.4980,  ..., 0.3020, 0.2980, 0.2902],
                            #           ...,
                            #           [0.2510, 0.2667, 0.2824,  ..., 0.3529, 0.3216, 0.2980],
                            #           [0.2549, 0.2745, 0.2863,  ..., 0.3373, 0.3176, 0.3020],
                            #           [0.2667, 0.2824, 0.2902,  ..., 0.3098, 0.2980, 0.2902]],
                            # 
                            #          [[0.2275, 0.2275, 0.2314,  ..., 0.1490, 0.1529, 0.1451],    b-plane
                            #           [0.2353, 0.2392, 0.2431,  ..., 0.1608, 0.1569, 0.1490],
                            #           [0.2392, 0.2471, 0.2549,  ..., 0.1529, 0.1490, 0.1490],
                            #           ...,
                            #           [0.1176, 0.1333, 0.1490,  ..., 0.2000, 0.1686, 0.1451],
                            #           [0.1216, 0.1412, 0.1529,  ..., 0.1882, 0.1686, 0.1529],
                            #           [0.1333, 0.1490, 0.1569,  ..., 0.1647, 0.1529, 0.1451]]])
                            # 
        ###  Two different ways of checking the type of the tensor.  The second call is more
        ###  informative
        print("\n\n\nType of image_as_tensor: %s" % type(image_as_tensor))       ## <class 'torch.Tensor'>
        print("\n[More informative]  Type of image_as_tensor: %s" % image_as_tensor.type())    
                                                                                 ## <class 'torch.FloatTensor'>
        print("\n\n\nShape of image_as_tensor: %s" % str(image_as_tensor.shape)) ## (3, 366, 320)

        ###  The following function will automatically re-convert the 0.0 to 1.0 floating
        ###  point values for at the pixels into the integer one-byte representations for
        ###  displaying the image.
        self.display_tensor_as_image(image_as_tensor,"color image in 'accessing each color plane method'")

        ###  n=0 means the R channel, n=1 the G channel, and n=2 the B channel
        channel_image = image_as_tensor[n]
        print("\n\n\nchannel image: %s" % str(channel_image))
                            # tensor([[0.4588, 0.4588, 0.4627,  ..., 0.2667, 0.2627, 0.2549],
                            #         [0.4588, 0.4627, 0.4667,  ..., 0.2784, 0.2745, 0.2667],
                            #         [0.4588, 0.4667, 0.4745,  ..., 0.2784, 0.2745, 0.2667],
                            #         ...,
                            #         [0.2078, 0.2235, 0.2392,  ..., 0.2941, 0.2627, 0.2392],
                            #         [0.2118, 0.2314, 0.2431,  ..., 0.2902, 0.2706, 0.2549],
                            #         [0.2235, 0.2392, 0.2471,  ..., 0.2706, 0.2588, 0.2510]]) 

        self.display_tensor_as_image(channel_image, "showing just the designated channel" )

        ###   In the statement shown below, the coefficients (0.4, 0.4, 0.2) are a measure
        ###   of how sensitive the human visual system is to the three different color
        ###   channels.  Index 0 is for R, index 1 for G, and the index 2 for B.
        ###
        ###   Note that these weights are predicated on the pixel values being
        ###   respresented by floating-point numbers between 0.0 and 1.0 (as opposed
        ###   to the more commonly used one-byte integers).
        gray_tensor = 0.4 * image_as_tensor[0]  +   0.4 * image_as_tensor[1]   + 0.2 * image_as_tensor[2]
        self.display_tensor_as_image(gray_tensor, "showing the grayscale version")


    def extract_data_pixels_in_bb(self, image_file, bounding_box):
        '''
        Mainly used for testing
        '''
        im_arr  =  np.asarray(Image.open(image_file))
        height,width,_ = im_arr.shape
        hmin,hmax = bounding_box[0],bounding_box[2]
        wmin,wmax = bounding_box[1],bounding_box[3]
        im_arr_portion = im_arr[hmin:hmax,wmin:wmax,:]
        return im_arr_portion

    def working_with_hsv_color_space(self, image_file, test=False):
        ''' 
        Shows color image conversion to HSV
        '''
        if os.path.isfile(image_file):
            im_pil = Image.open(image_file)
        else:
            sys.exit("the image file %s does not exist --- aborting" % image_file)

        ###   Get the HsV representation of the PIL Image object by invoking
        ###   "convert('HSV')" on it as shown below:
        hsv_image = im_pil.convert('HSV')
        hsv_arr = np.asarray(hsv_image)
        np.save("hsv_arr.npy", hsv_arr)
        image_to_tensor_converter = tvt.ToTensor()
        hsv_image_as_tensor = image_to_tensor_converter( hsv_image )
        ###   The index "1" as the last argument means that we want the three images
        ###   to be concatenated horizontally (meaning, along the 'width' dimension
        ###   as opposed to the 'height' dimension).  If you change that value to
        ###   "0", you will see the three images lined up vertically.
        if test is False:
            self.display_tensor_as_image(torch.cat((hsv_image_as_tensor[0], hsv_image_as_tensor[1], hsv_image_as_tensor[2] ),1), "displaying the HSV channels separately")


    def histogramming_the_image(self, image_file):
        '''
        PyTorch based experiments with histogramming the grayscale and the color values in an
        image
        '''
        if os.path.isfile(image_file):
            im_pil = Image.open(image_file)
        else:
            sys.exit("the image file %s does not exist --- aborting" % image_file)

        image_to_tensor_converter = tvt.ToTensor()
        color_image_as_tensor = image_to_tensor_converter( im_pil )

        ###   Let's first plot the histogram of the grayscale version of the image:
        gray_tensor = 0.4 * color_image_as_tensor[0]  +   0.4 * color_image_as_tensor[1]   + 0.2 * color_image_as_tensor[2]
        hist_gray = torch.histc(gray_tensor, bins = 10, min = 0.0, max = 1.0)
        hist_gray = hist_gray.div( hist_gray.sum() )

        fig = plt.figure("histogram of the grayscale")
        ax = fig.add_subplot(111)
        ax.bar( np.linspace(1.0, 10.0, num = 10), hist_gray.numpy(), color='black' )
        plt.show()

        ###   We will now plot separately the histogram for each color channel
        ###
        r_tensor = color_image_as_tensor[0]
        g_tensor = color_image_as_tensor[1]
        b_tensor = color_image_as_tensor[2]
        
        ###  Computing the hist for each color channel separately
        hist_r = torch.histc(r_tensor, bins = 10, min = 0.0, max = 1.0)
        hist_g = torch.histc(g_tensor, bins = 10, min = 0.0, max = 1.0)
        hist_b = torch.histc(b_tensor, bins = 10, min = 0.0, max = 1.0)
        
        ###  Normalizing the channel based hists so that the bin counts in each sum to 1.
        hist_r = hist_r.div(hist_r.sum())
        hist_g = hist_g.div(hist_g.sum())
        hist_b = hist_b.div(hist_b.sum())
        
        ### Displaying the channel histograms separately in one figure:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey = True)
        fig.title = "histogramming the color components separately"
        ax1.bar(np.linspace(1.0, 10.0, num = 10), hist_r.numpy(), color='r')
        ax2.bar(np.linspace(1.0, 10.0, num = 10), hist_g.numpy(), color='g')
        ax3.bar(np.linspace(1.0, 10.0, num = 10), hist_b.numpy(), color='b')
        plt.show();


    def displaying_and_histogramming_images_in_batch1(self, dir_name, batch_size):
        '''
        This method is the first of three such methods in this module for illustrating the
        functionality of matplotlib for simultaneously displaying multiple images and
        the results obtained on them in gridded arrangements.  In the implementation
        shown below, the core idea in this method is to call
        "plt.subplots(2,batch_size)" to create 'batch_size' number of subplot
        objects, called "axes", in the form of a '2xbatch_size' array. We use the first
        row of this grid to display each image in its own subplot object.  And we use
        the second row the grid to display the histogram of the corresponding image
        in the first row.
        '''
        fig, axes = plt.subplots(2,batch_size)
        image_files = glob.glob(dir_name + '/*.jpg')[:batch_size]
        images = list(map(Image.open, image_files))
        images = [tvt.Grayscale()(x) for x in images]
        images = [tvt.Resize((64,64), Image.ANTIALIAS)(x) for x in images]
        im_tensors = [tvt.ToTensor()(x) for x in images]
        im_tensors = [tvt.Normalize(mean=[0.5], std=[0.5])(x) for x in im_tensors]

        for j in range(batch_size):
            axes[0,j].imshow(im_tensors[j][0,:,:].numpy(), cmap='gray')

        hists = [torch.histc(x,  bins=10) for x in im_tensors]
        total_counts = list(map(sum, hists)) 
        hists_normed = [hists[i] / total_counts[i] for i in range(len(hists))]
        for j in range(batch_size):
            axes[1,j].bar(np.linspace(1.0, 10.0, num = 10), hists_normed[j].numpy())  
            axes[1,j].set_yticks([])
        plt.show()

    def displaying_and_histogramming_images_in_batch2(self, dir_name, batch_size):
        '''
        I now show a second approach to display multiple images and their corresponding
        histograms in a gridded display.  Unlike in the previous implementation of
        this method, now we do not call on "plt.subplots()" to create a grid
        structure for displaying the images.  On the other hand, we now call on
        "torchvision.utils.make_grid()" to construct a grid for us.  The grid is
        created by giving an argument like "nrow=4" to it.  When using this method,
        an important thing to keep in mind is that the first argument to make_grip()
        must be a tensor of shape "(B, C, H, W)" where B stands for batch_size, C for
        channels (3 for color, 1 for gray), and (H,W) for the height and width of the
        image. What that means in our example is that we need to synthesize a tensor
        of shape "(8,1,64,64)" in order to be able to call the "make_grid()"
        function. Note that the object returned by the call to make_grid() is a
        tensor unto itself.  For the example shown, if we had called
        "print(grid.shape)" on the "grid" returned by "make_grid()", the answer would
        be "torch.Size([3, 158, 306])" which, after it is converted into a numpy
        array, can be construed by a plotting function as a color image of size
        158x306.
        '''
        image_files = glob.glob(dir_name + '/*.jpg')[:batch_size]
        images = list(map(Image.open, image_files))
        images = [tvt.Grayscale()(x) for x in images]
        images = [tvt.Resize((64,64), Image.ANTIALIAS)(x) for x in images]
        im_tensors = [tvt.ToTensor()(x) for x in images]
        im_tensors = [tvt.Normalize(mean=[0.5], std=[0.5])(x) for x in im_tensors]
        IM_Tensor = torch.zeros(batch_size,1,64,64, dtype=float)
        for i in range(batch_size):
            IM_Tensor[i,0,:,:] = im_tensors[i][0,:,:]
        # for the display:
        grid = tutils.make_grid(IM_Tensor, nrow=4, padding=10, normalize=True)
        npgrid = grid.cpu().numpy()
        plt.imshow(np.transpose(npgrid, (1,2,0)), interpolation='nearest')
        plt.show()

        hists = [torch.histc(x,  bins=10) for x in im_tensors]
        total_counts = list(map(sum, hists)) 
        hists_normed = [hists[i] / total_counts[i] for i in range(len(hists))]
        fig, axes = plt.subplots(nrows=2, ncols=4, sharey = True)    

        for i in range(2):
            for j in range(batch_size // 2):
                k = i * (batch_size//2) + j
                axes[i,j].bar(np.linspace(1.0, 10.0, num = 10), hists_normed[k].numpy())  
        plt.show();

    def displaying_and_histogramming_images_in_batch3(self, dir_name, batch_size):
        '''
        The core idea here is to illustrate two things: (1) The syntax used for the
        'singular' version of the subplot function "plt.subplot()" --- although I'll
        be doing so by actually calling "fig.add_subplot()".  And (2) How you can put
        together multiple multi-image plots by creating multiple Figure objects.
        Figure is the top-level container of plots in matplotlib.  In the 
        implementation shown below, the key statements are: 

            fig1 = plt.figure(1)    
            axis = fig1.add_subplot(241)              
                                                                                                                      
        Calling "add_subplot()" on a Figure object returns an "axis" object.  The
        word "axis" is a misnomer for what should really be called a "subplot".
        Subsequently, you can call display functions lime "imshow()", "bar()", etc.,
        on the axis object to display an individual plot in a gridded arrangement.

        The argument "241" in the first call to "add_subplot()" means that your
        larger goal is to create a 2x4 display of plots and that you are supplying
        the 1st plot for that grid.  Similarly, the argument "242" in the next call
        to "add_subplot()" means that for your goal of creating a 2x4 gridded
        arrangement of plots, you are now supplying the second plot.  Along the same
        lines, the argument "248" toward the end of the code block that you are now
        supplying the 8th plot for the 2x4 arrangement of plots.

        Note how we create a second Figure object in the second major code block.  We
        use it to display the histograms for each of the images shown in the first
        Figure object.  The two Figure containers will be shown in two separate
        windows on your laptop screen.
        '''
        image_files = glob.glob(dir_name + '/*.jpg')[:batch_size]
        images = list(map(Image.open, image_files))
        images = [tvt.Grayscale()(x) for x in images]
        images = [tvt.Resize((64,64), Image.ANTIALIAS)(x) for x in images]
        im_tensors = [tvt.ToTensor()(x) for x in images]
        im_tensors = [tvt.Normalize(mean=[0.5], std=[0.5])(x) for x in im_tensors]

        # Let's make a Figure for the 8 images:
        fig1 = plt.figure(1)
        axis = fig1.add_subplot(241)
        axis.imshow(im_tensors[0][0,:,:].numpy(), cmap='gray') 
        axis = fig1.add_subplot(242)
        axis.imshow(im_tensors[1][0,:,:].numpy(), cmap='gray') 
        axis = fig1.add_subplot(243)
        axis.imshow(im_tensors[2][0,:,:].numpy(), cmap='gray') 
        axis = fig1.add_subplot(244)
        axis.imshow(im_tensors[3][0,:,:].numpy(), cmap='gray') 
        axis = fig1.add_subplot(245)
        axis.imshow(im_tensors[4][0,:,:].numpy(), cmap='gray') 
        axis = fig1.add_subplot(246)
        axis.imshow(im_tensors[5][0,:,:].numpy(), cmap='gray') 
        axis = fig1.add_subplot(247)
        axis.imshow(im_tensors[6][0,:,:].numpy(), cmap='gray') 
        axis = fig1.add_subplot(248)
        axis.imshow(im_tensors[7][0,:,:].numpy(), cmap='gray') 

        # Now let's make a second figure for the 8 corresponding histograms:
        hists = [torch.histc(x,  bins=10) for x in im_tensors]
        total_counts = list(map(sum, hists)) 
        hists_normed = [hists[i] / total_counts[i] for i in range(len(hists))]
        fig2 = plt.figure(2)
        axis = fig2.add_subplot(241)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[0].numpy())
        axis.set_yticks([])
        axis = fig2.add_subplot(242)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[1].numpy())
        axis.set_yticks([])
        axis = fig2.add_subplot(243)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[2].numpy())
        axis.set_yticks([])
        axis = fig2.add_subplot(244)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[3].numpy())
        axis.set_yticks([])
        axis = fig2.add_subplot(245)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[4].numpy())
        axis.set_yticks([])
        axis = fig2.add_subplot(246)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[5].numpy())
        axis.set_yticks([])
        axis = fig2.add_subplot(247)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[6].numpy())
        axis.set_yticks([])
        axis = fig2.add_subplot(248)
        axis.bar(np.linspace(1.0, 10.0, num = 10), hists_normed[7].numpy())
        axis.set_yticks([])
        plt.show()

    def histogramming_and_thresholding(self, image_file):
        '''
        PyTorch based experiments with histogramming and thresholding
        '''
        if os.path.isfile(image_file):
            im_pil = Image.open(image_file)
        else:
            sys.exit("the image file %s does not exist --- aborting" % image_file)

        image_to_tensor_converter = tvt.ToTensor()
        ###   Note that "self.original_im" is a PIL Image object
        color_image_as_tensor = image_to_tensor_converter( im_pil )
        print("\n\n\nshape of the image tensor: %s" % str(color_image_as_tensor.shape))
        print("\n\n\ndisplaying the original color image")
        self.display_tensor_as_image(color_image_as_tensor, "original color image")
        ###   Let's first plot the histogram of the grayscale version of the image:
        gray_tensor = 0.4 * color_image_as_tensor[0]  +   0.4 * color_image_as_tensor[1]   + 0.2 * color_image_as_tensor[2]
        print("\n\n\ndisplaying the grayscale version of the color image")
        self.display_tensor_as_image(gray_tensor, "grayscale version of color image")
#        hist_gray = torch.histc(gray_tensor, bins = 255, min = 0.0, max = 256.0)
        hist_gray = torch.histc(gray_tensor, bins = 255, min = 0.0, max = 1.0)
        fig = plt.figure("plot of the histogram")
        ax = fig.add_subplot(111)
        ax.bar( np.linspace(1.0, 256, num = 255), hist_gray.numpy(), color='black' )
        print("\n\n\ndisplaying the hostogram of the graylevels")
        plt.show()
        print("\n\n\nNumber of pixels in the histogram: %s" % str(hist_gray.sum()))
        print("\n\n\nhist_gray: %s" % str(hist_gray))
        prob = hist_gray.div( hist_gray.sum() )
        cumulative_prob = prob.cumsum(0)           ##  this gives us a cumulative probability distribution
        print("\n\n\ncumulative_probability: %s" % str(cumulative_prob))
        print("\n\n\nnumber of bins in the cumulative prob: %s" % str(len(cumulative_prob)))       ## 255

        ###  For the rest of the implementation of the Otsu algo, the fact that the
        ###  histogram of the gray levels was calculated with the grayscale values scaled
        ###  to floating point numbers between 0 and 1 by the tensor representation IS NOT
        ###  NOT NOT NOT an issue.  That is because cumulative_prob is an array of 256
        ###  numbers, which each number corresponding one of 256 gray levels.
        hist = prob
        cumu_hist = cumulative_prob
        sigmaBsquared = {k : None for k in range(255)}
        for k in range(255):
             ###   Notice calling ".item()" on one-element tensors to extract the number being
             ###   held by them:
            omega0 = cumu_hist[k].item()
            omega1 = 1 - omega0
            if omega0 > 0 and omega1 > 0:
                mu0 = (1.0/omega0) * sum([i * hist[i].item() for i in range(0,k+1)])     
                mu1 = (1.0/omega1) * sum([i * hist[i].item() for i in range(k+1,255)])      
                sigmaBsquared[k] = omega0 * omega1 * (mu1 - mu0) ** 2
        sigmaBsquared = {k : sigmaBsquared[k] for k in range(255) if sigmaBsquared[k] is not None}

        sorted_thresholds = sorted(sigmaBsquared.items(), key=lambda x: x[1], reverse=True)
        print("\nThe threshold discovered by Otsu: %d" % sorted_thresholds[0][0])
        otsu_threshold = sorted_thresholds[0][0]
        thresholded_gray_image_as_tensor =  torch.clamp( gray_tensor, min=(otsu_threshold / float(256) ) )
#        thresholded_gray_image_as_tensor =  torch.clone(gray_tensor)
        tensor_shape = thresholded_gray_image_as_tensor.shape
        for i in range(tensor_shape[0]):
            for j in range(tensor_shape[1]):
                if thresholded_gray_image_as_tensor[i,j] < (otsu_threshold / float(256)):
                    thresholded_gray_image_as_tensor[i,j] = 0.0
        print("\n\n\nDisplaying the Otsu thresholded image")
        self.display_tensor_as_image(thresholded_gray_image_as_tensor, "otsu thresholded version")


    def convolutions_with_pytorch(self, image_file, kernel):
        '''
        Using torch.nn.functional.conv2d() for demonstrating a single image convolution with
        a specified kernel
        '''
        if os.path.isfile(image_file):
            im_pil = Image.open(image_file)
        else:
            sys.exit("the image file %s does not exist --- aborting" % image_file)

        image_to_tensor_converter = tvt.ToTensor()
        color_image_as_tensor = image_to_tensor_converter( im_pil )
        gray_tensor = 0.4 * color_image_as_tensor[0]  +   0.4 * color_image_as_tensor[1]   + 0.2 * color_image_as_tensor[2] 
        self.display_tensor_as_image(gray_tensor, "grayscale version for demonstrating convolution")

        gray_section = gray_tensor[100:200, 100:250]
        self.display_tensor_as_image(gray_section, "showing a 100x150 section of the grayscale image")

        ###  converting the convolutional kernel into a tensor:
        op = torch.Tensor( kernel )

        ###  The input to the "nn.functional.conv2d()" requires a tensor of shape
        ###
        ###       (batch_size, num_input_channels, image_height, image_width)
        ###
        ###  Since we are dealing with a single image for demonstrating how you can carry
        ###  out a convolution, in our case batch_size=1.  Additionally, the convolution
        ###  demo is on a grayscale image, so we must set num_input_channels=1.
        input = torch.Tensor(1, 1, gray_section.shape[0], gray_section.shape[1])

        ###   The second arg to the "nn.functional.conv2d()" invoked below is the kernel
        ###   you want to use for the convolution.  This kernel must have the same shape
        ###   as the input image.  So the first two shape parameters are the same as for
        ###   the input image.
        kernel = torch.Tensor(1, 1, op.shape[0], op.shape[1])

        print("\n\n\nshape of input: %s" % str(input.shape))
        print("\n\n\nshape of kernel: %s" % str(kernel.shape))  

        ###   Now we must stuff the gray image where it belongs in teh input tensor:
        input[0,0,:,:] = gray_section

        ###   Finally, we must stuff the kernel where it belongs in the kernel tensor:
        kernel[0,0,:,:] = op
        output = nn.functional.conv2d( input, kernel, stride=1, padding=1 )
        print(output)

        ###   In order to respect the input conditions required by the display function,
        ###   we now extract the convolved output from the result of the convolution:
        output = output[0,0,:,:]
        self.display_tensor_as_image( output, "the result of convolution on the image section" )


    def gaussian_smooth(self, pil_grayscale_image):
        '''
        This method smooths an image with a Gaussian of specified sigma.
        '''
        sigma = self.sigma
        width,height = pil_grayscale_image.size
#        gray_image = self.data_im
        gray_image_as_array = np.zeros((height, width), dtype="float")
        for i in range(0, height):
            for j in range(0, width):
                gray_image_as_array[(i,j)] = pil_grayscale_image.getpixel((j,i))
        self.gray_image_as_array = gray_image_as_array
        smoothing_op = _gaussian(sigma)
        smoothed_image_array = _convolution_2D(gray_image_as_array, smoothing_op)
#        self._display_and_save_array_as_image( smoothed_image_array, "_gaussian_smoothed__" + str(sigma) )
        height,width = smoothed_image_array.shape
        maxVal = smoothed_image_array.max()
        minVal = smoothed_image_array.min()
        newimage = Image.new("L", (width,height), (0,))
        for i in range(0, height):
            for j in range(0, width):
                displayVal = int( (smoothed_image_array[(i,j)] - minVal) * (255/(maxVal-minVal)) )
                newimage.putpixel((j,i), displayVal)
        self.displayImage3(newimage, "Gaussian Smoother: close window when done viewing")
#        image_name = "smoothed" + "_" + self.data_im_name
        image_name = "smoothed.png"
        newimage.save(image_name)        
        return newimage


    def visualize_segmentation_in_pseudocolor(self, pixel_blobs, color_map, label=""):
        '''
        Assigns a random color to each blob in the output of an image segmentation algorithm
        '''
        height,width = self.im_array.shape
        colorized_mask_image = Image.new("RGB", (width,height), (0,0,0))
        for blob_idx in sorted(pixel_blobs, key=lambda x: len(pixel_blobs[x]), reverse=True):
            for (i,j) in pixel_blobs[blob_idx]:
                colorized_mask_image.putpixel((j,i), color_map[blob_idx])
        seg_mask_image = colorized_mask_image.resize((width*self.image_size_reduction_factor,height*self.image_size_reduction_factor), Image.ANTIALIAS)
        self.displayImage6(seg_mask_image, label + "_segmentation")

    def visualize_segmentation_with_mean_gray(self, pixel_blobs, label=""):
        '''
        Assigns the mean color to each each blob in the output of an image segmentation algorithm
        '''
        height,width = self.im_array.shape
        gray_mask_image = Image.new("L", (width,height), (0))
        for blob_idx in sorted(pixel_blobs, key=lambda x: len(pixel_blobs[x]), reverse=True):
            pixel_blob = pixel_blobs[blob_idx]
            pixel_vals = np.array([self.im_array[pixel] for pixel in pixel_blob])
            gray_mean = int(np.mean(pixel_vals))
            for (i,j) in pixel_blobs[blob_idx]:
                gray_mask_image.putpixel((j,i), gray_mean)
        seg_mask_image = gray_mask_image.resize((width*self.image_size_reduction_factor,height*self.image_size_reduction_factor), Image.ANTIALIAS)
        self.displayImage6(seg_mask_image, label)

    def repair_blobs(self, merged_blobs, color_map, all_pairwise_similarities):
        '''
        The goal here to do a final clean-up of the blob by merging tiny pixel blobs with
        an immediate neighbor, etc.  Such a cleanup requires adjacency info regarding the
        blobs in order to figure out which larger blob to merge a small blob with.
        '''
        pairwise_adjacency  =  all_pairwise_similarities['adjacency']
        pairwise_color_homogeneity_val  =  all_pairwise_similarities['color_homogeneity']
        pairwise_gray_var_comp =  all_pairwise_similarities['gray_var']
        pairwise_texture_comp = all_pairwise_similarities['texture']

        singleton_blobs = [blob_id for blob_id in merged_blobs if len(merged_blobs[blob_id]) == 1]
        sorted_blobs = sorted(merged_blobs, key=lambda x: len(merged_blobs[x]))
        for blob_id in singleton_blobs:
            if blob_id not in merged_blobs: continue
            for blb_id in sorted_blobs:            
                if blb_id == blob_id: continue
                if blb_id not in merged_blobs: continue
                if blb_id > blob_id:
                    pair_label = "%d,%d" % (blb_id,blob_id)
                else:
                    pair_label = "%d,%d" % (blob_id,blb_id)                    
                if blb_id in merged_blobs and blob_id in merged_blobs and pairwise_adjacency[pair_label] is True:
                    merged_blobs[blb_id] += merged_blobs[blob_id]
                    del merged_blobs[blob_id]
        '''
        tiny_blobs = [blob_id for blob_id in merged_blobs if len(merged_blobs[blob_id]) < 5]
        sorted_blobs = sorted(merged_blobs, key=lambda x: len(merged_blobs[x]))
        for blob_id in tiny_blobs:
            for blb_id in sorted_blobs:            
                if blb_id == blob_id: continue
                if blb_id not in merged_blobs: continue
                if blb_id > blob_id:
                    pair_label = "%d,%d" % (blb_id,blob_id)
                else:
                    pair_label = "%d,%d" % (blob_id,blb_id)                    
                if (blb_id in merged_blobs) and (blob_id in merged_blobs) and  (pairwise_adjacency[pair_label] is True) and (len(merged_blobs[blb_id]) > 4):
                    merged_blobs[blb_id] += merged_blobs[blob_id]
                    del merged_blobs[blob_id]
        '''
        sorted_blobs = sorted(merged_blobs, key=lambda x: len(merged_blobs[x]))
        for blob_id in sorted_blobs:
            if len(merged_blobs[blob_id]) > 200: continue
            neighboring_blobs = []          
            for blb_id in sorted_blobs:
                if blb_id == blob_id: continue
                if blb_id > blob_id:
                    pair_label = "%d,%d" % (blb_id,blob_id)
                else:
                    pair_label = "%d,%d" % (blob_id,blb_id)                    

                if ( (pairwise_adjacency[pair_label] is True) and 
                     (pairwise_color_homogeneity_val[pair_label] < self.color_homogeneity_thresh) and 
                     (pairwise_gray_var_comp[pair_label] < self.gray_var_thresh) and 
                     (pairwise_texture_comp[pair_label] < self.texture_homogeneity_thresh) ):
                    neighboring_blobs.append(blb_id)
            if self.debug: 
                print("\n\n\nneighboring_blobs for blob %d: %s" % (blob_id, str(neighboring_blobs)))
            if len(neighboring_blobs) == 1 and len(merged_blobs[neighboring_blobs[0]]) > len(merged_blobs[blob_id]):
                merged_blobs[neighboring_blobs[0]] += merged_blobs[blob_id] 
                del merged_blobs[blob_id]
        return merged_blobs,color_map                              


    def selective_search_for_region_proposals(self, graph, image_name):
        '''
        This method implements the Selective Search (SS) algorithm proposed by Uijlings,
        van de Sande, Gevers, and Smeulders for creating region proposals for object
        detection.  As mentioned elsewhere here, that algorithm sits on top of the graph
        based image segmentation algorithm that was proposed by Felzenszwalb and
        Huttenlocher.  The parameter 'pixel_blobs' required by the method presented here
        is supposed to be the pixel blobs produced by the Felzenszwalb and Huttenlocher
        algorithm.
        '''
        def are_two_blobs_adjacent(blob1, blob2):
            '''
            We say that two pixel blobs with no pixels in common are adjacent if at
            least one pixel in one block is 8-adjacent to any of the pixels in the other
            pixel blob.
            '''
            for pixel_u in blob1:
                for pixel_v in blob2:
                    if abs(pixel_u[0] - pixel_v[0])  <= 1 and abs(pixel_u[1] - pixel_v[1]) <= 1:
                        return True
            return False

        def estimate_lbp_texture(blob, im_array):
            '''
             This method implements the Local Binary Patterns (LBP) method of charactering image
            textures. This algorithm, proposed by Ojala, Pietikainen, and Maenpaa
            generates a grayscale and rotationally invariant texture signature through
            what is referred to as an LBP histogram.  For a tutorial introduction to this
            method, see:
                   https://engineering.purdue.edu/kak/Tutorials/TextureAndColor.pdf
            The code presented below is borrowed from this tutorial.
            '''
            height_coords = [p[0] for p in blob]
            width_coords  = [p[1] for p in blob]
            bb_height_min = min(height_coords)
            bb_height_max = max(height_coords)
            bb_width_min  = min(width_coords)
            bb_width_max  = max(width_coords) 
            ###  Creata bounding box for each blob to make it more convenient to apply
            ###  the LBP logic to the blob:
            bb = [[0 for w in range(bb_width_max - bb_width_min + 1)] 
                              for h in range(bb_height_max - bb_height_min + 1)]
            for h in range(bb_height_max - bb_height_min + 1):
                for w in range(bb_width_max - bb_width_min + 1):
                    if (h+bb_height_min, w+bb_width_min) in blob:
                        bb[h][w] = im_array[h+bb_height_min,w+bb_width_min]
            if self.debug:
                print("\n\n\nbb: %s" % str(bb))
            R,P = 1,8
            rowmax,colmax = bb_height_max-bb_height_min+1 - R, bb_width_max - bb_width_min + 1 - R
            lbp_hist = {t:0 for t in range(P+2)}                                  
            ###  Visit each pixel and find the LBP vector at that pixel.            
            for h in range(rowmax):           
                for w in range(colmax):       
                    pattern = [] 
                    for p in range(P):                                               
                        #  We use the index k to point straight down and l to point to the 
                        #  right in a circular neighborhood around the point (i,j). And we 
                        #  use (del_k, del_l) as the offset from (i,j) to the point on the 
                        #  R-radius circle as p varies.
                        del_k,del_l = R*math.cos(2*math.pi*p/P), R*math.sin(2*math.pi*p/P)  
                        if abs(del_k) < 0.001: del_k = 0.0                                  
                        if abs(del_l) < 0.001: del_l = 0.0                                  
                        k, l =  h + del_k, w + del_l                                        
                        k_base,l_base = int(k),int(l)                                       
                        delta_k,delta_l = k-k_base,l-l_base                                 
                        if (delta_k < 0.001) and (delta_l < 0.001):                         
                            image_val_at_p = float(bb[k_base][l_base])                   
                        elif (delta_l < 0.001):                                             
                            image_val_at_p = (1 - delta_k) * bb[k_base][l_base] +  \
                                                          delta_k * bb[k_base+1][l_base] 
                        elif (delta_k < 0.001):                                             
                            image_val_at_p = (1 - delta_l) * bb[k_base][l_base] +  \
                                                          delta_l * bb[k_base][l_base+1] 
                        else:                                                               
                            image_val_at_p = (1-delta_k)*(1-delta_l)*bb[k_base][l_base] + \
                                             (1-delta_k)*delta_l*bb[k_base][l_base+1]  + \
                                             delta_k*delta_l*bb[k_base+1][l_base+1]  + \
                                             delta_k*(1-delta_l)*bb[k_base+1][l_base]   
                        if image_val_at_p >= bb[h][w]:                                  
                            pattern.append(1)                                              
                        else:                                                              
                            pattern.append(0)                                              
                    if self.debug:
                        print("pattern: %s" % pattern)                                         
                    bv =  BitVector.BitVector( bitlist = pattern )                         
                    intvals_for_circular_shifts  =  [int(bv << 1) for _ in range(P)]       
                    minbv = BitVector.BitVector( intVal = min(intvals_for_circular_shifts), size = P )   
                    if self.debug:
                        print("minbv: %s" % minbv)                                               
                    bvruns = minbv.runs()                                                    
                    encoding = None
                    if len(bvruns) > 2:                                                
                        lbp_hist[P+1] += 1                                             
                        encoding = P+1                                                 
                    elif len(bvruns) == 1 and bvruns[0][0] == '1':                     
                        lbp_hist[P] += 1                                               
                        encoding = P                                                   
                    elif len(bvruns) == 1 and bvruns[0][0] == '0':                     
                        lbp_hist[0] += 1                                               
                        encoding = 0                                                   
                    else:                                                              
                        lbp_hist[len(bvruns[1])] += 1                                  
                        encoding = len(bvruns[1])                                      
                    if self.debug:
                        print("encoding: %s" % encoding)                                   
            if self.debug:
                print("\nLBP Histogram: %s" % lbp_hist)                                    
            lbp_array = np.zeros(len(lbp_hist))
            for i in range(len(lbp_hist)): lbp_array[i] = lbp_hist[i]
            return lbp_array
            ###  End of Texture operator definition

        ###  BEGIN CODE FOR SELECTIVE-SEARCH BASED MERGING OF THE BLOBS
        ###  BUT FIRST WE COMPUTE UNARY AND BINARY ATTRIBUTES OF THE BLOBS.
        pixel_blobs,E = graph
        ###  We need access to the underlying image to fetch the pixel values for the blobs
        ###  in question:
        im_array_color  =    np.asarray(self.low_res_PIL_image_color)
        im_array_gray = self.im_array
        ###  Compute unary properties of blobs:
        color_mean_vals = {}
        gray_mean_vals = {}
        gray_vars = {}
        texture_vals = {}
        sorted_blobs = sorted(pixel_blobs, key=lambda x: len(pixel_blobs[x]), reverse=True)
        for blob_id in sorted_blobs:
            pixel_blob = pixel_blobs[blob_id]
#            pixel_vals_color = np.array([im_array_color[pixel] for pixel in pixel_blob])
            pixel_vals_color = [im_array_color[pixel[0],pixel[1],:].tolist() for pixel in pixel_blob]
            pixel_vals_gray =  np.array([im_array_gray[pixel] for pixel in pixel_blob])
            color_mean_vals[blob_id]  = [ float(sum([pix[j] for pix in pixel_vals_color])) / float(len(pixel_vals_color)) for j in range(3) ]
            gray_mean_vals[blob_id] =  np.mean(pixel_vals_gray)
            gray_vars[blob_id] = np.var(pixel_vals_gray)
            texture_vals[blob_id] = estimate_lbp_texture(pixel_blob, im_array_gray)
        if self.debug:
            print("\n\n\ncolor_mean_vals: %s" % str(color_mean_vals))
            print("\n\n\ngray_mean_vals: %s" % str(gray_mean_vals))
            print("\n\n\ngray_vars: %s" % str(gray_vars))
            print("\n\n\ntexture_vals: %s" % str(texture_vals))

        ###  Compute pairwise similarity scores:
        all_pairwise_similarities = {}
        pairwise_adjacency = {}
        pairwise_gray_homogeneity_val = {}
        pairwise_color_homogeneity_val = {}
        pairwise_gray_var_comp = {}
        pairwise_texture_comp   = {}
        all_pairwise_similarities['adjacency'] = pairwise_adjacency
        all_pairwise_similarities['color_homogeneity'] = pairwise_color_homogeneity_val
        all_pairwise_similarities['gray_var'] = pairwise_gray_var_comp
        all_pairwise_similarities['texture'] = pairwise_texture_comp

        for blob_id_1 in pixel_blobs:
            for blob_id_2 in pixel_blobs:
                if blob_id_1 > blob_id_2:
                    pair_id = str("%d,%d" % (blob_id_1,blob_id_2))
                    pairwise_adjacency[pair_id] = True if pair_id in E else False
                    pairwise_gray_homogeneity_val[pair_id] = abs(gray_mean_vals[blob_id_1]
                                                                  - gray_mean_vals[blob_id_2])
                    pairwise_color_homogeneity_val[pair_id] = [abs(color_mean_vals[blob_id_1][j] 
                                               - color_mean_vals[blob_id_2][j]) for j in range(3)]
                    pairwise_gray_var_comp[pair_id] = abs(gray_vars[blob_id_1] - gray_vars[blob_id_2])
                    pairwise_texture_comp[pair_id] =  np.linalg.norm(texture_vals[blob_id_1] - 
                                                                     texture_vals[blob_id_2])
        if self.debug:
            print("\n\n\npairwise_adjacency: %s" % str(pairwise_adjacency))
            print("\n\n\npairwise_gray_homogeneity_val: %s" % str(pairwise_gray_homogeneity_val))
            print("\n\n\npairwise_color_homogeneity_val: %s" % str(pairwise_color_homogeneity_val))
            print("\n\n\npairwise_gray_var_comp: %s" % str(pairwise_gray_var_comp))
            print("\n\n\npairwise_texture_comp: %s" % str(pairwise_texture_comp)) 

        ###  Initialize merged blocks
        merged_blobs = pixel_blobs
        if self.debug:
            print("\n\n\ninitial blobs: %s" % str(pixel_blobs))
        next_blob_id = max(merged_blobs.keys()) + 1
        ###  You have to be careful with the program flow in the blob merging block of
        ###  code shown below in order to deal with the fact that you are modifying the
        ###  blobs as you iterate through them.  You merge two blobs because they are
        ###  adjacent and because they are color and texture homogeneous.  However, when
        ###  you merge two blobs, the original blobs must be deleted from the blob
        ###  dictionary.  At the same time, you must compute the unary properties of the
        ###  newly formed blob and also estimate its pairwise properties with respect to
        ###  all the other blobs in the blob dictionary.
        ss_iterations = 0
        '''
        In this version, we will make only one pass through the 'while' loop shown below
        because, in the UPDATE of the PAIRWISE PROPERTIES, I have not yet included
        those pairs that involve the latest LATEST NEW blob vis-a-vis the other older
        NEWLY DISCOVERED blobs.  In any case, my experience has shown that you need
        just one pass for the images in the Examples directory.  However, it is
        possible that, for complex imagery, you may need multiple (even an
        indeterminate number of) passes through the blob merging code shown below.
        '''
        while ss_iterations < 1:
            sorted_up_blobs = sorted(merged_blobs, key=lambda x: len(merged_blobs[x]))
            sorted_down_blobs = sorted(merged_blobs, key=lambda x: len(merged_blobs[x]), reverse=True)
            for blob_id_1 in sorted_up_blobs:
                if blob_id_1 not in merged_blobs: continue
                for blob_id_2 in sorted_down_blobs[:-1]:        # the largest blob is typically background
                    if blob_id_2 not in merged_blobs: continue
                    if blob_id_1 not in merged_blobs: break
                    if blob_id_1 > blob_id_2:
                        pair_id = "%d,%d" % (blob_id_1,blob_id_2)   
#                        if (pair_id in pairwise_adjacency) and (pairwise_adjacency[pair_id] is True):
                        if (pairwise_color_homogeneity_val[pair_id][0] < self.color_homogeneity_thresh[0])\
                           and                                                                   \
                           (pairwise_color_homogeneity_val[pair_id][1] < self.color_homogeneity_thresh[1])\
                           and                                                                   \
                           (pairwise_color_homogeneity_val[pair_id][2] < self.color_homogeneity_thresh[2])\
                           and                                                                    \
                           (pairwise_gray_var_comp[pair_id] < self.gray_var_thresh)               \
                           and                                                                    \
                           (pairwise_texture_comp[pair_id] < self.texture_homogeneity_thresh):          
                            if self.debug:
                                print("\n\n\nmerging blobs of id %d and %d" % (blob_id_1, blob_id_2))
                            new_merged_blob = merged_blobs[blob_id_1] +  merged_blobs[blob_id_2] 
                            merged_blobs[next_blob_id] = new_merged_blob
                            del merged_blobs[blob_id_1]
                            del merged_blobs[blob_id_2]
                            ###  We need to estimate the unary properties of the newly created
                            ###  blob:
                            pixel_vals_color = [im_array_color[pixel[0],pixel[1],:].tolist() for pixel in 
                                                                                    new_merged_blob]
                            pixel_vals_gray = np.array([im_array_gray[pixel] for pixel in new_merged_blob])
                            color_mean_vals[next_blob_id]  = [float(sum([pix[j] for pix in \
                                pixel_vals_color])) / float(len(pixel_vals_color)) for j in range(3)]
                            gray_mean_vals[next_blob_id] = np.mean(pixel_vals_gray)
                            gray_vars[next_blob_id] = np.var(pixel_vals_gray)
                            texture_vals[next_blob_id] = estimate_lbp_texture(new_merged_blob, im_array_gray)
                            ###  Now that we have merged two blobs, we need to create entries
                            ###  in pairwise dictionaries for entries related to this new blob
                            for blb_id in sorted_up_blobs:
                                if blb_id not in merged_blobs: continue
                                if next_blob_id > blb_id:
                                    pair_id = "%d,%d" % (next_blob_id, blb_id)
                                    pairwise_adjacency[pair_id] = \
                  True if are_two_blobs_adjacent(new_merged_blob, pixel_blobs[blb_id]) else False
                                    pairwise_color_homogeneity_val[pair_id] = \
                  [abs(color_mean_vals[next_blob_id][j]  - color_mean_vals[blb_id][j]) for j in range(3)]
                                    pairwise_gray_homogeneity_val[pair_id] = \
                                         abs(gray_mean_vals[next_blob_id] - gray_mean_vals[blb_id])
                                    pairwise_gray_var_comp[pair_id] = \
                                         abs(gray_vars[next_blob_id] - gray_vars[blb_id])
                                    pairwise_texture_comp[pair_id] =  \
                                np.linalg.norm(texture_vals[next_blob_id] - texture_vals[blb_id])
                    next_blob_id += 1                           
            ss_iterations += 1

        num_pixels_in_final_merged_blobs = sum( [len(blob) for _,blob in merged_blobs.items()] )
        print("\n\n\ntotal number of pixels in all merged blobs: %d" % num_pixels_in_final_merged_blobs)
        ###  color_map is a dictionary with blob_ids as keys and the assigned values the color
        ###  assigned to each blob for its visualization

        bounding_boxes = {}
        retained_vertex_list = []
        total_pixels_in_output = 0
        color_map = {}
        for blob_idx in sorted(merged_blobs, key=lambda x: len(merged_blobs[x]), reverse=True)[:self.max_num_blobs_expected]:
            color_map[blob_idx] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
            all_pixels_in_blob = merged_blobs[blob_idx]
            total_pixels_in_output += len(all_pixels_in_blob)
            retained_vertex_list.append(blob_idx)
            height_coords = [p[0] for p in all_pixels_in_blob]
            width_coords  = [p[1] for p in all_pixels_in_blob]
            bb_height_min = min(height_coords)
            bb_height_max = max(height_coords)
            bb_width_min  = min(width_coords)
            bb_width_max  = max(width_coords)
            bounding_boxes[blob_idx] = [bb_height_min, bb_width_min, bb_height_max, bb_width_max]

        print("\n\n\nTotal number of pixels in output blobs: %d" % total_pixels_in_output)
        title = "selective_search_based_bounding_boxes"
        arr_height,arr_width = im_array_gray.shape
        colorized_mask_image = Image.new("RGB", (arr_width,arr_height), (0,0,0))
        for blob_idx in retained_vertex_list:
            for (i,j) in merged_blobs[blob_idx]:
                colorized_mask_image.putpixel((j,i), color_map[blob_idx])
        mw = Tkinter.Tk()
        winsize_w,winsize_h = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_w = int(0.5 * screen_width)
            winsize_h = int(winsize_w * (arr_height * 1.0 / arr_width))            
        else:
            winsize_h = int(0.5 * screen_height)
            winsize_w = int(winsize_h * (arr_width * 1.0 / arr_height))
        scaled_image =  colorized_mask_image.copy().resize((winsize_w,winsize_h), Image.ANTIALIAS)
        mw.title(title) 
        mw.configure( height = winsize_h, width = winsize_w )         
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_h,            
                             width = winsize_w,             
                             cursor = "crosshair" )   
        canvas.pack(fill=BOTH, expand=True)
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = title + ".eps") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        photo = ImageTk.PhotoImage( scaled_image )
        canvas.create_image(winsize_w//2,winsize_h//2,image=photo)
        scale_w = winsize_w / float(arr_width)
        scale_h = winsize_h / float(arr_height)
        for v in bounding_boxes:
            bb = bounding_boxes[v]
            canvas.create_rectangle( (bb[1]*scale_w,bb[0]*scale_h,(bb[3]+1)*scale_w,(bb[2]+1)*scale_h), width='3', outline='red' )
        canvas.update()
        mw.update()
        print("\n\n\nIterations used: %d" % self.iterations_used)
        print("\n\n\nNumber of region proposals: %d" % len(bounding_boxes))
        mw.mainloop()
        if os.path.isfile(title + ".eps"):
            Image.open(title + ".eps").save(title + ".png")
            os.remove(title + ".eps")
        retained_vertices = {}
        for u in retained_vertex_list:
            retained_vertices[u] = merged_blobs[u]
        return retained_vertices, color_map

        def are_two_blobs_color_homogeneous(blob1, blob2, image):
            color_in_1 = [image[pixel] for pixel in blob1]
            color_in_2 = [image[pixel] for pixel in blob2]
            mean_diff = abs(np.mean(color_in_1) - np.mean(color_in_2))
            var1 = np.var(color_in_1)
            var2 = np.var(color_in_2)
            if var1 < self.var_threshold and var2 < self.var_thresh and mean_diff < self.mean_diff_thresh:
                return True
            return False

        def are_two_blobs_texture_homogeneous(blob1, blob2, image):
            lbp_hist_1 = estimate_lbp_texture(blob1)
            lpb_hist_2 = estimate_lbp_texture(blob2)
            if np_norm( np.to_array(lbp_hist_1) - np.to_array(lbp_hist_2) ) < self.texture_thresh:
                return True
            return False               

    def graph_based_segmentation(self, image_name, num_blobs_wanted=None):
        '''
        This is an implementation of the Felzenszwalb and Huttenlocher algorithm for
        graph-based segmentation of images.  At the moment, it is limited to working
        on grayscale images.
        '''
        ###  image_name may be a file, in which case it needs to be opened, or directly
        ###  a PIL.Image object
        try:
            image_pil_color = Image.open(image_name)
        except:
            image_pil_color = image_name                           ### needed for the interactive mode
        width,height = image_pil_color.size
        kay = self.kay
        print("\n\n\nImage of WIDTH=%d  and  HEIGHT=%d   being processed by graph_based_segmentation" % (width,height))
        self.displayImage6(image_pil_color, "input_image -- size: width=%d height=%d" % (width,height))
        kay = self.kay
        input_image_gray = image_pil_color.copy().convert("L")      ## first convert the image to grayscale
        if self.sigma > 0:
            smoothed_image_gray = self.gaussian_smooth(input_image_gray) 
            ##  we do NOT need a smoothed version of the original color image
        else:
            smoothed_image_gray = input_image_gray
        image_size_reduction_factor = self.image_size_reduction_factor
        width_to = width // image_size_reduction_factor
        height_to = height // image_size_reduction_factor
        if self.image_normalization_required:
            gray_resized_normalized = tvt.Compose( [tvt.Grayscale(num_output_channels = 1), tvt.Resize((height_to,width_to)), tvt.ToTensor(), tvt.Normalize(mean=[0.5], std=[0.5]) ] )
            color_resized_normalized = tvt.Compose( [tvt.Resize((height_to,width_to)), tvt.ToTensor(), tvt.Normalize(mean=[0.5], std=[0.5]) ] )
            img_tensor_gray = gray_resized_normalized(smoothed_image_gray)
            ### we do NOT need a smoothed version of the color image:
            img_tensor_color = color_resized_normalized(image_pil_color)
            to_image_xform = tvt.Compose([tvt.ToPILImage()])
            low_res_PIL_image_gray = to_image_xform(img_tensor_gray)
            low_res_PIL_image_color = to_image_xform(img_tensor_color)
        else:
            low_res_PIL_image_gray = smoothed_image_gray.resize((width_to,height_to), Image.ANTIALIAS)
            low_res_PIL_image_color = image_pil_color.resize((width_to,height_to), Image.ANTIALIAS)
        self.low_res_PIL_image_gray = low_res_PIL_image_gray
        self.low_res_PIL_image_color = low_res_PIL_image_color
        self.displayImage6(low_res_PIL_image_gray, "low_res_version_of_original")
        ###   VERY IMPORTANT:  In PIL.Image, the first coordinate refers to the width-wise coordinate
        ###                    and the second coordinate to the height-wise coordinate pointing downwards
        ###   However:         In numpy and tensor based representations, the first coordinate is the
        ###                    height-wise coordinate and the second coordiante the width-wise coordinate.
        ###   Since the tensor operations cause the grayscale image to be represented
        ###   by a 3D array, with the first dimension set to the number of channels
        ###   (which would be 1 for a grayscale image), we need to ignore it:
        img_array = np.asarray(low_res_PIL_image_gray)
        self.im_array = img_array
        arr_height,arr_width = img_array.shape
        print("\n\n\nimage array size: height=%d  width=%d" % (arr_height,arr_width))

        initial_num_graph_vertices = arr_height * arr_width
        print("\n\n\nnumber of vertices in graph: %d" % initial_num_graph_vertices)
        initial_graph_vertices = {i : None for i in range(initial_num_graph_vertices)}
        for i in range(initial_num_graph_vertices):
            h,w  =  i // arr_width, i - (i // arr_width)*arr_width
            initial_graph_vertices[i] = [(h,w)]
      
        initial_graph_edges = {}
        MInt = {}
        for i in range(initial_num_graph_vertices):
            hi,wi =  initial_graph_vertices[i][0]
            for j in range(initial_num_graph_vertices):
                hj,wj =  initial_graph_vertices[j][0]
                if i > j:
                    if abs(hi - hj) <= 1 and abs(wi - wj) <= 1:
                        ###  In order to take care of the error report: "overflow encountered in 
                        ###  ubyte_scalars":
                        ###  Since pixels are stored as the uint8 datatype (which implies that
                        ###  their values are only expected to be between 0 and 255), any 
                        ###  arithmetic on them could violate that range.  So we must first convert
                        ###  into the int datatype:
                        initial_graph_edges["%d,%d" % (i,j) ]  =  abs(int(img_array[hi,wi]) - int(img_array[hj,wj]))
                        MInt[ "%d,%d" % (i,j) ] = kay

        ###   INTERNAL DIFFERENCE property at the initial vertices in the graph
        ###   Internal Difference is defined as the max edge weight between the pixels in the pixel
        ###   blob represented by a graph vertex.
        Int_prop = {v : 0.0 for v in initial_graph_vertices}
        MInt_prop = {v : kay for v in initial_graph_vertices}   
        if self.debug:
            print("\n\n\ninitial graph_vertices: %s" % str(sorted(initial_graph_vertices.items())))
            print("\n\n\nnumber of vertices in initial graph: %d" % len(initial_graph_vertices))
            print("\n\n\ninitial graph_edges: %s" % str(sorted(initial_graph_edges.items())))
            print("\n\n\nnumber of edges in initial graph: %d" % len(initial_graph_edges))
            print("\n\n\ninitial MInt: %s" % str(sorted(MInt.items())))
            print("\n\n\nnumber of edges in initial MInt: %d" % len(MInt))

        initial_graph = (copy.deepcopy(initial_graph_vertices), copy.deepcopy(initial_graph_edges))

        def find_all_connections_for_a_vertex(vert, graph):
            vertices = graph[0]
            edges    = graph[1]
            print("pixels in vertex %d: %s" % (vert, str(vertices[vert])))
            connected_verts_in_graph = []
            for edge in edges:
                end1,end2 = int(edge[:edge.find(',')]), int(edge[edge.find(',')+1 :])                 
                if vert == end1:
                    connected_verts_in_graph.append(end2)
                elif vert == end2:
                    connected_verts_in_graph.append(end1)
            return connected_verts_in_graph

        index_for_new_vertex = len(initial_graph_vertices)
        master_iteration_index = 0
        self.iterations_terminated = False
        ###   graph = (V,E) with both V and E as dictionaries.
        ###   NOTE: The edges E in the graph stand for 'Dif(C1,C2)' in F&H
        def seg_gen( graph, MInt, index_for_new_vertex, master_iteration_index, Int_prop, MInt_prop, kay ):
            print("\n\n\n=========================== Starting iteration %d ==========================" % master_iteration_index)
            V,E = graph
            if num_blobs_wanted is not None and len(initial_graph[0]) > num_blobs_wanted:
                if num_blobs_wanted is not None and len(V) <= num_blobs_wanted: return graph
            if self.debug:
                print("\n\n\nV: %s" % str(V))
                print("\n\n\nE: %s" % str(E))
                print("\n\n\nMInt: %s" % str(MInt))
            max_iterations = self.max_iterations
            print("\n\n\nNumber of region proposals at the current level of merging: %d" % len(V))
            if len(E) == 0:
                print("\n\n\nThe graph has no edges left")
                return graph
            sorted_vals_and_edges = list( sorted( (v,k) for k,v in E.items() ) )
            sorted_edges = [x[1] for x in sorted_vals_and_edges]
            print("\n\n\n[Iter Index: %d] Dissiminarity value associated with the most similar edge: %s" % (master_iteration_index, str(sorted_vals_and_edges[0])))
            print("\nOne dot represents 100 possible merge operations in the graph representation of the image\n")
            edge_counter = 0

            ###  You have to be careful when debugging the code in the following 'for' loop.  The
            ###  problem is that the sorted edge list is made from the ogiginal edge list which is
            ###  modified by the code in the 'for' loop.  Let's say that the edge 'u,v' is a good
            ###  candidate for the merging of the pixel blobs corresponding to u and v.  After the
            ###  'for' loop has merged these two blobs corresponding to these two vertices, the 'u'
            ###  and 'v' vertices in the graph do not exist and must be deleted.  Deleting these two
            ###  vertices requires that we must also delete from E all the other edges that connect
            ###  with either u and v.  So if you are not careful, it is possible that in the next
            ###  go-around in the 'for' loop you will run into one of those edges as the next
            ###  candidate for the merging of two vertices.
            for edge in sorted_edges:
                if edge not in E: continue
                edge_counter += 1
                if edge_counter % 100 == 0: 
                    sys.stdout.write(". ")
                    sys.stdout.flush()
                ###  This is the fundamental condition for merging the pixel blobs corresponding to
                ###  two different vertices: The 'Diff' edge weight, which is represented by the
                ###  edge weight E[edge], must be LESS than the minimum of the Internal component
                ###  edge weight, the minimum being over the two vertices for the two pixel blobs.
                if E[edge] >  MInt[edge]: 
                    del E[edge]
                    del MInt[edge]
                    continue 
                ###  Let us now find the identities of the vertices of the edge whose two vertices
                ###  are the best candidates for the merging of the two pixel blobs.
                vert1,vert2 = int(edge[:edge.find(',')]), int(edge[edge.find(',')+1 :])
                if self.debug:
                    print("\n\n\n[Iter Index: %d] The least disimilar two vertices in the graph are: %s and %s" % (master_iteration_index, vert1, vert2))
                ###   Since we want to go through all the edges in 'sorted_edges" WHILE we are
                ###   deleting the vertices that are merged and the edges that are no longer
                ###   relevant because of vertex deletion, we need to be careful foing forward:
                if (vert1 not in V) or (vert2 not in V): continue
                affected_edges = []
                for edg in E:
                    end1,end2 = int(edg[:edg.find(',')]), int(edg[edg.find(',')+1 :])                
                    if (vert1 == end1) or (vert1 == end2) or (vert2 == end1) or (vert2 == end2):
                        affected_edges.append(edg)
                if self.debug:
                    print("\n\n\naffected edges to be deleted: %s" % str(affected_edges))
                for edg in affected_edges:
                    del E[edg]
                    del MInt[edg]
                merged_blob = V[vert1] + V[vert2]
#                change_flag = True
                if self.debug:
                    print("\n\n\nAdded vertex %d to V" % index_for_new_vertex)
                V[index_for_new_vertex] = merged_blob
                if self.debug:
                    print("\n\n\n[Iter Index: %d] index for new vertex: %d   and the merged blob: %s" % (master_iteration_index, index_for_new_vertex, str(merged_blob)))
                ###   We will now calculate the Int (Internal Difference) and MInt property to be
                ###   to be associated with the newly created vertex in the graph:
                within_blob_edge_weights = []
                for u1 in merged_blob:
                    i = u1[0] * arr_width + u1[1]
                    for u2 in merged_blob:
                        j = u2[0] * arr_width + u2[1]
                        if i > j:
                            ij_key = "%d,%d" % (i,j)
                            if ij_key in initial_graph_edges:
                                within_blob_edge_weights.append( initial_graph_edges[ ij_key ] )
                Int_prop[index_for_new_vertex] = max(within_blob_edge_weights) 
                MInt_prop[index_for_new_vertex] = Int_prop[index_for_new_vertex] + kay / float(len(merged_blob))
                ###   Now we must calculate the new graph edges formed by the connections between the newly
                ###   formed node and all other nodes.  However, we first must delete the two nodes that
                ###   we just merged:
                del V[vert1] 
                del V[vert2]
                del Int_prop[vert1]
                del Int_prop[vert2]
                del MInt_prop[vert1]
                del MInt_prop[vert2]
                if self.debug:
                    print("\n\n\nThe modified vertices: %s" % str(V))
                for v in sorted(V):
                    if v == index_for_new_vertex: continue
                    ###   we need to store the edge weights for the pixel-to-pixel edges
                    ###   in the initial graph with one pixel in the newly constructed
                    ###   blob and other in a target blob
                    pixels_in_v = V[v]
                    for u_pixel in merged_blob:
                        i = u_pixel[0] * arr_width + u_pixel[1]
                        inter_blob_edge_weights = []
                        for v_pixel in pixels_in_v:
                            j = v_pixel[0] * arr_width + v_pixel[1]
                            if i > j: 
                                ij_key = "%d,%d" % (i,j)
                            else:
                                ij_key = "%d,%d" % (j,i)
                            if ij_key in initial_graph_edges:
                                inter_blob_edge_weights.append( initial_graph_edges[ij_key ] )
                        if len(inter_blob_edge_weights) > 0:
                            uv_key = str("%d,%d" % (index_for_new_vertex,v))
                            E[uv_key] = min(inter_blob_edge_weights)                        
                            MInt[uv_key] = min( MInt_prop[index_for_new_vertex], MInt_prop[v] )
                if self.debug:
                    print("\n\n\nAt the bottom of for-loop for edges ---   E: %s" % str(E))
                    print("\n\nMInt: %s" % str(MInt))
                index_for_new_vertex = index_for_new_vertex + 1   
#                if change_flag is False: break
    
            new_graph = (copy.deepcopy(V), copy.deepcopy(E))
            MInt = copy.deepcopy(MInt)
            if self.debug:
                print("\n\n\nnew graph at end of iteration: %s" % str(new_graph))
            if master_iteration_index == max_iterations:
                return new_graph
            else:
                self.iterations_used = master_iteration_index
                master_iteration_index += 1
                if self.iterations_terminated:
                    return new_graph
                else:
                    return seg_gen(new_graph, MInt, index_for_new_vertex, master_iteration_index, Int_prop, MInt_prop, kay)  
        segmented_graph = seg_gen(initial_graph, MInt, index_for_new_vertex, master_iteration_index, Int_prop, MInt_prop, kay)
        if self.debug:
            print("\n\n\nsegmented_graph: %s" % str(segmented_graph))
        bounding_boxes = {}
        total_pixels_in_output = 0
        retained_vertex_list = []
        for vertex in sorted(segmented_graph[0]):
            all_pixels_in_blob = segmented_graph[0][vertex]
            total_pixels_in_output += len(all_pixels_in_blob)
            if len(all_pixels_in_blob) > self.min_size_for_graph_based_blobs:
                print("\n\n\npixels in blob indexed %d: %s" % (vertex, str(segmented_graph[0][vertex])))
                retained_vertex_list.append(vertex)
                height_coords = [p[0] for p in all_pixels_in_blob]
                width_coords  = [p[1] for p in all_pixels_in_blob]
                bb_height_min = min(height_coords)
                bb_height_max = max(height_coords)
                bb_width_min  = min(width_coords)
                bb_width_max  = max(width_coords)
                """
                if (abs(bb_width_max - bb_width_min) <= 2 or abs(bb_height_max - bb_height_min) <= 2): continue
                if abs(bb_width_max - bb_width_min) < 0.1 * abs(bb_height_max - bb_height_min): continue
                if abs(bb_height_max - bb_height_min)  <  0.1 * abs(bb_width_max - bb_width_min): continue
                """
                bounding_boxes[vertex] = [bb_height_min, bb_width_min, bb_height_max, bb_width_max]

        print("\n\n\nTotal number of pixels in output blobs: %d" % total_pixels_in_output)
        title = "graph_based_bounding_boxes"
        mw = Tkinter.Tk()
        winsize_w,winsize_h = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_w = int(0.5 * screen_width)
            winsize_h = int(winsize_w * (arr_height * 1.0 / arr_width))            
        else:
            winsize_h = int(0.5 * screen_height)
            winsize_w = int(winsize_h * (arr_width * 1.0 / arr_height))
        scaled_image =  image_pil_color.copy().resize((winsize_w,winsize_h), Image.ANTIALIAS)
        mw.title(title) 
        mw.configure( height = winsize_h, width = winsize_w )         
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_h,            
                             width = winsize_w,             
                             cursor = "crosshair" )   
        canvas.pack(fill=BOTH, expand=True)
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = title + ".eps") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        photo = ImageTk.PhotoImage( scaled_image )
        canvas.create_image(winsize_w//2,winsize_h//2,image=photo)
        scale_w = winsize_w / float(arr_width)
        scale_h = winsize_h / float(arr_height)
        for v in bounding_boxes:
            bb = bounding_boxes[v]
            print("\n\n\nFor region proposal with ID %d, the bounding box is: %s" % (v, str(bb)))
            canvas.create_rectangle( (bb[1]*scale_w,bb[0]*scale_h,(bb[3]+1)*scale_w,(bb[2]+1)*scale_h), width='3', outline='red' )
        canvas.update()
        mw.update()
        print("\n\n\nIterations used: %d" % self.iterations_used)
        print("\n\n\nNumber of region proposals: %d" % len(bounding_boxes))
        mw.mainloop()
        if os.path.isfile(title + ".eps"):
            Image.open(title + ".eps").save(title + ".png")
            os.remove(title + ".eps")

        retained_vertices = {}
        retained_edges = {}
        for u in retained_vertex_list:
            retained_vertices[u] = segmented_graph[0][u]
            for v in retained_vertex_list:
                if u > v:
                    uv_label = "%d,%d"%(u,v)
                    if uv_label in segmented_graph[1]:
                        retained_edges[uv_label] = segmented_graph[1][uv_label]
        output_segmentation_graph = (retained_vertices, retained_edges)

        ###  color_map is a dictionary with blob_ids as keys and the assigned values the color
        ###  assigned to each blob for its visualization
        color_map = {}
        for blob_idx in sorted(output_segmentation_graph[0], key=lambda x: len(output_segmentation_graph[0][x]), reverse=True):
            if blob_idx not in color_map:
                color_map[blob_idx] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
        return output_segmentation_graph, color_map

    def graph_based_segmentation_for_arrays(self, which_one):
        '''
        This method is provided to enable the user to play with small arrays when
        experimenting with graph-based logic for image segmentation.  At the moment, it
        provides three small arrays, one under the "which_one==1" option, one under the
        "which_one==2" option, and the last under the "which_one==3" option.
        '''
        print("\nExperiments with selective-search logic on made-up arrays")
        kay = self.kay
        if which_one == 1:
            img_array = np.zeros((20,24), dtype = np.float)             ## height=20  width=24
            arr_height,arr_width = img_array.shape
            print("\n\n\nimage array size: height=%d  width=%d" % (arr_height,arr_width))
            for h in range(arr_height):
                for w in range(arr_width):
                    if ((4 < h < 8) or (12 < h < 16)) and ((4 < w < 10) or (14 < w < 20)):
                        img_array[h,w] = 200
            print("\n\n\nimg_array:")
            print(img_array)
            image_pil = Image.fromarray(img_array.astype('uint8'), 'L')
            self.displayImage3(image_pil, "made-up image")
            image_pil.save("array1.png")
        elif which_one == 2:
            img_array = np.zeros((6,10), dtype = np.float)             ## height=6  width=10
            arr_height,arr_width = img_array.shape
            print("\n\n\nimage array size: height=%d  width=%d" % (arr_height,arr_width))
            for h in range(arr_height):
                for w in range(arr_width):
                    if (1 < h < 4) and ((1 < w < 4) or (6 < w < 9)):
                        img_array[h,w] = 128
            print("\n\n\nimg_array:")
            print(img_array)
            image_pil = Image.fromarray(img_array.astype('uint8'), 'L')
            self.displayImage3(image_pil, "made-up image")
            image_pil.save("array2.png")
        else:
            img_array = np.zeros((20,24), dtype = np.float)            ## height=20  width=24
            arr_height,arr_width = img_array.shape
            print("\n\n\nimage array size: height=%d  width=%d" % (arr_height,arr_width))
            for h in range(4,arr_height-4):
                for w in range(4,arr_width-4):
                    img_array[h,w] = 100
            for h in range(8,arr_height-8):
                for w in range(8,arr_width-8):
                    img_array[h,w] = 200
            print("\n\n\nimg_array:")
            print(img_array)
            image_pil = Image.fromarray(img_array.astype('uint8'), 'L')
            self.displayImage3(image_pil, "made-up image")
            image_pil.save("array3.png")

        initial_num_graph_vertices = arr_height * arr_width
        print("\n\n\nnumber of vertices in graph: %d" % initial_num_graph_vertices)
        initial_graph_vertices = {i : None for i in range(initial_num_graph_vertices)}
        for i in range(initial_num_graph_vertices):
            h,w  =  i // arr_width, i - (i // arr_width)*arr_width
            initial_graph_vertices[i] = [(h,w)]
      
        initial_graph_edges = {}
        MInt = {}
        for i in range(initial_num_graph_vertices):
            hi,wi =  initial_graph_vertices[i][0]
            for j in range(initial_num_graph_vertices):
                hj,wj =  initial_graph_vertices[j][0]
                if i > j:
                    if abs(hi - hj) <= 1 and abs(wi - wj) <= 1:
                        initial_graph_edges[ "%d,%d" % (i,j) ]  =  abs(img_array[hi,wi] - img_array[hj,wj])
                        MInt[ "%d,%d" % (i,j) ] = kay

        ###   INTERNAL DIFFERENCE property at the initial vertices in the graph
        ###   Internal Difference is defined as the max edge weight between the pixels in the pixel
        ###   blob represented by a graph vertex.
        Int_prop = {v : 0.0 for v in initial_graph_vertices}
        ###   MInt_prop at each vertex is the Int_prop plus the kay divided by the cardinality of the blob
        MInt_prop = {v : kay for v in initial_graph_vertices}   
        if self.debug:
            print("\n\n\ninitial graph_vertices: %s" % str(sorted(initial_graph_vertices.items())))
            print("\n\n\nnumber of vertices in initial graph: %d" % len(initial_graph_vertices))
            print("\n\n\ninitial graph_edges: %s" % str(sorted(initial_graph_edges.items())))
            print("\n\n\nnumber of edges in initial graph: %d" % len(initial_graph_edges))
            print("\n\n\ninitial MInt: %s" % str(sorted(MInt.items())))
            print("\n\n\nnumber of edges in initial MInt: %d" % len(MInt))

        initial_graph = (copy.deepcopy(initial_graph_vertices), copy.deepcopy(initial_graph_edges))

        def find_all_connections_for_a_vertex(vert, graph):
            vertices = graph[0]
            edges    = graph[1]
            print("pixels in vertex %d: %s" % (vert, str(vertices[vert])))
            connected_verts_in_graph = []
            for edge in edges:
                end1,end2 = int(edge[:edge.find(',')]), int(edge[edge.find(',')+1 :])                 
                if vert == end1:
                    connected_verts_in_graph.append(end2)
                elif vert == end2:
                    connected_verts_in_graph.append(end1)
            return connected_verts_in_graph

        index_for_new_vertex = len(initial_graph_vertices)
        master_iteration_index = 0
        self.iterations_terminated = False

        ###   graph = (V,E) with both V and E as dictionaries.
        ###   NOTE: The edges E in the graph stand for 'Dif(C1,C2)' in F&H
        def seg_gen( graph, MInt, index_for_new_vertex, master_iteration_index, Int_prop, MInt_prop, kay ):
            print("\n\n\n=========================== Starting iteration %d ========================== \n\n\n" % master_iteration_index)
            V,E = graph
            if self.debug:
                print("\n\n\nV: %s" % str(V))
                print("\n\n\nE: %s" % str(E))
                print("\n\n\nMInt: %s" % str(MInt))
            max_iterations = self.max_iterations
            print("\n\n\nNumber of region proposals at the current level of merging: %d" % len(V))
            if len(E) == 0:
                print("\n\n\nThe graph has no edges left")
                return graph
            sorted_vals_and_edges = sorted( (v,k) for k,v in E.iteritems() )
            sorted_edges = [x[1] for x in sorted_vals_and_edges]
            print("\n\n\n[Iter Index: %d] Dissiminarity value associated with the most similar edge: %s" % (master_iteration_index, str(sorted_vals_and_edges[0])))
            """    
            if sorted_vals_and_edges[0][0] > 0.5:
                print("\n\n\nIterations terminated at iteration index: %d" % master_iteration_index)
                self.iterations_terminated = True
                return graph
            """
#            change_flag = False
            print("\nOne dot represents TEN possible merge operations in the graph representation of the image\n")
            if self.debug:
                print("\n\n\nBefore entering the edge loop --- sorted_edges: %s" % str(sorted_edges))
                print("\n\n\nBefore entering the edge loop --- E: %s" % str(E))
                print("\n\n\nBefore entering the edge loop --- MInt: %s" % str(MInt))
                print("\n\n\nBefore entering the edge loop --- vertices: %s" % str(V))
            edge_counter = 0
            for edge in sorted_edges:
                if edge not in E: continue
                edge_counter += 1
                if edge_counter % 10 == 0: 
                    sys.stdout.write(". ") 
                    sys.stdout.flush()
                if edge not in MInt:
                    sys.exit("MInt does not have an entry for %s" % edge)
                if edge not in E:
                    sys.exit("\n\n\nE does not have an entry for %s" % edge)
                if E[edge] >  MInt[edge]: 
                    del E[edge]
                    del MInt[edge]
                    continue 
                vert1,vert2 = int(edge[:edge.find(',')]), int(edge[edge.find(',')+1 :])
                if self.debug:
                    print("\n\n\n[Iter Index: %d] The least disimilar two vertices in the graph are: %s and %s" % (master_iteration_index, vert1, vert2))
                ###   Since we want to go through all the edges in 'sorted_edges" WHILE we are
                ###   deleting the vertices that are merged and the edges that are no longer
                ###   relevant because of vertex deletion, we need to be careful foing forward:
                if (vert1 not in V) or (vert2 not in V): continue
                affected_edges = []
                for edg in E:
                    end1,end2 = int(edg[:edg.find(',')]), int(edg[edg.find(',')+1 :])                
                    if (vert1 == end1) or (vert1 == end2) or (vert2 == end1) or (vert2 == end2):
                        affected_edges.append(edg)
                if self.debug:
                    print("\n\n\naffected edges to be deleted: %s" % str(affected_edges))
                for edg in affected_edges:
                    del E[edg]
                    del MInt[edg]
                merged_blob = V[vert1] + V[vert2]
#                change_flag = True
                if self.debug:
                    print("\n\n\nAdded vertex %d to V" % index_for_new_vertex)
                V[index_for_new_vertex] = merged_blob
                if self.debug:
                    print("\n\n\n[Iter Index: %d] index for new vertex: %d   and the merged blob: %s" % (master_iteration_index, index_for_new_vertex, str(merged_blob)))
                ###   We will now calculate the Int (Internal Difference) and MInt property to be
                ###   to be associated with the newly created vertex in the graph:
                within_blob_edge_weights = []
                for u1 in merged_blob:
                    i = u1[0] * arr_width + u1[1]
                    for u2 in merged_blob:
                        j = u2[0] * arr_width + u2[1]
                        if i > j:
                            ij_key = "%d,%d" % (i,j)
                            if ij_key in initial_graph_edges:
                                within_blob_edge_weights.append( initial_graph_edges[ ij_key ] )
                Int_prop[index_for_new_vertex] = max(within_blob_edge_weights) 
                MInt_prop[index_for_new_vertex] = Int_prop[index_for_new_vertex] + kay / float(len(merged_blob))
                ###   Now we must calculate the new graph edges formed by the connections between the newly
                ###   formed node and all other nodes.  However, we first must delete the two nodes that
                ###   we just merged:
                del V[vert1] 
                del V[vert2]
                del Int_prop[vert1]
                del Int_prop[vert2]
                del MInt_prop[vert1]
                del MInt_prop[vert2]
                if self.debug:
                    print("\n\n\nThe modified vertices: %s" % str(V))
                for v in sorted(V):
                    if v == index_for_new_vertex: continue
                    ###   we need to store the edge weights for the pixel-to-pixel edges
                    ###   in the initial graph with one pixel in the newly constructed
                    ###   blob and other in a target blob
                    pixels_in_v = V[v]
                    for u_pixel in merged_blob:
                        i = u_pixel[0] * arr_width + u_pixel[1]
                        inter_blob_edge_weights = []
                        for v_pixel in pixels_in_v:
                            j = v_pixel[0] * arr_width + v_pixel[1]
                            if i > j: 
                                ij_key = "%d,%d" % (i,j)
                            else:
                                ij_key = "%d,%d" % (j,i)
                            if ij_key in initial_graph_edges:
                                inter_blob_edge_weights.append( initial_graph_edges[ij_key ] )
                        if len(inter_blob_edge_weights) > 0:
                            uv_key = "%d,%d" % (index_for_new_vertex,v)
                            E[uv_key] = min(inter_blob_edge_weights)                        
                            MInt[uv_key] = min( MInt_prop[index_for_new_vertex], MInt_prop[v] )
#                            MInt[uv_key] = min( Int_prop[index_for_new_vertex] + kay/float(len(merged_blob)), Int_prop[v]/float(len(V[v])) )
                if self.debug:
                    print("\n\n\nAt the bottom of for-loop for edges ---   E: %s" % str(E))
                    print("\n\nMInt: %s" % str(MInt))
                index_for_new_vertex = index_for_new_vertex + 1   
#                if change_flag is False: break
            new_graph = (copy.deepcopy(V), copy.deepcopy(E))
            MInt = copy.deepcopy(MInt)
            if self.debug:
                print("\n\n\nnew graph at end of iteration: %s" % str(new_graph))
            if master_iteration_index == max_iterations:
                return new_graph
            else:
                self.iterations_used = master_iteration_index - 1
                master_iteration_index += 1
                if self.iterations_terminated:
                    return new_graph
                else:
                    return seg_gen(new_graph, MInt, index_for_new_vertex, master_iteration_index, Int_prop, MInt_prop, kay)  
        segmented_graph = seg_gen(initial_graph, MInt, index_for_new_vertex, master_iteration_index, Int_prop, MInt_prop, kay)
        if self.debug:
            print("\n\n\nsegmented_graph: %s" % str(segmented_graph))
        bounding_boxes = {}
        total_pixels_in_output = 0
        for vertex in sorted(segmented_graph[0]):
            all_pixels_in_blob = segmented_graph[0][vertex]
            total_pixels_in_output += len(all_pixels_in_blob)
            if len(all_pixels_in_blob) > 1:
                print("\n\n\npixels in blob indexed %d: %s" % (vertex, str(segmented_graph[0][vertex])))
                height_coords = [p[0] for p in all_pixels_in_blob]
                width_coords  = [p[1] for p in all_pixels_in_blob]
                bb_height_min = min(height_coords)
                bb_height_max = max(height_coords)
                bb_width_min  = min(width_coords)
                bb_width_max  = max(width_coords)
                """
                if (abs(bb_width_max - bb_width_min) <= 2 or abs(bb_height_max - bb_height_min) <= 2): continue
                if abs(bb_width_max - bb_width_min) < 0.1 * abs(bb_height_max - bb_height_min): continue
                if abs(bb_height_max - bb_height_min)  <  0.1 * abs(bb_width_max - bb_width_min): continue
                """
                bounding_boxes[vertex] = [bb_height_min, bb_width_min, bb_height_max, bb_width_max]

        print("\n\n\nTotal number of pixels in output blobs: %d" % total_pixels_in_output)
        title = "graph_based_bounding_boxes"
        mw = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_w = int(0.5 * screen_width)
            winsize_h = int(winsize_w * (arr_height * 1.0 / arr_width))            
        else:
            winsize_h = int(0.5 * screen_height)
            winsize_w = int(winsize_h * (arr_width * 1.0 / arr_height))
        scaled_image =  image_pil.copy().resize((winsize_w,winsize_h), Image.ANTIALIAS)
        mw.title(title) 
        mw.configure( height = winsize_h, width = winsize_x )         
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_h,            
                             width = winsize_w,             
                             cursor = "crosshair" )   
        canvas.pack(fill=BOTH, expand=True)
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = title + ".eps") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        photo = ImageTk.PhotoImage( scaled_image )
        canvas.create_image(winsize_w//2,winsize_h//2,image=photo)
        scale_w = winsize_w / float(arr_width)
        scale_h = winsize_h / float(arr_height)
        for v in bounding_boxes:
            bb = bounding_boxes[v]
            print("\n\n\nFor region proposal with ID %d, the bounding box is: %s" % (v, str(bb)))
            canvas.create_rectangle( (bb[1]*scale_w,bb[0]*scale_h,(bb[3]+1)*scale_w,(bb[2]+1)*scale_h), width='3', outline='red' )
        canvas.update()
        mw.update()
        print("\n\n\nIterations used: %d" % self.iterations_used)
        print("\n\n\nNumber of region proposals: %d" % len(bounding_boxes))
        mw.mainloop()
        if os.path.isfile(title + ".eps"):
            Image.open(title + ".eps").save(title + ".png")
            os.remove(title + ".eps")
        return segmented_graph[0]


    def extract_image_region_interactively_by_dragging_mouse(self, image_name):
        '''
        This is one method you can use to apply selective search algorithm to just a
        portion of your image.  This method extract the portion you want.  You click
        at the upper left corner of the rectangular portion of the image you are
        interested in and you then drag the mouse pointer to the lower right corner.
        Make sure that you click on "save" and "exit" after you have delineated the
        area.
        '''
        global delineator_image      ### global so that methods like _on_mouse_motion etc can access it
        global delineator_polygon    ###                  """
        print("Drag the mouse pointer to delineate the portion of the image you want to extract:")
        RegionProposalGenerator.image_portion_delineation_coords = []
        pil_image = Image.open(image_name).convert("L")
        RegionProposalGenerator.image_type = "L"
        image_portion_delineation_coords = []
        mw = Tkinter.Tk() 
        mw.title("Click and then drag the mouse pointer --- THEN CLICK SAVE and EXIT")
        width,height = pil_image.size

        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        display_pil_image = pil_image.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        scale_w = width / float(winsize_x)
        scale_h = height / float(winsize_y)
        delineator_image =  display_pil_image.copy()
        extracted_image =  display_pil_image.copy()
        self.extracted_image_portion_file_name = os.path.basename(image_name)
        mw.configure(height = winsize_y, width = winsize_x) 
        photo_image = ImageTk.PhotoImage(display_pil_image)
        canvasM = Tkinter.Canvas( mw,   
                                  width = winsize_x,
                                  height =  winsize_y,
                                  cursor = "crosshair" )  
        canvasM.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                        command = lambda: RegionProposalGenerator.extracted_image.save(self.extracted_image_portion_file_name) 
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: mw.destroy()
                      ).pack( side = 'right' )  
        canvasM.bind("<ButtonPress-1>", lambda e: self._start_mouse_motion(e, delineator_image))
        canvasM.bind("<ButtonRelease-1>", lambda e:self._stop_mouse_motion(e, delineator_image))
        canvasM.bind("<B1-Motion>", lambda e: self._on_mouse_motion(e, delineator_image))
        canvasM.create_image( 0,0, anchor=NW, image=photo_image)
        canvasM.pack(fill=BOTH, expand=1)
        mw.mainloop()       
        self.displayImage3(RegionProposalGenerator.extracted_image, "extracted image -- close window when done viewing")
        extracted_image = RegionProposalGenerator.extracted_image
        width_ex, height_ex = extracted_image.size
        extracted_image = extracted_image.resize( (int(width_ex * scale_w), int(height_ex * scale_h)), Image.ANTIALIAS )
        self.displayImage6(extracted_image, "extracted image")
        return extracted_image


    def extract_image_region_interactively_through_mouse_clicks(self, image_file):
        '''
        This method allows a user to use a sequence of mouse clicks in order to specify a
        region of the input image that should be subject to furhter processing.  The
        mouse clicks taken together define a polygon. The method encloses the
        polygonal region by a minimum bounding rectangle, which then becomes the new
        input image for the rest of processing.
        '''
        global delineator_image
        global delineator_coordinates
        print("Click mouse in a clockwise fashion to specify the portion you want to extract:")
        RegionProposalGenerator.image_portion_delineation_coords = []

        if os.path.isfile(image_file):
            pil_image = Image.open(image_file).convert("L")
        else:
            sys.exit("the image file %s does not exist --- aborting" % image_file)
        RegionProposalGenerator.image_type = "L"
        mw = Tkinter.Tk() 
        mw.title("Place mouse clicks clockwise --- THEN CLICK SAVE and EXIT")
        width,height = pil_image.size
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        display_pil_image = pil_image.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        scale_w = width / float(winsize_x)
        scale_h = height / float(winsize_y)
        delineator_image =  display_pil_image.copy()
        extracted_image =  display_pil_image.copy()
        self.extracted_image_portion_file_name = "image_portion_of_" + image_file
        mw.configure(height = winsize_y, width = winsize_x) 
        photo_image = ImageTk.PhotoImage(display_pil_image)
        canvasM = Tkinter.Canvas( mw,   
                                  width = width,
                                  height =  height,
                                  cursor = "crosshair" )  
        canvasM.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                         command = RegionProposalGenerator._extract_and_save_image_portion_polygonal
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: mw.destroy()
                      ).pack( side = 'right' )  
        canvasM.bind("<Button-1>", lambda e: self._image_portion_delineator(e, delineator_image))
        canvasM.create_image( 0,0, anchor=NW, image=photo_image)
        canvasM.pack(fill=BOTH, expand=1)
        mw.mainloop()       
        self.displayImage3(RegionProposalGenerator.extracted_image, "extracted image -- close window when done viewing")
        extracted_image = RegionProposalGenerator.extracted_image
        width_ex, height_ex = extracted_image.size
        extracted_image = extracted_image.resize( (int(width_ex * scale_w), int(height_ex * scale_h)), Image.ANTIALIAS )
        self.displayImage6(extracted_image, "extracted image")
        return extracted_image


    def extract_rectangular_masked_segment_of_image(self, horiz_start, horiz_end, vert_start, vert_end):
        '''
        Keep in mind the following convention used in the PIL's Image class: the first
        coordinate in the args supplied to the getpixel() and putpixel() methods is for
        the horizontal axis (the x-axis, if you will) and the second coordinate for the
        vertical axis (the y-axis).  On the other hand, in the args supplied to the
        array and matrix processing functions, the first coordinate is for the row
        index (meaning the vertical) and the second coordinate for the column index
        (meaning the horizontal).  In what follows, I use the index 'i' with its
        positive direction going down for the vertical coordinate and the index 'j'
        with its positive direction going to the right as the horizontal coordinate. 
        The origin is at the upper left corner of the image.
        '''
        masked_image = self.original_im.copy()
        width,height = masked_image.size 
        mask_array = np.zeros((height, width), dtype="float")
        for i in range(0, height):
            for j in range(0, width):
                if (vert_start < i < vert_end) and (horiz_start < j < horiz_end):
                    mask_array[(i,j)] = 1
        self._display_and_save_array_as_image( mask_array, "_mask__" )
        for i in range(0, height):
            for j in range(0, width):
                if mask_array[(i,j)] == 0:
                    masked_image.putpixel((j,i), (0,0,0)) 
        self.displayImage3(masked_image, "a segment of the image")

    def displayImage(self, argimage, title=""):
        '''
        Displays the argument image.  The display stays on for the number of seconds
        that is the first argument in the call to tk.after() divided by 1000.
        '''
        width,height = argimage.size
        winsize_x,winsize_y = width,height
        if width > height:
            winsize_x = 600
            winsize_y = int(600.0 * (height * 1.0 / width))
        else:
            winsize_y = 600
            winsize_x = int(600.0 * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk = Tkinter.Tk()
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.after(1000, self._callback, tk)    # display will stay on for just one second
        tk.mainloop()

    def displayImage2(self, argimage, title=""):
        '''
        Displays the argument image.  The display stays on until the user closes the
        window.  If you want a display that automatically shuts off after a certain
        number of seconds, use the previous method displayImage().
        '''
        width,height = argimage.size
        winsize_x,winsize_y = width,height
        if width > height:
            winsize_x = 600
            winsize_y = int(600.0 * (height * 1.0 / width))
        else:
            winsize_y = 600
            winsize_x = int(600.0 * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk = Tkinter.Tk()
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.mainloop()

    def displayImage3(self, argimage, title=""):
        '''
        Displays the argument image (which must be of type Image) in its actual size.  The 
        display stays on until the user closes the window.  If you want a display that 
        automatically shuts off after a certain number of seconds, use the method 
        displayImage().
        '''
        width,height = argimage.size
        tk = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = tk.winfo_screenwidth(),tk.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.mainloop()

    def displayImage4(self, argimage, title=""):
        '''
        Displays the argument image (which must be of type Image) in its actual size without 
        imposing the constraint that the larger dimension of the image be at most half the 
        corresponding screen dimension.
        '''
        width,height = argimage.size
        tk = Tkinter.Tk()
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( argimage )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.mainloop()

    def displayImage5(self, argimage, title=""):
        '''
        This does the same thing as displayImage4() except that it also provides for
        "save" and "exit" buttons.  This method displays the argument image with more 
        liberal sizing constraints than the previous methods.  This method is 
        recommended for showing a composite of all the segmented objects, with each
        object displayed separately.  Note that 'argimage' must be of type Image.
        '''
        width,height = argimage.size
        winsize_x,winsize_y = None,None
        mw = Tkinter.Tk()
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.8 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.8 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        mw.configure(height = winsize_y, width = winsize_x)         
        mw.title(title)   
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,
                             width = winsize_x,
                             cursor = "crosshair" )   
        canvas.pack( side = 'top' )                               
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = title + ".eps") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        photo = ImageTk.PhotoImage(argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS))
        canvas.create_image(winsize_x/2,winsize_y/2,image=photo)
        mw.mainloop()
        if os.path.isfile(title + ".eps"):
            Image.open(title + ".eps").save(title + ".png")
            os.remove(title + ".eps")

    def displayImage6(self, argimage, title=""):
        '''
        For the argimge which must be of type PIL.Image, this does the same thing as
        displayImage3() except that it also provides for "save" and "exit" buttons.
        '''
        width,height = argimage.size
        mw = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title(title)   
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,
                             width = winsize_x,
                             cursor = "crosshair" )   
        canvas.pack( side = 'top' )                               
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = title + ".eps") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        photo = ImageTk.PhotoImage(argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS))
        canvas.create_image(winsize_x/2,winsize_y/2,image=photo)
        mw.mainloop()
        if os.path.isfile(title + ".eps"):
            Image.open(title + ".eps").save(title + ".png")
            os.remove(title + ".eps")

    # The destructor:
#    def __del__(self):                                     
#        try:
#            for filename in glob.glob('_region__*.jpg'): os.remove(filename)
#            for filename in glob.glob('_LoG__*.jpg'): os.remove(filename)
#        except: pass

    #__________________  Static Methods of the RegionProposalGenerator Class _____________________
    #
    #  These are needed for applying graph-based and selective-search based methods to
    #  to interactively extracted portions of an image

    @staticmethod    
    def _start_mouse_motion(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        RegionProposalGenerator.image_portion_delineation_coords.append((markX,markY))
        print("Button pressed at: x=%s  y=%s\n" % (markX, markY)) 
        canvasM.create_oval( markX-5, markY-5, markX+5, markY+5, outline="red", fill="green", width = 2 )  

    @staticmethod    
    def _stop_mouse_motion(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        RegionProposalGenerator.image_portion_delineation_coords.append((markX,markY))
        print("Button pressed at: x=%s  y=%s\n" % (markX, markY))
        points = RegionProposalGenerator.image_portion_delineation_coords
        canvasM.create_rectangle(points[0][0], points[0][1], points[-1][0], points[-1][1], outline="red", fill="green", width = 2 ) 
        RegionProposalGenerator.extracted_image = RegionProposalGenerator._extract_image_portion_rectangular()

    @staticmethod    
    def _on_mouse_motion(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        RegionProposalGenerator.image_portion_delineation_coords.append((markX,markY))
        points = RegionProposalGenerator.image_portion_delineation_coords
        canvasM.create_rectangle(points[0][0], points[0][1], points[-1][0], points[-1][1], outline="red", fill="green", width = 2 ) 

    @staticmethod    
    def _image_portion_delineator(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        RegionProposalGenerator.image_portion_delineation_coords.append((markX,markY))
        print("Button pressed at: x=%s  y=%s\n" % (markX, markY)) 
        canvasM.create_oval( markX-10, markY-10, markX+10, markY+10, outline="red", fill="green", width = 2 )  

    @staticmethod    
    def _extract_image_portion_rectangular():
        '''
        This extracts a rectangular region of the image as specified by dragging the mouse pointer
        from the upper left corner of the region to its lower right corner.  After extracting the
        region, it sets the 'original_im' and 'data_im' attributes of the RegionProposalGenerator
        instance to the region extracted.
        '''
        global delineator_image
        width,height = delineator_image.size
        polygon = RegionProposalGenerator.image_portion_delineation_coords
        extracted_width = polygon[-1][0] - polygon[0][0]
        extracted_height = polygon[-1][1] - polygon[0][1]
        extracted_image = Image.new(RegionProposalGenerator.image_type, (extracted_width,extracted_height), (0))
        for x in range(0, extracted_width):        
            for y in range(0, extracted_height):
                extracted_image.putpixel((x,y), delineator_image.getpixel((polygon[0][0]+x, polygon[0][1]+y)))
        return extracted_image

    @staticmethod    
    def _extract_and_save_image_portion_polygonal():
        '''
        This extracts a polygonal region of the image as specified by clicking the mouse in a clockwise
        direction.  After extracting the region, it sets the 'original_im' and 'data_im' attributes of 
        the RegionProposalGenerator instance to the minimum bounding rectangle portion of the original 
        image that encloses the polygonal --- with the pixels outside the polygonal area set to 0.
        '''
        global delineator_image
        width,height = delineator_image.size
        polygon = RegionProposalGenerator.image_portion_delineation_coords
        if len(polygon) <= 2:
            sys.exit("You need MORE THAN TWO mouse clicks (in a clockwise fashion) to extract a region --- aborting!")
        x_min,x_max = min([x for (x,y) in polygon]),max([x for (x,y) in polygon])
        y_min,y_max = min([y for (x,y) in polygon]),max([y for (x,y) in polygon]) 
        extracted_width = x_max - x_min
        extracted_height = y_max - y_min
        extracted_image = Image.new(RegionProposalGenerator.image_type, (extracted_width,extracted_height), (0))
        polygon = [(x - x_min, y - y_min) for (x,y) in polygon]
        for x in range(0, extracted_width):        
            for y in range(0, extracted_height):
                number_of_crossings = 0
                raster_line = (0,y,x,y)
                for l in range(0,len(polygon)-1):
                    line = (polygon[l][0],polygon[l][1],polygon[l+1][0],polygon[l+1][1])
                    if _line_intersection(raster_line, line):
                        number_of_crossings += 1
                last_line = (polygon[l+1][0],polygon[l+1][1],polygon[0][0],polygon[0][1])
                number_of_crossings += _line_intersection(raster_line, last_line)
                if number_of_crossings % 2 == 1:
                    extracted_image.putpixel((x,y), delineator_image.getpixel((x+x_min, y + y_min)))
        RegionProposalGenerator.extracted_image = extracted_image

#______________________  Private Methods of the RegionProposalGenerator Class  ________________

    def _callback(self,arg):                       ## needed in Test directory for flashing an
        arg.destroy()                              ##  image momentarily


#_________________________  End of RegionProposalGenerator Class Definition ___________________________



#______________________________    Test code follows    _________________________________

if __name__ == '__main__': 
    pass


