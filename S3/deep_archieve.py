#!/usr/bin/env python3
"""Copy S3 objects to DEEP_ARCHIVE.

Supports two modes:
1) In-place transition (same source and destination bucket).
2) Cross-bucket copy (source bucket to destination bucket).
"""

import argparse
import sys

import boto3
from botocore.exceptions import ClientError


DEFAULT_SOURCE_BUCKETS = [
    "aws-163544304364-cloudtrail",
    # "aws-163544304364-my-drive",
    # "aws-163544304364-repo",
    # "aws-163544304364-keys",
    # "aws-163544304364-billing",
    # "aws-163544304364-devbox",
    # "aws-163544304364-va-defense-force",
    # "aws-163544304364-ops",
]

ARCHIVAL_STORAGE_CLASSES = {
    "DEEP_ARCHIVE",
    "GLACIER",
    "GLACIER_IR",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy S3 objects with storage class DEEP_ARCHIVE."
    )
    parser.add_argument(
        "--source-bucket",
        nargs="*",
        help="One or more source S3 bucket names. If omitted, default list in script is used.",
    )
    parser.add_argument(
        "--source-prefix",
        default="",
        help="Optional source prefix to limit copied objects.",
    )
    parser.add_argument(
        "--destination-bucket",
        help="Destination bucket. Defaults to source bucket (in-place transition).",
    )
    parser.add_argument(
        "--destination-prefix",
        default="",
        help="Prefix to prepend to destination keys.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without changing objects.",
    )
    return parser.parse_args()


def build_destination_key(source_key: str, source_prefix: str, destination_prefix: str) -> str:
    if source_prefix and source_key.startswith(source_prefix):
        suffix = source_key[len(source_prefix) :]
    else:
        suffix = source_key
    return f"{destination_prefix}{suffix}"


def main() -> int:
    args = parse_args()
    s3 = boto3.client("s3")

    source_buckets = args.source_bucket or DEFAULT_SOURCE_BUCKETS
    source_prefix = args.source_prefix
    destination_prefix = args.destination_prefix

    processed = 0
    failed = 0
    skipped = 0

    paginator = s3.get_paginator("list_objects_v2")

    for source_bucket in source_buckets:
        destination_bucket = args.destination_bucket or source_bucket
        print(
            f"Starting copy: s3://{source_bucket}/{source_prefix} -> "
            f"s3://{destination_bucket}/{destination_prefix} (DEEP_ARCHIVE)"
        )

        pages = paginator.paginate(Bucket=source_bucket, Prefix=source_prefix)
        for page in pages:
            for obj in page.get("Contents", []):
                source_key = obj["Key"]
                storage_class = obj.get("StorageClass", "STANDARD")

                # Skip folder markers and objects already in an archive class.
                if source_key.endswith("/") and obj.get("Size", 0) == 0:
                    skipped += 1
                    continue
                if storage_class in ARCHIVAL_STORAGE_CLASSES:
                    skipped += 1
                    continue

                destination_key = build_destination_key(
                    source_key=source_key,
                    source_prefix=source_prefix,
                    destination_prefix=destination_prefix,
                )

                if args.dry_run:
                    print(f"[DRY-RUN] {source_bucket}/{source_key} -> {destination_bucket}/{destination_key}")
                    processed += 1
                    continue

                try:
                    s3.copy_object(
                        Bucket=destination_bucket,
                        Key=destination_key,
                        CopySource={"Bucket": source_bucket, "Key": source_key},
                        StorageClass="DEEP_ARCHIVE",
                        MetadataDirective="COPY",
                    )
                    print(f"Copied {source_bucket}/{source_key} -> {destination_bucket}/{destination_key}")
                    processed += 1
                except ClientError as error:
                    failed += 1
                    print(
                        f"Failed {source_bucket}/{source_key} -> {destination_bucket}/{destination_key}: "
                        f"{error.response.get('Error', {}).get('Message', str(error))}",
                        file=sys.stderr,
                    )

    print(f"Done. Processed: {processed}, Skipped: {skipped}, Failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())