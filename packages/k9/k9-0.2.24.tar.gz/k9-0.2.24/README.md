# K9 - Experimental

Tested with: kubernetes v10.0.1

K9 is a helper library to simplify the automation of Kubernetes.  It is an experiment to find the simplest interface that can be useful for automating Kubenetes.  If you need to automate the deployment if your application and the setup of Kubernetes, this is a new and simple way to get that done.

## Why K9?

YAML and JSON configuration files have a gone a long way towards automating the creation of cloud environments. These are great for concisely describing configurations, but as our configurations get progressively more complex and elaborate, we need the ability to build logic into our automation. Tools based on YAML/JSON configuration files have limited ability to construct loops, variables, and if-statements.

As coders, it’s much easier to just code in a language that naturally supports these constructs to perform the automation tasks. This library is created for coders that have the responsibility of fully automating their cloud environments, specifically Kubernetes environments.

K9 is a Python 3 based facade over the Kubernetes API, and it’s intent is to present a simplified interface to automate Kubernetes activities.

In addition, we are putting emphasis on providing complete documentation with lots of example code so that hopefully, you can accomplish your tasks easily relying only on this documentation. If you find areas that don’t make sense or needs better elaboration, let us know.

## Design Approach
Our primary objective is to make automating deployments on Kubernetes as simple and easy as possible. We are taking both a minimalist and opinionated approach to achieve this:

1. Create the smallest API that can provide the most functionality. That means cutting out functions that are redundant or infrequently used - focusing on the 20% that gets 80% or more of what you need done.
1. Reduce the complexity and number of parameters that need to be passed in to perform a given function.
1. Provide complete documentation with examples.

## Getting Started

The complete documentation can be found here: http://k9.docs.simoncomputing.com/.  You can follow the links at the bottom left of each page to step through all the features.