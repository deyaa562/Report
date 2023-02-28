import os

UUID = os.getenv('UUID', None)
if UUID is None:
    raise EnvironmentError(
        'UUID variable is missing make sure to add it to the .env file \n'
        'Example: UUID = "8cc58ff3-890e-4047-835c-05981dbbad2b"')

PROJECT = os.getenv('PROJECT', None)
if PROJECT is None:
    raise EnvironmentError(
        'PROJECT variable is missing make sure to add it to the .env file \n'
        'Example: PROJECT="rp_project"')

LAUNCH_NAME = os.getenv('LAUNCH_NAME')
