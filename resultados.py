import warnings
warnings.filterwarnings("ignore")

import datetime
import os
today = datetime.date.today()  
directory = today.strftime("%Y%m%d")

# Generación de directorio para resultados
try:
    os.makedirs(f'Resultados/{directory}')
except:
    pass


try:
    os.makedirs(f'Resultados/{directory}/eps')
except:
    pass

try:
    os.makedirs(f'Resultados/{directory}/Metrics')
except:
    pass

try:
    os.makedirs(f'Resultados/{directory}/Metrics/eps')
except:
    pass

directory = f'Resultados/{directory}'

print('==========================================================================================================================')
print(f'PATH de resultados {directory}')
print('==========================================================================================================================')
print(f'Cargando data...')
print('==========================================================================================================================')


from utils.Metadata import Metadata
from utils.Database import Database
from utils.outlier import isOutlier

import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter

import matplotlib.pyplot as plt
import math 
plt.style.use('classic')

meta = Metadata()
db = Database()

dfOpt = meta.dfOptimos()

dfEjec = meta.dfEjecuciones(db.getEjecucionesResultados())
dfEjec = dfEjec.merge(dfOpt,how='left',on='instance').set_index(['id_ejec'])
tabla = dfEjec

# cambiamos algorithm a categorical - para mantener este orden en los gráficos - 
jerarquia = ['GWO','GWOQL','ANTHH GWO','ANTHHQL GWO']
tabla["algorithm"] = pd.Categorical(tabla["algorithm"],jerarquia)

# calculo de tiempo de ejecución
tabla['exec_time_min'] = (tabla.date_end-tabla.date_start).astype('timedelta64[m]')
tabla['exec_time_hour'] = tabla.exec_time_min/60

tabla['RPD'] = tabla['fitness']/tabla['optimo']-1
tabla['RPD'] = tabla['RPD'].apply(lambda x: np.round(x,3))

print('==========================================================================================================================')
print('Data obtenida y procesada....')
print('==========================================================================================================================')

print('==========================================================================================================================')
print('Marcando outliers....')
print('==========================================================================================================================')

for alg in tabla.algorithm.unique():
    print(f'Algoritmo: {alg}')
    for idx,row in tabla.query("algorithm==@alg").iterrows():
        condicion = (tabla.instance == row['instance'])&(tabla.algorithm==row['algorithm'])&(tabla.status=='terminado')
        serie = tabla[condicion]['fitness']
        data, outliers = isOutlier(serie)
        
        for i,r in tabla[condicion].iterrows():
            fitness = r['fitness']
            if fitness in outliers:
                tabla.loc[i,'outlier'] = 1
            else:
                tabla.loc[i,'outlier'] = 0
print('==========================================================================================================================')
print('outliers ok')
print('==========================================================================================================================')

tabla.to_csv(f'{directory}/tabla_total.csv',sep="|",decimal=",")

print('Reporte resumen...')

reporte = tabla.groupby(['algorithm','instance']).agg({'fitness':'min','optimo':'min'}).reset_index().\
pivot(columns=['algorithm'],values=['fitness'],index=['instance','optimo'])
reporte.to_csv(f'{directory}/reporte_resumen.csv',sep="|",decimal=",")
reporte.to_latex(f'{directory}/reporte_resumen.tex',decimal=".",index=False)

print('Reporte resumen ok')

print('Reporte ejecuciones')
ejecuciones = tabla[tabla.status=='terminado'].reset_index().groupby(['algorithm','instance']).\
agg({'id_ejec':'count','exec_time_hour':'mean','outlier':['sum']})
ejecuciones['ejec_ok'] = ejecuciones['id_ejec']['count']-ejecuciones['outlier']['sum']
ejecuciones.reset_index().to_csv(f'{directory}/reporte_ejecuciones.csv',sep="|",decimal=",")
ejecuciones.reset_index().to_latex(f'{directory}/reporte_ejecuciones.tex',decimal=".",index=False)

print('Reporte ejecuciones ok')


print('Test de normalidad')

from scipy.stats import shapiro
from scipy.stats import kstest
from scipy.stats import mannwhitneyu

algorithms = tabla.algorithm.unique()
instances  = tabla.instance.unique()
normality = pd.DataFrame([])

for alg1 in algorithms:
    print(f'Haciendo test a {alg1}')

    for inst in instances:

        cond1 = (tabla.instance == inst)&(tabla.algorithm==alg1)&(tabla.outlier==0)
        data1 = tabla[cond1]['fitness'].sort_values()[0:31]

        if (len(data1)>0):
            ks_p1 = kstest(data1,'norm')[1]

            shap_p1 = shapiro(data1)[1]

            normality = normality.append({

                'algorithm1':alg1,
                'instance':inst,
                'ks_test_p1':ks_p1,
                'shap_test_p1':shap_p1,

            },ignore_index=True)
normality =np.round(normality,3)
normality.to_csv(f'{directory}/test_normalidad.csv',sep="|",decimal=",")
normality.reset_index().to_latex(f'{directory}/test_normalidad.tex',decimal=".",index=False)

print('Todo ok')


algorithms = tabla.algorithm.unique()
instances  = tabla.instance.unique()
mannwhitney = pd.DataFrame([])

for alg1 in algorithms:
    for alg2 in algorithms:
        if (alg1 != alg2):
            print(f'Comparando {alg1} vs {alg2}')

            for inst in instances:

                cond1 = (tabla.instance == inst)&(tabla.algorithm==alg1)&(tabla.outlier==0)
                cond2 = (tabla.instance == inst)&(tabla.algorithm==alg2)&(tabla.outlier==0)
                data1 = tabla[cond1]['fitness'].sort_values()[0:31]
                data2 = tabla[cond2]['fitness'].sort_values()[0:31]

                mw_p = mannwhitneyu(data1,data2)[1]

                if (len(data1)>0) & (len(data2)>0):

                    mw_p = mannwhitneyu(data1,data2)[1]
                    mannwhitney = mannwhitney.append({

                        'algorithm1':alg1,
                        'algorithm2':alg2,
                        'instance':inst,
                        'pvalue':mw_p

                    },ignore_index=True)
mannwhitney = np.round(mannwhitney,3)
mannwhitney.to_csv(f'{directory}/test_wilcoxonmannwhitney.csv',sep="|",decimal=",")
mannwhitney.reset_index().to_latex(f'{directory}/test_wilcoxonmannwhitney.tex',decimal=".",index=False)

test_mann = np.round(mannwhitney.pivot(index=['algorithm1','instance'],columns='algorithm2',values=['pvalue']).fillna(0),3)
test_mann.to_csv(f'{directory}/reporte_wilcoxonmannwhitney.csv',sep="|",decimal=",")
test_mann.reset_index().to_latex(f'{directory}/reporte_wilcoxonmannwhitney.csv',decimal=".",index=False)

print ('Tests ok y reporte guardado')

print('==========================================================================================================================')
print('Generando boxplots por instancia - sin outliers -')
print('==========================================================================================================================')
for instance in tabla.instance.unique():
    data = tabla[(tabla.instance==instance)&(tabla.outlier==0)&(tabla.status=='terminado')][['algorithm','fitness']]
    ax = data.boxplot(figsize=(12,4),by=['algorithm'],column='fitness')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0f}'.format(y))) 
    plt.suptitle(f'Boxplot for instance {instance}')
    plt.title('')
    plt.savefig(f'{directory}/BoxplotSinOutlier_{instance}.png',dpi=150)
    plt.savefig(f'{directory}/eps/BoxplotSinOutlier_{instance}.eps',dpi=150)
    plt.close()

print('==========================================================================================================================')
print(' Boxplots ok -')
print('==========================================================================================================================')


print('==========================================================================================================================')
print('Generando boxplots por instancia - con outliers -')
print('==========================================================================================================================')

for instance in tabla.instance.unique():
    data = tabla[(tabla.instance==instance)&(tabla.status=='terminado')][['algorithm','fitness']]
    ax = data.boxplot(figsize=(12,4),by=['algorithm'],column='fitness')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0f}'.format(y))) 
    plt.suptitle(f'Boxplot for {instance} instance')
    plt.title('')
    plt.savefig(f'{directory}/BoxplotConOutlier_{instance}.png',dpi=150)
    plt.savefig(f'{directory}/eps/BoxplotConOutlier_{instance}.eps',dpi=150)
    plt.close()

print('==========================================================================================================================')
print('Boxplots ok ')
print('==========================================================================================================================')



# totalplots = len(tabla.drop_duplicates(['algorithm','instance']).index)
# print('==========================================================================================================================')
# print(f'Iniciando generación de grupos de {totalplots} plots')
# print('==========================================================================================================================')

# i=0
# for alg in tabla.algorithm.unique():
#     for inst in tabla[tabla.algorithm==alg].instance.unique():
#         i+=1
        
#         print(f'[{i}/{totalplots}] Consultando a la db: {alg}-{inst}')
#         iters = db.getIteracionesByAlgInst(alg,inst)
#         if len(iters)>0:

#             dfIter = meta.dfIteraciones(iters)
            
#             print(f'[{i}/{totalplots}] Datos ok')
            
#             ax = dfIter.pivot(columns='id_ejec',values='fitness',index='iter').plot(figsize=(15,7),legend=False)
#             ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}'.format(y))) 
#             plt.title(f'Convergence plot for {alg} algorithm solving instance {inst}')
#             plt.savefig(f'{directory}/Convergence_{alg}_{inst}.png',dpi=150)
#             plt.savefig(f'{directory}/eps/Convergence_{alg}_{inst}.eps',dpi=150)
#             plt.close()
            
#             print(f'[{i}/{totalplots}] Convergence guardado ok')
            
            # id_ejecs = tabla[(tabla.algorithm==alg)&(tabla.instance==inst)&(tabla.outlier==0)].reset_index()['id_ejec'].unique()
            
            # for id_ejec in id_ejecs:
                
            #     for key in meta.getMetrics():
                    
            #         ax = dfIter[dfIter.id_ejec == id_ejec][['iter',key]].set_index('iter')
            #         if len(ax) > 0:
            #             ax = ax.plot(figsize=(15,7),legend=False)
            #             ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2f}'.format(y))) 
            #             plt.title(f'Exploration plot for {alg} algorithm solving instance {inst} \n{meta.getMetrics()[key]} Metric')
            #             plt.savefig(f'{directory}/Metrics/Exploration_{alg}_{inst}_{key}_{id_ejec}.png',dpi=150)
            #             plt.savefig(f'{directory}/Metrics/eps/Exploration_{alg}_{inst}_{key}_{id_ejec}.eps',dpi=150)
            #             plt.close()

            #             print(f'[{i}/{totalplots}] Exploration metric: {key}, ejec: {id_ejec} guardado ok')