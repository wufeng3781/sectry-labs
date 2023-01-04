.. raw:: html
    
	 <style> .font {font-family:'Consolas'; font-size:13pt} </style>

.. role:: font

.. _user manual file: https://github.com/nexus-lab/ezsetup/wiki/User-Guide

============
Data Privacy
============

Introduction
------------

**Overview:** Websites, applications, and social media platforms often collect and store personal data from their users. If applications and platforms do not place adequate safeguards on the data they collect, data breaches can happen and compromises user privacy. In this lab, students will learn data anonymization and the *k-anonymity* privacy model. The weakness of *k-anonymity* will also be introduced. This lab also lets students practice using ARX, a data anonymization tool, to apply *k-anonymity*.

**Objectives:** Upon completion of this lab, students will be able to

-	Explain the importance and necessity of data privacy;
-	Explain *k-anonymity* and its weakness;
-	Analyze the utility of anonymized data;
-	Apply ARX to anonymize sensitive personal data.

**Prerequisites:**

-	Practical experience with Linux commands;
-	Practical experience in using Excel or Google Sheets.

**Length of Completion:** 1 – 4 hours

**Level of Instruction:** sophomore/junior/senior

**Learning Setting:** both (face-to-face and online)

**Background:**

	**EZSetup** is a Web application capable of creating various user-defined cybersecurity practice environments (e.g., labs and competition scenarios) in one or more computing clouds (e.g., OpenStack or Amazon AWS). EZSetup provides a Web user interface for practice designers to visually create a practice scenario and easily deploy it in a computing cloud, which allows for customization and reduces overhead in creating and using practice environments. End users are shielded from the complexity of creating and maintaining practice environments and therefore can concentrate on cybersecurity practices.
	
	A few video clips that demonstrate creating and conducting a lab using EZSetup can be viewed on YouTube at `<https://www.youtube.com/playlist?list=PL8aGBn1vt25Seies5W9_2xkDFErfe3S7h>`_. For more information about EZSetup, please check the bundled `user manual file`_.
	
	**ARX** is a comprehensive open source software for anonymizing sensitive personal data. It supports a wide variety of (1) privacy and risk models, (2) methods for transforming data and (3) methods for analyzing the usefulness of output data. ARX software and sources can be accessed at `<https://arx.deidentifier.org/>`_.


**Lab Environment:**

	In this lab, students will access one virtual machine (VM) instance named arx-vm from EZSetup. The configuration of the instance is provided in **Table 1**. **Figure 1** illustrates the lab network topology.


	.. list-table:: **Table 1** VM properties and access information
           :header-rows: 1

	   * - Name
	     - Image
	     - RAM
	     - VCPU
	     - Disk
	     - Login Account
	   * - arx-vm
	     - ARM-VM
	     - 4GB
	     - 2
	     - 40GB
	     - See EZSetup
	
.. figure:: /xie/media/data_privacy/fig1.png
   :alt: alternate text
   :figclass: align-center
	
   **Figure 1** Lab Network topology
	
In the arx-vm instance, we prepare two datasets in the ``~/Desktop/data`` directory. One called ``adult.csv`` is a collection of data from the 1994 census database. The other called ``patients_csv.csv`` is a synthetic data set produced with the Synthea program. All personal information within the synthetic dataset is random and fictitious, so any resemblance to persons living or dead is coincidental.

In addition, we have pre-installed ARX in the arx-vm instance. Students can use it to import the dataset, implement the data anonymization approach and analyze the data utility.

Each student will get a specific slice (a collection of resources that run in an isolated environment) of this lab. Therefore, each one can work separately with no worry about his/her work being interfered by another’s operation.


Task 1: Linkage Attack
----------------------

Let us first study a classic case to see how linkage attack obtains personal sensitive data and why data anonymization is important for protecting personal data.

.. figure:: /xie/media/data_privacy/fig2.png
	:alt: alternate text
	:figclass: align-center
	
	**Figure 2** Linkage Attack

In 1997, the Massachusetts state Group Insurance Commission (GIC) released hospital visit data which included each patient’s 5-digit zip code, gender, and date of birth. Governor Weld of Massachusetts reassured the public that the data was adequately ‘anonymized’, as primary identifiers (such as name and address) had been deleted. However, Latanya Sweeney managed to find Governor Weld’s personal health records by combining the GIC data with an electoral roll database as illustrated in **Figure 2**. She showed that around 87% of the US population can be uniquely identified with their 5-digit zip code, gender, and date of birth (all publicly available). Therefore, she can identify lots of patients and their personal health records.

With a linkage attack, attackers combine the original data with other accessible data sources to uniquely identify an individual and learn (often sensitive) information about this person. Years later, attackers can access more datasets and utilize more powerful tools for linking and analyzing them.

Let us study one of the most common anonymous techniques, *k-anonymity*, in the next task to protect personal sensitive information.

Lab Exercise 1
##############

.. list-table:: **Table 2** Medical Information
   :header-rows: 1

   * - Gender
     - Birth
     - Race
     - Zip
     - Disease
   * - M
     - 1986
     - White
     - 0214*
     - Heart Disease
   * - F
     - 1993
     - White
     - 0214*
     - Hepatitis
   * - M
     - 1997
     - Black
     - 0213*
     - Bronchitis
   * - M
     - 1993
     - Black
     - 0213*
     - Broken Arm
   * - F
     - 1980
     - Asian
     - 0213*
     - Hang nail
   * - F
     - 1986
     - White
     - 0213*
     - Flu
	
	
.. list-table:: **Table 3** Voter Registration Information
   :header-rows: 1

   * - Name
     - Gender
     - Birth
     - Zip
     - Race
   * - Andre
     - Male
     - 1980
     - 02124
     - Asian
   * - Beth
     - Female
     - 1986
     - 02135
     - White
   * - Carol
     - Female
     - 1986
     - 02135
     - Black
   * - Dan
     - Male
     - 1993
     - 02135
     - White
   * - Ellen
     - Female
     - 1992
     - 02135
     - Black

1. Give **Table 2** and **Table 3**, whose sensitive information can you obtain via linkage attack? Can you explain it?

Task 2: *k-anonymity*
---------------------

Through Task 1, we have known that simply removing names from a dataset is not sufficient to achieve anonymization. Anonymized data can be re-identified by linking data with another (public) dataset. Addressing the risk of re-identification of anonymized data is an important topic in the data privacy area. Now, let us start to learn an anonymization approach called *K-anonymity* to protect sensitive data.

Task 2.1: Attribute categories in dataset
#########################################

According to the importance and sensitivity, the attributes of the input dataset can be divided into four categories:

**Identifying attributes:** those are associated with a high risk of re-identification. They should be removed from the dataset. Typical examples are names or social security numbers (SSN).

**Quasi-identifying attributes:** those can be used in combination for re-identification attacks. They should be transformed. Typical examples include gender, date of birth, and ZIP code.

**Sensitive attributes:** those encode properties with which individuals are not willing to be linked. As such, they might be of interest to an attacker and, if disclosed, could cause harm to data subjects. Typical examples include salary and diseases profile.

**Insensitive attributes:** those are not associated with privacy risks. 


Lab Exercise 2.1
~~~~~~~~~~~~~~~~

.. list-table:: **Table 4** Health Records
   :header-rows: 1

   * - Name
     - Gender
     - Age
     - Zip
     - Education
     - Marital Status
     - Disease
   * - Andre
     - Male
     - 39
     - 02134
     - Masters
     - Married
     - Viral infection
   * - Beth
     - Female
     - 34
     - 02134
     - Masters
     - Divorced
     - Cancer
   * - Carol
     - Female
     - 34
     - 02134
     - Masters
     - Married
     - Hepatitis
   * - Dan
     - Male
     - 27
     - 02135
     - Bachelors
     - Single
     - Heart Disease
   * - Ellen
     - Female
     - 27
     - 02135
     - Bachelors
     - Single
     - Flu
   * - Fabiano
     - Male
     - 38
     - 02135
     - Masters
     - Single
     - Bronchitis
   * - Gary
     - Male
     - 25
     - 02135
     - Bachelors
     - Single
     - Viral infection
   * - Hannah
     - Female
     - 29
     - 02135
     - Bachelors
     - Married
     - Broken Arm

1. Given **Table 4**, identify which attributes are identifying attributes, quasi-identifying attributes, and sensitive attributes.

Task 2.2: *k-anonymity* protection model
########################################

**k-anonymity protection model**, proposed by Latanya Sweeney, makes every record in the table indistinguishable from at least k-1 other records with respect to quasi-identifiers.

Let us see an example. There are 6 attributes and 8 records in **Table 4**. There are two methods for achieving k-anonymization for some value of k:

**Suppression:** In this method, certain values of the attributes are replaced by an asterisk ``*``. All or some values of a column may be replaced by ``*``. In **Table 5**, we have replaced all the values in the ``Name`` attribute and all the values in the ``Marital Status`` attribute with a ``*``.

**Generalization:** In this method, individual values of attributes are replaced with a broader category. One form of generalization is the hierarchy. In case of hierarchy, the commonalities are organized into a tree structured form. At the root of any subtree are found all the attributes and behavior common to all of the descendants of that root. This type of tree structure is referred to as a **generalization hierarchy** because the root provides more general properties shared by all its descendants. The diagram in **Figure 3** illustrates a possible hierarchical structure for ages. 

.. figure:: /xie/media/data_privacy/fig3.png
	:alt: alternate text
	:figclass: align-center
	
	**Figure 3** Age Hierarchy

For the **Table 4**, we can choose age range from level 2 in **Figure 3**. Thus, the value ``27`` of the attribute ``Age`` can be replaced by ``[20,30]``, the value ``39`` by ``[30,40]``.

.. list-table:: **Table 5** Anonymized Health Records
   :header-rows: 1

   * - Name
     - Gender
     - Age
     - Zip
     - Education
     - Marital Status
     - Disease
   * - *
     - Male
     - [30,40]
     - 02134
     - Masters
     - *
     - Viral infection
   * - *
     - Female
     - [30,40]
     - 02134
     - Masters
     - *
     - Cancer
   * - *
     - Female
     - [30,40]
     - 02134
     - Masters
     - *
     - Hepatitis
   * - *
     - Male
     - [20,30]
     - 02135
     - Bachelors
     - *
     - Heart Disease
   * - *
     - Female
     - [20,30]
     - 02135
     - Bachelors
     - *
     - Flu
   * - *
     - Male
     - [30,40]
     - 02134
     - Masters
     - *
     - Bronchitis
   * - *
     - Male
     - [20,30]
     - 02135
     - Bachelors
     - *
     - Viral Infection
   * - *
     - Female
     - [20,30]
     - 02135
     - Bachelors
     - *
     - Broken Arm

If we implement 2-anonymity to anonymize the records in **Table 4**, the result is shown in **Table 5**. The output records have 2-anonymity with respect to the attributes ``Gender``, ``Age``, ``Zip``, and ``Education`` since for any combination of these attributes found in any row of the table there are always at least 2 rows with those exact attributes. For example, the second and third lines in **Table 5** have the same values for all quasi-identifying attributes.

Lab Exercise 2.2
~~~~~~~~~~~~~~~~

1. Anonymize **Table 4** to achieve 3-anonymity and draw the anonymized table.

Task 2.3: ARX - Data anonymization tool
#######################################

After learning how to implement *k-anonymity* manually to handle a small-size dataset, we now learn how to use a data anonymization tool ARX for anonymizing large datasets.

First, we can log into ARX VM via a GUI interface (e.g., noVNC) and double click the ARX icon on the desktop to open ARX application.

.. figure:: /xie/media/data_privacy/fig4.png
	:alt: alternate text
	:figclass: align-center
	
	**Figure 4** arx-vm Desktop

After that, click ``File`` -> ``New project`` to start a new project.

.. note: The title you give your project is not what it will save as. Be sure to save it with your preferred file name.

Then, you can import the ``adult.csv`` dataset by clicking ``File`` -> ``Import data``. When you import data, you will see the dashboard like **Figure 5**.

.. figure:: /xie/media/data_privacy/fig5.png
	:alt: alternate text
	:figclass: align-center
	
	**Figure 5** ARX dashboard

For *k-anonymity*, mark **every** attribute in the input data section as quasi-identifying (``sex``, ``age``, ``race``, etc.). We can click the attribute column on the left side and choose ``Quasi-identifying`` from the ``Type`` drop-down menu.

.. figure:: /xie/media/data_privacy/fig6.png
	:alt: alternate text
	:figclass: align-center
	
	**Figure 6** Attribute Type
	
Now, we need to assign hierarchies. You will create the hierarchy for age, but others have been provided for you to import.

 1.	**To create the age hierarchy:** First, select the age column. Now, click ``Edit`` -> ``Create hierarchy``. Selecting ``Use intervals`` option, under the ``Range`` tab, make your values match those in **Figure 7**:

 .. figure:: /xie/media/data_privacy/fig7.png
 	:alt: alternate text
 	:figclass: align-center
	
	**Figure 7** Hierarchy Wizard
 
 2. Select the first set of numbers and, under the ``Interval`` tab, set the first interval to min: 0 and max: 5. Right click the interval and choose ``Add new level``. The subsequent levels consisting of groups of intervals from the previous level can be specified. Each group combines a given number of elements from the previous level. Any sequence of intervals or groups is automatically repeated to cover the complete range of the attribute. For example, to generalize arbitrary integers into intervals of length 10, only one interval [0, 10] needs to be defined. Defining a group of size two on the next level automatically generalizes integers into groups of size 20. As is shown in **Figure 8** below, the editor visually indicates automatically created repetitions of intervals and groups. Let’s create intervals until the final interval has a maximum value of 80.

  .. figure:: /xie/media/data_privacy/fig8.png
     :alt: alternate text
     :figclass: align-center
	
     **Figure 8** Create A Hierarchy By Defining Intervals

 3. **To import hierarchy:** select an attribute column and click ``File`` -> ``Import`` hierarchy to import the corresponding hierarchy file from ``~/Desktop/data/hierarchies`` directory.

Once all the hierarchies are set, click ``+`` button under the Attribute metadata tab to select and configure a privacy model. Let’s choose the *k-Anonymity* privacy model and set k to 2.

.. figure:: /xie/media/data_privacy/fig9.png
   :alt: alternate text
   :figclass: align-center
	
   **Figure 9** Privacy Models
   
In the ``general settings`` tab of **Figure 10**, make the suppression limit to 100%, which means the maximal number of records that can be removed from the input dataset.

.. figure:: /xie/media/data_privacy/fig10.png
   :alt: alternate text
   :figclass: align-center
	
   **Figure 10** Properties of the transformation process

We keep the configuration of the other tabs as default. If you want to know more about how to configure the properties of the transformation process, you can click ○? in upper right corner of **Figure 10**. 

After clicking the ``Edit`` -> ``Anonymize``, you can select the ``Explore results`` tab to explore how it was anonymized.

.. figure:: /xie/media/data_privacy/fig11.png
   :alt: alternate text
   :figclass: align-center
	
   **Figure 11** Visualization of the Solution Space


.. admonition:: Please Advise
	
	Once you reach this point, if your results do not appear as it does in **Figure 11**, ensure **every** attribute in the input data section was set to quasi-identifying (``sex``, ``age``, ``race``, ``marital-status``, ``education``, ``native-country``, ``workclass``, ``occupation``, and ``salary-class``) before continuing.

During the anonymization process, ARX characterizes a solution space of potential transformations of the input dataset. For each solution candidate, it is determined whether risk thresholds are met, and data quality is quantified according to the given model. **Figure 11** displays a set of the solution space. The solution space is displayed as a Hasse diagram of the underlying generalization lattice like **Figure 11** by default.

Here, each node represents a single transformation, which is identified by the generalization levels that it specifies for the quasi-identifiers in the input dataset. The green ellipse represents a transformation that results in a privacy-preserving dataset. The orange rectangle denotes the transformation that is optimal regarding to the specified utility measure. ARX applies the transformation in the orange rectangle by default. If you want to apply the other transforms, you can right click the green ellipse and select ``Apply transform``. 

The solution space could be visualized as a list or a set of titles by selecting the tab in the bottom left corner. 

Now we can select ``Analyze utility`` tab in **Figure 12**. In the upper left area, there are original data. The result of the currently selected transformation is shown in the upper right area. The bottom left and right areas compare statistical information about the currently selected attribute(s).

.. figure:: /xie/media/data_privacy/fig12.png
   :alt: alternate text
   :figclass: align-center
	
   **Figure 12** Analyzing Data Utility

Finally, you can select ``File`` -> ``Create certificate`` to generate a certificate PDF.


Lab Exercise 2.3
~~~~~~~~~~~~~~~~

Following the instructions in Task 2.3, please answer the following questions.

 1.	When you apply the transform in the orange rectangle, what is the number of total transformations? How many records are suppressed?
 
 2.	Generate the certificate PDF.
 
 3.	Set the weight of ``race`` attribute to 1 and conduct a **3-anonymity** model to anonymize the dataset.
 
  - What is the optimal transformation?
  -	Generate the certificate PDF.


Task 3: Attack Models
#####################

Many times, the *k-anonymity* method can offer a desired protection model. However, re-identification is still possible for this approach. In Task 3, we introduce two attack methods against the *k-anonymity*.

**Homogeneity attack:** All data with the same quasi-identifiers have the same sensitive attribute.

.. list-table:: **Table 6** Homogeneity Attack
   :header-rows: 1

   * - Gender
     - Age
     - Education
     - Zip
     - Race
     - Disease
   * - Female
     - 20 - 24
     - *
     - 3790*
     - Black
     - Lupus
   * - Female
     - 20 - 24
     - *
     - 3790*
     - Asian
     - PCOS
   * - **Male**
     - **55 - 59**
     - *
     - 3740*
     - **White**
     - **Diabetes II**
   * - **Male**
     - **55 - 59**
     - *
     - 3740*
     - **White**
     - **Diabetes II**
   * - **Male**
     - **55 - 59**
     - *
     - 3740*
     - **White**
     - **Diabetes II**
   * - Male
     - 30 - 35
     - *
     - 376**
     - *
     - Cirrhosis
   * - Male
     - 30 - 35
     - *
     - 376**
     - *
     - COPD

Our subject is a 57-year-old white man living in the area with ZIP code 37402. All the entries that could be narrowed down have the same diagnosis (sensitive attribute). Therefore, we can deduce that our subject has a Type II Diabetes.

**Background knowledge attack:** Information about one person or quasi-identifier connects an individual to a sensitive attribute.

.. list-table:: **Table 7** Homogeneity Attack
   :header-rows: 1

   * - Gender
     - Age
     - Education
     - Zip
     - Race
     - Disease
   * - Female
     - 20 - 24
     - *
     - 3790*
     - Black
     - Lupus
   * - Female
     - 20 - 24
     - *
     - 3790*
     - Asian
     - PCOS
   * - **Male**
     - **55 - 59**
     - *
     - 3740*
     - **White**
     - **Gaucher Disease**
   * - **Male**
     - **55 - 59**
     - *
     - 3740*
     - **White**
     - **Shingles**

Lab Exercise 3
~~~~~~~~~~~~~~

Assume you are an attacker who has acquired an anonymized healthcare dataset. Open the ``patient_kanon.csv`` file on your preferred spreadsheet software (Microsoft Excel, Google Sheets, or equivalent). 

Use one of the *k-anonymity* attack models, homogeneity or background information, to identify the illnesses of the following two patients. In your response, include their health record and the attack model you are able to use. 

 a.	You have been hired to release information about a politician in your state. Maria Angelos is a 45-year-old widow. She is white, but of Greek origin.
 
 b.	Your next target is Hoyt Walter, a Black man who is single and 27 years old.

.. admonition:: Hint

	You can filter the dataset as necessary to find rows of related data.

What To Sumbit
--------------

Typeset your answers (with screenshots as evidence) to all the questions in a.pdf file. Name the file as ``privacy--YourLastName_FirstName.pdf``. Submit this with a zip file containing your generated certificates. 
