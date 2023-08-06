"""Functions for visualizing models and designs"""

import matplotlib
from matplotlib import pyplot as plt
import numpy as np

def data_histogram(y_labels,y_values,title='',xlabel='',ylabel='',show=False,close_fig=True,output_file=None,figsize=[4.5,3.]):
    fig = plt.figure(figsize=figsize)
    histdata = {}
    for y_label,y_vals in zip(y_labels,y_values):
        #n_bins = round(len(y_vals)/5)
        #while n_bins > 100:
        #    n_bins = round(n_bins/5)
        #counts, bin_edges, _ = plt.hist(y_vals,alpha=0.6,bins=n_bins,label=y_label)
        counts, bin_edges, _ = plt.hist(y_vals,alpha=0.6,label=y_label)
        histdata[y_label] = {'bin_edges':bin_edges,'counts':counts}
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig, histdata

def data_histogram_dual_y(y_labels,y_values,title='',xlabel='',ylabel='',match_bins=False,show=False,close_fig=True,output_file=None,figsize=[4.5,3.]):
    fig = plt.figure(figsize=figsize)
    ax1 = fig.gca()
    ax2 = ax1.twinx()
    ax1.set_ylabel(ylabel+', '+y_labels[0])
    ax1.set_xlabel(xlabel)
    ax2.set_ylabel(ylabel+', '+y_labels[1])

    if match_bins:
        min1 = np.min(y_values[0])
        max1 = np.max(y_values[0])
        min2 = np.min(y_values[1])
        max2 = np.max(y_values[1])
        minmin = min([min1,min2])
        maxmax = max([max1,max2])
        counts1, bin_edges1, _ = ax1.hist(y_values[0],alpha=0.6,label=y_labels[0],bins=20,range=(minmin,maxmax))
        counts2, bin_edges2, _ = ax2.hist(y_values[1],alpha=0.6,label=y_labels[1],color='orange',bins=20,range=(minmin,maxmax))
    else:
        counts1, bin_edges1, _ = ax1.hist(y_values[0],alpha=0.6,label=y_labels[0])
        counts2, bin_edges2, _ = ax2.hist(y_values[1],alpha=0.6,label=y_labels[1],color='orange')

    #range1 = np.max(y_values[0])-np.min(y_values[0])
    #range2 = np.max(y_values[1])-np.min(y_values[1])
    #nbins1 = len(counts1)
    #nbins2 = max([int(2*nbins1*range2/range1),2])
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    histdata = {y_labels[0]:{'bin_edges':bin_edges1,'counts':counts1},\
                y_labels[1]:{'bin_edges':bin_edges2,'counts':counts2}}
    plt.title(title)
    #plt.xlabel(xlabel)
    #plt.ylabel(ylabel)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig, histdata

def data_plot(data,vlines={},title='',xlabel='',ylabel='',show=False,close_fig=True,output_file=None,figsize=[4.5,3.]):
    # data should be {'foo':{'x':[...] (opt),'y':[...] (req)}, 'bar':{...}, ...}
    fig = plt.figure(figsize=figsize)
    for lbl,xy in data.items():
        if 'x' in xy:
            x_vals = xy['x']
        else:
            x_vals = range(len(xy['y']))
        plt.plot(x_vals,xy['y'],label=lbl)
    #y_text = np.min(MAE)+0.9*(np.max(RMS)-np.min(MAE))
    for name,val in vlines.items():
        plt.axvline(val,color='r')
        #plt.text(val,y_text,name,rotation='vertical',color='r')
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig

def data_plot_dual_y(data,vlines={},title='',xlabel='',ylabels=[],legend_locs=['best','best'],show=False,close_fig=True,output_file=None,figsize=[4.5,3.]):
    # data should be {'foo':{'x':[...] (opt),'y':[...] (req)}, 'bar':{...}, ...}
    if len(data)>2:
        raise ValueError('dual-y plots should only have 2 data entries')
    fig = plt.figure(figsize=figsize)
    ax1 = fig.gca()
    ax2 = ax1.twinx()
    ax1.set_ylabel(ylabels[0])
    ax2.set_ylabel(ylabels[1])
    ax1.set_xlabel(xlabel)
    lbls = list(data.keys())
    y1 = data[lbls[0]].get('y')
    x1 = data[lbls[0]].get('x') or range(len(y1))
    y2 = data[lbls[1]].get('y')
    x2 = data[lbls[1]].get('x') or range(len(y2))
    ax1.plot(x1,y1,label=lbls[0])
    ax2.plot(x2,y2,label=lbls[1],color='orange')
    #y_text = np.min(MAE)+0.9*(np.max(RMS)-np.min(MAE))
    for name,val in vlines.items():
        ax2.axvline(val,color='r')
        #plt.text(val,y_text,name,rotation='vertical',color='r')
    ax1.legend(loc=legend_locs[0])
    ax2.legend(loc=legend_locs[1])
    plt.title(title)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig


def vertical_labeled_barchart(labels,values,title='',xlabel='',show=False,close_fig=True,output_file=None,figwidth=5.):
    ypos = np.arange(len(labels))
    figheight = 2+0.28*max(ypos)
    fig = plt.figure(figsize=(figwidth,figheight))
    ax1 = fig.gca()
    ax1.set_xlabel(xlabel)
    plt.title(title)
    ax1.barh(ypos,np.abs(values),align='center') 
    for yp,val in zip(ypos,values):
        plt.text(abs(val),yp,'{:.1e}'.format(val))
    ax1.set_yticks(ypos)
    ax1.set_yticklabels(labels)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig



def plot_rfe(RMS,MAE,title='',vlines={},show=False,close_fig=True,output_file=None,figsize=[4.5,3.]):
    # plot xval errors versus nfeats 
    fig = plt.figure(figsize=figsize)
    plt.plot(range(len(RMS)),RMS)
    plt.plot(range(len(MAE)),MAE)
    #y_text = np.min(MAE)+0.9*(np.max(RMS)-np.min(MAE))
    for name,val in vlines.items():
        plt.axvline(val,color='r')
        #plt.text(val,y_text,name,rotation='vertical',color='r')
    plt.legend(['RMS','MAE']+list(vlines.keys()))
    plt.title(title)
    plt.xlabel('remaining features')
    plt.ylabel('error')
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig

def plot_pred_xval(y_vals,y_pred,y_xval,title='',show=False,close_fig=True,output_file=None,figsize=[4.5,3.]):
    """Plot predicted and validated values versus actual values.

    Parameters
    ----------
    y_vals : iterable
        Actual y (output) values
    y_pred : iterable
        Predicted values corresponding to `y_vals`
    y_xval : iterable
        Cross-validation values corresponding to `y_vals`
    title : str (optional)
        Title for the plot 
    show : bool
        Whether or not to show the plot
    output_file : str 
        If provided, an image of the plot is saved at this path 
    figsize : [float,float] 
        List of two floats: [width,height]
    """
    # plot predictions versus test values
    x_limits = [np.min(y_vals),np.max(y_vals)]
    fig = plt.figure(figsize=figsize)
    plt.plot(x_limits,x_limits,'g')
    plt.scatter(y_vals,y_pred,8,'r')
    plt.scatter(y_vals,y_xval,8,'b')
    lgnd = ['true values','predictions','cross-validations']
    plt.title(title)
    plt.legend(lgnd)
    plt.xlabel('true values')
    plt.ylabel('modeled values')
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig 

def plot_logreg_cfs(results,file_path=None,show=False,close_fig=True,figsize=[4.5,3.]):
    """Plot the results of logistic regression combinatoric feature selection

    Parameters
    ----------
    results : dict
        Dict of logreg cfs results 
    file_path : str 
        If provided, figure is printed to this path 
    show : bool
        Flag for showing the figure on the display 
    close_fig : bool
        plt.close(fig) is called at the end if True
    figsize : [float,float]
        List of two floats: [width,height]

    Returns
    -------
    fig : matplotlib.figure.Figure
        matplotlib Figure object containing the rendered plot
    """
    fig = plt.figure(figsize=figsize)
    n_feats_list = list(results.keys())
    n_feats = np.sort(np.array(n_feats_list))
    f1 = [results[nf]['best_f1'] for nf in n_feats]
    prec = [results[nf]['best_precision'] for nf in n_feats]
    rec = [results[nf]['best_recall'] for nf in n_feats]
    acc = [results[nf]['best_accuracy'] for nf in n_feats]
    plt.plot(n_feats,f1)
    plt.plot(n_feats,prec)
    plt.plot(n_feats,rec)
    plt.plot(n_feats,acc)
    plt.legend(['f1','precision','recall','accuracy'])
    plt.title('best performance metrics over all combinations')
    plt.xlabel('number of features')
    plt.ylabel('performance metrics')
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    if file_path: plt.savefig(file_path, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig

def plot_gp_predictions(y_vals,y_means,y_sds,y_labels,title='',show=False,close_fig=True,output_file=None,figsize=[4.5,3.]):
    fig = plt.figure(figsize=figsize)
    plt.plot(y_vals,y_vals,'g')
    nbars = len(y_means)
    scales = np.arange(nbars+1,0,-1) 
    for y_mean,y_sd,y_label,scale in zip(y_means,y_sds,y_labels,scales):
        plt.errorbar(y_vals,y_mean,y_sd,elinewidth=1.*scale,label=y_label,fmt='o')
    plt.legend()
    plt.title(title)
    plt.xlabel('true values')
    plt.ylabel('modeled values')
    ax = plt.gca()
    new_ylims = list(ax.get_ylim())
    ymax = max(y_vals)
    ymin = min(y_vals)
    yval_range = ymax-ymin
    if new_ylims[0] < ymin-0.5*yval_range:
        new_ylims[0] = ymin-0.5*yval_range 
    if new_ylims[1] > ymax+0.5*yval_range: 
        new_ylims[1] = ymax+0.5*yval_range 
    ax.set_ylim(new_ylims)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file: plt.savefig(output_file, bbox_inches='tight',transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig

def data_scatter(x_vals,y_vals,vlines={},
                draw_colorbar=False,color_vals=None,colorlabel='',
                xlabel='',ylabel='',title='',
                figsize=[5.,4.],show=False,close_fig=True,output_file=None):
    xmin = np.min(x_vals)
    xmax = np.max(x_vals)
    xmin = np.min([xmin]+list(vlines.values()))
    xmax = np.max([xmax]+list(vlines.values()))
    ymin = np.min(y_vals)
    ymax = np.max(y_vals)
    if xmin < 0:
        xmin = xmin*1.2
    else:
        xmin = xmin*.8
    if xmax < 0:
        xmax = xmax*.8
    else:
        xmax = xmax*1.2
    fig = plt.figure(figsize=figsize)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    y_text = ymax-0.8*(ymax-ymin)
    for name,val in vlines.items():
        plt.axvline(val,color='r')
        plt.text(val,y_text,name,rotation='vertical')
    if color_vals is not None:
        scat = plt.scatter(x_vals,y_vals,s=8,c=color_vals,cmap='cool')
    else:
        scat = plt.scatter(x_vals,y_vals,s=8,c='r')
    if draw_colorbar:
        cbar = plt.colorbar(scat)
        cbar.ax.set_ylabel(colorlabel)
    ax = plt.gca()
    ax.set_xlim(left=xmin,right=xmax)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    if output_file:
        # TODO: clean up this hack:
        # it seems that sometimes, on some platforms,
        # the savefig fails with an underflow,
        # then succeeds on the next pass but without the colormap
        try:
            plt.savefig(output_file, bbox_inches='tight', transparent=True)
        except Exception as ex:
            plt.savefig(output_file, bbox_inches='tight', transparent=True)
    if show: plt.show()
    if close_fig: plt.close(fig)
    return fig


