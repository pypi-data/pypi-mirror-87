# ProMS: protein marker selection using proteomics or multiomics data


## Installation

To install `proms`, run:

```console
$ pip install proms
```

or

```console
$ pip install git+https://github.com/bzhanglab/proms
```


## Introduction

We provide two methods for selecting protein markers. 

### ProMS: Protein marker selection with proteomics data alone

The algorithm `ProMS` (Protein Marker Selection) works as follows. 
As a first step to remove uninformative features, `ProMS` examines each feature 
individually to determine the strength of the relationship between the feature 
and the target variable. A symmetric auroc score <!-- $AUC_{sym}$ --> <img src="https://render.githubusercontent.com/render/math?math=AUC_%7Bsym%7D"> 
is defined to evaluate such strength: <!-- $AUC_{sym} = 2 \times |AUC - 0.5|$ --> <img src="https://render.githubusercontent.com/render/math?math=AUC_%7Bsym%7D%20%3D%202%20%5Ctimes%20%7CAUC%20-%200.5%7C">


`ProMS` only keeps the features with the top <!-- $\alpha\%$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Calpha%5C%25"> highest <!-- $AUC_{sym}$ --> <img src="https://render.githubusercontent.com/render/math?math=AUC_%7Bsym%7D"> 
scores. Here <!-- $\alpha$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Calpha"> is a hyperparameter that needs to be tuned jointly 
with other hyperparameters of the final classifier. After the filtering step, data 
matrix <!-- $\mathbf{D}$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Cmathbf%7BD%7D"> is 
reduced to <!-- $\mathbf{D'}$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Cmathbf%7BD'%7D"> of size <!-- $n\times p'$ --><img src="https://render.githubusercontent.com/render/math?math=n%5Ctimes%20p'"> where <!-- $p' \ll p$ --> <img src="https://render.githubusercontent.com/render/math?math=p'%20%5Cll%20p">. To further reduce the redundancy among the remaining features,
`ProMS` groups <!-- $p'$ --> <img src="https://render.githubusercontent.com/render/math?math=p'"> features into <!-- $k$ --> <img src="https://render.githubusercontent.com/render/math?math=k"> clusters with weighted k-medoids clustering in sample space. The whole process is illustrated in the following diagram:

<center><img src="https://github.com/bzhanglab/proms/blob/main/docs/proms.png" alt="proms" height="800"/></center>


### ProMS_mo: Protein marker selection with multi-omics data
We have <!-- $H$ --> <img src="https://render.githubusercontent.com/render/math?math=H"> data sources, <!-- $\mathbf{D}_1,...,\mathbf{D}_H$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Cmathbf%7BD%7D_1%2C...%2C%5Cmathbf%7BD%7D_H">, representing <!-- $H$ --> <img src="https://render.githubusercontent.com/render/math?math=H">
different types of omics measurements that jointly depicts the same set of
samples <!-- $s_1,...,s_n$ --> <img src="https://render.githubusercontent.com/render/math?math=s_1%2C...%2Cs_n">. <!-- $\mathbf{D}_i (i=1...H)$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Cmathbf%7BD%7D_i%20(i%3D1...H)"> is a matrix of size <!-- $n\times p_i$ --> <img src="https://render.githubusercontent.com/render/math?math=n%5Ctimes%20p_i">
where rows correspond to samples and columns correspond to features in <!-- $i$ --> <img src="https://render.githubusercontent.com/render/math?math=i">th
data source. Without the loss of generality, we use <!-- $\mathbf{D}_1$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Cmathbf%7BD%7D_1">
to represent the proteomics data from which we seek to select a set of informative 
markers that can be used to predict the target labels. Similar to `ProMS`, the first 
step of `ProMS_mo` involves filtering out insignificant features from each data source 
separately. Again we use <!-- $AUC_{sym}$ --> <img src="https://render.githubusercontent.com/render/math?math=AUC_%7Bsym%7D"> as the scoring metric. `ProMS_mo` first applies the univariate filtering to target data source <!-- $\mathbf{D}_1$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Cmathbf%7BD%7D_1">
and keeps only the top <!-- $\alpha\%$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Calpha%5C%25">
 features with the highest scores. We denote the minimal score among these remaining 
 features as <!-- $\theta$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Ctheta">. For other data source, `ProMS_mo` only keeps those features 
 with score larger than <!-- $\theta$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Ctheta">. Filtered data matrices are combined into a new 
 matrix <!-- $\mathbf{D}'$ --> <img src="https://render.githubusercontent.com/render/math?math=%5Cmathbf%7BD%7D'"> of size <!-- $n\times p'$ --> <img src="https://render.githubusercontent.com/render/math?math=n%5Ctimes%20p'">, where <!-- $p' = \sum_{i=1}^{H}p'_{i}$ --> <img src="https://render.githubusercontent.com/render/math?math=p'%20%3D%20%5Csum_%7Bi%3D1%7D%5E%7BH%7Dp'_%7Bi%7D">
 and <!-- $p'_i$ --> <img src="https://render.githubusercontent.com/render/math?math=p'_i"> is the number of features in the filtered data source <!-- $i$ --> <img src="https://render.githubusercontent.com/render/math?math=i">. Finally, 
 weighted k-medoids clustering is performed to partition the <!-- $p'$ --> <img src="https://render.githubusercontent.com/render/math?math=p'"> features into <!-- $k$ --> <img src="https://render.githubusercontent.com/render/math?math=k">
 clusters in sample spaces. To guarantee that only protein markers are selected as 
 medoids, `ProMS_mo` first initializes the <!-- $k$ --> <img src="https://render.githubusercontent.com/render/math?math=k">
 medoids to protein markers. During the iterative steps of optimization, 
 a medoid can only be replaced by another protein marker if such exchange improves the 
 objective function. After the iterative process converges, <!-- $k$ --> <img src="https://render.githubusercontent.com/render/math?math=k">
 medoids are selected as the final protein markers for constructing a classifier.
The steps are depicted in the following diagram:

<center><img src="https://github.com/bzhanglab/proms/blob/main/docs/proms_mo.png" alt="proms" height="800"/></center>

## How to use the package

* Run training:

```console
proms_train -f run_config.json -d crc.json 2>proms.log
```

example run configuration file (`run_config.json`):

```json
{
  "repeat": 10,
  "k": [2, 5, 10, 15],
  "classifiers": ["logreg", "rf", "svm", "xgboost"],
  "percentile": [5, 10, 15],
  "n_jobs": 20
}
```


example data configuration file (`crc.json`):

```json
{
  "name": "crc",
  "data_root": "crc",
  "train_dataset": "train",
  "test_dataset": "test",
  "target_view": "pro",
  "target_label": "msi",
  "data": {
    "train": {
      "label": {
        "file": "clinical_data.tsv"
      },
      "view": [
        {
          "type": "mrna",
          "file": "Colon_rna_fpkm.tsv"
        },
        {
          "type": "pro",
          "file": "Colon_pro_spc.tsv"
        }
      ]
    },
    "test": {
      "label": {
        "file": "clinical_data.tsv"
      },
      "view": [
        {
          "type": "mrna",
          "file": "Colon_rna_fpkm.tsv"
        },
        {
          "type": "pro",
          "file": "Colon_pro_spc_2.tsv"
        }
      ]
    }
  }
}
```




* Run prediction:
```console
proms_predict -m /path/to/full_model.pkl -d crc_predict.json
```

Example data configuration for prediction (`crc_predict.json`):

```json
{
  "name": "crc",
  "data_root": "crc",
  "predict_dataset": "predict",
  "data": {
    "predict": {
      "view": [
        {
          "type": "mrna",
          "file": "Colon_rna_fpkm.tsv"
        },
        {
          "type": "pro",
          "file": "Colon_pro_spc.tsv"
        }
      ]
    }
  }
}
```

