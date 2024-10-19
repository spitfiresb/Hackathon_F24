import pandas as pd
import re

df = pd.read_csv('your_file.csv', header=None)

# # Sample data in a DataFrame
# data = {
#     'Course': [
#         "ANTH 471.   ,Zooarchaeology: [Topic].  4 Credits.                                              ,Analysis and interpretation of bone and shell animal remains from archaeological sites. Repeatable once for a maximum of 8 credits when the topic changes.Requisites:Prereq:ANTH 145orANTH 150.Repeatable 1 time for a maximum of 8 credits when topic changes, None",
#         "ANTH 472.   ,Primate Conservation Biology.  4 Credits.                                         ,\"Evaluates the conservation status of the order Primates. Explores biological-ecological issues and social-cultural influences on primate biodiversity, distribution, and abundance.Requisites:Prereq:ANTH 171orANTH 270.\", None",
#         "ANTH 473.   ,Advanced Forensic Anthropology.  4 Credits.                                       ,\"Teaches theory and analysis of human remains for medico-legal professionals, including estimating biological parameters from skeletons and outdoor crime scene processing and testimony.Requisites:Prereq:ANTH 176with a grade of B– or better orANTH 366with a C– or better.\", None",
#         "ANTH 475.   ,Regarding Remains.  4 Credits.                                                    ,\"This course covers the policies and regulations of human and non-human remains in biological anthropology and forensic sciences contexts. It explores the considerations important for establishing, building, maintaining and working with skeletal collections.Requisites:Prereq:ANTH 176.\", None",
#         "ANTH 479.   ,\"  Taphonomy: Bones, Bugs, and Burials.  4 Credits.\"                              ,\"Application of taphonomic studies in the fields of paleontology, archaeology, and forensic-medicolegal anthropology.Requisites:Prereq: one fromANTH 170,ANTH 176,ANTH 270,ANTH 366,BI 212, or equivalent.\", None"
#     ]
# }

# df = pd.DataFrame(data)

# Function to extract prerequisites from DataFrame
def extract_prerequisites_from_df(df):
    prereqs_list = []
    
    for index, row in df.iterrows():
        # Use regex to find text after "Prereq:"
        match = re.search(r'Prereq:(.*?)\.?$', row['Course'])
        if match:
            # Clean up and split the prerequisites
            prereq_str = match.group(1).strip()
            # Split by 'or' and clean spaces
            prereq_list = [prereq.strip() for prereq in re.split(r'\bor\b', prereq_str)]
            prereqs_list.append(prereq_list)
        else:
            prereqs_list.append([])  # Append an empty list if no prerequisites are found
            
    return prereqs_list

# Get the extracted prerequisites
prerequisites = extract_prerequisites_from_df(df)

# Add the prerequisites back to the DataFrame
df['Prerequisites'] = prerequisites

# Print the DataFrame with extracted prerequisites
print(df[['Course', 'Prerequisites']])