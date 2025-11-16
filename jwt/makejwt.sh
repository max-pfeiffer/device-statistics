#!/bin/bash

openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

b64url() {
    openssl base64 -A | tr '+/' '-_' | tr -d '='
}

HEADER=$(echo -n '{"alg":"RS256","typ":"JWT"}' | b64url)
PAYLOAD=$(echo -n "$1" | b64url)

DATA="${HEADER}.${PAYLOAD}"

SIGNATURE=$(printf '%s' "$DATA" \
  | openssl dgst -sha256 -sign private.pem \
  | b64url)

echo "${DATA}.${SIGNATURE}" | tee jwt.txt