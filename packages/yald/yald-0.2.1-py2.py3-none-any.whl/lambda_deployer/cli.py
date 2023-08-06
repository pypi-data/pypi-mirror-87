"""Console script for lambda_deployer."""
import argparse
import sys

from . import lambda_deployer


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--role-arn', default=None,
                   help='Role to assume for upload')
    p.add_argument('--bucket', default=None, help='Bucket to use for upload')
    p.add_argument('--function-name', required=True,
                   help='Name of function to update')
    p.add_argument('--filename', required=True, help='Filename to upload')
    p.add_argument('--key', default=None, help='Key to use in S3 bucket')
    p.add_argument('--env', '-E', action='append', help='key=value pairs to set in the environment')

    args = p.parse_args()

    if args.role_arn is not None:
        print(f'Assuming role {args.role_arn!r}')
        credentials = lambda_deployer.assume_role(args.role_arn)
    else:
        credentials = None

    env = {}
    for kv in args.env:
        k, v = kv.split('=', 1)
        env[k] = v

    lambda_deployer.update_lambda(
        function_name=args.function_name,
        bucket=args.bucket,
        key=args.key,
        filename=args.filename,
        credentials=credentials,
        env=env
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
