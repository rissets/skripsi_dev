# filename: bar_chart.py

import matplotlib.pyplot as plt

# Define the domains and the number of papers in each domain
domains = ['Text Classification', 'NLP - Varying Data Sizes', 'Instruction Following', 'NLP & Computer Vision', 'NLP - Privacy']
num_papers = [1, 1, 1, 1, 1]

# Create a bar chart
plt.bar(domains, num_papers)
plt.xlabel('Domains')
plt.ylabel('Number of Papers')
plt.title('Number of Papers in Each Domain')
plt.xticks(rotation=90)

# Save the figure to a file
plt.savefig('bar_chart.png', bbox_inches='tight')