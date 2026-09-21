install := "node scripts/install-skills.js --claude"

# Work Claude
ncl:
    {{install}} \
        --exclude ship/repos/infra.md \
        --exclude merge-renovate-prs/repos/infra.md \
        --exclude parametric-3d-printing \
        --exclude amazon-review-writer
