# SCALEX: Single-cell integrative Analysis via latent Feature EXtraction 

## Installation  	
#### install from PyPI

    pip install scalex
    
#### install from GitHub

	git clone git://github.com/jsxlei/scalex.git
	cd scalex
	python setup.py install
    
scalex is implemented in [Pytorch](https://pytorch.org/) framework.  
Running scalex on CUDA is recommended if available.   
Installation only requires a few minutes.  

## Quick Start


### 1. Command line

    SCALEX.py --data_list data1 data2 --batch_categories batch1 batch2 
    
    data_list: data path of each batch of single-cell dataset
    batch_categories: name of each batch
    

#### Output
Output will be saved in the output folder including:
* **checkpoint**:  saved model to reproduce results cooperated with option --checkpoint or -c
* **adata.h5ad**:  preprocessed data and results including, latent, clustering and imputation
* **umap.png**:  UMAP visualization of latent representations of cells 
* **log.txt**:  log file of training process

     
#### Useful options  
* output folder for saveing results: [-o] or [--outdir] 
* filter rare genes, default 3: [--min_cell]
* filter low quality cells, default 600: [--min_gene]  
* select the number of highly variable genes, keep all genes with -1, default 2000: [--n_top_genes]
	
    
#### Help
Look for more usage of scalex

	SCALEX.py --help 
    
    
### 2. API function

    from scalex.function import SCALEX
    adata = SCALEX(data_list, batch_categories)
    
Function of parameters are similar to command line options.
Output is a Anndata object for further analysis with scanpy.
    
#### Tutorial
