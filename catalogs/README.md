# Catalog publishing

The local component directories are the source of truth during development.
After the GitHub repository and release tags exist, add catalog entries whose
download URLs point to versioned release archives, not mutable branches.

Recommended order:

1. Publish extension archives and catalog entries.
2. Publish the preset archive and catalog entry.
3. Publish the workflow archive and catalog entry.
4. Build and publish the bundle archive.
5. Test installation from a clean Spec Kit project.

Keep community catalogs discovery-only until the artifacts have been reviewed.
For an organization, host a private catalog and mark it install-allowed only
after verifying every component and release checksum.

