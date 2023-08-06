Introduction
=============

KADMOS (Knowledge- and graph-based Agile Design with Multidisciplinary Optimization System) is a new software system which is currently being developed in the [AGILE](http://www.agile-project.eu/) innovation project. It aims at increasing the agility of aircraft design teams that perform multidisciplinary design optimization (MDO). By increased agility, an MDO-based development process is meant that better fits the iterative nature of performing aircraft design. KADMOS has been developed on the notion that performing MDO is analogous to performing music with a large symphonic orchestra, however, in the MDO domain a music notation system is missing, which prevents us from composing large, complex pieces. 

Repository Structure
====================

The repository is structured as follows:

- dist/

	 contains copies of all major distributions of KADMOS

- docs/

     contains the documentation

- examples/

     contains two example knowlegde bases and scripts
	 
- kadmos/

     - cmdows
	  
		 contains tools for interacting with CMDOWS files
	 
     - external

         contains mainly third party scripts used at various parts in the code

     - graph

         contains the main graph-based logic for KADMOS

     - utilities

         contains several helper functions

     - vistoms

         contains source files for the VISTOMS visualizations

- license.md

     contains the license

- readme.md

     contains this document


Credits
=======

KADMOS is currently being developed at [TU Delft](https://tudelft.nl) by [Imco van Gent](https://bitbucket.org/imcovangent/) as an open-source project. KADMOS can still be considered as an early beta and is subjected to change. Ideas and improvement suggestions are greatly appreciated!


Changelog
=========

## 0.9.9 (13/11/2019)

- Updated all code to work with NetworkX 2.4
- Several bug fixes

## 0.9.8 (18/10/2019)

- Changed variable node names to include all attributes (for OpenLEGO compatibility)
- Several bug fixes for Python 3 in combination with Windows

## 0.9.7 (27/02/2019)

- Bug fix in Python 3 compatibility of create_dsm method

## 0.9.6 (19/02/2019)

- Restructured process graphs
- Small bug fix in VISTOMS

## 0.9.5 (19/02/2019)

- Version skipped

## 0.9.4 (06/02/2019)

- Improved PDF compilation with pdflatex
- Small bug fix for Python 3 compatibility in XML merger

## 0.9.3 (05/02/2019)

- Added option for pdflatex path input to create_dsm method

## 0.9.2 (31/01/2019)

- KADMOS is now Python 3.7 compatible
- Bug fix in unconverged-MDA

## 0.9.1 (29/01/2019)

- Small updates for BLISS-2000 architecture
- Removed KeChainMixin
- Bug fixes for VISTOMS

## 0.9.0 (03/12/2018)

- Based on a new version of the Common MDO Workflow Schema (CMDOWS): 0.9
- Major update of VISTOMS, including interactive manipulation of graphs using KADMOS functions in the VISTOMS GUI.
- Several bug fixes and improvements

## 0.8.3 (23/10/2018)

- Several bug fixes and improvements
- Improvement and enhancements in static and interactive VISTOMS
- Additions for KE-chain integration

## 0.8.2 (31/05/2018)

- Several bug fixes and improvements
- Improvement and enhancements in interactive VISTOMS
- Detailed adjustments to further match KADMOS and CMDOWS 0.8
- Additions to the CMDOWS 0.8 schema (additional metadata on local execution, licensing, references)

## 0.8.1 (17/04/2018)

- Included first stable version of interactive VISTOMS
- Detailed adjustments to match KADMOS and CMDOWS 0.8

## 0.8.0 (29/03/2018)

- Matching KADMOS with CMDOWS 0.8
- Inclusion of distributed architectures CO and BLISS-2000
- Added SuperSonic Business Jet (SSBJ) example

## 0.7.7 (05/02/2017)

- Additional CMDOWS functions
- Bug fixes
- Pip install for latest KE-chain 2.7

## 0.7.6 (21/12/2017)

- Further matching of KADMOS with CMDOWS 0.7
- General improvements, enhancements and bug fixes
- Deprecated KnowledgeBase class and enhanced CMDOWS load to handle XML I/Os
- Improved MDAO Process Graph determination to account for data dependencies
- Extended CMDOWS file operations library
- Improved determination of function hierarchy
- Added function to automatically determine an optimal function order
- Updated all code to work with NetworkX 2.0

## 0.7 (08/09/2017)

- Matching KADMOS with CMDOWS 0.7
- General improvements and enhancements

## 0.6 

- Skipped

## 0.5 (31/05/17)

- First public release of KADMOS