import json
import pandas  as pd

class Metadata:

    optimos = {}

    def __init__(self):

        self.optimos = {
                'scp41.txt':[0,429]
                ,'scp42.txt':[1,512]
                ,'scp43.txt':[2,516]
                ,'scp44.txt':[3,494]
                ,'scp45.txt':[0,512]
                ,'scp46.txt':[1,560]
                ,'scp47.txt':[2,430]
                ,'scp48.txt':[3,492]
                ,'scp49.txt':[0,641]
                ,'scp410.txt':[1,514]
                ,'scp51.txt':[2,253]
                ,'scp52.txt':[3,302]
                ,'scp53.txt':[0,226]
                ,'scp54.txt':[1,242]
                ,'scp55.txt':[2,211]
                ,'scp56.txt':[3,213]
                ,'scp57.txt':[0,293]
                ,'scp58.txt':[1,288]
                ,'scp59.txt':[2,279]
                ,'scp510.txt':[3,265]
                ,'scp61.txt':[0,138]
                ,'scp62.txt':[1,146]
                ,'scp63.txt':[2,145]
                ,'scp64.txt':[3,131]
                ,'scp65.txt':[0,161]
                ,'scpa1.txt':[1,253]
                ,'scpa2.txt':[2,252]
                ,'scpa3.txt':[3,232]
                ,'scpa4.txt':[0,234]
                ,'scpa5.txt':[1,236]
                ,'scpb1.txt':[2,69]
                ,'scpb2.txt':[3,76]
                ,'scpb3.txt':[0,80]
                ,'scpb4.txt':[1,79]
                ,'scpb5.txt':[2,72]
                ,'scpc1.txt':[3,227]
                ,'scpc2.txt':[0,219]
                ,'scpc3.txt':[1,243]
                ,'scpc4.txt':[2,219]
                ,'scpc5.txt':[3,215]
                ,'scpd1.txt':[0,60]
                ,'scpd2.txt':[1,66]
                ,'scpd3.txt':[2,72]
                ,'scpd4.txt':[3,62]
                ,'scpd5.txt':[0,61]
                ,'scpnre1.txt':[1,29]
                ,'scpnre2.txt':[2,30]
                ,'scpnre3.txt':[3,27]
                ,'scpnre4.txt':[0,28]
                ,'scpnre5.txt':[1,28]
                ,'scpnrf1.txt':[2,14]
                ,'scpnrf2.txt':[3,15]
                ,'scpnrf3.txt':[0,14]
                ,'scpnrf4.txt':[1,14]
                ,'scpnrf5.txt':[2,13]
                ,'scpnrg1.txt':[3,176]
                ,'scpnrg2.txt':[0,154]
                ,'scpnrg3.txt':[1,166]
                ,'scpnrg4.txt':[2,168]
                ,'scpnrg5.txt':[3,168]
                ,'scpnrh1.txt':[0,63]
                ,'scpnrh2.txt':[1,63]
                ,'scpnrh3.txt':[2,59]
                ,'scpnrh4.txt':[3,58]
                ,'scpnrh5.txt':[0,55]

                }
    def getOptimos(self):
        return self.optimos
    
    def dfOptimos(self):
        
        dfOpt = pd.DataFrame([],columns=['instance','orden','optimo'])
        for inst,value in self.optimos.items():
            inst = inst.split(".")
            dfOpt = dfOpt.append({'instance':'m'+inst[0],'orden':value[0],'optimo':value[1]},ignore_index=True)
        dfOpt['orden'] = dfOpt['orden'].astype(int)
        return dfOpt
    
    
    def dfEjecuciones(self,ejecuciones):
        
        df = pd.DataFrame([])

        for row in ejecuciones:

            params = json.loads(row[2])

            df = df.append({
                        'id_ejec':row[0],
                        'algorithm':row[1],
                        'instance':params['instance_name'],
                        'population':params['population'],
                        'maxIter':params['maxIter'],
                        'ql_alpha':params['ql_alpha'],
                        'ql_gamma':params['ql_gamma'],
                        'policy':params['policy'],
                        'rewardType': params['rewardType'],
                        'qlAlphaType': params['qlAlphaType'],
                        'date_start':row[3],
                        'date_end':row[4],
                        'status':row[5]

            },ignore_index=True,sort=False)
            
        df['id_ejec'] = df['id_ejec'].astype(int)
        return df
    
    def dfResultados(self,resultados):

        df = pd.DataFrame([])
    
        for row in resultados:
            
            df = df.append({
                        'id_ejec':row[1], #id ejec
                        'fitness':row[2]
                        
            },ignore_index=True,sort=False)
            
        try:
            df['id_ejec'] = df['id_ejec'].astype(int)

        except:
            return []
        return df