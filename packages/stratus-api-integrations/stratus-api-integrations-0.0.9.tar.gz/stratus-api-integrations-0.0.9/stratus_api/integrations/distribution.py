UPLOADED_FILE_GCS_PATH_FORMAT = "{year}/{month}/{day}/{hour}/{minute}/{job_uuid}/uploaded.{chunk_number}.csv"
DELIVERED_SCHEMA = [
    dict(name='segment_uuid', type='STRING'),
    dict(name='internal_user_id', type='STRING'),
    dict(name='external_user_id', type='STRING'),
    dict(name='id_type', type='STRING'),
    dict(name='operation', type='BOOLEAN'),
    dict(name='integration_job_uuid', type='STRING'),
    dict(name='policy_uuid', type='STRING'),
    dict(name='created_ts', type='TIMESTAMP'),
]

INTEGRATION_LOG = [
    dict(name='integration_job_uuid', type='STRING'),
    dict(name='segment_uuid', type='STRING'),
    dict(name='file_pattern', type='STRING'),
    dict(name='created_ts', type='TIMESTAMP'),
    dict(name='id_type', type='STRING', mode='REPEATED'),
    dict(name='operation', type='STRING', mode='REPEATED'),
    # dict(name='id_type', type='STRING'),
    # dict(name='operation', type='STRING'),
    dict(name='status', type='STRING'),
]


def log_integration(rows):
    from stratus_api.core.settings import get_settings
    from stratus_api.bigquery import stream_records_to_bigquery
    from stratus_api.bigquery.bigquery import create_table
    from stratus_api.events import publish_event, create_topic

    create_table(project_id=get_settings()['integration_log_project_id'],
                 table_name=get_settings()['integration_log_table'],
                 dataset_name=get_settings()['integration_log_dataset'],
                 schema=INTEGRATION_LOG)

    create_topic(get_settings()['integration_log_topic'])
    errors = stream_records_to_bigquery(rows=rows, row_ids=None,
                                        project_id=get_settings()['integration_log_project_id'],
                                        table_name=get_settings()['integration_log_table'],
                                        dataset_name=get_settings()['integration_log_dataset'])
    if errors:
        raise Exception(errors)

    for row in rows:
        publish_event(topic_name=get_settings()['integration_log_topic'], attributes=dict(),
                      event_type='integration', payload=row)


def compose_integration_logs(job_uuid, segments, file_pattern, time, id_types, operations, status):
    rows = []
    for segment in segments:
        rows.append(dict(
            integration_job_uuid=job_uuid,
            segment_uuid=segment['segment_uuid'],
            file_pattern=file_pattern,
            created_ts=time,
            id_type=id_types,
            operation=operations,
            status=status
        ))
    return rows


def deliver_data(job_uuid, bucket_name, file_pattern, platform_name, destination, file_headers, segments, id_types,
                 operations,
                 **kwargs):
    from stratus_api.integrations import get_integration_function, get_integration_settings
    from stratus_api.integrations.chunks import create_file_chunks
    from datetime import datetime
    from stratus_api.core.settings import get_settings

    start_time = datetime.utcnow()

    rows = compose_integration_logs(job_uuid, segments, file_pattern, int(start_time.timestamp()), id_types, operations,
                                    'started')

    log_integration(rows)

    distribute_file = get_integration_function(function_name='distribute_file')
    segment_mapping = {i['segment_uuid']: i for i in segments}
    for local_path, delivered_path, chunk_number, in create_file_chunks(
            bucket_name=bucket_name,
            file_pattern=file_pattern,
            integration_settings=get_integration_settings(),
            file_headers=file_headers,
            job_uuid=job_uuid):

        try:
            success = distribute_file(
                destination=destination, platform_name=platform_name, segments=segment_mapping, local_path=local_path,
                chunk_number=chunk_number, start_time=start_time, id_types=id_types, operations=operations
            )
        except Exception as e:
            success = False
            if get_settings()['environment'] not in {'qa', 'prod'}:
                raise e
        if success:
            load_delivered_data(
                local_path=delivered_path,
                job_uuid=job_uuid,
                chunk_number=chunk_number
            )

    end_time = datetime.utcnow()

    rows = compose_integration_logs(job_uuid, segments, file_pattern, int(end_time.timestamp()), id_types, operations,
                                    'completed')

    log_integration(rows)

    return close_delivery(job_uuid=job_uuid)


def load_delivered_data(job_uuid, local_path, chunk_number):
    from stratus_api.storage.gcs import upload_file_to_gcs
    from datetime import datetime
    now = datetime.utcnow()
    upload_file_to_gcs(
        local_path=local_path,
        file_path=UPLOADED_FILE_GCS_PATH_FORMAT.format(
            job_uuid=job_uuid,
            chunk_number=chunk_number,
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute

        )
    )
    return True


def close_delivery(job_uuid):
    return job_uuid, True
