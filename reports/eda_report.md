Exploratory Data Analysis Report

 Dataset Overview

The BBC Full Text Document Classification Dataset contains
2,225 news articles collected from BBC News during 2004–2005.

The dataset contains two main columns:

- data: Full text of news articles.
- labels: News category.

There are five classification categories:

- Business
- Entertainment
- Politics
- Sport
- Tech

 Dataset Structure

- Original number of articles: 2,225
- Number of categories: 5
- Language: English
- Data format: CSV

After removing duplicate records:

- Remaining articles: 2,126
- Duplicate records removed: 99

 Missing Values

No missing values were found in the original dataset.

 Class Distribution

The category distribution is:

| Category | Percentage |
|---|---:|
| Sport | 23.75% |
| Business | 23.66% |
| Politics | 18.96% |
| Entertainment | 17.36% |
| Tech | 16.27% |

The dataset is relatively balanced across the five categories.

 Article Length Analysis

Word count was calculated for each article.

The analysis showed that article lengths vary across the dataset.

A histogram was used to visualize article length distribution.

A bar plot was also used to compare average article length
across different categories.

 Main Findings

- The dataset contains five news categories.
- No missing values were identified.
- 99 duplicate records were removed.
- The class distribution is relatively balanced.
- Article lengths vary across news categories.

 Conclusion

The dataset is suitable for multi-class news classification.

The duplicate records were removed before model training.

The dataset was then prepared for text preprocessing
and machine learning experiments.