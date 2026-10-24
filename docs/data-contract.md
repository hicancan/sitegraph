# SitePackage

The single current package format is `sitegraph-package-v4`.

Required files:

- `site.json`
- `nav_tree.json`
- `homepage_modules.json`
- `sections.json`
- `list_pages.jsonl`
- `detail_pages.jsonl`
- `attachments.jsonl`
- `external_links.jsonl`
- `edges.jsonl`
- `manifest.json`

The manifest contains the format, site identity, crawl start/end, counts, and
factual errors. Errors may describe HTTP requests, parsing, pagination limits,
or an unrecognized page type.

`validate_site_package` rejects missing or extra entries, a wrong format,
identity mismatch, an artifact size/hash mismatch, duplicate record identity,
inconsistent manifest counts, or a schema-invalid record. There is no reader
for older formats.
