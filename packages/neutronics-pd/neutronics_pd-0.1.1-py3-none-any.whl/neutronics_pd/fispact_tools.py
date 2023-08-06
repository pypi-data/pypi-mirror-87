import pandas as pd
import re
import glob
import numpy as np
import datetime as dt
import itertools
import pypact as pp
import json

def parse_time(time_str):
    """
    Parse a time string e.g. (2h13m) into a timedelta object.

    Modified from virhilo's answer at https://stackoverflow.com/a/4628148/851699

    :param time_str: A string identifying a duration.  (eg. 2h13m)
    :return datetime.timedelta: A datetime.timedelta object
    """
    time_str=time_str.replace(" ","")
    regex = re.compile(r'^((?P<years>[\.\d]+?)y)?((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')
    parts = regex.match(time_str)
    assert parts is not None, "Could not parse any time information from '{}'.  Examples of valid strings: '8h', '2d8h5m20s', '2m4s'".format(time_str)
    time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
    year_to_days=365.2425 #pd.to_timedelta(1,'Y')/np.timedelta64(1,'D')
    if 'years' in time_params.keys():
        days=time_params['years']*year_to_days
        if 'days' in time_params.keys():
            time_params['days']+=days
        else:
            time_params['days']=days
        del time_params['years']
    return dt.timedelta(**time_params).total_seconds()

def tryfloat(num):
    try:
        risultato = float(num)
        return risultato
    except:
        return str(num)

def read_fispact_cooling_table(inputfile):
    cooling_data_line=[]
    with open(inputfile) as fid:
        for line in fid:
            if 'Cooling Phase' in line:
                first_line=next(fid)
                first_line = first_line.replace('Cooling','').replace('+/-','').replace('%','').replace('\n','')
                cooling_data_line.append(first_line)
            elif cooling_data_line:
                if '0 Mass of material input' in line:
                    break
                else:
                    line=line.replace('Cooling','').replace('+/-','').replace('%','').replace('\n','')
                    cooling_data_line.append(line)
    table=[]
    for line in cooling_data_line:
        line_split=line.strip().split('   ')
        line_split=[tryfloat(value) for value in line_split if value !='']
        table.append(line_split)
     #table =[i for i in table]
    try:
        table_df=pd.DataFrame(table, columns=['Time step', 'Cumulative Years', 'Activity', 'Error Activity', 'Dose rate','Error Dose rate', 'Heat output','Error Heat output','Ingestion dose','Error Ingestion dose','Inhalation dose','Error Inhalation dose','Tritium activity'])
        error_col=[col for col in table_df.columns if 'Error' in col]
        table_df[error_col]=table_df[error_col]/100
    except:
        table_df=pd.DataFrame(table, columns=['Time step', 'Cumulative Years', 'Activity', 'Dose rate', 'Heat output','Ingestion dose','Inhalation dose','Tritium activity'])
    return table_df

class FispactRead:
    def __init__(self, line):
        self.line = line
        self.time_interval=int(line.split('TIME INTERVAL')[1].split()[0])
        try:
            #self.elapsed_time=line.split('ELAPSED TIME IS')[1].split('*')[0].strip()
            time_i=line.split('TIME IS')[1].split('OR')[-1].split('*')[0].strip()
            time_i2=line.split('ELAPSED TIME IS')[1].split('*')[0].strip()
            self.elapsed_time=str(float(time_i.split()[0]))+' '+time_i.split()[1][0].lower()
            self.elapsed_time2=str(float(time_i2.split()[0]))+' '+time_i2.split()[1][0].lower()
        except IndexError:
            time_i=line.split('TIME IS')[1].split('OR')[-1].split('*')[0].strip()
            self.elapsed_time=str(float(time_i.split()[0]))+' '+time_i.split()[1][0].lower()
            self.elapsed_time2=None
        self.time=line.split('TIME')[2].split('OR')[-1].replace('*','').replace('ELAPSED','').replace('IS','').strip().replace(' ','-')
        if 'COOLING TIME' in line:
            self.cooling=1
        else:
            self.cooling=0
        self.lines = [line]
    def append(self, line):
        if not len(line.strip())==0: 
            self.lines.append(line)
            
    def __repr__(self):
        return "FispactRead lines: {}".format(self.lines)

    def time_table(self):
        lines_r=[]
        columns= list(filter(None, self.lines[1].strip().split('  ')))
        columns = [title.strip().lower().replace(' ','_').replace('bq', 'activity').replace('b-energy','beta_heat').replace('a-energy','alpha_heat').replace('g-energy','gamma_heat') for title in columns]
        for line in self.lines[3:]:
            if 'TOTAL NUMBER OF NUCLIDES PRINTED IN INVENTORY' in line:
                break
            nuclide = [line[:8].strip().replace(' ','')]
            values=[]
            values_split=line[8:].replace('#','').replace('>','').replace('<','').replace('&','').replace('*','').replace('?','').split()
            for value in values_split:
                try:
                    value_float=float(value)
                    values.append(value_float)
                except ValueError:
                    values.append(value)
            linea = nuclide + values
            lines_r.append(linea)

        try:
            df=pd.DataFrame(lines_r, columns=columns)
            df['heat']=df['alpha_heat']+df['beta_heat']+df['gamma_heat']
            df['activity_total']=df['activity'].sum()
            df['dose_rate_total']=df['dose_rate'].sum()
            df['atoms_total']=df['atoms'].sum()
            df['heat_total']=df['heat'].sum()
            df['cooling']=self.cooling
            df['time_interval']=self.time_interval
            #df['step_time']=self.elapsed_time
            df['time_label']=self.elapsed_time2 if self.elapsed_time2 is not None else self.elapsed_time
            df['time']=df['time_label'].apply(lambda x: parse_time(x))
            df['time_label']=df['time_label'].apply(lambda x: re.sub(r'(\.0)(?=(\s+))','',x))
            df['time_day']=df['time']/(24*3600)
            df['decay_costant']=df['half_life'].apply(lambda _s: np.log(2)/_s if type(_s)==float else _s)
            df['element']=df['nuclide'].apply(lambda x: re.match(r'(?i)[A-Z]+(?=(\d+))',x).group(0))
            return df
        except:
            return None
        

class FISPACTSeries(pd.Series):

    @property
    def _constructor(self):
        return FISPACTSeries

    @property
    def _constructor_expanddim(self):
        return FISPACTDataFrame


class FISPACTDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return FISPACTDataFrame

    @property
    def _constructor_sliced(self):
        return FISPACTSeries

    def get_dominants(self, quantity, x=1, cooling_phase=1):
        quantity_total=f'{quantity}_total'
        return (self
                    .loc[self['cooling_phase']==cooling_phase]
                    .groupby(['time_interval','time_label'])
                    .apply(lambda _df: _df.nlargest(x, quantity).reset_index(drop=True))
                    .assign(percentage=lambda _df: _df[quantity]/_df[quantity_total])
                    .reset_index(level=0, drop=True)
                    [['nuclide',quantity,quantity_total,'percentage','time','time_day','time_interval']]
                    )
        

    def get_cooling_phase(self):
        return self.loc[self['cooling_phase']==True].reset_index(drop=True)

def read_fispact_output(inputfile):
    sections=[]
    with open(inputfile) as fid:
        for line in fid:
            if re.search(r'TIME INTERVAL', line):
                sections.append(FispactRead(line))
            elif sections:
                sections[-1].append(line)
    time_tables_od = list(section.time_table() for section in sections)
    df=pd.concat(time_tables_od, ignore_index=True)
    
    df['cooling_phase']=False
    try:
        idx=df.index[df['time'].diff()<0][0]
        df.loc[idx:,'cooling_phase']=True
        return FISPACTDataFrame(df)
    except:
        if (len(df['cooling'].unique())==1) and (df['cooling'].unique()[0]==1):
            df['cooling_phase']==True
        return FISPACTDataFrame(df)

def read_fispact_output_from_stringIO(fid):
    sections=[]
    for line in fid:
        if re.search(r'TIME INTERVAL', line):
            sections.append(FispactRead(line))
        elif sections:
            sections[-1].append(line)
    time_tables_od = list(section.time_table() for section in sections)
    df=pd.concat(time_tables_od, ignore_index=True)
    
    df['cooling_phase']=False
    try:
        idx=df.index[df['time'].diff()<0][0]
        df.loc[idx:,'cooling_phase']=True
        return FISPACTDataFrame(df)
    except:
        if (len(df['cooling'].unique())==1) and (df['cooling'].unique()[0]==1):
            df['cooling_phase']==True
        return FISPACTDataFrame(df)

def create_arb_flux(energy, value, filename_output='arb_flux', comment='comment'):
    stringa=''
    for i in range(0,len(energy),5):
        stringa+=' '.join(energy[i:i+5])+'\n'
    stringa+='0.100001E-01\n'
    for i in range(0,len(value),6):
        stringa+=' '.join(value[i:i+6])+'\n'
    stringa+='1.0\n'+comment
    with open(filename_output,'w') as f:
        f.write(stringa)

def create_arb_flux_mctal(df_input, tally, cell, volume, neutron_yield, filename_output='arb_flux', comment='comment'):
    df=df_input.get_results(tally=tally,cell=cell)
    df['volume']=volume
    df['spectra']=df['value']*neutron_yield/df['volume']
    energy=(df.sort_values('energy_ub',ascending=False)['energy_ub']*10**6).map('{:0.6E}'.format).astype(str).tolist()
    spectra=df.sort_values('energy_ub',ascending=False)['spectra'].map('{:0.6E}'.format).astype(str).tolist()
    create_arb_flux(energy, spectra, filename_output, comment)
    
def create_arb_flux_meshtal(df_input, tally, source, dir_output, filename_output='arb_flux', comment='comment'):
    df=df_input.loc[df_input['tally']==str(tally)]
    df['spectra']=df['result']*source
    number=itertools.count(start=1, step=1)
    df['voxel_id']=0
    df['voxel_id']=df.groupby(['I','J','K'])['voxel_id'].transform(lambda _s: next(number))
    
    for voxel_id in df['voxel_id'].unique():
        df_voxel=df.loc[df['voxel_id']==voxel_id].reset_index(drop=True)
        x=df_voxel['I'].values[0]
        y=df_voxel['J'].values[0]
        z=df_voxel['K'].values[0]
        position=f'{x}_{y}_{z}'
        comment=f'voxel Position: I={x} J={y} K={z}, source={source}'
        filename_output=f'{dir_output}/arb_flux_tally_{tally}_{position}'
        energy=(df_voxel.sort_values('energy',ascending=False)['energy']*10**6).map('{:0.6E}'.format).astype(str).tolist()
        spectra=df_voxel.sort_values('energy',ascending=False)['spectra'].map('{:0.6E}'.format).astype(str).tolist()
        create_arb_flux(energy, spectra, filename_output, comment)


def read_fispact_json(inputfile):
    AVOGADRO = 6.0221415 * 1e23 
    with open(inputfile) as json_file:
        data = json.load(json_file)
    lista_df=[]
    for i in range(len(data['inventory_data'])):
        irr_time=data['inventory_data'][i]['irradiation_time']
        cool_time=data['inventory_data'][i]['cooling_time']
        if i>0:
            irr_time_prev=data['inventory_data'][i-1]['irradiation_time']
            cool_time_prev=data['inventory_data'][i-1]['cooling_time']
            elapsed_time_prev=data['inventory_data'][i-1]['elapsed_time']
            
            if irr_time > irr_time_prev:
                data['inventory_data'][i]['cooling'] = 0
                data['inventory_data'][i]['elapsed_time']=elapsed_time_prev+irr_time - irr_time_prev
            elif cool_time > cool_time_prev:
                data['inventory_data'][i]['cooling'] = 1
                data['inventory_data'][i]['elapsed_time']=elapsed_time_prev+cool_time - cool_time_prev
            else:
                print('there is an error')
        else:
            if irr_time == 0:
                data['inventory_data'][i]['elapsed_time']=cool_time
                data['inventory_data'][i]['cooling'] = 1
            elif cool_time == 0:
                data['inventory_data'][i]['elapsed_time']=irr_time
                data['inventory_data'][i]['cooling'] = 0
            else:
                print('there is an error')
        if data['inventory_data'][i]['nuclides']:
            df=pd.DataFrame(data['inventory_data'][i]['nuclides'])
            df['atoms']=df['grams']/df['isotope']*AVOGADRO
            df['nuclide']=df['element']+df['isotope'].apply(str)+df['state']
            df['irradiation_time']=irr_time
            df['cooling_time']=cool_time
            df['time']=data['inventory_data'][i]['elapsed_time']
            df['flux']=data['inventory_data'][i]['flux']
            df['total_heat']=data['inventory_data'][i]['total_heat']
            df['total_alpha_heat']=data['inventory_data'][i]['alpha_heat']
            df['total_beta_heat']=data['inventory_data'][i]['beta_heat']
            df['total_gamma_heat']=data['inventory_data'][i]['gamma_heat']
            df['ingestion_dose']=data['inventory_data'][i]['ingestion_dose']
            df['inhalation_dose']=data['inventory_data'][i]['inhalation_dose']
            df['dose_rate']=data['inventory_data'][i]['dose_rate']['dose']
            df['cooling']=data['inventory_data'][i]['cooling']
            df['time_interval']=i+1
            lista_df.append(df)

    df=pd.concat(lista_df, ignore_index=True)
    id_stop_irradiation_phase=df[df['cooling']==0].last_valid_index()
    id_start_cooling_phase=id_stop_irradiation_phase+1
    df['cooling_phase']=False
    df.loc[df.index>=id_start_cooling_phase, 'cooling_phase']=True
    df['time_cooling_phase']=0
    time_end_irradiation=df.loc[df.index==id_stop_irradiation_phase,'time'].values[0]
    df.loc[df['cooling_phase']==True, 'time_cooling_phase']=df.loc[df['cooling_phase']==True, 'time']-time_end_irradiation
    df['time_day']=df['time']/24/3600

    return df


def read_fispact_out(inputfile):
    with pp.Reader(runname) as data:
        
        lista_df=[]
        for i in range(len(data.inventory_data)):
            irr_time=data.inventory_data[i].irradiation_time
            cool_time=data.inventory_data[i].cooling_time
            if i>0:
                irr_time_prev=data.inventory_data[i-1].irradiation_time
                cool_time_prev=data.inventory_data[i-1].cooling_time
                elapsed_time_prev=data.inventory_data[i-1].elapsed_time
                if irr_time > irr_time_prev:
                    data.inventory_data[i].cooling = 0
                    data.inventory_data[i].elapsed_time=elapsed_time_prev+irr_time - irr_time_prev
                elif cool_time > cool_time_prev:
                    data.inventory_data[i].cooling = 1
                    data.inventory_data[i].elapsed_time=elapsed_time_prev+cool_time - cool_time_prev
                else:
                    print('there is an error')
            else:
                if irr_time == 0:
                    data.inventory_data[i].elapsed_time=cool_time
                    data.inventory_data[i].cooling = 1
                elif cool_time == 0:
                    data.inventory_data[i].elapsed_time=irr_time
                    data.inventory_data[i].cooling = 0
                else:
                    print('there is an error')
            if data.inventory_data[i].nuclides:
                df=pd.DataFrame(data.inventory_data[i].nuclides)
                df['nuclide']=df['element']+df['isotope'].apply(str)+df['state']
                df['irradiation_time']=irr_time
                df['cooling_time']=cool_time
                df['time']=data['inventory_data'][i]['elapsed_time']
                df['flux']=data['inventory_data'][i]['flux']
                df['total_heat']=data['inventory_data'][i]['total_heat']
                df['total_alpha_heat']=data['inventory_data'][i]['alpha_heat']
                df['total_beta_heat']=data['inventory_data'][i]['beta_heat']
                df['total_gamma_heat']=data['inventory_data'][i]['gamma_heat']
                df['ingestion_dose']=data['inventory_data'][i]['ingestion_dose']
                df['inhalation_dose']=data['inventory_data'][i]['inhalation_dose']
                df['dose_rate']=data['inventory_data'][i]['dose_rate']['dose']
                df['cooling']=data['inventory_data'][i]['cooling']
                df['time_interval']=i+1
                lista_df.append(df)

    df=pd.concat(lista_df, ignore_index=True)
    id_stop_irradiation_phase=df[df['cooling']==0].last_valid_index()
    id_start_cooling_phase=id_stop_irradiation_phase+1
    df['cooling_phase']=False
    df.loc[df.index>=id_start_cooling_phase, 'cooling_phase']=True
    df['time_cooling_phase']=0
    time_end_irradiation=df.loc[df.index==id_stop_irradiation_phase,'time'].values[0]
    df.loc[df['cooling_phase']==True, 'time_cooling_phase']=df.loc[df['cooling_phase']==True, 'time']-time_end_irradiation
    df['time_day']=df['time']/24/3600

    return df