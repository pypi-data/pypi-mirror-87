import pandas as  pd
from decimal import Decimal
import re
#from mendeleev import element
#from periodictable import elements
pd.set_option('display.max_colwidth',10000)


def mendeleev_elements(ids):
    list_elements=['N', 'H', 'HE', 'LI', 'BE', 'B', 'C', 'N', 'O', 'F', 'NE', 'NA', 'MG', 'AL', 'SI', 'P', 'S', 'CL', 'AR', 'K', 'CA', 'SC', 'TI', 'V', 'CR', 'MN', 'FE', 'CO', 'NI', 'CU', 'ZN', 'GA', 'GE', 'AS', 'SE', 'BR', 'KR', 'RB', 'SR', 'Y', 'ZR', 'NB', 'MO', 'TC', 'RU', 'RH', 'PD', 'AG', 'CD', 'IN', 'SN', 'SB', 'TE', 'I', 'XE', 'CS', 'BA', 'LA', 'CE', 'PR', 'ND', 'PM', 'SM', 'EU', 'GD', 'TB', 'DY', 'HO', 'ER', 'TM', 'YB', 'LU', 'HF', 'TA', 'W', 'RE', 'OS', 'IR', 'PT', 'AU', 'HG', 'TL', 'PB', 'BI', 'PO', 'AT', 'RN', 'FR', 'RA', 'AC', 'TH', 'PA', 'U', 'NP', 'PU', 'AM', 'CM', 'BK', 'CF', 'ES', 'FM', 'MD', 'NO', 'LR', 'RF', 'DB', 'SG', 'BH', 'HS', 'MT', 'DS', 'RG', 'CN', 'NH', 'FL', 'MC', 'LV', 'TS', 'OG']
    return list_elements[ids]

def xround(num):
    working = str(num-int(num))
    for i, e in enumerate(working[2:]):
        if e != '0':
            return int(num) + float(working[:i+3])

def materials_df(inputfile):
    lines=[]
    with open(inputfile) as f:
        for line in f:
            if re.search(r'component nuclide, mass fraction', line):
                lines.append(line)
            elif lines:
                if re.search(r'warning',line) or re.search(r'print table 50',line):
                    break
                else:
                    lines.append(line)
    
    sections=[]
    for line in lines[2:]:
        line= line.replace(',','')
        split_line=line.split()
        if len(split_line) % 2 !=0:
            sections.append(split_line)
        elif sections:
            sections[-1] += split_line
    
    df_list=[]
    for section in sections:
        mat_id=section[0]
        nuclides=[]
        mass_fractions=[]
        nuclides+=section[1::2]
        mass_fractions+=section[2::2]
        df = pd.DataFrame({'zaid': nuclides, 'mass_fraction':mass_fractions})
        df['id']=mat_id
        df_list.append(df)
    df=pd.concat(df_list, ignore_index=True)
    df['mass_fraction']=pd.to_numeric(df['mass_fraction'])
    df['element']=df['zaid'].apply(lambda x: mendeleev_elements(int(x[:-3])))
    df=df[['id','element','zaid','mass_fraction']]
    return df

def extract_materials(inputfile):
    lines=[]
    with open(inputfile) as f:
        for line in f:
            if re.search(r'component nuclide, mass fraction', line):
                lines.append(line)
            elif lines:
                if re.search(r'warning',line) or re.search(r'print table 50',line):
                    break
                else:
                    lines.append(line)
    del lines[:2]
    sections=[]
    for line in lines:
        line= line.replace(',','')
        split_line=line.split()
        if len(split_line) % 2 !=0:
            sections.append(split_line)
        elif sections:
            sections[-1] += split_line
    
    dict_mat={}
    for section in sections:
        mat_id=section[0]
        nuclides=[]
        densities=[]
        nuclides+=section[1::2]
        densities+=section[2::2]
        df = pd.DataFrame({'Nuclides': nuclides, 'Densities':densities})
        df['Nuclides']=df['Nuclides'].apply(lambda x: mendeleev_elements(int(x[:-3])))
        df['Densities']=pd.to_numeric(df['Densities'])*100
        df=df.groupby('Nuclides')['Densities'].sum()
        df=df.round(decimals=4).astype(float)
        df2=df.loc[df!=df.max()]
        max_value=(100-df2.sum())
        df[df==df.max()]='{:.4f}'.format(round(max_value, 4)) 
        dict_mat[mat_id]=df
        
    mats_comp=[]
    for k, mat in dict_mat.items():
        lenght=len(mat)
        comp=mat.to_string(header=None)
        mats_comp.append([k,comp,lenght])
    composition_df=pd.DataFrame(mats_comp, columns=['mat_id','composition','len'])

    return composition_df