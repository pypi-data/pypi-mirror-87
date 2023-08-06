def distribute_file_request(user, token_info, body):
    from stratus_api.integrations.tasks.distributions import deliver_data_task
    from stratus_api.integrations.base import validate_platform_name
    from stratus_api.core.common import generate_random_id
    from stratus_api.core.exceptions import ApiError
    try:
        validate_platform_name(body['platform_name'])
    except ApiError as e:
        return dict(status=400, title='Bad Request', detail=e.args[0], type='about:blank'), 400
    else:
        job_uuid = generate_random_id()
        deliver_data_task.delay(**body, job_uuid=job_uuid)
        return dict(active=True, response=dict(job_uuid=job_uuid)), 200
