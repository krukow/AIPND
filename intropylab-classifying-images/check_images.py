#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#
# PROGRAMMER: Karl Krukow
# DATE CREATED: July 24
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print 
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##
# Program Outline
# Repeat below for all three image classification algorithms (e.g. input algorithm as command line argument):
#
# Time your program
# Use Time Module to compute program runtime
# Get program Inputs from the user
# Use command line arguments to get user inputs
# Create Pet Images Labels
# Use the pet images filenames to create labels
# Store the pet image labels in a data structure (e.g. dictionary)
# Create Classifier Labels and Compare Labels
# Use the Classifier function classify the images and create the classifier labels
# Compare Classifier Labels to Pet Image Labels
# Store Pet Labels, Classifier Labels, and their comparison in a complex data structure (e.g. dictionary of lists)
# Classifying Labels as "Dogs" or "Not Dogs"
# Classify all Labels (Pet & Classifier) as "Dogs" or "Not Dogs" using dognames.txt file
# Store new classifications in the complex data structure (e.g. dictionary of lists)
# Calculate the Results
# Use Labels and their classifications to determine how well the algorithm worked on classifying images.
# Print the Results

# Imports python modules

import argparse
from time import time, sleep, strftime, gmtime
from os import listdir, extsep
from os.path import join


# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # collecting start time
    start_time = time()

    # line arguments
    in_arg = get_input_args()
    
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    answers_dic = get_pet_labels(in_arg.dir)

    # labels with the classifier function using in_arg.arch, comparing the
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)

    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, in_arg.dogfile)

    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(result_dic)

    # incorrect classifications of dogs and breeds if requested.
    print_results(result_dic, results_stats_dic, in_arg.arch, True, True)

    # by collecting end time
    end_time = time()

    # seconds & prints it in hh:mm:ss format
    tot_time = strftime("%H:%M:%S", gmtime(end_time - start_time))
    print("\n** Total Elapsed Runtime:", tot_time)



# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    parser = argparse.ArgumentParser(description="""
        Check images & report results: read them in, predict their
        content (classifier), compare prediction to actual value labels
        and output results
""")
    parser.add_argument('--dir',
                        default='pet_images/',
                        help='Path to the pet image files(default- pet_images/)')

    parser.add_argument('--arch',
                        default='vgg',
                        help="CNN model architecture to use for image classification(default- vgg)",
                        choices=['vgg', 'alexnet', 'resnet'])

    parser.add_argument('--dogfile',
                        default='dognames.txt',
                        help="Text file that contains all labels associated to dogs(default- 'dognames.txt')")

    return parser.parse_args()


def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """

    def to_labels(name):
        return ' '.join(filter(lambda x: x.isalpha(), name.lower().split("_")))

    return dict(map(lambda f: (join(image_dir,f),
                               to_labels(f.split(extsep)[0])),
                    listdir(image_dir)))


def classify_images(images_dir, petlabel_dic, model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """

    # note decided to not use images_dir but instead iterate over dict keys

    def match(label, classified_labels):
        terms = classified_labels.strip().lower().split(',')
        for term in terms:
            if (term.strip() == label) or len(term.split(label)) > 1:
                return 1
        return 0

    results_dic = {}
    for f, label in petlabel_dic.items():
        label = label.strip()
        classifier_res = classifier(f, model)
        results_dic[f] = [label, classifier_res, match(label, classifier_res)]

    return results_dic


def adjust_results4_isadog(results_dic, dogsfile):
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """
    all_dogs = set()
    with open(dogsfile) as f:
        name_lines = list(f)
        for name_line in name_lines:
            names = name_line.strip().split(',')
            all_dogs.update(names)

    for _, res in results_dic.items():
        label = res[0]
        classified = set(res[1].lower().split(','))
        if label in all_dogs:
            res.append(1)
        else:
            res.append(0)

        if all_dogs.isdisjoint(classified):
            res.append(0)
        else:
            res.append(1)


def calculates_results_stats(results_dic):
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    results_stats = dict()
    n_images = len(results_dic)
    n_dogs = 0
    n_dogs_classified = 0
    n_non_dogs_classified = 0
    n_correct_breed = 0
    n_label_matches = 0
    for _, res in results_dic.items():
        is_dog = res[3] == 1
        agree = res[3] == res[4]
        label_match = res[2] == 1
        if is_dog:
            n_dogs += 1
            if agree: n_dogs_classified += 1
            if label_match: n_correct_breed += 1
        else:
            if agree: n_non_dogs_classified += 1

        if label_match:
            n_label_matches += 1

    results_stats['n_images'] = n_images
    results_stats['n_dogs'] = n_dogs
    results_stats['n_dogs_classified'] = n_dogs_classified
    results_stats['n_non_dogs_classified'] = n_non_dogs_classified
    results_stats['n_correct_breed'] = n_correct_breed
    results_stats['n_label_matches'] = n_label_matches

    if n_dogs > 0:
        results_stats['pct_correct_dogs'] = (float(n_dogs_classified) / n_dogs) * 100
    else:
        results_stats['pct_correct_dogs'] = 0.0

    if n_images == n_dogs:
        results_stats['pct_correct_non_dogs'] = 0.0
    else:
        results_stats['pct_correct_non_dogs'] = float(n_non_dogs_classified) / (n_images - n_dogs) * 100

    results_stats['pct_correct_breed'] = float(n_correct_breed) / n_dogs

    results_stats['pct_label_matches'] = float(n_label_matches) / n_images

    return results_stats



def print_results(results_dic, results_stats, model, print_incorrect_dogs, print_incorrect_breed):
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    print("CNN model architecture: " + model)

    non_dogs = results_stats['n_images'] - results_stats['n_dogs']
    print("Number of images: " + str(results_stats['n_images']))
    print("Number of dogs: " + str(results_stats['n_dogs']))
    print("Number of non-dogs: " + str(non_dogs))

    for k,v in results_stats.items():
        if k.startswith('pct_'):
            print(k + ": " + str(v))

    if not (print_incorrect_dogs or print_incorrect_breed): return

    made_mistakes = (results_stats['n_dogs'] != results_stats['n_dogs_classified'] or non_dogs != results_stats['n_non_dogs_classified'])
    if made_mistakes: print("Mistakes where made!")
    if made_mistakes:
        for k, res in results_dic.items():
            is_dog = res[3] == 1
            agree = res[3] == res[4]
            label_match = res[2] == 1
            if not agree and print_incorrect_dogs:
                print("Incorrect! {} is {}. Full data: {}.".format(k, "dog" if is_dog else "not a dog!", res))
            if agree and not label_match and print_incorrect_breed:
                print("Incorrect breed! {} is {} not {}. Full data: {}.".format(k, res[0], res[1], res))

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()
