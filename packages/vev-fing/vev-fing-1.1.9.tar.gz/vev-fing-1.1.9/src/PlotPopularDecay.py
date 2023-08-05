def plotPopularDecay(df):
    # gets values of the first passage
    minPassage = df['Passage'].min()

    passages = df['Passage'].unique()  # get passages

    info_df = str(df['info'].iloc[0])  # get info
    strain_df = info_df.split(',')[0]
    repetition_df = info_df.split(',')[1]

    posVal = df.Position.unique()  # get unique positions

    # look for the values of the probabilities for the first passage
    dfFirstPassage = df[df.Passage.eq(minPassage)]
    dfFirstPassage_val = dfFirstPassage[dfFirstPassage.Position.isin(posVal)].copy()
    dfFirstPassage_val_aux = dfFirstPassage_val.drop(
        ['Position', 'Coverage', 'Passage', 'Strain', 'Repetition', 'info'], axis=1)
    maxColumnsCodon = dfFirstPassage_val_aux.idxmax(axis=1)
    dfFirstPassage_val['MaxFreqCodon'] = maxColumnsCodon
    dfFirstPassage_val = dfFirstPassage_val[['Position', 'MaxFreqCodon']]
    return dfFirstPassage_val


    
    
    
