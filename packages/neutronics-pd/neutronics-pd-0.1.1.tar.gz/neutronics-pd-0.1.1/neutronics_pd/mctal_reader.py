import numpy as np
import re
import pandas as pd
import string
import xarray as xr

class MCTalInfo:
    def __init__(self, line):
        lline = line.split()
        self.name = lline[0]
        self.numbers = [int(ll) for ll in lline[1:]]
        self.values = []
        self.axis=np.arange(1)
        
        
    def append(self, line):
        self.values.append(line)
    
    def __repr__(self):
        return "MCInfo {}: {} - values - n lines: {}".format(self.name, self.numbers, len(self.values))

class MCTalSM(MCTalInfo):
    def __init__(self, line):
        super().__init__(line)
        self.len=max(1,self.numbers[0])
        self.le=max(1,self.numbers[0])
        self.name=self.name[0]
        if self.numbers[0]!=0:
            self.axis=np.arange(self.numbers[0])


class MCTalFloat(MCTalInfo):
    def __init__(self, line):
        super().__init__(line)
        self.len=max(1,self.numbers[0])
        self.le=max(1,len(self.values))
        self.name=self.name[0]
        
    def append(self,line):
        lline = line.split()
        self.values += [float(ll) for ll in lline]

        self.le=len(self.values)
        self.axis=self.values
        
    def __repr__(self):
        return super().__repr__() + " [Float]"

class MCTalInt(MCTalInfo):
    def append(self,line):
        lline = line.split()
        self.values += [int(ll) for ll in lline]
    def __repr__(self):
        return super().__repr__() + " [Int]"

class MCTalStr(MCTalInfo):
    def append(self,line):
        lline = line.split()
        self.values += [str(ll) for ll in lline]

    def __repr__(self):
        return super().__repr__() + " [Str]"

class MCTalVals(MCTalInfo):
    def __init__(self, line):
        super().__init__(line)
        self.errors =[]

        
    def append(self,line):
        lline = line.split()
        valerr = [float(ll) for ll in lline]
        self.values += valerr[::2]
        self.errors += valerr[1::2]
        
    def __repr__(self):
        return super().__repr__() + " [Float]"

_MCTALINFO = {
    #'d':MCTalFloat,
    'u':MCTalFloat,
    'ut':MCTalFloat,
    'uc':MCTalFloat,
    'm':MCTalSM,
    'mt':MCTalSM,
    'mc':MCTalSM,
    'c':MCTalFloat,
    'ct':MCTalFloat,
    'cc':MCTalFloat,
    'e':MCTalFloat,
    'et':MCTalFloat,
    'ec':MCTalFloat,
    't':MCTalFloat,
    'tt':MCTalFloat,
    'tc':MCTalFloat,
    'f':MCTalStr,
    'vals':MCTalVals
}
class MCTalRead:
    
    def __init__(self, inputfile):
        tally_list=self.tally_list(inputfile)
        tally_list_df =[MCTalDS(tally_dict).df for tally_dict in tally_list]
        self.df=pd.concat(tally_list_df,ignore_index=True)
        self.df['nps']=self.histories_number
        self.tally=tally_list
        
        
   # def __getitem__(self, val):
   #     return self.ds[val]#.to_dataframe()
   # 
   # def __repr__(self):
   #     string='tallies: '+str(list(self.ds.keys()))
   #     return string 
    
    def tally_list(self, inputfile):
        with open(inputfile) as fid:
            info = next(fid)
            self.histories_number = int(info.split()[-2])
            title = next(fid)
            section_list= []
            for line in fid:
                if re.match(r'\S', line):
                    section_list.append(self.MCTalFactory(line))
                elif section_list:
                    section_list[-1].append(line)

        tally_list = []
        for sect in section_list:
            if sect.name == 'tally':
                #d = OrderedDict()
                d = dict()
                d[sect.name]=sect
                tally_list.append(d)
            elif tally_list:
                tally_list[-1][sect.name]=sect
        return tally_list
    
    def MCTalFactory(self,line):
        lline = line.split()
        name = lline[0]
        #return MCTalInfo(line)
        return _MCTALINFO.get(name, MCTalInfo)(line)

    _MCTALINFO = {
        #'d':MCTalFloat,
        'u':MCTalFloat,
        'ut':MCTalFloat,
        'uc':MCTalFloat,
        'm':MCTalSM,
        'mt':MCTalSM,
        'mc':MCTalSM,
        'c':MCTalFloat,
        'ct':MCTalFloat,
        'cc':MCTalFloat,
        'e':MCTalFloat,
        'et':MCTalFloat,
        'ec':MCTalFloat,
        't':MCTalFloat,
        'tt':MCTalFloat,
        'tc':MCTalFloat,
        'f':MCTalStr,
        'vals':MCTalVals
    }


class MCTalDS():
    def __init__(self,tally_dict):
        self.tally_info=self.make_tallyinfo(tally_dict)
        self.df=self.make_dataset(tally_dict)
        
    
    def __repr__(self):
        return 'repr(self)'
    
    #def __getitem__(self, val):
    #    return self.ds[val]
    #
    def words(self,chars=string.ascii_lowercase):
        yield from chars
        for word in self.words(chars):
            for char in chars:
                yield word + char

    def make_dataset(self,tally_dict):
        tally_number='F'+str(tally_dict['tally'].numbers[0])
        
       # tally_comment=tally_dict['tally'].values[0].strip() if len(tally_dict['tally'].values)>0 else ''

        celle = tally_dict['f'].values
        iter_letters=self.words()
        celle = [next(iter_letters) if value=='0' else [value, next(iter_letters)][0] for value in celle]
        nc = len(celle)

        nd = max(1, tally_dict['d'].numbers[0])
        direct = np.arange(nd)

        nut = tally_dict['u'].len
        nu = tally_dict['u'].le
        nutt=nu+1
        user = tally_dict['u'].axis

        ns = max(1, tally_dict['s'].numbers[0])
        segment = np.arange(ns)

        net = tally_dict['e'].len
        ne = tally_dict['e'].le
        nett = ne + 1
        energie = tally_dict['e'].axis

        ntt = tally_dict['t'].len
        nt = tally_dict['t'].le
        nttt = nt + 1
        tempi = tally_dict['t'].axis

        nmt = tally_dict['m'].len
        nm = tally_dict['m'].le
        nmtt= nm + 1
        multiplier = tally_dict['m'].axis

        nct = tally_dict['c'].len
        ncc = tally_dict['c'].le
        nctt = ncc + 1
        cosine = tally_dict['c'].axis


        
        #midx=pd.MultiIndex.from_product([celle, direct, user, segment,multiplier,cosine, energie, tempi], names=['cell', 'direct', 'user', 'segment','multiplier','cosine', 'energy_ub', 'time_shake_ub'])
        values = np.empty((nc, nd, nutt, ns, nmtt, nctt, nett, nttt), dtype = 'object')
        values[:,:,:,:,:,:,:,:] = None
        errors = np.empty((nc, nd, nutt, ns, nmtt, nctt, nett, nttt), dtype = 'object')
        errors[:,:,:,:,:,:,:,:] = None
        values[:,:,:nut,:,:nmt,:nct,:net,:ntt] = np.array(tally_dict['vals'].values).reshape((nc, nd, nut, ns, nmt,nct, net, ntt))
        errors[:,:,:nut,:,:nmt,:nct,:net,:ntt] = np.array(tally_dict['vals'].errors).reshape((nc, nd, nut, ns, nmt,nct, net, ntt))

        #values_notot=values[:,:,:nu,:,:nm,:ncc,:ne,:nt].flatten()
        #errors_notot=errors[:,:,:nu,:,:nm,:ncc,:ne,:nt].flatten()   
        #value_error=np.array([values_notot,errors_notot]).T
        #df= pd.DataFrame(value_error, index = midx, columns=['value','relative_error'])
        #df=df.reset_index()

        coords = {'cell':celle, 'direct':direct, 'user':user, 'segment':segment,'multiplier':multiplier,
                  'cosine':cosine, 'energy_ub':energie, 'time_shake_ub':tempi}
    
        df = xr.Dataset({'value': (['cell','direct', 'user', 'segment', 'multiplier', 'cosine', 'energy_ub', 'time_shake_ub'],values[:,:,:nu,:,:nm,:ncc,:ne,:nt]),
                         'relative_error': (['cell','direct', 'user', 'segment', 'multiplier', 'cosine', 'energy_ub', 'time_shake_ub'],errors[:,:,:nu,:,:nm,:ncc,:ne,:nt]),
                         'value_tot_energy': (['cell','direct', 'user', 'segment', 'multiplier', 'cosine', 'time_shake_ub'],values[:,:,:nu,:,:nm,:ncc,-1,:nt]),
                         'relative_error_tot_energy': (['cell','direct', 'user', 'segment', 'multiplier', 'cosine', 'time_shake_ub'],errors[:,:,:nu,:,:nm,:ncc,-1,:nt]),
                         'value_tot_time_shake': (['cell','direct', 'user', 'segment', 'multiplier', 'cosine', 'energy_ub'],values[:,:,:nu,:,:nm,:ncc,:ne,-1]),
                         'relative_error_tot_time_shake': (['cell','direct', 'user', 'segment', 'multiplier', 'cosine', 'energy_ub'],errors[:,:,:nu,:,:nm,:ncc,:ne,-1]),
                         'value_tot_cosine': (['cell','direct', 'user', 'segment', 'multiplier', 'energy_ub', 'time_shake_ub'],values[:,:,:nu,:,:nm,-1,:ne,:nt]),
                         'relative_error_tot_cosine': (['cell','direct', 'user', 'segment', 'multiplier', 'energy_ub', 'time_shake_ub'],errors[:,:,:nu,:,:nm,-1,:ne,:nt]),
                         'value_tot_multiplier': (['cell','direct', 'user', 'segment', 'cosine', 'energy_ub', 'time_shake_ub'],values[:,:,:nu,:,-1,:ncc,:ne,:nt]),
                         'relative_error_tot_multiplier': (['cell','direct', 'user', 'segment', 'cosine', 'energy_ub', 'time_shake_ub'],errors[:,:,:nu,:,-1,:ncc,:ne,:nt]),
                         'value_tot_user': (['cell','direct', 'segment', 'multiplier', 'cosine', 'energy_ub', 'time_shake_ub'],values[:,:,-1,:,:nm,:ncc,:ne,:nt]),
                         'relative_error_tot_user': (['cell','direct', 'segment', 'multiplier', 'cosine', 'energy_ub', 'time_shake_ub'],errors[:,:,-1,:,:nm,:ncc,:ne,:nt]),
                        }, coords= coords).to_dataframe().reset_index()
        

        df.insert(0,'tally',tally_number)
        energy_lb=df.groupby(['cell', 'direct', 'user', 'segment','multiplier','cosine', 'time_shake_ub'])['energy_ub'].transform(lambda x:x.shift(fill_value=0))
        df.insert(7,'energy_lb',energy_lb)
        energy_center_bin=(df['energy_ub']+df['energy_lb'])/2
        df.insert(9,'energy',energy_center_bin)
        delta_energy=df['energy_ub']-df['energy_lb']
        df.insert(10,'delta_energy_bin',delta_energy)
        time_lb=df.groupby(['cell', 'direct', 'user', 'segment','multiplier','cosine', 'energy_ub'])['time_shake_ub'].transform(lambda x:x.shift(fill_value=0))
        df.insert(11,'time_shake_lb',time_lb)
        #time_shake_center_bin=(df['time_shake_ub']+df['time_shake_lb'])/2
        #df.insert(13,'time_shake',time_shake_center_bin)
        df['value_per_energy']=(df['value'].div(df['delta_energy_bin'].where(df['delta_energy_bin']!=0,np.nan))).replace([np.inf, -np.inf], np.nan).fillna(0)
        df['comment']=self.tally_info['comment']
        df['particle_type']=self.tally_info['particle']
        df['detector']=self.tally_info['detector']

        
        
        return df

    def make_tallyinfo(self,tally_dict):
        tally_comment= tally_dict['tally'].values[0].strip() if len(tally_dict['tally'].values)>0 else ''
        particleList = { 1 : "Neutron" , 2 : "Photon" , 3 : "Neutron + Photon"  , 
					          4 : "Electron", 5 : "Neutron + Electron" , 6 : "Photon + Electron" ,
                              7 : "Neutron + Photon + Electron" }

        detectorTypeList = { -6 : "smesh", -5 : "cmesh", -4 : "rmesh",
					   # The line below duplicates the line above with short names for tally naming during conversion.
					   # See the function getDetectorType to see how this information is used
					  -3 : "Spherical mesh tally" , -2 : "Cylindrical mesh tally", -1 : "Rectangular mesh tally",
					   0 : "None",  1 : "Point",  2 : "Ring",
					   3: 'FIP', 4:'FIR', 5:'FIC' }
        particle_id=tally_dict['tally'].numbers[1]
        detector_id=tally_dict['tally'].numbers[2]
        particletype=particleList.get(particle_id,'unknown') 
        detectortype=detectorTypeList.get(detector_id,'unknown')
        return {'comment':tally_comment,'particle':particletype,'detector':detectortype}



class MCTalSeries(pd.Series):

    @property
    def _constructor(self):
        return MCTalSeries

    @property
    def _constructor_expanddim(self):
        return MCTalDataFrame


class MCTalDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return MCTalDataFrame

    @property
    def _constructor_sliced(self):
        return MCTalSeries

    def get_results(self,**kwargs):
        dropable_cols=['cosine', 'direct', 'energy_ub', 'multiplier',
       'segment', 'energy_lb', 'time_shake_ub', 'energy', 'delta_energy_bin',
       'time_shake_lb', 'user', 'value_tot_cosine',
       'relative_error_tot_cosine', 'value_tot_multiplier',
       'relative_error_tot_multiplier', 'value_tot_user',
       'relative_error_tot_user', 'value_per_energy']
        cond=''
        index=''
        cond_cells=''
        for k,item in kwargs.items():
            
            if k!='index' and k!='cells':
                item=str(item)
                if cond:
                    cond += '& (self.'+k+'=="'+item+'")'
                else:
                    cond = '(self.'+k+'=="'+item+'")'
            else:
                if k=='index':
                    item=str(item)
                    index=item
                elif k=='cells':
                    if type(item) is list:
                        item=[str(i) for i in item]
                        cond_cells = item
                    else:
                        print('Variable type for cells must be list')
        df=self[pd.eval(cond)].reset_index(drop=True)
        if cond_cells:
            df=df[df.cell.isin(cond_cells)].reset_index(drop=True)
        for col in df.columns:
            if len(df[col].unique()) == 1 and col in dropable_cols:
                df = df.drop(col,axis=1)
        if index:
            df=df.set_index(index, drop=True)
        return df


def read_mctal(inputfile):
    df=MCTalRead(inputfile).df
    df=MCTalDataFrame(df)
    return df
