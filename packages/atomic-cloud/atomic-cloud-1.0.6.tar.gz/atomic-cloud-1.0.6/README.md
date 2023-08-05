# Atomic Cloud

This is a Python Library intended to simplify interactions with different cloud environments. 

## AWS Design Approach

For AWS, we are using CloudFormation to define and build the various resources.  It is a convenient mechanism because we can then delete those resources conveniently by deleting
the stacks that were created with CloudFormation.  

The vast majority of this library will consist of querying what resources exist in AWS.  
It is just easier to do query, filter and extract data using Python rather than using the 
command line interface.

## Getting Started

The complete documentation can be found here: http://atomic-cloud.docs.simoncomputing.com/.  You can follow the links at the bottom left of each page to step through all the features.