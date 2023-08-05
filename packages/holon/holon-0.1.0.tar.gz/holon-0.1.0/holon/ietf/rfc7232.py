from holon.headers import Header

REFERENCE = "https://www.iana.org/go/rfc7232"


etag = Header(field_name="Etag", reference=REFERENCE)
last_modified = Header(field_name="Last-Modified", reference=REFERENCE)
if_match = Header(field_name="If-Match", reference=REFERENCE)
if_modified_since = Header(field_name="If-Modified-Since", reference=REFERENCE)
if_unmodified_since = Header(field_name="If-Unmodified-Since", reference=REFERENCE)
if_none_match = Header(field_name="If-None-Match", reference=REFERENCE)
