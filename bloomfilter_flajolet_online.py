import streamlit as st
import helpers
from PIL import Image
import numpy as np

"""
This file can be run to start the interactive webpage at http://localhost:8501/
"""

# Lets start using streamlit for the interactive web page

# Section 1.) Title and dataframe
st.title('Bloom filter and Flajolet-Martin algorithm')
st.write('Lets have a look at our dataset:')
st.dataframe(helpers.load_dataset('diabetic_data.csv'))
patients = helpers.load_dataset('diabetic_data.csv')['patient_nbr']
st.write('We will analyse the patients number of our dataset')
st.write('Our dataset has ', len(patients), ' rows.')
st.write('We actually have:', patients.nunique(), ' distinct patient numbers')

# Section 2 Bloomfilter with slider for bit size and query field
st.subheader('Bloomfilter')
image = Image.open('720px-Bloom_filter.svg.png')
st.image(image, caption='Image of an bloom filter and how it is used.')
st.write('Let us create an bloom filter together')
bloom_filter_bits = st.slider('How many bits should the bloom filter have?', 100, 10000000,1000 )
distinct = 0
bloom_filter = helpers.generate_bloom_filter(bloom_filter_bits)
for patient_number in patients:
    if helpers.query_bloom_filter(bloom_filter, patient_number) == 'miss':
        distinct += 1
        bloom_filter = helpers.insert_into_bloom_filter(bloom_filter, patient_number)
st.write('The bloom filter will need:', 0.0000001192 * bloom_filter_bits, ' mb of storage')
st.write('The bloom filter has ', bloom_filter_bits, ' bits and predicted', distinct, ' distinct values.')
st.write('This means we have ', patients.nunique() - distinct, ' false positive values!')

st.write('Now you can enter any value you like to check if it is in the bloom filter!')
query = st.text_input('Query value:', '')
check_bloomfilter = helpers.query_bloom_filter(bloom_filter,query)
df = helpers.load_dataset('diabetic_data.csv')
check_pandas = False
for patient in patients:
    if str(patient) == str(query):
        check_pandas = True

results_property = ''
if check_pandas:
    if check_bloomfilter == 'match':
        results_property = 'True positive'
    else:
        results_property = 'False negative'
else:
    if check_bloomfilter == 'match':
        results_property = 'False positive'
    else:
        results_property = 'True negative'
st.write('This query is an: ', helpers.query_bloom_filter(bloom_filter,query), ',', results_property)


# Section 3. Flajolet martin algorithm for chosen column
st.subheader('Flajolet-Martin algorithm')
st.write('Lets choose one attribute that we want to count distinct on with the flajolet martin algorithm!')
attribute = st.text_input('Attribute name:', '')
if attribute in df.columns:
    column = df[attribute]
    st.write('This column actually has', column.nunique(), 'distinct values.')
    flajo = helpers.perform_flajolet_martin_algorithm(column)
    hash_functions = ['hash_CRC32', 'hash_Adler32', 'hash_MD5', 'hash_SHA']
    st.write('The falojelt-martin algorithm predicted:')
    for i,hash_function in enumerate(hash_functions):
        st.write(hash_function,':' ,flajo[i])
    st.write('Average:' , np.mean(flajo))
else:
    st.write('Please enter a valid column header name.')

