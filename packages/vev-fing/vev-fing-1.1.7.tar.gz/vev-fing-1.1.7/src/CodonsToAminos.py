import pandas as pd


def codonsToAminos(df):
    df_a = pd.DataFrame(
        columns=['Position', 'K', 'N', 'T', 'R', 'S', 'I', 'M', 'Q', 'H', 'P', 'L', 'E', 'D', 'A', 'G', 'V', '*', 'Y',
                 'C', 'W', 'F', 'Passage', 'Strain', 'Repetition'])
    df_a['Position'] = df.Position
    df_a['Passage'] = df.Passage
    df_a['Strain'] = df.Strain
    df_a['Repetition'] = df.Repetition
    df_a['K'] = df.AAA + df.AAG
    df_a['N'] = df.AAC + df.AAT
    df_a['T'] = df.ACA + df.ACC + df.ACG + df.ACT
    df_a['R'] = df.AGA + df.AGG + df.CGA + df.CGC + df.CGG + df.CGT
    df_a['S'] = df.AGC + df.AGT + df.TCA + df.TCC + df.TCG + df.TCT
    df_a['I'] = df.ATA + df.ATC + df.ATT
    df_a['M'] = df.ATG
    df_a['Q'] = df.CAA + df.CAG
    df_a['H'] = df.CAC + df.CAT
    df_a['P'] = df.CCA + df.CCC + df.CCG + df.CCT
    df_a['L'] = df.CTA + df.CTC + df.CTG + df.CTT + df.TTA + df.TTG
    df_a['E'] = df.GAA + df.GAG
    df_a['D'] = df.GAC + df.GAT
    df_a['A'] = df.GCA + df.GCC + df.GCG + df.GCT
    df_a['G'] = df.GGA + df.GGC + df.GGG + df.GGT
    df_a['V'] = df.GTA + df.GTC + df.GTG + df.GTT
    df_a['*'] = df.TAA + df.TAG + df.TGA
    df_a['Y'] = df.TAC + df.TAT
    df_a['C'] = df.TGC + df.TGT
    df_a['W'] = df.TGG
    df_a['F'] = df.TTC + df.TTT
    return df_a
