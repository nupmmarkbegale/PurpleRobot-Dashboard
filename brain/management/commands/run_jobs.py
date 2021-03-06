import arff
import datetime
import json
import uuid
import math

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from brain.models import ReportJob
from data_sources.models import DataSource, DataReport

IGNORE_KEYS = [
    'bluetoothdevicesprobedevices_devices',
    'callhistoryfeaturewindows_windows',
    'robothealthprobe_pending_size',
    'robothealthprobe_time_offset_ms',
    'batteryprobe_icon_sub_small',
    'softwareinformationprobe_installed_app_count',
    'robothealthprobe_app_version_code',
    'robothealthprobe_pending_count',
    'robothealthprobe_app_version_name',
    'robothealthprobe_active_runtime',
    'robothealthprobe_clear_time',
    'robothealthprobe_external_free',
    'robothealthprobe_last_boot',
    'runningsoftwareprobe_running_task_count',
    'robothealthprobe_last_halt',
    'runningsoftwareprobe_running_task_count',
    'locationprobe_time_fix',
    'batteryprobe_temperature',
    'batteryprobe_voltage',
    'weatherundergroundfeature_wind_dir',
    'weatherundergroundfeature_pressure_trend',
    'weatherundergroundfeature_wind_degrees',
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        count = 0
        
        for job in ReportJob.objects.filter(job_start=None):
            params = json.loads(job.parameters)

            source_name = params['database']
            
            label_table_name = None
            label_column_name = None
            
            for key,value in params['label'].iteritems():
                label_table_name = key
                label_column_name = value
                
            job.job_start = datetime.datetime.now()
            job.save()
            
            # Add parameters for setting ranges...
            
            past = datetime.datetime(datetime.MINYEAR, 1, 1)
            future = datetime.datetime(datetime.MAXYEAR, 12, 31)
            
            for ds in DataSource.objects.filter(name__contains=source_name):
                table_names = ds.table_names()
    
                table_columns = {}
                
                for name in table_names:
                    table_columns[name] = ds.table_columns(name)
            
                points = ds.fetch_data(label_table_name, label_column_name, past, future)
    
                label_value_name = label_table_name + '_' + label_column_name
                
                categorical_values = {}
                rows = []
                row_keys = []
                
                for point in points:
                    row_dict = {}
                    
                    point_time = point[0]
                    label_value = point[1]

                    row_dict[label_value_name] = label_value
                    
                    for table, columns in table_columns.iteritems():
                        fetched = ds.fetch_nearest(point_time, table, columns)
                        
#                        if table == 'undefined':
#                            print('FETCHED: ' +  table + ' -- ' + str(columns) + ' -- ' + str(fetched))
                        
                        if len(fetched) > 0:
                            for i in range(0, len(columns)):
                                column = columns[i]
                                
                                column_key = slugify(table + '_' + column[0])
                                
                                if column_key in IGNORE_KEYS:
                                    pass
                                elif fetched[i] == None:
                                    pass
                                else:
                                    if row_keys.count(column_key) == 0:
                                        row_keys.append(column_key)
                                    
                                    if column[1] == 'boolean':
                                        column_values = set([None])
        
                                        try:
                                            column_values = categorical_values[column_key]
                                        except KeyError:
                                            categorical_values[column_key] = column_values
                                        
                                        str_value = slugify(unicode(str(fetched[i])))
                                        
                                        column_values.add(str_value)
                                        
                                    if fetched[i] == True or fetched[i] == False:
                                        row_dict[column_key] = slugify(unicode(str(fetched[i])))
                                    elif column[1] == 'text' or isinstance(fetched[i], str):
                                        try:
                                            item = json.loads(fetched[i])
                                            
                                            if isinstance(item, dict):
                                                for k,v in item.iteritems():
                                                    column_key = slugify(column_key + '_' + k)
                                                    
                                                    column_values = set([None])
                                                    
                                                    if row_keys.count(column_key) == 0:
                                                        row_keys.append(column_key)
            
                                                    try:
                                                        column_values = categorical_values[column_key]
                                                    except KeyError:
                                                        categorical_values[column_key] = column_values
                                            
                                                    str_value = slugify(unicode(v))
                                            
                                                    if str_value.strip() == '':
                                                        str_value = 'empty_string'
                                                        
                                                    print('K: ' + column_key + '; V: ' + str_value)
                                            
                                                    column_values.add(str_value)
    
                                                    row_dict[column_key] = str_value
                                            else:
                                                column_values = set([None])
        
                                                try:
                                                    column_values = categorical_values[column_key]
                                                except KeyError:
                                                    categorical_values[column_key] = column_values
                                        
                                                str_value = slugify(unicode(str(fetched[i])))
                                        
                                                if str_value.strip() == '':
                                                    str_value = 'empty_string'
                                        
                                                column_values.add(str_value)

                                                row_dict[column_key] = str_value
                                        except ValueError:
                                            str_value = slugify(unicode(fetched[i]))
 
                                            column_values = set([None])
    
                                            try:
                                                column_values = categorical_values[column_key]
                                            except KeyError:
                                                categorical_values[column_key] = column_values
                                    
                                            str_value = slugify(unicode(str(fetched[i])))
                                    
                                            if str_value.strip() == '':
                                                str_value = 'empty_string'

                                            column_values.add(str_value)
                                        
                                            row_dict[column_key] = str_value
                                    else:
                                        if fetched[i] != None:
                                            row_dict[column_key] = fetched[i]
                            
                    rows.append(row_dict)
    
                row_keys.sort()
                
                try:
                    row_keys.insert(0, row_keys.pop(row_keys.index(slugify(label_value_name))))            
                except ValueError:
                    pass
                    
                data = { 'relation': slugify(label_table_name + '_' + label_column_name), 'description': '' }
                
                attributes = []
                
                ignore = []
               
                var_type = params.get('type', 'nominal')
                var_label = slugify(label_table_name + '_' + label_column_name)
    
                for row_key in row_keys:
                    value_def = 'REAL'
                    
                    print(str(row_key) + ' --> ' + str(var_label))
                    
                    if row_key.lower() == var_label.lower() and var_type == 'numeric':
                        value_def = 'REAL'
                    elif row_key in categorical_values:
                        value_def = []
                        
                        for value in categorical_values[row_key]:
                            value_def.append(value)
                    
                    if ('_sensor_dt_' in row_key) == False and (value_def == 'REAL' or len(value_def) > 2 or (((None in value_def) == False) and len(value_def) > 1)):        
                        attributes.append((row_key, value_def))
                    else:
                        ignore.append(row_key)
                    
                data['attributes'] = attributes
                
                data_rows = []
                
                for row_dict in rows:
                    data_row = []
                    
                    for row_key in row_keys:
                        if ignore.count(row_key) == 0:
                            try:
                                if row_dict[row_key] in (float("inf"), float("-inf")):
                                    data_row.append(None)
                                else:
                                    data_row.append(row_dict[row_key])
                            except KeyError:
                                data_row.append(None)
                    
                    data_rows.append(data_row)
                    
#                print('ATTS: ' + str(attributes))
                
                data['data'] = data_rows
                job.result_file.save(str(job.pk) + '_' + str(uuid.uuid4()), ContentFile(arff.dumps(data)))
                job.result_type = 'text/arff'

            job.job_end = datetime.datetime.now()
            job.save()
            
            count += 1
            
        print(str(count) + ' job(s) run.')
