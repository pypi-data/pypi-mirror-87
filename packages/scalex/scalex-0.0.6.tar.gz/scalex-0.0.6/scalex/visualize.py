#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Thu 16 Jul 2020 07:24:49 PM CST

# File Name: plot.py
# Description:

"""
import numpy as np
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns


def plot_batch(adata, by='batch', name='celltype', color_map=None, batches=None, condition=None, savefig=None, 
               legend_loc='right margin', legend_fontsize=None, legend_fontweight='bold'):
    
#     celltype_colors = dict(zip(result.obs['celltype'].cat.categories, result.uns['celltype_colors']))
#     color_map = [celltype_colors[i] for i in subset.obs['celltype'].cat.categories]
    if batches is None:
        batches = adata.obs[by].cat.categories
    for b in batches:
        adata.obs['tmp'] = adata.obs[name].astype(str)
        if condition is not None:
            adata.obs['tmp'][~adata.obs[condition[0]].isin(condition[1])] = ''
        adata.obs['tmp'][adata.obs[by]!=b] = ''
        adata.obs['tmp'] = adata.obs['tmp'].astype('category')
        if condition is not None:
            groups = list(adata[(adata.obs[by]==b) & (adata.obs[condition[0]].isin(condition[1]))].obs[name].astype('category').cat.categories.values)
        else:
            groups = list(adata[adata.obs[by]==b].obs[name].astype('category').cat.categories.values)
        if color_map is not None:
            palette = [color_map[i] if i in color_map else 'gray' for i in adata.obs['tmp'].cat.categories]
        else:
            palette = None
        size = min(40, 120000/len(adata[adata.obs[by]==b]))
        sc.pl.umap(adata, color='tmp', groups=groups, title=b, palette=palette, size=size, 
                   legend_loc=legend_loc, legend_fontsize=legend_fontsize, legend_fontweight=legend_fontweight)
        del adata.obs['tmp']
        
            
            
def plot_umap(adata, color='celltype', color_map=None, cond1='batch', range1=None, cond2=None, v2=None, save=None, 
               legend_loc='right margin', legend_fontsize=None, legend_fontweight='bold', sep='_', basis='umap'):
    
#     celltype_colors = dict(zip(result.obs['celltype'].cat.categories, result.uns['celltype_colors']))
#     color_map = [celltype_colors[i] for i in subset.obs['celltype'].cat.categories]
    if range1 is None:
        range1 = adata.obs[cond1].cat.categories
    for b in range1:
        adata.obs['tmp'] = adata.obs[color].astype(str)
        adata.obs['tmp'][adata.obs[cond1]!=b] = ''
        if cond2 is not None:
            adata.obs['tmp'][adata.obs[cond2]!=v2] = ''
            groups = list(adata[(adata.obs[cond1]==b) & 
                                (adata.obs[cond2]==v2)].obs[color].astype('category').cat.categories.values)
            size = min(10, 120000/len(adata[(adata.obs[cond1]==b) & (adata.obs[cond2]==v2)]))
            size = size
        else:
            groups = list(adata[adata.obs[cond1]==b].obs[color].astype('category').cat.categories.values)
            size = min(10, 120000/len(adata[adata.obs[cond1]==b]))
        adata.obs['tmp'] = adata.obs['tmp'].astype('category')
        if color_map is not None:
            palette = [color_map[i] if i in color_map else 'gray' for i in adata.obs['tmp'].cat.categories]
        else:
            palette = None

        title = b if cond2 is None else v2+sep+b
        if save is not None:
            save_ = '_'+b+save
        else:
            save_ = None
        if basis == 'umap':
            sc.pl.umap(adata, color='tmp', groups=groups, title=title, palette=palette, size=size, save=save_,
                   legend_loc=legend_loc, legend_fontsize=legend_fontsize, legend_fontweight=legend_fontweight)
        elif basis == 'diffmap':
            sc.pl.diffmap(adata, color='tmp', groups=groups, title=title, palette=palette, size=size, save=save_,
                   legend_loc=legend_loc, legend_fontsize=legend_fontsize, legend_fontweight=legend_fontweight)
        del adata.obs['tmp']

            
            
def plot_legend(color_map, savefig=None, figsize=(0.1, 0.1), ncol=7, title=''):
    import matplotlib.patches as mpatches
    plt.figure(figsize=figsize)
    legend_TN = [mpatches.Patch(color=color, label=c) for c,color in color_map.items()]
    plt.legend(handles=legend_TN, ncol=ncol, frameon=False, title=title) 
    plt.axis('off')
    if savefig:
        plt.savefig(savefig, bbox_inches='tight')
    else:
        plt.show()
        

def plot_meta2(adata, use_rep='latent', var='celltype', batch='batch', color_map=None, figsize=(10, 10), cmap='Blues',
              batches=None, annot=False, savefig=None, cbar=True, keep=False):
    """
    input: AnnData
    """
    meta = []
    name = []
#     if colors is None:
#         colors = ['red', 'royalblue', 'lawngreen', 'orange', 'gold',  'lightseagreen', 'blueviolet', 'black']
#     adata.obs[var] = adata.obs[var].astype('category')
    if batches is None:
        batches = np.unique(adata.obs[batch]);#print(batches)

    for i,b in enumerate(batches):
        for cat in adata.obs[var].cat.categories:
            index = np.where((adata.obs[var]==cat) & (adata.obs[batch]==b))[0]
            if len(index) > 0:
                if use_rep and use_rep in adata.obsm:
                    meta.append(adata.obsm[use_rep][index].mean(0))
                elif use_rep and use_rep in adata.layers:
                    meta.append(adata.layers[use_rep][index].mean(0))
                else:
                    meta.append(adata.X[index].mean(0))

                name.append(cat)
    
    meta = np.stack(meta)

    plt.figure(figsize=figsize)
    corr = np.corrcoef(meta)
    
    xticklabels = adata[adata.obs[batch]==batches[0]].obs['celltype'].cat.categories
    yticklabels = adata[adata.obs[batch]==batches[1]].obs['celltype'].cat.categories
#     print(len(xticklabels), len(yticklabels))
    corr = corr[len(xticklabels):, :len(xticklabels)] #;print(corr.shape)
    if keep:
        categories = adata.obs['celltype'].cat.categories
        corr_ = np.zeros((len(categories), len(categories)))
        x_ind = [i for i,k in enumerate(categories) if k in xticklabels]
        y_ind = [i for i,k in enumerate(categories) if k in yticklabels]
        corr_[np.ix_(y_ind, x_ind)] = corr
        corr = corr_
#         xticklabels, yticklabels = categories, categories
        xticklabels, yticklabels = [], []
    grid = sns.heatmap(corr, xticklabels=xticklabels, yticklabels=yticklabels, annot=annot,
                cmap=cmap, square=True, cbar=cbar, vmin=0, vmax=1)

    if color_map is not None:
        [ tick.set_color(color_map[tick.get_text()]) for tick in grid.get_xticklabels() ]
        [ tick.set_color(color_map[tick.get_text()]) for tick in grid.get_yticklabels() ]
    plt.xticks(rotation=45, horizontalalignment='right', fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel(batches[0], fontsize=18)
    plt.ylabel(batches[1], fontsize=18)
    
#     rainbow_text(15, 1, batches, colors[:len(batches)], size=14)#, ax=grid)
#     plt.xlabel('\n'.join([b+' : '+colors[i] for i,b in enumerate(np.unique(adata.obs.batch))]))
    if savefig:
        plt.savefig(savefig, bbox_inches='tight')
    else:
        plt.show()
        

def plot_meta(adata, use_rep=None, var='celltype', batch='batch', colors=None, cmap='Blues', vmax=1, vmin=0, mask=True,
              annot=False, savefig=None):
    """
    input: AnnData
    """
    meta = []
    name = []
    color = []
#     colors = ['red', 'blue', 'green', 'orange', 'yellow', 'purple', 'black']
    if colors is None:
        colors = ['red', 'orange', 'gold', 'lawngreen', 'lightseagreen', 'royalblue', 'blueviolet', 'black']
    adata.obs[var] = adata.obs[var].astype('category')
    batches = np.unique(adata.obs[batch])
#     for i,b in enumerate(batches):
#         for cat in adata.obs[var].cat.categories:
    for cat in adata.obs[var].cat.categories:
        for i,b in enumerate(batches):
            index = np.where((adata.obs[var]==cat) & (adata.obs[batch]==b))[0]
            if len(index) > 0:
                if use_rep and use_rep in adata.obsm:
                    meta.append(adata.obsm[use_rep][index].mean(0))
                elif use_rep and use_rep in adata.layers:
                    meta.append(adata.layers[use_rep][index].mean(0))
                else:
                    meta.append(adata.X[index].mean(0))
#                 if len(np.unique(adata.obs.batch))>1:
#                     name.append(batch+'_'+celltype)
#                 else:
                name.append(cat)
                color.append(colors[i])
    
    
    meta = np.stack(meta)
    plt.figure(figsize=(10, 10))
    corr = np.corrcoef(meta)
    if mask:
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask, k=1)] = True
    grid = sns.heatmap(corr, mask=mask, xticklabels=name, yticklabels=name, annot=annot, # name -> []
                cmap=cmap, square=True, cbar=True, vmin=vmin, vmax=vmax)
    [ tick.set_color(c) for tick,c in zip(grid.get_xticklabels(),color) ]
    [ tick.set_color(c) for tick,c in zip(grid.get_yticklabels(),color) ]
    plt.xticks(rotation=45, horizontalalignment='right', fontsize=10)
    plt.yticks(fontsize=10)
#     rainbow_text(15, 1, batches, colors[:len(batches)], size=14)#, ax=grid)
#     plt.xlabel('\n'.join([b+' : '+colors[i] for i,b in enumerate(np.unique(adata.obs.batch))]))
    if savefig:
        plt.savefig(savefig, bbox_inches='tight')
    else:
        plt.show()
        
        
from sklearn.metrics import confusion_matrix
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, f1_score

def reassign_cluster_with_ref(Y_pred, Y):
    """
    Reassign cluster to reference labels
    Inputs:
        Y_pred: predict y classes
        Y: true y classes
    Return:
        f1_score: clustering f1 score
        y_pred: reassignment index predict y classes
        indices: classes assignment
    """
    def reassign_cluster(y_pred, index):
        y_ = np.zeros_like(y_pred)
        for i, j in index:
            y_[np.where(y_pred==i)] = j
        return y_
    from sklearn.utils.linear_assignment_ import linear_assignment
#     print(Y_pred.size, Y.size)
    assert Y_pred.size == Y.size
    D = max(Y_pred.max(), Y.max())+1
    w = np.zeros((D,D), dtype=np.int64)
    for i in range(Y_pred.size):
        w[Y_pred[i], Y[i]] += 1
    ind = linear_assignment(w.max() - w)

    return reassign_cluster(Y_pred, ind), ind


def plot_confusion(adata, savefig=None, cmap='Blues'):
    y, ind = reassign_cluster_with_ref(adata.obs['leiden'].cat.codes, adata.obs['celltype'].cat.codes) # ind[:, 0] leiden, ind[:, 1] cell type
    d = dict(zip(ind[:, 1], ind[:, 0]))
#     print(len(d), adata.obs['celltype'].cat.categories.shape, adata.obs['leiden'].cat.categories.shape)
#     print(dict(zip(ind[:, 0], adata.obs['celltype'].cat.categories[ind[:, 1]])))

    pred_class = []
#     print(d.keys())
    for i in range(len(d)):
        if str(d[i]) in adata.obs['leiden'].cat.categories:
#         if d[i] in range(len(adata.obs['leiden'].cat.categories)):
            pred_class.append(str(d[i]))
        else:
            pred_class.append('')

    cm = confusion_matrix(y, adata.obs['celltype'].cat.codes)
    f1 = f1_score(adata.obs['celltype'].cat.codes, y, average='micro')
    nmi = normalized_mutual_info_score(adata.obs['celltype'].cat.codes, y)
    ari = adjusted_rand_score(adata.obs['celltype'].cat.codes, y)
    
    cm = cm.astype('float') / cm.sum(axis=0)[np.newaxis, :]

    # plot_confusion_matrix(cm, adata.obs['celltype'].cat.categories, pred_class, 
    #                      figsize=(20, 20), normalize=True)
    plt.figure(figsize=(14, 14))
    sns.heatmap(cm, xticklabels=adata.obs['celltype'].cat.categories, yticklabels=pred_class,
                    cmap=cmap, square=True, cbar=False, vmin=0, vmax=1)

    plt.xticks(rotation=45, horizontalalignment='right') #, fontsize=14)
    plt.yticks(fontsize=14, rotation=0)
    plt.ylabel('Leiden cluster', fontsize=18)
    
    if savefig:
        plt.savefig(savefig, bbox_inches='tight')
    else:
        plt.show()
    
    return f1, nmi, ari
    