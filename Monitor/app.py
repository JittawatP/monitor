from flask import Flask, jsonify, render_template,request
from database import get_connection
from datetime import datetime

app = Flask(__name__)

 
@app.route('/api/monitor804', methods=['GET'])
def get_data_monitor():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql1inout = "SELECT \
                    dates.date_str AS `date`, \
                    COALESCE(pqindex_input, 0) AS `pqindexinput`, \
                    COALESCE(pqindex_output, 0) AS `pqindexoutput`, \
                    COALESCE(icp_input, 0) AS `icpinput`, \
                    COALESCE(icp_output, 0) AS `icpoutput`, \
                    COALESCE(rde_input, 0) AS `rdeinput`, \
                    COALESCE(rde_output, 0) AS `rdeoutput`, \
                    COALESCE(rfs_input, 0) AS `rfsinput`, \
                    COALESCE(rfs_output, 0) AS `rfsoutput`, \
                    COALESCE(v40_input, 0) AS `v40input`, \
                    COALESCE(v40_output, 0) AS `v40output`, \
                    COALESCE(v100_input, 0) AS `v100input`, \
                    COALESCE(v100_output, 0) AS `v100output`, \
                    COALESCE(ftir_input, 0) AS `ftirinput`, \
                    COALESCE(ftir_output, 0) AS `ftiroutput`, \
                    COALESCE(an_input, 0) AS `aninput`, \
                    COALESCE(an_output, 0) AS `anoutput`, \
                    COALESCE(bn_input, 0) AS `bninput`, \
                    COALESCE(bn_output, 0) AS `bnoutput`, \
                    COALESCE(kf_input, 0) AS `kfinput`, \
                    COALESCE(kf_output, 0) AS `kfoutput`, \
                    COALESCE(fuel_input, 0) AS `fuelinput`, \
                    COALESCE(fuel_output, 0) AS `fueloutput`, \
                    COALESCE(pc_input, 0) AS `pcinput`, \
                    COALESCE(pc_output, 0) AS `pcoutput` \
                FROM ( \
                    SELECT DISTINCT DATE_FORMAT(`rt`.`created`, '%Y-%m-%d') AS `date_str` \
                    FROM `focuslabs_resulttags` `rt` \
                    WHERE `rt`.`created` >= (DATE(NOW() - INTERVAL 14 DAY)) \
                ) AS dates \
                LEFT JOIN ( \
                    SELECT \
                        DATE_FORMAT(`ta`.`ta_ent_dt`, '%Y-%m-%d') AS `date_str`, \
                        SUM((CASE \
                            WHEN (`labdo`.`PQindex` = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `pqindex_input`, \
                        SUM((CASE \
                            WHEN((`labdo`.`ICPtest` = 1) AND (`labdo`.`RDEcheck` = 1)) THEN 1 \
                            ELSE 0 \
                        END)) AS `icp_input`, \
                        SUM((CASE \
                            WHEN((`labdo`.`ICPtest` <> 1) AND (`labdo`.`RDEcheck` = 1)) THEN 1 \
                            ELSE 0 \
                        END)) AS `rde_input`, \
                         SUM((CASE \
                            WHEN (`labdo`.`RFScheck` = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `rfs_input`, \
                        SUM((CASE \
                            WHEN (`labdo`.`V40test` = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `v40_input`, \
                        SUM((CASE \
                            WHEN (`labdo`.`V100test` = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `v100_input`, \
                        SUM((CASE \
                            WHEN (`labdo`.`FTIRcheck` = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `ftir_input`, \
                        SUM((CASE \
                            WHEN ((`labdo`.`TANtest` = 1) or (`labdo`.`TANextra` = 1)  )  THEN 1 \
                            ELSE 0 \
                        END)) AS `an_input`, \
                        SUM((CASE \
                            WHEN ((`labdo`.`TBNtest` = 1) or (`labdo`.`TBNextra` = 1)) THEN 1 \
                            ELSE 0 \
                        END)) AS `bn_input`, \
                        SUM((CASE \
                            WHEN (`labdo`.`KFCheck` = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `kf_input`, \
                        SUM((CASE \
                            WHEN (`labdo`.`FuelCheck` = 1) THEN 1 \
                            ELSE 0 \
                        END \
                        )) AS `fuel_input`, \
                        SUM((CASE \
                            WHEN (`labdo`.`PCcheck` = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `pc_input` \
                    FROM \
                        `tblresult` `r` \
                    INNER JOIN `tbltimeanalysis` `ta` ON `ta`.`ta_batch` = `r`.`batch` \
                    INNER JOIN `sample_lab_do_vw` `labdo` ON `labdo`.`sample#` = `r`.`sample#` \
                    WHERE \
                        `ta`.`ta_ent_dt` >= (DATE(NOW() - INTERVAL 14 DAY)) \
                    GROUP BY `date_str` \
                ) AS input_data ON dates.date_str = input_data.date_str \
                LEFT JOIN ( \
                    SELECT \
                        DATE_FORMAT(`rt`.`created`, '%Y-%m-%d') AS `date_str`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'pqindex' = 1) THEN 1 \
                            ELSE 0 \
                        END)) AS `pqindex_output`, \
                        SUM((CASE \
                            WHEN((`labdo`.`ICPtest` = 1)AND (`t`.`name` = 'rde')) THEN 1 \
                            ELSE 0 \
                        END)) AS `icp_output`, \
                        SUM((CASE \
                            WHEN((`labdo`.`ICPtest` <> 1) AND (`t`.`name` = 'rde')) THEN 1 \
                            ELSE 0 \
                        END)) AS `rde_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'rfs') THEN 1 \
                            ELSE 0 \
                        END)) AS `rfs_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'v40') THEN 1 \
                            ELSE 0 \
                        END)) AS `v40_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'v100') THEN 1 \
                            ELSE 0 \
                        END)) AS `v100_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'ftir') THEN 1 \
                            ELSE 0 \
                        END)) AS `ftir_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'tan') THEN 1 \
                            ELSE 0 \
                        END)) AS `an_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'tbn') THEN 1 \
                            ELSE 0 \
                        END)) AS `bn_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'kf') THEN 1 \
                            ELSE 0 \
                        END)) AS `kf_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'fuel') THEN 1 \
                            ELSE 0 \
                        END)) AS `fuel_output`, \
                        SUM((CASE \
                            WHEN (`t`.`name` = 'pc') THEN 1 \
                            ELSE 0 \
                        END)) AS `pc_output` \
                    FROM \
                        `focuslabs_resulttags` `rt` \
                    INNER JOIN `focuslabs_tags` `t` ON `rt`.`tags_id` = `t`.`id` \
                    INNER JOIN `sample_lab_do_vw` `labdo` ON `labdo`.`sample#` = `rt`.`result_id` \
                    WHERE \
                        `t`.`name` IN ('pqindex','rde', 'rfs', 'v40', 'v100', 'ftir', 'tan', 'tbn', 'kf', 'fuel', 'pc') \
                        AND `rt`.`created` >= (DATE(NOW() - INTERVAL 14 DAY)) \
                    GROUP BY `date_str` \
                ) AS output_data ON dates.date_str = output_data.date_str \
                ORDER BY dates.date_str DESC;"

    sql2acc =   "SELECT \
                	SUM((CASE \
                			WHEN((`labdo`.`PQindex` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 42 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as pqindexacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`ICPtest` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 6 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as icpacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`ICPtest` = 0 AND `labdo`.`RDEcheck` = 1  ) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 6 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as rdeacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`RFScheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 7 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as rfsacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`v40test` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 2 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as v40acc, \
                	SUM((CASE \
                			WHEN((`labdo`.`v100test` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 3 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as v100acc, \
                	SUM((CASE \
                			WHEN((`labdo`.`ftircheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 8 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as ftiracc, \
                	SUM((CASE \
                			WHEN((`labdo`.`TANtest` = 1 or `labdo`.`TANextra` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 9 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as anacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`TBNtest` = 1 or `labdo`.`TBNextra` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 11 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as bnacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`KFCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 12 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as kfacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`FuelCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 13 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as fuelacc, \
                	SUM((CASE \
                			WHEN((`labdo`.`PCcheck` = 1 AND (`labdo`.`PC_P` = 1 or  `labdo`.`PC_L` = 1) ) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 32 limit 1) is null) \
                            THEN 1 \
                			ELSE 0 \
                		END)) as pcacc \
                FROM sample_lab_do_vw labdo \
                inner join tblresult r on labdo.`sample#` = r.`sample#` \
                inner join tbltimeanalysis ta on r.batch = ta.ta_batch \
                where r.drecieved >= (DATE(NOW() - INTERVAL 14 DAY)) \
                AND `labdo`.`sample#` >= 24060000 \
                AND (`labdo`.`ta_status` <> 'Finished');"

    sqlinlab = "SELECT \
                    DATE_FORMAT(IncomingReceivedDate,'%Y-%m-%d') as date_str , \
                    sum(IncomingAmount) as input \
                FROM tblincoming \
                WHERE (IncomingReceivedDate >= DATE(NOW() - INTERVAL 14 DAY)) \
                GROUP BY IncomingReceivedDate \
                ORDER BY IncomingReceivedDate desc;"
    
    sqloutput = "SELECT \
                    'Sent' AS operation,count(tblresult.`sample#`) as output, \
                    DATE_FORMAT(tbltimeanalysis.ta_sent_dt, '%Y-%m-%d') as date_str \
                FROM tblresult \
                INNER JOIN tbltimeanalysis on tblresult.batch = tbltimeanalysis.ta_batch \
                WHERE tbltimeanalysis.ta_sent_dt >= DATE(NOW() - INTERVAL 14 DAY) \
                GROUP BY DATE_FORMAT(tbltimeanalysis.ta_sent_dt, '%Y-%m-%d');"
    cursor.execute(sql1inout)  
    data1 = cursor.fetchall()

    cursor.execute(sql2acc)  
    data2 = cursor.fetchall()

    cursor.execute(sqlinlab)  
    data3 = cursor.fetchall()

    cursor.execute(sqloutput)  
    data4 = cursor.fetchall()

    conn.close()

    combined_data = combine_and_sort_data(data1,data2,data3,data4)
    return jsonify(combined_data)

def combine_and_sort_data(data1,data2,data3,data4):
    combined_data =[]
    for i, d1 in enumerate(data1):
        if i < len(data2):
            d2 = data2[i]
            combined_data.append({
                'date_str': d1['date'],
                'pqindex_input': d1['pqindexinput'],
                'pqindex_output': d1['pqindexoutput'],
                'pqindex_acc': d2['pqindexacc'] if i == 0 else '',

                'icp_input': d1['icpinput'],
                'icp_output': d1['icpoutput'],
                'icp_acc': d2['icpacc'] if i == 0 else '',

                'rde_input': d1['rdeinput'],
                'rde_output': d1['rdeoutput'],
                'rde_acc': d2['rdeacc'] if i == 0 else '',
  
                'rfs_input': d1['rfsinput'],
                'rfs_output': d1['rfsoutput'],
                'rfs_acc': d2['rfsacc'] if i == 0 else '',

                'v40_input': d1['v40input'],
                'v40_output': d1['v40output'],
                'v40_acc': d2['v40acc'] if i == 0 else '',

                'v100_input': d1['v100input'],
                'v100_output': d1['v100output'],
                'v100_acc': d2['v100acc'] if i == 0 else '',

                'ftir_input': d1['ftirinput'],
                'ftir_output': d1['ftiroutput'],
                'ftir_acc': d2['ftiracc'] if i == 0 else '',

                'an_input': d1['aninput'],
                'an_output': d1['anoutput'],
                'an_acc': d2['anacc'] if i == 0 else '',

                'bn_input': d1['bninput'],
                'bn_output': d1['bnoutput'],
                'bn_acc': d2['bnacc'] if i == 0 else '',

                'kf_input': d1['kfinput'],
                'kf_output': d1['kfoutput'],
                'kf_acc': d2['kfacc'] if i == 0 else '',

                'fuel_input': d1['fuelinput'],
                'fuel_output': d1['fueloutput'],
                'fuel_acc': d2['fuelacc'] if i == 0 else '',

                'pc_input': d1['pcinput'],
                'pc_output': d1['pcoutput'],
                'pc_acc': d2['pcacc'] if i == 0 else ''

            })
        else :
            combined_data.append({
                'date_str': d1['date'],

                'pqindex_input': d1['pqindexinput'],
                'pqindex_output': d1['pqindexoutput'],
                'pqindex_acc': '',

                'icp_input': d1['icpinput'],
                'icp_output': d1['icpoutput'],
                'icp_acc': '',

                'rde_input': d1['rdeinput'],
                'rde_output': d1['rdeoutput'],
                'rde_acc': '',
  
                'rfs_input': d1['rfsinput'],
                'rfs_output': d1['rfsoutput'],
                'rfs_acc': '',

                'v40_input': d1['v40input'],
                'v40_output': d1['v40output'],
                'v40_acc': '',

                'v100_input': d1['v100input'],
                'v100_output': d1['v100output'],
                'v100_acc': '',

                'ftir_input': d1['ftirinput'],
                'ftir_output': d1['ftiroutput'],
                'ftir_acc': '',

                'an_input': d1['aninput'],
                'an_output': d1['anoutput'],
                'an_acc': '',

                'bn_input': d1['bninput'],
                'bn_output': d1['bnoutput'],
                'bn_acc': '',

                'kf_input': d1['kfinput'],
                'kf_output': d1['kfoutput'],
                'kf_acc': '',

                'fuel_input': d1['fuelinput'],
                'fuel_output': d1['fueloutput'],
                'fuel_acc': '',

                'pc_input': d1['pcinput'],
                'pc_output': d1['pcoutput'],
                'pc_acc': ''
            })
    for d1 in combined_data:
        for d3 in data3:
            if d1['date_str'] == d3['date_str']:
                d1.update({
                    'input': d3['input']
                })
    for d1 in combined_data:
        for d4 in data4:
            if d1['date_str'] == d4['date_str']:
                d1.update({
                    'output' : d4['output']
                    })
            
    return combined_data

@app.route('/api/dashboard', methods=['GET'])
def get_data_dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sqltxt = "SELECT \
		SUM((CASE \
				WHEN((`labdo`.`PQindex` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 42 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as pqindexacc, \
		SUM((CASE \
				WHEN((`labdo`.`ICPtest` = 0 AND `labdo`.`RDEcheck` = 1  ) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 6 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as rdeacc, \
		SUM((CASE \
				WHEN((`labdo`.`ICPtest` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 6 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as icpacc, \
		SUM((CASE \
				WHEN((`labdo`.`RFScheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 7 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as rfsacc, \
		SUM((CASE \
				WHEN((`labdo`.`v40test` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 2 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as v40acc, \
		SUM((CASE \
				WHEN((`labdo`.`v100test` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 3 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as v100acc, \
		SUM((CASE \
				WHEN((`labdo`.`ftircheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 8 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as ftiracc, \
		SUM((CASE \
				WHEN((`labdo`.`TANtest` = 1 or `labdo`.`TANextra` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 9 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as anacc, \
		SUM((CASE \
				WHEN((`labdo`.`TBNtest` = 1 or `labdo`.`TBNextra` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 11 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as bnacc, \
		SUM((CASE \
				WHEN((`labdo`.`KFCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 12 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as kfacc, \
		SUM((CASE \
				WHEN((`labdo`.`FuelCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 13 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as fuelacc, \
		SUM((CASE \
				WHEN((`labdo`.`PCcheck` = 1 AND (`labdo`.`PC_P` = 1 or  `labdo`.`PC_L` = 1) ) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 32 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as pcacc, \
		SUM((CASE \
				WHEN((`labdo`.`FerroCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 40 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as ferroacc, \
		SUM((CASE \
				WHEN((`labdo`.`I-pH` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 30 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as iphacc, \
		SUM((CASE \
				WHEN((`labdo`.`GravCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 28 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as graviacc, \
		SUM((CASE \
				WHEN((`labdo`.`VPIcheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 38 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as mpcacc, \
		SUM((CASE \
				WHEN((`labdo`.`RulerCheck1` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 36 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as ruleracc, \
		SUM((CASE \
				WHEN((`labdo`.`Foaming` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 27 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as foamingacc, \
		SUM((CASE \
				WHEN((`labdo`.`AirRelCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 15 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as airrelacc, \
		SUM((CASE \
				WHEN((`labdo`.`WaterSepCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 39 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as watersepacc, \
		SUM((CASE \
				WHEN((`labdo`.`CopperStripCorrosion` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 20 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as copperstripacc, \
		SUM((CASE \
				WHEN((`labdo`.`RPVOTCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 34 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as rpvotacc, \
		SUM((CASE \
				WHEN((`labdo`.`OilFilCheck` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 24 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as oilfilacc, \
		SUM((CASE \
				WHEN((`labdo`.`AutoIgnition` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 16 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as autoigacc, \
		SUM((CASE \
				WHEN((`labdo`.`FlashPointD92` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 26 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as flaspointd92acc, \
		SUM((CASE \
				WHEN((`labdo`.`FlashPoint` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 25 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as flaspointcloseacc, \
		SUM((CASE \
				WHEN((`labdo`.`phcheck1` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 33 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as phacc, \
		SUM((CASE \
				WHEN((`labdo`.`RACheck1` = 1) AND (select id from focuslabs_resulttags rt where rt.result_id = r.`sample#` and rt.tags_id = 35 limit 1) is null) \
                THEN 1 \
				ELSE 0 \
			END)) as raacc \
FROM sample_lab_do_vw labdo \
left join tblresult r on labdo.`sample#` = r.`sample#` \
left join tbltimeanalysis ta on r.batch = ta.ta_batch \
where r.drecieved > (NOW() - INTERVAL 180 DAY) \
AND `labdo`.`sample#` >= 24060000 \
AND (`labdo`.`ta_status` <> 'Finished');"

    cursor.execute(sqltxt)  
    data = cursor.fetchall()
    conn.close()

    return jsonify(data)

def combine_daily(data1,data2,data3,data4,data5):
    combined_data = []
    # Map outputs to inputs
    mapping = {
        "dataentry_output": "lab_input",
        "lab_output": "qc_input",
        "qc_output": "interp_input",
        "interp_output": "print_input",
        "print_output": "sent_input"
    }
    # ดึงข้อมูลวันที่
    combined_data.append({"date":data1[0]["date"]})


    # ต่อข้อมูลจาก data1 ให้มี key เป็น operation และ output
    for d1 in data1:
        operation_key =d1["operation"].lower() + "_output"
        output_value = d1["output"]
        combined_data.append({operation_key: output_value})
        if operation_key in mapping:
            input_key = mapping[operation_key]            
            combined_data.append({input_key: output_value})
    # ต่อข้อมูลจาก data2 ให้มี key เป็น operation และ acc
    for d2 in data2:
        operation_key = d2["operation"].lower() + "_acc"
        combined_data.append({operation_key: d2["Acc"]})

    # ต่อข้อมูลจาก data3 (นำข้อมูลมาต่อเป็นพจนานุกรม)
    combined_data.append({'dataentry_acc': data3[0]['dataAcc']})
   
    # ต่อข้อมูลจาก data4 (นำข้อมูลมาต่อเป็นพจนานุกรม)
    combined_data.append({'ferro_acc': data4[0]['ferro']})

    for item in combined_data:
        if "interp_acc" in item:
            item['interp_acc'] = int(item['interp_acc']) - int(data4[0]['ferro'])
       
    # ต่อข้อมูลจาก data5 (นำข้อมูลมาต่อเป็นพจนานุกรม)
    for key, value in data5.items():
        combined_data.append({key: value})
    return combined_data

@app.route('/api/daily', methods=['GET','POST'])
def get_data_daily():
    today = request.form.get('today', datetime.now().strftime('%Y-%m-%d 00:00:00')) #('%Y-%m-%d 00:00:00')
    # รับข้อมูลจากฟอร์ม
    form_data = request.form.to_dict()
    # ตรวจสอบข้อมูลที่รับ
    print("Received form data:", form_data)
    pre_acc_dataentry = request.form.get('pre_acc_dataentry')
    pre_acc_lab = request.form.get('pre_acc_lab')
    pre_acc_qc = request.form.get('pre_acc_qc')
    pre_acc_interp = request.form.get('pre_acc_interp')
    pre_acc_print = request.form.get('pre_acc_print')
    pre_acc_sent = request.form.get('pre_acc_sent')

    dataentry_input = request.form.get('dataentry_input')
    print("pre_acc_interpwwww",pre_acc_interp)
    data5 = {
        'dataentry_input' : dataentry_input,
        'pre_acc_dataentry': pre_acc_dataentry,
        'pre_acc_lab': pre_acc_lab,
        'pre_acc_qc': pre_acc_qc,
        'pre_acc_interp': pre_acc_interp,
        'pre_acc_print': pre_acc_print,
        'pre_acc_sent': pre_acc_sent  
    }

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # กำหนดตัวแปร @tempDate ด้วยค่า today
    cursor.execute("SET @tempDate = %s", (today,))

    sqlOutPut = """ 
        select * from (
        select  'DataEntry' AS operation,count(tblResult.`sample#`) as output , DATE_FORMAT(tbltimeanalysis.ta_ent_dt, '%Y-%m-%d') as date
        from tblresult inner join tbltimeanalysis on tblresult.batch = tbltimeanalysis.ta_batch
        WHERE tblTimeAnalysis.ta_ent_dt >= @tempDate
        group by tblTimeAnalysis.ta_ent_dt

        union

        select  'Lab' AS operation,count(tblresult.`sample#`) as output, DATE_FORMAT(tbltimeanalysis.ta_lab_dt, '%Y-%m-%d') as date 
        from tblresult inner join tbltimeanalysis on tblresult.batch = tbltimeanalysis.ta_batch
        where tbltimeanalysis.ta_lab_dt >= @tempDate
        group by tblTimeanalysis.ta_lab_dt

        union

        select  'QC' AS operation,count(tblresult.`sample#`) as output, DATE_FORMAT(tbltimeanalysis.ta_qc_dt, '%Y-%m-%d') as date 
        from tblresult inner join tbltimeanalysis on tblresult.batch = tbltimeanalysis.ta_batch
        where tbltimeanalysis.ta_qc_dt >= @tempDate
        group by tblTimeanalysis.ta_qc_dt

        union

        select  'Interp' AS operation,count(tblresult.`sample#`) as output, DATE_FORMAT(tbltimeanalysis.ta_int2_dt, '%Y-%m-%d') as date 
        from tblresult inner join tbltimeanalysis on tblresult.batch = tbltimeanalysis.ta_batch
        where tbltimeanalysis.ta_int2_dt >= @tempDate
        group by tblTimeanalysis.ta_int2_dt

        union

        select  'Print' AS operation,count(tblresult.`sample#`) as output, DATE_FORMAT(tbltimeanalysis.ta_prt_dt, '%Y-%m-%d') as date 
        from tblresult inner join tbltimeanalysis on tblresult.batch = tbltimeanalysis.ta_batch
        where tbltimeanalysis.ta_prt_dt >= @tempDate
        group by tblTimeanalysis.ta_prt_dt

        union

        select  'Sent' AS operation,count(tblresult.`sample#`) as output, DATE_FORMAT(tbltimeanalysis.ta_sent_dt, '%Y-%m-%d') as date 
        from tblresult inner join tbltimeanalysis on tblresult.batch = tbltimeanalysis.ta_batch
        where tbltimeanalysis.ta_sent_dt >= @tempDate
        group by tblTimeanalysis.ta_sent_dt) as result_set
        order by date desc;
        """
    
    sqlAcc = """
        select 'LAB' as operation, count(r.`sample#`) as Acc from tbltimeanalysis ta
            inner join tblresult r on r.batch = ta.ta_batch
            where r.`sample#` > 23110000 and ta.ta_ent_dt is not null and ta.ta_lab_dt is null and (ta.ta_complete is null or ta.ta_complete <> 1)
        union
        select 'QC' as operation, count(r.`sample#`) as Acc from tbltimeanalysis ta
            inner join tblresult r on r.batch = ta.ta_batch
            where r.`sample#` > 23110000 and ta.ta_lab_dt is not null and ta.ta_qc_dt is null and (ta.ta_complete is null or ta.ta_complete <> 1)
        union
        select 'Interp' as operation, count(r.`sample#`) as Acc from tbltimeanalysis ta
            inner join tblresult r on r.batch = ta.ta_batch
            where r.`sample#` > 23110000 and ta.ta_qc_dt is not null and ta.ta_int2_dt is null and (ta.ta_complete is null or ta.ta_complete <> 1)
        union
            select 'Print' as operation, count(r.`sample#`) as Acc from tbltimeanalysis ta
            inner join tblresult r on r.batch = ta.ta_batch
            where r.`sample#` > 23110000 and ta.ta_int2_dt is not null and ta.ta_prt_dt is null and (ta.ta_complete is null or ta.ta_complete <> 1)
        union
        select 'Sent' as operation, count(r.`sample#`) as Acc from tbltimeanalysis ta
            inner join tblresult r on r.batch = ta.ta_batch
            where r.`sample#` > 23110000 and ta.ta_prt_dt is not null and ta.ta_sent_dt is null and (ta.ta_complete is null or ta.ta_complete <> 1);

    """

    sqlAccDataEntery = """
        SELECT 
            (SELECT SUM(ic.IncomingAmount) 
             FROM tblincoming ic 
             WHERE ic.IncomingReceivedDate > '2024-01-01') 
            - 
            (SELECT COUNT(ir.result_id_id) 
             FROM tblincoming ic
             LEFT JOIN tblincomingresult ir on ir.incoming_id_id = ic.`No`
             INNER JOIN tblresult r on r.`sample#` = ir.result_id_id
             INNER JOIN tbltimeanalysis ta on ta.ta_batch = r.batch
             WHERE ic.IncomingReceivedDate > '2024-01-01' and ta.ta_ent_dt is not null) 
        AS dataAcc;
    """

    sqlAccFerro = """
        SELECT 
             count(`lab_do`.`sample#`) AS `ferro`
        FROM
            ((((`sample_lab_do_vw` `lab_do`
            LEFT JOIN `tblresult` `result` ON ((`result`.`sample#` = `lab_do`.`sample#`)))
            LEFT JOIN `tblunit` `unit` ON ((`unit`.`unitnumber` = `result`.`unitid`)))
            LEFT JOIN `tblcustomer` `cus` ON ((`cus`.`customer#` = `unit`.`cusnum`)))
            LEFT JOIN `tbltimeanalysis` `time_ana` ON ((`time_ana`.`ta_batch` = `result`.`batch`)))
        WHERE
            `result`.`drecieved`  > DATE_SUB(CURDATE(), INTERVAL 180 DAY)
                #AND (`lab_do`.`ta_status` = 'Interpret')
                AND `result`.`sample#` >= 24060000
                AND (`time_ana`.`ta_status` <> 'Finished')
                AND (`lab_do`.`FerroCheck` = 1)
                AND (`result`.`ferVol` IS NULL)
                AND (select id from focuslabs_resulttags rt where rt.result_id = result.`sample#` and tags_id = 41 limit 1) is null
                AND (select id from focuslabs_resulttags rt where rt.result_id = result.`sample#` and tags_id = 40 limit 1) is not null
        ORDER BY `result`.`drecieved`;
    """

    cursor.execute(sqlOutPut)
    data1 = cursor.fetchall() or [{'operation': 'DataEntry', 'output': 0, 'date': None},
                                  {'operation': 'Lab', 'output': 0, 'date': None},
                                  {'operation': 'QC', 'output': 0, 'date': None},
                                  {'operation': 'Interp', 'output': 0, 'date': None},
                                  {'operation': 'Print', 'output': 0, 'date': None},
                                  {'operation': 'Sent', 'output': 0, 'date': None}]

    cursor.execute(sqlAcc)
    data2 = cursor.fetchall() or [{'operation': 'LAB', 'Acc': 0},
                                  {'operation': 'QC', 'Acc': 0},
                                  {'operation': 'Interp', 'Acc': 0},
                                  {'operation': 'Print', 'Acc': 0},
                                  {'operation': 'Sent', 'Acc': 0}]

    cursor.execute(sqlAccDataEntery)
    data3 = cursor.fetchall() or {'dataAcc': 0}

    cursor.execute(sqlAccFerro) or {'ferro': 0}
    data4 = cursor.fetchall()
    conn.close()

    combile_data = combine_daily(data1,data2,data3,data4,data5)

    # return jsonify(data5)
    return jsonify(combile_data)

@app.route('/')
def index():
    return render_template('monitor804.html')

@app.route('/monitor804')
def monitor804():
    return render_template('monitor804.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/daily')
def daily():
    today = request.form.get('today', datetime.now().strftime('%d-%b-%Y')) #('%Y-%m-%d 00:00:00')
    return render_template('daily.html', today=today)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
