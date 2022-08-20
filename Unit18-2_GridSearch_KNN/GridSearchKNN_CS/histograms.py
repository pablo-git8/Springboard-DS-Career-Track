def histograms(df, column, color='blue'):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,5))
    plt.hist(df[column], color=color)
    plt.title('{} in diabetes_data'.format(column))
    plt.xlabel('{}'.format(column))
    plt.ylabel('Counts')
    plt.show()