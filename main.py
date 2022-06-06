import helpers as h
import streamlit as st


def main():
    """
    Main function performs:
    1.) Bloom filter iniziaization and used to count distinct on multiple bloom filter sizes
    2.) Flajolet–Martin algorithm count distinct
    :return:
    """

    df = h.load_dataset('diabetic_data.csv')
    print("Size of dataset: ", len(df))
    for column in df.columns:
        print('ATTRIBUTE: ', column, 'NUMBER OF DISTINCT VALUES: ', df[column].nunique())
    bloom_filter = h.generate_bloom_filter(10000)
    patient_nbrs = df['patient_nbr']

    # lets count the number of distinct values using the bloom filter
    sizes = [100, 1000, 10000, 100000, 1000000, 10000000]
    patients = df['patient_nbr']
    print('Actual distinct: ', patients.nunique())
    for size in sizes:
        distinct = 0
        bloom_filter = h.generate_bloom_filter(size)
        for patient_number in patients:
            if h.query_bloom_filter(bloom_filter, patient_number) == 'miss':
                distinct += 1
                bloom_filter = h.insert_into_bloom_filter(bloom_filter, patient_number)
        print('Size: ', size)
        print('Distinct predicted: ', distinct)

    print('Flajolet–Martin algorithm')
    h.perform_flajolet_martin_algorithm(patients)

    print('lets start streamlit')
    st.title('Bloom filter and Flajolet-Martin algorithm')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
