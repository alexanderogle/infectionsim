import subprocess


def sync_s3(source, destination):
    _cmd = 'aws s3 sync {} {} --profile is'.format(
        source,
        destination
    )
    _ = subprocess.run(_cmd.split())
