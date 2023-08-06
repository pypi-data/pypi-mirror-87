# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 08:11:25 2020

@author: Harika
"""
#Importi
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px     
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

    
    
# Bar graph
def bar_graph(library, dataset_path, datasource_type, values_list_column, target_column, main_title, title_x_axis, title_y_axis):
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    target_column : dependent column mention
    main_title : Main title of graph
    title_x_axis : X_axis title of graph
    title_y_axis : Y_axis title of graph
    """
    if library == "plotly":
     
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        
        new_data = pd.pivot_table(dataset, values=values_list_column, columns= target_column)
        traces = [go.Bar(
        x = new_data.columns,
        y = new_data.loc[rowname],
        name = rowname
        )for rowname in new_data.index]
        layout = go.Layout(title = main_title)
        fig = plotly.graph_objs.Figure(data = traces,layout = layout)
        fig.update_layout(
            xaxis_title=title_x_axis,
            yaxis_title=title_y_axis)
        plotly.offline.iplot(fig)
        
    elif library =="matplotlib":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
            
        # Figure Size 
        fig = plt.figure(figsize =(10, 7)) 
        value = dataset[values_list_column]
        target = dataset[target_column]
        # Horizontal Bar Plot 
        plt.bar(value, target)
        plt.title(main_title)
        plt.xlabel(title_x_axis) 
        plt.ylabel(title_y_axis) 
    
        plt.show()
        
    elif library == "seaborn":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
      
        sns.barplot(x = values_list_column, y = target_column, data = dataset) 
        plt.title(main_title)
        plt.xlabel(title_x_axis) 
        plt.ylabel(title_y_axis) 
        plt.show() 
    
    else:
        print("incorrect library used")



#line graph
def line_graph(library, dataset_path, datasource_type, values_list_column, target_column, main_title, title_x_axis, title_y_axis):
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    target_column : dependent column mention
    main_title : Main title of graph
    title_x_axis : X_axis title of graph
    title_y_axis : Y_axis title of graph
    """
    if library == "plotly":
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
    
        new_data = pd.pivot_table(dataset, values=values_list_column, columns= target_column)
        traces = [go.Line(
        x = new_data.columns,
        y = new_data.loc[rowname],
        mode = 'lines',
        name = rowname
        )for rowname in new_data.index]
        layout = go.Layout(title = main_title)
        fig = plotly.graph_objs.Figure(data = traces,layout = layout)
        fig.update_layout(
            xaxis_title=title_x_axis,
            yaxis_title=title_y_axis)
        plotly.offline.iplot(fig)
        
        
    elif library == "matplotlib":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
            
        
        plt.plot(dataset[values_list_column], dataset[target_column])
        plt.title(main_title)
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
        
    elif library == "seaborn":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
  
        plt.figure(figsize=(15,15))
  
        plt.title(main_title)
        
        sns.lineplot(dataset[values_list_column],dataset[target_column])
  
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
        
    else:
        print("incorrect library used")



# scatter plot
def scatter_plot(library, dataset_path, datasource_type, values_list_column, target_column, main_title, title_x_axis, title_y_axis):
    
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    target_column : dependent column mention
    main_title : Main title of graph
    title_x_axis : X_axis title of graph
    title_y_axis : Y_axis title of graph
    """
    if library == "plotly": 
        
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
    
        new_data = pd.pivot_table(dataset, values=values_list_column, columns= target_column)
        traces = [go.Scatter(
        x = new_data.columns,
        y = new_data.loc[rowname],
        mode = 'markers',
        name = rowname
        )for rowname in new_data.index]
        layout = go.Layout(title = main_title)
        fig = plotly.graph_objs.Figure(data = traces,layout = layout)
        fig.update_layout(
            xaxis_title=title_x_axis,
            yaxis_title=title_y_axis)
        plotly.offline.iplot(fig)
   
        
   
    elif library == "matplotlib":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
    
  
        x = dataset[values_list_column]
        y = dataset[target_column]
       
        
        plt.scatter(x, y, cmap='viridis', alpha=0.3)
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
        
        
        
    elif library == "seaborn":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        
        # Set the width and height of the figure
        plt.figure(figsize=(14,6))
        
        # Add title
        plt.title(main_title)
        sns.scatterplot(data=dataset, x=values_list_column, y=target_column)
    
        
        # Add label for horizontal axis
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
        
    else :
        print("incorrect library used")
      
  
# Pie graph
def pie_graph(library, dataset_path, datasource_type, values_list_column, main_title):
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    main_title : Main title of graph
    """
    
    if library=="plotly":
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        trace = plotly.graph_objs.Pie(values=dataset[values_list_column].value_counts().values.tolist(),
                                      labels=dataset[values_list_column].value_counts().keys().tolist(),
                                      hoverinfo="label+percent+name",
                                      domain=dict(x=[0, .48]),
                                      marker=dict(line=dict(width=2,
                                                            color="rgb(243,243,243)")
                                                  ),
                                      hole=.6
                                      )
    
        layout = plotly.graph_objs.Layout(dict(title=values_list_column,
                                                plot_bgcolor="rgb(243,243,243)",
                                                paper_bgcolor="rgb(243,243,243)",
                                                annotations=[dict(text=main_title,
                                                                  font=dict(size=13),
                                                                  showarrow=False,
                                                                  x=.15, y=.5),
    
                                                            ]
                                                )
                                          )
        data = [trace]
        fig = plotly.graph_objs.Figure(data=data, layout=layout)
        plotly.offline.iplot(fig)
        
    elif library == "matplotlib":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        values = dataset[values_list_column].value_counts()
       
        per=[]
        for i in values:
            perc = i/values.sum()
            per.append(format(perc,'.2f'))
            
        plt.figure(figsize=(10,6))    
        plt.title(main_title,fontsize=20)
        plt.pie(per,autopct='%1.1f%%')
        plt.legend(values.index,loc='best', fontsize=15)
    
    
    elif library == "seaborn":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        
        pie, ax = plt.subplots(figsize=[10,6])
        values = dataset[values_list_column].value_counts().values.tolist()
        labels = dataset[values_list_column].value_counts().keys()
  
        plt.pie(x=values, autopct="%.1f%%", labels=labels, pctdistance=0.5)
        plt.title(main_title, fontsize=14);
        
                    
                    
    else:
        print("incorrect library used")
    

#Box Plot
def box_plot(library, dataset_path, datasource_type, values_list_column, target_column, main_title, title_x_axis, title_y_axis):
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    target_column : dependent column mention
    main_title : Main title of graph
    title_x_axis : X_axis title of graph
    title_y_axis : Y_axis title of graph
    """
    if library == "plotly": 
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
    
        fig = px.box(dataset, x=values_list_column, y=target_column)
        fig.show()
                      
          
    elif library == "matplotlib":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        
        
        dataset.boxplot(by = values_list_column, column = target_column, grid = False) 
        
        plt.title(main_title)
       
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
          
          
          
    elif library == "seaborn":
    
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
    
 
        plt.figure(figsize=(14,6))
    
        # Add title
        plt.title(main_title)
        ax= sns.boxplot(x=values_list_column,y=target_column,data=dataset)
       
        # Add label for horizontal axis
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
          
          
    else:
        print("incorrect library used")
      
      
  
  
#Violin Plot
def violin_plot(library, dataset_path, datasource_type, values_list_column, target_column, main_title, title_x_axis, title_y_axis):
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    target_column : dependent column mention
    main_title : Main title of graph
    title_x_axis : X_axis title of graph
    title_y_axis : Y_axis title of graph
    """
  
    if library == "matplotlib":
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
    
        data_to_plot = [dataset[values_list_column], dataset[target_column]]
        
        # Create a figure instance
        fig = plt.figure()
        
        # Create an axes instance
        ax = fig.add_axes([0,0,1,1])
        
        # Create the boxplot
        bp = ax.violinplot(data_to_plot)
        plt.title(main_title)
         
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
        plt.show() 
          
         
        
    elif library == "seaborn":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
            
        sns.violinplot(x=values_list_column, y=target_column, data=dataset, palette="Pastel1")
        plt.title(main_title)
       
        plt.xlabel(title_x_axis)
        plt.ylabel(title_y_axis)
        plt.show()
      
        
    elif library == "plotly":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
            
        
        fig1 = px.violin(dataset, y=values_list_column, x=target_column)
        
        fig1.show()
        
    
    else:
        print("incorrect library used")
                  
          
                  
  
# Function for correlation  matrix
def correlation_matrix(library, dataset_path, datasource_type, main_title, scale_title):
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    main_title : Main title of graph
    scale_title: Title of the scale mention
    """
    
    if library=="plotly":
        
      
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
  
        correlation = dataset.corr()
        matrix_cols = correlation.columns.tolist()
        corr_array = np.array(correlation)
  
        trace = plotly.graph_objs.Heatmap(z=corr_array,
                                          x=matrix_cols,
                                          y=matrix_cols,
                                          colorscale="Viridis",
                                          colorbar=dict(title=scale_title,
                                                        titleside="right"
                                                        ),
                                          )
  
        layout = plotly.graph_objs.Layout(dict(title=main_title,
                                                autosize=False,
                                                height=720,
                                                width=800,
                                                margin=dict(r=0, l=210,
                                                            t=25, b=210,
                                                            ),
                                                yaxis=dict(tickfont=dict(size=9)),
                                                xaxis=dict(tickfont=dict(size=9))
                                                )
                                          )
  
        data = [trace]
        fig = plotly.graph_objs.Figure(data=data, layout=layout)
        plotly.offline.iplot(fig)
        
  
    elif library=="matplotlib":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
  
        corr = dataset.corr()
  
        from matplotlib import rc
        rc('font',**{'family':'sans-serif','sans-serif':['Arial']})
        plt.suptitle(main_title, fontsize=16)
        
        plt.pcolor(corr, cmap='RdBu_r')
        cb = plt.colorbar()
        cb.set_label(scale_title, fontsize=14)
        plt.show()
        
        
    elif library=="seaborn":
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
            
        corr = dataset.corr()   
          
        plt.figure(figsize=(16, 6))
  
        heatmap = sns.heatmap(corr, vmin=-1, vmax=1, annot=True)
  
        heatmap.set_title(main_title, fontdict={'fontsize':12}, pad=12);
        plt.show()
        
    else:
        print("incorrect library used")




#Distribution Plot
def dist_plot(library, dataset_path, datasource_type, values_list_column, main_title):
    """
    Parameters:
    library : plotly/matplotlib/seaborn
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    main_title : Main title of graph
    """
    
    if library == "seaborn":
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        sns.set(rc={'figure.figsize':(11.7,8.27)})
        sns.distplot(dataset[values_list_column], bins=30)
        plt.title(main_title)
        plt.show()
      
    elif library == "matplotlib":
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        
        dataset[values_list_column].hist(bins=15, figsize=(11,11))
        plt.title(main_title)
        plt.show()
      
    elif library == "plotly":
        
        if datasource_type == 'csv':
            dataset = pd.read_csv(dataset_path)
        elif datasource_type == 'excel':
            dataset = pd.read_excel(dataset_path)
        elif datasource_type == 'dataframe':
            dataset = dataset_path
        
        
        hist_data = [dataset[values_list_column]]
        group_labels = [main_title] # name of the dataset
        
        fig = ff.create_distplot(hist_data, group_labels)
        fig.show()

    else:
        print("incorrect library used")
          
      
      

   
#Single lib plots      
def histogram(dataset_path, datasource_type):
    """
    Parameters:
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    """
    
    if datasource_type == 'csv':
        dataset = pd.read_csv(dataset_path)
    elif datasource_type == 'excel':
        dataset = pd.read_excel(dataset_path)
    elif datasource_type == 'dataframe':
        dataset = dataset_path
    dataset.hist(bins=15, figsize=(5,5))
    plt.show()
  
  
  
#To Check the missingvalues using heatmap
def missingvalues(dataset_path, datasource_type):
    """
    Parameters:
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    """
  
    if datasource_type == 'csv':
        dataset = pd.read_csv(dataset_path)
    elif datasource_type == 'excel':
        dataset = pd.read_excel(dataset_path)
    elif datasource_type == 'dataframe':
        dataset = dataset_path
        
    heatmap = sns.heatmap(dataset.isnull(),cbar=False, yticklabels=False, cmap = 'viridis')
    heatmap.set_title('Missing Values Check', fontdict={'fontsize':12}, pad=12);
    plt.show()


# to check count 
def count_plot(dataset_path, datasource_type, values_list_column, main_title):
    """
    Parameters:
    dataset_path : Path of dataset
    datasource_type : csv/excel/dataframe
    values_list_column : list of independent coumns mention
    main_title : Main title of graph
    """
 
    if datasource_type == 'csv':
        dataset = pd.read_csv(dataset_path)
    elif datasource_type == 'excel':
        dataset = pd.read_excel(dataset_path)
    elif datasource_type == 'dataframe':
        dataset = dataset_path
    sns.set(rc={'figure.figsize':(12,9)})
    sns.countplot(x = values_list_column, data = dataset, palette = "Set2") 
    plt.title(main_title)
    plt.show()
    # Show the plot 
    plt.show() 
   
                

   