import numpy as np
import re
import pandas as pd
from collections import OrderedDict
from pathlib import Path
import os
from .mctal_reader import read_mctal
from .fispact_tools import read_fispact_output


DECAY_STRING='''25    55    102    1.0000E+09    Mn56
26    56    103    1.0000E+09    Mn56
28    58    16     1.0025E+09    Ni57 O
28    58    103    1.0050E+09    Co58+Co58m CC
27    59    16     1.0050E+09    Co58+Co58m CC
28    64    102    1.0075E+09    Ni65 O
29    65    103    1.0075E+09    Ni65
28    60    103    1.0125E+09    Co60+Co60m CC
27    59    102    1.0125E+09    Co60+Co60m CC
28    61    28     1.0125E+09    Co60+Co60m CC
28    61    104    1.0125E+09    Co60+Co60m CC
29    63    107    1.0125E+09    Co60+Co60m CC
28    58    28     1.0150E+09    Co57 O
28    58    104    1.0150E+09    Co57 O
24    50    102    1.0200E+09    Cr51
24    52    16     1.0200E+09    Cr51
47    107   16     1.0225E+09    Ag106 O
47    109   102    1.0250E+09    Ag110m O
13    27    107    1.0275E+09    Na24 CC
11    23    102    1.0275E+09    Na24
29    63    102    1.0300E+09    Cu64
29    65    16     1.0300E+09    Cu64
29    63    16     1.0325E+09    Cu62
29    65    107    1.0350E+09    Co62m O
28    62    103    1.0350E+09    Co62m O
9     19    6      1.0375E+09    F18 O 
9     19    46     1.0375E+09    F18 O
17    37    102    1.0400E+09    Cl38 O
41    93    102    1.0425E+09    Nb94 O
28    61    103    1.0450E+09    Co61 O
28    62    104    1.0450E+09    Co61 O
28    62    28     1.0450E+09    Co61 O
41    93    16     1.0475E+09    Nb92m CC
28    58    107    1.0500E+09    Fe55
26    56    16     1.0500E+09    Fe55 O
12    24    103    1.0275E+09    Na24 SS-CC
26    58    102    1.0550E+09    Fe59
25    55    16     1.0575E+09    Mn54
26    54    103    1.0575E+09    Mn54
22    48    103    1.0625E+09    Sc48
17    35    16     1.0650E+09    Cl34 O
17    35    107    1.0675E+09    P32 O
31    71    102    1.0700E+09    Ga72 O
31    71    16     1.0725E+09    Ga70 O
31    69    102    1.0725E+09    Ga70 O
31    69    16     1.0750E+09    Ga68 O
33    75    102    1.0775E+09    As76 O
33    75    16     1.0800E+09    As74 O
40    94    102    1.0825E+09    Zr95 O
40    96    16     1.0825E+09    Zr95 O
73    181   102    1.0840e+09    Ta182
22    46    103    1.0850e+09    Sc46 NN CC
22    47    28     1.0850e+09    Sc46 NN CC
22    47    104    1.0850e+09    Sc46 NN CC
22    47    103    1.0875e+09    Sc47 NN 
22    48    28     1.0875e+09    Sc47 NN 
22    48    104    1.0875e+09    Sc47 NN
22    46    16     1.0900e+09    Ti45 NN
8     16    103    1.0925E+09    N16 NN
20    46    102    1.0950E+09    Ca47 NN
20    48    16     1.0950E+09    Ca47 NN
23    51    107    1.0625E+09    Sc48 NN 
26    54    107    1.0200E+09    Cr51 N 
26    56    105    1.0575E+09    Mn54 N
26    57    28     1.0000E+09    Mn56 N
26    57    104    1.0000E+09    Mn56 N
26    58    105    1.0000E+09    Mn56 N
27    59    107    1.0000E+09    Mn56 N
27    59    103    1.0550E+09    Fe59 N
28    62    107    1.0550E+09    Fe59 N
29    65    102    1.1000E+09    Cu66 O
42    92    103    1.0475E+09    Nb92m CC
42    92    107    1.1025E+09    Zr89 NN CC
42    96    103    1.1050E+09    Nb96 NN
42    98    102    1.1075E+09    Mo99+Tc99m NN
42    100   16     1.1075E+09    Mo99+Tc99m NN
74    182   103    1.0840e+09    Ta182 N
74    186   102    1.1100E+09    W187 NN
82    204   16     1.1125E+09    Pb203'''


PIKMT='''pikmt
c
        8016.99         0          $    103
        11023.99         0          $    102
        13027.99         0          $    107
        12014.99         0          $   103
        20046.99         0         $    102
        20048.99         0         $     16
        22046.99         0         $ 16 103
        22047.99         0         $ 103 28 104
        22048.99         0         $ 103 28 104
        23051.99         0         $ 107
        24050.99         0         $    102
        24052.99         0         $     16
        25055.99         0         $    102, 16
        26054.99         0         $ 103 107
        26056.99         0         $ 103 105
        26057.99         0         $ 28 104
        26058.99         0         $ 102 105
        27059.99         0         $ 16 102 103 107
        28058.99         0         $ 16, 103
        28060.99         0         $ 103
        28061.99         0         $ 28, 104
        28062.39         0         $ 107
        29063.99         0         $ 102, 107, 16
        29065.99         0         $ 16, 102, 103
        41093.99         0         $ 316 XX
        42092.99         0         $  403 XX, 107
        42096.99         0         $  103
        42098.99         0         $  102
        42100.99         0         $  16
        73181.99         0         $  102
        74182.99         0         $  103
        74186.99         0         $  102
        82204.99         0         $  16
C       old
c        47107.39         0         $  16
        47109.39         0         $  102
c         9019.39         0         $ 6,46
c        17035.39         0         $ 16,107
c        31071.39         0         $ 16,102
c        31069.39         0         $ 16,102
c        33075.39         0         $ 16,102
        40094.39         0         $ 102
        40096.39         0         $ 16 '''

def nuclides_dict_list(decay_string):
    list_nuclides=[]
    dict_ts={}
    for l in decay_string.splitlines():
        ts=float(l.split()[3])
        nuclide_i=l.split()[4]
        nuclides= nuclide_i.split('+')
        for nuclide in nuclides:
            dict_ts[nuclide]=ts
        list_nuclides.append(nuclide_i)
    return list_nuclides, dict_ts

def change_mat_library(inputfile, outputfile, pikmt=PIKMT):
    pikmt_list=[]
    start=''
    for l in pikmt.splitlines():
        if start:
            if l.split()[0]!='c' and l.split()[0]!='C':
                if re.match(r'\S', l):
                    break
                pikmt_list.append(l.split()[0])
            else:
                pass
        else:
            if 'pikmt' in l:
                start=1

    pikmt_dct={}
    for i in pikmt_list:
        key= i.split('.')[0]
        pikmt_dct[key]=i+'c'

    lines=[]
    with open(inputfile, 'r', encoding="utf-8", errors='ignore') as fid:
        start=0
        for line in fid:
            if start==2:
                line_split=line.split()
                for l in line_split:
                    if '.' in l:
                        key= l.split('.')[0]
                        if key in pikmt_dct.keys():
                            new_mat=pikmt_dct[key]
                            line=line.replace(l,str(new_mat))
            else:
                if line=='\n':
                    start +=1
            lines.append(line)
    if lines[-1]=='\n':
        del lines[-1]
    lines+=pikmt.splitlines()
    lines=[l.replace('\n','') for l in lines]
    lines='\n'.join(lines)
    with open(outputfile, 'w') as fid:
        fid.write(lines)

def correction_factors_calc(fisp_irradiation, fisp_1s, neutron_yield, spectra_name, decay_string=DECAY_STRING):    
    df=read_fispact_output(fisp_irradiation).get_cooling_phase()
    df1s=read_fispact_output(fisp_1s).get_cooling_phase()
    cooling_times=df['time'].unique()
    nuclides_ts=nuclides_dict_list(decay_string)[1]
    
    nuclides=[]
    
    for time in cooling_times:
        activity_df=df.loc[df['time']==time, ['time_label','nuclide','activity']]
        atoms_df=df1s.loc[df1s['time']==1, ['nuclide','atoms']]
        time_label=activity_df['time_label'].unique()[0]
        for nuclide, time_shake in nuclides_ts.items():
            activity=0 if activity_df.loc[activity_df['nuclide']==nuclide,'activity'].empty else activity_df.loc[activity_df['nuclide']==nuclide,'activity'].values[0] 
            atoms=0 if atoms_df.loc[atoms_df['nuclide']==nuclide,'atoms'].empty else atoms_df.loc[atoms_df['nuclide']==nuclide,'atoms'].values[0]
            
            nuclides.append([time, time_label, time_shake, nuclide, activity, atoms])
    D1S_df=pd.DataFrame(nuclides,columns=['time','time_label','time_shake_cf','nuclide','activity','atom'])
    
    D1S_df=D1S_df.groupby(['time','time_label','time_shake_cf']).agg({'nuclide':'+'.join,'activity':'sum','atom':'sum'}).reset_index()
    
    D1S_df['correction_factor']=(neutron_yield*D1S_df['activity']/D1S_df['atom']).replace(0,1).replace(np.inf,1).fillna(1)
    D1S_df['spectra_name']=spectra_name
    return D1S_df

def correction_factors(input_list, dir_path, safety_factor=1, unit_conversion=0.0036, decay_string=DECAY_STRING):
    nuclides_order=nuclides_dict_list(decay_string)[0]
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    results=[]
    for i in input_list:
        fisp_irradiation=i[0]
        fisp_1s=i[1]
        neutron_yield=i[2]
        spectra_name=i[3]
        results.append(correction_factors_calc(fisp_irradiation, fisp_1s, neutron_yield, spectra_name, decay_string=decay_string))
    
    df = pd.concat(results, ignore_index=True)
    df.to_csv(dir_path+'/correction_factors.csv', index=False)
    cooling_time=df['time_label'].unique()
    len_spectra_name=len(df['spectra_name'].unique())
    df_list=list(df.groupby('time'))
    if len_spectra_name==1:
        for i, ct in enumerate(df_list):
            cooling_time=str(i+1)+'_'+ct[1]['time_label'].unique()[0].replace(' ','_')
            ct_df=ct[1][['correction_factor','nuclide']]
            ct_df['correction_factor']=ct_df['correction_factor']*safety_factor*unit_conversion
            ct_df=ct_df.rename(columns={"correction_factor": "correction_factor_1"})
            ct_df['correction_factor_2']=ct_df['correction_factor_1']
            ct_df=ct_df.set_index('nuclide').reindex(nuclides_order).fillna(1).reset_index()[['correction_factor_1','correction_factor_2','nuclide']]
            ct_file= ct_df.to_csv(sep='\t', header=None, index=False, float_format='%.4E').replace('\t','    ')
            ct_file=[i.replace('\n','') for i in ct_file.splitlines()]
            ct_file='\n'.join(ct_file)
            file_name=dir_path+'/'+cooling_time
            with open(file_name,'w') as f:
                f.write(ct_file)
    elif len_spectra_name==2:
        for i, ct in enumerate(df_list):
            cooling_time=str(i+1)+'_'+ct[1]['time_label'].unique()[0].replace(' ','_')
            ct_df=ct[1].pivot_table(index='nuclide', columns='spectra_name', values='correction_factor', aggfunc='max')
            ct_df.columns=['correction_factor_'+str(k+1) for k,i in enumerate(ct_df.columns.values)]
            ct_df['correction_factor_1']=ct_df['correction_factor_1']*safety_factor*unit_conversion
            ct_df['correction_factor_2']=ct_df['correction_factor_2']*safety_factor*unit_conversion
            ct_df=ct_df.reindex(nuclides_order).fillna(1).reset_index()[['correction_factor_1','correction_factor_2','nuclide']]
            ct_file=ct_df.to_csv(sep='\t', header=None, index=False, float_format='%.4E').replace('\t','    ')          
            ct_file=[i.replace('\n','') for i in ct_file.splitlines()]
            ct_file='\n'.join(ct_file)
            file_name=dir_path+'/'+cooling_time
            with open(file_name,'w') as f:
                f.write(ct_file)
    else:
        print('Please respect the input format!')
        return None
    
    ct_df.loc[:,'correction_factor_1']=1.0
    ct_df.loc[:,'correction_factor_2']=1.0
    ct_file=ct_df[['correction_factor_1','correction_factor_2','nuclide']].to_csv(sep='\t', header=None, index=False, float_format='%.4E').replace('\t','    ')
    ct_file=[i.replace('\n','') for i in ct_file.splitlines()]
    ct_file='\n'.join(ct_file)
    file_name=dir_path+'/cf_zero'
    with open(file_name,'w') as f:
        f.write(ct_file)

def apply_correction_factors(mctal_inputs, coords, correction_factors_csv, unit_conversion=1):
    df_corr_factors=pd.read_csv(correction_factors_csv)
    df_list=[]
    for name, inp in mctal_inputs: 
        mctal_df=read_mctal(inp)
        df_tally=mctal_df.get_results(**coords).sort_values(['cell','time_shake_ub'])
        corr_factors_df=df_corr_factors.loc[(df_corr_factors['spectra_name']==name),['time','time_label','time_shake_cf','nuclide','correction_factor']]

        ts_cf = corr_factors_df['time_shake_cf'].values
        ts_ub = df_tally['time_shake_ub'].values
        ts_lb = df_tally['time_shake_lb'].values

        i, j = np.where((ts_cf[:, None] >= ts_lb) & (ts_cf[:, None] <= ts_ub))

        df_spectra=pd.DataFrame(
            np.column_stack([corr_factors_df.values[i], df_tally.values[j]]),
            columns=corr_factors_df.columns.append(df_tally.columns)
        )
        df_spectra['spectra_name']=name
        df_list.append(df_spectra)
        
        
    df=pd.concat(df_list, ignore_index=True)
    
    df=df.rename(columns={'value':'mctal_value','relative_error':'mctal_relative_error'})

    df['value_nuclide_spectra']=df['mctal_value']*df['correction_factor']*unit_conversion
    df['relative_error_nuclide_spectra']=df['mctal_relative_error']

    df['absolute_error_quad']=(df['value_nuclide_spectra']*df['relative_error_nuclide_spectra'])**2    

    return df

def temporal_sdr_df(mctal_inputs, coords, correction_factors_csv, safety_factor=1, unit_conversion=1):
    df=apply_correction_factors(mctal_inputs, coords, correction_factors_csv, unit_conversion=unit_conversion)

    df['value_nuclide']=df.groupby(['cell','time_label','nuclide'])['value_nuclide_spectra'].transform('sum')
    df['relative_error_nuclide']=((df.groupby(['cell','time_label','nuclide'])['absolute_error_quad'].transform('sum'))**0.5)/df['value_nuclide']

    df['value_spectra']=df.groupby(['cell','spectra_name','time_label'])['value_nuclide_spectra'].transform('sum')
    df['relative_error_spectra']=((df.groupby(['cell','spectra_name','time_label'])['absolute_error_quad'].transform('sum'))**0.5)/df['value_spectra']
    
    df['value']=df.groupby(['cell','time_label'])['value_nuclide_spectra'].transform('sum')
    df['relative_error']=((df.groupby(['cell','time_label'])['absolute_error_quad'].transform('sum'))**0.5)/df['value']
    
    df['percentage_value_nuclide']=df['value_nuclide']/df['value']
    df=df.fillna(0)
    df=df.drop('absolute_error_quad', axis=1)
    df['safety_factor']=1
    if safety_factor!=1:
        df_copy=df.copy()
        df_copy['safety_factor']=safety_factor
        df_copy['value_nuclide_spectra']=df_copy['value_nuclide_spectra']*df_copy['safety_factor']
        df_copy['value_nuclide']=df_copy['value_nuclide']*df_copy['safety_factor']
        df_copy['value_spectra']=df_copy['value_spectra']*df_copy['safety_factor']
        df_copy['value']=df_copy['value']*df_copy['safety_factor']
        df=df.append(df_copy, ignore_index=True)

    return df

def sdr_total_excel_df(df):

    df_total1=df.loc[:,['cell','time_label','spectra_name','time','value_spectra','relative_error_spectra','value','relative_error','safety_factor']].drop_duplicates().reset_index(drop=True)
    spectra=df_total1['spectra_name'].unique()
    
    sfs=df.loc[df['safety_factor']!=1,'safety_factor'].unique()
    df_total=df_total1.loc[df_total1['safety_factor']==1]
    df_total=df_total.drop(['safety_factor'],axis=1)
    
    df_result=df_total[['cell','time_label','time']].drop_duplicates().reset_index(drop=True)
    for spectrum in spectra:
        value_col='value_'+spectrum
        error_col='relative_error_'+spectrum
        df_result[value_col]=df_total.loc[df_total['spectra_name']==spectrum,'value_spectra'].values
        for sf in sfs:
           df_sf=df_total1.loc[df_total1['safety_factor']==sf].reset_index(drop=True)
           value_col_sf=value_col+'_sf_'+str(sf)
           
           df_result[value_col_sf]=df_sf.loc[df_sf['spectra_name']==spectrum,'value_spectra'].values
        df_result[error_col]=df_total.loc[df_total['spectra_name']==spectrum,'relative_error_spectra'].values
    df_result['total_value']=df_total.loc[df_total['spectra_name']==spectrum,'value'].values
    for sf in sfs:
        df_sf=df_total1.loc[df_total1['safety_factor']==sf].reset_index(drop=True)
        value_col_sf='total_value_sf_'+str(sf)
        df_result[value_col_sf]=df_sf.loc[df_sf['spectra_name']==spectrum,'value'].values
    df_result['total_relative_error']=df_total.loc[df_total['spectra_name']==spectrum,'relative_error'].values
    if len(spectra)==1:
        spectrum=spectra[0]
        value_col='value_'+spectrum
        error_col='relative_error_'+spectrum
        col_list=[value_col,error_col]
        for sf in sfs:
            col_list.append(value_col+'_sf_'+str(sf))

        df_result=df_result.drop(col_list, axis=1)
    df_result['len_spectra']=len(spectra)
    return df_result

def sdr_dominant_nuclides_excel_df(df_input, sort_nuclide_by=['value_nuclide'], sort_nuclide_ascending=[False]):
    
    df=df_input.loc[:,~df_input.columns.isin(['time','cell'])]
    df=df.sort_values(sort_nuclide_by, ascending=sort_nuclide_ascending)
    spectra=df_input['spectra_name'].unique()

    sfs=df.loc[df['safety_factor']!=1,'safety_factor'].unique()
    df1=df.loc[df['safety_factor']==1].reset_index(drop=True)
    
    df_result=df1[['time_shake_cf','nuclide']].drop_duplicates().reset_index(drop=True)
    for spectrum in spectra:
        cf_col='correction_factor_'+spectrum
        df_result[cf_col]=df1.loc[df1['spectra_name']==spectrum,'correction_factor'].values
    for spectrum in spectra:
        mctal_col='mctal_value_'+spectrum
        value_col='value_'+spectrum
        error_col='relative_error_'+spectrum
        df_result[mctal_col]=df1.loc[df1['spectra_name']==spectrum,'mctal_value'].values
        df_result[value_col]=df1.loc[df1['spectra_name']==spectrum,'value_nuclide_spectra'].values
        for sf in sfs:
           df_sf=df.loc[df['safety_factor']==sf].reset_index(drop=True)
           value_col_sf=value_col+'_sf_'+str(sf)
           df_result[value_col_sf]=df_sf.loc[df_sf['spectra_name']==spectrum,'value_nuclide_spectra'].values
        df_result[error_col]=df1.loc[df1['spectra_name']==spectrum,'relative_error_nuclide_spectra'].values
       
        
    df_result['value_nuclide']=df1.loc[df1['spectra_name']==spectrum,'value_nuclide'].values
    for sf in sfs:
        df_sf=df.loc[df['safety_factor']==sf].reset_index(drop=True)
        df_result['value_nuclide_sf_'+str(sf)]=df_sf.loc[df_sf['spectra_name']==spectrum,'value_nuclide'].values
    df_result['relative_error_nuclide']=df1.loc[df1['spectra_name']==spectrum,'relative_error_nuclide'].values
    
    df_result['percentage_value_nuclide']=df1.loc[df1['spectra_name']==spectrum,'percentage_value_nuclide'].values
    for spectrum in spectra:
        value_col='value_'+spectrum
        error_col='relative_error_'+spectrum
        df_result.at['Total',value_col]=df1.loc[df1['spectra_name']==spectrum,'value_spectra'].unique()[0]
        df_result.at['Total',error_col]=df1.loc[df1['spectra_name']==spectrum,'relative_error_spectra'].unique()[0]
        for sf in sfs:
            value_col_sf=value_col+'_sf_'+str(sf)
            df_sf=df.loc[df['safety_factor']==sf].reset_index(drop=True)
            df_result.at['Total',value_col_sf]=df_sf.loc[df_sf['spectra_name']==spectrum,'value_spectra'].unique()[0]
    df_result.at['Total','value_nuclide']=df1.loc[df1['spectra_name']==spectrum,'value'].unique()[0]
    df_result.at['Total','relative_error_nuclide']=df1.loc[df1['spectra_name']==spectrum,'relative_error'].unique()[0]
    for sf in sfs:
        df_sf=df.loc[df['safety_factor']==sf].reset_index(drop=True)
        df_result.at['Total','value_nuclide_sf_'+str(sf)]=df_sf.loc[df_sf['spectra_name']==spectrum,'value'].unique()[0]

    if len(spectra)==1:
        spectrum=spectra[0]
        mctal_col='mctal_value_'+spectrum
        value_col='value_'+spectrum
        error_col='relative_error_'+spectrum
        col_list=[value_col,error_col]
        for sf in sfs:
            col_list.append(value_col+'_sf_'+str(sf))
        
        df_result=df_result.drop(col_list, axis=1).rename(columns={mctal_col:'mctal_value'})
        


    df_result['len_spectra']=len(spectra)
    df_result.loc[df_result.index[-1],'nuclide']='Total'
    return df_result

def sdr_excel_report(mctal_inputs, coords, correction_factors_csv, name, output_dir, safety_factor=1, unit_conversion=0.0036, all_columns=False, sort_nuclide_by=['value_nuclide'], sort_nuclide_ascending=[False]):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df=temporal_sdr_df(mctal_inputs, coords, correction_factors_csv,safety_factor, unit_conversion)
    df.to_csv(f'{output_dir}/sdr_calc_{name}.csv', index=None)
    df_total=sdr_total_excel_df(df)
    df_total=df_total.drop('len_spectra', axis=1)
    for cell, dfg in df.groupby('cell'):
        filename=f'{name}_{cell}.xlsx'
        path_file=output_dir+'/'+filename
        with pd.ExcelWriter(path_file) as writer:
            format1 = writer.book.add_format({'num_format': '0.000E+00'})
            format2 = writer.book.add_format({'num_format': '0.00%'})
            df_total_cell=df_total.loc[df_total['cell']==cell]
            df_total_cell=df_total_cell.drop('cell',axis=1)
            df_total_cell.to_excel(writer, sheet_name='MAIN table', index=None)
            worksheet = writer.sheets['MAIN table']
            len_col=len(df_total_cell.columns)
            worksheet.set_column(0,len_col-1, 20, format1)
            relative_error_cols=[df_total_cell.columns.get_loc(c) for c in df_total_cell.columns[df_total_cell.columns.str.contains('relative_error')]]
            for col in relative_error_cols:
                worksheet.set_column(col,col, 20, format2)
            for i, dft in dfg.groupby('time'):
                time_label=dft['time_label'].unique()[0]
                dftt=sdr_dominant_nuclides_excel_df(dft, sort_nuclide_by=sort_nuclide_by, sort_nuclide_ascending=sort_nuclide_ascending)
                dftt=dftt.drop('len_spectra', axis=1)
                if all_columns!=True:
                    cols_drop=['time_shake_cf']+dftt.columns[dftt.columns.str.contains('correction_factor|mctal_value')].tolist()
                    dftt=dftt.drop(cols_drop, axis=1)
                len_col=len(dftt.columns)
                dftt.to_excel(writer, sheet_name=time_label, index=None)
                worksheet = writer.sheets[time_label]
                worksheet.set_column(0,len_col-1, 20, format1)
                relative_error_cols=[dftt.columns.get_loc(c) for c in dftt.columns[dftt.columns.str.contains('relative_error')]]
                for col in relative_error_cols:
                    worksheet.set_column(col,col, 20, format2)

                percentage_cols=[dftt.columns.get_loc(c) for c in dftt.columns[dftt.columns.str.contains('percentage')]]
                for col in percentage_cols:
                    worksheet.set_column(col,col, 25, format2)



def decay_gamma_spectra_df(mctal_inputs, coords, correction_factors_csv, safety_factor=1, unit_conversion=1):
    df=apply_correction_factors(mctal_inputs, coords, correction_factors_csv, unit_conversion)

    df['value_spectra']=df.groupby(['cell','spectra_name','time_label','energy'])['value_nuclide_spectra'].transform('sum')
    df['value_spectra_per_energy']=df['value_spectra']/df['delta_energy_bin']
    df['relative_error_spectra']=((df.groupby(['cell','spectra_name','time_label','energy'])['absolute_error_quad'].transform('sum'))**0.5)/df['value_spectra']
    
    df['value']=df.groupby(['cell','time_label','energy'])['value_nuclide_spectra'].transform('sum')
    df['value_per_energy']=df['value']/df['delta_energy_bin']
    df['relative_error']=((df.groupby(['cell','time_label','energy'])['absolute_error_quad'].transform('sum'))**0.5)/df['value']
    
    
    df=df.fillna(0)
    df=df.drop('absolute_error_quad', axis=1)
    df['safety_factor']=1
    if safety_factor!=1:
        df_copy=df.copy()
        df_copy['safety_factor']=safety_factor
        df_copy['value_nuclide_spectra']=df_copy['value_nuclide_spectra']*df_copy['safety_factor']
        df_copy['value_spectra']=df_copy['value_spectra']*df_copy['safety_factor']
        df_copy['value']=df_copy['value']*df_copy['safety_factor']
        df_copy['value_spectra_per_energy']=df_copy['value_spectra_per_energy']*df_copy['safety_factor']
        df_copy['value_per_energy']=df_copy['value_per_energy']*df_copy['safety_factor']
        df=df.append(df_copy, ignore_index=True)

    return df

def decay_gamma_spectra_excel_df(df):
    spectra=df['spectra_name'].unique()

    sfs=df.loc[df['safety_factor']!=1,'safety_factor'].unique()

    df1=df.loc[df['safety_factor']==1].reset_index(drop=True)
    
    df_result=df1.loc[df1['spectra_name']==spectra[0], ['cell','time','time_label','energy','delta_energy_bin']]

    for spectrum in spectra:
        value_col='value_'+spectrum
        value_per_energy_col='value_per_energy_'+spectrum
        error_col='relative_error_'+spectrum

        df_result[value_col]=df1.loc[df1['spectra_name']==spectrum,'value_spectra'].values
        df_result[value_per_energy_col]=df1.loc[df1['spectra_name']==spectrum,'value_spectra_per_energy'].values
        for sf in sfs:
           df_sf=df.loc[df['safety_factor']==sf].reset_index(drop=True)
           value_col_sf=value_col+'_sf_'+str(sf)
           value_per_energy_col_sf=value_per_energy_col+'_sf_'+str(sf)
           df_result[value_col_sf]=df_sf.loc[df_sf['spectra_name']==spectrum,'value'].values
           df_result[value_per_energy_col_sf]=df_sf.loc[df_sf['spectra_name']==spectrum,'value_spectra_per_energy'].values
           

        df_result[error_col]=df1.loc[df1['spectra_name']==spectrum,'relative_error_spectra'].values

    df_result['result']=df1.loc[df1['spectra_name']==spectrum,'value'].values
    df_result['result_per_energy']=df1.loc[df1['spectra_name']==spectrum,'value_per_energy'].values
    for sf in sfs:
        df_sf=df.loc[df['safety_factor']==sf].reset_index(drop=True)
        df_result['result_sf_'+str(sf)]=df_sf.loc[df_sf['spectra_name']==spectrum,'value'].values
        df_result['result_per_energy_sf_'+str(sf)]=df_sf.loc[df_sf['spectra_name']==spectrum,'value_per_energy'].values
    df_result['relative_error']=df1.loc[df1['spectra_name']==spectrum,'relative_error'].values
    df_result=df_result.drop_duplicates()
    return df_result

def decay_gamma_spectra_excel_report(mctal_inputs, coords, correction_factors_csv, name, output_dir, safety_factor=1, unit_conversion=1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df=decay_gamma_spectra_df(mctal_inputs, coords, correction_factors_csv, safety_factor, unit_conversion)
    df.to_csv(f'{output_dir}/decay_gamma_spectra_{name}.csv', index=None)
    df_excel=decay_gamma_spectra_excel_df(df)

    for cell, dfg in df_excel.groupby('cell'):
        filename=f'decay_gamma_{name}_{cell}.xlsx'
        path_file=output_dir+'/'+filename
        with pd.ExcelWriter(path_file) as writer:
            format1 = writer.book.add_format({'num_format': '0.000E+00'})
            format2 = writer.book.add_format({'num_format': '0.00%'})
            for i, dft in dfg.groupby('time'):
                time_label=dft['time_label'].unique()[0]
                dftt=dft.drop(['cell','time','time_label'], axis=1)
                len_col=len(dftt.columns)
                dftt.to_excel(writer, sheet_name=time_label, index=None)
                worksheet = writer.sheets[time_label]
                worksheet.set_column(0,len_col-1, 25, format1)
                relative_error_cols=[dftt.columns.get_loc(c) for c in dftt.columns[dftt.columns.str.contains('relative_error')]]
                for col in relative_error_cols:
                    worksheet.set_column(col,col, 25, format2)
