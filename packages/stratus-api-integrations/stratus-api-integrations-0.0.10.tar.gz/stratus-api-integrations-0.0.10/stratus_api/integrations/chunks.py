from stratus_api.integrations.distribution import DELIVERED_SCHEMA

delivered_headers = [i['name'] for i in DELIVERED_SCHEMA]


def create_file_chunks(bucket_name, file_pattern, job_uuid, file_headers, integration_settings, delimiter='|'):
    from stratus_api.storage.gcs import download_from_storage, get_filenames_by_pattern
    import os
    import csv
    from datetime import datetime
    from stratus_api.integrations.cache import cache_data
    from stratus_api.integrations.cache import get_cached_data

    chunk_number = 0
    chunk_records = 0
    start = datetime.utcnow().timestamp()
    chunk_pointer = None
    chunk_writer = None
    delivered_pointer = None
    delivered_writer = None
    delivered_file_path = ''

    checkpoint = get_cached_data('checkpoint '+job_uuid)

    last_incomplete_file = None
    last_uploaded_line_number = None
    last_chunk_number = None
    last_chunk_size = None
    start_line_number = 0
    # file_path, chunk_number, chunk_records, line_number
    if checkpoint:
        arr = checkpoint.split('|')
        last_incomplete_file = arr[0]
        last_chunk_number = int(arr[1])
        last_chunk_size = int(arr[2])
        last_uploaded_line_number = int(arr[3])

    if last_uploaded_line_number:
        start_line_number = last_uploaded_line_number + 1

    file_names = get_filenames_by_pattern(bucket_name=bucket_name, file_path=file_pattern)

    reached_last_file = False
    reached_last_chunk = False

    for file_path in file_names:
        # fast forward the last incomplete file
        if last_incomplete_file:
            if file_path == last_incomplete_file:
                reached_last_file = True
            if not reached_last_file:
                continue

        local_path = download_from_storage(bucket_name=bucket_name, file_path=file_path, job_id=job_uuid)
        with open(local_path, 'rt') as f:
            reader = csv.reader(f, delimiter=delimiter)
            line_number = 0

            for row in reader:
                # fast forward to the line number
                if line_number < start_line_number:
                    line_number += 1
                    continue

                if last_chunk_size and not reached_last_chunk:
                    if last_chunk_size < integration_settings['chunk_size']:
                        chunk_number = last_chunk_number
                        chunk_records = last_chunk_size
                    else:
                        chunk_number = last_chunk_number + 1
                    reached_last_chunk = True

                chunk_file_path, chunk_pointer, chunk_writer = add_row_to_chunk(
                    job_uuid=job_uuid,
                    file_headers=file_headers,
                    row=row,
                    delimiter=delimiter,
                    chunk_number=chunk_number,
                    writer=chunk_writer,
                    pointer=chunk_pointer)

                delivered_file_path, delivered_pointer, delivered_writer = add_row_to_delivered_path(
                    job_uuid=job_uuid, file_headers=file_headers, row=row, pointer=delivered_pointer,
                    writer=delivered_writer,
                    chunk_number=chunk_number, timestamp=start)

                chunk_records += 1

                if chunk_records >= integration_settings['chunk_size']:
                    chunk_pointer.close()
                    chunk_pointer = None
                    delivered_pointer.close()
                    delivered_pointer = None
                    yield chunk_file_path, delivered_file_path, chunk_number

                    cache_data('checkpoint ' + job_uuid,
                               '{}|{}|{}|{}'.format(file_path, chunk_number, chunk_records, line_number))

                    start = datetime.utcnow().timestamp()
                    os.remove(chunk_file_path)
                    os.remove(delivered_file_path)
                    chunk_records = 0
                    chunk_number += 1

            line_number += 1


        os.remove(local_path)
    if chunk_records > 0:
        chunk_pointer.close()
        delivered_pointer.close()
        yield chunk_file_path, delivered_file_path, chunk_number

        os.remove(chunk_file_path)
        os.remove(delivered_file_path)


def add_row_to_chunk(row, chunk_number, job_uuid, file_headers, delimiter, pointer=None, writer=None):
    from stratus_api.core.settings import get_settings
    import os
    chunk_path_pattern = os.path.join(get_settings().get('upload_folder', '/apps/files/'),
                                      'upload-{job_uuid}-{chunk_number}.csv')
    chunk_path = chunk_path_pattern.format(chunk_number=chunk_number, job_uuid=job_uuid)

    return add_to_file(path=chunk_path, row=row, headers=file_headers, delimiter=delimiter, pointer=pointer,
                       writer=writer)


def add_row_to_delivered_path(row, chunk_number, job_uuid, file_headers, timestamp, pointer=None,
                              writer=None):
    from stratus_api.core.settings import get_settings
    import os
    delivered_path_pattern = os.path.join(get_settings().get('upload_folder', '/apps/files/'),
                                          'delivered-{job_uuid}-{chunk_number}.csv')
    delivered_path = delivered_path_pattern.format(chunk_number=chunk_number, job_uuid=job_uuid)
    for segment_uuid, operation in {k: row[idx] for idx, k in enumerate(file_headers) if
                                    k not in ['internal_user_id', 'external_user_id', 'id_type', 'policy_uuid',
                                              'created_ts'] and row[
                                        idx] != ''}.items():
        delivered_path, pointer, writer = add_to_file(
            path=delivered_path, row=[
                segment_uuid,
                row[file_headers.index('internal_user_id')],
                row[file_headers.index('external_user_id')],
                row[file_headers.index('id_type')],
                operation,
                job_uuid,
                row[file_headers.index('policy_uuid')],
                timestamp
            ], headers=delivered_headers, delimiter=',',
            pointer=pointer,
            writer=writer,
        )
    return delivered_path, pointer, writer


def add_to_file(path, row, headers, delimiter, pointer, writer):
    import csv
    if pointer is None:
        pointer = open(path, 'wt')
        writer = csv.writer(pointer, headers, delimiter=delimiter)
        writer.writerow(headers)
    writer.writerow(row)
    return path, pointer, writer
