REM Upload to AWS
hugo -v --theme=mattgrogan
aws s3 sync --acl "public-read" --sse "AES256" public/ s3://mattgrogan.info
