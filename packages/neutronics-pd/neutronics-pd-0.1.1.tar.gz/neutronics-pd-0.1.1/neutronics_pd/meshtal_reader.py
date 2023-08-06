import pandas as pd
import numpy as np
import re

class MeshTalInfo:
    def __init__(self, section):
        self.name = section[1] 
        self.values = []
    def append(self, section):
        self.values.append(section)
        
class MeshTallyInfo:
    def __init__(self, section):
        self.name = 'Mesh Tally Number'
        self.section= section
        self.number= section[1].strip().split()[-1]
        self.comment='None'
        self.type=''.join(section[2:]).strip().replace('\n','')
        if re.match(r'^.*\s{2,}.*$',section[2]):
            self.comment=section[2].strip()
            self.type=''.join(section[3:]).strip().replace('\n','')
        self.tally_results=[]
        self.tally_bounds=''
        
    def append(self, subsect):
        self.tally_results.append(subsect)
        
    def append_bounds(self, subsect):
        self.tally_bounds=subsect

class MeshTallyBounds:
    def __init__(self, section):
        self.name = 'Tally bin boundaries'

        start = 3 if 'Cylinder' in section[2] else 2

        self.mesh_geom_type='CYL' if 'Cylinder' in section[2] else 'REC'
        self.i_name=section[start].split(':')[0].strip()
        self.j_name=section[start+1].split(':')[0].strip()
        self.k_name=section[start+2].split(':')[0].strip()
        i_b=section[start].split(':')[1].split()
        j_b=section[start+1].split(':')[1].split()
        k_b=section[start+2].split(':')[1].split()
        energy_b=section[start+3].split(':')[1].split()

        i_b=[np.float64(i) for i in i_b]
        j_b=[np.float64(j) for j in j_b]
        k_b=[np.float64(k) for k in k_b]
        energy_b=[np.float64(energy) for energy in energy_b]
        self.i_lb=i_b[:-1]
        self.i_ub=i_b[1:]
        self.j_lb=j_b[:-1]
        self.j_ub=j_b[1:]
        self.k_lb=k_b[:-1]
        self.k_ub=k_b[1:]
        
        
        self.energy_lb=energy_b[:-1]
        self.energy_ub=energy_b[1:]
        self.df_ib=pd.DataFrame({'I_lb':self.i_lb,'I_ub':self.i_ub})
        self.df_ib['I']=(self.df_ib['I_lb']+self.df_ib['I_ub'])/2
        self.df_jb=pd.DataFrame({'J_lb':self.j_lb,'J_ub':self.j_ub})
        self.df_jb['J']=(self.df_jb['J_lb']+self.df_jb['J_ub'])/2
        self.df_kb=pd.DataFrame({'K_lb':self.k_lb,'K_ub':self.k_ub})
        self.df_kb['K']=(self.df_kb['K_lb']+self.df_kb['K_ub'])/2
        self.df_energyb=pd.DataFrame({'energy_lb':self.energy_lb,'energy_ub':self.energy_ub,'energy':self.energy_ub})
        


class MeshTallyMatrixEnergyBounds:
    def __init__(self, section):
        self.name = 'Energy Bin'
        self.energy_bin_lb=0 if 'Total' in section[1] else np.float64(section[1].split()[2])
        self.energy_bin_ub=1e36 if 'Total' in section[1] else np.float64(section[1].split()[4])
        self.sons=[]
        self.plane={}
    def append(self, section):
        self.plane[section.coord_bin_ub]=section
        
class MeshTallyMatrixResult:
    def __init__(self, section):
        self.name = 'TallyMatrixResult'
        self.across_variable= section[1].split('(across)')[0].strip().split()[-1]
        self.down_variable= section[1].split('(down)')[0].strip().split()[-1]
        self.across_var_arr=section[2].split()
        self.across_var_arr=[np.float64(value) for value in self.across_var_arr]
        split_values=[line.split() for line in section[3:]]
        self.down_var_arr=[np.float64(values[0]) for values in split_values]
        self.result_array=np.array([values[1:] for values in split_values], np.float64).flatten()
        midx=pd.MultiIndex.from_product([self.down_var_arr, self.across_var_arr], names=['down','across'])
        self.df_results=pd.DataFrame(self.result_array, index=midx, columns=['result']).reset_index()
    

class MeshTallyMatrixError:
    def __init__(self, section):
        self.name = 'TallyMatrixRelativeErrors'
        self.across_var_arr=section[2].split()
        self.across_var_arr=[np.float64(value) for value in self.across_var_arr]
        split_values=[line.split() for line in section[3:]]
        self.down_var_arr=[np.float64(values[0]) for values in split_values]
        self.result_array=np.array([values[1:] for values in split_values], np.float64).flatten()
        midx=pd.MultiIndex.from_product([self.down_var_arr, self.across_var_arr], names=['down','across'])
        self.df_errors=pd.DataFrame(self.result_array, index=midx, columns=['relative_error']).reset_index()
   
        
class MeshTallyCoord:
    def __init__(self, section):
        self.name = 'third_coord_bin'
        self.coord_name=section[1].split()[0]
        self.coord_bin_lb=np.float64(section[1].split()[2])
        self.coord_bin_ub=np.float64(section[1].split()[4])
        self.coord_c=(self.coord_bin_lb+self.coord_bin_ub)/2
        self.sons=[]
    def append(self, section):
        self.sons.append(section)
        
class MeshTallyResColCf:
    def __init__(self, section):
        self.name = 'tally_results_col_cf'
        self.columns = section[1].replace('Rel Error', 'relative_error').replace('Rslt * Vol','rslt_x_vol').replace('Result','result').replace('Energy','energy').split()
        split_values=[line.replace('Total','1E36').split() for line in section[2:]]
        self.values = np.array([values for values in split_values], np.float64)
        self.df_values=pd.DataFrame(self.values, columns=self.columns)
                            
    def append(self, section):
        self.values.append(section)

class MeshTallyResCuV:
    def __init__(self, section):
        self.name = 'tally_results_cuv'
        self.columns = section[1].replace('Rel Error', 'relative_error').replace('Rslt * Vol','rslt_x_vol').replace('Result','result').replace('Energy','energy').replace('Cell bin','cell_bin').split()
        split_values=[line.replace('Total','1E36').split() for line in section[2:]]
        self.values = np.array([values for values in split_values], np.float64)
        self.df_values=pd.DataFrame(self.values, columns=self.columns)
                     
    def append(self, section):
        self.values.append(section)

#class MeshTallyResColCf:
#    def __init__(self, section):
#        self.name = 'tally_results_col_cf'
#        self.columns = section[1].replace('Rel Error', 'relative_error').replace('Rslt * Vol','rslt_x_vol').replace('Result','result').replace('Energy','energy').split()
#        split_values=[line.split() for line in section[2:]]
#        self.values = np.array([values for values in split_values if values[0]!='Total'], np.float64)
#        self.total_values = np.array([values[1:] for values in split_values if values[0]=='Total'], np.float64)
#        self.df_values=pd.DataFrame(self.values, columns=self.columns)
#                
#        if len(self.total_values)>0:
#            if self.columns[0]=='energy':
#                total_columns=[column.replace('rslt_x_vol','rslt_x_vol_tot_energy').replace('result','result_tot_energy').replace('relative_error','relative_error_tot_energy') for column in self.columns[1:]]
#            else:
#                total_columns=[column.replace('rslt_x_vol','rslt_x_vol_tot_energy').replace('result','result_tot_energy').replace('relative_error','relative_error_tot_energy') for column in self.columns]
#
#            self.df_total_values=pd.DataFrame(self.total_values, columns=total_columns)
#            if 'volume' in total_columns:
#                self.df_total_values=self.df_total_values.drop('volume', axis=1)
#            self.df_values=pd.merge(self.df_values,self.df_total_values, on=total_columns[:3])
#            
#    def append(self, section):
#        self.values.append(section)

#class MeshTallyResCuV:
#    def __init__(self, section):
#        self.name = 'tally_results_cuv'
#        self.columns = section[1].replace('Rel Error', 'relative_error').replace('Rslt * Vol','rslt_x_vol').replace('Result','result').replace('Energy','energy').replace('Cell bin','cell_bin').split()
#        split_values=[line.split() for line in section[2:]]
#        self.values = np.array([values for values in split_values if values[0]!='Total'], np.float64)
#        self.total_values = np.array([values[1:] for values in split_values if values[0]=='Total'], np.float64)
#        self.df_values=pd.DataFrame(self.values, columns=self.columns)
#                
#        if len(self.total_values)>0:
#            if self.columns[0]=='energy' or self.columns[0]=='cell_bin':
#                total_columns=[column.replace('rslt_x_vol','rslt_x_vol_tot_energy').replace('result','result_tot_energy').replace('relative_error','relative_error_tot_energy') for column in self.columns[1:]]
#            else:
#                total_columns=[column.replace('rslt_x_vol','rslt_x_vol_tot_energy').replace('result','result_tot_energy').replace('relative_error','relative_error_tot_energy') for column in self.columns]
#            
#            self.df_total_values=pd.DataFrame(self.total_values, columns=total_columns)
#            if 'volume' in total_columns:
#                self.df_total_values=self.df_total_values.drop('volume', axis=1)
#            self.df_values=pd.merge(self.df_values,self.df_total_values, on=total_columns[:3])
#            
#    def append(self, section):
#        self.values.append(section)

def MeshTalFactory(section):
    _MeshTALINFO = {
        #'d':MCTalFloat,
        'Mesh Tally Number':MeshTallyInfo,
        'Tally bin boundaries':MeshTallyBounds,
        'Energy Bin':MeshTallyMatrixEnergyBounds,
        'TallyMatrixResult':MeshTallyMatrixResult,
        'TallyMatrixRelativeErrors':MeshTallyMatrixError,
        'third_coord_bin':MeshTallyCoord,
        'tally_results_col_cf':MeshTallyResColCf,
        'tally_results_cuv':MeshTallyResCuV
    }
    name = section[1].strip()

    if 'Mesh Tally Number' in name:
        name='Mesh Tally Number'
    elif 'Tally bin boundaries' in name:
        name='Tally bin boundaries'
    elif 'Energy Bin' in name:
        name='Energy Bin'
    elif 'Cell bin' in name:
        name='tally_results_cuv'
    elif 'bin' in name:
        name='third_coord_bin'
    elif 'Rel Error' in name:
        name='tally_results_col_cf'
    elif 'Tally Results:' in name:
        name='TallyMatrixResult'
    elif 'Relative Errors' in name:
        name='TallyMatrixRelativeErrors'
    return _MeshTALINFO.get(name, MeshTalInfo)(section)

def dict_coords_to_ijk(geom):
    coords_dict_rec={'X':'I','Y':'J','Z':'K'}
    coords_dict_cyl={'R':'I','Z':'J','Th':'K','Theta':'K'}
    dict_geom={'REC':coords_dict_rec,'CYL':coords_dict_cyl}
    return dict_geom[geom]

def add_boundaries(df, I_lb, I_ub, J_lb, J_ub, K_lb, K_ub, energy_lb=None, energy_ub=None):
    coords={'I':[I_lb, I_ub],'J':[J_lb, J_ub],'K':[K_lb, K_ub]}
    if energy_lb and energy_ub:
        coords={'I':[I_lb, I_ub],'J':[J_lb, J_ub],'K':[K_lb, K_ub],'energy':[energy_lb, energy_ub]}
    
    for coord, bb in coords.items():
        coord_values=df[coord].values
        df_b=pd.DataFrame({coord+'_lb':bb[0],coord+'_ub':bb[1]})
        lb=df_b[coord+'_lb'].values
        ub=df_b[coord+'_ub'].values
        i, j = np.where((coord_values[:, None] > lb) & (coord_values[:, None] <= ub))
        df=pd.DataFrame(
        np.column_stack([df.values[i], df_b.values[j]]),
        columns=df.columns.append(df_b.columns)
        )
    return df

def read_meshtal(inputfile, calc_volume=False):
    with open(inputfile) as fid:
        mcnp_version=next(fid)
        file_comment=next(fid)
        particle_number=int(float(next(fid).strip().split('=')[1]))
        section_list= []
        for line in fid:
            if re.match('^\n', line):
                section_list.append([line])
            elif section_list:
                section_list[-1].append(line)
        section_list=[MeshTalFactory(section) for section in section_list if len(section)>1]

    tally_list={}
    for section in section_list:
        if section.name=='Mesh Tally Number':
            tally_num=section.number
            tally_list[tally_num]=section
        elif tally_list:
            if section.name=='Energy Bin':
                tally_list[tally_num].append(section)
            elif section.name=='third_coord_bin':
                tally_list[tally_num].tally_results[-1].append(section)
            elif section.name=='TallyMatrixResult' or section.name=='TallyMatrixRelativeErrors':
                tally_list[tally_num].tally_results[-1].sons[-1].append(section)
            elif section.name=='tally_results_col_cf':
                tally_list[tally_num].append(section)
            elif section.name=='tally_results_cuv':
                tally_list[tally_num].append(section)
            else:
                tally_list[tally_num].append_bounds(section)

    df_list=[]
    for i, tally in tally_list.items():
        tally_number=tally.number
        tally_geom_type=tally.tally_bounds.mesh_geom_type
        tally_energy_ub=tally.tally_bounds.energy_ub
        dict_ijk=dict_coords_to_ijk(tally_geom_type)
        df_list_e=[]
        for tally_e in tally.tally_results:
            if tally_e.name=='Energy Bin':
                energy_value=tally_e.energy_bin_ub
                df_list_c=[]
                for tally_c in tally_e.sons:
                    coord=tally_c.coord_name
                    coord_c_bin=tally_c.coord_c
                    across_variable=tally_c.sons[0].across_variable
                    down_variable=tally_c.sons[0].down_variable
                    result_df=tally_c.sons[0].df_results
                    error_df=tally_c.sons[1].df_errors
                    df=pd.merge(result_df,error_df, on=['down','across']).rename(columns={'down':down_variable,'across':across_variable})
                    df[coord]=coord_c_bin
                    df_list_c.append(df)
                df=pd.concat(df_list_c, ignore_index=True)

                df.columns=[dict_ijk.get(col, col) for col in df.columns]
                df['energy']=energy_value
                df=df[['energy','I','J','K','result','relative_error']]
                
                df_list_e.append(df)
            elif tally_e.name=='tally_results_col_cf':
                df=tally_e.df_values
                df.columns=[dict_ijk.get(col, col) for col in df.columns]
                if 'energy' in df.columns:
                    df_list_e.append(df)
                else:
                    N=(len(df)//len(tally_energy_ub))
                    energy=df.groupby(by=lambda x: x//N, axis=0).ngroup().apply(lambda i: tally_energy_ub[i])
                    df.insert(0,'energy',energy)
                    df_list_e.append(df)
            elif tally_e.name=='tally_results_cuv':
                df=tally_e.df_values
                df.columns=[dict_ijk.get(col, col) for col in df.columns]
                df_list_e.append(df)
                

        df=pd.concat(df_list_e, ignore_index=True)
        
        #if 'energy' in df.columns:
        #    if 'total' in df['energy'].values:
        #       
        #        df_total=df.loc[df['energy']=='total'].reset_index(drop=True).drop('energy', axis=1).rename(columns={'result':'result_tot_energy','relative_error':'relative_error_tot_energy'})
        #        df=pd.merge(df.loc[df['energy']!='total'],df_total, on=['I','J','K'])
         
        
        df['tally']=tally_number

        if 'energy' in df.columns:
            df=add_boundaries(df,tally.tally_bounds.i_lb,tally.tally_bounds.i_ub,tally.tally_bounds.j_lb,tally.tally_bounds.j_ub,tally.tally_bounds.k_lb,tally.tally_bounds.k_ub,tally.tally_bounds.energy_lb,tally.tally_bounds.energy_ub)
            columns_list=['tally','energy_lb','energy_ub','I_lb','I_ub','J_lb','J_ub','K_lb','K_ub','energy','I','J','K','result','relative_error','geometry_type','comment','tally_type']        
        else:
            df=add_boundaries(df,tally.tally_bounds.i_lb,tally.tally_bounds.i_ub,tally.tally_bounds.j_lb,tally.tally_bounds.j_ub,tally.tally_bounds.k_lb,tally.tally_bounds.k_ub)
            columns_list=['tally','I_lb','I_ub','J_lb','J_ub','K_lb','K_ub','I','J','K','result','relative_error','geometry_type','comment','tally_type']


        df['geometry_type']=tally_geom_type
        if 'volume' not in df.columns and calc_volume:
            df['volume_cf']=1
            df.loc[df['geometry_type']=='CYL','volume_cf']=np.pi*(df['I_ub']+df['I_lb'])
            
            df['volume']=(df['I_ub']-df['I_lb'])*(df['J_ub']-df['J_lb'])*(df['K_ub']-df['K_lb'])*df['volume_cf']
            df=df.drop('volume_cf', axis=1)
            df['rslt_x_vol']=df['result']*df['volume']
            columns_list.extend(['volume','rslt_x_vol','rslt_x_vol_tot_energy'])

        #if 'result_tot_energy' not in df.columns:
        #    df['result_tot_energy']=np.nan
        #    df['relative_error_tot_energy']=np.nan
#
        #if 'rslt_x_vol_tot_energy' not in df.columns:
        #    df['rslt_x_vol_tot_energy']=np.nan

        if 'cell_bin' in df.columns:
            columns_list.extend(['cell_bin'])

        

        df['comment']=tally.comment
        df['tally_type']=tally.type
        df=df[columns_list]
        df_list.append(df)

    df=pd.concat(df_list,ignore_index=True, sort=False)
    if 'energy' in df.columns:
        df['result_per_energy']=df['result']/(df['energy_ub']-df['energy_lb'])
        columns_list=['tally','energy_lb','energy_ub','I_lb','I_ub','J_lb','J_ub','K_lb','K_ub','energy','I','J','K','result','relative_error','result_per_energy','geometry_type','comment','tally_type']
    else:
        df['result_per_energy']=np.nan
        columns_list=['tally','I_lb','I_ub','J_lb','J_ub','K_lb','K_ub','I','J','K','result','relative_error','result_per_energy','geometry_type','comment','tally_type']
    if calc_volume:
        columns_list.extend(['volume','rslt_x_vol','rslt_x_vol_tot_energy'])
    
    if 'cell_bin' in df.columns:
        columns_list.extend(['cell_bin'])
    df=df[columns_list]

    return df
