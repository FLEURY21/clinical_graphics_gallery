
# Imports
#---------

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from typing import List
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib import lines as mlines

# Class MOSAIC
#-------------

class MOSAIC():
    def __init__(self, AE_data:pd.DataFrame, 
                       subjid_name:str, 
                       soc_terms:str, 
                       grade_num_name:str, 
                       by_mod1:str, 
                       by_mod2:str = "",
                       config:tuple = (1, 1),
                       title:str = "ADaM_AE_MOSAIC_plot_g", 
                       path:str = "None", 
                       save_fig:bool = False):
        """
        

        Parameters
        ----------
        AE_data : pd.DataFrame
            Adverse event table (AE) in format ADaM according to CDISC norm.
        subjid_name : str
            SUBJID column name. The SUBJID correspond to the Patient ID in
            clinical trial.
        soc_terms : str
            System Organ Class (SOC) column name.
        grade_num_name : str
            Adverse event grade column name. Grade must be coding according
            to CTC-AE classification in numeric.
        by_mod1 : str
            Column name of the first modality differenciation.
        by_mod2 : str, optional
            Column name of the second modality differenciation. The default is "".
        config: tuple, optional
            Configuration of modalities on the plot. If mod2 is not activate ("" value)
            then config must be (1) else config can be (1, 2) or (2, 1).
        title : str, optional
            Title of the plot. The default is "ADaM_AE_MOSAIC_plot_g".
        path : str, optional
            Save path. The default is None.
        save_fig : bool, optional
            If true then figure is save in the path. The default is False.

        Raises
        ------
        TypeError
            Test of parameters type.
        ValueError
            Test of data parameters.

        Returns
        -------
        None.

        """
        # Check parameters type.
        if not isinstance(subjid_name, str):
            raise TypeError("The SUBJID column name must be a string but find " + type(subjid_name) + " type.")
        if not isinstance(soc_terms, str):
            raise TypeError("The System Organ Class (SOC) column name must be a string but find " + type(soc_terms) + " type.")
        if not isinstance(grade_num_name, str):
            raise TypeError("The CTC-AE grades column name must be a string but find " + type(grade_num_name) + " type.")
        if not isinstance(by_mod1, str):
            raise TypeError("The first modality column name must be a string but find " + type(by_mod1) + " type.")
        if not isinstance(by_mod2, str):
            raise TypeError("The second modality column name must be a string but find " + type(by_mod2) + " type.")
        if not isinstance(config, tuple):
            raise TypeError("The config must be a tuple but find " + str(type(config)) + " type.")
        if not isinstance(title, str):
            raise TypeError("The title of the output document must be a string but find " + type(title) + " type.")
        if not isinstance(path, str):
            raise TypeError("The path for save the plot must be a string but find " + type(path) + " type.")
        if not isinstance(save_fig, bool):
            raise TypeError("The choice to save figure must be a boolean but find " + type(save_fig) + " type.")
        # Check if parameters data are present in dataset.
        if subjid_name not in AE_data.columns.to_list():
            raise ValueError(subjid_name + "column not found in the dataset.")
        if soc_terms not in AE_data.columns.to_list():
            raise ValueError(soc_terms + "column not found in the dataset.")
        if grade_num_name not in AE_data.columns.to_list():
            raise ValueError(grade_num_name + "column not found in the dataset.")
        if by_mod1 not in AE_data.columns.to_list():
            raise ValueError(by_mod1 + "column not found in the dataset.")
        if by_mod2 != "" and by_mod2 not in AE_data.columns.tolist():
            raise ValueError(by_mod2 + "column not found in the dataset.")
        if by_mod2 == "" and config != (1, 1):
            raise ValueError("If by_mod2 is desactivated then the config must be (1).")
        if by_mod2 != "" and config not in [(1, 2), (2, 1)]:
            raise ValueError("If by_mod2 is activated then the config must be (1, 2) or (2, 1).")
        # Check save figure configuration.
        if save_fig and title == "":
            raise ValueError("To save figure, title cannot be empty.")
        # Builder part.
        self.AE_data = AE_data
        self.subjid = subjid_name
        self.soc = soc_terms
        self.grade_num = grade_num_name
        self.mod1 = by_mod1
        self.mod2 = by_mod2
        self.config = config
        self.title = title
        self.path = path
        self.save_fig = save_fig
    
    # I. Accessor
    def get_AE_data(self):
        return self.AE_data
    def get_subjid(self):
        return self.subjid
    def get_soc(self):
        return self.soc
    def get_grade_num(self):
        return self.grade_num
    def get_mod1(self):
        return self.mod1
    def get_mod2(self):
        return self.mod2
    def get_config(self):
        return self.config
    def get_title(self):
        return self.title
    def get_path(self):
        return self.path
    def get_save_fig(self):
        return self.save_fig
    
    # II. Mutator
    def set_AE_data(self, new_data):
        self.AE_data = new_data
    def set_subjid(self, new_column_name):
        self.subjid = new_column_name
    def set_soc(self, new_column_name):
        self.soc = new_column_name
    def set_grade_num(self, new_column_name):
        self.grade_num = new_column_name
    def set_mod1(self, new_column_name):
        self.mod1 = new_column_name
    def set_mod2(self, new_column_name):
        self.mod2 = new_column_name
    def set_config(self, new_config):
        self.config = new_config
    def set_title(self, new_column_name):
        self.title = new_column_name
    def set_path(self, new_column_name):
        self.path = new_column_name
    def set_save_fig(self, new_column_name):
        self.save_fig = new_column_name
    
    # III. Data processing
    def select_variables_data(self):
        """
        Select columns for analysis.

        Returns
        -------
        None.

        """
        if self.get_mod2() == "":
            data_selected = self.get_AE_data().loc[:, [self.get_subjid(), self.get_mod1(), self.get_grade_num()]]
        else:
            data_selected = self.get_AE_data().loc[:, [self.get_subjid(), self.get_mod1(), self.get_mod2(), self.get_grade_num()]]
        self.set_AE_data(data_selected)
        
    def missing_data_processing(self):
        """
        Drop nan values

        Returns
        -------
        None.

        """
        # Drop nan values.
        AE_data_noNAN = self.get_AE_data().dropna()
        self.set_AE_data(AE_data_noNAN)
    
    def research_mod1_class(self):
        """
        Research all possible values for the first modality.

        Returns
        -------
        set
            Return a set of all possible values for the first modality.

        """
        return set(self.get_AE_data()[self.get_mod1()])
    
    def research_mod2_class(self):
        """
        Research all possible values for the second modality.

        Returns
        -------
        set
            Return a set of all possible values for the second modality.

        """
        return set(self.get_AE_data()[self.get_mod2()])
        
    
    def data_processing(self):
        """
        The method prepare MOSAIC data data for the MOSAIC plot.
        1) Variables are selected in AE table.
                Selected variables: SUBJID, first (and second) modality(ies)
                                    and numeric grade classification
        2) NaN values in AE table are dropped.
        3) Percent are computed according to modality(ies).

        Returns
        -------
        df_mosaic : pd.DataFrame
            Return MOSAIC pandas DataFrame. This dataset will be uses to
            build MOSAIC plot.

        """
        # Constantes
        ctc_ae_classification = {1, 2, 3, 4, 5}
        # 1) Variables selection.
        self.select_variables_data()
        # 2) Missing data processing.
        self.missing_data_processing()
        # 3) Prepare MOSAIC data
        mod1_class = self.research_mod1_class()
        ## If mod2 is empty
        if self.get_mod2() == "":
            mosaic_data = {"mod1": [],
                           "grade": [],
                           "percent_grade": []}
            for class_mod in mod1_class:
                local_data = self.get_AE_data()[self.get_AE_data()[self.get_mod1()] == class_mod]
                total_population_mod1 = local_data.shape[0]
                for ae_grade in ctc_ae_classification:
                    local_data2 = local_data[local_data[self.get_grade_num()] == ae_grade]
                    population_mod1_local_grade = local_data2.shape[0]
                    results = round((population_mod1_local_grade / total_population_mod1) * 100, 1)
                    mosaic_data["mod1"].append(class_mod)
                    mosaic_data["grade"].append(ae_grade)
                    mosaic_data["percent_grade"].append(results)
        else:
            mosaic_data = {"mod1": [],
                           "mod2": [],
                           "grade": [],
                           "percent_grade": []}
            mod2_class = self.research_mod2_class()
            for class_mod1 in mod1_class:
                for class_mod2 in mod2_class:
                    local_data = self.get_AE_data()[(self.get_AE_data()[self.get_mod1()] == class_mod1) & 
                                                    (self.get_AE_data()[self.get_mod2()] == class_mod2)]
                    total_population_mod1_and_mod2 = local_data.shape[0]
                    for ae_grade in ctc_ae_classification:
                        local_data2 = local_data[local_data[self.get_grade_num()] == ae_grade]
                        population_mod1_and_mod2_local_grade = local_data2.shape[0]
                        results = round((population_mod1_and_mod2_local_grade / total_population_mod1_and_mod2) * 100, 1)
                        mosaic_data["mod1"].append(class_mod1)
                        mosaic_data["mod2"].append(class_mod2)
                        mosaic_data["grade"].append(ae_grade)
                        mosaic_data["percent_grade"].append(results)
        df_mosaic = pd.DataFrame(mosaic_data)
        return df_mosaic
    
    # IV. Mosaic plot
    def plot_mosaic(self, fig_width=8, fig_height=10):
        """
        Plot MOSAIC plot of ADVERSE EVENT. 
        

        Parameters
        ----------
        fig_width : float, optional
            Figure width. The default is 8.
        fig_height : float, optional
            Figure height. The default is 10.

        Returns
        -------
        None.
        
        TO DO
        -----
            1) Adapte title and subtitle size  in function of groups size.
            2) Adapte legend location and size.
            3) Optimize length between bar and subplots.
            4) Adapt police size for x axis.
            5) Found a better theme and design for the global plot.
            6) Update the design for mosaic plot with one modality.

        """
        title_fig = self.get_path() + self.get_title() + ".png"
        colors = {1: "lightgreen", 2: "skyblue", 3: "goldenrod", 4: "tomato", 5: "orchid"}
        l = []
        for i,j in colors.items():
            l.append(mlines.Line2D([], [], 
                                   color=j, 
                                   linestyle="None", 
                                   marker="o", 
                                   markersize=8, 
                                   label=str(i)))
        mosaic_data = self.data_processing()
        mosaic_data["grade"] = pd.Categorical(mosaic_data["grade"], categories=[1, 2, 3, 4, 5], ordered=True)
        mosaic_data = mosaic_data.sort_values(by=["grade"])
        mosaic_data = mosaic_data[mosaic_data["percent_grade"] != 0]
        if self.get_mod2() == "":
            df_pivot = mosaic_data.pivot(index="mod1", 
                                         columns="grade", 
                                         values="percent_grade")
            ax = df_pivot.plot(kind="bar", 
                               stacked=True, 
                               figsize=(fig_width, fig_height), 
                               color=colors,
                               width=0.9,
                               edgecolor="black",
                               linewidth=2)
            for c in ax.containers:
                ax.bar_label(c, label_type='center', fontsize=13, fontweight='bold')
            ax.tick_params(axis='x', rotation=0)
            ax.set_xlabel("")
            plt.ylabel("Grade (%)")
            plt.legend(title="Grade")
            plt.tight_layout()
            if self.get_save_fig():
                plt.savefig(title_fig, format="png", bbox_inches='tight')
            plt.show()
        if self.get_mod2() != "" and self.get_config() == (1, 2):
            fig, ax = plt.subplots(1, len(set(mosaic_data["mod1"])), 
                                   figsize=(fig_width, fig_height), 
                                   sharey=True)
            for i, mod in enumerate(sorted(set(mosaic_data["mod1"]))):
                df_mod = mosaic_data[mosaic_data["mod1"] == mod]
                df_pivot = df_mod.pivot_table(
                    columns="grade",
                    index="mod2",
                    values="percent_grade")
                df_pivot.plot(kind="bar", 
                              stacked=True, 
                              color=colors, 
                              ax=ax[i], 
                              legend=False, 
                              width=0.9,
                              edgecolor="black",
                              linewidth=2)
                for c in ax[i].containers:
                    ax[i].bar_label(c, 
                                    label_type='center', 
                                    fontsize=10, 
                                    fontweight='bold')
                ax[i].set_xlabel("")
                ax[i].tick_params(axis='x', rotation=0)
                ax[i].set_title(mod,
                                fontsize=11.5,
                                bbox=dict(facecolor='white', 
                                          edgecolor='black', 
                                          boxstyle='round, pad=0.15'))
            ax[0].set_ylabel("Grade (%)")
            fig.patches.extend([plt.Rectangle((0, 0.95), 
                                              1, 0.03, 
                                              transform=fig.transFigure, 
                                              facecolor='gainsboro', 
                                              zorder=1, 
                                              edgecolor='black', 
                                              linewidth=2)])
            fig.text(0.5, 0.963, "Treatment", 
                     ha='center', 
                     va='center', 
                     fontsize=16, 
                     fontweight='bold', 
                     color='black', 
                     zorder=2)
            plt.legend(handles=l, loc="upper left", 
                       bbox_to_anchor=(1, 1), 
                       title="Grade", 
                       title_fontproperties={'weight': 'bold', 'style': 'normal', 'size': 10} , 
                       handletextpad=0.3, 
                       handlelength=1.0,
                       frameon=False)
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            if self.get_save_fig():
                plt.savefig(title_fig, format="png", bbox_inches='tight')
            plt.show()
        if self.get_mod2() != "" and self.get_config() == (2, 1):
            fig, ax = plt.subplots(1, len(set(mosaic_data["mod2"])), 
                                   figsize=(fig_width, fig_height), 
                                   sharey=True)
            for i, mod in enumerate(sorted(set(mosaic_data["mod2"]))):
                df_mod = mosaic_data[mosaic_data["mod2"] == mod]
                df_pivot = df_mod.pivot_table(
                    columns="grade",
                    index="mod1",
                    values="percent_grade")
                df_pivot.plot(kind="bar", 
                              stacked=True, 
                              color=colors, 
                              ax=ax[i], 
                              legend=False, 
                              width=0.9,
                              edgecolor="black",
                              linewidth=2)
                for c in ax[i].containers:
                    ax[i].bar_label(c, 
                                    label_type='center', 
                                    fontsize=10, 
                                    fontweight='bold')
                ax[i].set_xlabel("")
                ax[i].tick_params(axis='x', rotation=0)
                ax[i].set_title(mod, 
                                bbox=dict(facecolor='white', 
                                          edgecolor='black', 
                                          boxstyle='round, pad=0.3'))
            ax[0].set_ylabel("Grade (%)")
            fig.patches.extend([plt.Rectangle((0, 0.95), 
                                              1, 0.03, 
                                              transform=fig.transFigure, 
                                              facecolor='gainsboro', 
                                              zorder=1, 
                                              edgecolor='black', 
                                              linewidth=2)])
            fig.text(0.5, 0.963, "Group", 
                     ha='center', 
                     va='center', 
                     fontsize=16, 
                     fontweight='bold', 
                     color='black', 
                     zorder=2)
            plt.legend(handles=l, loc="upper left", 
                       bbox_to_anchor=(1, 1), 
                       title="Grade", 
                       title_fontproperties={'weight': 'bold', 'style': 'normal', 'size': 10} , 
                       handletextpad=0.3, 
                       handlelength=1.0,
                       frameon=False)
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            if self.get_save_fig():
                plt.savefig(title_fig, format="png", bbox_inches='tight')
            plt.show()
            
                
                    
                
            
            
        
        

        
    
        
                    
                    
                
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        


