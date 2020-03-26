#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[2]:


#Create a dataframe for the district summary
dsummary_df = pd.DataFrame({'Total Schools': [0], 'Total Students': [0],                           'Total Budget': [0], 'Average Math Score': [0],                            'Average Reading Score': [0], '% Passing Math': [0],                            '% Passing Reading': [0], '% Overall Passing Rate': [0]})
dsummary_df['Total Schools'] = len(school_data)
dsummary_df['Total Students'] = len(student_data)
dsummary_df['Total Budget'] = school_data['budget'].sum()
dsummary_df['Total Budget'] = dsummary_df['Total Budget'].map('${:,.2f}'.format)
dsummary_df['Average Math Score'] = school_data_complete['math_score'].mean()
dsummary_df['Average Reading Score'] = school_data_complete['reading_score'].mean()
dsummary_df['% Passing Math'] = len([score for score in school_data_complete['math_score'] if score >= 70]) / dsummary_df['Total Students'] * 100
dsummary_df['% Passing Reading'] = len([score for score in school_data_complete['reading_score'] if score >= 70]) / dsummary_df['Total Students'] * 100
dsummary_df['% Overall Passing Rate'] = (dsummary_df['Average Math Score'] + dsummary_df['Average Reading Score']) / 2
dsummary_df.head()


# In[ ]:





# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# In[14]:


#Find all the school names
schools = school_data_complete["school_name"].unique()

#Create a dictionary of schools with all students grades and school information
schoolsDict = {elem : pd.DataFrame for elem in schools}
for key in schoolsDict.keys():
    schoolsDict[key] = school_data_complete[:][school_data_complete["school_name"] == key]

#Create dataframe of School names and their type
ssummary_df = pd.DataFrame(columns = ["School Name", "School Type"])
ssummary_df["School Name"] = school_data_complete["school_name"].unique()
ssummary_df["School Type"] = [school for school in school_data["type"]]

#create and merge a dataframe with the number of students at each school
student_count = pd.DataFrame(school_data_complete.groupby("school_name")["student_name"].count()).reset_index()
student_count = student_count.rename(columns={"school_name": "School Name","student_name": "Total Students"})
ssummary_df = pd.merge(ssummary_df, student_count, how="left", on=["School Name", "School Name"])

#Cretae and merge a dataframe with each schools budget
budget = pd.DataFrame(school_data[["school_name","budget"]])
budget = budget.rename(columns={"school_name": "School Name","budget": "Total School Budget"})
ssummary_df = pd.merge(ssummary_df, budget, how="left", on=["School Name", "School Name"])

#Add to the dataframe the per student spending and format the values with dollar signs
ssummary_df["Per Student Budget"] = ssummary_df["Total School Budget"] / ssummary_df["Total Students"]
ssummary_df['Per Student Budget'] = ssummary_df["Per Student Budget"].map('${:,.2f}'.format)
ssummary_df['Total School Budget'] = ssummary_df["Total School Budget"].map('${:,.2f}'.format)

#Create and merge a dataframe with the average math scores at each school
ave_math_score = pd.DataFrame(school_data_complete.groupby("school_name")["math_score"].mean()).reset_index()
ave_math_score = ave_math_score.rename(columns={"school_name": "School Name", "math_score": "Average Math Score"})
ssummary_df = pd.merge(ssummary_df,ave_math_score, how="left",on=["School Name", "School Name"])

#Create and merge a dataframe with the average reading scores at each school
ave_read_score = pd.DataFrame(school_data_complete.groupby("school_name")["reading_score"].mean()).reset_index()
ave_read_score = ave_read_score.rename(columns={"school_name": "School Name", "reading_score": "Average Reading Score"})
ssummary_df = pd.merge(ssummary_df,ave_read_score, how="left",on=["School Name", "School Name"])

#Count the passing math grades and merge the % passed into the summary dataframe
passing_math = {}
for school in schools:
    passing_math[school] = len([score for score in schoolsDict[school]["math_score"] if score >= 70]) / len(schoolsDict[school]) * 100
passing_math_df = pd.DataFrame(passing_math.items(), columns = ["School Name", "% Passing Math"])
ssummary_df = pd.merge(ssummary_df,passing_math_df, how="left",on=["School Name", "School Name"])

#Count the passing reading grades and merge the % passed into the summary dataframe
passing_reading = {}
for school in schools:
    passing_reading[school] = len([score for score in schoolsDict[school]["reading_score"] if score >= 70]) / len(schoolsDict[school]) * 100
passing_reading_df = pd.DataFrame(passing_reading.items(), columns = ["School Name", "% Passing Reading"])
ssummary_df = pd.merge(ssummary_df,passing_reading_df, how="left",on=["School Name", "School Name"])

#Average the math and reading scores and add a new column
ssummary_df["% Overall Passing"] = ssummary_df[['% Passing Math', '% Passing Reading']].mean(axis=1)

#Set the index to the school name
ssummary_df = ssummary_df.set_index("School Name")

ssummary_df


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[4]:


#Sort %Overall Passing descending, display first five values 
ssummary_df = ssummary_df.sort_values(by='% Overall Passing', ascending=False)
ssummary_df.head(5)


# In[ ]:





# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[5]:


#Sort %Overall Passing ascending, display first five values 
ssummary_df = ssummary_df.sort_values(by='% Overall Passing', ascending=True)
ssummary_df.head(5)


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[6]:


#Break down the school data into four data frames, one for each grade
grade_9 = school_data_complete[school_data_complete["grade"] == "9th"]
grade_10 = school_data_complete[school_data_complete["grade"] == "10th"]
grade_11 = school_data_complete[school_data_complete["grade"] == "11th"]
grade_12 = school_data_complete[school_data_complete["grade"] == "12th"]

#Create a pandas series for each grade with the average math score by school
math_9_df = grade_9.groupby("school_name")["math_score"].mean()
math_10_df = grade_10.groupby("school_name")["math_score"].mean()
math_11_df = grade_11.groupby("school_name")["math_score"].mean()
math_12_df = grade_12.groupby("school_name")["math_score"].mean()

#Merge all the grades into a single dataframe
math_scores_merged = pd.merge(math_9_df,math_10_df, how="left",on="school_name")
math_scores_merged = math_scores_merged.rename(columns={"math_score_x": "9th", "math_score_y":"10th"})
math_scores_merged = pd.merge(math_scores_merged,math_11_df, how="left",on="school_name")
math_scores_merged = pd.merge(math_scores_merged,math_12_df, how="left",on="school_name")
math_scores_merged = math_scores_merged.rename(columns={"math_score_x": "11th", "math_score_y":"12th"})

math_scores_merged


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[7]:


#Create a pandas series for each grade with the average reading score by school
read_9_df = grade_9.groupby("school_name")["reading_score"].mean()
read_10_df = grade_10.groupby("school_name")["reading_score"].mean()
read_11_df = grade_11.groupby("school_name")["reading_score"].mean()
read_12_df = grade_12.groupby("school_name")["reading_score"].mean()

#Merge all the grades into a single dataframe
read_scores_merged = pd.merge(read_9_df,read_10_df, how="left",on="school_name")
read_scores_merged = read_scores_merged.rename(columns={"reading_score_x": "9th", "reading_score_y":"10th"})
read_scores_merged = pd.merge(read_scores_merged,read_11_df, how="left",on="school_name")
read_scores_merged = pd.merge(read_scores_merged,read_12_df, how="left",on="school_name")
read_scores_merged = read_scores_merged.rename(columns={"reading_score_x": "11th", "reading_score_y":"12th"})

read_scores_merged


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[18]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[21]:


#Create a new dataframe based on the school summary dataframe and cut it into bins based on spending and then display the average grade information
spending_df_vals = ssummary_df
#Get rid of formatting '$' and ',' and cast as floats
spending_df_vals["Per Student Budget"] = ssummary_df["Per Student Budget"].replace('[\$,]', '', regex=True).astype(float)
spending_df_vals["Spending Ranges"] = pd.cut(spending_df_vals["Per Student Budget"], spending_bins, labels=group_names)
spending_df_vals = spending_df_vals.set_index("Spending Ranges")
spending_df_vals = spending_df_vals.groupby("Spending Ranges").mean()
spending_df_vals = spending_df_vals[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"]]

spending_df_vals


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[10]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[11]:


#Create a new dataframe based on the school summary dataframe and cut it into bins based on school size and then display the average grade information
size_df = ssummary_df
size_df["School Size"] = pd.cut(size_df["Total Students"], size_bins, labels=group_names)
size_df = size_df.set_index("School Size")
size_df = size_df.groupby("School Size").mean()
size_df = size_df[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"]]
size_df


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[12]:


#Create a new dataframe based on the school summary dataframe and group it by school type and then display the average grade information
type_df = ssummary_df
type_df = type_df.set_index("School Type")
type_df = type_df.groupby("School Type").mean()
type_df = type_df[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"]]
type_df


# In[ ]:





# In[ ]:




