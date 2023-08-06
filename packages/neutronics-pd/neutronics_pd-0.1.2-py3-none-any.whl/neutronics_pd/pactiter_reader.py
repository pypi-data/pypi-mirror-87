import pandas as pd
import re

tranlate_cols={
    'calcul':'title',
    'JEPPrel':'time_rel',
    'JEPPabs':'time_abs',
    'cycl':'cycle',
    'ND':'data_cat',
    'NR':'reg_id',
    'libelle donnee':'data_label',
    'total 2':'total_per_unit',
    'Tfluid':'water_temp',
    'Tparoi':'wall_temp',
    'DDD':'dose_rate',
    'DEPOT':'deposition'
}

def translate_data_label(series):
    translate_data_label_dict={
        'Concent. paroi':'wall_concentration', 
        'Masse Depots':'mass_deposition', 
        'Masse Oxyde':'mass_oxide', 
        'Relachement':'release',
        'Crud (%)':'crud_percentage', 
        'Rela. total':'total_release', 
        '% particulation':'particulation_percentage', 
        'Total Depot':'total_deposition', 
        'Bilan matiere':'material_balance',
        'Act. Depot':'deposited_activity',
        'Act. Oxyde':'oxide_activity',
        'Act. Totale':'total_activity',
        'A.Suspension':'suspension_activity',   
        'A.Solution':'solution_activity',    
        'A.Eau':'water_activity',
        'A.Totale Ss flu':'total_activity_under_flux',
        'A.Depot  Ss flu':'deposited_activity_under_flux',
        'A.Totale Hs flu':'total_activity_out_flux',
        'A.Totale RCV':'total_activity_rcv',
        'A.FILTRES':'filters_activity',
        'A.RESINES':'resines_activity',
        'Act. Specifique':'specific_activity',
        'Cte Dï¿½pot App.':'cte_deposition_app',
        'cte_d‚pot_app':'cte_deposition_app'
    }
    return translate_data_label_dict.get(series.strip(), series.strip().lower().replace(' ','_'))
    
class PactiterOuput:
   

    def __init__(self, inputfile):
        self.input_file=inputfile
        self.df_dict = self.read_pactiter_output(inputfile)
        self.t1=self.df_dict['T1']
        self.t2=self.df_dict['T2']
        self.t3=self.df_dict['T3']
        self.t4=self.df_dict['T4']
        self.t5=self.df_dict['T5']
        self.t6=self.df_dict['T6']
        self.df=self.merge_results()
        


    def read_pactiter_output(self, inputfile):
        with open(inputfile, errors='ignore') as f:
            lines=f.readlines()
        lista1=[]
        for l in lines:
            if '$T0' in l:
                lista1.append([l])
            elif lista1:
                if re.search('\x0c',l):
                    lista1.append([l])
                elif re.search('T\d \|calcul |\$T\d',l): 
                    lista1[-1].append(l.strip())

        title=lista1[0][0].strip().split('|')[1]
        description=lista1[0][0].strip().split('|')[2]

        table_dict={}
        for table in lista1[1:]:  
            id_table=table[1:][0].split('|')[0][1:].strip()
            if id_table in table_dict.keys():
                tab_lines=[l.strip().split('|')[1:] for l in table[1:]]
                if id_table in ('T5'):
                    
                    for line in tab_lines[1:]:
                        line[1]=str(float(line[1])/10)
                        line[2]=str(float(line[2])/10)
                table_dict[id_table][1]+=tab_lines
            else:
                header=table[1:][0].split('|')
                if id_table in ('T1','T2','T3'):
                    a, b = header.index('JEPPrel'), header.index('JEPPabs')
                    header[b], header[a] = header[a], header[b]
                tab_lines=[l.split('|')[1:] for l in table[2:]]
                

                columns = [tranlate_cols.get(column.strip(), column.strip().lower()) for column in header[1:]]
                table_dict[id_table]=[columns, tab_lines]
                

        df_dict={}
        for k in table_dict.keys():
            columns=table_dict[k][0]
            rows=table_dict[k][1]
            if k in ['T2', 'T3']:
                rows=[(row[:-1]) for row in rows]
            df=pd.DataFrame(rows, columns=columns).apply(pd.to_numeric, errors='ignore')
            df_obj = df.select_dtypes(['object'])
            df[df_obj.columns] = df_obj.applymap(translate_data_label)
            #df['table_id']=k
            df_dict[k]=df


        return df_dict

  

    def merge_results(self):
        df_dict=self.df_dict
        var_col1=['title','time_abs','time_rel','data_cat','reg_id','data_label','reg']
        t1=pd.melt(df_dict['T1'], id_vars=var_col1, value_vars=df_dict['T1'].columns[7:], var_name='variable', value_name='result')
        t2=pd.melt(df_dict['T2'], id_vars=var_col1, value_vars=df_dict['T2'].columns[7:], var_name='variable', value_name='result')
        t3=pd.melt(df_dict['T3'], id_vars=var_col1, value_vars=df_dict['T3'].columns[7:], var_name='variable', value_name='result')
        df_dict['T4'].insert(3,'data_cat',99)
        df_dict['T4'].insert(5,'data_label','T4')
        df_dict['T4'].drop('torig', axis=1, inplace=True)
        #t5=df_dict['T5']
        #t6=df_dict['T6']
        t4=pd.melt(df_dict['T4'], id_vars=var_col1, value_vars=df_dict['T4'].columns[7:], var_name='variable', value_name='result')
        df=pd.concat([t1,t2,t3,t4], ignore_index=True, sort=False)
        #df=pd.merge(df,t5, on=['title','reg','reg_id','time_abs','time_rel'])
        #df=pd.merge(df,t6, on=['title','time_abs','time_rel'])
        df['reg_id']=df['reg_id'].astype(int).astype(str)
        df['data_cat']=df['data_cat'].astype(int).astype(str)
        df.loc[(df['data_cat']==5) | (df['data_cat']==15),'reg_id']='global'
        df.loc[(df['data_cat']==5) | (df['data_cat']==15),'reg']='global'
        df['result']=df['result'].replace('********',0).astype(float)
        df['input_file']=self.input_file
        
        return df


        

  

        
        

def read_pactiter_output(inputfile):
    inp=PactiterOuput(inputfile)
    return inp.df 

def read_pactiter_t5(inputfile):
    inp=PactiterOuput(inputfile)
    return inp.t5 

def read_pactiter_t6(inputfile):
    inp=PactiterOuput(inputfile)
    return inp.t6

def read_pactiter_tables(inputfile):
    inp=PactiterOuput(inputfile)
    return inp.df_dict

def read_pactiter_activity_output(inputfile):
    inp=PactiterOuput(inputfile)
    var_col1=['title','time_abs','time_rel','data_cat','reg_id','reg','data_label']
    t2=pd.melt(inp.t2, id_vars=var_col1, value_vars=inp.t2.columns[7:], var_name='nuclide', value_name='result')
    t3=pd.melt(inp.t3, id_vars=var_col1, value_vars=inp.t3.columns[7:], var_name='nuclide', value_name='result')
    df=pd.concat([t2,t3], ignore_index=True)
    df['result']=df['result'].replace('********',0).astype(float)
    df['region']=df['reg'].replace('','global')
    df=df[['title','time_abs','region','data_label', 'nuclide', 'result']]
    df['input_file']=inputfile
    df=df.rename(columns={'time_abs':'time'})
    return df

def read_pactiter_mass_output(inputfile):
    inp=PactiterOuput(inputfile)
    var_col1=['title','time_abs','time_rel','data_cat','reg_id','data_label','reg','total', 'total_per_unit']
    df=pd.melt(inp.t1, id_vars=var_col1, value_vars=inp.t1.columns[7:inp.t1.columns.get_loc("total")], var_name='element', value_name='result')
    df['region']=df['reg'].replace('','global')
    df['result']=df['result'].replace('********',0).astype(float)
    df=df[['title','time_abs','region','data_label','element','result','total', 'total_per_unit']]
    df['input_file']=inputfile
    df=df.rename(columns={'time_abs':'time'})
    return df

def specific_activity_base_metal(inputfile, time=None, region=None):
    df_input=read_pactiter_activity_output(inputfile)
    df=df_input.loc[(df_input['data_label']=='specific_activity')]
    mask_df=df.groupby(['time','region'])['result'].sum().reset_index()
    mask_df=mask_df.loc[mask_df['result']!=0,['time','region']].reset_index(drop=True)
    df=df.merge(mask_df, on=['time','region'])
    df=df[['time','region','nuclide','result']].reset_index(drop=True)
    if time:
        df=df.loc[df['time']==time].reset_index(drop=True)
    if region:
        df=df.loc[df['region']==region].reset_index(drop=True)
    return df
