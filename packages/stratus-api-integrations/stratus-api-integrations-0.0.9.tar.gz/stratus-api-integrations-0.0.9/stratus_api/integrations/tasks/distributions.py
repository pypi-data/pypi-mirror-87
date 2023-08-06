from celery import shared_task


@shared_task(bind=True, )
def deliver_data_task(self, platform_name, bucket_name, file_pattern, segments, destination, file_headers, job_uuid,
                      id_types, operations,
                      **kwargs):
    from stratus_api.integrations.distribution import deliver_data
    return deliver_data(bucket_name=bucket_name, platform_name=platform_name, file_pattern=file_pattern,
                        job_uuid=job_uuid, segments=segments, destination=destination, file_headers=file_headers,
                        id_types=id_types, operations=operations)
