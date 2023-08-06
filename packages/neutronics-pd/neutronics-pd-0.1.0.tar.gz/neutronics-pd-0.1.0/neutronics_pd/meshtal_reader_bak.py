import pandas as pd
import numpy as np
import re
from joblib import Parallel, delayed
import itertools
from collections import OrderedDict

class MeshTalInfo:
    def __init__(self, section):
        self.name = section[1] 
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
        self.tally_results={}
        self.tally_bounds=''
        
    def append(self, subsect):
        self.tally_results.append(subsect)
        
        
    def append_bounds(self, subsect):
        self.tally_bounds=subsect

class MeshTallyBounds:
    def __init__(self, section):
        self.name = 'Tally bin boundaries'
        if 'Cylinder' in section[2]:
            self.mesh_geom_type='CYL'
            self.i_name=section[3].split(':')[0].strip()
            self.j_name=section[4].split(':')[0].strip()
            self.k_name=section[5].split(':')[0].strip()
            i_b=section[3].split(':')[1].split()
            j_b=section[4].split(':')[1].split()
            k_b=section[5].split(':')[1].split()
        else:
            self.mesh_geom_type='REC' 
            self.i_name=section[2].split(':')[0].strip()
            self.j_name=section[3].split(':')[0].strip()
            self.k_name=section[4].split(':')[0].strip()
            i_b=section[2].split(':')[1].split()
            j_b=section[3].split(':')[1].split()
            k_b=section[4].split(':')[1].split()
            
        i_b=[float(i) for i in i_b]
        j_b=[float(j) for j in j_b]
        k_b=[float(k) for k in k_b]
        self.i_lb=i_b[:-1]
        self.i_ub=i_b[1:]
        self.j_lb=j_b[:-1]
        self.j_ub=j_b[1:]
        self.k_lb=k_b[:-1]
        self.k_ub=k_b[1:]
        energy_b=section[5].split(':')[1].split()
        energy_b=[float(energy) for energy in energy_b]
        self.energy_lb=energy_b[:-1]
        self.energy_ub=energy_b[1:]
        self.df_ib=pd.DataFrame({'I_lb':self.i_lb,'I_ub':self.i_ub})
        self.df_ib['I']=(self.df_ib['I_lb']+self.df_ib['I_ub'])/2
        self.df_jb=pd.DataFrame({'J_lb':self.j_lb,'J_ub':self.j_ub})
        self.df_jb['J']=(self.df_jb['J_lb']+self.df_jb['J_ub'])/2
        self.df_kb=pd.DataFrame({'K_lb':self.k_lb,'K_ub':self.k_ub})
        self.df_kb['K']=(self.df_kb['K_lb']+self.df_kb['K_ub'])/2
        self.df_energyb=pd.DataFrame({'energy_lb':self.energy_lb,'energy_ub':self.energy_ub,'energy':self.energy_ub})
        
    def append(self, section):
        self.values.append(section)

class MeshTallyEnergyBounds:
    def __init__(self, section):
        self.name = 'Energy Bin'
        if 'Total' in section[1]:
            self.energy_bin_lb='total'
            self.energy_bin_ub='total'
        else:
            self.energy_bin_lb=float(section[1].split()[2])
            self.energy_bin_ub=float(section[1].split()[4])
        self.sons={}
    def append(self, section):
        self.sons.append(section)
        
class MeshTallyRes:
    def __init__(self, section):
        self.name = 'Tally Results'
        self.across_variable= section[1].split('(across)')[0].strip().split()[-1]
        self.down_variable= section[1].split('(down)')[0].strip().split()[-1]
        self.across_var_arr=section[2].split()
        self.across_var_arr=[float(value) for value in self.across_var_arr]
        split_values=[line.split() for line in section[3:]]
        self.down_var_arr=[float(values[0]) for values in split_values]
        self.result_array=np.array([values[1:] for values in split_values], np.float64).flatten()
        midx=pd.MultiIndex.from_product([self.down_var_arr, self.across_var_arr], names=['down','across'])
        self.df_results=pd.DataFrame(self.result_array, index=midx, columns=['result']).reset_index()
    

class MeshTallyErr:
    def __init__(self, section):
        self.name = 'Relative Errors'
        self.across_var_arr=section[2].split()
        self.across_var_arr=[float(value) for value in self.across_var_arr]
        split_values=[line.split() for line in section[3:]]
        self.down_var_arr=[float(values[0]) for values in split_values]
        self.result_array=np.array([values[1:] for values in split_values], np.float64).flatten()
        midx=pd.MultiIndex.from_product([self.down_var_arr, self.across_var_arr], names=['down','across'])
        self.df_errors=pd.DataFrame(self.result_array, index=midx, columns=['relative_error']).reset_index()
   
        
class MeshTallyCoord:
    def __init__(self, section):
        self.name = 'third_coord_bin'
        self.coord_name=section[1].split()[0]
        self.coord_bin_lb=float(section[1].split()[2])
        self.coord_bin_ub=float(section[1].split()[4])
        self.coord_c=(self.coord_bin_lb+self.coord_bin_ub)/2
        self.sons={}
    def append(self, section):
        self.sons.append(section)
        
class MeshTallyResColCf:
    def __init__(self, section):
        self.name = 'tally_results_col_cf'
        self.columns = section[1].replace('Rel Error', 'relative_error').replace('Rslt * Vol','rslt_x_vol').replace('Result','result').replace('Energy','energy').replace('Cell bin','cell_bin').split()
        split_values=[line.split() for line in section[2:]]
        self.values = np.array([values for values in split_values if values[0]!='Total'], np.float64)
        self.total_values = np.array([values[1:] for values in split_values if values[0]=='Total'], np.float64)
        self.df_values=pd.DataFrame(self.values, columns=self.columns)
                
        if len(self.total_values)>0:
            if self.columns[0]=='energy' or self.columns[0]=='cell_bin':
                total_columns=[column.replace('rslt_x_vol','rslt_x_vol_tot_energy').replace('result','result_tot_energy').replace('relative_error','relative_error_tot_energy') for column in self.columns[1:]]
            else:
                total_columns=[column.replace('rslt_x_vol','rslt_x_vol_tot_energy').replace('result','result_tot_energy').replace('relative_error','relative_error_tot_energy') for column in self.columns]
            
            self.df_total_values=pd.DataFrame(self.total_values, columns=total_columns)
            if 'volume' in total_columns:
                self.df_total_values=self.df_total_values.drop('volume', axis=1)
            self.df_values=pd.merge(self.df_values,self.df_total_values, on=total_columns[:3])
            
    def append(self, section):
        self.values.append(section)

def MeshTalFactory(section):
    _MeshTALINFO = {
        #'d':MCTalFloat,
        'Mesh Tally Number':MeshTallyInfo,
        'Tally bin boundaries':MeshTallyBounds,
        'Energy Bin':MeshTallyEnergyBounds,
        'Tally Results':MeshTallyRes,
        'Relative Errors':MeshTallyErr,
        'third_coord_bin':MeshTallyCoord,
        'tally_results_col_cf':MeshTallyResColCf,
        'Cell Bin':MeshTallyResColCf
    }
    name = section[1].strip()
    if 'Mesh Tally Number' in name:
        name='Mesh Tally Number'
    elif 'Tally bin boundaries' in name:
        name='Tally bin boundaries'
    elif 'Energy Bin' in name:
        name='Energy Bin'
    elif 'Cell bin' in name:
        name='Cell Bin'
    elif 'bin' in name:
        name='third_coord_bin'
    elif 'Rel Error' in name:
        name='tally_results_col_cf'
    elif 'Tally Results:' in name:
        name='Tally Results'
    #return MCTalInfo(line)
    return _MeshTALINFO.get(name, MeshTalInfo)(section)

def dict_coords_to_ijk(geom):
    coords_dict_rec={'X':'I','Y':'J','Z':'K'}
    coords_dict_cyl={'R':'I','Z':'J','Th':'K','Theta':'K'}
    dict_geom={'REC':coords_dict_rec,'CYL':coords_dict_cyl}
    return dict_geom[geom]

def add_boundaries(df, I_lb, I_ub, J_lb, J_ub, K_lb, K_ub, energy_lb, energy_ub):
    
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

def create_tally_c(tally_c):
    coord=tally_c.coord_name
    coord_c_bin=tally_c.coord_c
    across_variable=tally_c.sons[0].across_variable
    down_variable=tally_c.sons[0].down_variable
    result_df=tally_c.sons[0].df_results
    error_df=tally_c.sons[1].df_errors
    df=pd.merge(result_df,error_df, on=['down','across']).rename(columns={'down':down_variable,'across':across_variable})
    df[coord]=coord_c_bin
    return df

def create_tally_e(tally_e, dict_ijk):
    if tally_e.name=='Energy Bin':
        energy_value=tally_e.energy_bin_ub
        df_list_c=(create_tally_c(tally_c) for tally_c in tally_e.sons)
        print('ciao')
        df_list_c=Parallel(n_jobs=-1, max_nbytes=None, verbose=100)(delayed(create_tally_c)(tally_c) for tally_c in tally_e.sons)
        df=pd.concat(df_list_c, ignore_index=True)

        df.columns=[dict_ijk.get(col, col) for col in df.columns]
        df['energy']=energy_value
        df=df[['energy','I','J','K','result','relative_error']]
            
    elif tally_e.name=='tally_results_col_cf':
        df=tally_e.df_values
        df.columns=[dict_ijk.get(col, col) for col in df.columns]
        if 'energy' not in df.columns:
            N=(len(df)//len(tally_energy_ub))
            energy=df.groupby(by=lambda x: x//N, axis=0).ngroup().apply(lambda i: tally_energy_ub[i])
            df.insert(0,'energy',energy)

    return df


def create_tally(tally):
    tally_number=tally.number
    tally_geom_type=tally.tally_bounds.mesh_geom_type
    tally_energy_ub=tally.tally_bounds.energy_ub
    dict_ijk=dict_coords_to_ijk(tally_geom_type)
    print('ciao_tally_e')
    df_list_e=(create_tally_e(tally_e, dict_ijk) for tally_e in tally.tally_results)
    print('fine ciao_tally_e')
        
    df=pd.concat(list(df_list_e), ignore_index=True)
    print('mica mi blocco qui?')
    df['tally']=tally_number
    if 'total' in df['energy'].values:
        voxel_g=df.groupby(['I','J','K'])
        list_groups=[]
        for i, group in voxel_g:
            group['result_tot_energy']=group.loc[group['energy']=='total','result'].values[0]
            group['relative_error_tot_energy']=group.loc[group['energy']=='total','relative_error'].values[0]
            group=group.loc[group['energy']!='total']
            list_groups.append(group)
        df=pd.concat(list_groups, ignore_index=True)
    
    print('add boundaries')
    df=add_boundaries(df,tally.tally_bounds.i_lb,tally.tally_bounds.i_ub,tally.tally_bounds.j_lb,tally.tally_bounds.j_ub,tally.tally_bounds.k_lb,tally.tally_bounds.k_ub,tally.tally_bounds.energy_lb,tally.tally_bounds.energy_ub)
    print('fine boundaries')


    df['geometry_type']=tally_geom_type
    if 'volume' not in df.columns:
        df['volume_cf']=1
        df.loc[df['geometry_type']=='CYL','volume_cf']=np.pi*(df['I_ub']+df['I_lb'])
        print('calc volume')
        df['volume']=(df['I_ub']-df['I_lb'])*(df['J_ub']-df['J_lb'])*(df['K_ub']-df['K_lb'])*df['volume_cf']
        print('end calc volume')
        df=df.drop('volume_cf', axis=1)
        df['rslt_x_vol']=df['result']*df['volume']

    if 'result_tot_energy' not in df.columns:
        df['result_tot_energy']=np.nan
        df['relative_error_tot_energy']=np.nan

    if 'rslt_x_vol_tot_energy' not in df.columns:
        df['rslt_x_vol_tot_energy']=np.nan

    df=df[['tally','energy_lb','energy_ub','I_lb','I_ub','J_lb','J_ub','K_lb','K_ub','energy','I','J','K','result','relative_error','result_tot_energy','relative_error_tot_energy','volume','rslt_x_vol','rslt_x_vol_tot_energy','geometry_type']]

    df['comment']=tally.comment
    df['tally_type']=tally.type
    return df
    



def read_meshtal(inputfile):
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

        #section_list=Parallel(n_jobs=-1, max_nbytes=None, verbose=100)(delayed(MeshTalFactory)(section)  for section in section_list if len(section)>1)
        #section_list=[section for section in section_list ]
        section_list=(MeshTalFactory(section) for section in section_list if len(section)>1)
        #print(section_list)

    tally_list=OrderedDict()
    for section in section_list:
        if section.name=='Mesh Tally Number':
            son_index_generator=itertools.count(0,1)
            tally_number=section.number
            tally_list[tally_number]=section
        elif tally_list:
            print(section.name)
            if section.name=='Energy Bin':
                son_index=next(son_index_generator)
                coord_index_generator=itertools.count(0,1)
                tally_list[tally_number].tally_results[son_index]=section
            elif section.name=='third_coord_bin':
                cord_index=next(coord_index_generator)
                #print(cord_index)
                tally_list[tally_number].tally_results[son_index].sons[cord_index]=section
            elif section.name=='Tally Results' or section.name=='Relative Errors':
                #print('hi!')
                tally_list[tally_number].tally_results[son_index].sons[cord_index].sons[section.name.lower().replace(' ','_')]=section
            elif section.name=='tally_results_col_cf':
                son_index=next(son_index_generator)
                tally_list[tally_number].tally_results[son_index]=section
            else:
                print('mica muoio qui?')
                #tally_list[tally_number].append_bounds(section)
            

    print('ciao_tally')
    df_list=(create_tally(tally) for tally in tally_list)
    
    print('fine lettura di tutti i tallies')    

    df=pd.concat(list(df_list),ignore_index=True, sort=False)
    df['result_per_energy']=df['result']/(df['energy_ub']-df['energy_lb'])

    df=df[['tally','energy_lb','energy_ub','I_lb','I_ub','J_lb','J_ub','K_lb','K_ub','energy','I','J','K','result','relative_error','result_per_energy','result_tot_energy','relative_error_tot_energy','volume','rslt_x_vol','rslt_x_vol_tot_energy','geometry_type','comment','tally_type']]

    return df
